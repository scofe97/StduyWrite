---
title: SSH Mastery — 정독 인덱스
tags: [moc, study-index, book, ssh, openssh, port-forwarding, tunnel, networking, os]
status: draft
source:
  - 《SSH Mastery: OpenSSH, PuTTY, Tunnels and Keys》 2nd ed. (Michael W. Lucas, Tilted Windmill Press, 저작권 표기 2017) ISBN 978-1-64235-002-9 — 단일 PDF 152쪽
  - 원서 PDF — GoogleDrive/내 드라이브/book/ssh-mastery-openssh/
  - https://mwl.io/static/books/ssh-mastery-2nd-edition.html  # 저자의 책 소개 페이지
related:
  - ../../README.md
  - ../tii_tcp-ip-illustrated/README.md
  - ../npg_network-programming-with-go/README.md
  - ../../project/ssh-bbs/README.md
  - ../../project/npg-lab/README.md
  - ../../project/portal-tunnel/README.md
learning:
  topic: ssh-mastery
  scope: durable
  level: 기본
  last_verified:
  blocked_count:
  next_lesson: "10장 Keeping SSH Connections Open — 유휴 연결 유지가 X9 하트비트와 같은 문제인지 확인"
updated: 2026-11-07
---

# SSH Mastery — 정독 인덱스

---

> 이 폴더는 『SSH Mastery』 2판(Lucas)을 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 읽을 범위와 순서를 정해 두고, 쓴 정독 노트를 아래 표에 모읍니다.

## 이 책을 여기 두는 이유

> SSH 를 운영하는 사람의 눈으로 OpenSSH 를 설명하는 책이라, 직접 만들 프로젝트 두 개가 쓰는 장치를 먼저 손으로 써 보는 자리입니다.

이 책을 들인 직접적인 이유는 리버스 터널입니다. npg 확장 트랙 X9 는 NAT 뒤 장비가 relay 로 먼저 연결을 걸어 두고, 바깥 요청을 그 연결로 받아 내는 구조를 만듭니다. OpenSSH 의 remote 포워딩(`ssh -R`)이 같은 모양을 명령 한 줄로 보여 줍니다. 공개 서버의 포트로 들어온 연결이 이미 맺어 둔 SSH 연결을 타고 안쪽 장비로 넘어가기 때문입니다. 리버스 터널 풀을 다루는 책은 찾지 못했으므로, 이 책으로 사용자 쪽 동작을 먼저 보고 구현은 portal-tunnel 소스와 RFC 로 넘어갑니다.

두 번째 이유는 [ssh-bbs](../../project/ssh-bbs/README.md) 입니다. 이 프로젝트는 SSH 서버를 직접 짜므로 호스트 키 검증, 공개키 인증, SFTP, 포트 포워딩을 서버 쪽에서 다시 만들어야 합니다. 이 책은 같은 기능을 `sshd` 설정과 클라이언트 사용법으로 설명하므로, 무엇을 만들지 정하는 기준으로 씁니다.

이 책의 한계도 분명합니다. 관리자가 쓰는 설정과 명령을 다루는 책이라 프로토콜 내부(키 교환 메시지, 채널 열기 요청의 바이트 모양)는 나오지 않습니다. 그 부분은 RFC 4251~4254 가 정본이고, 노트에서 필요한 절에 링크로 붙입니다.



## 범위와 읽는 순서

> 목차는 0~15장입니다. 쓰는 순서는 X9 와 ssh-bbs 단계가 먼저 필요로 하는 장부터입니다.

아래 표의 "다루는 것"은 저자가 서문에서 밝힌 각 장의 목표를 줄여 옮긴 것입니다. "쓰는 곳"은 이 저장소에서 그 장을 기대는 단계입니다.

