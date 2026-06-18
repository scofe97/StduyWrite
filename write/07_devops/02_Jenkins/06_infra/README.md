---
title: Jenkins 인프라 계획·배포·통합·확장·AI활용·CI설계·CI구현·CD학습 MOC
tags: [moc, jenkins, infra, planning, capacity, well-architected, iac, terraform, jcasc, helm, integration, github, sonarqube, artifactory, scaling, azure-vm-agents, ai, llm, chatgpt, ci-design, docker-registry, jenkinsfile, multibranch, blue-ocean, cd, gitops, argocd, k6, jfrog, xray, security, monitoring, metrics, prometheus]
status: draft
related:
  - ../README.md
  - ../01_core/README.md
  - ../03_agent/README.md
  - ../05_operations/README.md
updated: 2026-06-10
---

# Jenkins 인프라 계획·배포·통합·확장·AI활용·CI설계·CI구현·CD 학습 MOC

---

> Jenkins를 "어떻게 쓰는가"가 아니라 "어떻게 계획하고 배포하고, 외부 CI 도구와 통합하고, 확장하고, 하나의 CI 파이프라인으로 설계해 구현하고, GitOps로 프로덕션까지 배포하는가"를 다루는 묶음입니다. 본 묶음을 끝내면 controller 사양을 근거 있게 산정하고, 5가지 배포 형태를 Well-Architected 6 pillars로 평가하며, Terraform·JCasC·Helm으로 Jenkins를 코드로 재현 가능하게 배포하고, GitHub·SonarQube·Artifactory를 동일한 4단계로 연결하며, VM·K8s 동적 Agent로 수평 확장하고, LLM으로 파이프라인 초안을 짜되 반드시 검증하며, 이 모든 조각을 스테이지 순서가 있는 하나의 CI 파이프라인으로 설계하고, 동작하는 Jenkinsfile로 구현해 Multibranch·Blue Ocean으로 실행·시각화하며, Jenkins와 Argo CD의 역할분담으로 GitOps CD를 설계해 staging→production까지 자동 배포하는 흐름을 한 번에 설명할 수 있습니다.

## 왜 한 폴더로 묶었는가

