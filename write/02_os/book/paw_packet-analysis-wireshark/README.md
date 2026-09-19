---
title: Packet Analysis with Wireshark — 정독 인덱스
tags: [moc, study-index, book, wireshark, packet-analysis, tcpdump, networking, os]
status: draft
source:
  - 《Packet Analysis with Wireshark》(Anish Nath, Packt Publishing, 2015) ISBN 978-1-78588-781-9 — 절 단위 PDF 45편 (161쪽 · 23,372단어)
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Packet Analysis with Wireshark/
  - https://www.wireshark.org/docs/wsug_html_chunked/  # Wireshark User's Guide (2026-09-05 조회 — 현행 4.6 대조용)
  - https://www.wireshark.org/docs/dfref/  # Display Filter Reference (2026-09-05 조회)
related:
  - ./01-01.%ED%8C%A8%ED%82%B7%20%EB%B6%84%EC%84%9D%EA%B8%B0%EC%99%80%20Wireshark.md
  - ./01-02.%EC%8B%A4%EC%8A%B5%20%E2%80%94%20%EC%BA%A1%EC%B2%98%20%ED%99%98%EA%B2%BD%EA%B3%BC%20%EC%B2%AB%20%ED%94%84%EB%A0%88%EC%9E%84.md
  - ./02-01.%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9E%A1%EB%8A%94%20%EB%B2%95.md
  - ./02-02.%EC%9E%A1%EC%9D%80%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9D%BD%EB%8A%94%20%EB%B2%95.md
  - ./02-03.%EB%B6%84%EC%84%9D%EC%9D%84%20%EB%8F%95%EB%8A%94%20%EA%B8%B0%EB%8A%A5%EB%93%A4.md
  - ./02-04.%EC%8B%A4%EC%8A%B5%20%E2%80%94%20%ED%95%84%ED%84%B0%EC%99%80%20%ED%95%B4%EC%84%9D.md
  - ./03-01.TCP%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EC%83%9D%EC%95%A0.md
  - ./03-02.TCP%EA%B0%80%20%EC%96%B4%EA%B8%8B%EB%82%A0%20%EB%95%8C.md
  - ./04-01.TLS%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC%20%EC%9D%BD%EA%B8%B0.md
  - ./04-02.%EC%97%B4%EC%87%A0%EC%99%80%20%EC%8B%A4%ED%8C%A8.md
  - ./05-01.%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EB%B0%9B%EC%95%84%20%EC%98%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C.md
  - ./05-02.%EC%9D%B4%EB%A6%84%EA%B3%BC%20%EC%9A%94%EC%B2%AD.md
  - ./06-01.%EB%AC%B4%EC%84%A0%EC%97%90%EC%84%9C%20%EC%9E%A1%EA%B8%B0.md
  - ./07-01.%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%EB%AC%B4%EB%84%88%EB%9C%A8%EB%A6%AC%EB%8A%94%20%EA%B3%B5%EA%B2%A9.md
  - ./07-02.%ED%9B%94%EC%B3%90%EB%B3%B4%EA%B3%A0%20%EB%81%BC%EC%96%B4%EB%93%9C%EB%8A%94%20%EA%B3%B5%EA%B2%A9.md
  - ../../README.md
  - ../../networking/README.md
  - ../systems-performance/README.md
  - ../../../08_cloud/book/networking-and-kubernetes/README.md
