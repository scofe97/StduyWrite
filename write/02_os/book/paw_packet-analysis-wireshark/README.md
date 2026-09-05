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
  - ./02-01.%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9E%A1%EB%8A%94%20%EB%B2%95.md
  - ./02-02.%EC%9E%A1%EC%9D%80%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9D%BD%EB%8A%94%20%EB%B2%95.md
  - ./02-03.%EB%B6%84%EC%84%9D%EC%9D%84%20%EB%8F%95%EB%8A%94%20%EA%B8%B0%EB%8A%A5%EB%93%A4.md
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
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않습니다
  blocked_count: 0
  next_lesson: "Phase 4 자답 회차. 7개 장 노트가 모두 섰으므로 다음은 새 장이 아니라 회상 문항 자답과 실습입니다"
updated: 2026-09-05
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

> 개념은 원문을 1차 자료로 그대로 두고, 조작 절차와 필터 표기만 현행 4.6 기준을 나란히 적습니다.

원문의 스크린샷은 전부 **Wireshark 1.12.6** 입니다. 현행 안정판은 **4.6** 이고, 그 사이에 시작 화면 구성과 대화상자 여럿이 다시 설계됐으며 `ssl` 디스플레이 필터가 `tls` 로 개명됐습니다.[^ssl-tls]

정독 노트는 이렇게 다룹니다. **개념은 원문을 1차 자료로 그대로 두고, 조작 절차와 필터 표기만 4.6 기준을 함께 적습니다.** 캡처 필터와 디스플레이 필터가 왜 갈리는지, promiscuous 모드가 무엇을 바꾸는지, 네 개 창이 같은 바이트를 어떻게 나눠 보여주는지는 판본을 타지 않습니다. 바뀐 것은 메뉴 경로와 대화상자 이름 쪽입니다. 바뀐 자리에는 절 안에 `> **지금은 다릅니다 (4.6)**` 인용 블록을 두어 그 자리에서 대조됩니다.



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
| [03-01 TCP 연결의 생애](./03-01.TCP%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EC%83%9D%EC%95%A0.md) | 3장 전반 — TCP 의 여섯 약속, 헤더 20바이트와 필터 이름, 상태 목록, 3-way handshake 의 실제 시퀀스 값, 데이터 전송, 네 번 오가는 종료, Java 소켓 실습 |
| [03-02 TCP가 어긋날 때](./03-02.TCP%EA%B0%80%20%EC%96%B4%EA%B8%8B%EB%82%A0%20%EB%95%8C.md) | 3장 후반 — RST 두 자리, CLOSE_WAIT 재현과 해결, TIME_WAIT, 지연의 원인 가르기, 재전송·ZeroWindow·Window Update·중복 ACK |
| [04-01 TLS 핸드셰이크 읽기](./04-01.TLS%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC%20%EC%9D%BD%EA%B8%B0.md) | 4장 전반 — SSL/TLS 버전 연대, 메시지 열 가지와 필터 번호, Client/Server Hello 구조, 인증서와 키 교환 메시지, 암호화 시작 지점, Alert 목록 |
| [04-02 열쇠와 실패](./04-02.%EC%97%B4%EC%87%A0%EC%99%80%20%EC%8B%A4%ED%8C%A8.md) | 4장 후반 — 키 교환 방식이 정하는 셋, 전방 비밀성, RSA 복호화와 세션 키 공유, nmap·openssl 로 핸드셰이크 실패 디버깅 |
| [05-01 주소를 받아 오는 프로토콜](./05-01.%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EB%B0%9B%EC%95%84%20%EC%98%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C.md) | 5장 전반 — DHCPv6 의 메시지 열셋과 SARR 네 걸음, rapid commit, DHCPv4 의 DORA, BOOTP 와 DHCP 의 관계, dhclient 실습 |
| [05-02 이름과 요청](./05-02.%EC%9D%B4%EB%A6%84%EA%B3%BC%20%EC%9A%94%EC%B2%AD.md) | 5장 후반 — DNS 세 구성요소와 리소스 레코드, 질의 타입별 dig·nslookup, HTTP 응답 시간 찾기, 메서드와 상태 코드 필터 |
| [06-01 무선에서 잡기](./06-01.%EB%AC%B4%EC%84%A0%EC%97%90%EC%84%9C%20%EC%9E%A1%EA%B8%B0.md) | 6장 전체 — monitor 모드가 더 보는 것, 802.11 프레임 네 종류와 서브타입, STA 의 인증·결합 절차, EAPOL, 802.11 프로토콜 스택 |
| [07-01 서비스를 무너뜨리는 공격](./07-01.%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%EB%AC%B4%EB%84%88%EB%9C%A8%EB%A6%AC%EB%8A%94%20%EA%B3%B5%EA%B2%A9.md) | 7장 전반 — DoS 네 갈래, SYN 홍수의 IO Graph 판정과 ACK 절반의 이유, ICMP 홍수와 Conversations 총량 읽기, SSL 홍수, 완화가 서는 층, DrDoS 반사·증폭 |
| [07-02 훔쳐보고 끼어드는 공격](./07-02.%ED%9B%94%EC%B3%90%EB%B3%B4%EA%B3%A0%20%EB%81%BC%EC%96%B4%EB%93%9C%EB%8A%94%20%EA%B3%B5%EA%B2%A9.md) | 7장 후반 — Heartbleed 를 레코드 길이로 판정하기, 스캔에서 감사와 공격이 겹치는 자리, ARP 중복 IP 와 중간자, Endpoints·Protocol Hierarchy 두 통계 창 |



