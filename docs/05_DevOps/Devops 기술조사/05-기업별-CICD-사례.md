# 기업별 CI/CD 및 DevOps 사례

> 작성일: 2025-01-14
> 목적: 주요 기업들의 CI/CD 파이프라인, GitOps 활용 사례 정리

---

## 1. Netflix

### 1.1 개요

| 항목 | 내용 |
|-----|------|
| **규모** | 300M+ 구독자, 190+ 국가 |
| **배포 빈도** | 하루 수천 번 |
| **아키텍처** | 마이크로서비스 |
| **클라우드** | AWS |

### 1.2 CI/CD 스택

```
┌─────────────────────────────────────────────────────────────────┐
│                    Netflix CI/CD 파이프라인                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │   Git   │ →  │ Jenkins │ →  │ Docker  │ →  │Spinnaker│     │
│  │  Push   │    │  Build  │    │  Image  │    │ Deploy  │     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│                                     │                          │
│                                     ▼                          │
│                              ┌───────────┐                     │
│                              │   Titus   │                     │
│                              │(Container │                     │
│                              │ Runtime)  │                     │
│                              └───────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 도구 | 역할 | 특징 |
|-----|------|------|
| **Jenkins** | CI (빌드/테스트) | Gradle과 통합 |
| **Spinnaker** | CD (배포) | 자체 개발, 오픈소스화 |
| **Titus** | 컨테이너 관리 | 자체 개발, AWS 통합 |
| **Chaos Monkey** | 복원력 테스트 | Simian Army 일부 |

### 1.3 배포 전략

- **Canary 배포**: 일부 트래픽만 새 버전으로 라우팅
- **Red/Black (Blue/Green)**: 전체 환경 전환
- **자동 롤백**: 메트릭 기반 이상 감지 시 자동 롤백

### 1.4 핵심 도구 상세

**Spinnaker 파이프라인 예시**:
```yaml
# 일반적인 Spinnaker 파이프라인 구조
stages:
  - name: Bake
    type: bake
    # AMI 또는 Docker 이미지 생성

  - name: Deploy to Test
    type: deploy
    cluster:
      strategy: redblack
      capacity:
        min: 2
        max: 4

  - name: Manual Judgment
    type: manualJudgment
    # QA 승인 대기

  - name: Deploy to Prod
    type: deploy
    cluster:
      strategy: redblack
      targetHealthyDeployPercentage: 100
```

---

## 2. Spotify

### 2.1 개요

| 항목 | 내용 |
|-----|------|
| **서비스** | 음악 스트리밍 |
| **아키텍처** | 마이크로서비스 |
| **개발 문화** | Squad 모델 |

### 2.2 주요 도구

| 도구 | 역할 | 상태 |
|-----|------|------|
| **Tingle** | 통합 CI/CD 시스템 | 자체 개발 |
| **Tugboat** | 배포 시스템 | Tingle과 연동 |
| **Backstage** | 개발자 포털 | 자체 개발, 오픈소스화 |

### 2.3 Backstage 소개

Spotify가 개발하고 오픈소스화한 개발자 포털:

```
┌─────────────────────────────────────────────────────────────────┐
│                       Backstage 구조                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Software Catalog                        │  │
│  │  - 모든 서비스, API, 리소스 등록                            │  │
│  │  - 소유자, 의존성, 문서 통합                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Templates  │  │  TechDocs   │  │    CI/CD Statistics     │ │
│  │ (서비스 생성)│  │ (문서 통합) │  │   (파이프라인 메트릭)   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 성과

- 새 서비스 셋업 시간: **14일 → 5분 미만**
- 200개 이상의 독립 Jenkins 머신을 Tingle로 통합
- 개발자가 End-to-End 책임 (DevOps 모델)

### 2.5 GitOps 활용

- 인프라 관리에 GitOps 적용
- Golden Path (Paved Path) 제공: 표준화된 도구 및 워크플로우

---

## 3. Google

### 3.1 개요

| 항목 | 내용 |
|-----|------|
| **코드베이스** | 20억+ 라인 (모노레포) |
| **개발자 수** | 수만 명 |
| **배포 철학** | SRE (Site Reliability Engineering) |

### 3.2 내부 도구

