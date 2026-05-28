---
title: 07_devops MOC
tags: [moc, devops, jenkins, nexus]
status: final
related: []
updated: 2026-04-19
---

# 07_devops
---
> CI/CD, 아티팩트 저장소, 정적 분석 도구의 운영·확장 문서를 모은다. Jenkins 중심이다.

## 경계 기준

Jenkins 파이프라인 그루비 작성법은 여기로 온다. 반면 Jenkins가 만들어낸 메트릭을 해석하는 대시보드 구성은 `06_observability/`다.

## 하위

- `01_Sonarqube/` — 정적 분석, Quality Gate
- `02_Jenkins/` — 5개 주제 묶음 (2026-05-28 재구조화)
  - `01_core/` — Jenkins 제어 영역과 Declarative Pipeline 기초
  - `02_security/` — 인증·인가·시크릿·JCasC
  - `03_agent/` — VM/Docker Agent·이미지 빌드·Kubernetes Jenkins
  - `04_api/` — REST API 18+편 (TPS 통합 패턴 포함)
  - `05_operations/` — 내구성·가용성·공유 라이브러리·Groovy 커스텀·Hook
  - `_archive/`, `_practice/` (이전 검토본·실습 코드)
- `03_Nexus/` — 아티팩트 저장소
- `04_OS/` — 운영 OS 레벨 설정
