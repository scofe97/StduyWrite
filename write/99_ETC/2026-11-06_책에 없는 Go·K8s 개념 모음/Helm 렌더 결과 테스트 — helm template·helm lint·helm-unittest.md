---
title: "Helm 렌더 결과 테스트 — helm template·helm lint·helm-unittest"
tags: [helm, kubernetes, testing, helm-template, helm-lint, helm-unittest, rbac, ci]
status: draft
source:
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_template.md
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_lint.md
  - https://github.com/helm-unittest/helm-unittest/blob/v1.0.3/README.md
updated: 2026-11-06
---

# Helm 렌더 결과 테스트 — helm template·helm lint·helm-unittest

---

> 임시 참고 문서입니다. 정본은 나중에 따로 만듭니다.

차트의 렌더 결과를 테스트로 고정하는 세 가지 도구를 비교합니다. 셸로 단언하는 `helm template` 렌더 테스트, 형식 점검인 `helm lint`, YAML 로 테스트를 적는 `helm-unittest` 플러그인입니다.

셸 테스트와 lint 결과는 Helm v4.1.4 와 yq 로 직접 돌린 출력입니다. `helm-unittest` 는 플러그인을 내려받지 않아 README 문장만 근거로 썼고, 직접 돌려 보지 못한 부분을 문서 끝에 적었습니다.

## 1. helm template 렌더 결과를 셸로 단언

> 클러스터 없이 렌더한 매니페스트를 `yq`·`grep` 으로 검사하면 별도 플러그인 없이 렌더 테스트가 됩니다. RBAC 같은 보안 매니페스트가 의도대로 나오는지 CI 에서 고정하는 용도에 맞습니다.

### 차트 변경이 매니페스트를 조용히 바꾸는 문제

values 하나나 템플릿 한 줄을 고치면 최종 매니페스트가 예상과 다르게 바뀔 수 있습니다. 조건문 하나가 틀리면 Role 에 권한이 늘거나 Deployment 의 replica 수가 달라집니다. 이런 변화는 리뷰에서 diff 로 눈에 띄지 않고, 렌더 결과를 보기 전에는 알 수 없습니다.

### 동작 원리

`helm template` 은 차트를 로컬에서 렌더해 매니페스트를 표준 출력으로 냅니다. 공식 문서의 설명입니다.

> "Render chart templates locally and display the output."

클러스터에서 가져오는 값은 흉내 낸 값으로 채워지고, 서버 쪽 검증은 일어나지 않습니다.

> "Any values that would normally be looked up or retrieved in-cluster will be faked locally."

> "Additionally, none of the server-side testing of chart validity (e.g. whether an API is supported) is done."

그래서 kubeconfig 없이 CI 에서 돌릴 수 있고, 결과가 결정적이어서 단언하기 좋습니다. 대신 `lookup` 에 의존하는 값이나 API 지원 여부는 이 테스트로 검증되지 않습니다. 특정 파일만 보고 싶으면 `--show-only`, 값을 바꿔 보려면 `--set`·`--values` 를 씁니다.

### 최소 예제

Role 이 `configmaps` 에 `get`·`list` 만 허용하는지 고정하는 스크립트입니다.

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

정상 차트에서는 통과하고, Role 의 verbs 에 `"*"` 를 몰래 넣은 사본에서는 이렇게 실패합니다(실측).

```bash
./render-test.sh ./demo        # PASS, 종료 코드 0
./render-test.sh ./t3/demo     # FAIL: Role verbs: *,get,list, 종료 코드 1
```

4번 항목은 `fail` 이 실제로 렌더를 막는지 확인하는 단언입니다. `fail` 은 같은 폴더의 값 검증 문서에서 다룹니다.

### 흔한 함정

