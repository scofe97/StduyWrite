---
title: System Design Interview — 정독 인덱스
tags: [moc, study-index, book, system-design, scalability, interview]
status: draft
source:
  - 《System Design Interview – An Insider's Guide》(Alex Xu, 2판, 2020, ISBN 979-8664653403) — Volume 1 에 해당하는 16장
  - 원본 PDF — GoogleDrive/내 드라이브/book/system-design-interview-an-insiders-guide-volume-2.pdf (파일명과 달리 내용은 Volume 1)
related:
  - ./01-01.%EB%8B%A8%EC%9D%BC%20%EC%84%9C%EB%B2%84%EC%97%90%EC%84%9C%20%EC%B6%9C%EB%B0%9C%ED%95%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20DB%20%EB%B6%84%EB%A6%AC%C2%B7%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C%C2%B7DB%20%EB%B3%B5%EC%A0%9C%EB%A1%9C%20%EC%B2%AB%20%EB%B3%91%EB%AA%A9%EC%9D%84%20%EB%84%98%EB%8A%94%EB%8B%A4.md
  - ./01-02.%EC%BA%90%EC%8B%9C%C2%B7CDN%C2%B7%EB%AC%B4%EC%83%81%ED%83%9C%20%EC%9B%B9%20%EA%B3%84%EC%B8%B5%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%84%BC%ED%84%B0%C2%B7%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%C2%B7%EC%83%A4%EB%94%A9%EC%9D%B4%20%EC%88%98%EB%B0%B1%EB%A7%8C%20%EC%82%AC%EC%9A%A9%EC%9E%90%EA%B9%8C%EC%A7%80%20%EA%B7%9C%EB%AA%A8%EB%A5%BC%20%EB%8A%98%EB%A6%B0%EB%8B%A4.md
  - ./02-01.%EA%B0%9C%EB%9E%B5%EC%A0%81%20%EA%B7%9C%EB%AA%A8%20%EC%B6%94%EC%A0%95%EC%9D%80%202%EC%9D%98%20%EA%B1%B0%EB%93%AD%EC%A0%9C%EA%B3%B1%C2%B7%EC%A7%80%EC%97%B0%20%EC%8B%9C%EA%B0%84%C2%B7%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%88%98%EC%B9%98%EB%A1%9C%20QPS%20%EC%99%80%20%EC%A0%80%EC%9E%A5%20%EC%9A%A9%EB%9F%89%EC%9D%84%20%EC%96%B4%EB%A6%BC%ED%95%9C%EB%8B%A4.md
  - ./03-01.%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%84%A4%EA%B3%84%20%EB%A9%B4%EC%A0%91%EC%9D%80%20%EB%B2%94%EC%9C%84%20%ED%99%95%EC%A0%95%C2%B7%EA%B0%9C%EB%9E%B5%20%EC%84%A4%EA%B3%84%C2%B7%EC%83%81%EC%84%B8%20%EC%84%A4%EA%B3%84%C2%B7%EB%A7%88%EB%AC%B4%EB%A6%AC%20%EB%84%A4%20%EB%8B%A8%EA%B3%84%EB%A1%9C%20%EC%A7%84%ED%96%89%ED%95%9C%EB%8B%A4.md
  - ./04-01.%EC%B2%98%EB%A6%AC%EC%9C%A8%20%EC%A0%9C%ED%95%9C%EA%B8%B0%EB%8A%94%20%ED%86%A0%ED%81%B0%20%EB%B2%84%ED%82%B7%C2%B7%EB%88%84%EC%B6%9C%20%EB%B2%84%ED%82%B7%C2%B7%EA%B3%A0%EC%A0%95%20%EC%9C%88%EB%8F%84%C2%B7%EC%9D%B4%EB%8F%99%20%EC%9C%88%EB%8F%84%20%EB%A1%9C%EA%B7%B8%C2%B7%EC%9D%B4%EB%8F%99%20%EC%9C%88%EB%8F%84%20%EC%B9%B4%EC%9A%B4%ED%84%B0%EB%A1%9C%20%EC%9A%94%EC%B2%AD%EC%9D%84%20%EC%84%BC%EB%8B%A4.md
  - ./04-02.%EC%B2%98%EB%A6%AC%EC%9C%A8%20%EC%A0%9C%ED%95%9C%20%EB%AF%B8%EB%93%A4%EC%9B%A8%EC%96%B4%EB%8A%94%20%EA%B7%9C%EC%B9%99%EA%B3%BC%20Redis%20%EC%B9%B4%EC%9A%B4%ED%84%B0%EB%A1%9C%20429%20%EB%A5%BC%20%EB%8F%8C%EB%A0%A4%EC%A3%BC%EA%B3%A0%20%EB%B6%84%EC%82%B0%20%ED%99%98%EA%B2%BD%EC%9D%98%20%EA%B2%BD%EC%9F%81%20%EC%A1%B0%EA%B1%B4%EA%B3%BC%20%EB%8F%99%EA%B8%B0%ED%99%94%EB%A5%BC%20%ED%91%BC%EB%8B%A4.md
  - ./05-01.%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%EB%8A%94%20%ED%95%B4%EC%8B%9C%20%EB%A7%81%EA%B3%BC%20%EA%B0%80%EC%83%81%20%EB%85%B8%EB%93%9C%EB%A1%9C%20%EC%84%9C%EB%B2%84%EA%B0%80%20%EB%8A%98%EA%B3%A0%20%EC%A4%84%20%EB%95%8C%20%EC%98%AE%EA%B8%B8%20%ED%82%A4%EB%A5%BC%20%EC%A4%84%EC%9D%B8%EB%8B%A4.md
  - ./06-01.%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EB%8A%94%20CAP%20%EC%84%A0%ED%83%9D%20%EC%95%84%EB%9E%98%20%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%EB%A1%9C%20%EB%82%98%EB%88%84%EA%B3%A0%20N%C2%B7W%C2%B7R%20%EC%A0%95%EC%A1%B1%EC%88%98%EB%A1%9C%20%EB%B3%B5%EC%A0%9C%20%EC%9D%BC%EA%B4%80%EC%84%B1%EC%9D%84%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md
  - ./06-02.%EB%B2%A1%ED%84%B0%20%EC%8B%9C%EA%B3%84%C2%B7%EA%B0%80%EC%8B%AD%C2%B7%EC%9E%84%EC%8B%9C%20%EC%9C%84%ED%83%81%C2%B7%EB%A8%B8%ED%81%B4%20%ED%8A%B8%EB%A6%AC%EA%B0%80%20%EC%B6%A9%EB%8F%8C%EA%B3%BC%20%EC%9E%A5%EC%95%A0%EB%A5%BC%20%EB%8B%A4%EB%A3%A8%EA%B3%A0%20%EC%93%B0%EA%B8%B0%EC%99%80%20%EC%9D%BD%EA%B8%B0%EB%8A%94%20SSTable%20%EC%9D%84%20%EC%A7%80%EB%82%9C%EB%8B%A4.md
  - ./07-01.%EB%B6%84%EC%82%B0%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20UUID%C2%B7%ED%8B%B0%EC%BC%93%20%EC%84%9C%EB%B2%84%20%EB%8C%80%EC%8B%A0%20%ED%83%80%EC%9E%84%EC%8A%A4%ED%83%AC%ED%94%84%EC%99%80%20%EC%9D%BC%EB%A0%A8%EB%B2%88%ED%98%B8%EB%A5%BC%20%EB%AC%B6%EC%9D%80%2064%EB%B9%84%ED%8A%B8%20%EC%8A%A4%EB%85%B8%ED%94%8C%EB%A0%88%EC%9D%B4%ED%81%AC%EB%A1%9C%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md
  - ./08-01.URL%20%EB%8B%A8%EC%B6%95%EA%B8%B0%EB%8A%94%20301%C2%B7302%20%EB%A6%AC%EB%94%94%EB%A0%89%EC%85%98%EA%B3%BC%20%ED%95%B4%EC%8B%9C%20%EC%B6%A9%EB%8F%8C%20%ED%95%B4%EC%86%8C%20%EB%98%90%EB%8A%94%20base62%20%EB%B3%80%ED%99%98%EC%9C%BC%EB%A1%9C%20%EC%A7%A7%EC%9D%80%20%ED%82%A4%EB%A5%BC%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md
  - ./09-01.%EC%9B%B9%20%ED%81%AC%EB%A1%A4%EB%9F%AC%EB%8A%94%20URL%20%ED%94%84%EB%A1%A0%ED%8B%B0%EC%96%B4%EA%B0%80%20%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84%EC%99%80%20%EC%98%88%EC%9D%98%EB%A5%BC%20%EC%A7%80%ED%82%A4%EB%A9%B0%20BFS%20%EB%A1%9C%20%EB%82%B4%EB%A0%A4%EB%B0%9B%EA%B3%A0%20%EC%A4%91%EB%B3%B5%EA%B3%BC%20%ED%95%A8%EC%A0%95%EC%9D%84%20%EA%B1%B8%EB%9F%AC%20%EB%82%B8%EB%8B%A4.md
  - ./10-01.%EC%95%8C%EB%A6%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%A0%9C3%EC%9E%90%20%ED%91%B8%EC%8B%9C%C2%B7SMS%C2%B7%EC%9D%B4%EB%A9%94%EC%9D%BC%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%95%9E%EC%97%90%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%EC%99%80%20%EC%9E%91%EC%97%85%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%91%90%EC%96%B4%20%EC%9E%AC%EC%8B%9C%EB%8F%84%EC%99%80%20%EC%A4%91%EB%B3%B5%EC%9D%84%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md
  - ./11-01.%EB%89%B4%EC%8A%A4%20%ED%94%BC%EB%93%9C%EB%8A%94%20%EC%93%B8%20%EB%95%8C%20%EB%B0%80%EC%96%B4%20%EB%84%A3%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%EA%B3%BC%20%EC%9D%BD%EC%9D%84%20%EB%95%8C%20%EB%8B%B9%EA%B8%B0%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%EC%9D%84%20%EC%84%9E%EA%B3%A0%20%EC%BA%90%EC%8B%9C%EB%A5%BC%20%EB%8B%A4%EC%84%AF%20%EC%B8%B5%EC%9C%BC%EB%A1%9C%20%EB%82%98%EB%88%88%EB%8B%A4.md
  - ./12-01.%EC%B1%84%ED%8C%85%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%9B%B9%EC%86%8C%EC%BC%93%20%EC%97%B0%EA%B2%B0%EC%9D%84%20%EC%83%81%ED%83%9C%20%EC%9C%A0%EC%A7%80%20%EC%84%9C%EB%B2%84%EC%97%90%20%EB%91%90%EA%B3%A0%20%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EC%99%80%20%EB%A9%94%EC%8B%9C%EC%A7%80%20ID%20%EB%A1%9C%20%EB%8C%80%ED%99%94%EC%99%80%20%EC%A0%91%EC%86%8D%20%EC%83%81%ED%83%9C%EB%A5%BC%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md
  - ./13-01.%EA%B2%80%EC%83%89%EC%96%B4%20%EC%9E%90%EB%8F%99%EC%99%84%EC%84%B1%EC%9D%80%20%ED%8A%B8%EB%9D%BC%EC%9D%B4%20%EB%85%B8%EB%93%9C%EC%97%90%20%EC%83%81%EC%9C%84%20k%20%EA%B0%9C%EB%A5%BC%20%EC%BA%90%EC%8B%9C%ED%95%98%EA%B3%A0%20%EC%88%98%EC%A7%91%20%EA%B2%BD%EB%A1%9C%EA%B0%80%20%EC%A3%BC%EA%B8%B0%EC%A0%81%EC%9C%BC%EB%A1%9C%20%ED%8A%B8%EB%9D%BC%EC%9D%B4%EB%A5%BC%20%EB%8B%A4%EC%8B%9C%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md
  - ./14-01.YouTube%20%EC%97%85%EB%A1%9C%EB%93%9C%EB%8A%94%20%EC%9B%90%EB%B3%B8%EC%9D%84%20BLOB%20%EC%A0%80%EC%9E%A5%EC%86%8C%EC%97%90%20%EB%91%90%EA%B3%A0%20DAG%20%EB%A1%9C%20%EC%AA%BC%EA%B0%A0%20%ED%8A%B8%EB%9E%9C%EC%8A%A4%EC%BD%94%EB%94%A9%EC%9D%84%20%EA%B1%B0%EC%B3%90%20CDN%20%EC%9C%BC%EB%A1%9C%20%EC%8A%A4%ED%8A%B8%EB%A6%AC%EB%B0%8D%ED%95%9C%EB%8B%A4.md
  - ./14-02.%ED%8A%B8%EB%9E%9C%EC%8A%A4%EC%BD%94%EB%94%A9%EC%9D%80%20%EC%A0%84%EC%B2%98%EB%A6%AC%C2%B7DAG%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%C2%B7%EC%9E%90%EC%9B%90%20%EA%B4%80%EB%A6%AC%EC%9E%90%C2%B7%EC%9E%91%EC%97%85%20%EC%84%9C%EB%B2%84%EB%A1%9C%20%EB%82%98%EB%89%98%EA%B3%A0%20%EC%82%AC%EC%A0%84%20%EC%84%9C%EB%AA%85%20URL%C2%B7CDN%20%EB%B9%84%EC%9A%A9%C2%B7%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%EB%A1%9C%20%EB%8B%A4%EB%93%AC%EB%8A%94%EB%8B%A4.md
  - ./15-01.Google%20Drive%20%EB%8A%94%20%ED%8C%8C%EC%9D%BC%EC%9D%84%20%EB%B8%94%EB%A1%9D%EC%9C%BC%EB%A1%9C%20%EC%AA%BC%EA%B0%9C%20%EB%B3%80%EA%B2%BD%EB%B6%84%EB%A7%8C%20%EC%98%AC%EB%A6%AC%EA%B3%A0%20%EA%B0%95%ED%95%9C%20%EC%9D%BC%EA%B4%80%EC%84%B1%EC%9D%98%20%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%99%80%20%EB%A1%B1%20%ED%8F%B4%EB%A7%81%EC%9C%BC%EB%A1%9C%20%EB%8F%99%EA%B8%B0%ED%99%94%ED%95%9C%EB%8B%A4.md
  - ../bytebytego-system-design/README.md
  - ../sdp_system-design-primer/README.md
  - ../../03_distributed/01-01.분산 아키텍처 기초.md
  - ../../../05_data/book/designing-data-intensive-applications/06-01.복제 개요와 단일 리더.md
  - ../../../05_data/book/designing-data-intensive-applications/07-01.샤딩 개요와 키 범위 샤딩.md
  - ../../README.md