learning:
  topic: packet-analysis-with-wireshark
  scope: durable
  level: 기본            # 3장 Phase 4(2026-09-18) 막힌 문항 1 — 러너 규칙대로 입문에서 한 단계 올렸습니다
  last_verified: 2026-09-18  # 3장 Phase 4 자답 6축 통과(부분 통과 1). 1·2·4장 자답은 아직입니다
  blocked_count: 1          # 3장 Phase 4 기준 — ZeroWindowProbe 가 1바이트를 싣는다는 세부만 회상 실패. 번호 축·TIME_WAIT·CLOSE_WAIT 는 회상됨
  next_lesson: "3장 Phase 4 자답을 2026-09-18 에 통과했습니다 — 여섯 축 중 다섯이 통과이고 함정 축만 부분 통과입니다(창이 다시 열렸는지 떠보는 주체와 반복은 맞혔으나 그 패킷이 1바이트를 싣는다는 세부는 회상 실패). Phase 1 에서 어긋났던 번호 축과 TIME_WAIT 축은 자답에서 회상됐고, 실습 연결 축은 힌트 두 번 뒤에 간격과 부재로 정리했습니다. 3장 Phase 3 묶음 B 는 2026-09-18 에 마쳤습니다 — 닫힌 포트로 간 SYN 에 0.24ms 만에 RST,ACK 가 돌아오는 것(ICMP 가 아니라 TCP 자신의 거절), SO_LINGER 0 으로 파기하면 FIN 없이 RST 가 나가고 양쪽에 TIME_WAIT 조차 남지 않는 것, 원서의 iptables 규칙이 목적지 포트를 보기 때문에 서버 응답(출발지 8082)을 하나도 막지 못하는 것, `--sport` 로 고치면 SYN 이 1초 간격 다섯 번 뒤 두 배씩 물러나며 재전송되고 클라이언트가 SYN-SENT 에 머무는 것을 캡처로 확인했습니다. 다음은 묶음 C 입니다. 4장은 04-01·04-02 를 묶어 Phase 1(예측→채점)을 2026-09-18 에 마쳤습니다 — 예측 14문항·대조·분류까지 끝냈고 어긋난 것은 8번(평문 구간에서 알 수 있는 것을 알고리즘 협상으로만 좁힘) 하나이며 학습자 분류는 몰랐던 사실입니다. 대조 단계의 분담을 바꿨습니다 — AI 가 노트 문장을 떠서 판정과 분류까지 내고 학습자는 이견만 짚습니다(러너 문서에 반영). 그만큼 회상 확인은 Phase 4 자답이 맡습니다. 예측에서 스스로 세운 것은 합의 구간이 평문일 수밖에 없는 이유, 인증서 복제가 무의미한 이유(개인키가 없으면 못 열고, 내용을 바꾸면 서명이 깨짐), SNI 가 평문으로 먼저 가야 하는 이유, 전환 신호(ChangeCipherSpec)가 필요한 이유, 실패 이유를 알려 주는 메시지(Alert)가 필요한 이유, ECDHE 캡처는 계산이 아니라 세션 키를 받아 적어야 열린다는 것입니다. 막힌 자리는 디피-헬먼의 계산 성질과 정수 나머지 대 타원곡선의 차이로, 학습자가 두 번 "나중에 보강"을 요청했으니 노트에 그 설명이 있는지 대조 때 확인하고 없으면 보강 후보로 올립니다. 3장 Phase 1(예측→채점)은 2026-09-15 에 예측 14문항·03-01·03-02 대조·어긋남 분류까지 마쳤습니다 — 학습자 분류는 2′·5′·13·13′ 이 몰랐던 사실, 3·4·9 는 '이해했다'로만 답했고 9(TIME_WAIT 를 손실로 읽음)는 증거상 잘못 알던 인과라 Phase 4 출제 축으로 둡니다. 3장 Phase 3 는 맥 루프백 대신 OrbStack 리눅스 컨테이너 둘(~/study/paw-lab/03-tcp-lifecycle)로 3묶음 9단계를 짰습니다 — A 연결의 생애(정상·CLOSE_WAIT·20초 뒤 닫기), B 연결 실패(LISTEN 없음·SO_LINGER 0·원서 iptables 규칙), C 느림(netem delay 대 서버 sleep·느린 수신자 ZeroWindow·netem loss 중복 ACK). 한 세션에 한 묶음이며 A 는 2026-09-16 에 마쳤습니다 — 직접 뜬 캡처로 SYN·FIN 이 번호 하나를 차지하는 것(ACK·PSH 는 아님), 데이터 29바이트만큼의 전진, 먼저 닫은 쪽에 남는 TIME_WAIT, close() 를 안 부르면 오지 않는 프레임으로만 드러나는 CLOSE_WAIT, 고아가 된 FIN_WAIT_2 가 60초 뒤 선에 아무것도 내보내지 않고 접히는 것, 그 뒤 도착한 FIN 에 ack 0 인 RST 가 돌아오는 것, 20초 뒤 닫으면 종료가 셋이 아니라 넷이 되는 것을 확인했습니다. 다음은 묶음 B 입니다. 대조에서 가장 오래 막힌 자리가 '패킷이 아니라 패킷 사이의 시간으로만 보이는 상태'였기 때문입니다. 1장·2장 Phase 4 자답은 그대로 남아 있습니다(1장은 스위치 MAC 테이블·캡처 전 다섯 관문, 2장은 캡처 필터 비가역성·두 필터 문법·해석 경로 셋). 03-01·03-02 보강 프롬프트는 2026-09-15 세션에서 발급했고, 반영 여부는 학습 상태 표의 최근 검증 결과로 확인합니다"
updated: 2026-09-15
---

# Packet Analysis with Wireshark — 정독 인덱스

---

> 이 폴더는 『Packet Analysis with Wireshark』(Anish Nath, Packt, 2015)를 장 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 선에서 프레임을 그대로 떠서 프로토콜별로 해독하는 일을, Wireshark 라는 도구 하나를 축으로 7개 장에 걸쳐 훑습니다.

## 이 책을 여기 두는 이유

> `02_os` 안에서 `networking/` 이 패킷이 지나가는 길을 맡고, 이 책이 그 길 위에 계측기를 대는 쪽을 맡습니다.

