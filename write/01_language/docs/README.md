---
title: 01_language/docs — 언어 공식문서 정독
tags: [moc, go, official-docs]
status: draft
related:
  - ../README.md
  - ../book/lgo_learning-go/README.md
updated: 2026-10-07
---

# 01_language/docs — 언어 공식문서 정독

---

> 언어별 공식문서와 표준 라이브러리 구현을 1차 자료로 삼아 언어 명세와 핵심 패키지 계약을 정독하는 자리입니다. 전체 문법을 순서대로 훑는 일은 [book/](../book/)의 정독 노트가 맡습니다.

## 폴더 규칙

> 하위 폴더는 공식문서 경로 슬러그와 1:1 로 맞춥니다. pkg.go.dev/net → go/net/, pkg.go.dev/net/http → go/net-http/ 로 둡니다. go/ 를 앞에 두는 이유는 01_language 가 Java 도 품기 때문입니다. 책 정독은 book/ 이 맡습니다.

| 폴더 | 대응 공식문서 섹션 |
|------|-------------------|
| [go/net/](go/net/README.md) | `pkg.go.dev/net` |
| [go/net-http/](go/net-http/README.md) | `pkg.go.dev/net/http` |

새 주제를 쓸 때는 그 문서의 1차 근거가 가장 많이 나오는 섹션 폴더에 넣습니다. 한 문서가 여러 섹션을 가로지르는 일은 흔하므로, 나머지 섹션은 프론트매터 `source` 와 본문 각주로 남깁니다. 해당 섹션 폴더가 아직 없으면 그때 만들고 이 표에 한 줄을 더합니다.

파일명은 `05-file-placement.md` §5.1 의 `{장}-{절}.{제목}.md` 를 따릅니다. 번호는 작성 순서가 아니라 주제 묶음 기준이라, 같은 묶음이 늘면 `01-02` 로, 묶음이 바뀌면 `02-01` 로 넘어갑니다.



## 문서 목록

> 폴더별 현재 문서입니다. 각 폴더 README 에 그 섹션의 읽기 순서가 있습니다.

| 폴더 | 번호 | 제목 |
|------|------|------|
| go/net | 01-01 | [Conn·Listener·PacketConn·Addr](go/net/01-01.Conn%C2%B7Listener%C2%B7PacketConn%C2%B7Addr.md) |
| go/net | 01-02 | [netpoller](go/net/01-02.netpoller.md) |
| go/net | 02-01 | [Dial·Dialer](go/net/02-01.Dial%C2%B7Dialer.md) |
| go/net | 02-02 | [Listen·ListenConfig·TCPListener](go/net/02-02.Listen%C2%B7ListenConfig%C2%B7TCPListener.md) |
| go/net | 03-01 | [Conn.Read·Conn.Write·Close](go/net/03-01.Conn.Read%C2%B7Conn.Write%C2%B7Close.md) |
| go/net | 03-02 | [SetDeadline·SetReadDeadline·SetWriteDeadline](go/net/03-02.SetDeadline%C2%B7SetReadDeadline%C2%B7SetWriteDeadline.md) |
| go/net | 03-03 | [Error·OpError·DNSError](go/net/03-03.Error%C2%B7OpError%C2%B7DNSError.md) |
| go/net | 04-01 | [TCPConn](go/net/04-01.TCPConn.md) |
| go/net | 04-02 | [UDPConn·ListenPacket](go/net/04-02.UDPConn%C2%B7ListenPacket.md) |
| go/net-http | 01-01 | [Client·Transport·Server·Handler](go/net-http/01-01.Client%C2%B7Transport%C2%B7Server%C2%B7Handler.md) |
| go/net-http | 02-01 | [Client·Transport](go/net-http/02-01.Client%C2%B7Transport.md) |
| go/net-http | 02-02 | [Client.Timeout·Transport 타임아웃·httptrace](go/net-http/02-02.Client.Timeout%C2%B7Transport%20%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%C2%B7httptrace.md) |
| go/net-http | 03-01 | [Server·ServeMux·Handler](go/net-http/03-01.Server%C2%B7ServeMux%C2%B7Handler.md) |
| go/net-http | 03-02 | [Server 타임아웃·Shutdown](go/net-http/03-02.Server%20%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%C2%B7Shutdown.md) |



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [01_language MOC](../README.md) — 대분류 지도
- [Learning Go 정독본](../book/lgo_learning-go/README.md) — Go 문법·타입·인터페이스·동시성 기초
- [Network Programming with Go 정독본](../../02_os/book/npg_network-programming-with-go/README.md) — TCP/IP·소켓 프로그래밍 책 정독
- [gonet-lab 학습 문서](../../02_os/project/gonet-lab/README.md) — 리눅스 커널 소켓·패킷·시스템 콜 실측 관측