| 장 | 제목 | 다루는 것 | 쓰는 곳 | 쓰는 순서 |
|---|---|---|---|---|
| 0 | Introduction | 책의 범위와 장 안내 | — | — |
| 1 | Encryption, Algorithms, and Keys | 암호화의 기초와 SSH 가 그것을 쓰는 방식 | ssh-bbs S1 | 4 |
| 2 | Common Configuration | 서버와 클라이언트가 함께 쓰는 설정 문법 | ssh-bbs S1 | 4 |
| 3 | The OpenSSH Server | `sshd` 설정의 큰 틀 | ssh-bbs S1·S10 | 3 |
| 4 | Verifying Server Keys | 처음 접속한 서버의 호스트 키를 확인하는 일 | ssh-bbs S1 | 2 |
| 5 | SSH Clients | OpenSSH `ssh` 와 PuTTY | — | 5 |
| 6 | Copying Files over SSH | SCP 와 SFTP 로 파일 옮기기 | ssh-bbs S6 | 3 |
| 7 | SSH Keys | 개인 키 쌍 만들기와 에이전트 | ssh-bbs S1 | 2 |
| 8 | X Forwarding | SSH 위로 화면 띄우기 | — | 범위 밖 |
| 9 | Port Forwarding | local·remote·dynamic 포워딩, SSH 를 TCP 프록시로 쓰기 | npg X9 · ssh-bbs S8 | 1 |
| 10 | Keeping SSH Connections Open | 방화벽·프록시가 끊는 유휴 연결을 살려 두기 | npg X9 · ssh-bbs S2 | 1 |
| 11 | Key Distribution | 호스트 키와 사용자 키를 여러 서버에 나눠 주기 | ssh-bbs S12 | 5 |
| 12 | Automation | 자동화 도구의 전송로로 쓰기, 한 가지 일만 하는 키 | ssh-bbs S10 | 5 |
| 13 | Virtual Private Networks | 두 사이트를 OpenSSH 터널로 잇기 | npg X9 비교 | 3 |
| 14 | Certificate Authorities | 인증 기관으로 허락한 키만 받기 | ssh-bbs S12 | 5 |
| 15 | OpenSSH Scraps | 남은 기능 모음 | — | 필요할 때 |

9장과 10장을 먼저 씁니다. 9장의 remote 포워딩이 X9 리버스 터널의 사용자 쪽 모습이고, 10장의 유휴 연결 유지가 X9 의 하트비트와 같은 문제를 SSH 쪽에서 풉니다. 10장은 [tii 17-01 keepalive](../tii_tcp-ip-illustrated/README.md) 와 겹치므로, TCP keepalive 는 그 노트로 링크하고 SSH 가 따로 두는 생존 확인만 씁니다.



## 작성된 정독 노트

> 9장 한 편이 있습니다. 편을 쓰면 원문 절 범위와 한 줄 핵심을 이 표에 채웁니다.

| 편 | 원문 | 한 줄 핵심 |
|---|---|---|
| [09-01 포트 포워딩](./09-01.포트%20포워딩%20—%20local·remote·dynamic%20과%20리버스%20터널의%20최소%20모형.md) | 9장 Port Forwarding (OpenSSH 절과 문제 해결. PuTTY 포워딩 화면 세 절은 제외) | 세 포워딩은 수신 포트를 여는 쪽만 다르고 모두 SSH 연결 하나 위의 채널이며, remote 가 리버스 터널의 최소 모형입니다 |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 9장 정독 노트 1편 작성 (2026-11-07) |
| 난이도 레벨 | 기본 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 10장 Keeping SSH Connections Open |
| 최근 검증 결과 | 09-01 게이트 실패 항목 합계 0, 적대적 검증 지적 9건 모두 반영 (2026-11-07) |
| 복습 회차 | 없음 |



## 출처와 톤

- 원문 PDF 가 1차 자료입니다. 사실·명령·설정 이름은 원문에서만 가져오고, 책 밖 보강은 RFC 와 OpenSSH 공식 문서를 그 사실이 쓰이는 절에 링크로 붙입니다.
- 책은 OpenSSH 7.5~7.6 을 기준으로 씁니다. 지금 판과 기본값이나 동작이 다르면 그 절 안에 현재 동작을 OpenSSH release notes 링크와 함께 씁니다.
- 노트는 책 없이 읽히게 씁니다. 본문에 쪽·그림 번호 같은 책 지칭을 두지 않고, 출처는 frontmatter 와 `## 참고 자료` 에만 적습니다.
- 실측은 맥북과 OrbStack 의 Ubuntu 머신 사이에서 합니다. 도구 버전과 날짜를 결과 옆에 적습니다.
- 톤은 합니다체로 통일합니다.
