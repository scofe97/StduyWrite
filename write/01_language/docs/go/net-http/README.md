---
title: 01_language/docs/go/net-http — Go net/http 패키지 공식문서 정독
tags: [moc, go, net-http, official-docs]
status: draft
related:
  - ../../README.md
  - ../net/README.md
  - ../../../book/lgo_learning-go/README.md
updated: 2026-10-07
---

# 01_language/docs/go/net-http — Go net/http 패키지 공식문서 정독

---

> Go 표준 라이브러리 net/http 패키지의 API 계약과 내부 동작(go1.25.1)을 정독하는 섹션입니다. 대응하는 공식문서는 pkg.go.dev/net/http 입니다.

## 문서 목록

> 파일 번호가 읽기 순서입니다. 각 문서는 HTTP 클라이언트·전송 계층·서버·핸들러의 계약과 내부 구현을 다룹니다.

| 장 묶음 | 번호 | 제목 | 한 줄 소개 |
|---------|------|------|-----------|
| 01 패키지 구조 | 01-01 | [Client·Transport·Server·Handler](01-01.Client%C2%B7Transport%C2%B7Server%C2%B7Handler.md) | Client·Transport 발신 축과 Server·Handler 수신 축의 역할 분담, 인터페이스 계약과 기본 동작 |
| 02 클라이언트 | 02-01 | [Client·Transport](02-01.Client%C2%B7Transport.md) | Client 오케스트레이션과 RoundTripper 계약, Transport 의 persistConn 커넥션 풀링과 TCP 연결 재사용 |
| 02 클라이언트 | 02-02 | [Client.Timeout·Transport 타임아웃·httptrace](02-02.Client.Timeout%C2%B7Transport%20%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%C2%B7httptrace.md) | 전체 트랜잭션을 감싸는 Client.Timeout 과 네트워크 구간별 Transport 타임아웃, httptrace 계측 훅 |
| 03 서버 | 03-01 | [Server·ServeMux·Handler](03-01.Server%C2%B7ServeMux%C2%B7Handler.md) | Server.Serve 연결 수락 루프, conn.serve 전용 고루틴 디스패치, Go 1.22 ServeMux 패턴 라우팅과 핸들러 격리 |
| 03 서버 | 03-02 | [Server 타임아웃·Shutdown](03-02.Server%20%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%C2%B7Shutdown.md) | 헤더·본문·핸들러·유휴 소켓 데드라인 4대 타임아웃과 Graceful Shutdown 의 신규 차단 및 연결 회수 |



## 이 섹션이 다른 노트와 나누는 일

> HTTP 관련 지식이 나뉘는 기준입니다.

Learning Go [13-04](../../../book/lgo_learning-go/13-04.net-http%20%EB%8A%94%20%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%EC%9D%84%20%EC%A7%81%EC%A0%91%20%EC%A0%95%ED%95%98%EA%B3%A0%20%EB%AF%B8%EB%93%A4%EC%9B%A8%EC%96%B4%EB%8A%94%20Handler%20%EB%A5%BC%20%EA%B0%90%EC%8B%B8%EB%A9%B0%20slog%20%EB%A1%9C%20%EA%B5%AC%EC%A1%B0%ED%99%94%20%EB%A1%9C%EA%B7%B8%EB%A5%BC%20%EB%82%A8%EA%B9%81%EB%8B%88%EB%8B%A4.md)(net/http 타임아웃·미들웨어)와 겹치는 부분은 해당 편으로 링크하여 연결합니다. 이 섹션은 일반 튜토리얼이 아니라 `net/http` 표준 라이브러리의 핵심 인터페이스 계약과 소스 수준의 구조에 집중합니다.



## 관련 문서

> 이 폴더가 딛고 서는 이웃입니다.

- [docs MOC](../../README.md) — 언어 공식문서 정독 전체 목록
- [net 섹션](../net/README.md) — 네트워크 기초 I/O 계층 정독
- [Learning Go 정독본](../../../book/lgo_learning-go/README.md) — Go 언어 문법과 표준 라이브러리 기초
