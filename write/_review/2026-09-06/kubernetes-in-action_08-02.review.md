---
title: "ConfigMap으로 설정 분리하기 — 복습 회차 2"
tags: [review, kubernetes, configmap]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/08-02.ConfigMap으로 설정 분리하기.md"
round: 2
round_date: 2026-09-06
prev_round_date: 2026-07-14
next_round_date: 2026-09-07
quality: 1
metacog:
  interview: 1
  speak_without_diagram: 1
  apply_to_other_env: 2
updated: 2026-09-06
---

# ConfigMap으로 설정 분리하기 — 복습 회차 2

> 원본: [ConfigMap으로 설정 분리하기](../../08_cloud/book/kubernetes-in-action/08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md)
> 회차 2 · 2026-09-06 · 이전 회차: 2026-07-14 (quality 3)
>
> **본 복습 규약 (Karpicke & Roediger 2006, testing effect):**
> 1. 각 질문에 *먼저 자기 답을 적어라* — 답을 보지 말 것
> 2. 자기 답 작성 후에만 `<details>` 의 정답을 열어라
> 3. 정답과 비교해 0~5 점 self-quality 점수를 매겨라
> 4. 회차 끝 종합 평가에서 다음 회차 날짜가 결정됨

## 학습 목표 (원본 §진입 인용)

> 이 문서를 읽고 나면 --from-literal·--from-file·--from-env-file로 ConfigMap을 만들고, configMapKeyRef·envFrom으로 환경변수에 주입하고 optional의 효과를 설명하며, ConfigMap 갱신이 실행 중인 Pod에 언제 반영되는지와 immutable을 쓰는 이유를 말할 수 있습니다.

회차 1에서 quality 3. 가장 낮았던 축은 **생성 구조 2/5**(`--from-file`과 `--from-env-file`을 원문과 치환의 차이로 혼동)였고, **주입 방식·누락 상태·갱신**이 각각 3/5였습니다. 다섯 질문을 그 넷에 배치했습니다.

## Q&A 5문제

### Q1. 정의 — 세 생성 옵션이 만드는 data 키 구조

**질문**: 같은 내용을 담은 파일 `application.env`(`APP_MODE=practice` / `LOG_LEVEL=info` / `SERVER_PORT=8080` 세 줄)를 `--from-file`로 넣을 때와 `--from-env-file`로 넣을 때, 생성되는 ConfigMap의 `data`가 각각 어떤 모양이 됩니까? 키가 몇 개이고 무엇입니까?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

<details>
<summary>정답 보기 (먼저 자기 답 적은 뒤)</summary>

- `--from-file` — 키는 **1개**, 파일명(`application.env`)이 키가 되고 **파일 내용 전체**가 값이 됩니다.
- `--from-env-file` — 키는 **3개**, 파일의 각 `KEY=value` 줄이 **별도 엔트리**가 됩니다 (`APP_MODE: practice`, `LOG_LEVEL: info`, `SERVER_PORT: "8080"`).

원본 §2의 dry-run 출력:

```yaml
# --from-file 결과: 파일명 하나가 키, 파일 전체가 값이 됩니다.
data:
  application.yml: |
    server:
      port: 8080
---
# --from-env-file 결과: 각 KEY=value 줄이 별도 엔트리가 됩니다.
data:
  APP_MODE: practice
  LOG_LEVEL: info
  SERVER_PORT: "8080"
```

회차 1에서 이 둘을 "원문이냐 치환이냐"의 차이로 잡았던 것이 오답의 원인이었습니다. **두 방식 모두 값을 치환하지 않습니다** (원본 §6 Q1). 갈리는 것은 치환 여부가 아니라 **키를 몇 개로 쪼개는가**입니다.

곁가지 — `--from-file`에 **디렉터리**를 주면 안의 각 파일이 별도 엔트리가 되고, `key=파일` 형태로 키를 직접 지정할 수도 있습니다. UTF-8이 아닌 바이트가 있으면 kubectl이 `binaryData`에 Base64로 넣습니다 (원본 §2).
</details>

