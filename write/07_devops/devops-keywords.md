---
title: DevOps 개발 키워드
tags: [keywords, devops, ci-cd, jenkins, gitops, argocd, helm, kustomize, iac, terraform]
status: draft
source:
  - ../07_devops/README.md
related:
  - ../README.md
  - ../08_cloud/k8s-keywords.md
  - ../06_observability/observability-keywords.md
  - ../10_AI/ai-keywords.md
  - ../09_spring/spring-keywords.md
updated: 2026-11-03
---

# DevOps 개발 키워드
---

> DevOps 개발 키워드 표. 문서를 쓸 때 참고합니다.



## 1단계 · 전달 모델

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 배포 단위 · 서버 배포와 로컬의 한계 | 필수 | [앱 배포 방법](../07_devops/book/fdsd_fundamentals-devops/01-01.How%20to%20Deploy%20Your%20App.md) | Fundamentals of DevOps and Software Delivery 1장 |
| 버전 관리 · 변경 추적 · Git | 필수 | [코드 버전 관리와 빌드](../07_devops/book/fdsd_fundamentals-devops/04-01.How%20to%20Version%20Build%20and%20Test%20Your%20Code.md) | Fundamentals of DevOps and Software Delivery 4장 · DevOps Tools for Java Developers 2장 |
| 브랜치 전략 · trunk-based development · 짧은 브랜치 수명 | 필수 | [CD와 GitOps](../07_devops/02_Jenkins/06_infra/05-03.CD%EC%99%80%20GitOps%20%E2%80%94%20%EA%B0%9C%EB%85%90%C2%B7%EB%B8%8C%EB%9E%9C%EC%B9%98%20%EC%A0%84%EB%9E%B5.md) | Software Engineering at Google 16장 |
| 다른 저장소 코드 끌어오기 — submodule 과 subtree 의 차이 | 선택 |  |  |
| 커밋 옮기기 — cherry-pick 이 diff 를 적용하는 원리와 충돌 | 선택 |  |  |
| 지속적 전달(CD) vs 지속적 배포 · 빌드 사이클 5단계 | 필수 | [CI/CD 기초 패턴](../07_devops/book/cicd_cicd-patterns/01-01.Foundations%20of%20CICD%20Design%20Patterns.md) | Software Engineering at Google 24장 |
| 배포 모델 — Push 모델 vs Pull 모델(GitOps) | 필수 | [CI/CD 기초 패턴](../07_devops/book/cicd_cicd-patterns/01-01.Foundations%20of%20CICD%20Design%20Patterns.md) | CI/CD Design Patterns 1장 |
| 배포 환경 분리 — dev · stage · prod 다중 환경 격리 | 추천 | [다중 환경과 분할](../07_devops/book/fdsd_fundamentals-devops/06-01.How%20to%20Work%20with%20Multiple%20Teams%20and%20Environments.md) | Fundamentals of DevOps and Software Delivery 6장 |
| DORA 4대 지표 — 배포 빈도 · 리드 타임 · 변경 실패율 · MTTR | 추천 | [DORA와 비즈니스 정렬](../07_devops/book/cicd_cicd-patterns/04-01.Business%20Outcome%20Alignment%20with%20CICD.md) | CI/CD Design Patterns 4장 |
| 추상화의 진화 — 플랫폼 엔지니어링과 IDP | 선택 | [DevOps의 미래](../07_devops/book/fdsd_fundamentals-devops/11-01.The%20Future%20of%20DevOps%20and%20Software%20Delivery.md) | Fundamentals of DevOps and Software Delivery 11장 |