learning:
  topic: system-design-interview
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않는다
  blocked_count:
  next_lesson: "15장까지 정독 완료 — 01-01 부터 Phase 4 자답·복습으로 넘어간다"
updated: 2026-10-13
---

# System Design Interview — 정독 인덱스

---

> 이 폴더는 Alex Xu 의 『System Design Interview – An Insider's Guide』(2판, Volume 1)를 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 1~15장을 모두 썼고(긴 장 넷은 두 편씩, 모두 19편), 참고 자료 목록인 16장은 이 README 에서만 다룹니다.



## 이 책을 여기 두는 이유

> 같은 폴더의 다른 시스템 설계 자료가 구성요소를 하나씩 설명한다면, 이 책은 면접 45분 안에 요구를 좁히고 수로 어림한 뒤 구성요소를 골라 잇는 순서를 사례 열둘로 연습시킵니다.

[System Design Primer 정독본](../sdp_system-design-primer/README.md)은 캐시·복제·샤딩 같은 구성요소를 주제별로 정리합니다. [ByteByteGo 그림 해설 묶음](../bytebytego-system-design/README.md)은 같은 저자 쪽의 짧은 해설을 주제별로 모았습니다. 이 책은 그 구성요소를 실제 문제에 대입하는 쪽입니다. 처리율 제한기·URL 단축기·채팅·영상 서비스처럼 요구가 다른 시스템마다 무엇부터 정하고 어디서 맞바꾸는지가 이 폴더의 몫입니다.

