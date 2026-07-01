---
title: 04_cicd MOC
tags: [moc, devops, cicd, ci-cd, design-pattern, book]
status: draft
related:
  - ../README.md
  - ./roadmap.md
  - ./book/fdsd_fundamentals-devops/README.md
  - ./book/cicd_cicd-patterns/README.md
  - ./book/aic_ai-infra-claude/README.md
updated: 2026-06-29
---

# 04_cicd
---
> 특정 도구에 묶이지 않는 DevOps·CI/CD 이론을 모은다. 단행본 정독 노트와 도구 공통 개념 로드맵이 두 축이다.

## 경계 기준

이 카테고리는 **도구 종속이 아닌 일반 이론**을 다룬다. Jenkins 파이프라인 그루비 작성법은 `02_Jenkins/`, SonarQube Quality Gate 운영은 `01_Sonarqube/`, Nexus 아티팩트 저장소는 `03_Nexus/`로 간다. 반면 "CI/CD란 무엇이고 도구를 관통하는 공통 골격은 무엇인가", "배포 전략·디자인 패턴은 어떻게 분류되는가" 같은 도구 무관 개념은 여기로 온다.

`roadmap.md`는 Jenkins·Woodpecker·Concourse·Tekton·Argo·Rundeck 등 여러 도구를 관통하는 공통 개념(실행·격리·상태·권한·산출물·배포·감사)의 키워드 원문 기록이다. 도구별 심화는 각 도구 폴더가 맡고, 이 문서는 "도구 이름이 바뀌어도 남는 것"의 SSOT다.

## 하위

- `roadmap.md` — CI/CD 공통 개념 로드맵 (33섹션 + 도구 비교표 + Level 1~8 학습 경로). 도구 독립형 Jenkins-light 후보 분석 포함.
- `book/` — 단행본 정독 노트. 상위 `05_JVM/book/`과 같이 책 전용 폴더로 출처를 구분한다.
  - `fdsd_fundamentals-devops/` — 《Fundamentals of DevOps and Software Delivery》 (11장). 배포·IaC·오케스트레이션·CI/CD·네트워킹·보안·데이터·모니터링까지 소프트웨어 딜리버리 전체 라이프사이클.
  - `cicd_cicd-patterns/` — 《CI/CD Design Patterns》 (14장). GoF 디자인 패턴 렌즈로 본 CI/CD — 구조·행위·생성 패턴, 배포 전략, 안티패턴.
  - `aic_ai-infra-claude/` — 《AI 인프라 — Claude로》 (sysnet4admin, 9장). Claude Code로 GKE 위에 배포 인프라를 직접 쌓는 실습서. 핵심 개념은 GitOps+AI=**GitAIOps**. GitOps(ArgoCD)·관측 가능성·무중단 배포(Blue/Green→Canary)·규모 확장(멀티 노드풀·멀티테넌시)·위험 작업 통제(command-guardrails). 1~2장 정독 노트 5편 완료, 3장부터 진행 중.

## 톤·시각화

정독 노트는 합니다체로 쓰고, 각 편 도입부에 요약 SVG 1장(`_assets/`)을 임베드하며 흐름·상태전이에 Mermaid를 더한다. 상위 writing 스킬 SSOT를 따른다. 로드맵은 원문 키워드 기록이므로 `status: reference`로 두고 사실·표·수치를 보존한다.
