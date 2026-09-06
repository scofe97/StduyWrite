---
title: "command·args와 환경변수 — 복습 회차 2"
tags: [review, kubernetes, command, args, environment-variable]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/08-01.command·args와 환경변수.md"
round: 2
round_date: 2026-09-06
prev_round_date: 2026-07-13
next_round_date: 2026-09-07
quality: 1
metacog:
  interview: 1
  speak_without_diagram: 2
  apply_to_other_env: 1
updated: 2026-09-06
---

# command·args와 환경변수 — 복습 회차 2

> 원본: [command·args와 환경변수](../../08_cloud/book/kubernetes-in-action/08-01.command%C2%B7args%EC%99%80%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98.md)
> 회차 2 · 2026-09-06 · 이전 회차: 2026-07-13 (quality 3)
>
> **본 복습 규약 (Karpicke & Roediger 2006, testing effect):**
> 1. 각 질문에 *먼저 자기 답을 적어라* — 답을 보지 말 것
> 2. 자기 답 작성 후에만 `<details>` 의 정답을 열어라
> 3. 정답과 비교해 0~5 점 self-quality 점수를 매겨라
> 4. 회차 끝 종합 평가에서 다음 회차 날짜가 결정됨

## 학습 목표 (원본 §진입 인용)

> 이 문서를 읽고 나면 Dockerfile의 ENTRYPOINT·CMD가 Pod 매니페스트의 command·args에 어떻게 대응하는지 설명할 수 있습니다. 이미지를 다시 빌드하지 않고 실행 명령·인자·환경변수를 바꾸며 $(VAR_NAME) 참조가 해석되지 않는 세 가지 상황도 구분할 수 있습니다.

회차 1에서 quality 3. 막힌 축은 **exec의 프로세스 교체**(확장 주체 3/5), **미정의 변수 조회의 종료 코드**(적용 3/5), **종료 신호 전달 과정**(함정 3/5) 셋이었습니다. 이번 회차의 다섯 질문은 그 셋을 정면으로 겨눕니다.

## Q&A 5문제

### Q1. 정의 — 해석 못 한 참조와 없는 변수는 어떻게 다른가

**질문**: 다음 두 상황의 결과를 각각 한 줄로 말하십시오. (가) Pod의 `env` 목록에서 뒤에 선언된 변수를 `$(LATE)`로 참조했다. (나) 컨테이너 안에서 `printenv UNKNOWN`을 실행했고 `UNKNOWN`은 어디에도 없다.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

<details>
<summary>정답 보기 (먼저 자기 답 적은 뒤)</summary>

(가) **참조 문자열이 그대로 남습니다.** `env[].value`의 `$(VAR_NAME)`은 같은 컨테이너의 env 목록에서 *먼저 정의된* 변수와 쿠버네티스가 주입한 Service 환경변수만 해석합니다. 해석하지 못하면 값이 비는 것이 아니라 `$(LATE)`라는 문자 그대로 남습니다 (원본 §4).

실측 출력 — `MESSAGE=early=kiada, late=$(LATE), image=$(IMAGE_ONLY), escaped=$(EARLY)` (원본 §7).

(나) **출력 없이 종료 코드 1을 반환합니다.** 변수가 존재하지 않으므로 `printenv`가 실패합니다 (원본 §7 실측 `exit=1`).

둘의 차이는 *누가 못 찾았는가*입니다 — (가)는 kubelet이 확장 단계에서 못 찾아 문자열을 보존한 것이고, (나)는 실행 중 프로세스의 환경에 그 이름이 아예 없는 것입니다.

**원문 밖 보충**: 문자 그대로 `$(VAR_NAME)`을 담고 싶으면 `$$(VAR_NAME)`으로 달러를 겹칩니다 (원본 §4에 명시돼 있으므로 원문 범위 안).
</details>

**점수 (0~5)**: **2** (채점: Claude — (가) 미해결 이유는 정확. 결과가 "문자열 그대로 보존"임을 미기술, (나) 종료 코드 1 누락 — 회차 1과 같은 자리)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — sh -c로 JVM을 띄울 때 exec를 왜 붙이는가

**질문**: `command: ["sh", "-c"]` / `args: ['java $JAVA_OPTS -jar app.jar']`처럼 셸을 거쳐 JVM을 실행합니다. 여기에 `exec`를 붙여야 하는 이유는 무엇이며, 붙이지 않으면 운영에서 무엇이 깨집니까?

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

`exec`가 셸을 JVM으로 **교체**하면 JVM이 PID 1이 됩니다. Kubernetes의 종료 신호가 JVM에 직접 도착하므로 Spring의 graceful shutdown과 종료 훅이 실행될 수 있습니다 (원본 §8 Q3).

붙이지 않으면 셸이 PID 1로 남습니다. **Kubernetes의 종료 신호는 우선 PID 1인 셸에 도착하므로, 셸이 신호를 자식에게 전달하지 않으면 애플리케이션이 정상 종료 절차를 실행하지 못할 수 있습니다** (원본 §6).