- `yq` 문법은 도구 버전에 따라 다릅니다. 이 문서의 `select(.kind=="Role")` 형태는 멀티 문서 YAML 을 문서마다 걸러 내는 표현으로, 실행한 yq 에서 동작했습니다.
- 출력 전체를 파일과 `diff` 로 비교하는 골든 파일 방식은 만들기 쉽지만, 라벨 하나만 바뀌어도 깨집니다. 지키려는 속성만 단언하면 변경에 덜 민감합니다.
- `set -e` 아래에서 `grep` 이 못 찾으면 종료 코드 1 로 스크립트가 끝납니다. 일부러 없음을 확인할 때는 위 예제처럼 `if` 안에 넣습니다.
- `lookup` 이나 `.Capabilities` 가 결과를 바꾸는 차트는 `--api-versions`·`--kube-version` 플래그로 조건을 맞춰 줍니다.

### 공식 문서 근거

- 로컬 렌더와 서버 검증 생략, `--show-only`·`--set`·`--values` 설명 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_template.md



## 2. helm lint 와 렌더 테스트의 역할 차이

> `helm lint` 는 차트가 형식에 맞는지 보고, 렌더 테스트는 결과가 의도한 값인지 봅니다. lint 가 통과해도 위험한 매니페스트는 그대로 나올 수 있습니다.

### lint 만 믿을 때 생기는 문제

lint 가 초록이면 안전하다고 생각하기 쉽습니다. 하지만 lint 가 보는 것은 차트가 잘 짜였는지입니다. 문서가 설명하는 범위는 이렇습니다.

> "This command takes a path to a chart and runs a series of tests to verify that the chart is well-formed."

문서에 따르면 설치를 실패하게 만드는 문제는 `[ERROR]`, 관례나 권고를 어기는 문제는 `[WARNING]` 으로 보고합니다. `--strict` 는 경고를 실패로 바꿉니다.

> `--strict`: "fail on lint warnings"

값의 의미는 lint 의 관심 밖입니다. Role 에 `"*"` 권한이 들어간 차트도 형식은 올바른 YAML 이기 때문입니다.

### 실측 비교

같은 위험한 사본에 두 도구를 돌렸습니다(Helm v4.1.4).

```bash
helm lint ./t3/demo --strict   # 종료 코드 0
./render-test.sh ./t3/demo     # FAIL, 종료 코드 1
```

앞 문서에서 본 것처럼 `fail` 로 막은 잘못된 `mode` 값도 lint 는 통과시켰습니다. lint 는 `Chart.yaml` 형식이나 템플릿 문법 오류를 잡는 첫 관문으로 두고, 값의 의미는 렌더 테스트가 맡습니다.

### 흔한 함정

- `helm lint` 의 종료 코드 정의는 열어 본 공식 페이지에 없습니다. 위 0 은 실측일 뿐 문서 근거가 아닙니다.
- lint 에 values 를 주려면 `-f`·`--set` 을 줍니다. values 를 주지 않으면 기본값으로만 점검해, 환경별 values 에서 터지는 오류를 놓칩니다.
- 두 도구는 대체 관계가 아니라 순서입니다. lint 로 형식을 거르고, 렌더 테스트로 의도를 고정합니다.

### 공식 문서 근거

- lint 의 점검 범위와 `[ERROR]`·`[WARNING]`, `--strict` — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_lint.md



## 3. helm-unittest 로 YAML 테스트 작성

> `helm-unittest` 는 테스트를 YAML 로 적는 플러그인입니다. 셸 단언보다 선언적이어서 읽기 쉽지만, 플러그인 설치가 CI 에 하나 더 늘어납니다.

### 셸 테스트가 커질 때 생기는 문제

단언이 늘면 `yq` 경로와 `grep` 식이 쌓여 스크립트가 읽기 어려워집니다. 어떤 속성을 고정하려는지가 코드에 묻히고, 실패 메시지도 직접 만들어야 합니다. 테스트 형식이 정해진 도구가 있으면 이 비용을 줄입니다.

### 동작 원리

README 는 이 플러그인을 이렇게 소개합니다.

> "Unit test for _helm chart_ in YAML to keep your chart consistent and robust!"