| 도구 | 역할 |
|-----|------|
| **Blaze/Bazel** | 빌드 시스템 |
| **Borg/Kubernetes** | 컨테이너 오케스트레이션 |
| **Spanner** | 글로벌 분산 데이터베이스 |

### 3.3 GKE 기반 권장 아키텍처

```yaml
# Google Cloud 권장 CI/CD 파이프라인
pipeline:
  source:
    - Cloud Source Repositories
    - GitHub / GitLab 연동

  build:
    - Cloud Build
    - Artifact Registry (이미지 저장)

  deploy:
    - Config Sync (GitOps)
    - ArgoCD / Flux

  infrastructure:
    - Terraform
    - Config Connector
```

### 3.4 핵심 원칙

1. **Environment-as-Code**: 선언적 배포 매니페스트
2. **이미지 재빌드 금지**: 한 번 빌드 → 여러 환경 배포
3. **CI 파이프라인 10분 이내**: Fast/Full 파이프라인 분리
4. **Policy-as-Code**: OPA 기반 정책 관리

---

## 4. Amazon/AWS

### 4.1 개요

| 항목 | 내용 |
|-----|------|
| **철학** | Two-Pizza Teams |
| **배포** | 독립적인 서비스 배포 |

### 4.2 AWS 내부 실천법

```
┌─────────────────────────────────────────────────────────────────┐
│                  Amazon 배포 철학                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  "You build it, you run it"                                    │
│                                                                 │
│  - 팀이 서비스의 전체 수명주기 책임                               │
│  - 독립적인 배포 파이프라인                                      │
│  - 자동화된 롤백                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 AWS CI/CD 서비스 스택

| 서비스 | 역할 | 대안 |
|-------|------|------|
| **CodeCommit** | 소스 저장소 | GitHub, GitLab |
| **CodeBuild** | 빌드 | Jenkins, GitHub Actions |
| **CodeDeploy** | 배포 | Spinnaker, ArgoCD |
| **CodePipeline** | 오케스트레이션 | Jenkins, GitLab CI |
| **ECR** | 컨테이너 레지스트리 | Docker Hub |
| **EKS** | Kubernetes | 자체 관리 K8s |

### 4.4 베스트 프랙티스

1. **환경별 계정 분리**: Dev, Staging, Prod 별도 AWS 계정
2. **IaC 필수**: Terraform, CloudFormation, CDK
3. **최소 권한 IAM**: 각 서비스별 최소 권한
4. **시크릿 관리**: Secrets Manager 사용

---

## 5. Microsoft

### 5.1 개요

| 항목 | 내용 |
|-----|------|
| **개발 방식** | Trunk-Based Development |
| **릴리스 주기** | 3주 스프린트 |

### 5.2 Azure DevOps 사용

```
┌─────────────────────────────────────────────────────────────────┐
│                Microsoft 개발 워크플로우                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Trunk-Based Development                                    │
│     - 단일 main 브랜치                                          │
│     - 짧은 수명의 피처 브랜치                                    │
│                                                                 │
│  2. Feature Flags                                              │
│     - 배포와 릴리스 분리                                         │
│     - LaunchDarkly 또는 자체 시스템                              │
│                                                                 │
│  3. Ring-Based Deployment                                       │
│     - Ring 0: 내부 팀                                           │
│     - Ring 1: 얼리 어답터                                       │
│     - Ring 2: 전체 사용자                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 핵심 전략

- **Feature Flags**: 기능 배포와 노출 분리
- **Ring Deployment**: 점진적 롤아웃
- **3주 스프린트**: 정기 릴리스 케이던스

---

## 6. 기업별 도구 요약

### 6.1 CI 도구

| 기업 | 도구 | 특징 |
|-----|------|------|
| Netflix | Jenkins | Gradle 통합 |
| Spotify | Tingle (자체) | 통합 CI/CD |
| Google | Cloud Build | GCP 네이티브 |
| Amazon | CodeBuild | AWS 네이티브 |
| Microsoft | Azure Pipelines | Azure 통합 |

### 6.2 CD 도구

| 기업 | 도구 | 배포 전략 |
|-----|------|----------|
| Netflix | Spinnaker | Canary, Red/Black |
| Spotify | Tugboat | - |
| Google | Config Sync | GitOps |
| Amazon | CodeDeploy | Rolling, Blue/Green |
| Microsoft | Azure Pipelines | Ring Deployment |

