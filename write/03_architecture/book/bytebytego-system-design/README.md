---
title: ByteByteGo System Design — 정독 인덱스
tags: [moc, study-index, book, system-design, bytebytego]
status: draft
source:
  - ByteByteGo(Alex Xu 외), 「System Design」 그림 해설 모음 PDF — 짧은 글과 그림으로 된 159쪽. 저자·판·연도·ISBN 은 1차 자료로 확인하지 못해 비웁니다
  - 원본 PDF — GoogleDrive/내 드라이브/book/system-design-interview-an-insiders-guide-volume-1.pdf (파일명·PDF 메타데이터의 제목과 달리 내용은 이 모음)
  - https://github.com/ByteByteGoHq/system-design-101 — 같은 글 상당수가 공개된 저장소
related:
  - ./01-01.%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EB%82%99%EA%B4%80%EC%A0%81%20%EC%9E%A0%EA%B8%88%EC%9D%B4%20%EB%8F%99%EC%8B%9C%20%EC%93%B0%EA%B8%B0%EC%9D%98%20%EC%9D%B4%EC%83%81%20%ED%98%84%EC%83%81%EC%9D%84%20%EB%A7%89%EA%B3%A0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EC%96%91%EC%9D%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%A2%85%EB%A5%98%EB%A5%BC%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md
  - ./01-02.%ED%8C%8C%ED%8B%B0%EC%85%94%EB%8B%9D%EA%B3%BC%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9D%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%A5%BC%20%EB%84%93%ED%9E%88%EA%B3%A0%20%EC%A0%84%EC%97%AD%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20%EB%82%98%EB%89%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%97%90%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EC%A4%80%EB%8B%A4.md
  - ./02-01.%EC%BA%90%EC%8B%9C%20%EC%A0%84%EB%9E%B5%EC%9D%80%20%EC%9D%BD%EA%B8%B0%C2%B7%EC%93%B0%EA%B8%B0%20%EA%B2%BD%EB%A1%9C%EC%97%90%EC%84%9C%20%EC%BA%90%EC%8B%9C%20%EC%9E%90%EB%A6%AC%EB%A5%BC%20%EC%A0%95%ED%95%98%EA%B3%A0%20Redis%20%EB%8A%94%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%A3%A8%ED%94%84%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EB%8B%A4.md
  - ./03-01.URL%20%EC%9D%84%20%EC%B9%98%EB%A9%B4%20DNS%C2%B7TCP%C2%B7TLS%C2%B7HTTP%20%EB%A5%BC%20%EA%B1%B0%EC%B3%90%20%EB%B8%8C%EB%9D%BC%EC%9A%B0%EC%A0%80%EA%B0%80%20%ED%99%94%EB%A9%B4%EC%9D%84%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20CDN%20%EC%9D%B4%20%EA%B7%B8%20%EA%B8%B8%EC%9D%84%20%EC%A4%84%EC%9D%B8%EB%8B%A4.md
  - ./03-02.API%20%EB%8A%94%20SOAP%C2%B7REST%C2%B7GraphQL%C2%B7RPC%20%EB%A1%9C%20%EA%B0%88%EB%A6%AC%EA%B3%A0%20%ED%86%A0%ED%81%B0%C2%B7HMAC%C2%B7SSO%C2%B7%EC%86%94%ED%8A%B8%20%ED%95%B4%EC%8B%9C%EA%B0%80%20%EC%A0%91%EA%B7%BC%EA%B3%BC%20%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%EB%A5%BC%20%EC%A7%80%ED%82%A8%EB%8B%A4.md
  - ./04-01.%EB%B8%94%EB%A1%9D%C2%B7%ED%8C%8C%EC%9D%BC%C2%B7%EA%B0%9D%EC%B2%B4%20%EC%A0%80%EC%9E%A5%EC%86%8C%EB%8A%94%20%EC%A0%91%EA%B7%BC%20%EB%8B%A8%EC%9C%84%EA%B0%80%20%EB%8B%A4%EB%A5%B4%EA%B3%A0%20%EC%9D%B4%EB%A0%88%EC%9D%B4%EC%A0%80%20%EC%BD%94%EB%94%A9%EA%B3%BC%20%EB%B6%84%ED%95%A0%20%EC%97%85%EB%A1%9C%EB%93%9C%EA%B0%80%20%ED%81%B0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%EC%8B%B8%EA%B3%A0%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EB%8B%B4%EB%8A%94%EB%8B%A4.md
  - ./05-01.Kafka%20%EB%8A%94%20%EC%88%9C%EC%B0%A8%20IO%20%EC%99%80%20%EC%A0%9C%EB%A1%9C%20%EC%B9%B4%ED%94%BC%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EA%B3%A0%20%EC%A0%84%EB%8B%AC%20%EB%B3%B4%EC%9E%A5%EC%9D%80%20%EC%B5%9C%EB%8C%80%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%B5%9C%EC%86%8C%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%A0%95%ED%99%95%ED%9E%88%20%ED%95%9C%20%EB%B2%88%EC%9C%BC%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md
  - ./05-02.%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B8%B0%EC%88%A0%EC%9D%80%20GFS%C2%B7MapReduce%C2%B7BigTable%20%EC%97%90%EC%84%9C%20%EC%B6%9C%EB%B0%9C%ED%95%B4%20OLTP%C2%B7OLAP%C2%B7%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%EA%B0%88%EB%9E%98%EB%A1%9C%20%EC%95%9E%20%EC%84%B8%EB%8C%80%EC%9D%98%20%ED%95%9C%EA%B3%84%EB%A5%BC%20%ED%95%98%EB%82%98%EC%94%A9%20%ED%92%80%EC%97%88%EB%8B%A4.md
  - ./06-01.IaaS%C2%B7PaaS%C2%B7SaaS%20%EC%99%80%20%EA%B0%80%EC%83%81%20%EB%A8%B8%EC%8B%A0%C2%B7%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7%EC%84%9C%EB%B2%84%EB%A6%AC%EC%8A%A4%EB%8A%94%20%EC%9A%B4%EC%98%81%20%EC%B1%85%EC%9E%84%EC%9D%84%20%EC%96%B4%EB%94%94%EA%B9%8C%EC%A7%80%20%EB%84%98%EA%B8%B0%EB%8A%94%EC%A7%80%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md
  - ./06-02.%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%EC%9D%80%20%EC%83%88%20%EB%B2%84%EC%A0%84%EC%9D%84%20%EC%96%BC%EB%A7%88%EB%82%98%20%EC%A1%B0%EA%B8%88%EC%94%A9%20%EB%82%B4%EB%B3%B4%EB%82%BC%EC%A7%80%20%EC%A0%95%ED%95%98%EA%B3%A0%20%EC%9E%A5%EC%95%A0%20%EB%8C%80%EC%9D%91%EC%9D%80%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%EC%99%80%20%EC%82%AC%ED%9B%84%20%EA%B2%80%ED%86%A0%EB%A1%9C%20%EC%9D%B4%EC%96%B4%EC%A7%84%EB%8B%A4.md
  - ./07-01.%EC%98%A8%EB%9D%BC%EC%9D%B8%20%EA%B2%B0%EC%A0%9C%EB%8A%94%20%EC%B9%B4%EB%93%9C%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%C2%B7SWIFT%C2%B7%EC%99%B8%ED%99%98%20%EA%B2%BD%EB%A1%9C%EB%A1%9C%20%EB%8F%88%EC%9D%B4%20%EC%9B%80%EC%A7%81%EC%9D%B4%EA%B3%A0%20%EC%A7%80%EA%B0%91%EA%B3%BC%20%EC%9E%A5%EB%B6%80%EA%B0%80%20%EA%B7%B8%20%ED%9D%90%EB%A6%84%EC%9D%84%20%EA%B8%B0%EB%A1%9D%ED%95%9C%EB%8B%A4.md
  - ./07-02.%EA%B2%B0%EC%A0%9C%20%EC%A0%95%ED%99%95%EC%84%B1%EC%9D%80%20%EB%A9%B1%EB%93%B1%20%ED%82%A4%EB%A1%9C%20%EC%9D%B4%EC%A4%91%20%EC%B2%AD%EA%B5%AC%EB%A5%BC%20%EB%A7%89%EA%B3%A0%20%EB%8C%80%EC%82%AC%EB%A1%9C%20%EC%9E%A5%EB%B6%80%20%EB%B6%88%EC%9D%BC%EC%B9%98%EB%A5%BC%20%EC%B0%BE%EA%B3%A0%20%ED%86%A0%ED%81%B0%ED%99%94%EB%A1%9C%20%EC%B9%B4%EB%93%9C%20%EC%A0%95%EB%B3%B4%EB%A5%BC%20%EC%A7%80%ED%82%A8%EB%8B%A4.md
  - ./07-03.%EA%B2%B0%EC%A0%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EA%B2%B0%EC%A0%9C%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%EB%A5%BC%20%EA%B2%B0%EC%A0%9C%20%EC%A3%BC%EB%AC%B8%EC%9C%BC%EB%A1%9C%20%EB%82%98%EB%88%A0%20PSP%20%EC%97%90%20%EB%A7%A1%EA%B8%B0%EA%B3%A0%20%ED%94%8C%EB%9E%98%EC%8B%9C%20%EC%84%B8%EC%9D%BC%EC%9D%80%20%EB%B9%84%EB%8F%99%EA%B8%B0%20%ED%81%90%EC%99%80%20%EC%9E%AC%EA%B3%A0%20%EC%B0%A8%EA%B0%90%20%EC%88%9C%EC%84%9C%EB%A1%9C%20%EA%B3%BC%ED%8C%90%EB%A7%A4%EB%A5%BC%20%EB%A7%89%EB%8A%94%EB%8B%A4.md
  - ./08-01.%ED%8A%B8%EC%9C%84%ED%84%B0%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%C2%B7%EA%B5%AC%EA%B8%80%20%EB%8F%85%EC%8A%A4%20%EB%8F%99%EC%8B%9C%20%ED%8E%B8%EC%A7%91%C2%B7%EC%8A%AC%EB%9E%99%20%EC%95%8C%EB%A6%BC%20%ED%8C%90%EC%A0%95%C2%B7%ED%81%AC%EB%A1%A4%EB%9F%AC%20%EC%A4%91%EB%B3%B5%20%EC%A0%9C%EA%B1%B0%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%C2%B7OT%C2%B7%ED%9D%90%EB%A6%84%EB%8F%84%C2%B7%EB%B8%94%EB%A3%B8%20%ED%95%84%ED%84%B0%EB%A1%9C%20%ED%91%BC%EB%8B%A4.md
  - ./08-02.Gmail%20%EC%9D%80%20SMTP%20%EB%A1%9C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20IMAP%C2%B7POP%20%EC%9C%BC%EB%A1%9C%20%EB%B0%9B%EC%9C%BC%EB%A9%B0%20Google%20Maps%20%EB%8A%94%20%ED%83%80%EC%9D%BC%EC%9D%84%20%EC%A4%8C%20%EB%A0%88%EB%B2%A8%EB%B3%84%EB%A1%9C%20%EB%AF%B8%EB%A6%AC%20%EA%B7%B8%EB%A0%A4%20%EB%82%B4%EB%A0%A4%EC%A4%80%EB%8B%A4.md
  - ./08-03.%EB%A9%94%ED%8A%B8%EB%A6%AD%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EC%9D%80%20%EC%8B%9C%EA%B3%84%EC%97%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EC%97%90%20%EC%93%B0%EA%B8%B0%EB%A5%BC%20%EB%AA%B0%EC%95%84%20%EB%8B%B4%EA%B3%A0%20%EC%88%98%EC%A7%91%C2%B7%EC%A7%88%EC%9D%98%C2%B7%EA%B2%BD%EB%B3%B4%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md
  - ./09-01.%EA%B7%BC%EC%A0%91%20%EA%B2%80%EC%83%89%EC%9D%80%20%EC%A7%80%EC%98%A4%ED%95%B4%EC%8B%9C%EC%99%80%20%EC%BF%BC%EB%93%9C%ED%8A%B8%EB%A6%AC%EB%A1%9C%20%EC%A7%80%EB%8F%84%EB%A5%BC%20%EA%B2%A9%EC%9E%90%EB%A1%9C%20%EB%82%98%EB%88%84%EA%B3%A0%20%EC%83%89%EC%9D%B8%EC%9D%B4%20%EC%9E%91%EC%9C%BC%EB%A9%B4%20%EC%83%A4%EB%94%A9%20%EB%8C%80%EC%8B%A0%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9C%BC%EB%A1%9C%20%EB%84%93%ED%9E%8C%EB%8B%A4.md
  - ./09-02.%EC%A6%9D%EA%B6%8C%20%EA%B1%B0%EB%9E%98%EC%86%8C%EB%8A%94%20%ED%98%B8%EA%B0%80%EC%B0%BD%EC%9C%BC%EB%A1%9C%20%EB%A7%A4%EC%88%98%C2%B7%EB%A7%A4%EB%8F%84%EB%A5%BC%20%EB%A7%9E%EC%B6%94%EA%B3%A0%20%EC%8B%9C%ED%80%80%EC%84%9C%EB%A1%9C%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EA%B3%A0%EC%A0%95%ED%95%98%EB%A9%B0%20%EC%9E%84%EA%B3%84%20%EA%B2%BD%EB%A1%9C%EB%A5%BC%20%ED%95%9C%20%EC%84%9C%EB%B2%84%EC%9D%98%20%EB%8B%A8%EC%9D%BC%20%EC%8A%A4%EB%A0%88%EB%93%9C%EB%A1%9C%20%EC%A4%84%EC%9D%B8%EB%8B%A4.md
  - ../system-design/README.md
  - ../sdp_system-design-primer/README.md
  - ../../README.md