`02_os`는 언어가 아닌 실행 환경, 곧 커널과 그 위의 자원·네트워크 메커니즘을 모으는 카테고리입니다. 그 안의 [`networking/`](../../networking/README.md)이 커널이 패킷을 *어떻게 나르는가*(netns·veth·netfilter·conntrack)를 맡는다면, 이 책은 그 패킷을 *어떻게 들여다보는가*를 맡습니다. 같은 대상의 반대편이라 한 카테고리 안에 두는 편이 탐색에 유리합니다.

경계를 한 문장으로 그으면 이렇습니다. **`networking/`은 패킷이 지나가는 길을 다루고, 이 책은 그 길 위에 계측기를 대는 법을 다룹니다.** 패킷 분석기는 애플리케이션을 거치지 않고 커널의 패킷 소켓에서 프레임을 복사해 가므로, 동작 위치가 소켓 API 아래·드라이버 위입니다. 그 자리가 `02_os`의 관심사입니다.

`06_observability`와는 층이 다릅니다. 그쪽은 애플리케이션과 인프라가 *스스로 내보내는* 메트릭·로그·트레이스를 다루고, 이 책은 아무도 내보내 주지 않는 것을 선에서 직접 뜹니다. 애플리케이션 로그가 침묵할 때 남는 마지막 증거가 패킷이라, 두 축은 대체가 아니라 보완입니다.



## 판본 주의 — 2015년판이고 화면은 Wireshark 1.12.6입니다

> 개념은 원문을 1차 자료로 그대로 두고, 조작 절차와 필터 표기는 현행 4.6 기준으로 적되 원문 표기를 한 구절로 남깁니다.

원문의 스크린샷은 전부 **Wireshark 1.12.6** 입니다. 현행 안정판은 **4.6** 이고, 그 사이에 시작 화면 구성과 대화상자 여럿이 다시 설계됐으며 `ssl` 디스플레이 필터가 `tls` 로 개명됐습니다.[^ssl-tls]

정독 노트는 이렇게 다룹니다. **개념은 원문을 1차 자료로 그대로 두고, 조작 절차와 필터 표기는 4.6 기준으로 적습니다.** 캡처 필터와 디스플레이 필터가 왜 갈리는지, promiscuous 모드가 무엇을 바꾸는지, 네 개 창이 같은 바이트를 어떻게 나눠 보여주는지는 판본을 타지 않습니다. 바뀐 것은 메뉴 경로와 대화상자 이름 쪽입니다. 바뀐 자리는 따로 인용 블록을 두지 않고 본문을 현행 판 기준으로 적습니다. 원문 표기는 "원문은 단수형 `Statistics | IO graph` 로 적었고"처럼 한 구절로만 남겨 그 자리에서 대조됩니다.



## 장 구성

> 절 단위 PDF 45편의 장별 목표를 각 장 도입부의 원문 문구에서 그대로 옮긴 표입니다.

절 단위 PDF 45편, 161쪽, 23,372단어입니다. 장별 목표는 추측하지 않고 각 장 도입부의 "covering the following topics" 원문에서 옮겼습니다.

| 장 | 제목 | 원문이 밝힌 토픽 | 분량 |
|----|------|-----------------|------|
| 1 | Packet Analyzers | Uses for packet analyzers · Introducing Wireshark · Other packet analyzer tools · Mobile packet capturing | 8쪽 · 1,068단어 |
| 2 | Capturing Packets | Interface lists · Start options · Capture options · Filter examples · Packet List pane · Packet Details pane · Wireshark features · tcpdump과 snoop | 34쪽 · 4,536단어 |
| 3 | Analyzing the TCP Network | Recapping TCP · connection establishment and clearing · troubleshooting · latency issues · Wireshark TCP sequence analysis | 33쪽 · 4,894단어 |
| 4 | Analyzing SSL/TLS | SSL/TLS 소개 · Handshake Protocol · 통신 복호화 · handshake 실패 디버깅 | 27쪽 · 3,533단어 |
| 5 | Analyzing Application Layer Protocols | DHCPv6 · DHCPv4 · DNS · HTTP | 26쪽 · 3,959단어 |
| 6 | WLAN Capturing | 802.11 캡처 설정과 monitor 모드 · tcpdump 802.11 · 디스플레이 필터 · L2 프레임 종류 · 인증 과정 · 802.1X EAPOL · 프로토콜 스택 | 16쪽 · 2,318단어 |
| 7 | Security Analysis | Heartbleed · DoS SYN flood · DoS ICMP flood · 스캐닝 · ARP 중복 IP 탐지(MITM) · DrDoS · BitTorrent · endpoints와 protocol hierarchy | 17쪽 · 3,064단어 |

