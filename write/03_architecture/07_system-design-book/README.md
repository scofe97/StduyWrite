---
title: 07_system-design-book — 『가상 면접 사례로 배우는 대규모 시스템 설계 기초』 학습 시리즈
tags: [moc, system-design, scalability, interview, book-study]
status: in-progress
book:
  title: System Design Interview — An Insider's Guide
  author: Alex Xu
  edition: Second Edition (Volume 1)
related:
  - ../03_distributed/01-01.분산 아키텍처 기초.md
  - ../../05_data/theory/02-03.복제.md
  - ../../05_data/theory/02-04.샤딩.md
updated: 2026-06-10
---


# 『System Design Interview』 학습 시리즈
---
> Alex Xu 의 『System Design Interview: An Insider's Guide』를 한 챕터씩 읽으면서, 면접에서 바로 말할 수 있는 수준으로 핵심을 재구성하는 시리즈입니다. 책이 영어 + 그림 위주라, 본 시리즈는 같은 내용을 합니다체 설명 문장 + SVG 종합도 + Mermaid 흐름으로 옮겨 "책을 다시 펴지 않아도 설명할 수 있게" 만드는 데 목적이 있습니다.


## 책 식별 메모 — 파일명은 volume-2 지만 내용은 Volume 1

원본 PDF 파일명이 `...volume-2.pdf` 였지만, 실제 목차는 Volume 1 입니다. 근거는 챕터 구성입니다. Rate Limiter, Consistent Hashing, Key-Value Store, URL Shortener, Web Crawler, Notification, News Feed, Chat, Search Autocomplete, YouTube, Google Drive 로 이어지는 16개 챕터는 Volume 1 의 목차이고, Volume 2 의 고유 주제인 근접 서비스(Proximity Service)·결제 시스템·검색 엔진·분산 메시지 큐·메트릭 모니터링은 이 PDF 어디에도 없습니다. 그래서 본 시리즈는 파일명 오기를 무시하고 **내용 기준으로 Volume 1** 로 분류했습니다.


## 전체 목차와 진행 상태

책은 크게 세 묶음으로 읽습니다. 도입부 3개 챕터(기초·추정·면접 방법론)를 한 묶음으로, 나머지 13개 챕터는 개별 시스템 설계 사례로 봅니다. 현재는 도입부 묶음만 작성했습니다.

| # | 챕터 | 문서 | 상태 |
|---|------|------|------|
| 1 | Scale from Zero to Millions of Users | [01-01](01-01.0부터%20수백만%20사용자까지%20확장.md) | 작성 완료 |
| 2 | Back-of-the-Envelope Estimation | [01-02](01-02.개략적%20규모%20추정.md) | 작성 완료 |
| 3 | A Framework for System Design Interviews | [01-03](01-03.시스템%20설계%20면접%204단계%20프레임워크.md) | 작성 완료 |
| 4 | Design a Rate Limiter | [02-01](02-01.처리율%20제한기%20설계.md) | 작성 완료 |
| 5 | Design Consistent Hashing | [02-02](02-02.안정%20해시%20설계.md) | 작성 완료 |
| 6 | Design a Key-Value Store | [02-03](02-03.키-값%20저장소%20설계.md) | 작성 완료 |
| 7 | Design a Unique ID Generator | [02-04](02-04.분산%20유일%20ID%20생성기%20설계.md) | 작성 완료 |
| 8 | Design a URL Shortener | [02-05](02-05.URL%20단축기%20설계.md) | 작성 완료 |
| 9 | Design a Web Crawler | [02-06](02-06.웹%20크롤러%20설계.md) | 작성 완료 |
| 10 | Design a Notification System | [02-07](02-07.알림%20시스템%20설계.md) | 작성 완료 |
| 11 | Design a News Feed System | [02-08](02-08.뉴스%20피드%20시스템%20설계.md) | 작성 완료 |
| 12 | Design a Chat System | [02-09](02-09.채팅%20시스템%20설계.md) | 작성 완료 |
| 13 | Design a Search Autocomplete System | — | 예정 |
| 14 | Design YouTube | — | 예정 |
| 15 | Design Google Drive | — | 예정 |
| 16 | The Learning Continues | — | 예정 |


