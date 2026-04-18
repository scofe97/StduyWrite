# 06. CI/CD 연계 (Jenkins, GitLab)

Redpanda와 Jenkins, GitLab CI/CD 파이프라인 연계, Testcontainers 활용, GitOps, 자동화 배포

---

## 구성

### 1. CI/CD에서 Redpanda가 필요한 이유

#### 문제점

Kafka 애플리케이션을 테스트하려면 실제 브로커가 필요합니다. 그런데 CI 환경(Jenkins, GitLab Runner)에서 Kafka 클러스터를 관리하기가 어렵습니다. 외부 Kafka 클러스터에 의존하면 테스트 격리가 불가능하고 환경 간 충돌이 발생할 수 있습니다.

#### 해결 방안

Testcontainers와 Redpanda를 조합하면 테스트마다 독립적인 브로커를 생성할 수 있습니다. Redpanda는 JVM을 사용하지 않기 때문에 Kafka보다 컨테이너 시작 시간이 절반으로 줄어듭니다. CI 파이프라인에서 별도 설정 없이 동일한 테스트 코드를 실행할 수 있습니다.

---

### 2. Testcontainers + Redpanda (CI 핵심)

#### 의존성 추가

```xml
<!-- Maven -->
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>redpanda</artifactId>
    <version>1.19.7</version>
    <scope>test</scope>
</dependency>
```

```groovy
// Gradle
testImplementation 'org.testcontainers:redpanda:1.19.7'
```

#### 테스트 코드

```java
@SpringBootTest
@Testcontainers
class OrderServiceIntegrationTest {

    @Container
    static RedpandaContainer redpanda = new RedpandaContainer(
        "docker.redpanda.com/redpandadata/redpanda:v25.1.1"
    );

    @DynamicPropertySource
    static void kafkaProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.bootstrap-servers", redpanda::getBootstrapServers);
    }

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @Autowired
    private OrderService orderService;

    @Test
    void 주문_생성시_이벤트가_발행된다() {
        // Given
        OrderRequest request = new OrderRequest("item-1", 3);

        // When
        orderService.createOrder(request);

        // Then
        ConsumerRecords<String, String> records = KafkaTestUtils.getRecords(consumer);
        assertThat(records).hasSize(1);
        assertThat(records.iterator().next().value()).contains("item-1");
    }
}
```

`@Testcontainers` 어노테이션은 테스트 실행 시 자동으로 Redpanda 컨테이너를 시작합니다. `@Container`로 선언한 static 필드는 모든 테스트 메서드에서 공유되며, `@DynamicPropertySource`는 Spring Boot의 설정을 런타임에 주입하기 때문에 application.yml을 수정하지 않아도 됩니다.

#### Redpanda 설정 커스터마이징

```java
@Container
static RedpandaContainer redpanda = new RedpandaContainer(
    "docker.redpanda.com/redpandadata/redpanda:v25.1.1"
)
.withStartupTimeout(Duration.ofSeconds(60))
.withExposedPorts(9092, 8081, 8082);  // Schema Registry, Pandaproxy 포함
```

Schema Registry(8081)와 Pandaproxy(8082) 포트를 노출하면 Avro/Protobuf 스키마와 REST API를 활용한 테스트도 가능합니다. 시작 타임아웃을 늘리면 CI 환경의 느린 네트워크에서도 안정적으로 실행됩니다.

#### Testcontainers에서 rpk 실행

```java
@BeforeAll
static void setupTopics() throws Exception {
    redpanda.execInContainer("rpk", "topic", "create", "orders", "-p", "3");
    redpanda.execInContainer("rpk", "topic", "create", "orders.DLT", "-p", "3");

    ExecResult result = redpanda.execInContainer("rpk", "cluster", "info");
    System.out.println(result.getStdout());
}
```

Redpanda 컨테이너 내부의 `rpk` 명령어를 직접 실행할 수 있습니다. 테스트 시작 전에 토픽을 생성하거나 클러스터 상태를 확인하는 용도로 사용합니다. 프로덕션과 동일한 토픽 설정을 테스트에서 재현할 수 있습니다.

---

### 3. Jenkins Pipeline 통합

#### Jenkinsfile

