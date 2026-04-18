# Ch08. 탐구 질문 — 생성 패턴과 클라우드 네이티브

이 파일은 LEARN.md를 읽은 후 더 깊이 파고들 질문들을 담는다.
각 질문에 스스로 답해보고, 실제로 실습하거나 코드를 작성해보는 것이 목표다.

---

## Q1. Factory vs Builder 패턴 선택 기준은 무엇인가?

**탐구 방향**

Factory와 Builder는 둘 다 객체 생성을 캡슐화하지만 적합한 상황이 다르다.
Factory는 "무엇을 만들지"가 런타임에 결정될 때 적합하고,
Builder는 "어떻게 조립할지"의 선택지가 많을 때 적합하다.

- 파이프라인에서 단계(stage) 수가 고정되어 있다면 Factory로 충분할까, Builder가 필요할까?
- `PipelineFactory.create("prod")`와 `PipelineBuilder().add_lint().add_test().build()`가 반환하는 객체가 동일하다면, 두 패턴을 함께 쓰는 경우는 언제인가?
- 실제 Jenkins의 `pipeline {}` DSL, GitHub Actions의 `jobs:` 블록은 어느 패턴에 더 가까운가?

**실습 제안**

같은 prod 파이프라인을 Factory로 구현한 버전과 Builder로 구현한 버전을 모두 작성하고,
코드 라인 수와 변경 용이성을 비교해본다.

---

## Q2. AWS CodePipeline vs GitHub Actions 아키텍처 차이

**탐구 방향**

AWS CodePipeline은 AWS 생태계에 강하게 결합된 관리형 서비스이고,
GitHub Actions는 이벤트 기반의 범용 자동화 플랫폼이다.
이 차이는 설계 결정에 큰 영향을 미친다.

- CodePipeline은 단계(stage) 간 아티팩트를 S3를 통해 전달한다. GitHub Actions는 어떤 메커니즘을 사용하는가? (`actions/upload-artifact` vs S3의 트레이드오프는?)
- CodePipeline의 "수동 승인(Manual Approval)" 액션과 GitHub Actions의 `environment: production` + `required_reviewers`는 구현 방식이 어떻게 다른가?
- CodePipeline은 AWS EventBridge와 연동하여 다른 AWS 서비스를 트리거할 수 있다. GitHub Actions에서 동일한 이벤트 연동을 구현하려면 어떤 방법을 쓸 수 있을까?

**실습 제안**

동일한 "소스 → 빌드 → 스테이징 배포 → 수동 승인 → 프로덕션 배포" 파이프라인을
CodePipeline(Terraform)과 GitHub Actions 양쪽으로 구현하고 차이점을 정리한다.

---

## Q3. 멀티클라우드 CI/CD의 추상화 레이어 설계

**탐구 방향**

멀티클라우드 파이프라인의 핵심 도전은 "공통 인터페이스를 어디까지 추상화할 것인가"다.
너무 추상화하면 각 클라우드의 고유 기능을 활용하지 못하고,
너무 구체적으로 만들면 클라우드 교체 시 전면 재작성이 필요하다.

- `./scripts/deploy.sh aws prod`처럼 쉘 스크립트로 추상화하는 방식과,
  Terraform의 provider 추상화로 관리하는 방식의 장단점은 무엇인가?
- AWS IAM, GCP Workload Identity Federation, Azure Managed Identity는 모두 "파이프라인이 클라우드 리소스에 접근하는 방법"이다. 이 세 가지를 통일된 방식으로 관리할 수 있는가?
- Crossplane, Pulumi, Terraform CDK는 멀티클라우드 추상화에서 어떤 위치에 있는가?

**실습 제안**

`deploy.sh`를 AWS와 GCP 두 버전으로 작성하고, 공통 인터페이스(입력 파라미터, 종료 코드, 출력 형식)를 정의해본다.

---

## Q4. Pipeline Template의 버전 관리