learning:
  topic: bytebytego-system-design
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않는다
  blocked_count:
  next_lesson: "모든 주제 묶음 정독 완료 — 01-01 부터 Phase 4 자답·복습으로 넘어간다"
updated: 2026-10-13
---

# ByteByteGo System Design — 정독 인덱스

---

> 이 폴더는 ByteByteGo 의 「System Design」 그림 해설 모음을 주제별로 묶어 정리한 책-종속 학습노트입니다. 한두 쪽짜리 글과 그림을 주제가 같은 것끼리 묶어 한 편으로 썼고(모두 18편), 책·언어 목록 같은 목록형 글은 이 README 에서만 다룹니다.



## 이 묶음을 여기 두는 이유

> 사례 하나를 45분 동안 끝까지 설계하는 면접 책과 달리, 이 모음은 캐시 전략·격리 수준·전달 보장처럼 설계 중에 꺼내 쓰는 판단 하나를 그림 한 장으로 보여 줍니다.

[System Design Interview 정독본](../system-design/README.md)은 처리율 제한기·URL 단축기·채팅처럼 시스템 하나를 요구사항부터 상세 설계까지 따라갑니다. 이 모음은 그 과정에서 자주 나오는 부품과 맞바꿈을 짧게 떼어 냅니다. 예를 들어 면접 책이 "캐시를 둔다"고 결정하는 자리에서, 이 폴더의 [02-01](./02-01.%EC%BA%90%EC%8B%9C%20%EC%A0%84%EB%9E%B5%EC%9D%80%20%EC%9D%BD%EA%B8%B0%C2%B7%EC%93%B0%EA%B8%B0%20%EA%B2%BD%EB%A1%9C%EC%97%90%EC%84%9C%20%EC%BA%90%EC%8B%9C%20%EC%9E%90%EB%A6%AC%EB%A5%BC%20%EC%A0%95%ED%95%98%EA%B3%A0%20Redis%20%EB%8A%94%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%A3%A8%ED%94%84%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EB%8B%A4.md)은 그 캐시를 읽기·쓰기 경로의 어디에 두고 없는 키 공격을 어떻게 막는지를 다룹니다.

