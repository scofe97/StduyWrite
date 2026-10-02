---
title: gonet-lab — 프로젝트 인덱스
tags: [moc, study-index, lab, networking, go, linux]
status: draft
source:
  - ~/study/gonet-lab  # 직접 만드는 네트워크 primitive 실습 저장소 — Phase 0 구현 시점
  - https://github.com/scofe97/ai-context/blob/1a8b9d7/project/go-network-lab.md  # 원본 로드맵 (비공개)
  - https://github.com/projectdiscovery/naabu  # Phase 4 Port Scanner 비교 구현 — 2026-10-01 README 확인
  - https://github.com/grpc/grpc-go  # Phase 7·9·10·13·14 비교 구현
  - https://protohackers.com/problems  # Phase 별 외부 채점 과제
related:
  - ./STATE.md
  - ../../README.md
  - ../netpath-lab/README.md
  - ../network-fundamentals-lab/README.md
  - ../../../roadmap/go-roadmap.md
  - ../../../roadmap/network-roadmap.md
updated: 2026-10-02
---

# gonet-lab — 프로젝트 인덱스

---

> Go 로 네트워크 primitive 를 하나씩 직접 짜고, 일부러 깨뜨리고, 커널 쪽에서 관측하는 랩의 학습 문서 모음입니다. 코드와 로드맵은 `~/study/gonet-lab` 에 있고, 여기에는 Phase 별 학습 문서와 학습 상태만 둡니다.

## 왜 이 랩을 하는가

> 네트워크 기술을 제품 이름으로 외우면 장애 앞에서 어느 계층을 볼지 고르지 못합니다. 이 랩은 Go 코드 한 줄에서 커널 자원까지를 직접 이어 보는 것이 목표입니다.

Envoy·frp·Cilium 같은 이름은 알아도, 접속 하나가 끊겼을 때 무엇이 남는지 설명하기는 어렵습니다. `net.Conn` 뒤에는 goroutine 과 Go runtime 의 netpoller 가 있고, 그 아래에 epoll 과 소켓, 파일 디스크립터(FD)가 있습니다. 이 사슬을 한 번도 손으로 따라가 보지 않으면 "타임아웃은 누가 책임지는가", "배압이 걸리면 어디에 큐가 쌓이는가" 같은 질문에 추측으로 답하게 됩니다.

그래서 각 Phase 는 기능이 도는 데서 끝나지 않습니다. 같은 사이클을 늘 끝까지 밟습니다.

```bash
구현 → 정상 동작 → 장애 주입 → 관측 → 원인 설명 → 문서화
```

완료 기준은 "돈다"가 아니라 "회수된다"입니다. echo 서버라면 접속이 끊기는 모든 경로에서 goroutine 과 FD 가 돌아오는지를 `ss`·`lsof`·`strace` 로 확인해야 그 Phase 가 끝납니다.



## 어떻게 진행하는가

> 랩 Phase 하나가 학습 토픽 하나이고, 각 토픽을 4-Phase 로 돕니다. 진행은 `/learning-session gonet-lab` 으로 엽니다.

개념 이해 단계에서는 그 Phase 가 다루는 primitive 와 실패를 자기 말로 세웁니다. 그 설명을 학습 문서 단계에서 이 폴더에 `NN-01.<제목>.md` 로 적습니다. 번호 `NN` 은 랩 Phase 번호를 두 자리로 쓴 것이고, 문서가 둘 이상 나오면 `NN-02` 로 잇습니다.

실습은 AI 가 쓴 코드로 정상 동작과 장애 주입을 짝으로 돌립니다. 검증은 로드맵의 학습 완료 질문에 코드와 관측 결과로 답하는 것으로 닫습니다.

Linux 에서만 되는 관측(`strace`·`ss`·`tc netem`·eBPF)은 OrbStack `ubuntu` 머신에서 합니다. macOS 에서 `make build-linux` 로 빌드한 바이너리를 `orb -m ubuntu` 로 그대로 실행하면 됩니다. 절차는 저장소의 `docs/02-01.orbstack-linux-setup.md` 에 있습니다.



## Phase 와 문서

> 열여섯 Phase 는 소켓 하나에서 출발해 프록시, 터널, 오버레이를 거쳐 커널 관측까지 내려갑니다. Phase 8 Reverse Tunnel 이 첫 핵심 이정표입니다.

