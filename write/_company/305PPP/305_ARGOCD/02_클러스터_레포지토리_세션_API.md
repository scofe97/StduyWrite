---
title: 305 ArgoCD 클러스터 레포지토리 세션 API
tags: [305p, argocd, cluster, repository, session]
status: final
source:
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/infrastructure/util/argocd/service/ArgoCdService.java
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/infrastructure/external/client/ArgoCdFeignClient.java
related:
  - ./01_Application_생성_수정_삭제_흐름.md
updated: 2026-04-23
---

# 305 ArgoCD 클러스터 레포지토리 세션 API
---
> ArgoCD 기반 API는 session token 발급, cluster 연결, repository 연결로 구성된다. Application 생성은 이 기반 연결이 준비되어 있어야만 진행된다.



## 조사 기준

> 이 문서는 ArgoCD FeignClient와 `ArgoCdService`의 기반 API를 기준으로 한다.

화면의 cluster CRUD는 `/cluster/v3`에서 TPS DB를 관리한다. ArgoCD에 실제 cluster를 연결하는 작업은 Application 생성 과정에서 `ClusterWriter.connectCluster`를 통해 수행된다.



## 현재 코드에서 실제로 쓰는 흐름

> ArgoCD API 호출은 먼저 session token을 받고, 이후 Bearer token으로 호출한다.

| 영역 | 외부 API | 현재 사용 방식 | 개선 관점 |
|---|---|---|---|
| session | `POST /api/v1/session` | username/password를 body로 보내 token을 받는다 | 실패 시 빈 token 반환을 막아야 한다 |
| settings | `GET /api/v1/settings` | `controllerNamespace`를 appNamespace로 사용한다 | namespace 누락 시 기본값 정책이 필요하다 |
| cluster 조회 | `GET /api/v1/clusters/{clusterUrl}` | URL encode 후 조회한다 | encode 후 lower-case 처리 위험을 확인해야 한다 |
| cluster 연결 | `POST /api/v1/clusters` | server, config 정보를 body로 보낸다 | 연결 실패와 권한 실패를 구분해야 한다 |
| cluster 해제 | `DELETE /api/v1/clusters/{clusterUrl}` | 실패 보상 또는 삭제 시 호출한다 | idempotent delete 정책이 필요하다 |
| repository 조회 | `GET /api/v1/repositories/{encodeRepoUrl}` | manifest repo 존재 여부를 확인한다 | 403을 not found로 보는 정책을 검토해야 한다 |
| repository 연결 | `POST /api/v1/repositories` | repo URL, type, username, password를 body로 보낸다 | credential 노출 방지가 필요하다 |
| repository 해제 | `DELETE /api/v1/repositories/{encodeRepoUrl}` | 최초 연결 보상 처리에서 호출한다 | 공유 repo 삭제 방지 검증이 필요하다 |



## 외부 API 사용 방식

> cluster와 repository API는 Application 생성 중 "없으면 연결"하는 보조 작업이다.

`ApplicationService.createApplication`은 ArgoCD cluster가 이미 있으면 연결을 건너뛴다. 없으면 `firstClusterYn`을 `true`로 두고 연결한다. repository도 같은 방식으로 `firstRepoYn`을 기록한다. 이후 Application 생성이나 sync가 실패하면, 최초 연결한 자원만 해제한다.

이 정책은 공유 cluster/repository를 잘못 삭제하지 않기 위한 방어로 볼 수 있다. 다만 최초 연결 판별이 로그와 DB 이력에 남지 않으면 운영자가 실패 보상 범위를 확인하기 어렵다.



## 개선점

> 기반 API는 인증 실패와 URL 처리 문제를 먼저 정리해야 한다.

- `getAuthInfo`는 인증 실패 시 빈 token을 담은 `ArgoCdAuthVo`를 반환할 수 있어 후속 API가 원인 불명의 실패로 이어진다.
- `encodeUrl(...).toLowerCase()` 계열 처리는 case-sensitive URL이나 repository path를 훼손할 수 있다.
- ArgoCD가 403을 not found처럼 반환하는 상황을 코드에서 일부 허용하지만, 권한 없음과 미존재를 구분하기 어렵다.
- repository 연결 body에는 username/password가 포함되므로 로그와 문서에 값이 노출되지 않아야 한다.
- cluster/repository 연결과 TPS cluster CRUD의 책임 경계를 운영 문서에 분리해서 표시해야 한다.



## 확인한 로컬 코드 위치

> 아래 파일에서 ArgoCD 기반 API 사용을 확인했다.

- `ArgoCdFeignClient.java`
- `ArgoCdService.java`
- `ClusterController.java`
- `ClusterWriterImpl.java`
- `ManifestRepositoryWriterImpl.java`
- `ApplicationService.java`
