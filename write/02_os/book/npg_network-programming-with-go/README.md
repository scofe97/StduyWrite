---
title: Network Programming with Go — 정독 인덱스
tags: [moc, study-index, book, go, networking, os]
status: draft
source:
  - 《Network Programming with Go》 (Adam Woodbeck, No Starch Press, 2021-03) ISBN 978-1-7185-0088-4 — 서문과 장 단위 PDF 14편. 저자·출판 정보는 https://nostarch.com/networkprogrammingwithgo 에서 2026-10-06 확인
  - https://learning.oreilly.com/library/view/network-programming-with/9781098128890/  # 챕터 PDF 를 뜬 O'Reilly 판
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Network Programming with Go/
  - ../../../roadmap/go-roadmap.md  # 이 책을 6단계 필수로 둔 로드맵
related:
  - ../../README.md
  - ../tii_tcp-ip-illustrated/README.md
  - ../cntd_computer-networking-top-down/README.md
  - ../../project/gonet-lab/README.md
  - ../../../01_language/book/lgo_learning-go/README.md
  - ../../../roadmap/go-roadmap.md
  - ../../../roadmap/network-roadmap.md
learning:
  topic: network-programming-with-go
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시
  blocked_count:
  next_lesson: "3장 Phase 1 통과(2026-10-06, 대조 판정은 학습자 위임 → 이견 없음). Phase 2 진행 중 — 보강 4건(03-01 §3 송신 버퍼·탐침 주체, 03-03 §2 다중 IP, §3 패배 다이얼러, §4 지난 데드라인 즉시 실패) 학습자 승인, agy-bh2 창(agy-npg3-fix)이 반영, 메인이 4곳 원문·go doc 대조 확인 + 03-02 링크 앵커 후속 수정, 게이트 실패 0(2026-10-06). Phase 2 메타인지(2026-10-06, 학습자 자기 평가): 자신 없는 곳 넷 — context 기초(Background·WithDeadline·WithCancel), 팬아웃 코드(select 로 응답 받는 구조), "원문 Listing" 용어, Pinger 와 5초 데드라인의 역할 구분(Pinger 가 데드라인을 민다고 봄 — 실제로는 읽기 루프가 수신 때 민다). 넷 다 설명으로 채움(도움받은 응답). 학습자 승인으로 03-03 에 넷 보강(agy-bh1 창 agy-npg3-fix2, 게이트 0) → Phase 2 통과(2026-10-06). Phase 3 진행 중 — 계획 승인(실험 1 context 다이얼 취소 · 2 팬아웃 select · 3 지난 데드라인 바쁜 루프 · 4 하트비트 · 5 선택 읽지 않는 수신자, 코드는 메인 작성), ~/study/npg-practice/ch03/ 생성, 실험 1 코드 작성·컴파일 확인, 예측 대기. 원문 정오 후보 1건: 원문 p.(Listing 3-6 뒤) "여러 IP 면 각 IP 사이 연결 경합" — go doc 은 같은 계열 순차·타임아웃 분할, 경합은 IPv6/IPv4 사이뿐. 노트 03-03 §2 는 고쳤지만 원문 정오 블록이 없음(다음 agy 배치)(~/study/npg-practice/ch03/, 첫 실험 후보: 팬아웃·지난 데드라인 바쁜 루프·데드라인 없는 하트비트). 맞음: Q1 핵심·Q2·Q3·Q5. 잘못 알던 인과: Q4 errors.Is 를 타입 꺼내기로 봄(Is=값 비교, 타입은 As·단언), Q6·Q7 연결 시도 취소를 close 로 봄(ctx 를 DialContext 에 넘기면 Dial 이 에러로 돌아옴), Q8 지난 데드라인 뒤 Read 가 다시 기다린다고 봄(즉시 실패 — gonet ph1 에서 설명 받았던 축, 정착 안 됨), Q9 close 없이 기다려도 된다고 봄. 몰랐던 사실: net.Error Timeout/Temporary(후자 deprecated), Dialer.Timeout·DialContext, 다중 IP 타임아웃 분할·IPv4/6 Fast Fallback, 하트비트 수신마다 데드라인 전진. 다음: 이견 확인 → Phase 1 출구 → Phase 2 는 03-01~03 보강(agy 위임, 후보 4건)"
updated: 2026-10-06
---

# Network Programming with Go — 정독 인덱스

---

> 이 폴더는 『Network Programming with Go』(Adam Woodbeck, 2021)를 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 소켓에서 HTTP·TLS·직렬화·관측까지, 같은 네트워크 장치를 Go 표준 라이브러리로 직접 짜는 쪽을 맡습니다.