## 도입부 3개 챕터를 한 묶음으로 보는 이유

CH1~3 은 특정 시스템을 설계하지 않습니다. 셋 다 *어떤 설계 문제에도 공통으로 쓰는 기초 체력*을 다룹니다. CH1 은 확장의 큰 그림(어떤 순서로 시스템을 키우는가), CH2 는 규모를 수로 따지는 법(QPS·스토리지·가용성), CH3 은 면접이라는 상황을 푸는 절차(4단계)입니다. CH4 부터는 이 셋을 도구로 써서 개별 시스템을 설계하므로, 본 시리즈도 도입부를 `01-01 ~ 01-03` 한 묶음으로 묶었습니다.

CH4 부터는 개별 시스템 설계 사례라 `02-xx` 묶음으로 분리합니다. 파일 번호와 챕터 번호가 어긋나므로(02-01 = CH4, 02-02 = CH5), 위 목차 표의 매핑을 기준으로 찾습니다.


## 시각화 규약

각 문서는 챕터의 척추를 한 장으로 압축한 **SVG 핵심 요약 종합도**를 1개씩 가집니다(`_assets/` 하위). 흐름·시퀀스·간단한 분기는 Mermaid 로 본문에 인라인합니다. SVG 가 1순위인 이유는 확장 단계나 면접 4단계처럼 *박스 위치 자체가 의미를 갖는* 도식이 많기 때문입니다.

| 챕터 | SVG 종합도 |
|------|-----------|
| CH1 | [`_assets/01-01.scaling-journey.svg`](_assets/01-01.scaling-journey.svg) — 점진 확장 11단계 + 최종 아키텍처 |
| CH2 | [`_assets/01-02.estimation-cheatsheet.svg`](_assets/01-02.estimation-cheatsheet.svg) — 거듭제곱·latency·가용성 치트시트 |
| CH3 | [`_assets/01-03.interview-framework.svg`](_assets/01-03.interview-framework.svg) — 4단계 + 시간 배분 + 산출물 |
| CH4 | [`_assets/02-01.rate-limiter-algorithms.svg`](_assets/02-01.rate-limiter-algorithms.svg) — 5개 알고리즘 비교 + 분산 아키텍처 |
| CH5 | [`_assets/02-02.consistent-hashing.svg`](_assets/02-02.consistent-hashing.svg) — 재해싱 문제 + 해시 링·가상 노드 |
| CH6 | [`_assets/02-03.key-value-store.svg`](_assets/02-03.key-value-store.svg) — 8개 빌딩 블록(CAP·정족수·벡터시계·Merkle·SSTable) |
| CH7 | [`_assets/02-04.unique-id-generator.svg`](_assets/02-04.unique-id-generator.svg) — 4가지 접근 + 스노우플레이크 64비트 레이아웃 |
| CH8 | [`_assets/02-05.url-shortener.svg`](_assets/02-05.url-shortener.svg) — 두 해시 접근 + base62 변환 + 301/302 |
| CH9 | [`_assets/02-06.web-crawler.svg`](_assets/02-06.web-crawler.svg) — 워크플로우 파이프라인 + URL Frontier 2계층 |
| CH10 | [`_assets/02-07.notification-system.svg`](_assets/02-07.notification-system.svg) — 채널별 큐 아키텍처 + 안정성 고려 |
| CH11 | [`_assets/02-08.news-feed-system.svg`](_assets/02-08.news-feed-system.svg) — fanout push/pull + 하이브리드 + 5계층 캐시 |
| CH12 | [`_assets/02-09.chat-system.svg`](_assets/02-09.chat-system.svg) — WebSocket·아키텍처·1:1 흐름·heartbeat |