### 6.3 컨테이너 오케스트레이션

| 기업 | 도구 |
|-----|------|
| Netflix | Titus (자체) → EKS |
| Spotify | Kubernetes |
| Google | Kubernetes (창시자) |
| Amazon | ECS, EKS |
| Microsoft | AKS |

---

## 7. 도구 채택 트렌드 (2025)

### 7.1 CI 도구 시장 점유율

```
Jenkins         ████████████████████████████████ 54%
GitHub Actions  ██████████████████████████████   51%
GitLab CI       ██████████████████               상당수
CircleCI        █████████████                    -
Azure Pipelines ████████████                     -
```

### 7.2 GitOps 도구

| 도구 | 채택률 | 트렌드 |
|-----|-------|--------|
| ArgoCD | ~60% | 상승 |
| FluxCD | - | 하락 (Weaveworks 폐업) |
| Spinnaker | - | 유지 |

### 7.3 주요 트렌드

1. **GitOps 주류화**: ArgoCD가 사실상 표준
2. **Platform Engineering**: 내부 개발자 플랫폼(IDP) 구축
3. **AI/ML Ops**: AI 기반 파이프라인 최적화
4. **Security Shift Left**: 보안 스캔 초기 단계 통합
5. **Progressive Delivery**: Canary, Feature Flags 일반화

---

## 8. 교훈 및 적용 포인트

### 8.1 공통 패턴

| 패턴 | 설명 | 적용 기업 |
|-----|------|----------|
| **마이크로서비스** | 독립적 배포 단위 | 전체 |
| **컨테이너화** | Docker 기반 패키징 | 전체 |
| **자동화** | 수동 작업 최소화 | 전체 |
| **모니터링** | 배포 후 지속 관찰 | 전체 |
| **롤백 자동화** | 이상 감지 시 자동 복구 | Netflix, Amazon |

### 8.2 단계별 성숙도 모델

```
Level 1: 기본 CI/CD
├── Git 기반 버전 관리
├── 자동화된 빌드
└── 자동화된 테스트

Level 2: 지속적 배포
├── 자동화된 배포
├── 환경별 파이프라인
└── 기본 모니터링

Level 3: GitOps
├── 선언적 인프라
├── Git 기반 배포 트리거
└── 자동 동기화

Level 4: Progressive Delivery
├── Canary 배포
├── Feature Flags
├── 자동 롤백
└── 메트릭 기반 프로모션

Level 5: Platform Engineering
├── 내부 개발자 플랫폼
├── Self-Service 인프라
├── Golden Path 제공
└── 개발자 경험 최적화
```

---

## 9. 참고 자료

### Netflix
- [Netflix Tech Stack - CI/CD Pipeline (ByteByteGo)](https://bytebytego.com/guides/netflix-tech-stack-cicd-pipeline/)
- [How Netflix Became A Master of DevOps (Simform)](https://www.simform.com/blog/netflix-devops-case-study/)

### Spotify
- [How Spotify Manages Infrastructure with GitOps (The New Stack)](https://thenewstack.io/platformcon-how-spotify-manages-infrastructure-with-gitops/)
- [How Spotify Leverages Paved Paths (InfoQ)](https://www.infoq.com/news/2021/03/spotify-paved-paths/)
- [Spotify Developer Productivity (Spotify Engineering)](https://engineering.atspotify.com/2020/08/how-we-improved-developer-productivity-for-our-devops-teams)

### Google
- [Google GKE CI/CD Best Practices](https://cloud.google.com/kubernetes-engine/docs/concepts/best-practices-continuous-integration-delivery-kubernetes)
- [GitOps Best Practices (Google Cloud)](https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/concepts/gitops-best-practices)

### Microsoft
- [How Microsoft Develops with DevOps](https://learn.microsoft.com/en-us/devops/develop/how-microsoft-develops-devops)

### AWS
- [AWS CI/CD Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/cicd-best-practices.html)

### 시장 동향
- [The State of CI/CD in 2025 (JetBrains)](https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/)
- [GitOps in 2025 (CNCF)](https://www.cncf.io/blog/2025/06/09/gitops-in-2025-from-old-school-updates-to-the-modern-way/)