**점수 (0~5)**: **0** (채점: Claude — 미답. "차이를 모르겠다". 회차 1 에서 2/5 로 최저였던 축이 0 으로 내려감)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — configMapKeyRef와 envFrom이 따로 있는 이유

**질문**: 두 필드가 나뉘어 있는 이유를 설명하십시오. 그리고 유일한 키가 `status-message`인 ConfigMap을 `envFrom`으로 주입하면 컨테이너에 어떤 환경변수가 생깁니까?

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

두 필드가 나뉜 이유는 **ConfigMap과 컨테이너 사이의 결합 범위**를 선택하기 위해서입니다 (원본 §3).

| 선택 기준 | configMapKeyRef | envFrom |
|---|---|---|
| 가져오는 범위 | 지정한 키 하나 | ConfigMap의 모든 키 |
| 환경변수 이름 | `env[].name`으로 변경 가능 | ConfigMap 키를 그대로 사용하며 prefix만 추가 가능 |
| 새 키가 추가될 때 | 매니페스트를 고치기 전에는 안 들어옴 | 매니페스트를 안 고쳐도 들어오지만 **다음에 만들어지는 파드부터** |

`status-message`를 `envFrom`으로 주입하면 **환경변수가 하나도 만들어지지 않습니다.** 대시가 들어간 이름은 유효한 환경변수 이름이 아니기 때문입니다 (원본 §3).

이 제약이 두 필드가 나뉜 이유를 선명하게 합니다 — `configMapKeyRef`는 `env[].name`으로 이름을 새로 지으므로 `status-message` 같은 키도 `INITIAL_STATUS_MESSAGE`로 받을 수 있습니다. `envFrom`은 키 이름을 그대로 쓰니 ConfigMap을 만들 때부터 이름을 맞춰 둬야 합니다.

우선순위도 함께 — envFrom은 리스트라 여러 ConfigMap을 조합할 수 있고, 같은 키가 있으면 **마지막 것이 우선**합니다. envFrom과 env를 함께 쓰면 **env가 우선**합니다 (원본 §3).
</details>

**점수 (0~5)**: **0** (채점: Claude — 미답. 더불어 Q1 재진술에서 `--from-file` 을 `--from-literal` 자리로 오인)

---

### Q3. 메커니즘 — 참조 대상이 없을 때 무엇이 어떤 상태가 되는가

**질문**: 컨테이너 둘을 가진 Pod가 있습니다. 한 컨테이너만 존재하지 않는 ConfigMap을 `optional` 없이 참조합니다. (가) Pod phase, (나) 참조 컨테이너의 waiting reason, (다) 다른 컨테이너의 상태, (라) `optional: true`였다면 무엇이 달라지는지를 각각 말하십시오.

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

(가) Pod phase는 **`Pending`** — Pod는 스케줄링됩니다 (원본 §6 Q3).
(나) 참조하는 컨테이너는 **`state.waiting.reason=CreateContainerConfigError`**로 기다립니다 (원본 §3·§6 Q3).
(다) 같은 Pod의 다른 컨테이너는 **문제가 된 ConfigMap을 참조하지 않는다면 실행될 수 있습니다.** 실습에서 READY가 `1/2`로 나왔습니다 (원본 §5).

```pseudocode
configmap-required   1/2   CreateContainerConfigError
independent => running
required => configmap "does-not-exist" not found
```

(라) `optional: true`면 ConfigMap이나 키가 없어도 **컨테이너가 실행되고 환경변수만 설정되지 않습니다.** 실습에서 `1/1 Running`이 됐고, 없는 변수를 `printenv`로 조회하니 종료 코드 1이었습니다 (원본 §3·§5).

회차 1에서 막힌 지점은 phase와 waiting reason을 **구분**하는 것이었습니다. 둘은 다른 층위입니다 — phase는 Pod 전체의 생애주기 단계, waiting reason은 개별 컨테이너가 왜 못 뜨는지의 이유입니다.
</details>

**점수 (0~5)**: **2** (채점: Claude — (다) 다른 컨테이너 정상 실행 정확, (라) 방향 맞음. (가)`Pending`·(나)`CreateContainerConfigError` 명명 미도달 — 회차 1 과 동일 지점. (라) 를 "공백 값"으로 답해 부재와 빈 문자열을 혼동)