01_core~05_operations가 "Jenkins를 어떻게 쓰는가"(파이프라인·Agent·API·내구성)에 집중한다면, 06_infra는 그 앞단인 "Jenkins 자체를 어떻게 세우는가"를 다룹니다. 용량 산정·배포 형태 선택·IaC 배포는 코드를 작성하기 전 인프라 설계 단계의 결정이고, 한 번 굳으면 바꾸기 어렵습니다. 세 주제는 결국 *처음 한 번을 제대로 세운다*는 같은 목적을 가집니다 — 용량 산정이 "얼마나 큰 서버가 필요한가"에, 배포 평가가 "어디에 어떤 방식으로 올릴까"에, IaC가 "그 결정을 어떻게 코드로 재현할까"에 답합니다. 한 폴더에 두면 "Jenkins를 진지하게 배포하려면 무엇을 먼저 정해야 하는가"의 답이 한 페이지에 잡힙니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 계획·배포 | 01-00 | [점검 — 핵심 질문과 답 (계획·배포)](01-00.점검.핵심%20질문과%20답%20%28계획%C2%B7배포%29.md) | 계획·배포 그룹 자가 점검 |
| 01 계획·배포 | 01-01 | [Jenkins 서버 용량 산정과 시스템 요구사항](01-01.Jenkins%20서버%20용량%20산정과%20시스템%20요구사항.md) | controller 자원 소비, CPU·RAM·디스크 추정식, 포트, JVM 튜닝 |
| 01 계획·배포 | 01-02 | [배포 시나리오와 Well-Architected 평가](01-02.배포%20시나리오와%20Well-Architected%20평가.md) | serverless·container·VM·bare metal, 6 pillars 평가, use-case 매핑 |
| 01 계획·배포 | 01-03 | [IaC로 Jenkins 배포 — Terraform·JCasC·Helm](01-03.IaC로%20Jenkins%20배포%20%E2%80%94%20Terraform%C2%B7JCasC%C2%B7Helm.md) | 재현성, JCasC 3종 파일, Terraform 흐름, K8s vs VM 선택 |
| 02 외부도구 통합 | 02-00 | [점검 — 핵심 질문과 답 (통합)](02-00.점검.핵심%20질문과%20답%20%28통합%29.md) | 외부도구 통합 그룹 자가 점검 |
| 02 외부도구 통합 | 02-01 | [GitHub 연동 — 플러그인·PAT·웹훅](02-01.GitHub%20연동%20%E2%80%94%20플러그인%C2%B7PAT%C2%B7웹훅.md) | GitHub 플러그인, PAT 스코프(admin:repo_hook·repo), 크레덴셜 2종, Test Connection |
| 02 외부도구 통합 | 02-02 | [SonarQube 연동 — 정적분석 게이트](02-02.SonarQube%20연동%20%E2%80%94%20정적분석%20게이트.md) | SonarQube Helm 배포, Scanner 플러그인, analysis token, Quality Gate, gradle 직접 호출 |
| 02 외부도구 통합 | 02-03 | [Artifactory 연동 — 아티팩트 저장소](02-03.Artifactory%20연동%20%E2%80%94%20아티팩트%20저장소.md) | Artifactory Helm 배포(OSS), user·permission, JFrog 플러그인 설정 |
| 02 외부도구 통합 | 02-04 | [외부 도구 통합 4단계 비교](02-04.외부%20도구%20통합%204단계%20비교.md) | 공통 4단계, 도구별 토큰 경로·크레덴셜 타입 차이, 전역 설정이 마지막인 이유 |
| 03 확장 | 03-00 | [점검 — 핵심 질문과 답 (확장)](03-00.점검.핵심%20질문과%20답%20%28확장%29.md) | 확장 그룹 자가 점검 |
| 03 확장 | 03-01 | [클라우드 VM 동적 Agent — Azure VM Agents 플러그인](03-01.클라우드%20VM%20동적%20Agent%20%E2%80%94%20Azure%20VM%20Agents%20플러그인.md) | VM vs K8s on-demand, service principal 인증, retention 3전략, 이미지 캐싱 |
| 04 AI 활용 | 04-00 | [점검 — 핵심 질문과 답 (AI 활용)](04-00.점검.핵심%20질문과%20답%20%28AI%20활용%29.md) | AI 활용 그룹 자가 점검 |
| 04 AI 활용 | 04-01 | [AI로 파이프라인 초안 짜기 — Describe·Run·Troubleshoot·Refine](04-01.AI로%20파이프라인%20초안%20짜기%20%E2%80%94%20Describe%C2%B7Run%C2%B7Troubleshoot%C2%B7Refine.md) | LLM 4단계 협업 루프, 요구사항 기술, 환경 추측 오류, AI 코드 검증 의무 |
| 05 CI·CD 파이프라인 | 05-00 | [점검 — 핵심 질문과 답 (CI·CD)](05-00.점검.핵심%20질문과%20답%20%28CI%C2%B7CD%29.md) | CI·CD 파이프라인 그룹 자가 점검 |
| 05 CI·CD 파이프라인 | 05-01 | [CI 파이프라인 전체 설계 — 스테이지 순서·Docker 레지스트리·인증](05-01.CI%20파이프라인%20전체%20설계%20%E2%80%94%20스테이지%20순서%C2%B7Docker%20레지스트리%C2%B7인증.md) | 7스테이지 순서·이유, webhook 트리거, Artifactory Docker 레지스트리, Kaniko 인증 Secret, Kaniko vs docker build |
| 05 CI·CD 파이프라인 | 05-02 | [첫 CI Jenkinsfile 구현 — 완성 코드·Multibranch·Blue Ocean](05-02.첫%20CI%20Jenkinsfile%20구현%20%E2%80%94%20완성%20코드%C2%B7Multibranch%C2%B7Blue%20Ocean.md) | 멀티컨테이너 Pod·container() 전환, 완성 Jenkinsfile, Multibranch·Blue Ocean, checkout ref 분기·docker DSL |
| 05 CI·CD 파이프라인 | 05-03 | [CD와 GitOps — 개념·브랜치 전략](05-03.CD와%20GitOps%20%E2%80%94%20개념%C2%B7브랜치%20전략.md) | CD vs Delivery, master-only CD·universal CD 전략, GitOps self-healing, JCasC GitOps와 구분 |
| 05 CI·CD 파이프라인 | 05-04 | [Argo CD로 CD 설계 — Jenkins 역할분담·staging→prod](05-04.Argo%20CD로%20CD%20설계%20%E2%80%94%20Jenkins%20역할분담%C2%B7staging%E2%86%92prod.md) | Jenkins·Argo CD 역할분담, 앱 Helm chart 환경분리, Application·auto-sync, staging→k6→prod |
| 05 CI·CD 파이프라인 | 05-05 | [첫 CD Jenkinsfile 구현 — values 갱신·Argo CD 헬스체크·k6 게이트](05-05.첫%20CD%20Jenkinsfile%20구현%20%E2%80%94%20values%20갱신%C2%B7Argo%20CD%20헬스체크%C2%B7k6%20게이트.md) | git·alpine 컨테이너 추가, yq values 갱신 push, Argo CD API 헬스체크(sync vs health), k6 성능 게이트, disableConcurrentBuilds |
| 05 CI·CD 파이프라인 | 05-06 | [JFrog Xray로 CI 보안 게이트 — 취약점 스캔·xrayScan·SonarQube와 역할 구분](05-06.JFrog%20Xray로%20CI%20보안%20게이트%20%E2%80%94%20취약점%20스캔%C2%B7xrayScan%C2%B7SonarQube와%20역할%20구분.md) | 아티팩트 SCA(SonarQube와 대상 구분), Xray Helm 설치·join key·namespace 격리, xrayScan failBuild 게이트, Scans List·취약점 리포트 |
| 05 CI·CD 파이프라인 | 05-07 | [Jenkins 성능 모니터링 — 지표·수집 토폴로지·부하 실측](05-07.Jenkins%20성능%20모니터링%20%E2%80%94%20지표%C2%B7수집%20토폴로지%C2%B7부하%20실측.md) | Metrics·Prometheus 플러그인 분업, 지표 4그룹(큐·executor·빌드·vm), VM/K8s/혼합 수집 설계, controller JVM 본체론, 200건 부하 실측 |
| 06 Job 조직·운영 | 06-00 | [점검 — 핵심 질문과 답 (Job 조직·운영)](06-00.점검.핵심%20질문과%20답%20%28Job%20조직·운영%29.md) | Job 조직·운영 그룹 자가 점검 |
| 06 Job 조직·운영 | 06-01 | [Folder 플러그인 — namespace 격리·full name 식별·폴더 스코핑](06-01.Folder%20플러그인%20%E2%80%94%20namespace%20격리%C2%B7full%20name%20식별%C2%B7폴더%20스코핑.md) | 평면 namespace 이름 충돌, AbstractFolder(TopLevelItem+ItemGroup), full name 식별, 폴더 스코프 credential·RBAC·Library 책임 구분, Multibranch 상속 체인, API 경로 중첩 대가 |
| 06 Job 조직·운영 | 06-02 | [SSH로 VM 배포 — sshPut·sshCommand·인증 분기·parallel 타깃](06-02.SSH로%20VM%20배포%20%E2%80%94%20sshPut%C2%B7sshCommand%C2%B7인증%20분기%C2%B7parallel%20타깃.md) | ssh-steps 플러그인, remote 맵, sshPut/sshCommand, PASSWORD/PRIVATE_KEY 인증 분기, parallel 다중 타깃, 키 충돌 회피 |
| 06 Job 조직·운영 | 06-03 | [MinIO 아티팩트 레지스트리 — mc CLI·버전 핀·빌드 산출물 연계](06-03.MinIO%20아티팩트%20레지스트리%20%E2%80%94%20mc%20CLI%C2%B7버전%20핀%C2%B7빌드%20산출물%20연계.md) | S3 호환 오브젝트 스토리지, mc alias/cp, --version-id 버전 핀, 빌드→배포 산출물 전달, Artifactory와 대조 |
| 06 Job 조직·운영 | 06-04 | [인라인 Pipeline Script형 Job — config.xml 형상·CpsFlowDefinition·파라미터화](06-04.인라인%20Pipeline%20Script형%20Job%20%E2%80%94%20config.xml%20형상%C2%B7CpsFlowDefinition%C2%B7파라미터화.md) | flow-definition config.xml 해부, 인라인(CpsFlowDefinition) vs SCM(CpsScmFlowDefinition), sandbox, DeclarativeJobPropertyTracker, ParametersDefinitionProperty·params.* |

