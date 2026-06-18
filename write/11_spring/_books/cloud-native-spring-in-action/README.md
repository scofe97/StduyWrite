---
title: Cloud Native Spring in Action — 책 요약 MOC
tags: [moc, spring, spring-boot, cloud-native, book-summary]
status: draft
source:
  - "Cloud Native Spring in Action, Thomas Vitale (Manning, 2021)"
related:
  - ../../README.md
updated: 2026-06-09
---


# Cloud Native Spring in Action — 책 요약 MOC
---
> Thomas Vitale의 *Cloud Native Spring in Action*(Manning)을 정리하는 학습 노트 모음입니다. 이 페이지가 이 책의 진입점이 됩니다.


## 왜 책 전용 폴더인가

`11_spring/`의 다른 폴더(`01_core`, `02_data-binding` 등)는 주제 축으로 묶입니다. 반면 이 폴더는 **책 한 권의 흐름**을 보존합니다. 이 책은 Spring Boot로 클라우드 네이티브 앱을 짓는 실무서라, 15-Factor 방법론·외부화 설정·복원력·쿠버네티스 배포 같은 운영 관점이 챕터마다 이어집니다. 전체를 순서대로 읽기보다 **필요한 챕터를 골라** 깊게 보는 쪽이 잘 맞습니다. 그래서 이 폴더는 선택한 챕터만 정리하며, 각 편을 다 쓴 뒤에는 해당 주제의 정식 카테고리 폴더로 교차참조를 겁니다.


## 챕터 목록

선택한 챕터만 정리합니다. 챕터순이 아니라 받은 순서대로 채우며, 파일명은 책의 실제 챕터 번호를 그대로 씁니다.

| # | 파일 | 상태 |
|---|------|------|
| 04 | [외부화 설정 관리 — 프로퍼티·프로파일·Spring Cloud Config](04.외부화%20설정%20관리.md) | draft |
| 05 | [클라우드 데이터 영속화와 관리 — Spring Data JDBC·Testcontainers·Flyway](05.클라우드%20데이터%20영속화와%20관리.md) | draft |
| 06 | [Spring Boot 컨테이너화 — Dockerfile·Buildpacks·Docker Compose·GitHub Actions](06.Spring%20Boot%20컨테이너화.md) | draft |

> 외부화 설정(4장)은 같은 주제의 노션 원본(`_notion_import/msa/02-1~02-4`)이 따로 있습니다. 그쪽은 가공 전 보관소이고, 이 노트는 책 관점(15-Factor·immutable build)으로 독립 정리하면서 related로 교차참조합니다.


## 작성 규약

이 폴더의 모든 노트는 writing 스킬 `07-04-book-summary.md` 정본의 풀 구조를 따릅니다. 핵심요약·학습목표·본문정리·심화학습·실무적용·면접대비·체크리스트를 갖추고, 설명은 면접에서 말할 수 있는 완전한 문장으로 씁니다. 각 편은 핵심요약 SVG 1개와, 원서 그림을 다크 테마로 재현한 SVG를 포함합니다(코드는 원형 보존, 라벨만 한글로 옮김).