설치와 실행은 아래 두 줄입니다. 설치 명령은 최신 바이너리를 helm 플러그인 디렉터리에 둔다고 README 가 설명합니다.

```bash
helm plugin install https://github.com/helm-unittest/helm-unittest.git
helm unittest $YOUR_CHART
```

테스트 묶음은 기본적으로 차트의 `tests/` 디렉터리에 `_test.yaml` 접미사로 둡니다.

> "default placed under the `tests/` directory of the chart with suffix `_test.yaml`."

### 예제

README 의 시작 예제에서 쓰는 단언은 `isKind`·`matchRegex`·`equal` 입니다.

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

같은 형식으로 위 1절의 Role 단언을 옮기면 이런 모양이 됩니다. 직접 돌려 보지는 못했고 README 의 `equal` 용법을 따라 쓴 것입니다.

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

### 보안 매니페스트를 테스트로 고정하는 이유

RBAC·NetworkPolicy·securityContext 같은 매니페스트는 값 하나가 바뀌면 보안 경계가 바뀝니다. 앱 기능 테스트는 이런 변화를 잡지 못합니다. 권한이 늘어도 앱은 잘 돌기 때문입니다. 허용 목록을 테스트로 적어 두면, 권한을 늘리는 변경이 CI 에서 실패로 드러나 리뷰에서 의도를 설명해야 합니다.

### CI 에서 돌리는 법

README 의 Docker 절에는 CI 검증을 위해 JUnit 출력으로 돌리는 예가 있습니다. 옵션은 `-o test-output.xml -t junit` 입니다. CI 단계는 이렇게 이어 붙입니다(문법만 확인한 예시입니다).

```yaml
steps:
  - run: helm lint ./chart --strict
  - run: ./render-test.sh ./chart
  - run: helm plugin install https://github.com/helm-unittest/helm-unittest.git
  - run: helm unittest ./chart -o test-output.xml -t junit
```

### 흔한 함정

- 플러그인 설치 주소를 태그 없이 쓰면 CI 가 돌 때마다 최신 버전을 받아 결과가 흔들릴 수 있습니다. 설치 때 특정 버전을 고정하는 방법은 열어 본 README 에서 확인하지 못했습니다.
- 이 환경의 Helm v4.1.4 에서 플러그인이 설치되고 동작하는지는 확인하지 못했습니다. README 페이지는 v1.0.3 태그 기준입니다.
- `isKind` 나 `matchRegex` 만 쓰면 값이 틀려도 통과합니다. 고정하려는 값은 `equal` 로 정확히 적습니다.
- 플러그인은 외부 코드를 내려받아 실행합니다. 사내 CI 에 들일 때는 설치 전에 소스와 버전을 점검합니다.

### 공식 문서 근거

- 소개·설치·`tests/*_test.yaml` 위치·예제·JUnit 출력 — https://github.com/helm-unittest/helm-unittest/blob/v1.0.3/README.md



## 확인하지 못한 것

- `helm-unittest` 를 설치해 돌려 보지 않았습니다. 3절의 두 번째 YAML 은 README 용법을 따라 쓴 것이며 실행 검증을 거치지 않았습니다.
- 플러그인 버전 고정 설치 방법과 Helm 4 호환 여부는 열어 본 README 에서 확인하지 못했습니다.
- `helm lint` 종료 코드에 대한 공식 문서 문장은 열어 본 페이지에 없었습니다. 종료 코드는 모두 v4.1.4 실측입니다.
- `hasDocuments` 같은 다른 단언의 사용법은 README 시작 예제에 없어 다루지 않았습니다.
- CI 예시 YAML 은 문법만 확인했고 실제 CI 서비스에서 실행하지 않았습니다.



## 관련 문서

- [Helm 고급](../../08_cloud/docs/helm/01-02.Helm 고급.md) — `helm template` 워크플로우와 `kubeconform`
- [Helm 기초](../../08_cloud/docs/helm/01-01.Helm 기초.md) — `helm template` 과 `--dry-run` 차이