용량부터 보려면 01-01, 배포 형태 결정이 먼저면 01-02, 코드화 구현이 급하면 01-03부터 진입합니다. 계획·배포 세 편은 01-01(얼마나) → 01-02(어디에) → 01-03(어떻게 코드로) 순으로 이어집니다. 외부 도구 연동은 02-01~02-03을 도구별로 보고, 02-04 비교표로 공통 4단계를 정리합니다. 03-01은 03_agent의 K8s 동적 Agent와 짝을 이루는 VM 기반 동적 Agent 편으로, 수평 확장의 두 갈래를 비교합니다. 04-01은 LLM으로 파이프라인 초안을 짜는 방법론과 그 검증 의무를 다루며, 02-02·02-03의 플러그인 step과 이어집니다. 05-01은 02-01~02-03과 03_agent Kaniko를 한 순서로 잇는 CI 파이프라인 전체 설계도이고, 05-02는 그 설계를 동작하는 Jenkinsfile로 구현해 Multibranch·Blue Ocean으로 실행·시각화합니다. 05-03·05-04·05-05는 CI가 끝난 지점(이미지 push)에서 이어집니다. CD와 GitOps 개념(05-03), Jenkins·Argo CD 역할분담으로 staging→production까지 자동 배포하는 설계(05-04)에 더해, 05-05는 그 설계를 실제 Jenkinsfile 스테이지 코드(values 갱신·Argo CD 헬스체크·k6 게이트)로 구현합니다. 05-06은 02-03 Artifactory에 JFrog Xray를 붙여 빌드 아티팩트의 취약점을 스캔하는 CI 보안 게이트를 다루며, 02-02 SonarQube(소스 코드 SCA)와 검사 대상을 구분합니다. 05-07은 01-01 용량 산정의 후속 *측정* 편으로, 추정식을 실측 지표로 보정하는 모니터링 설계와 VM·K8s 혼합 토폴로지의 수집 지점, 200건 부하 실측 기록을 다룹니다. 06-01은 Job이 늘었을 때의 *조직화* 편으로, 평면 namespace의 이름 충돌을 Folder 플러그인의 full name 식별로 푸는 원리를 다룹니다. 05-02의 Multibranch가 사실 이 폴더 모델(AbstractFolder→ComputedFolder) 위에 올라간다는 점, 04_api·07_engine에서 외운 `/job/` 중첩 경로가 폴더 계층의 결과라는 점이 이 편에서 한데 묶입니다. 06-02~06-04는 실제 운영 파이프라인을 분석해 책 정석 밖의 패턴을 메운 묶음입니다. K8s가 아닌 VM에 SSH로 배포하는 흐름(06-02), 이미지가 아닌 산출물을 MinIO에 두고 빌드→배포로 넘기는 연계(06-03), 파이프라인을 SCM Jenkinsfile이 아니라 Job 설정에 인라인으로 박는 형태와 그 config.xml 형상·파라미터화(06-04)를 다룹니다. 06-02의 SSH 배포는 06-03의 MinIO 산출물 수령과 한 흐름이고, 06-04의 인라인·파라미터화는 05-02 §5의 checkout 분기·docker DSL 변형과 짝을 이룹니다.