애초에 셸을 거치는 이유도 함께 짚습니다 — 이미지의 `JAVA_OPTS`처럼 셸이 해석해야 하는 변수를 쓰려면 `sh -c`가 필요합니다. 즉 "변수 확장은 셸에게 맡기되, 확장이 끝난 뒤에는 셸을 남겨 두지 않는다"가 이 조합의 의도입니다 (원본 §6).
</details>

**점수 (0~5)**: **1** (채점: Claude — exec 를 command/args 필드 문제로 오인. 셸 내장 명령이라는 것도, PID 1 교체·SIGTERM 전달도 미도달. 회차 1(3/5)에서 **퇴행**)

---

### Q3. 메커니즘 — 그림 없이 프로세스 트리로 설명할 수 있는가

**질문**: `sh -c 'sleep 3600 & wait'`와 `sh -c 'exec sleep 3600'`를 각각 컨테이너의 최상위 명령으로 두고 `ps -o pid,ppid,comm`을 찍었습니다. 두 출력의 PID·PPID를 말로 설명하고, `exec`가 프로세스에 실제로 무슨 일을 하는지 설명하십시오.

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

원본 §6 실측:

```pseudocode
# exec 없음: sh -c 'sleep 3600 & wait'
PID   PPID  COMMAND
1     0     sh
11    1     sleep

# exec 사용: sh -c 'exec sleep 3600'
PID   PPID  COMMAND
1     0     sleep
```

- exec 없음 — `sh`가 PID 1이고 `sleep`은 PID 11에 PPID 1입니다. PPID가 1이라는 사실이 `sh`가 부모임을 알려 줍니다. 프로세스가 **둘**입니다.
- exec 사용 — 프로세스가 **하나**입니다. 셸이 새 자식을 만드는 대신 **자기 프로세스를 대상 명령으로 교체**합니다. PID 값 1은 유지되고 실행 프로그램만 `sh`에서 `sleep`으로 바뀝니다.

핵심은 "exec는 프로세스를 하나 더 만드는 것이 아니라 지금 프로세스의 알맹이를 바꿔 끼운다"입니다. 그래서 PID가 보존되고, PID 1에 도착하는 종료 신호를 대상 프로그램이 직접 받게 됩니다.

**곁가지 함정**: `kubectl exec`로 추가 실행한 `ps`의 PPID가 0으로 보일 수 있습니다. 이 프로세스는 기존 PID 1이 만든 자식이 아니라 컨테이너 런타임이 외부에서 추가한 것이고, PID namespace 안에서는 그 부모가 보이지 않기 때문입니다 (원본 §6).
</details>

**점수 (0~5)**: **2** (채점: Claude — 프로세스 트리 구조는 정확히 재구성(sh PID 1 / sleep PPID 1, exec 시 sleep PID 1). 다만 Q2 에서 정답을 전부 제공하고 PID·PPID·exec 까지 풀어 준 뒤라 **인출 증거 아님**. 다음 회차 재확인 대상)

---

### Q4. 적용 — 이 매니페스트는 왜 안 되는가

**질문**: 다음 설정으로 JVM 옵션을 넘기려 했으나 동작하지 않았습니다. 원인을 설명하고 고친 매니페스트를 쓰십시오.

```yaml
command: ["java"]
args: ["$JAVA_OPTS", "-jar", "app.jar"]
```

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

**원인**: Kubernetes와 컨테이너 런타임은 이 문자열을 셸 문법으로 해석하지 않습니다. 따라서 JVM은 `$JAVA_OPTS`라는 **문자열 하나를 그대로 인자로** 받습니다 (원본 §6).

두 겹으로 틀렸습니다. 첫째, `$VAR` 문법은 셸의 것인데 셸이 없습니다. 둘째, 설령 확장되더라도 `$(VAR_NAME)` 쪽은 이미지의 `ENV`를 참조하지 못하므로 `JAVA_OPTS`가 이미지에 정의된 변수라면 그 경로로도 못 가져옵니다 — command·args의 `$(VAR_NAME)`은 컨테이너 시작 전에 Kubernetes가 구성한 환경만 참조하고, **이미지의 `ENV`는 이 확장에 쓰이지 않습니다** (원본 §4).

**고친 매니페스트** (원본 §6):

```yaml
command: ["sh", "-c"]
args:
- 'exec java $JAVA_OPTS -jar app.jar'
```

셸이 문자열을 해석해 여러 JVM 인자로 펼치고, 해석이 끝난 뒤 `exec`로 셸을 JVM으로 교체합니다.
</details>

**점수 (0~5)**: **1** (채점: Claude — 미답. "이미지에 ENV 있으면 되는 거 아닌가"로 되물어, 값의 **소재**와 **치환 주체**를 하나로 봄. command/args 배열이 셸을 거치지 않는다는 사실 미보유)

---

### Q5. 함정 — command만 덮어쓰면 무엇이 사라지는가