| Phase | 학습 질문 | 문서 | 상태 |
|---|---|---|---|
| 0 Network CLI | `net.Listen` 한 줄 아래에서 어떤 syscall 과 FD 가 생기고, listener 소켓과 accept 된 소켓은 어떻게 다른가 | [00-01](./00-01.listener%20%EC%86%8C%EC%BC%93%EA%B3%BC%20%EC%97%B0%EA%B2%B0%20%EC%86%8C%EC%BC%93.md) · [00-02](./00-02.strace%20%EC%99%80%20proc%20%EB%A1%9C%20%EC%9D%BD%EC%9D%80%20%EA%B2%83%20-%20%EC%8B%A4%EC%8A%B5%EC%97%90%EC%84%9C%20%EB%A7%8C%EB%82%9C%20syscall%C2%B7FD%C2%B7TCP%20%EC%83%81%ED%83%9C.md) · [00-03](./00-03.Go%20%EB%AC%B8%EB%B2%95%20-%20goroutine%C2%B7io.Copy%C2%B7context%C2%B7WaitGroup.md) | 4-Phase 4 완료 2026-09-28 (문서 draft) |
| 1 TCP Echo / Chat | blocking Read 를 부른 goroutine 은 OS 스레드도 붙잡는가, 접속 1,000 개에서 먼저 바닥나는 자원은 무엇인가 | [01-01](./01-01.%EC%A1%B0%EC%9A%A9%ED%95%9C%20%EC%97%B0%EA%B2%B0%EC%9D%B4%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%A9%88%EC%B6%98%EB%8B%A4%20-%20goroutine%C2%B7FD%C2%B7idle%20timeout.md) | 4-Phase 4 완료 2026-09-28 (문서 draft) |
| 2 UDP | 패킷 손실과 순서 뒤바뀜이 TCP 와 UDP 에서 각각 어떻게 드러나는가 | [02-01](./02-01.%EA%B2%BD%EA%B3%84%EB%A5%BC%20%EC%A7%80%ED%82%A4%EB%8A%94%20UDP,%20%EB%8C%80%EC%8B%A0%20%EB%96%A0%EC%95%88%EB%8A%94%20%EA%B2%83%20-%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B7%B8%EB%9E%A8%C2%B7%EC%86%90%EC%8B%A4%C2%B7%EC%88%9C%EC%84%9C.md)  · [02-02](./02-02.TCP%20%EB%8A%94%20%EC%86%90%EC%8B%A4%EC%9D%84%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%ED%8C%90%EC%A0%95%ED%95%98%EB%82%98%20-%20%EC%A4%91%EB%B3%B5%20ACK%20%EB%AC%B8%ED%84%B1%C2%B7RACK%C2%B7TLP.md) · [02-03](./02-03.UDP%20%EC%8B%A4%EC%8A%B5%20%EA%B8%B0%EB%A1%9D%20-%20%EA%B2%BD%EA%B3%84%C2%B7%EC%9E%98%EB%A6%BC%C2%B7%EC%86%8C%EC%BC%93%C2%B7netem%20%EC%86%90%EC%8B%A4%EA%B3%BC%20%EC%88%9C%EC%84%9C.md) | 4-Phase 3 통과, Phase 4 대기 (문서 draft) |
| 3 DNS Client | 라이브러리 없이 DNS 질의를 바이트로 짜면 무엇을 직접 정해야 하는가 | [03-01](./03-01.DNS%20%EC%A7%88%EC%9D%98%20%ED%95%9C%20%EC%9E%A5%EC%9D%84%20%EB%B0%94%EC%9D%B4%ED%8A%B8%EB%A1%9C%20-%20%ED%97%A4%EB%8D%94%C2%B7%EB%9D%BC%EB%B2%A8%C2%B7%EC%95%95%EC%B6%95%20%ED%8F%AC%EC%9D%B8%ED%84%B0%C2%B7TC.md) (draft) | 4-Phase 2 통과, Phase 3 실습 대기 |
| 4 Port Scanner | 같은 포트를 CONNECT·SYN·UDP 로 물었을 때 커널은 무엇을 대신 해 주고 무엇을 숨기는가, 무응답은 닫힘인가 필터인가 손실인가 | | |
| 5 TCP Proxy | 한쪽이 EOF 일 때 반대쪽을 닫을지 half-close 를 허용할지, 접속 수명의 주인은 누구인가 | | |
| 6 SOCKS5 Proxy | 단순 전달이 프로토콜을 아는 프록시가 되면 상태 기계가 어떻게 생기는가 | | |
| 7 HTTP CONNECT | TLS 를 풀지 않고 전달만 하는 프록시는 무엇을 알고 무엇을 모르는가 | | |
| 8 Reverse Tunnel | 바깥에서 들어올 수 없는 사설망 서비스를 밖으로 나가는 접속 하나로 어떻게 노출하는가 | | |
| 9 Stream Multiplexing | 물리 접속 하나 위의 논리 스트림 여럿에서 느린 스트림 하나가 나머지를 막는가 | | |
| 10 Discovery | 고정 주소 없이 이웃 노드를 찾고, 사라진 노드를 언제 죽었다고 판정하는가 | | |
| 11 P2P Overlay | 노드의 정체와 네트워크 위치를 떼어 놓으면 도달 불가능한 peer 를 어떻게 우회하는가 | | |
| 12 Mini DHT | 전체 peer 목록 없이 XOR 거리만으로 값을 어떻게 찾아가는가 | | |
| 13 Failure / Chaos | 지연이 큐 증가, 타임아웃, 재시도, 재시도 폭주로 번지는 사슬을 어디서 끊는가 | | |
| 14 Observability | packet·connection·stream·tunnel·peer 를 서로 다른 관측 단위로 어떻게 나누는가 | | |
| 15 eBPF Observer | 애플리케이션 밖, 커널에서 같은 네트워크 동작을 보면 무엇이 더 보이는가 | | |

