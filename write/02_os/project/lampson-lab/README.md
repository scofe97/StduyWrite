---
title: lampson-lab — 실습 인덱스
tags: [moc, study-index, lab, spiffe, spire, step-ca, ssh-certificate, os]
status: draft
source:
  - https://github.com/gnu-gnu/lampson-lab  # 저장소
  - ~/study/lampson-lab@2397998  # 로컬 clone — 수용 테스트 AC-01 ~ AC-22 와 EP-11
related:
  - ./01-01.%EA%B3%A0%EC%A0%95%20%ED%82%A4%EB%A5%BC%20%EB%B2%84%EB%A6%AC%EA%B3%A0%205%EB%B6%84%EC%A7%9C%EB%A6%AC%20%EC%9D%B8%EC%A6%9D%EC%84%9C%EB%A5%BC%20%EC%93%B4%EB%8B%A4.md
  - ./02-01.%EC%8B%A0%EC%9B%90%EC%9D%80%20%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EC%97%90%EC%84%9C%20%EB%82%98%EC%98%A8%EB%8B%A4.md
  - ./03-01.principal%20%EC%9D%80%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EA%B3%A0%EB%A5%B4%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4.md
  - ./04-01.%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EB%8A%94%20%EA%B0%9C%EC%9D%B8%20%EA%B3%84%EC%A0%95%EC%9D%B4%20%EC%97%86%EB%8B%A4.md
  - ./05-01.%EC%8B%A4%ED%8C%A8%ED%95%B4%EC%95%BC%20%ED%95%A0%20%EA%B2%83%EC%9D%B4%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%8A%94%EC%A7%80%20%EB%B3%B8%EB%8B%A4.md
  - ./06-01.%EB%A7%8C%EB%A3%8C%EB%8F%BC%EB%8F%84%20%EC%97%B4%EB%A6%B0%20%EC%97%B0%EA%B2%B0%EC%9D%80%20%EB%82%A8%EB%8A%94%EB%8B%A4.md
  - ../../README.md
  - ../../../08_cloud/book/istio-in-action/a0-03.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%EC%8B%A0%EC%9B%90%EC%9D%84%20%EB%AC%B8%EC%84%9C%EB%A1%9C%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%84%A4%20%EA%B7%9C%EA%B2%A9.md
  - ../../book/sshm_ssh-mastery/09-01.%ED%8F%AC%ED%8A%B8%20%ED%8F%AC%EC%9B%8C%EB%94%A9%20%E2%80%94%20local%C2%B7remote%C2%B7dynamic%20%EA%B3%BC%20%EB%A6%AC%EB%B2%84%EC%8A%A4%20%ED%84%B0%EB%84%90%EC%9D%98%20%EC%B5%9C%EC%86%8C%20%EB%AA%A8%ED%98%95.md
  - ../../../08_cloud/book/container-security/11-01.TLS%EB%A1%9C%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0%20%E2%80%94%20%ED%82%A4%C2%B7%EC%9D%B8%EC%A6%9D%EC%84%9C%C2%B7CA%EC%9D%98%20%EC%97%AD%ED%95%A0.md
learning:
  topic: lampson-lab
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 작성일로 대신 채우지 않습니다
  blocked_count: 0
  next_lesson: "01-01 고정 키를 버리고 5분짜리 인증서를 쓴다 — Phase 1 읽기 전 예측"
updated: 2026-11-09
---

# lampson-lab — 실습 인덱스

---