복제·샤딩의 일반 원리는 [복제 개요와 단일 리더](../../../05_data/book/designing-data-intensive-applications/06-01.%EB%B3%B5%EC%A0%9C%20%EA%B0%9C%EC%9A%94%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EB%A6%AC%EB%8D%94.md)·[샤딩 개요와 키 범위 샤딩](../../../05_data/book/designing-data-intensive-applications/07-01.%EC%83%A4%EB%94%A9%20%EA%B0%9C%EC%9A%94%EC%99%80%20%ED%82%A4%20%EB%B2%94%EC%9C%84%20%EC%83%A4%EB%94%A9.md) 문서가 정본이고, 이 폴더는 사례 안에서 그 선택이 어떻게 쓰이는지만 남깁니다.



## 범위와 읽는 순서

> 1~3장이 확장의 큰 그림·규모 어림·면접 절차라는 공통 도구를 세우고, 4~15장이 그 도구로 시스템을 하나씩 설계합니다. 4~7장의 처리율 제한·안정 해시·키-값 저장소·유일 ID 는 뒤 사례들이 부품으로 다시 씁니다.

| 장 | 제목 | 편 |
|---|---|---|
| 1 | Scale From Zero To Millions Of Users | 01-01, 01-02 |
| 2 | Back-of-the-Envelope Estimation | 02-01 |
| 3 | A Framework For System Design Interviews | 03-01 |
| 4 | Design A Rate Limiter | 04-01, 04-02 |
| 5 | Design Consistent Hashing | 05-01 |
| 6 | Design A Key-Value Store | 06-01, 06-02 |
| 7 | Design A Unique ID Generator In Distributed Systems | 07-01 |
| 8 | Design A URL Shortener | 08-01 |
| 9 | Design A Web Crawler | 09-01 |
| 10 | Design A Notification System | 10-01 |
| 11 | Design A News Feed System | 11-01 |
| 12 | Design A Chat System | 12-01 |
| 13 | Design A Search Autocomplete System | 13-01 |
| 14 | Design YouTube | 14-01, 14-02 |
| 15 | Design Google Drive | 15-01 |
| 16 | The Learning Continues | README 아래 「16장 읽을거리」 |