[System Design Primer 정독본](../sdp_system-design-primer/README.md)은 같은 부품을 primer 의 순서로 모아 둔 지도입니다. 세 폴더가 겹치는 주제는 노트 안에서 서로 링크하고 같은 설명을 두 번 쓰지 않습니다.



## 범위와 읽는 순서

> 원본은 글 순서에 주제 흐름이 없어서 노트 번호를 주제 축으로 새로 매겼습니다. 앞 번호일수록 뒤 노트가 부품으로 다시 쓰는 기초입니다.

| 번호 | 주제 축 | 편 |
|---|---|---|
| 01 | 데이터베이스 — 동시성·복제·분할 | 01-01, 01-02 |
| 02 | 캐시 | 02-01 |
| 03 | 네트워크와 API | 03-01, 03-02 |
| 04 | 저장소 | 04-01 |
| 05 | 메시징과 데이터 처리 | 05-01, 05-02 |
| 06 | 클라우드·배포·운영 | 06-01, 06-02 |
| 07 | 결제 | 07-01, 07-02, 07-03 |
| 08 | 서비스 사례 — 소셜·협업·메일·지도·모니터링 | 08-01, 08-02, 08-03 |
| 09 | 위치와 금융 시스템 | 09-01, 09-02 |

처음 읽는다면 01 → 02 → 03 순으로 부품을 세운 뒤 관심 있는 사례로 건너가도 됩니다. 07 의 세 편은 01-01 의 격리와 05-01 의 전달 보장을, 09-01 은 01-02 의 읽기 복제본과 08-02 의 지도 타일을 전제로 씁니다.