## 이 책을 여기 두는 이유

> 문법은 Learning Go 가, 규격과 패킷은 CNTD·TCP/IP Illustrated 가 맡습니다. 이 책은 그 사이에서 같은 장치를 `net` 패키지 코드로 옮기는 자리라 `02_os/book/` 에 둡니다.

[Learning Go 정독 인덱스](../../../01_language/book/lgo_learning-go/README.md)는 이 책을 문법 뒤에 읽는 서비스 구현서로 보고, 정독할 때 `02_os/book/` 에 두기로 이미 정해 두었습니다. 이 폴더는 그 결정을 따른 것입니다.

같은 폴더의 다른 정독본과는 보는 방향이 다릅니다. [CNTD](../cntd_computer-networking-top-down/README.md)는 TCP 가 왜 그렇게 설계됐는지를 추상 모델로 쌓습니다. [TCP/IP Illustrated](../tii_tcp-ip-illustrated/README.md)는 같은 장치가 실제 구현과 tcpdump 출력에서 어떤 모양인지 보입니다. 이 책은 그 장치를 애플리케이션 쪽에서 다룹니다. `net.Dial` 이 핸드셰이크를 어떻게 감추는지, 데드라인을 어디에 거는지, 연결을 언제 닫아야 자원이 돌아오는지를 Go 코드로 보입니다.

[gonet-lab](../../project/gonet-lab/README.md)과는 역할을 나눕니다. gonet-lab 은 primitive 를 직접 짜고 일부러 깨뜨려 커널 쪽에서 관측하는 랩입니다. 이 책은 그 랩이 기대는 표준 라이브러리 사용법의 정본입니다. 랩 문서가 이미 설명한 개념(listener 소켓과 연결 소켓, UDP 데이터그램 경계)은 이 폴더에서 다시 풀지 않고 그 문서로 링크합니다.



## 범위와 읽는 순서

> 책은 기초 지식, 소켓, 응용 프로토콜, 직렬화·관측·배포의 4부 14장입니다. 로드맵이 필수로 둔 개념을 받치는 1~4·8·9장을 먼저 쓰고, 추천 장은 그다음, 선택·보완 장은 그 개념에 닿을 때 씁니다.

서문 "What's in This Book" 은 책을 4부로 나눕니다. 1·2장이 네트워크 기초를 깔고, 3~7장이 TCP·UDP·Unix 소켓을 짭니다. 8~11장은 HTTP 와 TLS 를, 12~14장은 직렬화·관측·클라우드 배포를 다룹니다. 아래 표의 "원문이 밝힌 목표"는 서문의 장 소개 문장을 옮긴 것입니다.

"로드맵에서 받치는 개념" 칸은 그 장이 로드맵의 어느 개념 행을 채우는지와 그 행의 우선순위를 적습니다. 선행 조건이 아닙니다. 예를 들어 "Go 6단계 TCP 스트림 · 필수"는 [Go 로드맵](../../../roadmap/go-roadmap.md) 6단계(서비스)의 "TCP 스트림" 개념을 이 장으로 배우고, 그 개념을 빼면 뒤가 막힌다는 뜻입니다.

이 책을 펴기 전에 갖출 것은 서문이 밝힌 대로 Go 문법과 모듈 사용 경험이고, 로드맵에서는 [Learning Go](../../../01_language/book/lgo_learning-go/README.md)가 맡는 1~5단계가 그 자리입니다.

