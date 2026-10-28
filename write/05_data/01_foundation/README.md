---
title: 05_data/01_foundation — 데이터 시스템 기초
tags: [moc, theory, transaction, mvcc, index, nosql, caching, wal]
status: final
related:
  - ../README.md
  - ../book/designing-data-intensive-applications/README.md
updated: 2026-10-28
---

# 05_data/01_foundation — 데이터 시스템 기초
---
> 책 한 권의 장 순서에 매이지 않는 데이터 시스템 기초 5편입니다. DDIA 의 데이터 모델·저장·복제·트랜잭션·배치·스트림 이론은 2판 정독 노트 [`book/designing-data-intensive-applications/`](../book/designing-data-intensive-applications/README.md)가 정본이고, 이 폴더에는 1판 요약 중 2판에 없는 PostgreSQL MVCC 설명이 든 트랜잭션 편(01-04)과 인덱스·NoSQL·캐싱·WAL 편이 남아 있습니다.

## 문서

| # | 문서 |
|---|------|
| 01-04 | [트랜잭션과 격리 수준](01-04.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EA%B3%BC%20%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80.md) |
| 01-05 | [인덱스 이론](01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) |
| 01-06 | [NoSQL 비교](01-06.NoSQL%20%EB%B9%84%EA%B5%90.md) |
| 01-07 | [캐싱 전략](01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) |
| 03-04 | [WAL 패턴](03-04.WAL%20%ED%8C%A8%ED%84%B4.md) |

번호는 옛 목록의 번호를 그대로 둡니다. 다른 문서 여럿이 이 번호가 붙은 파일명으로 링크하고 있어서, 번호를 바꾸면 그 링크를 모두 고쳐야 합니다.

## 1판 요약을 걷어 낸 이유

이 폴더에는 DDIA 1판을 요약한 노트 14편이 있었습니다. 그중 13편은 같은 주제를 2판 정독 노트가 장별로 다루고 있어 2026-10-28 에 지웠고, 그 13편을 가리키던 링크는 2판 노트의 해당 편으로 옮겼습니다. 지운 원문은 git 이력에 남아 있습니다. 01-04 는 2판 `08-02` 에 없는 PostgreSQL MVCC 구현 설명(`xmin`·`VACUUM`·long-running transaction)과 격리 수준 선택 가이드가 들어 있어 남겼습니다. 이 밖에 2판에 대응 절이 없는 내용(멀티테넌시 샤딩 모델 비교, 조정 회피 시스템 등)은 알고 지웠습니다.