```groovy
pipeline {
    agent {
        docker {
            image 'eclipse-temurin:21-jdk'
            args '-v /var/run/docker.sock:/var/run/docker.sock'  // Docker-in-Docker
        }
    }

    environment {
        TESTCONTAINERS_RYUK_DISABLED = 'false'
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh './gradlew build -x test'
            }
        }

        stage('Unit Tests') {
            steps {
                sh './gradlew test --tests "*Unit*"'
            }
        }

        stage('Integration Tests (Redpanda)') {
            steps {
                sh './gradlew test --tests "*Integration*"'
            }
            post {
                always {
                    junit 'build/test-results/**/*.xml'
                }
            }
        }

        stage('Topic Setup (Staging)') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                    rpk topic create orders -p 6 -r 3 \
                      --brokers staging-redpanda:9092 || true
                    rpk topic create orders.DLT -p 3 -r 3 \
                      --brokers staging-redpanda:9092 \
                      --config retention.ms=604800000 || true
                '''
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'helm upgrade --install my-app ./helm-chart -f values-prod.yaml'
            }
        }
    }

    post {
        failure {
            slackSend channel: '#ci-alerts', message: "Build FAILED: ${env.JOB_NAME}"
        }
    }
}
```

#### Jenkins에서 Docker-in-Docker 설정

Jenkins에서 Testcontainers를 사용하려면 Docker 소켓을 Jenkins 에이전트에 마운트해야 합니다.

**방법 1: Docker Socket 마운트**
```
args '-v /var/run/docker.sock:/var/run/docker.sock'
```
Jenkins 에이전트가 호스트의 Docker 데몬을 직접 사용합니다. 가장 간단하지만 보안상 주의가 필요합니다.

**방법 2: Docker-in-Docker (DinD) 사이드카**
```
services:
  - docker:dind
```
독립적인 Docker 데몬을 컨테이너로 실행합니다. 격리성이 높지만 설정이 복잡합니다.

**방법 3: Testcontainers Cloud (원격 Docker)**
```
TESTCONTAINERS_HOST_OVERRIDE=cloud-host
```
Testcontainers가 제공하는 클라우드 환경을 사용합니다. 로컬 Docker 설정이 필요 없지만 네트워크 지연이 발생할 수 있습니다.

---

### 4. GitLab CI/CD 통합

#### .gitlab-ci.yml

```yaml
stages:
  - build
  - test
  - deploy-staging
  - deploy-production

variables:
  GRADLE_OPTS: "-Dorg.gradle.daemon=false"
  DOCKER_HOST: tcp://docker:2376
  DOCKER_TLS_CERTDIR: "/certs"

# Testcontainers를 위한 Docker-in-Docker
services:
  - docker:24.0-dind

build:
  stage: build
  image: eclipse-temurin:21-jdk
  script:
    - ./gradlew build -x test
  artifacts:
    paths:
      - build/libs/*.jar
    expire_in: 1 hour

unit-test:
  stage: test
  image: eclipse-temurin:21-jdk
  script:
    - ./gradlew test --tests "*Unit*"
  artifacts:
    reports:
      junit: build/test-results/**/*.xml

integration-test:
  stage: test
  image: eclipse-temurin:21-jdk
  variables:
    TESTCONTAINERS_HOST_OVERRIDE: "docker"
    TESTCONTAINERS_RYUK_DISABLED: "true"  # GitLab DinD에서 권장
  script:
    - ./gradlew test --tests "*Integration*"
  artifacts:
    reports:
      junit: build/test-results/**/*.xml
  allow_failure: false

topic-setup-staging:
  stage: deploy-staging
  image: docker.redpanda.com/redpandadata/redpanda:v25.1.1
  only:
    - develop
  script:
    - rpk topic create orders -p 6 -r 3 --brokers $STAGING_BROKERS || true
    - rpk topic create orders.DLT -p 3 -r 3 --brokers $STAGING_BROKERS --config retention.ms=604800000 || true
    - rpk topic list --brokers $STAGING_BROKERS

deploy-production:
  stage: deploy-production
  image: bitnami/kubectl:latest
  only:
    - main
  when: manual
  script:
    - kubectl apply -f k8s/ --namespace=production
    - kubectl rollout status deployment/order-service --namespace=production
  environment:
    name: production
```

#### GitLab에서 Testcontainers 사용 시 주의사항

**1. Docker-in-Docker (DinD) 서비스 필수**
```yaml
services:
  - docker:24.0-dind
```
GitLab Runner가 Docker 컨테이너를 실행하려면 DinD 서비스가 필요합니다.