| 장 | 제목 | 원문이 밝힌 목표 | 로드맵에서 받치는 개념 | 쓰는 순서 |
|---|---|---|---|---|
| 1 | An Overview of Networked Systems | 네트워크 조직 모델과 대역폭·지연·계층·캡슐화 개념 소개 | Go 6단계 주소 해석·라우팅 · 필수 | 3 |
| 2 | Resource Location and Traffic Routing | 사람이 읽는 이름과 주소로 자원을 찾는 법, 노드 사이 트래픽 라우팅 | Go 6단계 주소 해석·라우팅 · 필수 | 3 |
| 3 | Reliable TCP Data Streams | TCP 핸드셰이크·순서 번호·ACK·재전송을 살피고 Go 로 TCP 세션을 맺어 통신 | Go 6단계 TCP 스트림 · 필수, 네트워크 1단계 socket API (보완 참조) | 1 |
| 4 | Sending TCP Data | TCP 로 데이터를 보내는 기법, 연결 사이 프록시, 트래픽 관찰, 흔한 연결 처리 버그 피하기 | Go 6단계 TCP 데이터 전송·half-close · 필수 | 1 |
| 5 | Unreliable UDP Communication | TCP 와 대비한 UDP, 그 차이가 코드에 미치는 영향과 UDP 를 쓸 때 | Go 6단계 UDP·신뢰성 보강 · 추천 | 4 |
| 6 | Ensuring UDP Reliability | UDP 위에서 신뢰 전송을 구현하는 실전 예제 | Go 6단계 UDP·신뢰성 보강 · 추천 | 4 |
| 7 | Unix Domain Sockets | 같은 노드의 서비스끼리 파일 기반 통신으로 데이터를 효율적으로 주고받기 | Go 6단계 Unix domain socket · 선택 | 5 |
| 8 | Writing HTTP Clients | Go 의 HTTP 클라이언트로 요청을 보내고 자원을 받기 | Go 6단계 HTTP 클라이언트 · 필수 | 2 |
| 9 | Building HTTP Services | 핸들러·미들웨어·멀티플렉서로 HTTP 애플리케이션 만들기 | Go 6단계 HTTP 서비스 · 필수 | 2 |
| 10 | Caddy: A Contemporary Web Server | 모듈과 설정 어댑터로 보안·성능·확장성을 주는 웹 서버 Caddy 소개 | 네트워크 1단계 reverse proxy · 추천 (보완 참조) | 5 |
| 11 | Securing Communications with TLS | TLS 로 인증과 암호화를 붙이고 클라이언트·서버 상호 인증까지 구성 | Go 6단계 TLS · 추천 | 4 |
| 12 | Data Serialization | Gob·JSON·프로토콜 버퍼로 직렬화하고 gRPC 로 통신 | Go 6단계 직렬화·slog·지표 · 추천 | 4 |
| 13 | Logging and Metrics | 서비스 동작을 들여다보는 도구로 문제를 미리 잡고 장애에서 회복 | Go 6단계 직렬화·slog·지표 · 추천 | 4 |
| 14 | Moving to the Cloud | AWS·Google Cloud·Azure 에 서버리스 애플리케이션 개발·배포 | 없음 | 범위 밖 |

Go 로드맵의 책 읽기 흐름이 이 책의 읽을 장으로 둔 것은 필수 개념을 받치는 1~4·8·9장입니다. 나머지 장은 로드맵의 보완 참조 표에 있어서, 그 개념에 닿았을 때 엽니다.

쓰는 순서도 이 우선순위를 따릅니다. 3·4장은 TCP 연결을 Go 코드로 맺고 닫고 데드라인을 거는 자리이고 이 책만 줄 수 있는 내용이 가장 많아 먼저 씁니다. 8·9장의 HTTP 가 그다음입니다. 1·2장도 필수지만 계층·주소·라우팅은 CNTD 와 Networking and Kubernetes 정독본이 이미 채운 개념이라, 이 책에만 있는 차이분만 짧게 씁니다. 14장은 두 로드맵 어디에도 없어 범위 밖입니다.



## 작성된 정독 노트

> 편마다 원문 절 범위와 한 줄 핵심을 둡니다.

