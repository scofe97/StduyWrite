---
title: 305 ArgoCD 연동 인덱스
tags: [305p, argocd, manifest, deployment]
status: final
source:
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/presentation/application/api/ApplicationController.java
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/presentation/manifest/api/ManifestControllerV3.java
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/infrastructure/external/client/ArgoCdFeignClient.java
related:
  - ../305_JENKINS/00_Jenkins_연동_인덱스.md
updated: 2026-04-23
---

# 305 ArgoCD 연동 인덱스
---
> ArgoCD 연동 문서는 Application API 목록이 아니라 유스케이스별 조합을 기준으로 읽는다. 생성은 통합관리, manifest DB, cluster/repository 연결, ArgoCD Application 생성/sync가 묶이고, 배포는 Jenkins callback, GitLab manifest 수정, ArgoCD sync가 묶인다.



## 문서 맵

> ArgoCD 문서는 Application 생성, 기반 API, deploy callback, rollback, 조회 API 순서로 읽는다.

| 문서 | 범위 | 핵심 내용 |
|---|---|---|
| [01_Application_생성_수정_삭제_흐름.md](01_Application_생성_수정_삭제_흐름.md) | Application 관리 | 통합관리, manifest, cluster/repository 연결, Application 생성/sync |
| [02_클러스터_레포지토리_세션_API.md](02_클러스터_레포지토리_세션_API.md) | 기반 API | session token, cluster, repository API |
| [03_매니페스트_배포_동기화_callback.md](03_매니페스트_배포_동기화_callback.md) | deploy callback | logging callback, manifest image tag 변경, ArgoCD sync |
| [04_배포실패_롤백_복구_흐름.md](04_배포실패_롤백_복구_흐름.md) | rollback | deploy failure, rollback availability, recovery application |
| [05_리소스_트리_로그_이벤트_조회_API.md](05_리소스_트리_로그_이벤트_조회_API.md) | 조회 API | resource-tree, resource manifest, events, logs, diff |



## 공통 구조

> Application 생성은 ArgoCD에 Application을 만들기 전에 TPS 통합관리와 manifest 정보를 먼저 만든다.

`ApplicationService.createApplication`은 application 중복을 확인하고, 통합관리로 manifest 파일을 등록하고, TPS application key와 manifest DB 정보를 만든다. 이후 toolchain에서 ArgoCD/GitLab/cluster 정보를 조회하고, ArgoCD에 cluster와 repository가 없으면 연결한 뒤 Application을 생성하고 sync한다.

`ManifestWriterImpl.updateManifestInfoByPipeline`은 Jenkins 배포 pipeline 종료 후 logging-api callback으로 호출된다. 이 흐름은 GitLab manifest 파일의 image tag를 새 tag로 바꾸고, 통합관리의 manifest branch/commit을 갱신한 뒤 ArgoCD sync를 호출한다.



## 유스케이스 읽기 순서

> ArgoCD는 생성, 배포, 실패 복구, 조회 순서로 API가 조합된다.

| 순서 | 유스케이스 | 조합되는 시스템 |
|---|---|---|
| 1 | Application 최초 등록 | Application API, 통합관리, manifest DB, ArgoCD session/cluster/repository/application/sync API |
| 2 | 배포 pipeline 종료 후 manifest 반영 | ppln-logging callback, GitLab manifest repo, 통합관리 deploy update, ArgoCD Application update/sync |
| 3 | 배포 실패와 rollback | deploy failure 상태 갱신, trigger rollback 가능 여부, 통합관리 rollback, ArgoCD recovery sync |
| 4 | 리소스 조회와 운영 확인 | Application 조회 API, ArgoCD resource-tree/resource/events/logs/managed-resources API |



## 공통 인증 규칙

> ArgoCD API는 session token을 받아 Bearer token으로 호출한다.

`ArgoCdService.getAuthInfo`는 `/api/v1/session`에 username/password를 보내 token을 얻고, 이후 API에는 `Authorization: Bearer {token}`을 사용한다. token 발급 실패 시 빈 token이 반환될 수 있으므로, 호출자 쪽에서 인증 실패를 명확히 드러내는 개선이 필요하다.



## 확인한 로컬 코드 위치

> 아래 파일을 기준으로 ArgoCD 문서를 나누었다.

- `ApplicationController.java`
- `ManifestControllerV3.java`
- `ClusterController.java`
- `ApplicationService.java`
- `ManifestService.java`
- `ApplicationWriterImpl.java`
- `ManifestWriterImpl.java`
- `ClusterWriterImpl.java`
- `ManifestRepositoryWriterImpl.java`
- `ArgoCdFeignClient.java`
- `ArgoCdService.java`
