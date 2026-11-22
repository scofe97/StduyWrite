---
title: 07_devops MOC
tags: [moc, devops, jenkins, nexus]
status: final
related: []
updated: 2026-11-21
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

- [`03_Nexus/`](03_Nexus/) — 아티팩트 저장소
- [`book/`](book/) — 단행본 정독 노트
  - [`argocd-up-and-running/`](book/argocd-up-and-running/README.md) — 《Argo CD: Up and Running》 정독 노트 16편 (5단계 GitOps)
- [`docs/`](docs/) — 공식 문서 기반 노트
  - [`jenkins/`](docs/jenkins/README.md) — Jenkins 구조·엔진·Pipeline·Groovy 확장·보안·운영·REST API 를 원리 중심으로 다룬 20편
  - [`sonarqube/`](docs/sonarqube/) — 정적 분석, Quality Gate, CI 연계, Web API (2026.1 LTA 기준 19편)
  - [`iac/`](docs/iac/README.md) — IaC 개념 폴더. Helm 다섯 편(차트 작성·values와 렌더 검증·릴리스 운영·Hook·의존성과 저장소), Kustomize (4단계 패키징·7단계 인프라를 코드로)
  - [`cmd/`](docs/cmd/README.md) — DevOps 명령어 시트. 도구별 분류와 후보 명령 (시트는 아직 없음). 컨테이너·쿠버네티스 명령은 [08_cloud 의 시트](../08_cloud/docs/cmd/README.md)
