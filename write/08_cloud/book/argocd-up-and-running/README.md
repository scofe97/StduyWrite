---
title: Argo CD Up and Running — 정독 인덱스
tags: [moc, study-index, book, argocd, gitops, kubernetes, helm, applicationset, multi-tenancy]
status: draft
source:
  - 《Argo CD: Up and Running — A Hands-On Guide to GitOps and Kubernetes》(Andrew Block · Christian Hernandez, O'Reilly, 2025, ISBN 978-1-098-14200-1) — 판 표기는 확인 안 됨 (서문 저작권 줄에 판 표시 없음)
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Argo CD Up and Running/ (서문 + 14개 장)
  - https://www.schweitzer-online.de/en/buch/Block/Argo-CD-Up-Running/9781098142001/A71915297/  # 저자·출판사·출판일(2025-07-01 표기)·ISBN-13·280쪽·저자 소개 확인 (2026-11-06 조회)
related:
  - ../cks-study-guide/README.md
  - ../kubernetes-up-and-running/README.md
  - ../../argocd/README.md
  - ../../../roadmap/devops-roadmap.md
  - ../../README.md
learning:
  topic: argocd-up-and-running
  scope: durable
  level: 기본
  last_verified:
  blocked_count:
  next_lesson: "2장 02-01 정독 노트 검증·반영"
updated: 2026-11-06
---

# Argo CD Up and Running — 정독 인덱스
---
> 이 폴더는 《Argo CD: Up and Running》(Andrew Block · Christian Hernandez, O'Reilly, 2025)을 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

> 이 책은 클러스터 위에 놓이는 GitOps·CD 계층을 맡습니다. 형제 책이 클러스터 안쪽을 다루는 동안, 이 책은 Git에 적은 선언을 클러스터가 따라가게 만드는 도구 하나를 끝까지 파고듭니다.

### 클러스터 위에 놓이는 GitOps·CD 계층

`08_cloud`는 "클러스터 내부에서 어떻게 돌아가는가"를 다루는 카테고리입니다. 이 책은 그 위에서 **GitOps**(Git 저장소에 적어 둔 선언을 기준 상태로 삼아 인프라와 애플리케이션을 관리하는 방식)를 실현하는 도구 Argo CD 를 다룹니다.

저자 두 사람은 각각 Helm 과 OpenGitOps 쪽 메인테이너로 소개됩니다.[^author] 서문은 GitOps 가 쿠버네티스에서 플랫폼 관리의 초석이 되었다고 설명합니다. 그 방식을 구현하는 도구로는 Argo CD 가 가장 널리 쓰인다고 덧붙입니다. 그래서 이 책은 개념 소개에 머물지 않습니다. 설치와 Application 에서 출발해 동기화, 인증, 멀티테넌시, 보안, 대규모 배포, 확장, CI 연동, 운영 순서로 한 도구를 따라갑니다.

### 형제 책과 보는 층의 차이

[『Kubernetes: Up and Running』](../kubernetes-up-and-running/README.md)은 쿠버네티스 오브젝트와 클러스터 운영을 다룹니다. 무엇을 클러스터에 올리는가가 질문입니다.

[『CKS Study Guide』](../cks-study-guide/README.md)는 기본 설정이 열어 둔 공격 표면을 닫는 하드닝 절차를 다룹니다. 이 책의 9장 보안은 Argo CD 자신의 TLS, 저장소 자격 증명, 서명 검증, 동기화 권한을 다루므로 클러스터 하드닝은 그쪽에 맡깁니다.

이 책의 질문은 올릴 대상을 Git 에 적어 두고, 클러스터가 그 선언을 계속 따라가게 하려면 무엇이 필요한가입니다.

### 옛 argocd/ 노트와의 관계

[옛 argocd/ 노트](../../argocd/README.md) 16편은 이 책을 바탕으로 쓴 것입니다. 16편 가운데 14편은 frontmatter `source` 에 `docs/03_CloudNative/03_ArgoCD/NN_<장 이름>.md` 를 적었고, 그 장 이름이 이 책의 장 이름과 같습니다. 다만 책의 서지가 어디에도 적혀 있지 않아 출처가 끊긴 상태였습니다.

장별 정독 노트를 쓰면서 옛 노트와 그 `deepdive/` 점검 질문, [ArgoCD와 GitOps](../../kubernetes/11_devtools/11-03.ArgoCD%EC%99%80%20GitOps.md), [ArgoCD App-of-Apps 패턴](../../../99_ETC/2026-04-19_ArgoCD%20App-of-Apps%20%ED%8C%A8%ED%84%B4.md)을 보충 재료로 흡수합니다. 모든 장이 흡수되면 옛 자리를 정리합니다. 옛 노트 04-03 Argo Rollouts 는 책에 대응하는 장이 없으므로 `docs/argo-rollouts/` 로 옮길 예정입니다.

### 로드맵 속 자리

[DevOps 로드맵](../../../roadmap/devops-roadmap.md)의 5단계 GitOps 는 개념 행 네 개로 나뉩니다. 대응하는 장은 다음과 같습니다. GitOps 원칙과 선언은 1~3장, 동기화와 배포 제어는 4·5장, 대규모 배포와 테넌시는 7·8·10장입니다. 환경 승격과 연계는 12장과 14장의 GitOps Promotions 절에 대응합니다.

6단계 점진 배포의 Argo Rollouts 행에는 대응하는 장이 없습니다. 14장은 Argo CD 가 점진 배포를 직접 하지 않고 Argo Rollouts 같은 다른 도구에 맡긴다고 짧게 밝힙니다. 세부는 책의 범위 밖이라고 선을 긋습니다. 10장의 Progressive Sync 는 ApplicationSet 이 Application 을 단계적으로 동기화하는 기능입니다. 트래픽을 나누는 점진 배포와는 다른 것입니다.

### 책의 전제

서문에 따르면 대상 독자는 GitOps 로 클라우드 네이티브 기술의 사용자 경험을 높이려는 쿠버네티스 관리자와 개발자입니다. 쿠버네티스 설치와 클러스터 수명주기 관리는 다루지 않고, 예제는 Helm 을 중심에 두며 로컬 클러스터는 kind 로 만듭니다. 준비물은 kind, Helm, kubectl, argocd CLI, jq·yq, Git 이고 예제 코드는 별도 Git 저장소로 제공됩니다.[^bib]





## 장별 목표

> 각 장 PDF 앞머리의 저자 선언을 `pdftotext`로 추출해 근거로 삼았습니다. 원문에 없는 목표를 추측해 넣지 않으며, 서문은 행으로 두지 않았습니다.

| 장 | 제목 | 저자가 선언한 목표 | 주요 토픽 |
|----|------|------------------|----------|
| 1 | Introduction to Argo CD | 클러스터 난립(cluster sprawl)이라는 쿠버네티스 도입 과제에서 출발해, Argo CD 가 무엇이고 쿠버네티스·클라우드 네이티브 생태계에서 어떤 역할을 하는지 설명함 | What Is Argo CD?, Why Argo CD?(애플리케이션 정의 통일·구성 드리프트·롤백과 재해 복구), GitOps 운동(기원·OpenGitOps 원칙 네 가지), Flux 와 Argo CD 비교, Argo 생태계 |
| 2 | Installing Argo CD | Argo CD 의 아키텍처와 설계를 소개하고, 쿠버네티스 환경에 설치하는 여러 방법을 설명함 | 컨트롤러 패턴, 커스텀 리소스, Repository Server·API server·Redis·Notifications, 핵심 패턴, YAML 매니페스트·Helm·Argo CD Operator 설치, 고가용성 |
| 3 | Interacting with Argo CD | 완전 선언형 구성 모델을 전제로, 서버와 직접 상호작용하는 UI·CLI·REST API 같은 수단을 2장 위에 더해 소개함 | UI 심화(Ingress 로 노출, Settings 페이지), CLI, OpenAPI 명세와 REST API, 선언적 구성(ConfigMap·Secret 종류) |
| 4 | Managing Applications | Application 의 기본, 구성 요소(연결 가능한 소스 종류 포함), Argo CD 가 기본 지원하는 템플릿 도구 사용법, Application 의 생애주기를 다룸 | Application 개요, 소스(Git·Helm)와 대상 클러스터, Helm, Kustomize, 첫 Application 배포, 삭제와 finalizer |
| 5 | Synchronizing Applications | 동기화가 시작되는 시점과 리소스를 적용하는 방식의 선택지, 그것이 Application·Argo CD 서버·대상 클러스터에 미치는 영향을 살핌 | 동기화 기본값과 자동 동기화, Sync Options(Application·리소스 수준), Hooks 와 Sync Waves, ignoreDifferences, 사용 사례(데이터베이스 스키마 설정), Probes |
| 6 | Authentication and Authorization | 사용자가 어디에 어떻게 정의되는지, 도구에서 무엇을 할 수 있는지, 접근을 제어하는 RBAC 정책을 어떻게 정의하는지 설명함 | admin 사용자, 로컬 사용자, 인증 토큰, SSO(Dex·직접 OIDC, Keycloak 실습, CLI SSO), RBAC, 사용자 정의 역할, 기본 정책과 익명 접근 |
| 7 | Cluster Management | 클러스터가 Argo CD 에서 어떻게 관리되는지, 컨트롤 플레인 어디에 어떻게 정의되는지, 멀티테넌트 상황에서 접근을 어떻게 제어하는지 설명함 | 클러스터 아키텍처(로컬·원격, 허브 앤 스포크), 클러스터 정의 방식, 원격 클러스터 추가(CLI·선언적), 여러 클러스터에 배포(App-of-Apps·Helm·ApplicationSet) |
| 8 | Multi-Tenancy | 6장의 RBAC 지식을 AppProject 개념과 프로젝트 단위 RBAC 구성 관리로 넓힘 | 설치 모드(클러스터 범위·네임스페이스 범위), Projects, 프로젝트로 하는 리소스 관리, 사용 사례(GitOps 대시보드) |
| 9 | Security | Argo CD 의 보안 수준을 높이는 방법과 대상 시스템과의 안전한 통신, 수명주기 곳곳의 민감 정보를 노출되지 않게 다루는 방법을 살핌 | Argo CD 서버 보안, TLS 인증서, 저장소 TLS 인증서, HTTPS·SSH 인증, 자격 증명 템플릿, GPG 서명 검증, Application Sync Impersonation |
| 10 | Applications at Scale | sync wave 를 쓴 App-of-Apps 와 Progressive Sync 를 쓴 ApplicationSet 같은 배포 패턴으로 Application 사이 의존성을 관리하고 대규모 배포를 돕는 방법을 탐색함 | Application 의 한계, 모범 사례(Probes·헬스 체크·Application Health·최종 일관성), 사용 사례 설정, ApplicationSets, Progressive Sync |
| 11 | Extending Argo CD | 기본 구성을 넘어 확장하는 여러 메커니즘, 그중에서도 리소스 생성 도구를 끼우는 플러그인 프레임워크를 소개함 | Config Management Plugins(매니페스트·등록·환경 변수·파라미터), UI 맞춤(Custom Styles·UI Extensions) |
| 12 | Integrating CI with Argo CD | CI 시스템과 Argo CD 를 통합해 두 과정의 강점을 각각 살리는 방법을 다룸 | 조정(reconciliation) 응답 시간, Webhook, Tekton Pipelines 연동, Tekton Triggers |
| 13 | Operationalizing Argo CD | 모니터링, 알림, 고가용성, 확장성을 다루며 Argo CD 를 운영 단계에 올리는 방법을 안내함 | Monitoring(Prometheus 스택), Notifications(Mattermost 연동), High Availability, Scaling Up, Sharding |
| 14 | Future Considerations | 지금과 앞으로 Argo CD 구현을 최대한 활용하는 데 필요한 맥락과 자료를 제공함 | GitOps 의 진화(DRY·매개변수화·저장소 수·디렉터리 구조·Rendered Manifests 패턴), 워크플로 모범 사례(관심사 분리·병합 전략), 커뮤니티(Slack·GitHub), 다음 단계(Progressive Delivery·GitOps Promotions) |



## 작성된 정독 노트

> 편을 작성하는 대로 채우며, 아직 쓰지 않은 편은 상태만 "작성 예정"으로 둡니다. 제목 칸은 장 제목을 옮긴 가제입니다.

| 편 | 제목 | 상태 | 보충 재료 |
|----|------|------|----------|
| 01-01 | [Argo CD 가 푸는 문제 — GitOps 원칙과 Argo 생태계](./01-01.Argo%20CD%20%EA%B0%80%20%ED%91%B8%EB%8A%94%20%EB%AC%B8%EC%A0%9C%20%E2%80%94%20GitOps%20%EC%9B%90%EC%B9%99%EA%B3%BC%20Argo%20%EC%83%9D%ED%83%9C%EA%B3%84.md) | 작성 완료 | [ArgoCD와 GitOps 기초](../../argocd/01-01.ArgoCD%EC%99%80%20GitOps%20%EA%B8%B0%EC%B4%88.md), [ArgoCD와 GitOps (kubernetes/11-03)](../../kubernetes/11_devtools/11-03.ArgoCD%EC%99%80%20GitOps.md) |
| 02-01 | Installing Argo CD (2장 전체, 가제) | 작성 예정 | [ArgoCD 설치와 아키텍처](../../argocd/01-02.ArgoCD%20%EC%84%A4%EC%B9%98%EC%99%80%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) |
| 03-01 | Interacting with Argo CD (3장 전체, 가제) | 작성 예정 | [ArgoCD 접근과 선언적 설정](../../argocd/01-03.ArgoCD%20%EC%A0%91%EA%B7%BC%EA%B3%BC%20%EC%84%A0%EC%96%B8%EC%A0%81%20%EC%84%A4%EC%A0%95.md) |
| 04-01 | Managing Applications (4장 전체, 가제) | 작성 예정 | [Application과 배포 대상 관리](../../argocd/02-01.Application%EA%B3%BC%20%EB%B0%B0%ED%8F%AC%20%EB%8C%80%EC%83%81%20%EA%B4%80%EB%A6%AC.md) |
| 05-01 | Synchronizing Applications (5장 전체, 가제) | 작성 예정 | [Sync 전략과 배포 순서 제어](../../argocd/02-02.Sync%20%EC%A0%84%EB%9E%B5%EA%B3%BC%20%EB%B0%B0%ED%8F%AC%20%EC%88%9C%EC%84%9C%20%EC%A0%9C%EC%96%B4.md) |
| 06-01 · 06-02 | Authentication and Authorization (6장, 가제, 두 편 후보) | 작성 예정 | [인증·인가와 AppProject](../../argocd/03-01.%EC%9D%B8%EC%A6%9D%C2%B7%EC%9D%B8%EA%B0%80%EC%99%80%20AppProject.md) |
| 07-01 | Cluster Management (7장 전체, 가제) | 작성 예정 | [멀티클러스터와 멀티테넌시](../../argocd/03-02.%EB%A9%80%ED%8B%B0%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EC%99%80%20%EB%A9%80%ED%8B%B0%ED%85%8C%EB%84%8C%EC%8B%9C.md) (8장과 나눠 씀) |
| 08-01 | Multi-Tenancy (8장 전체, 가제) | 작성 예정 | [멀티클러스터와 멀티테넌시](../../argocd/03-02.%EB%A9%80%ED%8B%B0%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EC%99%80%20%EB%A9%80%ED%8B%B0%ED%85%8C%EB%84%8C%EC%8B%9C.md) (7장과 나눠 씀) |
| 09-01 · 09-02 | Security (9장, 가제, 두 편 후보) | 작성 예정 | [보안 운영](../../argocd/03-03.%EB%B3%B4%EC%95%88%20%EC%9A%B4%EC%98%81.md) |
| 10-01 | Applications at Scale (10장 전체, 가제) | 작성 예정 | [App of Apps와 ApplicationSet](../../argocd/02-03.App%20of%20Apps%EC%99%80%20ApplicationSet.md), [대규모 운영과 Progressive Sync](../../argocd/05-02.%EB%8C%80%EA%B7%9C%EB%AA%A8%20%EC%9A%B4%EC%98%81%EA%B3%BC%20Progressive%20Sync.md), [ArgoCD App-of-Apps 패턴](../../../99_ETC/2026-04-19_ArgoCD%20App-of-Apps%20%ED%8C%A8%ED%84%B4.md) |
| 11-01 | Extending Argo CD (11장 전체, 가제) | 작성 예정 | [ArgoCD 확장과 플러그인](../../argocd/04-01.ArgoCD%20%ED%99%95%EC%9E%A5%EA%B3%BC%20%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8.md) |
| 12-01 | Integrating CI with Argo CD (12장 전체, 가제) | 작성 예정 | [CI 연동과 Image Updater](../../argocd/04-02.CI%20%EC%97%B0%EB%8F%99%EA%B3%BC%20Image%20Updater.md), [마이크로서비스 CI/CD 파이프라인 통합](../../argocd/04-04.%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%EC%84%9C%EB%B9%84%EC%8A%A4%20CI_CD%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%ED%86%B5%ED%95%A9.md) |
| 13-01 | Operationalizing Argo CD (13장 전체, 가제) | 작성 예정 | [모니터링·알림·HA 운영](../../argocd/05-01.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%C2%B7%EC%95%8C%EB%A6%BC%C2%B7HA%20%EC%9A%B4%EC%98%81.md) |
| 14-01 | Future Considerations (14장 전체, 가제) | 작성 예정 | [GitOps 성숙도와 미래 고려사항](../../argocd/05-03.GitOps%20%EC%84%B1%EC%88%99%EB%8F%84%EC%99%80%20%EB%AF%B8%EB%9E%98%20%EA%B3%A0%EB%A0%A4%EC%82%AC%ED%95%AD.md) |

각 옛 노트의 [`deepdive/`](../../argocd/deepdive/) 점검·실습 파일은 같은 장의 연습 문제 재료입니다.

### 편 나누기 계획

한 편은 원문 4,000~5,000단어를 기준으로 합니다. 경계는 그 근처의 원문 절 경계에 맞춥니다(`learning-method` 스킬의 정독 노트 세션 규약). 장별 단어 수는 `pdftotext -layout` 추출본을 `wc -w` 로 쟀으므로 코드 블록과 표가 들어 있습니다.

| 장 | 단어 수 | 계획 |
|----|-------:|------|
| 서문 | 2,543 | 별도 편을 두지 않습니다. 대상 독자·준비물 같은 사실은 이 README 에 적었습니다 |
| 1 | 2,960 | 한 편 |
| 2 | 4,367 | 한 편 |
| 3 | 3,509 | 한 편 |
| 4 | 3,489 | 한 편 |
| 5 | 4,619 | 한 편 |
| 6 | 8,372 | 두 편 후보. SSO using Dex 절이 시작되는 지점에서 나눕니다. 앞 약 5,060단어(admin·로컬 사용자·인증 토큰·SSO 개요·Keycloak 실습), 뒤 약 3,310단어(Dex·직접 OIDC·CLI SSO·RBAC). 주제로 나누려면 Role-Based Access Control 절 앞에서 끊을 수 있지만 앞 약 6,500단어, 뒤 약 1,870단어로 기웁니다 |
| 7 | 4,612 | 한 편 |
| 8 | 2,576 | 한 편 |
| 9 | 8,266 | 두 편 후보. SSH-Based Authentication 절이 시작되는 지점에서 나눕니다. 앞 약 4,320단어(서버 TLS·저장소 TLS 인증서·HTTPS 인증), 뒤 약 3,940단어(SSH 인증·자격 증명 템플릿·서명 검증·Sync Impersonation) |
| 10 | 4,069 | 한 편 |
| 11 | 5,801 | 한 편. 기준보다 길어서 Customizing Plugin Execution 절 뒤 User Interface Customization 절 앞(약 4,190단어 지점)이 둘로 나눌 후보 지점입니다 |
| 12 | 5,100 | 한 편 |
| 13 | 5,331 | 한 편 |
| 14 | 4,885 | 한 편 |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 1/14 장. 정독 노트 1편 |
| 난이도 레벨 | 미정 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 02-01 (2장 Installing Argo CD, 작성됨·검증 중) |
| 최근 검증 결과 | 01-01 `verify-gate.sh --type=learning --style=jondae` 실패 항목 합계 0. 적대적 검증 지적 11건 반영, agy 2차 검토 지적 없음 (2026-11-06) |
| 원문 정오 누적 | 0 |
| 버전 차이 기록 | 0 |
| 복습 회차 | 0 |



## 번호 체계와 작성 규약

> 파일명은 `NN-MM.제목.md`이고, 버전에 따라 바뀌는 값은 Argo CD 버전과 함께 적습니다.

`NN`은 책의 장 번호이고 `MM`은 그 장을 여러 편으로 나눌 때의 편 순번입니다. 정밀 도식은 `_assets/`에 SVG로 두고, 흐름·관계 중 자동 배치가 나은 것은 Mermaid로 본문에 직접 그립니다.

Argo CD 는 버전마다 CRD 필드와 기능 상태가 바뀝니다. 그래서 노트에는 버전에 따라 바뀌는 값을 Argo CD 버전과 함께 적습니다. 대상은 Argo CD 버전, CRD 필드, 설치 매니페스트 주소, Image Updater 와 ApplicationSet 의 기능 상태입니다. 이 값들은 현재 공식 문서([argo-cd.readthedocs.io stable](https://argo-cd.readthedocs.io/en/stable/))와 대조합니다. 원문과 현재 값이 다르면 노트에는 현재 값만 출처와 함께 적고, 바뀐 항목은 학습 상태 표의 버전 차이 기록에만 셉니다.

노트 끝 순서는 `## 연습 문제` → `## 정답 (자답 후 펼치기)` → `## 참고 자료` 입니다. 연습 문제 재료는 옛 노트의 `deepdive/` 파일에서 가져옵니다.



## 관련 문서

- [『CKS Study Guide』 정독본](../cks-study-guide/README.md) — 같은 `book/` 영역, 클러스터 하드닝 절차의 짝이자 9장 보안과 층이 다른 비교 대상
- [『Kubernetes: Up and Running』 정독본](../kubernetes-up-and-running/README.md) — 오브젝트와 운영 관점의 짝, Application 이 배포하는 대상의 기초
- [옛 argocd/ 노트](../../argocd/README.md) — 이 책을 바탕으로 쓴 옛 노트 16편, 장별 노트의 보충 재료
- [DevOps 로드맵](../../../roadmap/devops-roadmap.md) — 5단계 GitOps·6단계 점진 배포에서 이 주제가 놓인 자리
- [08_cloud MOC](../../README.md) — 상위 카테고리 경계

[^author]: 저자 소개는 서점 목록 페이지(https://www.schweitzer-online.de/en/buch/Block/Argo-CD-Up-Running/9781098142001/A71915297/, 2026-11-06 조회)에 실린 소개문을 따릅니다. Andrew Block 은 Helm 의 핵심 메인테이너이자 『Managing Kubernetes Resources Using Helm』 등 클라우드 네이티브 책을 쓴 저자이고, Christian Hernandez 는 OpenGitOps 프로젝트 메인테이너이자 Argo Project 구성원입니다. 서문의 감사의 말도 두 사람이 Argo 프로젝트와 GitOps 커뮤니티에서 오래 활동했다고 밝힙니다.

[^bib]: 서지 확인 결과입니다. ISBN 978-1-098-14200-1 은 서문 저작권 줄의 attribution 예시에서 끝자리까지 읽었고, 서점 목록 페이지(위 `source` 의 URL)와 일치합니다. 출판일은 그 서점 페이지에 2025-07-01 로 나오지만 다른 서점 목록에는 2025-07-22 로 적힌 곳도 있어 하루로 단정하지 않고 2025년으로만 씁니다. 출판사 O'Reilly 의 제품 페이지는 접근이 막혀(HTTP 403) 직접 읽지 못했으므로 판 표기는 확인 안 됨으로 둡니다.