> 1·2장이 도구를 익히는 구간이고 3장부터가 프로토콜 구간입니다. 3장 TCP 를 축으로 4장이 그 위의 TLS, 5장이 그 위의 응용 프로토콜로 올라가고, 6장이 매체를 무선으로 바꾸며, 7장이 앞의 모두를 공격 탐지에 씁니다.



## 작성된 정독 노트

> 7개 장을 13편에 나눠 담았습니다. 편의 경계는 장 경계가 아니라 그 편이 다루는 주제 축입니다.

| 노트 | 범위 |
|------|------|
| [01-01 패킷 분석기와 Wireshark](./01-01.%ED%8C%A8%ED%82%B7%20%EB%B6%84%EC%84%9D%EA%B8%B0%EC%99%80%20Wireshark.md) | 1장 전체 — 분석기의 용도 넷, libpcap 위의 Wireshark, dumpcap·tshark 분업, 캡처 전 5단계 절차, 타 도구 비교표, 모바일 캡처 |
| [02-01 패킷을 잡는 법](./02-01.%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9E%A1%EB%8A%94%20%EB%B2%95.md) | 2장 캡처 축 — 시작 화면 네 경로, 인터페이스 이름 읽기, promiscuous·snaplen·이름 해석, 캡처 필터(BPF), 파일 자동 분할, tcpdump·snoop, 패킷이 안 잡힐 때 |
| [02-02 잡은 패킷을 읽는 법](./02-02.%EC%9E%A1%EC%9D%80%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9D%BD%EB%8A%94%20%EB%B2%95.md) | 2장 분석 축 — 네 개 창과 컬러링 규칙, 디스플레이 필터와 예제 12개, Packet List 일곱 열, Details 계층별 필드, 이더넷 프레임 구조 |
| [02-03 분석을 돕는 기능들](./02-03.%EB%B6%84%EC%84%9D%EC%9D%84%20%EB%8F%95%EB%8A%94%20%EA%B8%B0%EB%8A%A5%EB%93%A4.md) | 2장 기능 축 — Decode-As, 프로토콜 설정, I/O Graphs, Follow TCP Stream, Export Specified Packets, 방화벽 ACL 규칙 생성 |
| [02-05 터미널에서 같은 화면을 읽는 법](./02-05.%ED%84%B0%EB%AF%B8%EB%84%90%EC%97%90%EC%84%9C%20%EA%B0%99%EC%9D%80%20%ED%99%94%EB%A9%B4%EC%9D%84%20%EC%9D%BD%EB%8A%94%20%EB%B2%95.md) | 2장 터미널 축 — 02-02 의 짝. 예제 캡처 뜨기, `--color`·`-Y`·`-t` 로 색·필터·시간 형식, `-V`·`-O`·`-x` 로 Details 와 Bytes 창, 이더넷과 루프백에서 갈리는 자리 |
| [03-01 TCP 연결의 생애](./03-01.TCP%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EC%83%9D%EC%95%A0.md) | 3장 전반 — TCP 의 여섯 약속, 헤더 20바이트와 필터 이름, 확인 번호를 만드는 식(SYN·FIN 이 번호 하나를 차지하는 이유), 상태 목록과 서버의 여는 경로, 3-way handshake 의 실제 시퀀스 값, 29바이트 데이터로 한 SEQ 검산, 네 번 오가는 종료와 세그먼트 셋 종료, packet#4~#9 표와 CLOSE_WAIT 가 패킷 사이의 시간인 이유, Java 소켓 실습 |
| [03-02 TCP가 어긋날 때](./03-02.TCP%EA%B0%80%20%EC%96%B4%EA%B8%8B%EB%82%A0%20%EB%95%8C.md) | 3장 후반의 이론 — RST 두 자리(거부와 차단의 구분)와 SYN 을 다시 보내는 주체, CLOSE_WAIT 와 close() 한 줄, TIME_WAIT 와 TCB, 지연의 원인 가르기, Wireshark 판정 다섯의 조건 표와 재전송·ZeroWindow·ZeroWindowProbe·중복 ACK. 실행 절차는 03-03 이 맡습니다 |
| [03-03 실습 — 연결의 생애를 직접 잡기](./03-03.%EC%8B%A4%EC%8A%B5%20%E2%80%94%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EC%83%9D%EC%95%A0%EB%A5%BC%20%EC%A7%81%EC%A0%91%20%EC%9E%A1%EA%B8%B0.md) | 3장 실습편 — 리눅스 컨테이너 둘로 만든 캡처 7개, 정상 종료가 세 세그먼트인 이유와 40밀리초 지연 ACK 창, 닫지 않는 클라이언트가 남기는 일곱 줄, 고아 `FIN_WAIT_2` 가 접힐 때의 침묵과 60초를 기준으로 갈리는 ACK·RST, 20초 뒤 종료로 드러난 `CLOSE_WAIT` 구간, `ip.id` 로 가르는 캡처 중복과 재전송 |
| [04-01 TLS 핸드셰이크 읽기](./04-01.TLS%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC%20%EC%9D%BD%EA%B8%B0.md) | 4장 전반 — SSL/TLS 버전 연대, 메시지 열 가지와 필터 번호, Client/Server Hello 구조와 SNI 가 평문으로 먼저 가는 이유, cipher suite 이름 네 조각, 인증서와 조건부 메시지(베낀 인증서가 무력한 이유 포함), 암호화 시작 구간과 그 뒤에도 평문으로 남는 것, Alert 번호 구간 |
| [04-02 열쇠와 실패](./04-02.%EC%97%B4%EC%87%A0%EC%99%80%20%EC%8B%A4%ED%8C%A8.md) | 4장 후반 — 키 교환 방식이 정하는 셋, 디피-헬먼이 한쪽 방향만 쉬운 이유와 곡선 쪽 키 길이, 전방 비밀성, RSA 복호화와 세션 키 공유, nmap·openssl 로 핸드셰이크 실패 디버깅 |
| [05-01 주소를 받아 오는 프로토콜](./05-01.%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EB%B0%9B%EC%95%84%20%EC%98%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C.md) | 5장 전반 — DHCPv6 의 메시지 열셋과 SARR 네 걸음, rapid commit, DHCPv4 의 DORA, BOOTP 와 DHCP 의 관계, dhclient 실습 |
| [05-02 이름과 요청](./05-02.%EC%9D%B4%EB%A6%84%EA%B3%BC%20%EC%9A%94%EC%B2%AD.md) | 5장 후반 — DNS 세 구성요소와 리소스 레코드, 질의 타입별 dig·nslookup, HTTP 응답 시간 찾기, 메서드와 상태 코드 필터 |
| [06-01 무선에서 잡기](./06-01.%EB%AC%B4%EC%84%A0%EC%97%90%EC%84%9C%20%EC%9E%A1%EA%B8%B0.md) | 6장 전체 — monitor 모드가 더 보는 것, 802.11 프레임 네 종류와 서브타입, STA 의 인증·결합 절차, EAPOL, 802.11 프로토콜 스택 |
| [07-01 서비스를 무너뜨리는 공격](./07-01.%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%EB%AC%B4%EB%84%88%EB%9C%A8%EB%A6%AC%EB%8A%94%20%EA%B3%B5%EA%B2%A9.md) | 7장 전반 — DoS 네 갈래, SYN 홍수의 IO Graph 판정과 ACK 절반의 이유, ICMP 홍수와 Conversations 총량 읽기, SSL 홍수, 완화가 서는 층, DrDoS 반사·증폭 |
| [07-02 훔쳐보고 끼어드는 공격](./07-02.%ED%9B%94%EC%B3%90%EB%B3%B4%EA%B3%A0%20%EB%81%BC%EC%96%B4%EB%93%9C%EB%8A%94%20%EA%B3%B5%EA%B2%A9.md) | 7장 후반 — Heartbleed 를 레코드 길이로 판정하기, 스캔에서 감사와 공격이 겹치는 자리, ARP 중복 IP 와 중간자, Endpoints·Protocol Hierarchy 두 통계 창 |