**질문**: 이미지가 `ENTRYPOINT ["node", "app.js"]` / `CMD ["--listen-port", "8080"]`입니다. 매니페스트에 `command: ["node", "--cpu-prof", "app.js"]`만 적고 `args`는 생략했습니다. 실제 실행되는 전체 명령은 무엇이며, 그 규칙을 한 줄로 일반화하십시오.

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

실행되는 것은 **`node --cpu-prof app.js`뿐**입니다. `args`를 생략했으니 이미지의 CMD가 남아 붙을 것 같지만 그렇지 않습니다 — **`command`를 지정하는 순간 이미지의 CMD는 버려집니다** (원본 §2). 프로파일링을 켜려다 포트 설정을 잃는 셈입니다.

네 조합 (원본 §2):

| `command` | `args` | 실제 실행되는 명령 |
|---|---|---|
| 생략 | 생략 | 이미지 ENTRYPOINT + 이미지 CMD |
| 생략 | 지정 | 이미지 ENTRYPOINT + 매니페스트 `args` |
| 지정 | 생략 | 매니페스트 `command` 만 — **이미지 CMD 는 버려진다** |
| 지정 | 지정 | 매니페스트 `command` + 매니페스트 `args` |

**한 줄 일반화**: 생략한 쪽만 이미지 기본값이 채워지는데, `command`를 채우면 CMD 자리는 기본값 대신 빈 채로 남습니다. `args`를 생략했을 때 CMD가 살아남는 것은 `command`도 함께 생략했을 때뿐입니다 (원본 §2·§8 Q1).

원본은 이 비대칭이 공식 문서에 없어 kind v1.35로 직접 확인했다고 각주에 적어 두었습니다 (원본 `[^cmd-args]`).
</details>

**점수 (0~5)**: **1** (채점: Claude — `--listen-port 8080` 이 붙는다고 답해 함정에 그대로 빠짐. command 지정 시 CMD 폐기라는 비대칭 미보유)

## 회차 종합 평가

### 1. SM-2 quality 점수 (0~5)

**quality**: **1** (Q1~Q5 = 2·1·2·1·1, 평균 1.4. 회차 1 의 3 에서 **퇴행**)

> Wozniak SM-2: 5=완벽, 4=정답+머뭇, 3=정답+힘듦, 2=오답+쉬워 보였음, 1=오답+정답 기억남, 0=완전 blackout.

### 2. 3축 메타인지 자가평가 (1~5)

| 축 | 점수 (1~5) | 메모 |
|----|----------|------|
| A. 면접 답변 가능성 | 1 | exec·CMD 폐기 모두 미답. 면접 표준 질문 3개 중 0개 |
| B. 그림 없이 말로 설명 | 2 | 설명 후 프로세스 트리는 재구성. 자력 서술은 아님 |
| C. 다른 환경 응용 | 1 | `$JAVA_OPTS` 사례에서 값의 소재와 치환 주체를 분리하지 못함 |

**평균**: **1.33**

### 3. 다음 회차 결정

회차 2 기준: quality 5 → +30일 · 4 → +14일 · 3 → +7일 · 0~2 → +1일.

**다음 회차 날짜**: **2026-09-07** (회차 2 · quality 1 → +1일)

### 3-1. 회차 소견 (2026-09-06)

회차 1(2026-07-13) quality 3 → 회차 2 quality 1 로 **퇴행**. 예정일(2026-07-16)에서 52일 연체된 뒤의 결과이므로 망각곡선상 이례적이지는 않으나, 회차 1 에서 이미 막혔던 축(exec 프로세스 교체·종료 코드)이 그대로 재현된 것이 아니라 **더 내려갔다**는 점이 문제다.

한 갈래로 모인다 — **셸이 있는가 없는가**. Q2(exec), Q4(`$JAVA_OPTS`), Q5(CMD 폐기) 셋 다 "command/args 배열은 셸을 거치지 않고 직접 exec 된다"는 한 문장을 모르면 전부 막힌다. 다음 학습은 항목별 복습이 아니라 이 문장 하나를 축으로 재구성한다.

곁가지로 PID·PPID·종료 코드 같은 셸·프로세스 기초 용어가 비어 있었다. 08 장 이전에 그쪽을 한 번 훑는 편이 빠르다.

### 4. 졸업 판정

- [ ] 본 회차 quality ≥ 4
- [ ] 3축 메타인지 평균 ≥ 3.6
- [ ] _mistakes.md 미해결 패턴 0개

### 5. 오답 박제 → _mistakes.md

quality ≤ 3인 질문을 `write/08_cloud/book/kubernetes-in-action/_mistakes.md`에 append.

## 관련 자료

- [원본 학습 문서](../../08_cloud/book/kubernetes-in-action/08-01.command%C2%B7args%EC%99%80%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98.md)
- 이전 회차: [회차 1 (2026-07-13)](../2026-07-13/kubernetes-in-action_08-01.review.md)
- 실습: `study/k8s_in_action/08-configuring-apps/command-env/`