**2. TESTCONTAINERS_RYUK_DISABLED=true**
GitLab Runner의 DinD 환경에서 Ryuk가 컨테이너를 정리하지 못할 수 있습니다. Ryuk는 테스트 종료 후 컨테이너를 자동으로 삭제하는 도구인데, DinD 환경에서는 권한 문제로 동작하지 않을 수 있기 때문입니다.

**3. TESTCONTAINERS_HOST_OVERRIDE=docker**
DinD 서비스의 호스트명이 'docker'이므로 Testcontainers에게 명시적으로 알려야 합니다. 이렇게 하지 않으면 Testcontainers가 localhost를 사용하려고 시도하면서 실패합니다.

**4. 러너 타입에 따라 다름**
- **Shell Runner**: Docker 소켓 직접 접근 가능 (추가 설정 불필요)
- **Docker Runner**: DinD 서비스 필요
- **Kubernetes Runner**: DinD 사이드카 또는 Testcontainers Cloud

---

### 5. rpk를 활용한 토픽 자동화

#### 토픽 라이프사이클 자동화 스크립트

```bash
#!/bin/bash
# scripts/manage-topics.sh

BROKERS=${BROKERS:-"localhost:19092"}
ENV=${ENV:-"dev"}

# 환경별 설정
case $ENV in
  dev)
    PARTITIONS=3; REPLICAS=1; RETENTION=86400000  # 1일
    ;;
  staging)
    PARTITIONS=6; REPLICAS=3; RETENTION=259200000  # 3일
    ;;
  production)
    PARTITIONS=12; REPLICAS=3; RETENTION=604800000  # 7일
    ;;
esac

# 토픽 목록 (topics.txt)
TOPICS=(
  "orders"
  "payments"
  "inventory"
  "notifications"
)

# 토픽 생성
for topic in "${TOPICS[@]}"; do
  echo "Creating topic: $topic (env=$ENV)"
  rpk topic create "$topic" \
    -p $PARTITIONS -r $REPLICAS \
    --brokers $BROKERS \
    --config retention.ms=$RETENTION || true

  # DLT 토픽도 함께 생성
  rpk topic create "${topic}.DLT" \
    -p $PARTITIONS -r $REPLICAS \
    --brokers $BROKERS \
    --config retention.ms=604800000 || true  # DLT는 항상 7일
done

echo "All topics created for $ENV environment"
rpk topic list --brokers $BROKERS
```

환경별로 파티션 수, 레플리카 수, 리텐션을 다르게 설정합니다. 개발 환경은 리소스를 절약하기 위해 파티션 3개, 레플리카 1개로 가볍게 구성하고, 프로덕션은 성능과 가용성을 위해 파티션 12개, 레플리카 3개로 설정합니다. DLT(Dead Letter Topic)는 항상 7일 보관하여 실패한 메시지를 분석할 시간을 확보합니다.

---

### 6. GitOps + Redpanda Connect

#### Argo CD와 Redpanda Connect

**GitOps 워크플로우**
1. Git 저장소에 Redpanda Connect 파이프라인 YAML 저장
2. Argo CD가 Git 상태와 K8s 상태 비교
3. 차이가 있으면 자동으로 Sync (파이프라인 배포/업데이트)

**장점**
- 파이프라인 설정 변경이 Git 히스토리에 남습니다. 누가, 언제, 왜 변경했는지 추적할 수 있습니다.
- PR 리뷰를 통한 변경 관리가 가능합니다. 파이프라인 변경도 코드 리뷰를 거치게 됩니다.
- 롤백이 Git revert로 가능합니다. 문제가 발생하면 즉시 이전 상태로 되돌릴 수 있습니다.

#### Streams Mode (멀티 파이프라인)

```yaml
# ConfigMap으로 파이프라인 관리
apiVersion: v1
kind: ConfigMap
metadata:
  name: redpanda-connect-streams
data:
  orders-pipeline.yaml: |
    input:
      redpanda:
        addresses: ["redpanda:9092"]
        topics: ["orders"]
        consumer_group: "connect-orders"
    pipeline:
      processors:
        - mapping: |
            root = this
            root.processed_at = now()
    output:
      redpanda_common:
        topic: orders-processed

  payments-pipeline.yaml: |
    input:
      redpanda:
        addresses: ["redpanda:9092"]
        topics: ["payments"]
        consumer_group: "connect-payments"
    output:
      http_client:
        url: http://payment-gateway/webhook
        verb: POST
```