[System Design Interview 정독본의 수백만 사용자 확장](../system-design/01-01.%EB%8B%A8%EC%9D%BC%20%EC%84%9C%EB%B2%84%EC%97%90%EC%84%9C%20%EC%B6%9C%EB%B0%9C%ED%95%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20DB%20%EB%B6%84%EB%A6%AC%C2%B7%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C%C2%B7DB%20%EB%B3%B5%EC%A0%9C%EB%A1%9C%20%EC%B2%AB%20%EB%B3%91%EB%AA%A9%EC%9D%84%20%EB%84%98%EB%8A%94%EB%8B%A4.md) 편과 [그 뒤 확장](../system-design/01-02.%EC%BA%90%EC%8B%9C%C2%B7CDN%C2%B7%EB%AC%B4%EC%83%81%ED%83%9C%20%EC%9B%B9%20%EA%B3%84%EC%B8%B5%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%84%BC%ED%84%B0%C2%B7%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%C2%B7%EC%83%A4%EB%94%A9%EC%9D%B4%20%EC%88%98%EB%B0%B1%EB%A7%8C%20%EC%82%AC%EC%9A%A9%EC%9E%90%EA%B9%8C%EC%A7%80%20%EA%B7%9C%EB%AA%A8%EB%A5%BC%20%EB%8A%98%EB%A6%B0%EB%8B%A4.md) 편은 이 모음의 "수백만 사용자로 확장" 글과 겹쳐서, 그 글은 따로 쓰지 않고 06-02 에서 링크로 갈음했습니다.



## 작성된 정독 노트

> 편마다 묶은 원 글과 한 줄 핵심을 둡니다.

