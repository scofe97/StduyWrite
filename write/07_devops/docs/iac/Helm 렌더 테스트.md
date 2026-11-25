---
title: "Helm 렌더 테스트"
tags: [kubernetes, helm, testing, helm-template, helm-lint, helm-unittest, rbac, ci]
status: draft
source:
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_template.md
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_lint.md
  - https://github.com/helm-unittest/helm-unittest/blob/v1.0.3/README.md
related:
  - Helm%20values%EC%99%80%20%EB%A0%8C%EB%8D%94%20%EA%B2%80%EC%A6%9D.md
  - Helm%20%EC%B0%A8%ED%8A%B8%20%EC%9E%91%EC%84%B1.md
created: "2026-11-25"
updated: "2026-11-25"
---

# Helm 렌더 테스트

---

> 클러스터 없이 `helm template` 출력을 단언해 의도치 않은 매니페스트 변경을 막는 방법과 `helm lint`·`helm-unittest` 의 역할을 비교합니다.

## 학습 목표와 범위

> `helm lint` 로 거르지 못하는 값의 의미를 `helm template` 셸 단언과 `helm-unittest` 로 고정할 수 있습니다.

1. `helm template` 의 로컬 렌더링 원리와 `yq`·`grep` 단언 스크립트의 함정을 설명합니다.
2. `helm lint` 가 검사하는 형식 오류와 렌더 테스트가 고정하는 값의 의미를 구분합니다.
3. `helm-unittest` 의 테스트 파일 형식과 CI 도입 전 확인 사항을 판단합니다.

`helm lint` 와 `helm template` 셸 단언 출력은 Helm v4.1.4 와 `yq` 실측입니다. 다른 Helm 버전에서는 실행을 확인하지 않았습니다. `helm-unittest` 는 플러그인을 내려받지 않고 v1.0.3 태그의 공식 README 만 근거로 썼습니다.

