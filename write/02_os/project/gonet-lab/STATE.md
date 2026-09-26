---
topic: gonet-lab
scope: durable
level: 기본
last_verified:
blocked_count: 0
next_lesson: "Phase 0 개념 이해 — net.Listen 아래의 socket·bind·listen·accept 와 FD. listener 소켓과 accept 된 소켓이 왜 따로인지 자기 말로"
updated: 2026-09-26
---

# gonet-lab 학습 상태

## 미션 — 왜 이걸 배우는가

네트워크 장애 앞에서 애플리케이션 로그만 보지 않고, `ss`·`tcpdump`·`strace`·metric·eBPF 가운데 맞는 계층의 도구를 고를 수 있게 되는 것이 미션이다. 그러려면 Go 코드 한 줄이 goroutine, netpoller, epoll, 소켓, FD 로 어떻게 내려가는지 손으로 따라가 봐야 한다. 네트워크 프로그램 하나를 완성하는 것은 목표가 아니다.

## 진행 구조

랩 Phase 하나 = 학습 토픽 하나. 각 Phase 안을 4-Phase(개념 이해 → 학습 문서 → 실습 → 검증)로 돈다. 실습은 늘 정상 동작과 장애 주입이 짝이다. 코드는 `~/study/gonet-lab`, 로드맵은 그 저장소의 `docs/01-01.gonet-lab-roadmap.md`, Phase 상세 계획은 `docs/03-NN.gonet-lab-phase<N>-plan.md` 가 기준이다. Linux 관측은 OrbStack `ubuntu` 머신에서 한다. 이 폴더에는 Phase 별 학습 문서와 이 상태 파일만 둔다.

| 랩 Phase | 학습 문서 | 4-Phase 진행 | 검증일 |
|---|---|---|---|
| 0 Network CLI | (미작성) | 개념 이해 전 (코드 완료) | |
| 1 TCP Echo / Chat | | | |
| 2 UDP | | | |
| 3 DNS Client | | | |
| 4 TCP Proxy | | | |
| 5 SOCKS5 Proxy | | | |
| 6 HTTP CONNECT | | | |
| 7 Reverse Tunnel | | | |
| 8 Stream Multiplexing | | | |
| 9 Discovery | | | |
| 10 P2P Overlay | | | |
| 11 Mini DHT | | | |
| 12 Failure / Chaos | | | |
| 13 Observability | | | |
| 14 eBPF Observer | | | |

## 현재 난이도 레벨

기본. Go 로 netpath-lab 1국면(DNS·TCP·HTTP 측정)을 짰고 `errors.Is`·`context`·`httptrace` 는 써 봤다. 서버 쪽 소켓 수명, netpoller, half-close 는 아직 직접 다뤄 보지 않았다.

## 이해 근거 (선택)

- (시작 전)

## 막힌 지점

- (없음 — 시작 전)

## 미해결 질문

- OrbStack 커널(7.0.14-orbstack)이 eBPF kprobe·tracepoint·BTF 를 어디까지 지원하는가. Phase 14 직전에 `bpftool feature` 로 확인한다.
- `tc netem` 을 OrbStack 머신의 `lo` 에 걸 수 있는가. Phase 2 직전에 확인한다.

## 다음 레슨 후보 + 고른 이유

- Phase 0 개념 이해. 코드는 이미 돌지만, `lsof` 에 LISTEN 소켓과 ESTABLISHED 소켓이 FD 번호를 따로 받는 이유를 설명하지 못하면 Phase 1 의 "접속 1,000 개에서 먼저 바닥나는 자원" 질문에 답할 수 없다.

## 물어볼 곳

- Go 표준 라이브러리 `net` 패키지 문서 (https://pkg.go.dev/net) — Listener·Conn·Dialer 동작이 기대와 다를 때.
- Linux man pages `socket(7)`, `tcp(7)`, `epoll(7)` (https://man7.org/linux/man-pages/) — syscall 과 소켓 옵션.