문서 칸은 학습 문서를 쓰면 채우고, 상태 칸의 세부 진행은 [STATE.md](./STATE.md) 가 맡습니다.



## 비교 구현과 외부 채점

> 직접 짠 primitive 는 두 방향에서 다시 확인합니다. 운영급 구현과 나란히 읽어 빠진 것을 찾고, 외부 채점기에 붙여 명세대로 도는지를 밖에서 봅니다.

내가 짠 echo 서버가 테스트를 통과해도, 그 테스트도 내가 짰다면 내가 아는 경우만 확인한 것입니다. 그래서 Phase 마다 확인 방법을 두 가지 더 둡니다.

첫째는 비교 구현을 읽는 것입니다. 포트 스캐너 naabu 는 랩 Phase 4 를 만든 계기입니다. 지금까지 모든 Phase 가 `net.Dial`·`net.Listen` 위에서만 진행했고, SYN 패킷을 직접 만들어 보내고 받는 계층은 비어 있었기 때문입니다.

grpc-go 는 뒤쪽 Phase 에서 직접 짤 primitive 를 운영급으로 완성한 구현입니다. 멀티플렉싱, keepalive, backoff, resolver 가 그 예입니다. 두 구현 모두 먼저 직접 짠 뒤에 읽습니다. 먼저 읽으면 답을 베끼게 되고, 그러면 "내 구현은 왜 여기서 막히는가"라는 질문이 생기지 않습니다.