---

### Q4. 적용 — LOG_LEVEL을 debug로 고쳤다, 세 경로는 각각 어떻게 되는가

**질문**: 운영 중인 Deployment(replica 2)가 `LOG_LEVEL`을 쓰고 있습니다. ConfigMap을 `info` → `debug`로 수정했습니다. (가) 환경변수로 주입한 경우, (나) 일반 ConfigMap 볼륨으로 마운트한 경우, (다) `subPath`로 파일 하나를 마운트한 경우 각각 어떻게 되며, 모든 인스턴스를 새 값으로 통일하려면 무엇을 합니까?

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

원본 §4의 표가 그대로 답입니다.

| 전달 방식 | 실행 중인 Pod에서 ConfigMap 수정 결과 | 새 설정을 적용하는 방법 |
|---|---|---|
| 환경변수 | 기존 값 유지 | Pod 롤링 교체 |
| 일반 ConfigMap 볼륨 | kubelet 동기화 후 파일 갱신 | 애플리케이션이 파일을 다시 읽음 |
| `subPath` 파일 마운트 | 파일이 갱신되지 않음 | Pod를 새로 생성 |

(가) 환경변수는 **kubelet이 컨테이너 시작 전에 값을 복사**해 실행 환경을 만듭니다. 실행 중인 프로세스의 환경은 ConfigMap과 계속 연결돼 있지 않으므로 원본을 수정해도 바뀌지 않습니다. 통일하려면 `kubectl rollout restart deployment/<이름>`.

여기서 **설정 혼재**가 생깁니다 — 교체 전에 스케일 아웃하거나 장애로 새 Pod가 만들어지면 기존 Pod는 `info`, 새 Pod는 `debug`를 씁니다. 실습에서 그대로 재현됐습니다 (원본 §5).

(나) 일반 볼륨은 kubelet 동기화 후 파일이 바뀝니다. **파드 교체나 컨테이너 재시작 없이 일어나므로 무중단이되 즉시는 아닙니다** — kind v1.35 실측으로 약 56초, 그동안 파드 UID와 `restartCount`는 그대로였습니다 (원본 §4). 다만 애플리케이션이 파일을 다시 읽지 않으면 실제 동작은 이전 설정을 계속 씁니다.

(다) `subPath`는 컨테이너 시작 시 선택한 파일 하나를 고정 마운트하므로 **갱신되지 않습니다.** 실습에서 일반 마운트는 `after`, `subPath`는 `before`였습니다 (원본 §5).

**원문 밖 보충 아님 — 원본 §Spring 관점**: "파일 갱신은 무중단"과 "그 값을 앱이 런타임에 받아들인다"는 별개입니다. `server.port`는 톰캣이 부팅하며 소켓을 bind하므로 파일이 바뀌어도 재기동이 필요하고, 로그 레벨·기능 플래그는 요청마다 다시 읽히므로 무중단 반영됩니다.
</details>

**점수 (0~5)**: **3** (채점: Claude — (가) 환경변수는 파드 재생성 필요 정확. (나) 파일 갱신은 맞으나 "자동으로 읽힌다"로 앱 재읽기 필요를 놓침. (다) subPath 개념 미보유로 일반 볼륨과 동일하다고 답함 — 회차 1 과 같은 지점)

---

### Q5. 함정 — 넣었는데 없다, 로그에도 없다

**질문**: ConfigMap에 분명히 키를 넣고 `envFrom`으로 주입했는데 컨테이너에 그 환경변수가 없습니다. 파드는 정상적으로 떴고 로그에도 오류가 없습니다. 원인이 무엇이며 어떻게 확인합니까? 그리고 `immutable: true`는 무엇을 막고 값을 바꾸려면 어떻게 합니까?

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

**원인**: 유효하지 않은 환경변수 이름의 키는 **오류 없이 건너뛰어지고 파드는 정상적으로 뜹니다.** 실패가 조용합니다 (원본 §3).

**확인**: 파드 이벤트의 `InvalidVariableNames`를 봅니다.

```bash
kubectl describe pod <pod-name> | grep -A2 InvalidVariableNames
```