## 학습 상태

> 읽기는 7개 장 전부 끝났고, 남은 것은 자답 회차와 실습입니다.

| 항목 | 값 |
|------|-----|
| 난이도 레벨 | 기본 — **7개 장을 모두 마쳤습니다.** 도구 사용법(1·2장), TCP 의 상태와 이상 신호(3장), TLS 협상과 복호화 경계(4장), 응용 프로토콜의 질의·응답(5장), 무선 캡처의 모드와 프레임(6장), 공격 탐지(7장)까지 훑었습니다. 읽기는 끝났고 자답과 실습이 남았습니다 |
| 막힌 지점 | 자답 미실시라 막힘이 드러날 기회가 아직 없었습니다. 실습 공백이 큽니다 — 원문이 인용하는 예제 캡처 파일(`normal-connection.pcap`·`RST-01.pcap`·`close_wait.pcap`·`slow_download.pcap`·`two-way-handshake.pcap`·`DHCPv6-Flow-SOLICIT.pcap`·`802.11.pcap` 등)이 PDF 에 경로 없이 이름만 나와 있어, 화면 대조 없이 원문 서술과 페이지 이미지로만 작성했습니다. 3장의 Java 소켓 실습과 6장의 monitor 모드 캡처는 직접 재현할 수 있는 축이라 다음 회차 후보입니다 |
| 다음 레슨 후보 | 새 장이 아니라 **Phase 4 자답 회차**입니다. 각 편의 회상 문항을 노트를 덮고 답해 보고, 어긋난 자리만 되짚습니다. 그다음이 실습입니다 — 3장의 Java 소켓 재현과 6장의 monitor 모드 캡처는 맥북에서 바로 만들 수 있고, 7장의 SYN 홍수·ICMP 홍수는 로컬에서 직접 캡처를 떠 IO Graph 와 Conversations 를 실제로 열어 볼 수 있습니다 |
| 최근 검증 결과 | **2026-09-05 문서 전체 검증. 정본 07-verification §1(12종)·§2·§4·§5 를 문서 14개와 도식 42장에 전수로 걸었습니다.** §5 적대적 검증은 정본이 정한 대로 맥락을 공유하지 않는 서브에이전트가 "전부 틀렸다"를 기본값으로 정오 주장 35건을 하나씩 반박하는 형태로 돌렸고, 판정은 CONFIRMED 31 · OVERSTATED 3 · REFUTED 1 · MISQUOTE 0 입니다. **오인 고발 1건을 철회했습니다** — `tcp_max_tw_buckets` 주석이 "방향이 반대"라고 적었으나, 커널 문서 해당 항목의 세 번째 문장이 "이 한계는 오직 단순한 DoS 공격을 막기 위해 존재하므로 인위적으로 낮추지 말고 오히려 키우라"고 적어 원문 주석과 같은 말을 합니다. 제가 앞 두 문장만 인용하고 반대 결론을 냈습니다. 격하 3건은 `tcp_syn_retries`(원문 산문은 옳은 손잡이를 지목함)·nmap 라벨(셋 중 하나만 실제 오류)·1장 첫 문장(편집 결함이지 사실 오류 아님)이며 전부 "노트의 읽기"로 옮겼습니다. 기계 검증에서 결함 4건을 고쳤습니다 — 원문에 없는 파일명 `decrypt-ssl-01.pcap`(원문은 `decrypt-ssl01.pcap`), 산문 내 유니코드 화살표, §11 미등록 사설 IP 4개, MOC 절 요약 6곳 누락. 앞선 회차 기록: **7장 2편 추가로 전 7장 13편 완성. 13편 전부 §1 센서 12종 + 벽 단락 통과, 도식 42장 타입 선언·오버플로·겹침·가독성 전부 통과.** 7장에서 새로 확인한 값은 Conversations 의 999,599패킷·41,983,438바이트·41.96초, Heartbleed 프레임 15·16 의 레코드 길이 112·144, Protocol Hierarchy 의 계층별 비율, Endpoints 의 `IPv4: 17` 탭이며 전부 300dpi 페이지 이미지에서 판독했습니다. Wireshark 4.6.8 의 `dftest`·`tshark -G fields` 로 필터 표기를 직접 실측해 `ssl.` 별칭의 deprecated 경고와 `tls.heartbeat_message.payload_length.invalid` 필드 존재를 확인했습니다. 앞선 1~6장 회차의 기록: **1~6장 11편 작성. §1 센서 12종 + 벽 단락 전수 통과, 도식 34장 타입 선언·오버플로·린트 통과, 죽은 링크 0건, 각주 참조·정의 일치, 민감정보 0건.** 원문 값 124개를 추출 텍스트와 기계 대조했고, pdftotext 가 표의 열을 뒤섞은 자리는 300dpi 페이지 이미지로 직접 판독했습니다. 책 밖 보강은 RFC 5246·5681·6891·8415·8446·9293, Linux 커널 문서, tcpdump·dumpcap·tshark man page, IANA 레지스트리, Wireshark User's Guide·Wiki·릴리스 노트로 각각 확인했습니다. 정오 후보 1건은 반증돼 철회했습니다 — MAC 이름 해석의 IP 변환 서술은 공식 User's Guide 가 세 갈래 중 첫째로 적고 있어 정오가 아니라 *공백*이었습니다. **다만 그 회차에서 `dd-legibility-check.py` 를 돌리지 않아 도식 34장 중 10장에 한글 10px 라벨 48건이 남아 있었습니다. 7장 회차에서 전수 발견해 11px 이상으로 올렸고, 범례 줄과 본문이 겹친 2장도 함께 고쳤습니다.** |
| 복습 회차 | 0회차 (미실시) |