Streams 모드는 하나의 Redpanda Connect 배포에서 여러 파이프라인을 동적으로 로드합니다. ConfigMap이 변경되면 파이프라인이 자동으로 추가/수정/삭제됩니다. 각 파이프라인은 독립적으로 동작하며, 한 파이프라인에 문제가 생겨도 다른 파이프라인에 영향을 주지 않습니다.

---

### 7. Terraform + Ansible 자동화 배포

#### Redpanda 공식 자동화 도구

**github.com/redpanda-data/deployment-automation**

- **Terraform**: 인프라 프로비저닝 (AWS EC2, GCP VM)
- **Ansible**: Redpanda 설치 및 설정

**CI/CD 연계**
1. git push → Jenkins/GitLab 트리거
2. Terraform으로 VM 프로비저닝
3. Ansible로 Redpanda 설치
4. rpk로 토픽 생성
5. 헬스체크 후 완료

```bash
# 자동화 시작
git clone https://github.com/redpanda-data/deployment-automation.git
cd deployment-automation

# Terraform
terraform init
terraform plan -var="nodes=3"
terraform apply -auto-approve

# Ansible (멱등성 보장 → CI/CD에서 반복 실행 가능)
ansible-playbook --private-key=~/.ssh/id_rsa ansible/playbooks/provision-node.yml
```

Terraform은 클라우드 리소스를 선언적으로 관리하기 때문에 현재 상태와 원하는 상태를 비교하여 변경 사항만 적용합니다. Ansible은 멱등성을 보장하기 때문에 여러 번 실행해도 결과가 동일합니다. 이러한 특성 덕분에 CI/CD 파이프라인에서 안전하게 반복 실행할 수 있습니다.

---

### 8. Helm 기반 자동 배포 (K8s 환경)

```bash
# CI/CD에서 Helm 배포
helm repo add redpanda https://charts.redpanda.com/
helm repo update

# 설치 (최초)
helm install redpanda redpanda/redpanda \
  --namespace redpanda --create-namespace \
  -f values-prod.yaml

# 업그레이드 (설정 변경 시)
helm upgrade redpanda redpanda/redpanda \
  --namespace redpanda \
  -f values-prod.yaml

# 검증
kubectl exec -n redpanda redpanda-0 -- rpk cluster health
kubectl exec -n redpanda redpanda-0 -- rpk cluster info
```

Helm은 Kubernetes 애플리케이션 패키지 매니저입니다. 복잡한 Redpanda 클러스터 설정을 values.yaml 파일로 관리할 수 있습니다. `helm upgrade`는 무중단 배포를 지원하기 때문에 서비스 중단 없이 설정을 변경할 수 있습니다.

---

### 9. CI/CD 파이프라인 비교

| 항목 | Jenkins | GitLab CI | GitHub Actions |
|------|---------|-----------|----------------|
| 설정 파일 | Jenkinsfile | .gitlab-ci.yml | .github/workflows/*.yml |
| Docker 접근 | 소켓 마운트 | DinD 서비스 | 기본 제공 |
| Testcontainers | 소켓 마운트 필요 | DinD + 환경변수 | 기본 동작 |
| Helm 배포 | 플러그인 또는 CLI | kubectl/helm 이미지 | actions/helm |
| 비용 | 자체 호스팅 | 자체/SaaS | SaaS (무료 티어) |
| 시장 점유율 (2025) | ~47% | ~20% | ~33% |

Jenkins는 자체 호스팅이 기본이기 때문에 초기 설정이 복잡하지만 커스터마이징 자유도가 높습니다. GitLab CI는 Git 저장소와 통합되어 있어 별도 설정 없이 사용할 수 있습니다. GitHub Actions는 Marketplace의 다양한 액션을 활용할 수 있어 생산성이 높습니다.

---

### 10. 참고 자료

- [Redpanda TDD & CI Testing](https://www.redpanda.com/blog/test-driven-development-ci-testing-kafka)
- [Testcontainers Redpanda Module](https://java.testcontainers.org/modules/redpanda/)
- [Redpanda GitOps](https://www.redpanda.com/blog/operationalize-redpanda-connect-gitops)
- [Redpanda Deployment Automation](https://github.com/redpanda-data/deployment-automation)
- [Redpanda Connect Helm Chart](https://docs.redpanda.com/redpanda-connect/get-started/quickstarts/helm-chart/)
