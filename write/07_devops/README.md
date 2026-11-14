---
title: 07_devops MOC
tags: [moc, devops, jenkins, nexus]
status: final
related: []
updated: 2026-11-14
---

# 07_devops

> CI/CD, 아티팩트 저장소, 정적 분석 도구의 운영·확장 문서를 모읍니다. Jenkins 중심입니다.



## 경계 기준

Jenkins 파이프라인 그루비 작성법은 여기로 배치합니다. 반면 Jenkins가 만들어 낸 메트릭을 해석하는 대시보드 구성은 [`06_observability/`](../06_observability/)로 분류합니다.



## 키워드

### devops-keywords.md

키워드 파일: [devops-keywords.md](devops-keywords.md)

| 묶음 | 다룬 문서 | 빈 필수 키워드 |
|---|---|---|
| 1단계 · 전달 모델 | 7편 | — |
| 2단계 · CI 파이프라인 | 27편 | 머지 게이트 — branch protection · required status checks 로 실패한 PR 병합 차단 |
| 3단계 · 산출물 | 7편 | 컨테이너 실행과 점검 — `docker run` · `logs` · `exec` · `inspect` · 포트 · 볼륨 · 네트워크 · Build Once, Deploy Many — 같은 digest 를 staging 에서 prod 로 승격 |
| 4단계 · 패키징 | 0편 | — |
| 5단계 · GitOps | 5편 | — |
| 6단계 · 점진 배포 | 5편 | Expand and Contract — DB 스키마 변경과 버전 공존 · dual write · backfill |
| 7단계 · 인프라를 코드로 | 2편 | — |
| 8단계 · 파이프라인 보안 | 13편 | — |



## 하위 폴더·문서 목록

- [`02_Jenkins/`](02_Jenkins/) — 7개 주제 묶음 (2026-06-10 [`07_engine`](02_Jenkins/07_engine/) 신설)
  - [`01_core/`](02_Jenkins/01_core/) — Jenkins 제어 영역과 Declarative Pipeline 기초
  - [`02_security/`](02_Jenkins/02_security/) — 인증·인가·시크릿·JCasC
  - [`03_agent/`](02_Jenkins/03_agent/) — VM/Docker Agent·이미지 빌드·Kubernetes Jenkins
  - [`04_api/`](02_Jenkins/04_api/) — REST API 18+편 (TPS 통합 패턴 포함)
  - [`05_operations/`](02_Jenkins/05_operations/) — 내구성·가용성·공유 라이브러리·Groovy 커스텀·Hook
  - [`06_infra/`](02_Jenkins/06_infra/) — 용량 산정·IaC·GitHub/SonarQube/Artifactory 통합·CI/CD 구현
  - [`07_engine/`](02_Jenkins/07_engine/) — 엔진 심화: 내부 동작(Stapler·큐·실행기)·플러그인 확장·Script Console 제어·외부 통합
  - `_archive/`, `_practice/` (이전 검토본·실습 코드)
- [`03_Nexus/`](03_Nexus/) — 아티팩트 저장소
- [`book/`](book/) — 단행본 정독 노트
- [`docs/`](docs/) — 공식 문서 기반 노트
  - [`sonarqube/`](docs/sonarqube/) — 정적 분석, Quality Gate, CI 연계, Web API (2026.1 LTA 기준 19편)