장 제목은 원본 PDF 의 장 머리에서 옮겼습니다. 파일 번호 앞자리가 곧 장 번호입니다.



## 작성된 정독 노트

> 편마다 원문 장과 한 줄 핵심을 둡니다.

| 편 | 원문 | 한 줄 핵심 |
|---|---|---|
| [01-01 단일 서버에서 출발한 시스템은 DB 분리·로드밸런서·DB 복제로 첫 병목을 넘는다](./01-01.%EB%8B%A8%EC%9D%BC%20%EC%84%9C%EB%B2%84%EC%97%90%EC%84%9C%20%EC%B6%9C%EB%B0%9C%ED%95%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20DB%20%EB%B6%84%EB%A6%AC%C2%B7%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C%C2%B7DB%20%EB%B3%B5%EC%A0%9C%EB%A1%9C%20%EC%B2%AB%20%EB%B3%91%EB%AA%A9%EC%9D%84%20%EB%84%98%EB%8A%94%EB%8B%A4.md) | 1장 | 웹·DB 분리, 로드밸런서, DB 주·부 복제로 서버 한 대의 단일 장애점을 하나씩 걷어 내는 첫 확장 |
| [01-02 캐시·CDN·무상태 웹 계층·데이터 센터·메시지 큐·샤딩이 수백만 사용자까지 규모를 늘린다](./01-02.%EC%BA%90%EC%8B%9C%C2%B7CDN%C2%B7%EB%AC%B4%EC%83%81%ED%83%9C%20%EC%9B%B9%20%EA%B3%84%EC%B8%B5%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%84%BC%ED%84%B0%C2%B7%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%C2%B7%EC%83%A4%EB%94%A9%EC%9D%B4%20%EC%88%98%EB%B0%B1%EB%A7%8C%20%EC%82%AC%EC%9A%A9%EC%9E%90%EA%B9%8C%EC%A7%80%20%EA%B7%9C%EB%AA%A8%EB%A5%BC%20%EB%8A%98%EB%A6%B0%EB%8B%A4.md) | 1장 | 캐시·CDN 으로 읽기를 줄이고 세션을 밖으로 빼 웹 계층을 무상태로 만든 뒤 데이터 센터·메시지 큐·샤딩으로 넓히는 길 |
| [02-01 개략적 규모 추정은 2의 거듭제곱·지연 시간·가용성 수치로 QPS 와 저장 용량을 어림한다](./02-01.%EA%B0%9C%EB%9E%B5%EC%A0%81%20%EA%B7%9C%EB%AA%A8%20%EC%B6%94%EC%A0%95%EC%9D%80%202%EC%9D%98%20%EA%B1%B0%EB%93%AD%EC%A0%9C%EA%B3%B1%C2%B7%EC%A7%80%EC%97%B0%20%EC%8B%9C%EA%B0%84%C2%B7%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%88%98%EC%B9%98%EB%A1%9C%20QPS%20%EC%99%80%20%EC%A0%80%EC%9E%A5%20%EC%9A%A9%EB%9F%89%EC%9D%84%20%EC%96%B4%EB%A6%BC%ED%95%9C%EB%8B%A4.md) | 2장 | 2의 거듭제곱·지연 시간·가용성 기준 값과 반올림으로 QPS·저장 용량을 자릿수 단위로 어림하는 법 |
| [03-01 시스템 설계 면접은 범위 확정·개략 설계·상세 설계·마무리 네 단계로 진행한다](./03-01.%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%84%A4%EA%B3%84%20%EB%A9%B4%EC%A0%91%EC%9D%80%20%EB%B2%94%EC%9C%84%20%ED%99%95%EC%A0%95%C2%B7%EA%B0%9C%EB%9E%B5%20%EC%84%A4%EA%B3%84%C2%B7%EC%83%81%EC%84%B8%20%EC%84%A4%EA%B3%84%C2%B7%EB%A7%88%EB%AC%B4%EB%A6%AC%20%EB%84%A4%20%EB%8B%A8%EA%B3%84%EB%A1%9C%20%EC%A7%84%ED%96%89%ED%95%9C%EB%8B%A4.md) | 3장 | 범위 확정·개략 설계·상세 설계·마무리 네 단계로 45분을 나눠 모호한 문제를 면접관과 함께 좁히는 절차 |
| [04-01 처리율 제한기는 토큰 버킷·누출 버킷·고정 윈도·이동 윈도 로그·이동 윈도 카운터로 요청을 센다](./04-01.%EC%B2%98%EB%A6%AC%EC%9C%A8%20%EC%A0%9C%ED%95%9C%EA%B8%B0%EB%8A%94%20%ED%86%A0%ED%81%B0%20%EB%B2%84%ED%82%B7%C2%B7%EB%88%84%EC%B6%9C%20%EB%B2%84%ED%82%B7%C2%B7%EA%B3%A0%EC%A0%95%20%EC%9C%88%EB%8F%84%C2%B7%EC%9D%B4%EB%8F%99%20%EC%9C%88%EB%8F%84%20%EB%A1%9C%EA%B7%B8%C2%B7%EC%9D%B4%EB%8F%99%20%EC%9C%88%EB%8F%84%20%EC%B9%B4%EC%9A%B4%ED%84%B0%EB%A1%9C%20%EC%9A%94%EC%B2%AD%EC%9D%84%20%EC%84%BC%EB%8B%A4.md) | 4장 | 토큰 버킷·누출 버킷·고정 윈도·이동 윈도 로그·이동 윈도 카운터가 몰림 허용·정확도·메모리를 맞바꾸는 방식 |
| [04-02 처리율 제한 미들웨어는 규칙과 Redis 카운터로 429 를 돌려주고 분산 환경의 경쟁 조건과 동기화를 푼다](./04-02.%EC%B2%98%EB%A6%AC%EC%9C%A8%20%EC%A0%9C%ED%95%9C%20%EB%AF%B8%EB%93%A4%EC%9B%A8%EC%96%B4%EB%8A%94%20%EA%B7%9C%EC%B9%99%EA%B3%BC%20Redis%20%EC%B9%B4%EC%9A%B4%ED%84%B0%EB%A1%9C%20429%20%EB%A5%BC%20%EB%8F%8C%EB%A0%A4%EC%A3%BC%EA%B3%A0%20%EB%B6%84%EC%82%B0%20%ED%99%98%EA%B2%BD%EC%9D%98%20%EA%B2%BD%EC%9F%81%20%EC%A1%B0%EA%B1%B4%EA%B3%BC%20%EB%8F%99%EA%B8%B0%ED%99%94%EB%A5%BC%20%ED%91%BC%EB%8B%A4.md) | 4장 | 규칙과 Redis 카운터로 429 를 돌려주는 미들웨어, 분산 환경의 경쟁 조건과 카운터 동기화 |
| [05-01 안정 해시는 해시 링과 가상 노드로 서버가 늘고 줄 때 옮길 키를 줄인다](./05-01.%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%EB%8A%94%20%ED%95%B4%EC%8B%9C%20%EB%A7%81%EA%B3%BC%20%EA%B0%80%EC%83%81%20%EB%85%B8%EB%93%9C%EB%A1%9C%20%EC%84%9C%EB%B2%84%EA%B0%80%20%EB%8A%98%EA%B3%A0%20%EC%A4%84%20%EB%95%8C%20%EC%98%AE%EA%B8%B8%20%ED%82%A4%EB%A5%BC%20%EC%A4%84%EC%9D%B8%EB%8B%A4.md) | 5장 | 나머지 연산 대신 해시 링과 가상 노드를 써서 서버가 늘고 줄 때 옮길 키를 이웃 구간으로 줄이는 원리 |
| [06-01 키-값 저장소는 CAP 선택 아래 안정 해시로 나누고 N·W·R 정족수로 복제 일관성을 고른다](./06-01.%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EB%8A%94%20CAP%20%EC%84%A0%ED%83%9D%20%EC%95%84%EB%9E%98%20%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%EB%A1%9C%20%EB%82%98%EB%88%84%EA%B3%A0%20N%C2%B7W%C2%B7R%20%EC%A0%95%EC%A1%B1%EC%88%98%EB%A1%9C%20%EB%B3%B5%EC%A0%9C%20%EC%9D%BC%EA%B4%80%EC%84%B1%EC%9D%84%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md) | 6장 | CAP 선택을 먼저 정하고 안정 해시로 나눈 뒤 N·W·R 정족수로 복제 일관성의 강도를 고르는 설계 |
| [06-02 벡터 시계·가십·임시 위탁·머클 트리가 충돌과 장애를 다루고 쓰기와 읽기는 SSTable 을 지난다](./06-02.%EB%B2%A1%ED%84%B0%20%EC%8B%9C%EA%B3%84%C2%B7%EA%B0%80%EC%8B%AD%C2%B7%EC%9E%84%EC%8B%9C%20%EC%9C%84%ED%83%81%C2%B7%EB%A8%B8%ED%81%B4%20%ED%8A%B8%EB%A6%AC%EA%B0%80%20%EC%B6%A9%EB%8F%8C%EA%B3%BC%20%EC%9E%A5%EC%95%A0%EB%A5%BC%20%EB%8B%A4%EB%A3%A8%EA%B3%A0%20%EC%93%B0%EA%B8%B0%EC%99%80%20%EC%9D%BD%EA%B8%B0%EB%8A%94%20SSTable%20%EC%9D%84%20%EC%A7%80%EB%82%9C%EB%8B%A4.md) | 6장 | 벡터 시계·가십·임시 위탁·머클 트리가 충돌과 장애를 나눠 맡고, 쓰기·읽기가 커밋 로그·멤테이블·SSTable·블룸 필터를 지나는 경로 |
| [07-01 분산 유일 ID 는 UUID·티켓 서버 대신 타임스탬프와 일련번호를 묶은 64비트 스노플레이크로 만든다](./07-01.%EB%B6%84%EC%82%B0%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20UUID%C2%B7%ED%8B%B0%EC%BC%93%20%EC%84%9C%EB%B2%84%20%EB%8C%80%EC%8B%A0%20%ED%83%80%EC%9E%84%EC%8A%A4%ED%83%AC%ED%94%84%EC%99%80%20%EC%9D%BC%EB%A0%A8%EB%B2%88%ED%98%B8%EB%A5%BC%20%EB%AC%B6%EC%9D%80%2064%EB%B9%84%ED%8A%B8%20%EC%8A%A4%EB%85%B8%ED%94%8C%EB%A0%88%EC%9D%B4%ED%81%AC%EB%A1%9C%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md) | 7장 | UUID·티켓 서버의 한계와 밀리초 시각·데이터 센터·서버·순번을 64비트에 묶는 스노플레이크 |
| [08-01 URL 단축기는 301·302 리디렉션과 해시 충돌 해소 또는 base62 변환으로 짧은 키를 만든다](./08-01.URL%20%EB%8B%A8%EC%B6%95%EA%B8%B0%EB%8A%94%20301%C2%B7302%20%EB%A6%AC%EB%94%94%EB%A0%89%EC%85%98%EA%B3%BC%20%ED%95%B4%EC%8B%9C%20%EC%B6%A9%EB%8F%8C%20%ED%95%B4%EC%86%8C%20%EB%98%90%EB%8A%94%20base62%20%EB%B3%80%ED%99%98%EC%9C%BC%EB%A1%9C%20%EC%A7%A7%EC%9D%80%20%ED%82%A4%EB%A5%BC%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md) | 8장 | 301·302 리디렉션 차이와, 해시를 잘라 충돌을 풀거나 유일 ID 를 base62 로 바꿔 7 자 키를 만드는 두 방법 |
| [09-01 웹 크롤러는 URL 프론티어가 우선순위와 예의를 지키며 BFS 로 내려받고 중복과 함정을 걸러 낸다](./09-01.%EC%9B%B9%20%ED%81%AC%EB%A1%A4%EB%9F%AC%EB%8A%94%20URL%20%ED%94%84%EB%A1%A0%ED%8B%B0%EC%96%B4%EA%B0%80%20%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84%EC%99%80%20%EC%98%88%EC%9D%98%EB%A5%BC%20%EC%A7%80%ED%82%A4%EB%A9%B0%20BFS%20%EB%A1%9C%20%EB%82%B4%EB%A0%A4%EB%B0%9B%EA%B3%A0%20%EC%A4%91%EB%B3%B5%EA%B3%BC%20%ED%95%A8%EC%A0%95%EC%9D%84%20%EA%B1%B8%EB%9F%AC%20%EB%82%B8%EB%8B%A4.md) | 9장 | URL 프론티어가 우선순위와 호스트별 예의를 지키며 BFS 로 내려받고 해시·길이 상한으로 중복과 함정을 거르는 크롤러 |
| [10-01 알림 시스템은 제3자 푸시·SMS·이메일 서비스 앞에 메시지 큐와 작업 서버를 두어 재시도와 중복을 다룬다](./10-01.%EC%95%8C%EB%A6%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%A0%9C3%EC%9E%90%20%ED%91%B8%EC%8B%9C%C2%B7SMS%C2%B7%EC%9D%B4%EB%A9%94%EC%9D%BC%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%95%9E%EC%97%90%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%EC%99%80%20%EC%9E%91%EC%97%85%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%91%90%EC%96%B4%20%EC%9E%AC%EC%8B%9C%EB%8F%84%EC%99%80%20%EC%A4%91%EB%B3%B5%EC%9D%84%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md) | 10장 | 푸시·SMS·이메일 제3자 서비스 앞에 알림 서버·유형별 큐·작업 서버를 두고 알림 로그·재시도·이벤트 ID 로 유실과 중복을 다루는 구조 |
| [11-01 뉴스 피드는 쓸 때 밀어 넣는 팬아웃과 읽을 때 당기는 팬아웃을 섞고 캐시를 다섯 층으로 나눈다](./11-01.%EB%89%B4%EC%8A%A4%20%ED%94%BC%EB%93%9C%EB%8A%94%20%EC%93%B8%20%EB%95%8C%20%EB%B0%80%EC%96%B4%20%EB%84%A3%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%EA%B3%BC%20%EC%9D%BD%EC%9D%84%20%EB%95%8C%20%EB%8B%B9%EA%B8%B0%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%EC%9D%84%20%EC%84%9E%EA%B3%A0%20%EC%BA%90%EC%8B%9C%EB%A5%BC%20%EB%8B%A4%EC%84%AF%20%EC%B8%B5%EC%9C%BC%EB%A1%9C%20%EB%82%98%EB%88%88%EB%8B%A4.md) | 11장 | 쓸 때 밀어 넣는 팬아웃과 읽을 때 당기는 팬아웃을 사용자 규모로 섞고 캐시를 다섯 층으로 나누는 피드 |
| [12-01 채팅 시스템은 웹소켓 연결을 상태 유지 서버에 두고 키-값 저장소와 메시지 ID 로 대화와 접속 상태를 다룬다](./12-01.%EC%B1%84%ED%8C%85%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%9B%B9%EC%86%8C%EC%BC%93%20%EC%97%B0%EA%B2%B0%EC%9D%84%20%EC%83%81%ED%83%9C%20%EC%9C%A0%EC%A7%80%20%EC%84%9C%EB%B2%84%EC%97%90%20%EB%91%90%EA%B3%A0%20%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EC%99%80%20%EB%A9%94%EC%8B%9C%EC%A7%80%20ID%20%EB%A1%9C%20%EB%8C%80%ED%99%94%EC%99%80%20%EC%A0%91%EC%86%8D%20%EC%83%81%ED%83%9C%EB%A5%BC%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md) | 12장 | 웹소켓 연결을 쥔 상태 유지 서버, 키-값 저장소와 메시지 ID 로 쌓는 대화 기록, 하트비트로 판정하는 접속 상태 |
| [13-01 검색어 자동완성은 트라이 노드에 상위 k 개를 캐시하고 수집 경로가 주기적으로 트라이를 다시 만든다](./13-01.%EA%B2%80%EC%83%89%EC%96%B4%20%EC%9E%90%EB%8F%99%EC%99%84%EC%84%B1%EC%9D%80%20%ED%8A%B8%EB%9D%BC%EC%9D%B4%20%EB%85%B8%EB%93%9C%EC%97%90%20%EC%83%81%EC%9C%84%20k%20%EA%B0%9C%EB%A5%BC%20%EC%BA%90%EC%8B%9C%ED%95%98%EA%B3%A0%20%EC%88%98%EC%A7%91%20%EA%B2%BD%EB%A1%9C%EA%B0%80%20%EC%A3%BC%EA%B8%B0%EC%A0%81%EC%9C%BC%EB%A1%9C%20%ED%8A%B8%EB%9D%BC%EC%9D%B4%EB%A5%BC%20%EB%8B%A4%EC%8B%9C%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md) | 13장 | 트라이 노드마다 상위 k 개를 캐시해 접두사 하나로 읽고, 로그 집계 작업자가 트라이를 주기적으로 다시 만드는 자동완성 |
| [14-01 YouTube 업로드는 원본을 BLOB 저장소에 두고 DAG 로 쪼갠 트랜스코딩을 거쳐 CDN 으로 스트리밍한다](./14-01.YouTube%20%EC%97%85%EB%A1%9C%EB%93%9C%EB%8A%94%20%EC%9B%90%EB%B3%B8%EC%9D%84%20BLOB%20%EC%A0%80%EC%9E%A5%EC%86%8C%EC%97%90%20%EB%91%90%EA%B3%A0%20DAG%20%EB%A1%9C%20%EC%AA%BC%EA%B0%A0%20%ED%8A%B8%EB%9E%9C%EC%8A%A4%EC%BD%94%EB%94%A9%EC%9D%84%20%EA%B1%B0%EC%B3%90%20CDN%20%EC%9C%BC%EB%A1%9C%20%EC%8A%A4%ED%8A%B8%EB%A6%AC%EB%B0%8D%ED%95%9C%EB%8B%A4.md) | 14장 | 원본을 BLOB 저장소에 두고 DAG 로 쪼갠 트랜스코딩을 거쳐 CDN 에서 조각 단위로 스트리밍하는 영상 서비스의 큰 흐름 |
| [14-02 트랜스코딩은 전처리·DAG 스케줄러·자원 관리자·작업 서버로 나뉘고 사전 서명 URL·CDN 비용·오류 처리로 다듬는다](./14-02.%ED%8A%B8%EB%9E%9C%EC%8A%A4%EC%BD%94%EB%94%A9%EC%9D%80%20%EC%A0%84%EC%B2%98%EB%A6%AC%C2%B7DAG%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%C2%B7%EC%9E%90%EC%9B%90%20%EA%B4%80%EB%A6%AC%EC%9E%90%C2%B7%EC%9E%91%EC%97%85%20%EC%84%9C%EB%B2%84%EB%A1%9C%20%EB%82%98%EB%89%98%EA%B3%A0%20%EC%82%AC%EC%A0%84%20%EC%84%9C%EB%AA%85%20URL%C2%B7CDN%20%EB%B9%84%EC%9A%A9%C2%B7%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%EB%A1%9C%20%EB%8B%A4%EB%93%AC%EB%8A%94%EB%8B%A4.md) | 14장 | 전처리기·DAG 스케줄러·자원 관리자·작업 서버로 나뉜 트랜스코딩과 사전 서명 URL·CDN 비용·오류 처리로 다듬는 부분 |
| [15-01 Google Drive 는 파일을 블록으로 쪼개 변경분만 올리고 강한 일관성의 메타데이터와 롱 폴링으로 동기화한다](./15-01.Google%20Drive%20%EB%8A%94%20%ED%8C%8C%EC%9D%BC%EC%9D%84%20%EB%B8%94%EB%A1%9D%EC%9C%BC%EB%A1%9C%20%EC%AA%BC%EA%B0%9C%20%EB%B3%80%EA%B2%BD%EB%B6%84%EB%A7%8C%20%EC%98%AC%EB%A6%AC%EA%B3%A0%20%EA%B0%95%ED%95%9C%20%EC%9D%BC%EA%B4%80%EC%84%B1%EC%9D%98%20%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%99%80%20%EB%A1%B1%20%ED%8F%B4%EB%A7%81%EC%9C%BC%EB%A1%9C%20%EB%8F%99%EA%B8%B0%ED%99%94%ED%95%9C%EB%8B%A4.md) | 15장 | 파일을 블록으로 쪼개 바뀐 블록만 올리고 메타데이터는 강한 일관성으로 지키며 롱 폴링으로 다른 기기에 알리는 동기화 |