| 편 | 묶은 글 | 한 줄 핵심 |
|---|---|---|
| [01-01 격리 수준과 낙관적 잠금이 동시 쓰기의 이상 현상을 막고 데이터 모양이 데이터베이스 종류를 고른다](./01-01.%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EB%82%99%EA%B4%80%EC%A0%81%20%EC%9E%A0%EA%B8%88%EC%9D%B4%20%EB%8F%99%EC%8B%9C%20%EC%93%B0%EA%B8%B0%EC%9D%98%20%EC%9D%B4%EC%83%81%20%ED%98%84%EC%83%81%EC%9D%84%20%EB%A7%89%EA%B3%A0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EC%96%91%EC%9D%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%A2%85%EB%A5%98%EB%A5%BC%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md) | 격리 수준 · 데이터베이스 고르기 · 낙관적 잠금 · 지연과 일관성 | 네 격리 수준이 막는 이상 현상, MVCC·잠금과 버전 번호로 충돌을 잡는 낙관적 잠금, 복제 확인 수가 맞바꾸는 지연과 일관성, 데이터 모양으로 고르는 저장소 |
| [01-02 파티셔닝과 읽기 복제본은 데이터베이스를 넓히고 전역 유일 ID 는 나뉜 데이터에 순서를 준다](./01-02.%ED%8C%8C%ED%8B%B0%EC%85%94%EB%8B%9D%EA%B3%BC%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9D%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%A5%BC%20%EB%84%93%ED%9E%88%EA%B3%A0%20%EC%A0%84%EC%97%AD%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20%EB%82%98%EB%89%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%97%90%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EC%A4%80%EB%8B%A4.md) | 수직·수평 파티셔닝 · 읽기 복제본 두 편 · 전역 유일 ID | 열·행으로 나누고 읽기를 복제본으로 흩을 때 따라오는 샤딩 키·복제 지연, 서버를 가로질러 순서를 주는 ID |
| [02-01 캐시 전략은 읽기·쓰기 경로에서 캐시 자리를 정하고 Redis 는 메모리와 단일 스레드 이벤트 루프로 빠르다](./02-01.%EC%BA%90%EC%8B%9C%20%EC%A0%84%EB%9E%B5%EC%9D%80%20%EC%9D%BD%EA%B8%B0%C2%B7%EC%93%B0%EA%B8%B0%20%EA%B2%BD%EB%A1%9C%EC%97%90%EC%84%9C%20%EC%BA%90%EC%8B%9C%20%EC%9E%90%EB%A6%AC%EB%A5%BC%20%EC%A0%95%ED%95%98%EA%B3%A0%20Redis%20%EB%8A%94%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%A3%A8%ED%94%84%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EB%8B%A4.md) | 캐시 전략 · 캐시 미스 공격 · Redis 와 Memcached · Redis 가 빠른 이유 | miss 뒤 누가 채우는지와 쓰기를 언제 DB 에 넘기는지로 갈리는 캐시 경로, 널 캐시·블룸 필터, Redis 의 메모리·이벤트 루프·자료 구조 |
| [03-01 URL 을 치면 DNS·TCP·TLS·HTTP 를 거쳐 브라우저가 화면을 그리고 CDN 이 그 길을 줄인다](./03-01.URL%20%EC%9D%84%20%EC%B9%98%EB%A9%B4%20DNS%C2%B7TCP%C2%B7TLS%C2%B7HTTP%20%EB%A5%BC%20%EA%B1%B0%EC%B3%90%20%EB%B8%8C%EB%9D%BC%EC%9A%B0%EC%A0%80%EA%B0%80%20%ED%99%94%EB%A9%B4%EC%9D%84%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20CDN%20%EC%9D%B4%20%EA%B7%B8%20%EA%B8%B8%EC%9D%84%20%EC%A4%84%EC%9D%B8%EB%8B%A4.md) | URL 을 치면 · DNS 조회 · HTTPS · HTTP 1.0~3 · 브라우저 동작 · CDN | 이름 조회·연결·암호화 합의·요청의 왕복, 브라우저의 스타일·레이아웃·합성 단계, CDN 이 줄이는 거리 |
| [03-02 API 는 SOAP·REST·GraphQL·RPC 로 갈리고 토큰·HMAC·SSO·솔트 해시가 접근과 비밀번호를 지킨다](./03-02.API%20%EB%8A%94%20SOAP%C2%B7REST%C2%B7GraphQL%C2%B7RPC%20%EB%A1%9C%20%EA%B0%88%EB%A6%AC%EA%B3%A0%20%ED%86%A0%ED%81%B0%C2%B7HMAC%C2%B7SSO%C2%B7%EC%86%94%ED%8A%B8%20%ED%95%B4%EC%8B%9C%EA%B0%80%20%EC%A0%91%EA%B7%BC%EA%B3%BC%20%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%EB%A5%BC%20%EC%A7%80%ED%82%A8%EB%8B%A4.md) | API 스타일 비교 · 웹 API 접근 보안 · SSO · 비밀번호 저장 | 요청이 가리키는 대상으로 갈리는 API 스타일, 토큰·HMAC 서명·SSO 로 호출자를 증명하고 솔트를 섞은 느린 해시로 비밀번호를 지키는 법 |
| [04-01 블록·파일·객체 저장소는 접근 단위가 다르고 이레이저 코딩과 분할 업로드가 큰 데이터를 싸고 안전하게 담는다](./04-01.%EB%B8%94%EB%A1%9D%C2%B7%ED%8C%8C%EC%9D%BC%C2%B7%EA%B0%9D%EC%B2%B4%20%EC%A0%80%EC%9E%A5%EC%86%8C%EB%8A%94%20%EC%A0%91%EA%B7%BC%20%EB%8B%A8%EC%9C%84%EA%B0%80%20%EB%8B%A4%EB%A5%B4%EA%B3%A0%20%EC%9D%B4%EB%A0%88%EC%9D%B4%EC%A0%80%20%EC%BD%94%EB%94%A9%EA%B3%BC%20%EB%B6%84%ED%95%A0%20%EC%97%85%EB%A1%9C%EB%93%9C%EA%B0%80%20%ED%81%B0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%EC%8B%B8%EA%B3%A0%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EB%8B%B4%EB%8A%94%EB%8B%A4.md) | SSD · 블록·파일·객체 저장소 · 이레이저 코딩 · 큰 파일 올리기 | SSD 의 page 쓰기와 채널 병렬, 접근 단위로 갈리는 세 저장소, 복제의 절반 공간으로 같은 손실을 견디는 이레이저 코딩과 분할 업로드 |
| [05-01 Kafka 는 순차 IO 와 제로 카피로 빠르고 전달 보장은 최대 한 번·최소 한 번·정확히 한 번으로 갈린다](./05-01.Kafka%20%EB%8A%94%20%EC%88%9C%EC%B0%A8%20IO%20%EC%99%80%20%EC%A0%9C%EB%A1%9C%20%EC%B9%B4%ED%94%BC%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EA%B3%A0%20%EC%A0%84%EB%8B%AC%20%EB%B3%B4%EC%9E%A5%EC%9D%80%20%EC%B5%9C%EB%8C%80%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%B5%9C%EC%86%8C%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%A0%95%ED%99%95%ED%9E%88%20%ED%95%9C%20%EB%B2%88%EC%9C%BC%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md) | Kafka 가 빠른 이유 · 전달 보장 세 가지 · 당기기와 밀기 · 마이크로서비스의 협업 | 순차 IO·페이지 캐시·sendfile 로 빠른 Kafka, 오프셋 커밋 시점과 트랜잭션으로 갈리는 전달 보장, 당기는 소비자 |
| [05-02 빅데이터 기술은 GFS·MapReduce·BigTable 에서 출발해 OLTP·OLAP·스트림 처리 갈래로 앞 세대의 한계를 하나씩 풀었다](./05-02.%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B8%B0%EC%88%A0%EC%9D%80%20GFS%C2%B7MapReduce%C2%B7BigTable%20%EC%97%90%EC%84%9C%20%EC%B6%9C%EB%B0%9C%ED%95%B4%20OLTP%C2%B7OLAP%C2%B7%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%EA%B0%88%EB%9E%98%EB%A1%9C%20%EC%95%9E%20%EC%84%B8%EB%8C%80%EC%9D%98%20%ED%95%9C%EA%B3%84%EB%A5%BC%20%ED%95%98%EB%82%98%EC%94%A9%20%ED%92%80%EC%97%88%EB%8B%A4.md) | 빅데이터 논문 연대표 · 빅데이터의 진화 | 구글 논문 셋에서 갈라진 OLTP·OLAP·스트림 처리 갈래, 람다와 카파 아키텍처, Dataflow 모델 |
| [06-01 IaaS·PaaS·SaaS 와 가상 머신·컨테이너·서버리스는 운영 책임을 어디까지 넘기는지로 갈린다](./06-01.IaaS%C2%B7PaaS%C2%B7SaaS%20%EC%99%80%20%EA%B0%80%EC%83%81%20%EB%A8%B8%EC%8B%A0%C2%B7%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7%EC%84%9C%EB%B2%84%EB%A6%AC%EC%8A%A4%EB%8A%94%20%EC%9A%B4%EC%98%81%20%EC%B1%85%EC%9E%84%EC%9D%84%20%EC%96%B4%EB%94%94%EA%B9%8C%EC%A7%80%20%EB%84%98%EA%B8%B0%EB%8A%94%EC%A7%80%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md) | IaaS·PaaS·SaaS · 가상화와 컨테이너 · AWS Lambda 내부 · 빅데이터용 클라우드 · 프로세스와 스레드 | 고객이 맡는 층의 수로 갈리는 서비스 모델, 믿지 못하는 코드를 갈라 놓는 층으로 갈리는 가상 머신·컨테이너·서버리스 |
| [06-02 배포 전략은 새 버전을 얼마나 조금씩 내보낼지 정하고 장애 대응은 진단 도구와 사후 검토로 이어진다](./06-02.%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%EC%9D%80%20%EC%83%88%20%EB%B2%84%EC%A0%84%EC%9D%84%20%EC%96%BC%EB%A7%88%EB%82%98%20%EC%A1%B0%EA%B8%88%EC%94%A9%20%EB%82%B4%EB%B3%B4%EB%82%BC%EC%A7%80%20%EC%A0%95%ED%95%98%EA%B3%A0%20%EC%9E%A5%EC%95%A0%20%EB%8C%80%EC%9D%91%EC%9D%80%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%EC%99%80%20%EC%82%AC%ED%9B%84%20%EA%B2%80%ED%86%A0%EB%A1%9C%20%EC%9D%B4%EC%96%B4%EC%A7%84%EB%8B%A4.md) | 배포 전략 · 아마존의 빌드·운영 · 대규모 장애 대응 · 프로세스 진단 | 비율과 대기 시간을 정해 조금씩 내보내는 배포, 역할을 나눈 복구와 사후 검토, 자원별 진단 도구 |
| [07-01 온라인 결제는 카드 네트워크·SWIFT·외환 경로로 돈이 움직이고 지갑과 장부가 그 흐름을 기록한다](./07-01.%EC%98%A8%EB%9D%BC%EC%9D%B8%20%EA%B2%B0%EC%A0%9C%EB%8A%94%20%EC%B9%B4%EB%93%9C%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%C2%B7SWIFT%C2%B7%EC%99%B8%ED%99%98%20%EA%B2%BD%EB%A1%9C%EB%A1%9C%20%EB%8F%88%EC%9D%B4%20%EC%9B%80%EC%A7%81%EC%9D%B4%EA%B3%A0%20%EC%A7%80%EA%B0%91%EA%B3%BC%20%EC%9E%A5%EB%B6%80%EA%B0%80%20%EA%B7%B8%20%ED%9D%90%EB%A6%84%EC%9D%84%20%EA%B8%B0%EB%A1%9D%ED%95%9C%EB%8B%A4.md) | 온라인 결제의 미래 · SWIFT 결제망 · 결제의 외환 · 돈의 이동 | 메시지는 카드 네트워크와 SWIFT 로 곧바로, 돈은 장부와 준비금에서 나중에 순액으로 움직이는 결제 한 건 |
| [07-02 결제 정확성은 멱등 키로 이중 청구를 막고 대사로 장부 불일치를 찾고 토큰화로 카드 정보를 지킨다](./07-02.%EA%B2%B0%EC%A0%9C%20%EC%A0%95%ED%99%95%EC%84%B1%EC%9D%80%20%EB%A9%B1%EB%93%B1%20%ED%82%A4%EB%A1%9C%20%EC%9D%B4%EC%A4%91%20%EC%B2%AD%EA%B5%AC%EB%A5%BC%20%EB%A7%89%EA%B3%A0%20%EB%8C%80%EC%82%AC%EB%A1%9C%20%EC%9E%A5%EB%B6%80%20%EB%B6%88%EC%9D%BC%EC%B9%98%EB%A5%BC%20%EC%B0%BE%EA%B3%A0%20%ED%86%A0%ED%81%B0%ED%99%94%EB%A1%9C%20%EC%B9%B4%EB%93%9C%20%EC%A0%95%EB%B3%B4%EB%A5%BC%20%EC%A7%80%ED%82%A8%EB%8B%A4.md) | 이중 청구 막기 · 대사 두 편 · 결제 보안 | 재시도가 만든 중복을 멱등 키로 한 번만 처리하고, 어긋난 기록을 대사로 찾고, 카드 번호를 토큰으로 바꾸는 법 |
| [07-03 결제 시스템은 결제 이벤트를 결제 주문으로 나눠 PSP 에 맡기고 플래시 세일은 비동기 큐와 재고 차감 순서로 과판매를 막는다](./07-03.%EA%B2%B0%EC%A0%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EA%B2%B0%EC%A0%9C%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%EB%A5%BC%20%EA%B2%B0%EC%A0%9C%20%EC%A3%BC%EB%AC%B8%EC%9C%BC%EB%A1%9C%20%EB%82%98%EB%88%A0%20PSP%20%EC%97%90%20%EB%A7%A1%EA%B8%B0%EA%B3%A0%20%ED%94%8C%EB%9E%98%EC%8B%9C%20%EC%84%B8%EC%9D%BC%EC%9D%80%20%EB%B9%84%EB%8F%99%EA%B8%B0%20%ED%81%90%EC%99%80%20%EC%9E%AC%EA%B3%A0%20%EC%B0%A8%EA%B0%90%20%EC%88%9C%EC%84%9C%EB%A1%9C%20%EA%B3%BC%ED%8C%90%EB%A7%A4%EB%A5%BC%20%EB%A7%89%EB%8A%94%EB%8B%A4.md) | 결제 시스템 설계 · 플래시 세일 시스템 설계 | 구매 버튼 뒤 결제 이벤트·결제 주문·PSP·지갑·장부의 순서, 극단적 동시성을 비동기 큐와 재고 차감으로 견디는 플래시 세일 |
| [08-01 트위터 타임라인·구글 독스 동시 편집·슬랙 알림 판정·크롤러 중복 제거는 팬아웃·OT·흐름도·블룸 필터로 푼다](./08-01.%ED%8A%B8%EC%9C%84%ED%84%B0%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%C2%B7%EA%B5%AC%EA%B8%80%20%EB%8F%85%EC%8A%A4%20%EB%8F%99%EC%8B%9C%20%ED%8E%B8%EC%A7%91%C2%B7%EC%8A%AC%EB%9E%99%20%EC%95%8C%EB%A6%BC%20%ED%8C%90%EC%A0%95%C2%B7%ED%81%AC%EB%A1%A4%EB%9F%AC%20%EC%A4%91%EB%B3%B5%20%EC%A0%9C%EA%B1%B0%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%C2%B7OT%C2%B7%ED%9D%90%EB%A6%84%EB%8F%84%C2%B7%EB%B8%94%EB%A3%B8%20%ED%95%84%ED%84%B0%EB%A1%9C%20%ED%91%BC%EB%8B%A4.md) | 트위터 동작 · 구글 독스 설계 · 슬랙 알림 흐름도 · 중복 URL 피하기 · AI 코딩 엔진 | 한 요청의 비용을 쓸 때·읽을 때·서버에서·비트 하나로·만든 뒤 거르기 중 어디에 둘지 고르는 다섯 사례 |
| [08-02 Gmail 은 SMTP 로 보내고 IMAP·POP 으로 받으며 Google Maps 는 타일을 줌 레벨별로 미리 그려 내려준다](./08-02.Gmail%20%EC%9D%80%20SMTP%20%EB%A1%9C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20IMAP%C2%B7POP%20%EC%9C%BC%EB%A1%9C%20%EB%B0%9B%EC%9C%BC%EB%A9%B0%20Google%20Maps%20%EB%8A%94%20%ED%83%80%EC%9D%BC%EC%9D%84%20%EC%A4%8C%20%EB%A0%88%EB%B2%A8%EB%B3%84%EB%A1%9C%20%EB%AF%B8%EB%A6%AC%20%EA%B7%B8%EB%A0%A4%20%EB%82%B4%EB%A0%A4%EC%A4%80%EB%8B%A4.md) | 메일 받기·보내기 · Gmail 설계 · 지도 렌더링 · Google Maps 설계 | MX 레코드와 SMTP 로 넘기고 IMAP·POP3 로 가져가는 메일, 줌 레벨마다 4배씩 느는 256 픽셀 타일을 CDN 으로 내리는 지도 |
| [08-03 메트릭 모니터링은 시계열 데이터베이스에 쓰기를 몰아 담고 수집·질의·경보·시각화로 나뉜다](./08-03.%EB%A9%94%ED%8A%B8%EB%A6%AD%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EC%9D%80%20%EC%8B%9C%EA%B3%84%EC%97%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EC%97%90%20%EC%93%B0%EA%B8%B0%EB%A5%BC%20%EB%AA%B0%EC%95%84%20%EB%8B%B4%EA%B3%A0%20%EC%88%98%EC%A7%91%C2%B7%EC%A7%88%EC%9D%98%C2%B7%EA%B2%BD%EB%B3%B4%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md) | 메트릭 수집용 데이터베이스 · 메트릭 모니터링·경보 시스템 | 쓰기 중심 데이터를 시계열 데이터베이스에 몰고 수집·질의·경보·시각화를 갈라 놓는 구조 |
| [09-01 근접 검색은 지오해시와 쿼드트리로 지도를 격자로 나누고 색인이 작으면 샤딩 대신 읽기 복제본으로 넓힌다](./09-01.%EA%B7%BC%EC%A0%91%20%EA%B2%80%EC%83%89%EC%9D%80%20%EC%A7%80%EC%98%A4%ED%95%B4%EC%8B%9C%EC%99%80%20%EC%BF%BC%EB%93%9C%ED%8A%B8%EB%A6%AC%EB%A1%9C%20%EC%A7%80%EB%8F%84%EB%A5%BC%20%EA%B2%A9%EC%9E%90%EB%A1%9C%20%EB%82%98%EB%88%84%EA%B3%A0%20%EC%83%89%EC%9D%B8%EC%9D%B4%20%EC%9E%91%EC%9C%BC%EB%A9%B4%20%EC%83%A4%EB%94%A9%20%EB%8C%80%EC%8B%A0%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9C%BC%EB%A1%9C%20%EB%84%93%ED%9E%8C%EB%8B%A4.md) | 쿼드트리 · Yelp 의 근처 식당 찾기 · 개략적 규모 추정 | 지오해시 접두사와 쿼드트리로 근처를 찾고, 색인 크기를 어림해 샤딩 대신 읽기 복제본을 고르는 근접 서비스 |
| [09-02 증권 거래소는 호가창으로 매수·매도를 맞추고 시퀀서로 순서를 고정하며 임계 경로를 한 서버의 단일 스레드로 줄인다](./09-02.%EC%A6%9D%EA%B6%8C%20%EA%B1%B0%EB%9E%98%EC%86%8C%EB%8A%94%20%ED%98%B8%EA%B0%80%EC%B0%BD%EC%9C%BC%EB%A1%9C%20%EB%A7%A4%EC%88%98%C2%B7%EB%A7%A4%EB%8F%84%EB%A5%BC%20%EB%A7%9E%EC%B6%94%EA%B3%A0%20%EC%8B%9C%ED%80%80%EC%84%9C%EB%A1%9C%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EA%B3%A0%EC%A0%95%ED%95%98%EB%A9%B0%20%EC%9E%84%EA%B3%84%20%EA%B2%BD%EB%A1%9C%EB%A5%BC%20%ED%95%9C%20%EC%84%9C%EB%B2%84%EC%9D%98%20%EB%8B%A8%EC%9D%BC%20%EC%8A%A4%EB%A0%88%EB%93%9C%EB%A1%9C%20%EC%A4%84%EC%9D%B8%EB%8B%A4.md) | 마이크로초 지연 · 매수·매도 주문 맞추기 · 증권 거래소 설계 | 가격 레벨별 FIFO 호가창으로 주문을 맞추고 시퀀서로 결정성을 지키며 임계 경로를 한 서버의 CPU 고정 단일 스레드로 줄이는 거래소 |