**탐구 방향**

LEARN.md의 Prototype 패턴은 기본 템플릿을 복제하여 팀별로 커스터마이징한다.
그런데 기본 템플릿이 업데이트되면 이미 복제된 팀별 파이프라인은 어떻게 되는가?

- Git의 `rebase` 전략과 파이프라인 템플릿 업데이트를 어떻게 비유할 수 있는가?
- GitHub의 "Reusable Workflows"(`workflow_call`)는 Prototype 패턴과 Template Method 패턴 중 어느 쪽에 더 가까운가?
- 템플릿 v1을 사용하는 팀과 v2를 사용하는 팀이 공존할 때, 어떤 버저닝 전략(semver, sha pin, branch pin)이 적합한가?

**실습 제안**

GitHub Reusable Workflow를 작성하고, 두 개의 다른 리포지토리에서 `uses: my-org/shared-workflows/.github/workflows/build.yml@v1` 형태로 호출하는 예시를 만들어본다.

---

## Q5. Singleton 패턴의 공유 리소스 동시성 문제

**탐구 방향**

ECR 레지스트리나 S3 아티팩트 버킷은 Singleton처럼 공유된다.
여러 팀의 파이프라인이 동시에 같은 레지스트리에 접근할 때 문제가 발생할 수 있다.

- 두 파이프라인이 같은 Docker 이미지 태그(예: `app:latest`)를 동시에 푸시하면 어떻게 되는가? ECR의 `IMMUTABLE` 태그 설정이 이 문제를 어떻게 해결하는가?
- S3 아티팩트 버킷에 여러 파이프라인이 동시에 쓰기를 시도할 때 경쟁 조건이 발생하는가? S3의 일관성 모델(strong read-after-write consistency)은 이를 어떻게 보장하는가?
- Terraform의 `state lock`(DynamoDB 기반)은 인프라 수준의 Singleton 잠금이다. 파이프라인 수준에서 유사한 잠금이 필요한 시나리오는 무엇인가?

**실습 제안**

같은 ECR 레지스트리에 두 개의 GitHub Actions 워크플로우가 동시에 푸시하는 실험을 구성하고, 태그 충돌 시 어떤 오류가 발생하는지 관찰한다.

---

## Q6. 클라우드 네이티브 CI/CD의 비용 최적화

**탐구 방향**

클라우드 CI/CD는 사용량 기반 과금이라 파이프라인 설계가 곧 비용 설계다.
AWS CodeBuild는 빌드 분당 과금이고, GitHub Actions는 분당 과금(셀프 호스팅은 무료)이다.

- LEARN.md의 Terraform 코드에서 `build_timeout = 20`과 `compute_type = "BUILD_GENERAL1_SMALL"`은 비용과 속도의 트레이드오프다. 어떤 기준으로 이 값을 정해야 하는가?
- 멀티클라우드 matrix 워크플로우에서 `fail-fast: false`는 비용을 증가시킨다. `fail-fast: true`로 설정하면 어떤 경우에 비용을 절감할 수 있고, 어떤 경우에 오히려 재실행 비용이 증가하는가?
- Docker layer caching, S3 캐시, GitHub Actions cache action을 활용한 빌드 시간 단축 전략을 비교하면? 캐시 적중률이 낮을 때의 오버헤드는 얼마나 되는가?
- Spot 인스턴스(AWS) 또는 Preemptible VM(GCP)을 CI 워커로 사용할 때 주의해야 할 점은 무엇인가?

**실습 제안**

동일한 프로젝트의 빌드를 캐시 없음, S3 캐시, GitHub Actions 캐시 세 가지 방식으로 실행하고, 평균 빌드 시간과 월 예상 비용을 계산해본다.

---

*참고*: 각 질문의 답은 `references/` 디렉토리에 별도 파일로 정리할 수 있다.
실습 결과는 `practice/` 디렉토리에 코드와 함께 기록한다.