## 학습 상태

> 읽기는 7개 장 전부 끝났고, 남은 것은 자답 회차와 실습입니다.

| 항목 | 값 |
|------|-----|
| 난이도 레벨 | 입문 — **읽기는 7개 장 전부 끝났으나 정착은 그만큼 가지 않았습니다.** 2026-09-14 에 1장을 4-Phase 로 열었을 때, 계획은 Phase 4 자답이었는데 회상할 것이 서 있지 않아 Phase 1 로 내려가 개념을 새로 세웠습니다. 노트가 있다는 것과 그 내용이 머리에 있다는 것이 다르다는 게 이 회차의 소득입니다. 같은 날 1장 Phase 3, 2장 Phase 1·3 까지 이어 갔습니다. 러너의 난이도 규칙(3문항 이상 막힘 또는 전제 오류 시 선행 개념으로)에 따라 기본에서 입문으로 내렸습니다 |
| 막힌 지점 | **2026-09-15 3장을 03-01·03-02 통합으로 Phase 1(예측→채점)에 열었고, 예측 14문항에서 어긋난 인과가 네 축으로 나왔습니다.** 첫째, `TIME_WAIT` 가 많은 것을 ACK 손실의 증거로 읽었습니다. "ACK 가 도착하든 말든 모든 연결이 거친다"고 스스로 답한 직후에도 한 번 더 손실 쪽으로 되돌아갔고, 손실이 전혀 없는 네트워크라는 반례를 주고서야 풀렸습니다. 둘째, SYN 은 데이터가 0바이트이니 ACK 가 +0 이라고 예측했습니다. SYN·FIN 이 번호 하나를 차지한다는 사실(RFC 9293 §3.4)이 빈자리였고, 노트에도 결과만 있고 이유가 없었습니다. 셋째, `CLOSE_WAIT` 를 한 답에서는 B 의 FIN 뒤에, 다른 답에서는 FIN 전에 두었습니다. 넷째, 윈도우가 다시 열렸음을 알리는 일을 받는 쪽이 확인받는 방식으로 예측했는데, 실제로는 보내는 쪽이 떠보는 Zero-Window Probing(RFC 9293 §3.8.6.1)입니다. 반면 `CLOSE_WAIT` 가 애플리케이션 몫인 이유(커널은 데이터를 언제까지 보낼지 모른다), handshake 지연이 순수한 선 지연인 이유, 중복 ACK 가 빠른 재전송을 부르는 순서는 스스로 끌어냈습니다. **1장에서 본 경향이 그대로입니다 — 인과를 끌어내는 쪽은 강하고, 무엇이 없는가(0바이트 세그먼트, ACK 에 대한 ACK 의 부재, 캡처에 찍히지 않는 상태)에서 무너집니다.** 세션 초반에는 제가 SEQ 칸이 첫 바이트 번호라는 정의를 전제로 주지 않아 104 라는 예측이 나왔고, 전제를 표로 보강하자 바로 101 로 고쳤습니다. 이것은 학습자 쪽이 아니라 출제 쪽 보폭 결손입니다. 앞선 기록: **2026-09-14 1장 Phase 1 에서 전제 결손 세 건이 드러났고, 같은 날 Phase 3 실습으로 그중 하나가 닫혔습니다.** 첫째, 패킷 분석기의 자리를 IP 계층으로 잡았습니다 — 링크 계층 프레임과 IP 패킷을 "다음에 오는 것" 으로 보는 순차 감각이 원인이라, 프레임이 IP 패킷을 담는 포함 관계를 먼저 세운 뒤에야 "MAC 이 보이면 안 벗겨진 것" 으로 스스로 뒤집었습니다. **이 축은 실습에서 닫혔습니다** — `tshark -i en0 -c 1 -V` 출력의 맨 위 `Ethernet II` 와 `[Protocols in frame: eth:ethertype:ip:udp:mdns]` 를 보고 바깥과 안쪽을 스스로 갈랐습니다. 둘째, 같은 LAN 에서 프레임을 어느 포트로 보낼지 정하는 장비를 게이트웨이로 지목했습니다 — NAT·포트포워딩은 알고 있으나 스위치의 MAC 테이블이 빈자리였습니다. 셋째, 캡처 전 다섯 관문을 회상하지 못했습니다. 뒤 두 축은 아직 열려 있습니다. 반면 promiscuous 모드는 정의만 듣고 "안 오는 트래픽은 어차피 안 보인다" 를 스스로 끌어냈고, `dumpcap` 이 실제 캡처를 맡는 것도 맞혔습니다 — **개념을 주면 그 자리에서 반례를 만들어 검증하는 쪽은 강하고, 계층 위치·절차 순서 같은 정적 지식의 회상이 약합니다.** 원문 예제 캡처 파일 공백은 그대로입니다 — `normal-connection.pcap`·`RST-01.pcap`·`close_wait.pcap`·`slow_download.pcap`·`two-way-handshake.pcap`·`DHCPv6-Flow-SOLICIT.pcap`·`802.11.pcap` 등이 PDF 에 경로 없이 이름만 나와 있어, 화면 대조 없이 원문 서술과 페이지 이미지로만 작성했습니다 |
| 다음 레슨 후보 | **2026-09-15 갱신 — 3장 Phase 1 의 어긋남 분류를 먼저 닫고, 이어서 3장 Phase 3 로 03-02 §2 의 `CLOSE_WAIT` 를 루프백에서 재현합니다.** 대조에서 packet#7 과 #8 이 무엇을 표현하는지가 가장 오래 막혔고, 원본 `normal-connection.pcap`·`close_wait.pcap` 이 없어 노트 값으로 재구성한 표만 봤기 때문입니다. 재현 캡처에서 "`CLOSE_WAIT` 는 패킷이 아니라 #7 과 #8 사이의 시간"을 직접 확인하는 것이 목표입니다. 아래는 그 이전 계획이며 1·2장 자답은 여전히 유효합니다. **1장 Phase 4 자답이 먼저이고 그다음이 2장 Phase 4 입니다.** 2026-09-14 하루에 1장 Phase 1·3 과 2장 Phase 1·3 을 마쳤습니다. 2장 실습은 자리를 루프백으로 옮겨 돌렸습니다 — 1장 실습이 Wi-Fi 에서 남의 기기 이름을 잡아 왔기 때문이고, `lo0` 에 `python3 -m http.server 18080` 을 띄우면 민감정보가 애초에 생기지 않습니다. 그 회차에서 확인한 것은 `NULL/Loopback` 4바이트 링크 계층, 캡처 필터의 비가역성(14장 대 36장), `-f` BPF 와 `-Y` Wireshark 문법 차이, `--disable-protocol` 과 `-d` 대조, `tcp.reassembled_in` 으로 확정한 재조립, `-z follow` 의 스트림 복원입니다. **예측이 빗나간 자리가 둘 있었고 둘 다 휴리스틱 때문이었습니다** — NFS 가 비표준 포트에서, HTTP 가 `18080` 에서 해석됐습니다. 자답 출제 축은 이 둘을 포함합니다. 3장의 Java 소켓 재현과 6장의 monitor 모드 캡처, 7장의 SYN 홍수·ICMP 홍수는 그 뒤입니다 |
| 최근 검증 결과 | **2026-09-15 03-01·03-02 보강 검증.** 3장 Phase 1 에서 막힌 자리를 본문 문장으로 드러냈습니다. 0바이트 세그먼트, SYN·FIN 이 번호를 차지하는 이유, `CLOSE_WAIT` 가 패킷이 아니라 #7 과 #8 사이의 시간이라는 것, `TIME_WAIT` 와 TCB, Window Update 가 나가는 시점과 Zero-Window Probing 이 그것이고, 근거는 RFC 9293·5681, 커널 ip-sysctl, Wireshark User's Guide 의 축자 인용입니다. 두 편의 `원문 정오` 인용 블록 8개(03-01 셋, 03-02 다섯)는 본문 서술과 "원문은 … 로 적었지만" 한 구절로 옮겼습니다. 도식은 tcp-states 에 서버의 여는 경로를 더하고 선이 라벨을 관통하던 자리를 풀었으며, close-sequence·zero-window 를 넓히고 03-02 세 장의 문장형 라벨 11건을 명사구로 줄였습니다. §1 게이트는 두 편 모두 실패 0 입니다(보강 전 03-02 는 도식 라벨로 실패 1). 7장 전부를 2배로 렌더해 눈으로 보았고, 센서가 못 잡던 레일 점선의 칩·머리글 관통을 세 장에서 찾아 고쳤습니다. §5 적대적 검증은 맥락을 공유하지 않는 서브에이전트가 새 주장 18건을 두 회차로 반박했습니다. 1회차 CONFIRMED 8 · OVERSTATED 7 · REFUTED 3 이었고, 고친 뒤 2회차에서 남은 경미한 지적 5건과 새 과장 1건을 마저 고쳤습니다. **오판 하나를 철회했습니다** — 종료 절의 packet#6 과 #9 확인 번호를 "원문에 없어 계산했다"고 적었는데, 원서 PDF 에 박힌 패킷 목록 스크린샷에 #1~#9 가 모두 찍혀 있었습니다. 텍스트 추출본과 표만 보고 이미지를 꺼내 보지 않은 탓이라 `pdfimages` 로 스크린샷을 뽑아 대조했습니다. 같은 절 전이 표(Sr. No. 1~10)의 5행 SEQ·ACK 뒤바뀜은 이 대조에서 새로 확인해 본문에 적었습니다. 앞선 회차 기록: **2026-09-05 문서 전체 검증. 정본 07-verification §1(12종)·§2·§4·§5 를 문서 14개와 도식 42장에 전수로 걸었습니다.** §5 적대적 검증은 정본이 정한 대로 맥락을 공유하지 않는 서브에이전트가 "전부 틀렸다"를 기본값으로 정오 주장 35건을 하나씩 반박하는 형태로 돌렸고, 판정은 CONFIRMED 31 · OVERSTATED 3 · REFUTED 1 · MISQUOTE 0 입니다. **오인 고발 1건을 철회했습니다** — `tcp_max_tw_buckets` 주석이 "방향이 반대"라고 적었으나, 커널 문서 해당 항목의 세 번째 문장이 "이 한계는 오직 단순한 DoS 공격을 막기 위해 존재하므로 인위적으로 낮추지 말고 오히려 키우라"고 적어 원문 주석과 같은 말을 합니다. 제가 앞 두 문장만 인용하고 반대 결론을 냈습니다. 격하 3건은 `tcp_syn_retries`(원문 산문은 옳은 손잡이를 지목함)·nmap 라벨(셋 중 하나만 실제 오류)·1장 첫 문장(편집 결함이지 사실 오류 아님)이며 전부 "노트의 읽기"로 옮겼습니다. 기계 검증에서 결함 4건을 고쳤습니다 — 원문에 없는 파일명 `decrypt-ssl-01.pcap`(원문은 `decrypt-ssl01.pcap`), 산문 내 유니코드 화살표, §11 미등록 사설 IP 4개, MOC 절 요약 6곳 누락. 앞선 회차 기록: **7장 2편 추가로 전 7장 13편 완성. 13편 전부 §1 센서 12종 + 벽 단락 통과, 도식 42장 타입 선언·오버플로·겹침·가독성 전부 통과.** 7장에서 새로 확인한 값은 Conversations 의 999,599패킷·41,983,438바이트·41.96초, Heartbleed 프레임 15·16 의 레코드 길이 112·144, Protocol Hierarchy 의 계층별 비율, Endpoints 의 `IPv4: 17` 탭이며 전부 300dpi 페이지 이미지에서 판독했습니다. Wireshark 4.6.8 의 `dftest`·`tshark -G fields` 로 필터 표기를 직접 실측해 `ssl.` 별칭의 deprecated 경고와 `tls.heartbeat_message.payload_length.invalid` 필드 존재를 확인했습니다. 앞선 1~6장 회차의 기록: **1~6장 11편 작성. §1 센서 12종 + 벽 단락 전수 통과, 도식 34장 타입 선언·오버플로·린트 통과, 죽은 링크 0건, 각주 참조·정의 일치, 민감정보 0건.** 원문 값 124개를 추출 텍스트와 기계 대조했고, pdftotext 가 표의 열을 뒤섞은 자리는 300dpi 페이지 이미지로 직접 판독했습니다. 책 밖 보강은 RFC 5246·5681·6891·8415·8446·9293, Linux 커널 문서, tcpdump·dumpcap·tshark man page, IANA 레지스트리, Wireshark User's Guide·Wiki·릴리스 노트로 각각 확인했습니다. 정오 후보 1건은 반증돼 철회했습니다 — MAC 이름 해석의 IP 변환 서술은 공식 User's Guide 가 세 갈래 중 첫째로 적고 있어 정오가 아니라 *공백*이었습니다. **다만 그 회차에서 `dd-legibility-check.py` 를 돌리지 않아 도식 34장 중 10장에 한글 10px 라벨 48건이 남아 있었습니다. 7장 회차에서 전수 발견해 11px 이상으로 올렸고, 범례 줄과 본문이 겹친 2장도 함께 고쳤습니다.** |
| 복습 회차 | 0회차 (미실시) — 1장은 Phase 4 자답을 통과한 뒤에 큐에서 `대기` 로 올라갑니다 |