| 편 | 원문 | 한 줄 핵심 |
|---|---|---|
| [03-01](./03-01.TCP%20%EC%84%B8%EC%85%98%EC%9D%80%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC%EB%A1%9C%20%EC%97%B4%EA%B3%A0%20%EC%B0%BD%EC%9C%BC%EB%A1%9C%20%EC%86%8D%EB%8F%84%EB%A5%BC%20%EB%A7%9E%EC%B6%94%EA%B3%A0%20FIN%C2%B7RST%20%EB%A1%9C%20%EB%81%9D%EB%82%9C%EB%8B%A4.md) | 3장 도입 ~ Handling Less Graceful Terminations (Fig 3-1~3-4) | TCP 의 신뢰성은 핸드셰이크·순서 번호·창·FIN/RST 교환이고, Go 앱은 이를 몇 개 API 호출 뒤에서 누린다 |
| [03-02](./03-02.Go%20%EC%9D%98%20TCP%20%EC%97%B0%EA%B2%B0%EC%9D%80%20Listen%C2%B7Accept%C2%B7Dial%20%EC%84%B8%20%ED%98%B8%EC%B6%9C%EB%A1%9C%20%EB%A7%BA%EB%8A%94%EB%8B%A4.md) | Establishing a TCP Connection ~ …with a Server (Listing 3-1~3-3) | Listen·Accept·Dial 로 맺고, goroutine 으로 나누고, `io.EOF` 로 정중히 끝낸다 |
| [03-03](./03-03.%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%EC%9D%80%20Dialer%C2%B7context%20%EB%A1%9C%2C%20%EC%9C%A0%ED%9C%B4%20%EA%B0%90%EC%A7%80%EB%8A%94%20%EB%8D%B0%EB%93%9C%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%ED%95%98%ED%8A%B8%EB%B9%84%ED%8A%B8%EB%A1%9C%20%EA%B1%B4%EB%8B%A4.md) | Time-outs and Temporary Errors ~ Advancing the Deadline (Listing 3-4~3-12) | 연결은 무한정 침묵할 수 있으니 Dialer·context·데드라인·하트비트로 시간 한도를 건다 |
| [04-01](./04-01.TCP%20%EB%8A%94%20%EA%B2%BD%EA%B3%84%20%EC%97%86%EB%8A%94%20%EB%B0%94%EC%9D%B4%ED%8A%B8%20%ED%9D%90%EB%A6%84%EC%9D%B4%EB%9D%BC%20%EC%9D%BD%EB%8A%94%20%EC%AA%BD%EC%9D%B4%20%EB%A9%94%EC%8B%9C%EC%A7%80%EB%A5%BC%20%EC%9E%90%EB%A5%B8%EB%8B%A4.md) | 4장 도입 ~ Handling Errors While Reading and Writing (Listing 4-1~4-13) | TCP 는 경계 없는 바이트 흐름이라 읽는 쪽이 고정 버퍼·구분자·TLV 로 메시지를 자른다 |
| [04-02](./04-02.io%20%EC%9D%98%20Copy%C2%B7MultiWriter%C2%B7TeeReader%20%EB%A1%9C%20%EC%97%B0%EA%B2%B0%EC%9D%84%20%EC%9E%87%EA%B3%A0%20%EC%97%BF%EB%B3%B8%EB%8B%A4.md) | Creating Robust Network Applications ~ Pinging a Host (Listing 4-14~4-22) | `io.Copy` 두 개로 프록시를 잇고 TeeReader·MultiWriter 로 엿본다. half-close 는 Go 문서로 보강 |
| [04-03](./04-03.TCPConn%20%EC%86%90%EC%9E%A1%EC%9D%B4%EC%99%80%20%ED%9D%94%ED%95%9C%20%EB%B2%84%EA%B7%B8%20%E2%80%94%20keepalive%C2%B7linger%C2%B7%EB%B2%84%ED%8D%BC%C2%B7zero%20window%C2%B7CLOSE_WAIT.md) | Exploring Go's TCPConn ~ CLOSE_WAIT (Listing 4-23~4-27) | TCPConn 의 keepalive·linger·버퍼 손잡이와, 읽기 지연·Close 누락이 만드는 zero window·CLOSE_WAIT |
| [05-01](./05-01.UDP%20%EB%8A%94%20%EC%97%B0%EA%B2%B0%20%EC%97%86%EC%9D%B4%20%EB%B3%B4%EB%82%B4%EA%B3%A0%2C%20%EC%86%8C%EC%BC%93%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%88%84%EA%B5%AC%EC%97%90%EA%B2%8C%EC%84%9C%EB%93%A0%20%EB%B0%9B%EB%8A%94%EB%8B%A4.md) | 5장 도입 ~ Every UDP Connection Is a Listener (Listing 5-1~5-5) | UDP 엔 연결 상태가 없어 모든 소켓이 리스너이고, 받을 때마다 보낸 주소를 확인해야 한다 |
| [05-02](./05-02.net.Conn%20%EC%9C%BC%EB%A1%9C%20%EC%83%81%EB%8C%80%EB%A5%BC%20%EA%B3%A0%EC%A0%95%ED%95%98%EA%B3%A0%20MTU%20%EC%95%84%EB%9E%98%EB%A1%9C%20%EB%B3%B4%EB%82%B4%20%EB%8B%A8%ED%8E%B8%ED%99%94%EB%A5%BC%20%ED%94%BC%ED%95%9C%EB%8B%A4.md) | Using net.Conn in UDP ~ Avoiding Fragmentation (Listing 5-6~5-10) | `net.Dial` 로 상대를 고정하고 페이로드를 MTU 예산(1,472B) 안에 두어 단편화를 피한다 |
| [06-01](./06-01.TFTP%20%ED%8C%A8%ED%82%B7%20%EB%84%A4%20%EC%A2%85%EC%9D%84%20%EB%B0%94%EC%9D%B4%ED%8A%B8%EB%A1%9C%20%EC%A7%A0%EB%8B%A4.md) | 6장 도입 ~ Handling Errors (Listing 6-1~6-8) | TFTP 의 RRQ·DATA·ACK·ERROR 네 패킷을 opcode 와 바이트 배치로 짠다 |
| [06-02](./06-02.TFTP%20%EC%84%9C%EB%B2%84%EB%8A%94%20%EB%B8%94%EB%A1%9D%EB%A7%88%EB%8B%A4%20ACK%20%EB%A5%BC%20%EA%B8%B0%EB%8B%A4%EB%A6%AC%EA%B3%A0%20%EC%9E%AC%EC%A0%84%EC%86%A1%ED%95%B4%20UDP%20%EC%9C%84%EC%97%90%20%EC%8B%A0%EB%A2%B0%EC%84%B1%EC%9D%84%20%EC%98%AC%EB%A6%B0%EB%8B%A4.md) | The TFTP Server ~ Downloading Files over UDP (Listing 6-9~6-13) | 요청마다 연결을 나누고 블록마다 ACK 를 기다리며 재전송해 UDP 위에 신뢰성을 올린다 |
| [07-01](./07-01.Unix%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%86%8C%EC%BC%93%EC%9D%80%20%ED%8C%8C%EC%9D%BC%20%EA%B2%BD%EB%A1%9C%EB%A1%9C%20%EB%AC%B6%EC%9D%B4%EA%B3%A0%20%EC%84%B8%20%EA%B0%80%EC%A7%80%20%ED%83%80%EC%9E%85%EC%9D%B4%20%EA%B2%BD%EA%B3%84%EB%A5%BC%20%EB%8B%A4%EB%A5%B4%EA%B2%8C%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md) | 7장 도입 ~ unixpacket (Listing 7-1~7-12) | 소켓 파일로 묶이는 Unix 도메인 소켓의 생성·권한·정리와, unix·unixgram·unixpacket 이 메시지 경계를 다루는 차이 |
| [07-02](./07-02.%ED%94%BC%EC%96%B4%20%EC%9E%90%EA%B2%A9%20%EC%A6%9D%EB%AA%85%EC%9C%BC%EB%A1%9C%20%EC%A0%91%EC%86%8D%ED%95%9C%20%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EB%A5%BC%20%EC%9D%B8%EC%A6%9D%ED%95%98%EB%8A%94%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) | Writing a Service That Authenticates Clients ~ 장 끝 (Listing 7-13~7-16) | 커널이 알려 주는 피어 자격 증명으로 접속 프로세스의 그룹을 확인해 허용하거나 끊는다 |