> 이 폴더는 [`gnu-gnu/lampson-lab`](https://github.com/gnu-gnu/lampson-lab) 저장소를 블록 단위로 정독하며 정리하는 **랩 저장소 기반 학습노트**입니다. 원자료는 `make up` 한 번으로 뜨는 SPIRE·step-ca·sshd 참조 구현이고, 이 랩이 보이려는 것은 SSH 고정 키 없이 워크로드 신원만으로 호스트의 역할 계정에 들어가는 체인입니다.

## 이 폴더를 여기 두는 이유

> `02_os` 는 커널과 그 위의 자원·접속 메커니즘을 모으는 카테고리입니다. 이 랩은 그 가운데 **사람과 프로세스가 호스트에 들어가는 길**을 맡습니다.

SSH 접속은 호스트가 누구를 들여보낼지 정하는 일이라 운영체제 층의 문제입니다. 사용자 계정, `sshd` 의 설정, 접속 기록이 모두 호스트 안에 있고, 이 랩의 마지막 단계도 호스트의 principal 파일과 sudoers 로 끝납니다. 그래서 신원 규격을 다루는 `08_cloud` 가 아니라 이 카테고리에 둡니다.

신원 발급의 규격(SPIFFE ID, SVID, trust bundle)은 [istio 부록](../../../08_cloud/book/istio-in-action/a0-03.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%EC%8B%A0%EC%9B%90%EC%9D%84%20%EB%AC%B8%EC%84%9C%EB%A1%9C%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%84%A4%20%EA%B7%9C%EA%B2%A9.md) 이 다룹니다. 이 폴더는 그 규격이 **실제로 SSH 접속까지 이어지는 경로**를 따라가며, 규격 자체는 다시 정의하지 않고 링크로 넘깁니다. 인증서와 CA 의 기본은 [container-security 11-01](../../../08_cloud/book/container-security/11-01.TLS%EB%A1%9C%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0%20%E2%80%94%20%ED%82%A4%C2%B7%EC%9D%B8%EC%A6%9D%EC%84%9C%C2%B7CA%EC%9D%98%20%EC%97%AD%ED%95%A0.md) 에 있습니다.

`book/` 이 아니라 `project/` 아래에 둔 이유는 원자료가 책이 아니라 저장소이기 때문입니다. `02_os/README` 의 프로젝트 표에서 이 폴더도 `(외부 저장소 기반)` 으로 적습니다.



## 저장소가 돌아가는 방식

> `make up` 한 번으로 PKI 를 만들고, SPIRE 와 step-ca 를 띄우고, 호스트 둘과 client 를 세웁니다. 그다음 client 에서 계정을 골라 들어가 보는 구조입니다.

저장소의 흐름은 네 걸음입니다. client 의 프로세스가 SPIRE agent 에서 SVID 를 받습니다. 그 SVID 로 서명한 토큰으로 step-ca 에 SSH 인증서를 요청합니다.

인증서를 받은 프로세스는 그것으로만 호스트에 접속합니다. 호스트는 CA 공개키 하나만 믿습니다.

손은 이렇게 움직입니다. 명령줄은 저장소 README 의 형태를 따릅니다.

```bash
make up                                          # PKI·SPIRE·step-ca·호스트가 한 번에 뜹니다
docker compose exec -u deployer client bash     # 계정을 지정해 client 에 들어갑니다
lab-login role-operator@billing operator@host-billing 'id'
make test                                        # 수용 테스트 AC-01 ~ AC-22, EP-11
make down                                        # 컨테이너와 볼륨을 지웁니다
```

계정은 넷이고 uid 는 1001 부터 1004 까지 차례입니다. deployer 와 monitor 가 정상 경로입니다. stranger 는 SVID 는 받지만 매핑이 없습니다. intruder 는 SVID 도 받지 못합니다.

호스트는 `host-billing`, `host-crm` 둘입니다. 역할 계정은 `admin`, `operator`, `readonly` 입니다.



## 저장소 블록과 노트 여섯 편

> 저장소는 파일 묶음이 아니라 체인의 걸음 순서로 읽는 편이 낫습니다. 노트는 그 걸음을 블록으로 묶었습니다.

디렉토리마다 노트를 끊으면 같은 설명을 세 번 하게 됩니다. 신원 발급 하나만 해도 `spire/` 설정과 `bootstrap/` 의 entry 표와 테스트 두 개가 함께 보여 주기 때문입니다. 그래서 노트는 디렉토리가 아니라 걸음 단위로 묶었습니다.

| 노트 | 걸음 | 원자료 |
|---|---|---|
| `01-01` | 왜 고정 키를 버리는가, 한 바퀴 | README 「왜 필요한가」·「동작 구조」, `client/` |
| `02-01` | 프로세스에서 SVID 까지 | `spire/`, `bootstrap/`, `tests/ac/01·02` |
| `03-01` | SVID 에서 SSH 인증서까지 | `step/`, `bootstrap/`, `tests/ac/03 ~ 10` |
| `04-01` | 인증서에서 호스트 계정까지 | `sshd/`, `tests/ac/11 ~ 18` |
| `05-01` | 거부가 증거가 되는 조건 | `tests/lib.sh`, `tests/run.sh`, `tests/ac/` 전체 |
| `06-01` | 만료와 열린 연결 | `tests/ac/19`, `tests/ac/23` |

### 편별 목표

- [고정 키를 버리고 5분짜리 인증서를 쓴다](./01-01.%EA%B3%A0%EC%A0%95%20%ED%82%A4%EB%A5%BC%20%EB%B2%84%EB%A6%AC%EA%B3%A0%205%EB%B6%84%EC%A7%9C%EB%A6%AC%20%EC%9D%B8%EC%A6%9D%EC%84%9C%EB%A5%BC%20%EC%93%B4%EB%8B%A4.md): 고정 키의 세 가지 문제와 5분짜리 인증서가 그것을 어떻게 바꾸는지, 남는 문제가 요청자임을 압니다. uid 에서 세션까지의 한 바퀴를 따라갑니다.
- [신원은 프로세스에서 나온다](./02-01.%EC%8B%A0%EC%9B%90%EC%9D%80%20%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EC%97%90%EC%84%9C%20%EB%82%98%EC%98%A8%EB%8B%A4.md): 요청에 신원이 없고 커널이 호출자의 uid 를 알려 준다는 것을 압니다. entry 표가 uid 에 이름을 붙이고, 표에 없는 계정은 SVID 를 받지 못합니다.
- [principal 은 클라이언트가 고르지 않는다](./03-01.principal%20%EC%9D%80%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EA%B3%A0%EB%A5%B4%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4.md): step-ca 가 요청한 principal 이 아니라 SVID 의 신원으로 발급 내용을 정한다는 것을 압니다. 거부 경로 다섯 가지와 수명 상한, add-user 인증서라는 한계를 읽습니다.
- [호스트에는 개인 계정이 없다](./04-01.%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EB%8A%94%20%EA%B0%9C%EC%9D%B8%20%EA%B3%84%EC%A0%95%EC%9D%B4%20%EC%97%86%EB%8B%A4.md): 호스트가 CA 공개키와 principal 파일만 믿는 구조를 읽습니다. 포워딩 차단, 역할 계정의 권한, 접속 기록을 봅니다.
- [실패해야 할 것이 실패하는지 본다](./05-01.%EC%8B%A4%ED%8C%A8%ED%95%B4%EC%95%BC%20%ED%95%A0%20%EA%B2%83%EC%9D%B4%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%8A%94%EC%A7%80%20%EB%B3%B8%EB%8B%A4.md): 거부 테스트가 증거가 되려면 정상 경로의 성공과 로그의 거부 사유를 함께 봐야 하는 이유를 압니다.
- [만료돼도 열린 연결은 남는다](./06-01.%EB%A7%8C%EB%A3%8C%EB%8F%BC%EB%8F%84%20%EC%97%B4%EB%A6%B0%20%EC%97%B0%EA%B2%B0%EC%9D%80%20%EB%82%A8%EB%8A%94%EB%8B%A4.md): 인증서가 만료돼도 열린 연결이 남는 이유와, 호스트가 연결 길이를 60분으로 묶는 이유를 읽습니다.



## 작성된 정독 노트

> 편 하나가 노트 한 편입니다. 상태 칸은 Phase 2 를 마친 시점에 갱신합니다.

| 노트 | 원자료 | 다루는 것 | 상태 |
|---|---|---|---|
| [고정 키를 버리고 5분짜리 인증서를 쓴다](./01-01.%EA%B3%A0%EC%A0%95%20%ED%82%A4%EB%A5%BC%20%EB%B2%84%EB%A6%AC%EA%B3%A0%205%EB%B6%84%EC%A7%9C%EB%A6%AC%20%EC%9D%B8%EC%A6%9D%EC%84%9C%EB%A5%BC%20%EC%93%B4%EB%8B%A4.md) | README 와 `client/` | 고정 키의 문제·SSH 인증서·한 바퀴 | 초안 |
| [신원은 프로세스에서 나온다](./02-01.%EC%8B%A0%EC%9B%90%EC%9D%80%20%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EC%97%90%EC%84%9C%20%EB%82%98%EC%98%A8%EB%8B%A4.md) | `spire/`, `tests/ac/01·02` | SPIRE server·agent·join token·entry·uid 신원 | 초안 |
| [principal 은 클라이언트가 고르지 않는다](./03-01.principal%20%EC%9D%80%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EA%B3%A0%EB%A5%B4%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4.md) | `step/`, `tests/ac/03 ~ 10` | X5C 토큰·매핑·템플릿·policy·수명·add-user | 초안 |
| [호스트에는 개인 계정이 없다](./04-01.%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EB%8A%94%20%EA%B0%9C%EC%9D%B8%20%EA%B3%84%EC%A0%95%EC%9D%B4%20%EC%97%86%EB%8B%A4.md) | `sshd/`, `tests/ac/11 ~ 18` | principal 파일·포워딩 차단·sudoers·감사 로그 | 초안 |
| [실패해야 할 것이 실패하는지 본다](./05-01.%EC%8B%A4%ED%8C%A8%ED%95%B4%EC%95%BC%20%ED%95%A0%20%EA%B2%83%EC%9D%B4%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%8A%94%EC%A7%80%20%EB%B3%B8%EB%8B%A4.md) | `tests/` | 거부 판정·FAIL 로 세는 것·수용 기준 | 초안 |
| [만료돼도 열린 연결은 남는다](./06-01.%EB%A7%8C%EB%A3%8C%EB%8F%BC%EB%8F%84%20%EC%97%B4%EB%A6%B0%20%EC%97%B0%EA%B2%B0%EC%9D%80%20%EB%82%A8%EB%8A%94%EB%8B%A4.md) | `tests/ac/19·23` | 만료 뒤 열린 세션·연결 최대 60분 | 초안 |



## 학습 상태

> 부팅 의례가 읽는 칸입니다. 프론트매터 `learning:` 이 값을 갖고, 이 표가 그 값의 근거를 갖습니다.

| 항목 | 값 | 근거 |
|---|---|---|
| 난이도 레벨 | 기본 | Phase 1 미실시라 임시값입니다. SSH 와 TLS 인증서 어휘는 이미 있고, 처음 보는 것은 SPIRE 의 entry 와 step-ca 템플릿입니다 |
| 막힌 지점 | 없음 | Phase 1 미실시. 노트 여섯 편은 자료 추출로 먼저 세웠습니다 |
| 최근 검증 결과 | 없음 | Phase 4 자답 회차 미실시. `last_verified` 를 작성일로 대신 채우지 않았습니다 |
| 복습 회차 | 없음 | `_review/_queue.md` 등록은 Phase 4 이후입니다 |
| 다음 레슨 후보 | `01-01` Phase 1 | 한 바퀴를 먼저 잡아야 02 ~ 06 이 어느 걸음을 확대하는지 보입니다 |



## 이 맥에서의 제약

> 저장소가 전제한 환경과 이 맥이 다른 곳을 적습니다. 아래는 이 맥에서 실제로 돌려 확인한 사실입니다.

이 맥은 arm64 이고 Docker 는 OrbStack 만 씁니다. 저장소는 linux/arm64 에서 검증했다고 적어 두어서 이미지 아키텍처로 막히는 곳은 없었습니다.

- **기동 시간**: `make up` 이 49초 걸렸습니다. 이미지 캐시가 남아 있었는지는 기록하지 않았습니다
- **호스트 bash**: 호스트에서 `make test` 를 돌리려면 bash 4.4 이상이 필요합니다. macOS 기본 bash 3.2 에서는 `tests/run.sh` 가 `skipped[*]: unbound variable` 로 1초 만에 멈췄습니다. 검사 줄이 모두 FAIL 로 찍히지만 테스트 실패가 아니라 실행 환경 실패여서 그 출력은 근거로 쓰지 않았습니다. Homebrew bash 5.3.20 을 PATH 앞에 두고 다시 돌렸습니다
- **테스트 결과**: bash 5.3.20 으로 돌린 `make test` 에서 AC-01 ~ AC-20 이 PASS 했습니다. AC-21 과 AC-22 는 macOS 와 맞지 않아 FAIL 했습니다. EP-11 은 그 연쇄로 FAIL 했고, lab 을 다시 띄워 단독으로 돌리면 PASS 했습니다
- **AC-21 의 FAIL**: BSD `wc -l` 이 숫자 앞에 공백을 붙여 기대 문자열 `0 containers, ...` 와 어긋납니다. `make down` 뒤 실제로는 컨테이너·볼륨·네트워크가 0개였습니다
- **AC-22 의 FAIL**: 테스트가 호스트에서 Linux 전용 파일 `/proc/sys/kernel/random/uuid` 를 읽는데 macOS 에는 없습니다. 그래서 심어 둔 가짜 비밀이 빈 값이 되어 스캔이 놓친 것으로 판정됩니다
- **테스트 시간**: `make test` 는 181초 걸렸습니다. 저장소 README 는 약 9분이라고 적지만, AC-21 이 사이클을 건너뛰어 그 경로를 타지 않았으므로 9분은 확인하지 못했습니다
- **정리 확인**: `make down` 뒤 컨테이너와 볼륨이 0개로 남았습니다

compose 파일에 공개 포트(`ports:`)가 없고 client 에는 `docker compose exec` 로 들어갑니다. 이 맥의 다른 컨테이너와 포트가 겹칠 일은 없습니다.



## 이 폴더가 맡지 않는 것

> 겹치는 주제가 많아 경계를 적어 둡니다. 이것이 없으면 같은 내용이 여러 곳에 흩어집니다.

- **SPIFFE 규격 자체**: SPIFFE ID, SVID, trust bundle 의 규격은 [istio 부록](../../../08_cloud/book/istio-in-action/a0-03.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%EC%8B%A0%EC%9B%90%EC%9D%84%20%EB%AC%B8%EC%84%9C%EB%A1%9C%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%84%A4%20%EA%B7%9C%EA%B2%A9.md) 이 맡습니다. 이 폴더는 규격이 이 랩의 설정으로 내려온 모양만 봅니다
- **SSH 프로토콜과 포워딩**: SSH 채널과 포트 포워딩의 동작은 [sshm 09-01](../../book/sshm_ssh-mastery/09-01.%ED%8F%AC%ED%8A%B8%20%ED%8F%AC%EC%9B%8C%EB%94%A9%20%E2%80%94%20local%C2%B7remote%C2%B7dynamic%20%EA%B3%BC%20%EB%A6%AC%EB%B2%84%EC%8A%A4%20%ED%84%B0%EB%84%90%EC%9D%98%20%EC%B5%9C%EC%86%8C%20%EB%AA%A8%ED%98%95.md) 이 맡습니다. 이 폴더는 포워딩을 호스트가 왜 막는지만 04편에서 다룹니다
- **KMS 와 HSM**: 저장소가 CA 키를 암호화 없이 볼륨에 둔다고 알려진 한계로 적어 두었고, 키 보호는 비목표입니다
- **실습 절차의 전재**: 저장소 README 가 지시서이고 이 노트는 개념 축입니다. 명령은 관전 포인트에 필요한 것만 옮깁니다



## 이 폴더의 작성 규약

> 다른 `project/` 폴더와 같은 형태를 따르되, 이 폴더만의 선택이 두 가지 있습니다.

도식은 편마다 학습 목표 아래 전체 지도 한 장을 둡니다. 그릴 형태가 분명한 절에만 세부 도식을 더하므로 편당 두세 장입니다. 강조색은 그 편의 핵심 한 칸에만 씁니다.

각 편 끝의 `## 실습 메모` 는 이 맥에서 실제로 돌린 출력을 옮깁니다. 실행 기록에는 출력만 남아 있어서 명령줄은 저장소 README 의 형태를 따랐습니다. 값을 지어내지 않으려고, 기록이 없는 단계(entry 생성, join token 발급)의 로그는 인용하지 않았습니다.

사실의 기준 버전은 SPIRE 1.16.0, step-ca 0.30.2, OpenSSH 10.0 입니다. 저장소의 설정 파일을 1차 자료로 삼고, 일반 동작은 공식 문서와 대조했습니다.



## 출처와 톤

> 원자료는 저장소이고, 노트는 합니다체입니다.

번호를 두 가지로 씁니다. 노트는 `03-01` 처럼 하이픈 번호로, 저장소의 수용 테스트는 `AC-05` 처럼 AC 번호로 부릅니다.

원자료는 `gnu-gnu/lampson-lab` 저장소이며 로컬 clone 의 기준 커밋은 `2397998` 입니다. 편마다 설정 파일과 `tests/ac/` 를 1차 자료로 삼고, 저장소 README 는 의도를 확인하는 용도로 참조합니다. 저장소 밖에서 보강한 내용은 그 자리에 보강임을 밝힙니다.

원문의 오류를 조용히 고치지 않습니다. 저장소 README 와 실측이 어긋나면 그 차이를 해당 편의 실습 메모에 적습니다.
