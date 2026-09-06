---
title: "Linux 네트워크 진단 도구 — 계층 순서대로 수사하기 — 복습 회차 1"
tags: [review, networking, diagnostics, dig, ss, nmap, curl]
status: in_progress
source: "../../08_cloud/book/networking-and-kubernetes/02-03.Linux 네트워크 진단 도구 — 계층 순서대로 수사하기.md"
round: 1
round_date: 2026-08-31
prev_round_date: null
next_round_date: null
quality: null
metacog:
  interview: null
  speak_without_diagram: null
  apply_to_other_env: null
updated: 2026-08-31
---

# Linux 네트워크 진단 도구 — 계층 순서대로 수사하기 — 복습 회차 1

> 원본: [Linux 네트워크 진단 도구 — 계층 순서대로 수사하기](../../08_cloud/book/networking-and-kubernetes/02-03.Linux%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EA%B3%84%EC%B8%B5%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%EC%88%98%EC%82%AC%ED%95%98%EA%B8%B0.md)
> 회차 1 · 2026-08-31 · 이전 학습: 2026-08-28 (Phase 1 통과)
>
> **본 복습 규약 (Karpicke & Roediger 2006, testing effect):**
> 1. 각 질문에 *먼저 자기 답을 적어라* — 답을 보지 말 것
> 2. 자기 답 작성 후에만 `<details>` 의 정답을 열어라
> 3. 정답과 비교해 0~5 점 self-quality 점수를 매겨라
> 4. 회차 끝 종합 평가에서 다음 회차 날짜가 결정됨



## 학습 목표 (원본 §학습목표 인용)

도구 이름을 외우는 대신, 증상을 보고 어느 계층부터 의심할지 정하고 그 순서로 도구를 고르는 상태.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.



## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)** 다섯 갈래로 챕터의 핵심을 잡는다.

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: `traceroute` 를 한 문장으로 정의하고, TTL 과 TIME_EXCEEDED 로 경로를 어떻게 알아내는지 답하라. **마지막 홉만 예외**인 이유도 함께.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

<details>
<summary>정답 보기 (먼저 자기 답 적은 뒤)</summary>

TTL 을 1 부터 올려 보내며 각 라우터의 TIME_EXCEEDED 회신으로 경로상 홉을 한 줄씩 알아내는 경로 진단 도구다.

TTL 이 0 이 된 지점의 라우터가 발신자에게 TIME_EXCEEDED 를 돌려주므로, TTL 을 1·2·3… 으로 늘리면 첫 홉부터 한 홉씩 드러난다.

**마지막 홉은 예외다.** 목적지는 TTL 이 남아 있으니 TIME_EXCEEDED 를 보내지 않는다. 대신 프로브 종류에 따라 다르게 답하고 그 응답이 트레이스를 끝낸다 — 기본 UDP 프로브면 ICMP Port Unreachable, `-I` 면 Echo Reply, `-T` 면 SYN/ACK·RST 다 — 원본 §2.
</details>

**자가 점수 (0~5)**: __
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*
---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: 진단을 **계층 순서로** 좁혀야 하는 이유는 무엇인가. 그 순서와 각 단의 도구를 들어 답하라.

**자기 답**:

```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

**앞 관문이 막히면 뒤를 볼 필요가 없기** 때문이다. 순서대로 좁히면 실패 지점이 빠르게 격리된다. 위에서부터 아무 데나 찔러 보면 어디서부터 안 되는지가 안 나온다.

1. 이름 — `dig`
2. 도달 — `ping`·`traceroute`
3. 포트 — `ss`·`nmap`
4. 프로토콜 — `telnet`·`openssl`·`curl`

다만 실무에서는 `curl -v` 로 위에서 한 번 찔러 멈춘 지점부터 아래로 판다. **사다리는 오르는 순서가 아니라 어디를 팔지 정하는 지도다** — 원본 §수사 순서.
</details>

**자가 점수 (0~5)**: __

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: `nmap` 이 내놓는 `open` · `closed` · `filtered` 세 상태는 각각 **무엇을 받아서** 그렇게 판정한 것인가.

**자기 답**:

```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

받은 응답의 종류가 판정을 가른다.