## 출처·톤 메모

> 이 폴더의 문서를 고칠 때 지키는 다섯 가지입니다. 원문이 1차 자료라는 것이 그 중심입니다.

- **원문이 1차 자료입니다.** 사실·수치·필터 문자열·명령은 `pdftotext` 로 추출한 절 PDF 본문과 `pdftoppm` 으로 렌더한 페이지 이미지에서만 가져옵니다.
- **이 책은 스크린샷이 내용을 나릅니다.** 본문에 "as shown in the following screenshot" 만 남고 정보가 그림에만 있는 자리가 많아, 표와 도해는 텍스트 추출본이 아니라 300dpi 로 렌더한 페이지 이미지로 판독했습니다. `pdftotext` 는 이 책의 표에서 열 순서를 섞습니다.
- **1장 일부 그림은 PDF 에 렌더되지 않았습니다.** O'Reilly Learning 인쇄 캡처라 지연 로딩 이미지가 빈 영역으로 남은 자리가 있습니다. 없는 그림은 없는 것으로 두고 도식으로 지어내지 않았습니다.
- **책 밖 보강은 4.6 대조에 한정합니다.** 현행 동작은 Wireshark 공식 문서·릴리스 노트·man page 로만 확인하고 각주로 링크를 답니다. 블로그·요약글은 근거로 쓰지 않습니다.
- **원문의 오류도 조용히 지우지 않습니다.** 본문은 1차 자료가 말하는 올바른 내용으로 쓰고, 원문 표기는 「판본 주의」와 같은 방식으로 "원문은 … 로 적었지만" 한 구절로만 남겨 책을 다시 폈을 때 그 자리에서 대조되게 합니다. 저자가 *틀리게 적은 것*은 이렇게 본문에 녹이고, *안 적은 것*은 "노트의 읽기"로 표시합니다. 2026-09-15 에 03-01·03-02 를 이 방식으로 옮겼고, 다른 장에는 아직 `> **원문 정오**:` 인용 블록이 남아 있습니다.

[^ssl-tls]: Wireshark 3.0.0 릴리스 노트 — "The SSL dissector has been renamed to TLS. As with BOOTP the old "ssl.\*" display filter fields are supported but may be removed in a future release." <https://www.wireshark.org/docs/relnotes/wireshark-3.0.0.html>