## 환경과 버전

> 본 묶음 예제는 다음 조합 기준입니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Jenkins | LTS 2.4xx 이상 | JCasC, durability 표준 |
| Java | 11 | 책 기준 JVM 튜닝 예시 |
| Terraform | azurerm provider | 예시는 Azure, GCP·AWS도 대응 provider |
| Helm chart | jenkins/jenkins | K8s 배포용 공식 차트 |

> 용량 추정식·6 pillars 점수는 *Learning Continuous Integration with Jenkins 3e*가 제시하는 휴리스틱입니다. Jenkins 공식 보장이 아니므로 설계의 출발점으로만 삼고 실측으로 보정합니다.

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`../01_core/`](../01_core/README.md)의 Controller·Agent 역할 분리와 [`../03_agent/`](../03_agent/README.md)의 K8s 실행 환경을 알고 있습니다.
2. [`../02_security/`](../02_security/README.md)의 JCasC 기본 개념을 한 번이라도 본 적이 있습니다(01-03 진입 조건).
3. 클라우드 VM·컨테이너·Kubernetes의 차이를 개념 수준에서 구분할 수 있습니다.

위 항목 중 막히는 부분이 있으면 [`../01_core/`](../01_core/README.md), [`../03_agent/`](../03_agent/README.md)를 먼저 보고 돌아옵니다.