차트 변경 검증 전체 순서는 [Helm 차트 작성](Helm%20%EC%B0%A8%ED%8A%B8%20%EC%9E%91%EC%84%B1.md)에서 다룹니다. `--show-only`·`lookup` 동작과 `values.schema.json` 검증은 [Helm values와 렌더 검증](Helm%20values%EC%99%80%20%EB%A0%8C%EB%8D%94%20%EA%B2%80%EC%A6%9D.md#4-렌더링-결과-사전-검증)을 참조합니다.



## 1. helm template 렌더 결과 단언

> 클러스터 없이 렌더링한 매니페스트를 `yq`·`grep` 으로 검사하면 별도 플러그인 없이도 RBAC 같은 보안 설정을 CI 에서 고정할 수 있습니다.

values 나 템플릿을 한 줄만 고쳐도 최종 매니페스트가 예상과 다르게 나옵니다. 조건문 하나가 틀리면 Role 에 권한이 추가되거나 Deployment 의 replica 수가 바뀝니다. 이런 변화는 템플릿 diff 리뷰에서 눈에 띄지 않고 렌더링 결과를 검사하기 전에는 드러나지 않습니다.

### 로컬 렌더링 원리와 단언 범위

`helm template` 은 차트를 로컬에서 렌더링해 매니페스트를 표준 출력으로 냅니다[^helm-template]. 클러스터에서 조회하는 값은 로컬에서 흉내 낸 값으로 채우고 서버 측 검증은 수행하지 않습니다[^helm-template].

이 동작 덕분에 kubeconfig 없이 CI 에서 돌릴 수 있습니다. 같은 입력에서 결과가 결정적이므로 단언 테스트에도 적합합니다. `--show-only`·`--set`·`--values` 사용법과 `lookup` 동작은 [Helm values와 렌더 검증](Helm%20values%EC%99%80%20%EB%A0%8C%EB%8D%94%20%EA%B2%80%EC%A6%9D.md#4-렌더링-결과-사전-검증)에서 다룹니다.

### 셸 단언 스크립트 예제

다음 스크립트는 Role 이 `configmaps` 에 `get`·`list` 만 허용하고 와일드카드(`*`) 권한이 없는지 확인합니다. 기본 `replicas` 가 2인지와 잘못된 `mode` 가 렌더링을 막는지도 함께 점검합니다.

```bash
#!/usr/bin/env bash
set -euo pipefail
chart="${1:-./demo}"
out="$(helm template demo "$chart")"
fail() { echo "FAIL: $1" >&2; exit 1; }

# 1. Role 은 get/list 만 허용한다
verbs="$(echo "$out" | yq -r 'select(.kind=="Role") | .rules[].verbs[]' | sort | paste -sd, -)"
[ "$verbs" = "get,list" ] || fail "Role verbs: $verbs"

# 2. 와일드카드 권한이 없다
if echo "$out" | yq -r 'select(.kind=="Role") | .rules[] | (.resources + .verbs)[]' | command grep -qx '\*'; then
  fail "wildcard in Role"
fi

# 3. 기본 replicaCount 가 2 이다
replicas="$(echo "$out" | yq -r 'select(.kind=="Deployment") | .spec.replicas')"
[ "$replicas" = "2" ] || fail "replicas: $replicas"

# 4. 잘못된 mode 는 렌더 자체가 실패한다
if helm template demo "$chart" --set mode=weird >/dev/null 2>&1; then
  fail "mode=weird must fail"
fi
echo "PASS"
```

정상 차트에서는 `PASS` 로 통과합니다. Role 의 `verbs` 에 `"*"` 를 넣은 사본(`./t3/demo`)에서는 다음과 같이 실패합니다(Helm v4.1.4 실측).

```bash
# 정상 차트 검증
./render-test.sh ./demo        # PASS, 종료 코드 0

# 와일드카드 권한을 넣은 사본 검증
./render-test.sh ./t3/demo     # FAIL: Role verbs: *,get,list, 종료 코드 1
```

4번 항목은 템플릿 안의 `fail` 함수가 잘못된 입력에서 실제로 렌더링을 중단하는지 검증합니다. `required` 와 `fail` 을 이용한 값 검증은 [Helm 템플릿 값 검증](Helm%20%ED%85%9C%ED%94%8C%EB%A6%BF%20%EA%B0%92%20%EA%B2%80%EC%A6%9D.md)에서 다룹니다.

### 셸 단언 작성 시 주의점

`yq` 문법은 도구 구현과 버전에 따라 다릅니다. 위 예제의 `select(.kind=="Role")` 은 멀티 문서 YAML 을 문서마다 걸러 내는 표현이며 실행에 쓴 `yq` 에서 동작했습니다.

출력 전체를 기준 파일과 `diff` 로 비교하는 **골든 파일** 방식은 만들기 쉽지만 라벨 하나만 바뀌어도 테스트가 깨집니다. 지키려는 핵심 속성만 골라 단언하면 변경에 덜 민감합니다.

`set -e` 가 켜진 셸에서는 `grep` 이 문자열을 찾지 못할 때 종료 코드 1 을 내어 스크립트가 즉시 끝납니다. 와일드카드처럼 없어야 정상인 값을 검사할 때는 위 예제의 2번 항목처럼 `if` 조건문 안에 넣습니다.

`lookup` 이나 `.Capabilities` 가 결과를 바꾸는 차트라면 대상 조건을 맞춰 주어야 합니다. 이 경우 `--api-versions` 와 `--kube-version` 플래그로 값을 지정합니다[^helm-template].



## 2. helm lint 와 렌더 테스트 구분

> `helm lint` 는 차트가 형식에 맞는지 보고, 렌더 테스트는 출력 값이 의도한 값인지 봅니다. lint 가 통과해도 위험한 매니페스트는 그대로 나옵니다.

`helm lint` 결과가 초록이면 차트가 안전하다고 착각하기 쉽습니다. Role 에 `"*"` 권한이 들어가도 YAML 문법과 차트 구조가 맞으면 `lint` 는 막지 못합니다.

`./t3/demo` 사본을 `helm lint --strict` 와 `./render-test.sh` 에 넣었을 때 결과가 갈립니다.
![helm lint 와 렌더 테스트의 오류 검출 분기](_assets/Helm%20%EB%A0%8C%EB%8D%94%20%ED%85%8C%EC%8A%A4%ED%8A%B8.lint-vs-render-test.svg)

그림 왼쪽 경로의 `helm lint` 는 문법·구조 규칙만 훑고 값의 의미 검사를 건너뛰어 종료 코드 0 으로 끝납니다. 오른쪽 경로의 `./render-test.sh` 는 첫 단언에서 `*,get,list` 를 잡아내고 즉시 종료 코드 1 로 멈춥니다. 뒤의 `mode=weird` 단언은 실행되지 않습니다.

### lint 검사 범위와 경고 수준

공식 문서에 따르면 `helm lint` 는 차트 경로를 받아 차트가 형식에 맞게 짜였는지(`well-formed`) 점검합니다[^helm-lint]. 설치를 실패하게 만드는 문제는 `[ERROR]` 로 보고하고 관례나 권고를 어기는 문제는 `[WARNING]` 으로 보고합니다[^helm-lint].

`--strict` 플래그를 주면 `[WARNING]` 도 실패로 바꿉니다[^helm-lint]. 다만 값의 의미는 여전히 `lint` 의 관심 밖입니다.

### 실측 비교와 values 전달

Role 에 `"*"` 권한을 넣은 같은 사본(`./t3/demo`)에 두 도구를 돌린 결과는 다음과 같습니다(Helm v4.1.4 실측).

```bash
# 엄격 모드로 차트 형식 점검
helm lint ./t3/demo --strict   # 종료 코드 0

# 렌더 결과 속성 단언 실행
./render-test.sh ./t3/demo     # FAIL, 종료 코드 1
```

템플릿의 `fail` 함수로 막아 둔 잘못된 `mode` 값도 `helm lint` 는 통과시켰습니다. 열어 본 공식 페이지(`helm_lint.md`)에는 종료 코드 정의가 없습니다. 따라서 위 종료 코드 0 은 공식 문서 근거가 아니라 Helm v4.1.4 실측 결과입니다.

`helm lint` 에 환경별 values 를 주려면 `-f` 또는 `--set` 을 붙입니다. 값을 주지 않으면 기본 `values.yaml` 로만 점검해 환경별 values 에서 터지는 오류를 놓칩니다.

두 도구는 대체 관계가 아니라 순서입니다. `helm lint` 로 `Chart.yaml` 형식과 템플릿 문법을 먼저 거르고 렌더 테스트로 출력 의도를 고정합니다. 전체 검증 흐름은 [Helm 차트 작성](Helm%20%EC%B0%A8%ED%8A%B8%20%EC%9E%91%EC%84%B1.md)을 참조합니다.



## 3. helm-unittest YAML 테스트

> `helm-unittest` 는 테스트를 YAML 로 적는 Helm 플러그인입니다. 셸 단언보다 선언적이어서 읽기 쉽지만 CI 에 플러그인 설치 단계가 추가됩니다.

단언 항목이 늘어나면 `yq` 경로와 `grep` 식이 쌓여 셸 스크립트를 읽기 어려워집니다. 어떤 속성을 고정하려는지 의도가 코드에 묻히고 실패 메시지도 매번 직접 만들어야 합니다.

### 설치와 테스트 파일 배치

`helm-unittest` 는 차트의 일관성을 유지하려고 YAML 로 단위 테스트를 적는 플러그인입니다[^helm-unittest]. 아래 명령은 v1.0.3 태그 README 의 형식을 옮긴 것이며 이 환경에서는 직접 설치하거나 실행하지 않았습니다.

```bash
# 플러그인 설치 (최신 바이너리를 helm 플러그인 디렉터리에 저장)
helm plugin install https://github.com/helm-unittest/helm-unittest.git

# 차트 테스트 실행
helm unittest $YOUR_CHART
```

테스트 묶음은 기본적으로 차트의 `tests/` 디렉터리에 `_test.yaml` 접미사로 둡니다[^helm-unittest].

### 단언 작성과 보안 매니페스트 고정

v1.0.3 README 의 시작 예제는 `isKind`·`matchRegex`·`equal` 단언을 씁니다[^helm-unittest].

```yaml
suite: test deployment
templates:
  - deployment.yaml
tests:
  - it: should work
    set:
      image.tag: latest
    asserts:
      - isKind:
          of: Deployment
      - matchRegex:
          path: metadata.name
          pattern: \-my-chart$
      - equal:
          path: spec.template.spec.containers\[0\].image
          value: nginx:latest
```

같은 형식으로 1절의 Role 단언을 옮기면 다음과 같은 모양이 됩니다. 아래 예시는 플러그인을 설치하지 않아 실행 검증을 거치지 않았고 README 의 `equal` 용법만 따라 적은 것입니다.

```yaml
suite: test role
templates:
  - role.yaml
tests:
  - it: should allow only get and list
    asserts:
      - isKind:
          of: Role
      - equal:
          path: rules[0].verbs
          value: ["get", "list"]
```

`hasDocuments` 같은 다른 단언의 사용법은 v1.0.3 README 시작 예제에 없어 다루지 않았습니다.

RBAC·NetworkPolicy·`securityContext` 같은 보안 매니페스트는 값 하나만 바뀌어도 보안 경계가 달라집니다. 애플리케이션 기능 테스트는 권한이 늘어나도 앱이 잘 동작하므로 이런 변화를 잡지 못합니다. 허용 목록을 테스트로 고정해 두면 권한을 넓히는 변경이 CI 에서 실패로 드러납니다.

### CI 파이프라인 연동과 주의점

v1.0.3 README 의 Docker 절은 JUnit 출력 옵션 `-o test-output.xml -t junit` 을 보입니다[^helm-unittest]. 아래 CI 단계 예시는 문법만 확인했고 실제 CI 서비스에서는 실행하지 않았습니다.

```yaml
steps:
  - run: helm lint ./chart --strict
  - run: ./render-test.sh ./chart
  - run: helm plugin install https://github.com/helm-unittest/helm-unittest.git
  - run: helm unittest ./chart -o test-output.xml -t junit
```

도입 전에는 네 가지를 확인합니다.

- 버전 미고정 위험: 설치 주소에 태그를 생략하면 CI 가 돌 때마다 최신 버전을 받아 결과가 흔들릴 수 있습니다. 설치 때 특정 버전을 고정하는 방법은 v1.0.3 README 에서 확인하지 못했습니다.
- Helm 4 호환 미확인: Helm v4.1.4 환경에서 v1.0.3 플러그인이 설치되고 동작하는지는 확인하지 않았습니다.
- 느슨한 단언 함정: `isKind` 나 `matchRegex` 만 쓰면 필드 값이 바뀌어도 통과하므로 고정하려는 값은 `equal` 로 적습니다.
- 외부 코드 실행 주의: 플러그인은 외부 저장소 코드를 내려받아 실행하므로 사내 CI 에 들일 때는 설치 전에 소스와 버전을 점검합니다.



## 결정 치트시트

> 목적과 CI 제약에 맞춰 도구와 단언 방식을 고르는 기준표입니다.

| 도구·방식 | 점검 대상 | 장점 | 제약과 주의점 |
|---|---|---|---|
| `helm lint --strict` | `Chart.yaml`, 템플릿 문법, `[WARNING]` 승격 | 추가 도구 없이 빠른 형식 점검 | Role `"*"` 나 `fail` 값 오류는 통과(v4.1.4 실측) |
| `helm template` + `yq`·`grep` | 렌더링된 매니페스트의 핵심 속성, `fail` 중단 | 플러그인 설치 없이 셸로 즉시 실행 | `yq` 버전별 문법 차이, `set -e` 에서 `grep` 처리 |
| `helm-unittest` | `tests/*_test.yaml` 의 선언적 YAML 단언 | 단언 의도가 읽기 쉽고 JUnit 출력 지원 | 외부 플러그인 설치 필요, Helm 4 호환 미확인 |
| 골든 파일 `diff` | 렌더링된 YAML 출력 전체 | 초기 작성이 간단함 | 라벨 하나만 바뀌어도 테스트가 깨짐 |



## 실무 적용 포인트

> PR 검증 단계에서 형식 점검 뒤에 속성 단위 렌더 테스트를 함께 돌립니다.

### 한 가지 실행

CI 파이프라인에 `helm lint ./chart --strict` 와 함께 속성 단언 스크립트를 추가합니다. RBAC 권한이나 replica 수처럼 바뀌면 안 되는 값만 고정합니다.

### 사용하는 상황

- Role·ClusterRole·NetworkPolicy 같은 보안 매니페스트의 허용 목록을 고정할 때
- 환경별 values 나 템플릿 조건문을 바꾼 뒤 의도하지 않은 필드 변경을 배포 전에 막을 때

### 주의할 점

- `helm lint` 에는 `-f` 나 `--set` 으로 환경별 values 를 넘겨야 기본값 이외의 설정 오류를 점검합니다.
- `helm template` 은 `lookup` 을 흉내 낸 값으로 처리하며 서버 검증을 하지 않습니다. 클러스터 의존 동작은 `--api-versions`·`--kube-version` 을 맞추거나 서버 dry-run 을 병행합니다.
- `helm-unittest` 를 CI 에 들일 때는 외부 플러그인 소스와 버전 고정 방식을 먼저 확인합니다.



## 면접 질문

> `helm lint` 와 렌더 테스트의 경계, 단언 방식 선택, 보안 매니페스트 검증에 관한 질문입니다.

1. `helm lint --strict` 가 통과했는데도 위험한 Role 권한이나 잘못된 값이 배포될 수 있는 이유는 무엇입니까?
2. `helm template` 출력 전체를 골든 파일과 `diff` 로 비교하는 방식보다 핵심 속성만 단언하는 방식이 유지보수에 유리한 이유는 무엇입니까?
3. `helm template` 셸 단언 대신 `helm-unittest` 플러그인을 도입할 때 얻는 이점과 CI 에서 챙겨야 할 제약은 무엇입니까?



## 정답 (자답 후 펼치기)

> 위 면접 질문 3개에 먼저 자답한 뒤 아래를 읽으세요.

### 정답 1 — helm lint 와 렌더 테스트의 경계

`helm lint` 는 차트가 형식에 맞게 짜였는지(`well-formed`)와 문법·관례 위반(`[ERROR]`·`[WARNING]`)만 점검하기 때문입니다. Role 에 `"*"` 권한이 들어가도 올바른 YAML 형식이면 `--strict` 를 붙여도 통과하므로, 값의 의도는 `helm template` 출력 단언이나 `helm-unittest` 같은 렌더 테스트로 막아야 합니다.

### 정답 2 — 속성 단언과 골든 파일 비교

골든 파일 방식은 렌더링된 출력 전체를 비교하므로 무해한 라벨이나 주석 한 줄만 바뀌어도 테스트가 깨집니다. 지키려는 핵심 속성(Role `verbs`, 기본 `replicas`, `fail` 실패 여부 등)만 골라 `yq`·`grep` 이나 `equal` 로 단언하면 변경에 덜 민감하게 의도를 고정할 수 있습니다.

### 정답 3 — helm-unittest 의 이점과 제약

`helm-unittest` 는 `tests/*_test.yaml` 에 선언적 YAML 단언과 JUnit 출력(`-o test-output.xml -t junit`)을 제공해 단언이 늘어날수록 셸 스크립트보다 읽기 쉽습니다. 대신 외부 플러그인을 내려받아 설치해야 하므로 설치 주소의 버전 고정 여부, 사용 중인 Helm 버전 호환성, 외부 코드 소스 점검이 CI 도입 전에 필요합니다.



## 참고 자료

[^helm-template]: Helm 공식 문서 `helm template` — 로컬 렌더링과 서버 측 검증 생략, `--show-only`·`--set`·`--values`·`--api-versions`·`--kube-version` 설명. <https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_template.md>
[^helm-lint]: Helm 공식 문서 `helm lint` — 형식 점검(`well-formed`) 범위, `[ERROR]`·`[WARNING]` 구분, `--strict` 설명. <https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_lint.md>
[^helm-unittest]: helm-unittest v1.0.3 README — YAML 단위 테스트 소개, `helm plugin install`, `tests/*_test.yaml`, `isKind`·`matchRegex`·`equal` 예제, `-o test-output.xml -t junit` JUnit 출력. <https://github.com/helm-unittest/helm-unittest/blob/v1.0.3/README.md>

- [Helm values와 렌더 검증](Helm%20values%EC%99%80%20%EB%A0%8C%EB%8D%94%20%EA%B2%80%EC%A6%9D.md) — `--show-only`·`lookup`·`--dry-run=server` 와 `values.schema.json` 검증
- [Helm 템플릿 값 검증](Helm%20%ED%85%9C%ED%94%8C%EB%A6%BF%20%EA%B0%92%20%EA%B2%80%EC%A6%9D.md) — `required`·`fail` 값 검증
- [Helm 차트 작성](Helm%20%EC%B0%A8%ED%8A%B8%20%EC%9E%91%EC%84%B1.md) — `lint` → `template` → 서버 검증 순서