## 출처·톤 메모

> 이 폴더의 문서를 고칠 때 지키는 다섯 가지입니다. 원문이 1차 자료라는 것이 그 중심입니다.

- **원문이 1차 자료입니다.** 사실·수치·필터 문자열·명령은 `pdftotext` 로 추출한 절 PDF 본문과 `pdftoppm` 으로 렌더한 페이지 이미지에서만 가져옵니다.
- **이 책은 스크린샷이 내용을 나릅니다.** 본문에 "as shown in the following screenshot" 만 남고 정보가 그림에만 있는 자리가 많아, 표와 도해는 텍스트 추출본이 아니라 300dpi 로 렌더한 페이지 이미지로 판독했습니다. `pdftotext` 는 이 책의 표에서 열 순서를 섞습니다.
- **1장 일부 그림은 PDF 에 렌더되지 않았습니다.** O'Reilly Learning 인쇄 캡처라 지연 로딩 이미지가 빈 영역으로 남은 자리가 있습니다. 없는 그림은 없는 것으로 두고 도식으로 지어내지 않았습니다.
- **책 밖 보강은 4.6 대조에 한정합니다.** 현행 동작은 Wireshark 공식 문서·릴리스 노트·man page 로만 확인하고 각주로 링크를 답니다. 블로그·요약글은 근거로 쓰지 않습니다.
- **원문의 오류는 조용히 고치지 않습니다.** `> **원문 정오**:` 인용 블록으로 병기해, 학습자가 책을 다시 폈을 때 대응되게 합니다. 저자가 *틀리게 적은 것*만 정오이고, *안 적은 것*은 "노트의 읽기"로 표시합니다.

[^ssl-tls]: Wireshark 3.0.0 릴리스 노트 — "The SSL dissector has been renamed to TLS. As with BOOTP the old "ssl.\*" display filter fields are supported but may be removed in a future release." <https://www.wireshark.org/docs/relnotes/wireshark-3.0.0.html>