둘째는 [protohackers](https://protohackers.com/problems) 외부 채점입니다. 채점 서버가 우리 서버에 직접 접속해, 동시 접속·잘못된 입력·연결 끊김을 일부러 섞어 가며 명세대로 도는지 봅니다. 이 채점은 선택 과제입니다. Phase 의 완료 기준은 그대로 "회수된다"이고, 채점은 그 위에 덧붙이는 검증입니다. 채점기는 공인 주소로 접속해야 해서 NAT 뒤에 있는 OrbStack 머신에는 바로 붙지 못합니다. 이 문제는 랩 Phase 8 Reverse Tunnel 을 만든 뒤 그 터널로 풉니다. 그 전까지는 명세를 보고 짠 로컬 테스트만 돌립니다.

| 랩 Phase | 비교 구현 (직접 짠 뒤 읽음) | 외부 채점 과제 (선택) |
|---|---|---|
| 1 TCP Echo / Chat | | 0 Smoke Test, 3 Budget Chat |
| 2 UDP | | 4 Unusual Database Program, 7 Line Reversal |
| 3 DNS Client | | 1 Prime Time, 2 Means to an End, 10 Voracious Code Storage (후순위) |
| 4 Port Scanner | naabu `pkg/scan`·`pkg/runner` — SYN 응답의 짝 맞추기, rate 제어 위치 | |
| 5 TCP Proxy | | 5 Mob in the Middle, 11 Pest Control |
| 7 HTTP CONNECT | grpc-go `Documentation/proxy.md` — CONNECT 터널 위에 HTTP/2 싣기 | |
| 8 Reverse Tunnel | frp·gost·portal-tunnel | 이 터널로 위 채점을 받는 것 자체가 검증 (UDP 문제는 UDP 포워딩 필요) |
| 9 Stream Multiplexing | grpc-go `internal/transport` — 스트림 윈도, WINDOW_UPDATE, 5바이트 메시지 접두 | 8 Insecure Sockets Layer |
| 10 Discovery | grpc-go `resolver`·`balancer` — 이름 해석과 연결 선택의 분리 | |
| 13 Failure / Chaos | grpc-go `keepalive`·`backoff`·연결 상태 기계 | 6 Speed Daemon, 9 Job Centre |
| 14 Observability | grpc-go `channelz`, 상태 코드 | |

표에 없는 Phase 는 아직 붙일 짝을 찾지 못한 것입니다. 표 칸에는 이름만 적었고, 각 칸에서 무엇을 비교할지 묻는 질문은 로드맵의 해당 Phase 절 `### Reference` 와 `### 외부 채점 과제 (선택)` 에 있습니다.

Phase 2 의 7번 Line Reversal 은 따로 짚어 둘 만합니다. UDP 위에 순서 보장과 재전송을 직접 짜는 과제라서 [02-02](./02-02.TCP%20%EB%8A%94%20%EC%86%90%EC%8B%A4%EC%9D%84%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%ED%8C%90%EC%A0%95%ED%95%98%EB%82%98%20-%20%EC%A4%91%EB%B3%B5%20ACK%20%EB%AC%B8%ED%84%B1%C2%B7RACK%C2%B7TLP.md) 에서 정리한 손실 판정을 앱 쪽에서 다시 설계해 보게 됩니다. "언제 손실로 보고 다시 보낼 것인가"를 커널이 아니라 내가 정해야 하기 때문입니다.



## 기존 노트와의 관계

> 이 랩은 개념을 다시 쓰지 않습니다. 개념의 정본은 기존 노트에 두고, 랩 문서에는 직접 짜고 깨뜨리며 관찰한 것만 적습니다.

| 기존 노트·랩 | 이 랩과 겹치는 곳 | 나누는 방식 |
|---|---|---|
| [netpath-lab](../netpath-lab/README.md) | TCP·DNS 실패를 errno 에서 Go 에러 값까지 따라가는 축 | netpath 는 클라이언트 쪽에서 요청 경로를 잽니다. gonet 은 서버·프록시·터널을 직접 짭니다 |
| [network-fundamentals-lab](../network-fundamentals-lab/README.md) | 3-way handshake, conntrack, NAT, MTU | 그쪽은 장전된 토폴로지를 진단하고, 이쪽은 그 위에서 도는 프로그램을 만듭니다 |
| [networking-and-kubernetes](../../../08_cloud/book/networking-and-kubernetes/README.md) | netns, veth, conntrack, CNI | 커널 메커니즘 설명은 이 정독본이 정본입니다. Phase 15 에서 그 README 의 「질문별 정본」 절로 보냅니다 |
| [paw_packet-analysis-wireshark](../../book/paw_packet-analysis-wireshark/README.md) | tcpdump·Wireshark 로 FIN·RST 읽기 | 캡처를 읽는 법은 그쪽, 무엇을 캡처할지는 이쪽입니다 |
| [systems-performance](../../book/systems-performance/README.md) | `strace`, `perf`, BPF 추적 | 도구 사용법과 방법론은 그쪽을 참조합니다 |
| [go-roadmap](../../../roadmap/go-roadmap.md) 「손으로 확인하는 실습」 | TCP echo, reverse proxy, 멀티플렉서, reverse tunnel | 그 표의 네 항목이 이 랩의 Phase 1·5·9·8 과 같은 과제입니다. 같은 절이 protohackers 0·5·3·9·7번을 외부 검증으로 드는데, 위 「비교 구현과 외부 채점」 표의 배치와 같습니다. 학습 순서는 로드맵이 정합니다 |

`~/study/portal-tunnel` 은 Phase 8 에서 비교할 reference 구현입니다. 바로 따라 하지 않고, Phase 0~9 에서 primitive 를 직접 짠 뒤 frp·gost 와 함께 읽습니다. 실험 중 기존 노트의 설명이 틀렸거나 빠진 것을 발견하면 랩 문서가 아니라 그 노트를 고칩니다.



## 참고

- 코드와 규칙: `~/study/gonet-lab` 의 `README.md`, `AGENTS.md`
- 로드맵 전사본: `~/study/gonet-lab/docs/01-01.gonet-lab-roadmap.md` (원본은 비공개 저장소 `scofe97/ai-context` 의 `project/go-network-lab.md`)
- 원격 저장소: `scofe97/gonet-lab` (private, 2026-10-01 생성)
- 로드맵 로컬 변경(2026-10-01): Phase 4 Port Scanner 추가, 기존 4~14 를 5~15 로 이동, grpc-go Reference 와 외부 채점 과제 추가. 원본을 다시 가져오면 이 세 변경을 다시 합칩니다. 이력은 로드맵 첫 줄 주석에 있습니다
- Phase 0 범위와 완료 조건: `~/study/gonet-lab/docs/03-01.gonet-lab-phase0-plan.md`
- Phase 4 범위·실험·배울 개념·naabu 플래그 대응표: `~/study/gonet-lab/docs/03-02.gonet-lab-phase4-plan.md`
- 비교 구현: [projectdiscovery/naabu](https://github.com/projectdiscovery/naabu), [grpc/grpc-go](https://github.com/grpc/grpc-go)
- 외부 채점: [protohackers.com/problems](https://protohackers.com/problems)