3~7장 12편은 2026-10-06 메인 Claude 가 틀을 잡고 agy(Gemini)가 작성했습니다. 3·4장은 교차 검증을 마쳤고, 3~7장 도식은 메인이 렌더해 확인했습니다. 학습자 검증(Phase 4·복습)은 아직입니다.



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 3장 03-01~03 초안(AI 작성, 학습자 미검증)이 디스크에 있습니다. 2026-10-06 3장 4-Phase 세션을 시작해 Phase 1 예측 단계입니다 |
| 난이도 레벨 | 기본. 학습자 자답 전이라 조정 근거가 없습니다 |
| 막힌 지점 | 아직 없음 |
| 다음 레슨 후보 | 03-01 — 3장 TCP 스트림. 첫 편의 절 범위는 원문을 읽고 정합니다 |
| 최근 검증 결과 | 없음 |
| 원문 정오 누적 | 0건 |
| 책과 현재의 차이 | 아직 기록 없음. 서문은 Go 1.12 이상(일부 예제 1.14 이상)을 전제합니다 |
| 복습 회차 | 없음 |



## 출처와 톤

- 원문(챕터 PDF)이 1차 자료입니다. 사실·수치·이름은 추출한 원문에서만 가져오고, 책 밖 보강은 Go 공식 문서·RFC 같은 1차 자료를 그 사실이 쓰이는 절에 링크로 달아 녹입니다.
- 책은 2021년 판이라 Go 1.12~1.14 와 Ubuntu 20.04 시절 환경을 전제합니다. 현재 Go 표준 라이브러리와 다른 자리는 "책은 X, 현재는 Y" 로 병기합니다.
- 노트는 책 없이 읽고 배우는 문서입니다. 정오 블록이나 쪽 번호처럼 원문을 펴야 의미가 생기는 내용은 두지 않습니다. 원문 오류의 처리 기준은 정독 노트 규약 04b 6단계를 따릅니다.
- 톤은 합니다체로 통일합니다. 도식과 생성기는 `_assets/` 에 둡니다.
- 실습 코드는 `write/` 밖 저장소에 두고, 커널 쪽 관측은 OrbStack 의 `ubuntu` 머신에서 합니다. 커널·Go 버전과 날짜를 캡처 옆에 적습니다.