## 면접 대비 체크리스트

> 여섯 그룹을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. controller가 빌드를 직접 돌리지 않는데도 CPU·RAM 산정이 중요한 이유는? 책 추정식(요청÷250, agent×3)의 한계는?
2. controller가 쓰는 네 포트(8080·443·50000·22)는 각각 무엇이며, 50000이 막히면 어떤 증상이 납니까?
3. 5가지 배포 형태를 6 pillars로 평가하면 어디가 종합 최적이고, bare metal은 무엇을 포기합니까?
4. JCasC 배포 3종 파일(jenkins.yaml·plugins.txt·override.conf)의 역할과 처리 순서는? 순서를 어기면?
5. `terraform init·plan·apply`는 각각 무엇을 하며, K8s Helm 배포와 VM Terraform 배포를 가르는 기준은?
6. GitHub·SonarQube·Artifactory 통합의 공통 4단계는 무엇이며, "전역 설정"이 항상 마지막인 이유는?
7. secret text와 username&password 크레덴셜은 각각 언제 쓰며, GitHub가 둘 다 쓰는 이유는?
8. VM 동적 Agent와 K8s on-demand는 각각 어떤 워크로드에 유리하며, VM의 retention 3전략(Idle·Pool·Once)은 어떻게 다릅니까?
9. LLM으로 파이프라인을 짤 때 Describe→Run→Troubleshoot→Refine 중 가장 중요한 단계는? AI 생성 코드를 그대로 믿으면 안 되는 이유와 검증 원칙은?
10. CI 파이프라인 스테이지 순서(Clone→Test→SCA→Quality Gate→Build→Publish)에서 SCA·Gate가 Build 앞에 오는 이유는? Artifactory를 Docker 레지스트리로 쓸 때 package type과 Kaniko 인증 Secret의 namespace는?
11. 한 Pod 3컨테이너(node·sonar·kaniko)를 stage별 `container()`로 전환할 때 Kaniko에 `sleep 99d`를 두는 이유는? Multibranch Pipeline의 주 기능과 Blue Ocean의 역할은?
12. Continuous Deployment와 Continuous Delivery의 차이는? GitOps의 "단일 진실"·"self-healing"은 무엇이며, JCasC GitOps와 앱 배포 GitOps는 어떻게 다릅니까?
13. GitOps CD에서 Jenkins와 Argo CD는 각각 무엇을 맡고 누가 Git을 감시합니까? Argo CD가 감시하는 파일은? staging→production 승급 전 무엇을 확인합니까?
14. CD Jenkinsfile에서 `disableConcurrentBuilds()`를 main/master에만 두는 이유는? 앱의 sync 상태와 health 상태가 같지 않은 이유는? Argo CD health를 프로그래매틱으로 가져오는 방법은?
15. SonarQube와 JFrog Xray는 보안 스캔 대상이 어떻게 다릅니까? `xrayScan(failBuild: true)`는 CI에서 무엇을 보장하며, Xray를 스캔하려면 빌드를 어디에 등록해야 합니까?
16. 두 팀이 똑같이 `deploy`라는 Job을 만들 수 없는 이유는? Folder 플러그인은 full name으로 이걸 어떻게 풉니까? 폴더만 깔면 RBAC가 되는지, Multibranch Pipeline이 Folder와 무슨 관계인지 설명할 수 있습니까?
17. K8s가 아닌 VM에 배포할 때 `sshPut`·`sshCommand`는 각각 무엇을 하며, 비밀번호 인증과 키 인증은 코드에서 어떻게 갈립니까? `parallel` 브랜치 키를 일련번호로 두는 이유는?
18. 컨테이너 이미지는 Harbor에 두는데 VM 배포용 tar는 왜 MinIO에 둡니까? `mc cp --version-id`가 재현 가능한 배포에 중요한 이유는? MinIO와 Artifactory는 언제 어느 것을 씁니까?
19. 같은 파이프라인 코드가 인라인(`CpsFlowDefinition`)과 SCM(`CpsScmFlowDefinition`)으로 갈리는 지점과 운영 차이는? `<sandbox>true`는 무엇을 보장하며, 파라미터를 `error()`로 검증하는 이유는?

각 질문에 막히면 해당 절로 돌아갑니다.