## 2단계 · CI 파이프라인

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| CI 파이프라인 원칙 · 빠른 피드백 루프 | 필수 | [Jenkins 제어 범위](../07_devops/02_Jenkins/01_core/01-01.Jenkins%EA%B0%80%20%EC%A0%9C%EC%96%B4%ED%95%98%EB%8A%94%20%EA%B2%83.md) · [CI/CD 설정](../07_devops/book/fdsd_fundamentals-devops/05-01.How%20to%20Set%20Up%20CI%20CD.md) | Learning Continuous Integration with Jenkins 1장 · Software Engineering at Google 23장 |
| 빌드 요청에서 실행까지 — 트리거 · 큐 · 익스큐터 배정 | 필수 | [Queue 상태 전이와 Executor 로 가는 길](../07_devops/docs/jenkins/02-02.Queue%20%EC%83%81%ED%83%9C%20%EC%A0%84%EC%9D%B4%EC%99%80%20Executor%20%EB%A1%9C%20%EA%B0%80%EB%8A%94%20%EA%B8%B8.md) | Learning Continuous Integration with Jenkins 2장 |
| 코드로 파이프라인 정의하기 — Scripted vs Declarative | 필수 | [파이프라인 정의](../07_devops/02_Jenkins/01_core/02-01.%EC%BD%94%EB%93%9C%EB%A1%9C%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EC%A0%95%EC%9D%98%ED%95%98%EA%B8%B0.md) · [PaC 유형](../07_devops/book/cicd_cicd-patterns/02-01.Types%20of%20CICD%20Design%20Patterns%20and%20Components.md) | Learning Continuous Integration with Jenkins 6·8장 |
| Declarative Pipeline 핵심 구조 — pipeline · agent · stages · steps · post | 필수 | [Declarative Pipeline 핵심 구조](../07_devops/02_Jenkins/01_core/02-02.Declarative%20Pipeline%20%ED%95%B5%EC%8B%AC%20%EA%B5%AC%EC%A1%B0.md) | Learning Continuous Integration with Jenkins 9장 |
| 파이프라인 패턴 — 병렬 실행 · 조건부 실행(when) · 환경변수 | 필수 | [Pipeline 패턴](../07_devops/02_Jenkins/01_core/02-03.Pipeline%20%ED%8C%A8%ED%84%B4.md) · [구조 패턴](../07_devops/book/cicd_cicd-patterns/05-01.Exploring%20Structural%20CICD%20Design%20Patterns.md) | Learning Continuous Integration with Jenkins 9장 |
| 실패 대응과 셸 실행 위생 — retry · timeout · sh step 위생 | 추천 | [실패 대응과 파이프라인 원칙](../07_devops/02_Jenkins/01_core/02-04.%EC%8B%A4%ED%8C%A8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EC%9B%90%EC%B9%99.md) · [sh step 실행 위생](../07_devops/02_Jenkins/01_core/02-05.sh%20step%20%EC%85%B8%20%EC%8B%A4%ED%96%89%20%EC%9C%84%EC%83%9D.md) | Software Engineering at Google 18장 |
| 실행환경으로서의 Agent — 컨트롤러와 에이전트 분리 | 필수 | [실행환경 Agent](../07_devops/02_Jenkins/03_agent/01-01.%EC%8B%A4%ED%96%89%ED%99%98%EA%B2%BD%EC%9C%BC%EB%A1%9C%EC%84%9C%EC%9D%98%20Agent.md) | Learning Continuous Integration with Jenkins 5장 |
| Docker with Pipeline — 컨테이너 기반 빌드 격리 | 필수 | [Docker with Pipeline](../07_devops/02_Jenkins/03_agent/01-02.Docker%20with%20Pipeline.md) | DevOps Tools for Java Developers 5장 |
| Kubernetes Jenkins — 동적 Pod 에이전트 프로비저닝 | 추천 | [K8s Jenkins 구축](../07_devops/02_Jenkins/03_agent/02-01.Kubernetes%20Jenkins%20%EA%B5%AC%EC%B6%95.md) · [K8s Jenkins 운영](../07_devops/02_Jenkins/03_agent/02-02.Kubernetes%20Jenkins%20%EC%9A%B4%EC%98%81.md) |  |
| GitHub Actions 와 runner 종류 — hosted · self-hosted · ephemeral | 선택 | [CI/CD 설정](../07_devops/book/fdsd_fundamentals-devops/05-01.How%20to%20Set%20Up%20CI%20CD.md) | Fundamentals of DevOps and Software Delivery 5장 |
| Pipeline 내구성과 재기동 — CpsFlowExecution 영속화 | 추천 | [Pipeline 내구성과 재기동](../07_devops/02_Jenkins/05_operations/01-01.Pipeline%20%EB%82%B4%EA%B5%AC%EC%84%B1%EA%B3%BC%20%EC%9E%AC%EA%B8%B0%EB%8F%99.md) | Learning Continuous Integration with Jenkins 2장 |
| 공유 라이브러리(Shared Library) — vars 와 src 로 파이프라인 재사용 | 추천 | [공유 라이브러리](../07_devops/02_Jenkins/05_operations/02-01.%EA%B3%B5%EC%9C%A0%20%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC.md) · [공유 라이브러리 실전](../07_devops/02_Jenkins/05_operations/02-01a.%EA%B3%B5%EC%9C%A0%20%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC%20%EC%8B%A4%EC%A0%84%20%ED%8C%A8%ED%84%B4.md) | Learning Continuous Integration with Jenkins 12장 |
| Multibranch Pipeline — branch-source 기반 PR 자동 빌드 | 추천 | [CI 파이프라인 전체 설계](../07_devops/02_Jenkins/06_infra/05-01.CI%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EC%A0%84%EC%B2%B4%20%EC%84%A4%EA%B3%84%20%E2%80%94%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%20%EC%88%9C%EC%84%9C%C2%B7Docker%20%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%C2%B7%EC%9D%B8%EC%A6%9D.md) · [첫 CI Jenkinsfile 구현](../07_devops/02_Jenkins/06_infra/05-02.%EC%B2%AB%20CI%20Jenkinsfile%20%EA%B5%AC%ED%98%84%20%E2%80%94%20%EC%99%84%EC%84%B1%20%EC%BD%94%EB%93%9C%C2%B7Multibranch%C2%B7Blue%20Ocean.md) | Learning Continuous Integration with Jenkins 12장 |
| 머지 게이트 — branch protection · required status checks 로 실패한 PR 병합 차단 | 필수 |  |  |
| 로컬 검사와 비밀정보 탐지 — pre-commit hook · Gitleaks · CI 재검사 | 추천 |  | [Gitleaks](https://github.com/gitleaks/gitleaks) |
| 정적 분석과 결함 탐지 — 버그 · 취약점 · 코드 스멜 | 필수 | [정적 분석이 푸는 결함](../07_devops/docs/sonarqube/01-01.%EC%A0%95%EC%A0%81%20%EB%B6%84%EC%84%9D%EC%9D%B4%20%ED%91%B8%EB%8A%94%20%EA%B2%B0%ED%95%A8.md) | Software Engineering at Google 20장 |
| Clean as You Code — 신규 코드 중심 품질 관리 | 추천 | [Clean as You Code](../07_devops/docs/sonarqube/01-03.Clean%20as%20You%20Code%EC%99%80%20MQR.md) |  |
| SonarQube Quality Gate — 임계치 판정과 빌드 게이트 | 필수 | [Quality Gate](../07_devops/docs/sonarqube/02-04.Quality%20Gate.md) · [Jenkins 연계](../07_devops/docs/sonarqube/04-01.Jenkins%20%EC%97%B0%EA%B3%84.md) | CI/CD Design Patterns 7장 |
| 클러스터 안 CI 도구 — Jenkins · SonarQube · Harbor | 선택 | [Jenkins on K8s](../08_cloud/kubernetes/11_devtools/11-01.Jenkins%20on%20K8s.md) · [Harbor](../08_cloud/kubernetes/11_devtools/11-04.Harbor.md) |  |
| 파이프라인 행위·생성 디자인 패턴 — Observer · Strategy · Builder | 선택 | [행위 디자인 패턴](../07_devops/book/cicd_cicd-patterns/07-01.Understanding%20Behavioral%20Design%20Patterns%20for%20CICD.md) · [생성 디자인 패턴](../07_devops/book/cicd_cicd-patterns/09-01.Applying%20Creational%20CICD%20Design%20Patterns.md) | CI/CD Design Patterns 7·9장 |
| Jenkins REST API — 빌드 트리거 · 큐 및 실행기 원격 제어 | 선택 | [Jenkins API](../07_devops/02_Jenkins/04_api/README.md) |  |
| Jenkins 내부 엔진 — Stapler 라우팅 · Queue 스케줄링 | 선택 | [Jenkins 엔진](../07_devops/02_Jenkins/07_engine/README.md) |  |



## 3단계 · 산출물

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 컨테이너 실행과 점검 — `docker run` · `logs` · `exec` · `inspect` · 포트 · 볼륨 · 네트워크 | 필수 |  | DevOps Tools for Java Developers 3장 |
| Docker Compose — 여러 컨테이너를 한 파일로 띄우는 로컬 환경 | 추천 |  | [Compose 공식 문서](https://docs.docker.com/compose/) |
| 빌드 도구 선택과 컨테이너화 — Gradle · Maven · npm | 필수 | [빌드 도구 비교와 선택](../07_devops/02_Jenkins/03_agent/01-03.%EB%B9%8C%EB%93%9C%20%EB%8F%84%EA%B5%AC%20%EB%B9%84%EA%B5%90%EC%99%80%20%EC%84%A0%ED%83%9D.md) | DevOps Tools for Java Developers 6장 |
| 컨테이너 이미지 빌드 — multi-stage · BuildKit · Kaniko | 필수 | [컨테이너 이미지 빌드](../07_devops/02_Jenkins/03_agent/01-04.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%93%9C.md) | Container Security 6장 · DevOps Tools for Java Developers 3장 |
| 빌드 캐시 두 종류 — 의존성 캐시와 Docker 레이어 캐시 | 추천 | [컨테이너 이미지 빌드](../07_devops/02_Jenkins/03_agent/01-04.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%93%9C.md) |  |
| tag 와 digest — 태그 가변성 한계와 sha256 불변 참조 | 필수 | [컨테이너 이미지 빌드](../07_devops/02_Jenkins/03_agent/01-04.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%93%9C.md) | Container Security 6장 |
| Build Once, Deploy Many — 같은 digest 를 staging 에서 prod 로 승격 | 필수 |  |  |
| 아티팩트 관리 기초 — 바이너리 격리 · hosted · proxy · group | 필수 | [아티팩트 관리 기초](../07_devops/03_Nexus/01-01.%EC%95%84%ED%8B%B0%ED%8C%A9%ED%8A%B8%20%EA%B4%80%EB%A6%AC%EC%9D%98%20%EA%B8%B0%EC%B4%88.md) · [리포지토리 포맷](../07_devops/03_Nexus/02-01.%EB%A6%AC%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC%20%ED%8F%AC%EB%A7%B7%EA%B3%BC%20%EA%B5%AC%EC%84%B1.md) | DevOps Tools for Java Developers 6장 |
| 사설 Docker 레지스트리 운영 — Nexus Docker Registry | 추천 | [Docker Registry Nexus](../07_devops/03_Nexus/04-02.Docker%20Registry%EB%A1%9C%EC%84%9C%EC%9D%98%20Nexus.md) |  |
| 클라우드 네이티브 레지스트리 — Harbor 프로젝트 격리와 복제 | 추천 | [Harbor](../08_cloud/kubernetes/11_devtools/11-04.Harbor.md) |  |
| 엔터프라이즈 산출물 관리 — Artifactory 와 build-info 추적 | 선택 | [Artifactory 연동](../07_devops/02_Jenkins/06_infra/02-03.Artifactory%20%EC%97%B0%EB%8F%99%20%E2%80%94%20%EC%95%84%ED%8B%B0%ED%8C%A9%ED%8A%B8%20%EC%A0%80%EC%9E%A5%EC%86%8C.md) | DevOps Tools for Java Developers 6장 |
| 객체 스토리지 산출물 보관 — MinIO 아티팩트 레지스트리 | 선택 | [MinIO 아티팩트 레지스트리](../07_devops/02_Jenkins/06_infra/06-03.MinIO%20%EC%95%84%ED%8B%B0%ED%8C%A9%ED%8A%B8%20%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%E2%80%94%20mc%20CLI%C2%B7%EB%B2%84%EC%A0%84%20%ED%95%80%C2%B7%EB%B9%8C%EB%93%9C%20%EC%82%B0%EC%B6%9C%EB%AC%BC%20%EC%97%B0%EA%B3%84.md) |  |



## 4단계 · 패키징

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| Helm 차트 구조 · Chart.yaml · values.yaml · 템플릿 렌더링 | 필수 | [Helm 기초](../08_cloud/docs/helm/01-01.Helm%20%EA%B8%B0%EC%B4%88.md) | [Helm 공식 문서](https://helm.sh/docs/) |
| Helm 릴리스 생애주기 · 롤백 · 의존성 관리 · 라이프사이클 훅 | 추천 | [Helm 고급](../08_cloud/docs/helm/01-02.Helm%20%EA%B3%A0%EA%B8%89.md) | [Helm 공식 문서](https://helm.sh/docs/) |
| Helm 값 검증 — `required` · `fail` 로 렌더링 단계에서 실패시키기 | 추천 | | [Helm 차트 팁](https://helm.sh/docs/howto/charts_tips_and_tricks/) |
| Helm 설정 변경 시 파드 롤링 — Deployment 의 `checksum/config` annotation | 추천 | | Kubernetes Best Practices 4장 · [Helm 차트 팁](https://helm.sh/docs/howto/charts_tips_and_tricks/) |
| Helm `helm.sh/resource-policy: keep` — 삭제·롤백에서 리소스 남기기 | 선택 | [Helm 고급](../08_cloud/docs/helm/01-02.Helm%20%EA%B3%A0%EA%B8%89.md) | [Helm 차트 팁](https://helm.sh/docs/howto/charts_tips_and_tricks/) |
| Helm `.Files.Get` — 차트 안 파일 읽기 | 선택 | [Helm 고급](../08_cloud/docs/helm/01-02.Helm%20%EA%B3%A0%EA%B8%89.md) | [Accessing Files](https://helm.sh/docs/chart_template_guide/accessing_files/) |
| `helm upgrade --reset-then-reuse-values` · `--reuse-values` 와의 갈림 | 추천 | [Helm 기초](../08_cloud/docs/helm/01-01.Helm%20%EA%B8%B0%EC%B4%88.md) | [helm upgrade](https://helm.sh/docs/helm/helm_upgrade/) |
| Helm 렌더 결과 테스트 — `helm template` + 셸·단위 테스트로 RBAC·매니페스트 고정 · helm-unittest | 추천 | [Helm 기초](../08_cloud/docs/helm/01-01.Helm%20%EA%B8%B0%EC%B4%88.md) | [helm template](https://helm.sh/docs/helm/helm_template/) · [helm-unittest](https://github.com/helm-unittest/helm-unittest) |
| Kustomize 오버레이 · base 와 overlays · 리소스 패치 | 필수 | [Kustomize](../08_cloud/docs/kustomize/01-01.Kustomize.md) | [Kustomize 공식 문서](https://kubectl.docs.kubernetes.io/) |
| Helm · Kustomize | 추천 | [Helm 기초](../08_cloud/docs/helm/01-01.Helm%20%EA%B8%B0%EC%B4%88.md) ~ [Kustomize](../08_cloud/docs/kustomize/01-01.Kustomize.md) |  |



## 5단계 · GitOps

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| GitOps 원칙과 아키텍처 — 선언적 상태 · 풀 기반 동기화 루프 | 필수 | [ArgoCD와 GitOps 기초](../08_cloud/book/argocd-up-and-running/01-01.Argo%20CD%20%EA%B0%80%20%ED%91%B8%EB%8A%94%20%EB%AC%B8%EC%A0%9C%20%E2%80%94%20GitOps%20%EC%9B%90%EC%B9%99%EA%B3%BC%20Argo%20%EC%83%9D%ED%83%9C%EA%B3%84.md) · [ArgoCD 설치와 아키텍처](../08_cloud/book/argocd-up-and-running/02-01.Argo%20CD%20%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0%20%E2%80%94%20%EA%B5%AC%EC%84%B1%20%EC%9A%94%EC%86%8C%C2%B7%EC%84%A4%EC%B9%98%20%EC%9C%A0%ED%98%95%C2%B7%EB%A7%A4%EB%8B%88%ED%8E%98%EC%8A%A4%ED%8A%B8%EC%99%80%20Helm.md) | Kubernetes Best Practices 18장 |
| ArgoCD 접근과 선언적 설정 — GitOps 로 ArgoCD 자체 관리 | 추천 | [선언적 설정](../08_cloud/book/argocd-up-and-running/03-01.Argo%20CD%20%EC%99%80%20%EC%83%81%ED%98%B8%EC%9E%91%EC%9A%A9%ED%95%98%EA%B8%B0%20%E2%80%94%20UI%C2%B7CLI%C2%B7REST%20API%20%EC%99%80%20%EC%84%A0%EC%96%B8%EC%A0%81%20%EA%B5%AC%EC%84%B1.md) | [ArgoCD 공식 문서](https://argo-cd.readthedocs.io/) |
| Application CRD — 배포 소스(Git)와 목적지(Cluster) 관리 | 필수 | [Application 관리](../08_cloud/book/argocd-up-and-running/04-01.Application%20%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EC%86%8C%EC%8A%A4%C2%B7%EB%8C%80%EC%83%81%C2%B7Helm%C2%B7Kustomize%20%EC%99%80%20%EC%82%AD%EC%A0%9C%C2%B7finalizer.md) | DevOps Tools for Java Developers 8장 |
| Sync 전략과 순서 제어 — automated sync · self-heal · prune · Sync Waves | 필수 | [Sync 전략](../08_cloud/book/argocd-up-and-running/05-01.Application%20%EB%8F%99%EA%B8%B0%ED%99%94%20%E2%80%94%20%EC%9E%90%EB%8F%99%20%EB%8F%99%EA%B8%B0%ED%99%94%C2%B7Sync%20Option%C2%B7Hook%C2%B7Sync%20Wave%20%EC%99%80%20%EC%B0%A8%EC%9D%B4%20%EB%AC%B4%EC%8B%9C.md) | Kubernetes Best Practices 18장 |
| GitOps · ArgoCD · App of Apps · ApplicationSet | 추천 | [ArgoCD와 GitOps](../08_cloud/kubernetes/11_devtools/11-03.ArgoCD%EC%99%80%20GitOps.md) · [ArgoCD 노트](../08_cloud/book/argocd-up-and-running/README.md) | Kubernetes Best Practices 18장 |
| 대규모 배포 패턴 — App of Apps 패턴 · ApplicationSet 생성기 | 추천 | [App of Apps와 ApplicationSet](../08_cloud/book/argocd-up-and-running/10-01.Application%20%EC%97%AC%EB%9F%BF%EC%9D%84%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%E2%80%94%20%ED%97%AC%EC%8A%A4%20%EC%B2%B4%ED%81%AC%C2%B7App-of-Apps%20sync%20wave%C2%B7Progressive%20Sync.md) · [App of Apps와 멀티테넌시](../07_devops/book/aic_ai-infra-claude/07-02.App%20of%20Apps%EC%99%80%20%EB%A9%80%ED%8B%B0%ED%85%8C%EB%84%8C%EC%8B%9C.md) | Kubernetes Best Practices 18장 |
| 멀티테넌시와 권한 격리 — AppProject · 리소스 화이트리스트 | 추천 | [SSO 연결과 RBAC](../08_cloud/book/argocd-up-and-running/06-02.SSO%20%EC%97%B0%EA%B2%B0%EA%B3%BC%20RBAC%20%E2%80%94%20Dex%C2%B7%EC%A7%81%EC%A0%91%20OIDC%C2%B7%EC%97%AD%ED%95%A0%EA%B3%BC%20%EC%A0%95%EC%B1%85.md) · [멀티 테넌시](../08_cloud/book/argocd-up-and-running/08-01.%EB%A9%80%ED%8B%B0%20%ED%85%8C%EB%84%8C%EC%8B%9C%20%E2%80%94%20%EC%84%A4%EC%B9%98%20%EB%AA%A8%EB%93%9C%EC%99%80%20AppProject%C2%B7%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EC%97%AD%ED%95%A0.md) | [ArgoCD 공식 문서](https://argo-cd.readthedocs.io/) |
| 환경 승격 파이프라인 — 저장소 분리 · staging→prod 승격 | 필수 | [CD와 GitOps](../07_devops/02_Jenkins/06_infra/05-03.CD%EC%99%80%20GitOps%20%E2%80%94%20%EA%B0%9C%EB%85%90%C2%B7%EB%B8%8C%EB%9E%9C%EC%B9%98%20%EC%A0%84%EB%9E%B5.md) · [Argo CD로 CD 설계](../07_devops/02_Jenkins/06_infra/05-04.Argo%20CD%EB%A1%9C%20CD%20%EC%84%A4%EA%B3%84%20%E2%80%94%20Jenkins%20%EC%97%AD%ED%95%A0%EB%B6%84%EB%8B%B4%C2%B7staging%E2%86%92prod.md) | Learning Continuous Integration with Jenkins 10·11장 |
| CI-CD 파이프라인 통합 — values 갱신 · ArgoCD 헬스체크 게이트 | 추천 | [첫 CD Jenkinsfile 구현](../07_devops/02_Jenkins/06_infra/05-05.%EC%B2%AB%20CD%20Jenkinsfile%20%EA%B5%AC%ED%98%84%20%E2%80%94%20values%20%EA%B0%B1%EC%8B%A0%C2%B7Argo%20CD%20%ED%97%AC%EC%8A%A4%EC%B2%B4%ED%81%AC%C2%B7k6%20%EA%B2%8C%EC%9D%B4%ED%8A%B8.md) · [푸시 배포의 한계와 ArgoCD](../07_devops/book/aic_ai-infra-claude/03-01.%ED%91%B8%EC%8B%9C%20%EB%B0%B0%ED%8F%AC%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20ArgoCD%20GitOps%20%E2%80%94%20%EC%84%A4%EC%B9%98%C2%B7%EC%97%B0%EA%B2%B0%C2%B7%EB%A1%A4%EB%A7%81%C2%B7%EB%A1%A4%EB%B0%B1.md) | Learning Continuous Integration with Jenkins 11장 |
| Image Updater — 컨테이너 레지스트리 새 이미지 감지와 Git 자동 커밋 | 추천 | [Image Updater 설정과 write-back](../08_cloud/book/argocd-up-and-running/14-01.GitOps%20%EB%8B%A4%EC%9D%8C%20%EA%B1%B8%EC%9D%8C%20%E2%80%94%20%EC%A0%80%EC%9E%A5%EC%86%8C%20%EA%B5%AC%EC%A1%B0%C2%B7Rendered%20Manifests%C2%B7%EC%8A%B9%EA%B2%A9.md#image-updater-%EC%84%A4%EC%A0%95%EA%B3%BC-write-back) |  |



## 6단계 · 점진 배포

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| RollingUpdate 의 한계 — 트래픽 분기 불가와 버전 혼재 | 필수 | [Rolling Update의 한계](../07_devops/book/aic_ai-infra-claude/05-01.Rolling%20Update%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20Gateway%20API.md) | CI/CD Design Patterns 6장 |
| Blue-Green 배포 — Service / Gateway API 스위칭과 무중단 전환 | 필수 | [Blue-Green 무중단 전환](../07_devops/book/aic_ai-infra-claude/05-02.Blue-Green%20%EB%AC%B4%EC%A4%91%EB%8B%A8%20%EC%A0%84%ED%99%98%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B2%B0%EC%A0%95%20%EA%B8%B0%EB%A1%9D.md) | CI/CD Design Patterns 6·10장 · DevOps Tools for Java Developers 10장 |
| Canary 배포 — 소량 트래픽 점진 이동과 위험 최소화 | 필수 | [점진적 배포 Canary](../07_devops/book/aic_ai-infra-claude/06-02.%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%20Canary%EC%99%80%20claude-context.md) | CI/CD Design Patterns 6·10장 |
| 점진 배포 — canary · blue-green · Argo Rollouts · progressive delivery | 추천 |  | [Argo Rollouts](https://argo-rollouts.readthedocs.io/) |
| Argo Rollouts — Rollout CRD 와 트래픽 라우팅 연동 | 필수 | [Argo Rollouts와 배포 전략](../08_cloud/docs/argo-rollouts/01-01.Argo%20Rollouts%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5.md) | [Argo Rollouts](https://argo-rollouts.readthedocs.io/) |
| AnalysisTemplate — 관측 지표 기반 자동 분석과 실패 시 자동 롤백 | 추천 | [Argo Rollouts와 배포 전략](../08_cloud/docs/argo-rollouts/01-01.Argo%20Rollouts%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5.md) | [Argo Rollouts](https://argo-rollouts.readthedocs.io/) |
| Progressive Delivery — 피처 플래그 · Dark Launch · 비즈니스 분리 | 추천 | [배포 전략 패턴](../07_devops/book/cicd_cicd-patterns/06-01.Deployment%20Strategies%20for%20Structural%20Patterns.md) | DevOps Tools for Java Developers 10장 |
| 배포 후 검증 — smoke test · E2E(Playwright) · 배포 검증 게이트 | 필수 | [첫 CD Jenkinsfile 구현](../07_devops/02_Jenkins/06_infra/05-05.%EC%B2%AB%20CD%20Jenkinsfile%20%EA%B5%AC%ED%98%84%20%E2%80%94%20values%20%EA%B0%B1%EC%8B%A0%C2%B7Argo%20CD%20%ED%97%AC%EC%8A%A4%EC%B2%B4%ED%81%AC%C2%B7k6%20%EA%B2%8C%EC%9D%B4%ED%8A%B8.md) |  |
| Expand and Contract — DB 스키마 변경과 버전 공존 · dual write · backfill | 필수 |  |  |
| 롤백 메커니즘 구분 — Argo 동기화 · ReplicaSet · Canary 중단 · Git revert · DB 비가역성 | 추천 |  |  |
| 블루-그린 배포 · 카나리 배포 · 프로그레시브 딜리버리·롤아웃 · 트래픽 시프팅 | 선택 | [블루-그린 배포](../07_devops/book/aic_ai-infra-claude/05-02.Blue-Green%20%EB%AC%B4%EC%A4%91%EB%8B%A8%20%EC%A0%84%ED%99%98%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B2%B0%EC%A0%95%20%EA%B8%B0%EB%A1%9D.md) · [카나리 배포](../07_devops/book/aic_ai-infra-claude/06-02.%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%20Canary%EC%99%80%20claude-context.md) · [프로그레시브 딜리버리·롤아웃](../07_devops/book/aic_ai-infra-claude/06-02.%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%20Canary%EC%99%80%20claude-context.md) | |
| 카나리 분석 · 카나리 분석 자동화 · 트래픽 미러링 · 섀도 트래픽 · 트래픽 미러링 검증 · 다크 론치 · 섀도 론치 | 선택 | [트래픽 미러링](../08_cloud/book/istio-in-action/05-01.%EC%9C%84%ED%97%98%EC%97%90%20%EB%85%B8%EC%B6%9C%EB%90%98%EB%8A%94%20%ED%8A%B8%EB%9E%98%ED%94%BD%EC%9D%84%20%EC%A4%84%EC%97%AC%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) | |
| 피처 플래그 기반 롤아웃 · A/B 테스트 인프라 · 실험 플랫폼 | 선택 | [A/B 테스트 인프라](../08_cloud/book/kubernetes-in-action/15-03.rollout%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%E2%80%94%20pause%C2%B7faulty%C2%B7rollback%C2%B7%EC%A0%84%EB%9E%B5%205%EC%A2%85.md) | |
| 롤링 업데이트 | 선택 | [롤링 업데이트](../07_devops/book/aic_ai-infra-claude/03-01.%ED%91%B8%EC%8B%9C%20%EB%B0%B0%ED%8F%AC%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20ArgoCD%20GitOps%20%E2%80%94%20%EC%84%A4%EC%B9%98%C2%B7%EC%97%B0%EA%B2%B0%C2%B7%EB%A1%A4%EB%A7%81%C2%B7%EB%A1%A4%EB%B0%B1.md) | |



## 7단계 · 인프라를 코드로

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| IaC 와 Immutable Infrastructure — 고치지 않고 다시 만든다 | 추천 | [IaC 관리](../07_devops/book/fdsd_fundamentals-devops/02-01.How%20to%20Manage%20Your%20Infrastructure%20as%20Code.md) | Terraform Up and Running 1장 · Infrastructure as Code 11장 |
| Terraform state · module · 비밀 관리 | 추천 |  | Terraform Up and Running 3·4·6장 |
| IaC로 배포 파이프라인 프로비저닝 — Terraform · Helm · JCasC 연계 | 추천 | [IaC로 Jenkins 배포](../07_devops/02_Jenkins/06_infra/01-03.IaC%EB%A1%9C%20Jenkins%20%EB%B0%B0%ED%8F%AC%20%E2%80%94%20Terraform%C2%B7JCasC%C2%B7Helm.md) | Infrastructure as Code 1장 |
| 클러스터를 오브젝트로 선언 — Cluster API · Crossplane | 선택 |  | Production Kubernetes 2장 · [Cluster API](https://cluster-api.sigs.k8s.io/) |
| IaC 정책 검사 — Security as Code | 선택 |  | Policy as Code 11·12장 · Infrastructure as Code 21장 |



## 8단계 · 파이프라인 보안

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| Jenkins 인증과 인가 — Security Realm · Matrix / Role-Based 인가 | 필수 | [인증과 인가](../07_devops/02_Jenkins/02_security/01-01.%EC%9D%B8%EC%A6%9D%EA%B3%BC%20%EC%9D%B8%EA%B0%80%20%E2%80%94%20%EB%88%84%EA%B0%80%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%95%A0%20%EC%88%98%20%EC%9E%88%EB%8A%94%EA%B0%80.md) | Learning Continuous Integration with Jenkins 3장 |
| 시크릿 관리와 최소 권한 원칙 — Credentials 바인딩과 마스킹 | 필수 | [시크릿 관리와 최소 권한](../07_devops/02_Jenkins/02_security/01-02.%EC%8B%9C%ED%81%AC%EB%A6%BF%20%EA%B4%80%EB%A6%AC%EC%99%80%20%EC%B5%9C%EC%86%8C%20%EA%B6%8C%ED%95%9C%20%EC%9B%90%EC%B9%99.md) | Learning Continuous Integration with Jenkins 3장 · Fundamentals of DevOps and Software Delivery 8장 |
| CI 의 클라우드 접근 — OIDC 임시 자격 증명 · IAM Role Trust Policy · 최소 권한 | 필수 | [CI/CD 설정](../07_devops/book/fdsd_fundamentals-devops/05-01.How%20to%20Set%20Up%20CI%20CD.md) | Fundamentals of DevOps and Software Delivery 5장 |
| 설정을 코드로 — JCasC(Jenkins Configuration as Code) | 추천 | [설정을 코드로 JCasC](../07_devops/02_Jenkins/02_security/02-01.%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%BD%94%EB%93%9C%EB%A1%9C%20%E2%80%94%20JCasC.md) |  |
| JCasC 운영과 GitOps — jenkins.yaml 버전 관리와 자동 반영 | 추천 | [JCasC 운영과 GitOps](../07_devops/02_Jenkins/02_security/02-02.JCasC%20%EC%9A%B4%EC%98%81%EA%B3%BC%20GitOps.md) |  |
| JCasC 시크릿과 실전 패턴 — 환경변수 치환과 Vault 연동 | 추천 | [JCasC 시크릿과 실전](../07_devops/02_Jenkins/02_security/02-03.JCasC%20%EC%8B%9C%ED%81%AC%EB%A6%BF%EA%B3%BC%20%EC%8B%A4%EC%A0%84%20%ED%8C%A8%ED%84%B4.md) |  |
| 빌드 환경 격리와 권한 최소화 — Rootless 에이전트와 DinD 위험 회피 | 추천 | [VM Jenkins Docker 보안](../07_devops/02_Jenkins/03_agent/01-05.VM%20Jenkins%EC%97%90%EC%84%9C%EC%9D%98%20Docker%20%EB%B3%B4%EC%95%88%20%EB%AA%A8%EB%8D%B8.md) | DevOps Tools for Java Developers 7장 |
| 취약점 스캔의 원리 — CVE 와 심각도 · 취약점 DB 출처(OS 배포판 피드 · GitHub Advisory) · OS 패키지와 언어 라이브러리 두 층 | 필수 | [이미지 속 소프트웨어 취약점](../08_cloud/book/container-security/07-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%86%8D%20%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%E2%80%94%20CVE%EB%B6%80%ED%84%B0%20%EC%8A%A4%EC%BA%94%20%EC%9A%B4%EC%98%81%EA%B9%8C%EC%A7%80.md) | Container Security 7장 |
| 취약점 스캔 게이트 — JFrog Xray 의존성·이미지 CVE 차단 | 필수 | [Xray 보안 게이트](../07_devops/02_Jenkins/06_infra/05-06.JFrog%20Xray%EB%A1%9C%20CI%20%EB%B3%B4%EC%95%88%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%20%E2%80%94%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%EC%8A%A4%EC%BA%94%C2%B7xrayScan%C2%B7SonarQube%EC%99%80%20%EC%97%AD%ED%95%A0%20%EA%B5%AC%EB%B6%84.md) | Container Security 7장 · Policy as Code 14장 |
| Trivy 와 CI 게이트 — image · fs · repo 스캔 · `--severity` · `--exit-code` · `--ignore-unfixed` · `.trivyignore` | 추천 |  | [Trivy 공식 문서](https://trivy.dev/) |
| 스캔 결과 조치 — 설치 버전과 수정 버전 · 베이스 이미지 교체와 패키지 업그레이드 · 재빌드가 곧 패치 | 추천 | [이미지 속 소프트웨어 취약점](../08_cloud/book/container-security/07-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%86%8D%20%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%E2%80%94%20CVE%EB%B6%80%ED%84%B0%20%EC%8A%A4%EC%BA%94%20%EC%9A%B4%EC%98%81%EA%B9%8C%EC%A7%80.md) | Container Security 7장 |
| 스캐너 비교 — Trivy · Grype · Docker Scout 와 스캐너마다 결과가 다른 이유 | 선택 | [이미지 속 소프트웨어 취약점](../08_cloud/book/container-security/07-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%86%8D%20%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%E2%80%94%20CVE%EB%B6%80%ED%84%B0%20%EC%8A%A4%EC%BA%94%20%EC%9A%B4%EC%98%81%EA%B9%8C%EC%A7%80.md) | Container Security 7장 |
| 공급망 보안 — SBOM(Software Bill of Materials) 생성과 이미지 서명 | 추천 | [이미지 공급망 보안](../08_cloud/book/container-security/06-02.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md) | Policy as Code 14장 |
| Provenance 와 Attestation — 빌드 출처 증명(SLSA)과 배포 전 검증 | 추천 | [이미지 공급망 보안](../08_cloud/book/container-security/06-02.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md) | Container Security 6장 |
| 규제 산업 준수 파이프라인 — 감사 추적과 정책 준수 | 선택 | [규제 준수 파이프라인](../07_devops/book/cicd_cicd-patterns/08-01.Domain%20Driven%20Design%20Patterns%20for%20Regulated%20Sectors.md) | CI/CD Design Patterns 8장 |
| Shift-Left 보안 감사 — 파이프라인 평가와 성숙도 모델 | 추천 | [감사와 평가](../07_devops/book/cicd_cicd-patterns/11-01.Auditing%20and%20Assessment%20of%20Design%20Patterns.md) | CI/CD Design Patterns 11장 |
| CI/CD 안티패턴 방지 — 보안 우회 · 비밀 노출 · 수동 개입 제거 | 추천 | [안티패턴 탐색](../07_devops/book/cicd_cicd-patterns/13-01.Exploring%20Anti-Patterns%20for%20CICD%20Design%20Pattern%20Deployments.md) | CI/CD Design Patterns 13장 |
| 공급망 공격 · 의존성 혼란 · 타이포스쿼팅 · 의존성 피닝 · 패키지 서명 · 서명 검증 파이프라인 · SBOM 생성 | 선택 | [의존성 피닝](../07_devops/02_Jenkins/05_operations/02-01a.%EA%B3%B5%EC%9C%A0%20%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC%20%EC%8B%A4%EC%A0%84%20%ED%8C%A8%ED%84%B4.md) · [SBOM 생성](../08_cloud/book/container-security/07-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%86%8D%20%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%E2%80%94%20CVE%EB%B6%80%ED%84%B0%20%EC%8A%A4%EC%BA%94%20%EC%9A%B4%EC%98%81%EA%B9%8C%EC%A7%80.md) | |
| 의존성 취약점 스캔 · SAST · DAST · IAST | 선택 | [의존성 취약점 스캔](../07_devops/02_Jenkins/06_infra/05-06.JFrog%20Xray%EB%A1%9C%20CI%20%EB%B3%B4%EC%95%88%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%20%E2%80%94%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%EC%8A%A4%EC%BA%94%C2%B7xrayScan%C2%B7SonarQube%EC%99%80%20%EC%97%AD%ED%95%A0%20%EA%B5%AC%EB%B6%84.md) · [SAST](../07_devops/docs/sonarqube/06-02.Advanced%20Security%EC%99%80%20AI%20%EA%B8%B0%EB%8A%A5.md) | |
| RASP | 선택 | | |
| SCA | 선택 | [SCA](../07_devops/02_Jenkins/06_infra/05-06.JFrog%20Xray%EB%A1%9C%20CI%20%EB%B3%B4%EC%95%88%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%20%E2%80%94%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%EC%8A%A4%EC%BA%94%C2%B7xrayScan%C2%B7SonarQube%EC%99%80%20%EC%97%AD%ED%95%A0%20%EA%B5%AC%EB%B6%84.md) | |



## 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| 클러스터 오브젝트 · admission 정책 · 런타임 보안 | [Kubernetes 로드맵](../08_cloud/k8s-keywords.md) 6단계가 맡습니다 |
| Jenkins 메트릭 대시보드 · 관측 설정 코드화 | [관측 가능성 로드맵](../06_observability/observability-keywords.md) 7단계가 맡습니다 |
| GitAIOps — AI 와 함께 선언하고 배포하기 | [AI 로드맵](../10_AI/ai-keywords.md) 6단계가 맡습니다 |
| bootJar · Layered JAR 등 프레임워크 빌드 산출물 | [Spring 로드맵](../09_spring/spring-keywords.md) 9단계가 맡습니다 |
| cgroup · namespace 의 커널 격리 구현 | [OS 로드맵](../02_os/os-keywords.md) 3단계가 맡습니다 |
| Istio 및 서비스 메시 트래픽 관리 | [네트워크 로드맵](../02_os/network-keywords.md) 7단계가 맡습니다 |