| 상태 | 받은 것 | 뜻 |
|---|---|---|
| `open` | SYN-ACK | 누가 듣고 있음 |
| `closed` | **TCP RST** | 호스트는 살아 있고 그 포트에 소켓 없음 |
| `filtered` | 아무 답 없음 | 중간에서 DROP 됨 |

`closed` 와 `filtered` 의 차이가 곧 REJECT 와 DROP 의 차이다. `nmap` 은 그 판정을 대신해 준다. `-Pn` 은 핑으로 생사 확인을 먼저 하지 말라는 뜻으로, ICMP 가 막힌 호스트를 죽었다고 단정해 스캔을 포기하는 것을 막는다 — 원본 §4.
</details>

**자가 점수 (0~5)**: __

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: 서비스가 안 붙는다는 신고를 받았다. 어떤 순서로 도구를 쓰겠는가. 각 단에서 **무엇을 보는지**까지 답하라.

**자기 답**:

```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

먼저 `dig` 으로 이름이 풀리는지 본다 — `status` 와 `ANSWER SECTION`, 그리고 어느 서버가 답했는지(`;; SERVER:`)를 함께 읽는다.

도달은 `ping`·`traceroute` 로 본다. 단 K8s Service 는 여기서 믿으면 안 된다.

도달하면 `ss -ltnp` 로 대상 포트에서 프로세스가 실제로 듣는지, 그리고 리스닝 주소가 `0.0.0.0`·`*` 인지 `127.0.0.1` 인지 본다. 그 주소가 노출 범위의 첫 단서다.

마지막으로 `telnet`·`curl` 로 프로토콜 수준 응답을 확인한다 — 원본 §정답 4.
</details>

**자가 점수 (0~5)**: __

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: Kubernetes Service 에 `ping` 을 쳤다. 그 결과로 서비스 정상 여부를 판단할 수 있는가.

**자기 답**:

```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

**없다. 실패해도 정상일 수 있고 성공해도 백엔드가 없을 수 있다.**

Service 가 받는 프로토콜은 TCP·UDP·SCTP 이고 ICMP 는 그중에 없다. kube-proxy 가 iptables 모드로 도는 클러스터에서 ClusterIP 는 어느 인터페이스에도 없는 **가상 주소**라, ICMP 에 답할 주체가 없어 `ping` 이 실패한다.

**다만 "항상 실패"는 아니다.** IPVS 모드에서는 ClusterIP 가 노드의 더미 인터페이스(`kube-ipvs0`)에 실제로 바인딩되므로 `ping` 이 응답할 수 있다.

확인은 `telnet`·`curl` 같은 TCP 기반 도구로 한다. 개별 Pod IP 로는 `ping` 이 될 수 있다 — 원본 §2·§정답 3.
</details>

**자가 점수 (0~5)**: __

---


## 회차 종합 평가

### 1. SM-2 quality 점수 (0~5)

Q1~Q5 평균을 반올림, 또는 *가장 막힌 질문 기준* 으로 보수적으로.

**quality**: __

> Wozniak SM-2: 5=완벽, 4=정답+머뭇, 3=정답+힘듦, 2=오답+쉬워 보였음, 1=오답+정답 기억남, 0=완전 blackout.

### 2. 3축 메타인지 자가평가 (1~5)

| 축 | 점수 (1~5) | 메모 |
|----|----------|------|
| A. 면접 답변 가능성 | __ | |
| B. 그림 없이 말로 설명 | __ | |
| C. 다른 환경 응용 | __ | |

**평균**: __

### 3. 다음 회차 결정

| 현재 회차 | quality 5 | quality 4 | quality 3 | quality 0~2 |
|----------|----------|----------|----------|------------|
| 1 | +14일 | +7일 | +3일 | +1일 (즉시 재학습) |

**다음 회차 날짜**: __ → 정한 값을 이 파일 frontmatter 의 `next_round_date` 에 반드시 쓴다.
이 필드가 비어 있으면 `learning-status.mjs` 가 다음 회차를 못 잡는다.

### 4. 졸업 판정

- [ ] 본 회차 quality ≥ 4
- [ ] 3축 메타인지 평균 ≥ 3.6
- [ ] `_mistakes.md` 에 본 문서 관련 미해결 패턴 0개

### 5. 오답 박제 → `_mistakes.md`

quality ≤ 3 인 질문을 `write/08_cloud/book/networking-and-kubernetes/_mistakes.md` 에 append (없으면 신규 생성).
