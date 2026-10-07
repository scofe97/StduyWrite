---
title: 01_language/docs/go/net — Go net 패키지 공식문서 정독
tags: [moc, go, net, official-docs]
status: draft
related:
  - ../../README.md
  - ../net-http/README.md
  - ../../../../02_os/book/npg_network-programming-with-go/README.md
updated: 2026-10-07
---

# 01_language/docs/go/net — Go net 패키지 공식문서 정독

---

> Go 표준 라이브러리 net 패키지의 API 계약과 내부 구현(go1.25.1)을 정독하는 섹션입니다. 대응하는 공식문서는 pkg.go.dev/net 입니다.

## 문서 목록

> 파일 번호가 읽기 순서입니다. 각 문서는 공식문서가 약속하는 인터페이스 계약과 Go 런타임·소켓 계층의 내부 구현을 다룹니다.

| 장 묶음 | 번호 | 제목 | 한 줄 소개 |
|---------|------|------|-----------|
| 01 패키지 구조 | 01-01 | [Conn·Listener·PacketConn·Addr](01-01.Conn%C2%B7Listener%C2%B7PacketConn%C2%B7Addr.md) | Conn·Listener·PacketConn 인터페이스와 TCPConn·UDPConn·UnixConn·IPConn 구체 타입, 내부 conn·netFD 계층 |
| 01 패키지 구조 | 01-02 | [netpoller](01-02.netpoller.md) | EAGAIN 에서 gopark 으로 고루틴을 재우고 epoll/kqueue 가 unpark 하는 netpoller 논블로킹 I/O 메커니즘 |
| 02 연결 맺기 | 02-01 | [Dial·Dialer](02-01.Dial%C2%B7Dialer.md) | 목적지 연결 관문 net.Dial 과 Happy Eyeballs(IPv6/IPv4 경합), 타임아웃 배분, 저수준 소켓 훅 Dialer 제어 |
| 02 연결 맺기 | 02-02 | [Listen·ListenConfig·TCPListener](02-02.Listen%C2%B7ListenConfig%C2%B7TCPListener.md) | 서버 수신 소켓 바인딩, 커널 TCP 백로그 큐와 Accept 메커니즘, ListenConfig 및 TCPListener 생명주기 |
| 03 연결 위의 I/O | 03-01 | [Conn.Read·Conn.Write·Close](03-01.Conn.Read%C2%B7Conn.Write%C2%B7Close.md) | io.Reader/Writer 계약 준수, 부분 읽기와 완전 쓰기 루프, fdMutex 기반 동시성 제어와 evict 해제 |
| 03 연결 위의 I/O | 03-02 | [SetDeadline·SetReadDeadline·SetWriteDeadline](03-02.SetDeadline%C2%B7SetReadDeadline%C2%B7SetWriteDeadline.md) | 절대 시각 데드라인 계약, 런타임 타이머와 poll.FD 상호작용, 유휴 타임아웃 갱신 패턴과 바쁜 루프 방지 |
| 03 연결 위의 I/O | 03-03 | [Error·OpError·DNSError](03-03.Error%C2%B7OpError%C2%B7DNSError.md) | net.Error 인터페이스, *net.OpError 및 *net.DNSError 구조체, errors.Is/As 에러 계통 판별과 타임아웃 감지 |
| 04 소켓 손잡이와 다른 전송 | 04-01 | [TCPConn](04-01.TCPConn.md) | TCP 저수준 소켓 옵션(KeepAlive, NoDelay, Linger) 제어와 splice·sendfile 제로카피 커널 최적화 |
| 04 소켓 손잡이와 다른 전송 | 04-02 | [UDPConn·ListenPacket](04-02.UDPConn%C2%B7ListenPacket.md) | 비연결 데이터그램 통신, PacketConn 인터페이스와 UDPConn, connected UDP 및 수신 버퍼 잘림(truncation) |
| 05 이름 해석 | 05-01 | [Resolver](05-01.Resolver.md) | 호스트 이름 해석기 Resolver 와 DefaultResolver, 순수 Go 와 cgo 듀얼 엔진 판정 규칙 및 DNS 패킷 교환 |



## 이 섹션이 다른 노트와 나누는 일

> 네트워크와 Go 를 다루는 세 노트가 각자 맡은 초점입니다.

- NPG 정독본([02_os/book/npg_network-programming-with-go/](../../../../02_os/book/npg_network-programming-with-go/README.md)) — 책의 장·절과 Listing 예제 코드를 따라가며 소켓 프로그래밍을 학습하는 정독 축입니다.
- gonet-lab([02_os/project/gonet-lab/](../../../../02_os/project/gonet-lab/README.md)) — 커널 관측(strace, proc, tcpdump, tc netem)을 통해 네트워크 프로토콜 동작을 실험하고 실측하는 관측 축입니다.
- 이 섹션([01_language/docs/go/net/](README.md)) — 공식 문서(`pkg.go.dev/net`)의 계약을 정본으로 삼고 Go 표준 라이브러리 소스(go1.25.1)로 내부 동작 근거를 밝히는 계약과 소스 축입니다.



## 관련 문서

> 이 폴더가 딛고 서는 이웃입니다.

- [docs MOC](../../README.md) — 언어 공식문서 정독 전체 목록
- [net-http 섹션](../net-http/README.md) — HTTP 클라이언트·서버 표준 라이브러리 정독
- [Network Programming with Go 정독본](../../../../02_os/book/npg_network-programming-with-go/README.md) — 네트워크 프로그래밍 책 정독
- [gonet-lab 학습 문서](../../../../02_os/project/gonet-lab/README.md) — 소켓·패킷 커널 실측 관측