## 노트로 쓰지 않은 글

> 책·언어 순위·면접 요령처럼 설명할 메커니즘이 없는 목록형 글은 노트를 두지 않고 여기에 무엇이 있는지만 적습니다.

| 글 | 무엇이 있나 | 이어지는 곳 |
|---|---|---|
| Most popular programming languages | Stack Overflow 설문 기준으로 많이 쓰는 언어 38개를 등장 연도순으로 늘어놓은 그림 | 없음 |
| How to learn design patterns? | GoF 의 『Design Patterns』가 어려웠다면 『Head First Design Patterns』 2판을 먼저 읽으라는 추천 | 없음 |
| DevOps Books | 『Accelerate』·『Continuous Delivery』·『Site Reliability Engineering』·『Effective DevOps』·『The Phoenix Project』·『The DevOps Handbook』 여섯 권의 한 줄 소개 | [DevOps 기초 정독본](../../../07_devops/book/fdsd_fundamentals-devops/)·[CI/CD 패턴 정독본](../../../07_devops/book/cicd_cicd-patterns/) |
| System Design Interview Tip | 면접 볼 회사의 엔지니어링 블로그를 읽으라는 요령과 Twitter 블로그 글 네 편 | [면접 네 단계](../system-design/03-01.%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%84%A4%EA%B3%84%20%EB%A9%B4%EC%A0%91%EC%9D%80%20%EB%B2%94%EC%9C%84%20%ED%99%95%EC%A0%95%C2%B7%EA%B0%9C%EB%9E%B5%20%EC%84%A4%EA%B3%84%C2%B7%EC%83%81%EC%84%B8%20%EC%84%A4%EA%B3%84%C2%B7%EB%A7%88%EB%AC%B4%EB%A6%AC%20%EB%84%A4%20%EB%8B%A8%EA%B3%84%EB%A1%9C%20%EC%A7%84%ED%96%89%ED%95%9C%EB%8B%A4.md) |
| Log4j 공격과 방어 그림 | 스위스 GovCERT 의 Log4j 제로데이 공격·방어 그림을 옮긴 한 쪽. 그림 원본은 [GovCERT 글](https://www.govcert.ch/blog/zero-day-exploit-targeting-popular-java-library-log4j/)에 있습니다 | 없음 |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 주제 묶음 18편 완료, 목록형 글 다섯은 위 표로 대신 |
| 난이도 레벨 | 기본. 학습자 자답 전이라 조정 근거는 아직 없습니다 |
| 막힌 지점 | 아직 없음 |
| 다음 레슨 후보 | 정독은 끝났습니다. 01-01 부터 Phase 4 자답으로 이해를 확인합니다 |
| 최근 검증 결과 | 2026-10-13 18편을 현행 규약으로 썼습니다. 편마다 원본 그림과 추출본, 공식 문서·RFC 같은 1차 자료로 대조하는 적대적 검증, 수정, 재검증, 재수정을 거쳤습니다. 원 글 이후 달라진 사실은 그 절의 본문에 1차 자료 링크와 함께 썼습니다 |
| 복습 회차 | 없음 |



## 출처와 톤

- 원본 PDF 가 1차 자료입니다. 파일명과 PDF 메타데이터의 제목은 System Design Interview Volume 1 이지만 내용은 ByteByteGo 의 짧은 그림 해설 모음이라 이 폴더에 따로 둡니다.
- 원 글의 그림은 저작권물이라 노트에 넣지 않았습니다. 노트의 도식은 모두 원 글을 읽고 다시 그린 것이고, 같은 글이 [system-design-101 저장소](https://github.com/ByteByteGoHq/system-design-101)에 있으면 노트의 `## 참고 자료` 에 링크했습니다.
- 노트는 책 없이 읽히게 씁니다. 본문에 그림 번호·쪽 같은 원본 지칭을 두지 않고, 출처는 frontmatter 와 `## 참고 자료` 에만 적습니다.
- 톤은 합니다체입니다. 도식 생성기는 `_assets/_gen/` 에 있고 `_assets/` 에서 실행합니다. `dd.py` 는 Learning eBPF 정독본 `_assets/dd.py` 의 사본입니다.
- 이 저장소의 원격은 공개 저장소이므로 실습 기록을 붙일 때 사내 주소·이름을 쓰지 않습니다.