**immutable**: 한 번 설정하면 `data`와 `binaryData`를 바꿀 수 없고 `immutable` 필드를 다시 제거할 수도 없습니다. API 서버가 `field is immutable`로 요청을 거부합니다 (원본 §4·§5). 사용자의 실수를 막을 뿐 아니라 kubelet이 변경 감시를 유지할 필요가 없어 API 서버 부하도 줄입니다.

값을 바꾸려면 **새 이름의 ConfigMap을 만들고 Deployment의 참조 이름을 변경해 롤링 업데이트를 일으킵니다.** 운영에서는 `kiada-config-8f3a2b`처럼 내용 해시를 이름에 넣고, Kustomize의 `configMapGenerator`가 이 이름 생성과 참조 변경을 자동화합니다 (원본 §Spring 관점).

삭제도 같은 결이 있습니다 — ConfigMap을 지우면 환경변수로 이미 받은 실행 중 Pod는 계속 돌지만, optional이 아닌 참조를 가진 **새 Pod는 시작하지 못합니다** (원본 §4).
</details>

**점수 (0~5)**: **1** (채점: Claude — immutable 은 이름 뜻 재진술까지. 새 오브젝트 생성이라는 변경 경로와 envFrom 의 조용한 실패·InvalidVariableNames 이벤트 미도달)

## 회차 종합 평가

### 1. SM-2 quality 점수 (0~5)

**quality**: **1** (Q1~Q5 = 0·0·2·3·1, 평균 1.2. 회차 1 의 3 에서 **퇴행**)

### 2. 3축 메타인지 자가평가 (1~5)

| 축 | 점수 (1~5) | 메모 |
|----|----------|------|
| A. 면접 답변 가능성 | 1 | 생성 옵션·주입 필드 모두 미답 |
| B. 그림 없이 말로 설명 | 1 | `Pending`·`CreateContainerConfigError`·`subPath` 명명 전부 미도달 |
| C. 다른 환경 응용 | 2 | 환경변수 재기동 필요는 자력. subPath 심링크 교체 메커니즘은 설명 후 정확히 재구성 |

**평균**: **1.33**

### 3. 다음 회차 결정

회차 2 기준: quality 5 → +30일 · 4 → +14일 · 3 → +7일 · 0~2 → +1일.

**다음 회차 날짜**: **2026-09-07** (회차 2 · quality 1 → +1일)

### 3-1. 회차 소견 (2026-09-06)

회차 1(2026-07-14) quality 3 → 회차 2 quality 1 로 **퇴행**. 51일 연체 후 결과다. 회차 1 에서 최저였던 **생성 구조**(2/5)가 0 으로 내려간 것이 가장 뚜렷하다.

갈리는 축은 **명명**이다. 개념 질문(환경변수는 파드 재생성이 필요한가, subPath 는 왜 안 바뀌는가)에는 답하거나 설명 후 정확히 재구성했지만, `Pending`·`CreateContainerConfigError`·`InvalidVariableNames`·`--from-env-file` 처럼 **화면에서 읽어야 하는 글자**는 하나도 나오지 않았다. 08-01 과 같은 패턴이다.

다음 학습은 본문 재독이 아니라 **kubectl 출력 화면을 보고 이름을 대는 과제**로 짠다 — `kubectl get pod` 의 STATUS 열, `kubectl describe` 의 Events 열, `kubectl create configmap --dry-run=client -o yaml` 의 data 블록 셋.

### 4. 졸업 판정

- [ ] 본 회차 quality ≥ 4
- [ ] 3축 메타인지 평균 ≥ 3.6
- [ ] _mistakes.md 미해결 패턴 0개

### 5. 오답 박제 → _mistakes.md

quality ≤ 3인 질문을 `write/08_cloud/book/kubernetes-in-action/_mistakes.md`에 append.

## 관련 자료

- [원본 학습 문서](../../08_cloud/book/kubernetes-in-action/08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md)
- 이전 회차: [회차 1 (2026-07-14)](../2026-07-14/kubernetes-in-action_08-02.review.md)
- 실습: `study/k8s_in_action/08-configuring-apps/configmap/`
