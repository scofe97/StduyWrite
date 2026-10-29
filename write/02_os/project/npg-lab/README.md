---
title: npg-lab — 프로젝트 인덱스
tags: [moc, study-index, lab, networking, go, http, reverse-proxy]
status: draft
source:
  - ~/study/runners-lab/net/npg  # 책 Network Programming with Go 를 따라 만드는 실습 저장소, 8장부터 리버스 프록시 npgproxy
  - https://github.com/scofe97/StudyLab/tree/0873c0f/net/npg  # 옛 npg-lab main 0dbf86f·태그 v0.8.0 와 같은 커밋
  - docs/adr/0011-reverse-proxy-product.md@73fbcee  # 8장부터 리버스 프록시를 만드는 결정
  - docs/adr/0012-upstream-deadlines-and-pool.md@0dbf86f  # 업스트림 기한·연결 풀 결정
  - docs/adr/0013-upstream-retry-and-idempotency.md@0dbf86f  # 재시도·멱등성 결정
related:
  - ../../book/npg_network-programming-with-go/README.md
  - ../gonet-lab/README.md
  - ./01-01.기본값 리버스 프록시가 겪는 장애 - 느린 검색·포트 고갈·POST 502·회복 지연·중복 등록.md
updated: "2026-10-29"
---

# npg-lab — 프로젝트 인덱스

---

> Network Programming with Go 실습을 바탕으로 리버스 프록시 npgproxy를 구현하고 장애 상황을 관측하는 프로젝트 인덱스입니다. 실제 소스코드는 실습 저장소에 보관하고 이 폴더에는 장별 학습 문서만 둡니다. 설계 결정(ADR)은 실습 저장소의 `docs/adr/`에 있습니다.

## 이 폴더는 무엇인가

> 책 예제 코드를 따라 치는 실습과 분리하여 아키텍처와 장애 분석을 학습 문서로 정리하는 공간입니다. 책 노트와 중복되는 네트워크 기초 이론은 링크로 대체하고 프록시 구현과 운영 관점의 분석에 집중합니다.

실습 소스코드는 `~/study/runners-lab/net/npg`(GitHub 모노레포 `scofe97/StudyLab`)에 보관되어 있습니다. 프로젝트는 전달 계층(`internal/proxy/`), 프록시 실행 진입점(`cmd/npgproxy`), 관측 화면(`cmd/npgwatch`), 장애 훈련용 가짜 백엔드(`cmd/fakeinv`), 부하 도구(`cmd/npgload`)로 구성됩니다.

책의 정독 기록은 책 노트 폴더에 별도로 정리되어 있습니다. 따라서 이 폴더의 학습 문서는 책 정독 노트와 겹치는 기초 내용을 반복 서술하지 않고 해당 문서로 연결합니다.



## 왜 리버스 프록시인가

> 책 8장의 HTTP 클라이언트를 백엔드로 요청을 중계하는 업스트림 계층으로 확장하여 실무 웹서버 구조로 구현합니다. 연결 풀 관리와 타임아웃, 실패 분류를 직접 다루며 Envoy나 Nginx의 업스트림 처리 원리를 체득합니다.

ADR 0011에 따라 8장부터 단순 클라이언트 작성을 넘어 실제 Envoy나 Nginx 같은 웹서버처럼 동작하는 리버스 프록시를 제작합니다. 책 8장에서 다루는 HTTP 클라이언트는 프록시에서 백엔드로 향하는 연결 풀을 관리하고 기한을 제어하는 업스트림 층의 핵심 동작과 일치합니다.

Envoy의 클러스터나 Nginx의 업스트림처럼 백엔드 전달 계층을 직접 구성해 봅니다. 8장은 프록시의 업스트림 전달 층을 구현하고 9장에서는 다운스트림 수신 층을 다루며 10장에서는 Caddy와 비교합니다. 기본값 리버스 프록시가 겪는 장애 분석과 세부 시나리오는 [01-01 학습 문서](./01-01.기본값%20리버스%20프록시가%20겪는%20장애%20-%20느린%20검색·포트%20고갈·POST%20502·회복%20지연·중복%20등록.md)에서 다룹니다.



## 장과 문서

> 각 장이 다루는 핵심 질문과 학습 문서 목록 및 진행 상태를 안내합니다. 신규 문서가 작성될 때마다 이 인덱스 표에 행을 추가합니다.

| 장 | 학습 질문 | 문서 | 상태 |
|---|---|---|---|
| 8 업스트림 층 | 기본값 그대로 낸 프록시에 실제 운영 장애가 나면 어떤 신호로 원인을 좁히고 무엇을 고치는가 | [01-01](./01-01.기본값%20리버스%20프록시가%20겪는%20장애%20-%20느린%20검색·포트%20고갈·POST%20502·회복%20지연·중복%20등록.md) · [01-02](./01-02.리버스%20프록시%20업스트림%20층%20—%20연결%20풀·기한·대기열·재시도와%20실패%20분류.md) | draft (I1·I2·I3 진단·고침, v0.8.0) |



## 책 노트와 읽는 순서

> 프록시 실습 문서를 읽기 전에 필요한 HTTP 규약과 Go 클라이언트 기본기는 책 정독 노트를 먼저 확인합니다. 선행 지식을 갖춘 상태에서 프록시 구현 문서를 읽으면 세부 설계 의도를 명확하게 이해할 수 있습니다.

8장 실습 문서를 읽기 전에는 책 8장의 기본기를 다룬 [08-01 HTTP 기초](../../book/npg_network-programming-with-go/08-01.HTTP%20%EB%8A%94%20URL%20%EB%A1%9C%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EA%B0%80%EB%A6%AC%ED%82%A4%EA%B3%A0%20%EB%A9%94%EC%84%9C%EB%93%9C%EB%A1%9C%20%EC%9A%94%EC%B2%AD%ED%95%98%EB%A9%B0%20%EC%83%81%ED%83%9C%20%EC%BD%94%EB%93%9C%EB%A1%9C%20%EB%8B%B5%ED%95%9C%EB%8B%A4.md)과 [08-02 Go HTTP 클라이언트](../../book/npg_network-programming-with-go/08-02.Go%20HTTP%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EB%8A%94%20%EC%9D%91%EB%8B%B5%20%EB%B3%B8%EB%AC%B8%EC%9D%84%20%EB%8B%AB%EC%95%84%EC%95%BC%20%EC%97%B0%EA%B2%B0%EC%9D%84%20%EC%9E%AC%EC%82%AC%EC%9A%A9%ED%95%98%EA%B3%A0%20context%20%EB%A1%9C%20%EC%9A%94%EC%B2%AD%EC%9D%84%20%EB%81%8A%EB%8A%94%EB%8B%A4.md)를 먼저 읽기를 권장합니다. 전체 책 정독 목록은 [Network Programming with Go 책 인덱스](../../book/npg_network-programming-with-go/README.md)에서 확인할 수 있습니다.