## 16장 읽을거리

> 16장은 실제 회사의 아키텍처 글과 기술 블로그 목록이라 본편을 두지 않았습니다. 목록 가운데 노트가 이미 다룬 사례만 이어 둡니다.

목록은 두 부분입니다. 앞부분은 Facebook·Amazon·Netflix·Google·Twitter·Uber·Dropbox·WhatsApp 등의 아키텍처 글과 논문이고, 뒷부분은 회사별 엔지니어링 블로그 주소입니다. 앞부분의 주소는 대부분 단축 URL 이라 원래 글 제목으로 찾는 편이 빠릅니다.

| 목록의 글 | 이어지는 노트 |
|---|---|
| Dynamo: Amazon's Highly Available Key-value Store | 06-01·06-02 (정족수·벡터 시계·가십·임시 위탁·머클 트리), 05-01 (가상 노드) |
| Announcing Snowflake | 07-01 |
| Scaling Memcache at Facebook | 01-02 |
| Bigtable | 06-02 (SSTable 읽기·쓰기 경로) |
| The WhatsApp Architecture | 12-01 |
| How We've Scaled Dropbox | 15-01 |
| System design primer | [System Design Primer 정독본](../sdp_system-design-primer/README.md) |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 1~15장 완료 (19편), 16장은 위 표로 대신 |
| 난이도 레벨 | 기본. 학습자 자답 전이라 조정 근거는 아직 없습니다 |
| 막힌 지점 | 아직 없음 |
| 다음 레슨 후보 | 정독은 끝났습니다. 01-01 부터 Phase 4 자답으로 이해를 확인합니다 |
| 최근 검증 결과 | 2026-10-13 1~15장 19편을 현행 규약으로 새로 썼습니다(도식 106장). 편마다 원문 추출본과 공식 문서·RFC 같은 1차 자료로 대조하는 적대적 검증, 수정, 재검증, 재수정을 거쳤습니다. 2020년 판 이후 달라진 사실(클라우드 요금·서비스 한도·프로토콜 상태 등)은 그 절의 본문에 1차 자료 링크와 함께 썼습니다. 1·4·6·14장은 분량 때문에 두 편으로 나눴습니다. 19편 게이트 실패 0, 도식 위반 0. 12-01·13-01·14-01·14-02·15-01 은 목표 분량보다 깁니다 |
| 복습 회차 | 없음 |



## 출처와 톤

- 원본 PDF 가 1차 자료입니다. 파일명은 `volume-2` 지만 목차가 Volume 1(처리율 제한기부터 Google Drive 까지)이고 Volume 2 의 고유 주제(근접 서비스·결제·분산 메시지 큐 등)는 없어서 Volume 1 로 다룹니다.
- 노트는 책 없이 읽히게 씁니다. 본문에 그림 번호·쪽·장 번호 같은 책 지칭을 두지 않고, 출처는 frontmatter 와 `## 참고 자료` 에만 적습니다. 책 밖 보강과 현재 사실은 그 사실이 쓰이는 절에 1차 자료 링크로 녹입니다.
- 톤은 합니다체입니다. 도식 생성기는 `_assets/_gen/` 에 있고 `_assets/` 에서 실행합니다. `dd.py` 는 Learning eBPF 정독본 `_assets/dd.py` 의 사본입니다.
- 2026-06 에 쓴 옛 노트 15편(`01-01.0부터 수백만 사용자까지 확장` 등 제목형 파일명)은 이 19편으로 바꿨습니다.
- 이 저장소의 원격은 공개 저장소이므로 실습 기록을 붙일 때 사내 주소·이름을 쓰지 않습니다.
