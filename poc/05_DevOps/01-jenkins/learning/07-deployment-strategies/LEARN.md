# Ch07. Deployment Strategies

## 학습 목표
프로덕션 배포 전략(Blue-Green, Canary, Rolling Update)의 동작 원리와 트레이드오프를 이해하고, Jenkins 파이프라인에서 Kubernetes 배포와 자동 롤백을 구현하는 방법을 면접에서 설명할 수 있다.

**핵심 질문**: "프로덕션 배포 중 장애가 발생하면 어떻게 30초 안에 롤백하는가?"

---

## 1. 배포 전략 비교

배포 전략을 선택할 때 핵심은 "장애 시 얼마나 빠르게 이전 상태로 돌아갈 수 있는가"입니다. 모든 전략은 결국 **롤백 속도와 리소스 비용 사이의 트레이드오프**를 다룹니다.

### 1.1 Blue-Green 배포

Blue-Green 배포는 두 개의 동일한 프로덕션 환경을 운영하는 전략입니다. Blue는 현재 트래픽을 처리하는 환경이고, Green은 새 버전을 배포할 환경입니다. 새 버전을 Green에 배포하고, 스모크 테스트를 통과하면 로드밸런서(또는 라우터)가 트래픽을 Blue에서 Green으로 전환합니다. 문제가 발생하면 트래픽을 다시 Blue로 돌리기만 하면 됩니다.

이 전략이 강력한 이유는 **롤백이 배포의 역순이 아니라 단순한 스위칭**이기 때문입니다. 이전 버전을 다시 빌드하거나 배포할 필요 없이, 이미 동작 중인 Blue 환경으로 트래픽만 전환하면 됩니다. 그래서 롤백 시간이 수초에 불과합니다.

**단점은 인프라 비용입니다.** 항상 두 벌의 환경을 유지해야 하므로 서버 비용이 약 2배로 증가합니다. 또한 데이터베이스 마이그레이션이 복잡합니다. Blue와 Green이 같은 DB를 공유하는 경우, 스키마 변경이 양쪽 버전 모두와 호환되어야 하기 때문입니다. 이를 해결하기 위해 "확장 후 축소(Expand-Contract)" 마이그레이션 패턴을 사용합니다. 먼저 새 컬럼을 추가하고(확장), 양쪽 버전이 모두 새 스키마와 호환되는 것을 확인한 후, 이전 컬럼을 제거합니다(축소).

### 1.2 Canary 배포

Canary 배포는 새 버전을 전체 트래픽의 일부(보통 1~5%)에게만 먼저 노출하는 전략입니다. 이름은 탄광에서 유독가스를 감지하기 위해 카나리아 새를 먼저 보냈던 관행에서 유래했습니다. 소수의 사용자가 새 버전을 먼저 경험하고, 에러율이나 응답 시간 같은 메트릭이 정상이면 트래픽 비율을 점진적으로 높여갑니다(5% -> 25% -> 50% -> 100%).

Canary의 핵심 가치는 **실제 프로덕션 트래픽으로 새 버전을 검증**한다는 점입니다. 스테이징 환경에서 아무리 테스트해도 프로덕션의 트래픽 패턴, 데이터 분포, 엣지 케이스를 완벽히 재현할 수 없습니다. Canary는 이 간극을 좁혀줍니다.

**단점은 구현 복잡도입니다.** 트래픽을 비율로 분할하는 인프라(Istio Service Mesh, NGINX weighted routing 등)가 필요하고, 두 버전의 메트릭을 실시간으로 비교하는 모니터링 시스템이 필수입니다. 또한 두 버전이 동시에 운영되므로 API 호환성에 주의해야 합니다.

### 1.3 Rolling Update

Rolling Update는 기존 인스턴스를 하나씩(또는 일정 비율씩) 새 버전으로 교체하는 전략입니다. Kubernetes의 기본 배포 전략이며, `maxSurge`(최대 추가 가능 Pod 수)와 `maxUnavailable`(최대 중단 가능 Pod 수)로 롤링 속도를 제어합니다.

이 전략이 널리 쓰이는 이유는 **추가 인프라 없이 기존 리소스만으로 배포**할 수 있기 때문입니다. Blue-Green처럼 2배의 서버가 필요하지 않습니다. Kubernetes가 자동으로 새 Pod를 생성하고, 헬스체크를 통과하면 이전 Pod를 종료합니다.

**단점은 롤백 속도입니다.** 문제가 발생하면 이미 교체된 인스턴스를 다시 이전 버전으로 교체해야 하므로, 배포에 걸린 시간만큼 롤백에도 시간이 소요됩니다. 또한 배포 중에 두 버전이 혼재하므로, 사용자에 따라 서로 다른 버전의 응답을 받을 수 있습니다.

### 전략 비교 테이블

| 기준 | Blue-Green | Canary | Rolling Update |
|------|-----------|--------|---------------|
| **롤백 속도** | 즉시 (수초) | 빠름 (트래픽 전환) | 느림 (재배포 필요) |
| **리소스 비용** | 2배 (이중 환경) | 약간 추가 | 최소 (기존 리소스) |
| **구현 복잡도** | 중간 | 높음 (메트릭 비교) | 낮음 (K8s 기본) |
| **다운타임** | 제로 | 제로 | 제로 |
| **실트래픽 검증** | 전체 전환 후 | 점진적 검증 | 점진적 (비의도적) |
| **적합한 상황** | 미션 크리티컬 서비스 | 대규모 사용자 서비스 | 내부 도구, 마이크로서비스 |

### 배포 전략 흐름 비교

```mermaid
sequenceDiagram
    participant LB as Load Balancer
    participant Blue as Blue (v1)
    participant Green as Green (v2)

    Note over LB,Green: === Blue-Green 배포 ===
    LB->>Blue: 100% 트래픽
    Note over Green: v2 배포 + 검증
    Green-->>Green: 스모크 테스트 통과
    LB->>Green: 100% 트래픽 전환
    Note over Blue: 대기 (롤백 대비)

    Note over LB,Green: === Canary 배포 ===
    LB->>Blue: 95% 트래픽
    LB->>Green: 5% 트래픽 (Canary)
    Note over Green: 메트릭 모니터링
    LB->>Blue: 75% 트래픽
    LB->>Green: 25% 트래픽
    LB->>Green: 100% 트래픽

    Note over LB,Green: === Rolling Update ===
    LB->>Blue: Pod 1,2,3 (v1)
    Note over Blue: Pod 1 → v2 교체
    Note over Blue: Pod 2 → v2 교체
    Note over Blue: Pod 3 → v2 교체
    LB->>Green: 모든 Pod v2 완료
```

---

## 2. Jenkins + Kubernetes 배포

Jenkins에서 Kubernetes로 배포하는 방법은 크게 두 가지입니다. `kubectl apply`로 매니페스트를 직접 적용하는 방식과, `helm upgrade`로 Helm Chart를 통해 배포하는 방식입니다.

### 2.1 kubectl을 이용한 직접 배포

가장 직관적인 방법입니다. Jenkins 파이프라인에서 Kubernetes 매니페스트의 이미지 태그를 업데이트하고 `kubectl apply`를 실행합니다.

```groovy
pipeline {
    agent any

    environment {
        REGISTRY = 'registry.example.com'
        IMAGE = "${REGISTRY}/my-app"
        K8S_NAMESPACE = 'production'
    }

    stages {
        stage('Build & Push Image') {
            steps {
                script {
                    def imageTag = "${IMAGE}:${env.BUILD_NUMBER}"
                    sh "docker build -t ${imageTag} ."
                    sh "docker push ${imageTag}"
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl set image deployment/my-app \
                            my-app=${IMAGE}:${env.BUILD_NUMBER} \
                            -n ${K8S_NAMESPACE}
                        kubectl rollout status deployment/my-app \
                            -n ${K8S_NAMESPACE} --timeout=300s
                    """
                }
            }
        }
    }
}
```

여기서 `kubectl rollout status`가 중요합니다. 이 명령은 배포가 완전히 완료될 때까지 대기하며, 타임아웃 내에 완료되지 않으면 실패를 반환합니다. 이를 통해 파이프라인이 배포 성공 여부를 확인할 수 있습니다.

### 2.2 Helm을 이용한 Chart 기반 배포

Helm은 Kubernetes 패키지 매니저입니다. 복잡한 매니페스트를 Chart로 패키징하고, `values.yaml`로 환경별 설정을 관리할 수 있습니다. 동일한 Chart를 dev, staging, production에 각각 다른 values로 배포할 수 있어서 환경 간 일관성을 보장합니다.

```groovy
stage('Deploy with Helm') {
    steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
            sh """
                helm upgrade my-app ./charts/my-app \
                    --namespace ${K8S_NAMESPACE} \
                    --set image.tag=${env.BUILD_NUMBER} \
                    --set image.repository=${IMAGE} \
                    --values ./charts/my-app/values-production.yaml \
                    --wait --timeout 5m \
                    --atomic
            """
        }
    }
}
```

`--atomic` 플래그가 핵심입니다. 배포가 실패하면 자동으로 이전 릴리스로 롤백합니다. `--wait`는 모든 리소스가 Ready 상태가 될 때까지 대기합니다.

### 2.3 kubectl 크레덴셜 관리

Jenkins에서 `kubeconfig`를 다루는 것은 보안상 매우 민감합니다. kubeconfig에는 클러스터 접근 권한이 담겨 있으므로 유출 시 클러스터 전체가 위험해집니다.

| 방법 | 설명 | 보안 수준 |
|------|------|----------|
| **Jenkins Credentials** | kubeconfig를 Secret File로 저장 | 중간 |
| **ServiceAccount Token** | K8s ServiceAccount의 토큰만 사용 | 높음 |
| **OIDC 연동** | Jenkins → OIDC Provider → K8s | 매우 높음 |
| **Vault 연동** | HashiCorp Vault에서 동적 크레덴셜 발급 | 매우 높음 |

가장 권장되는 방식은 **ServiceAccount에 최소 권한을 부여하고, 해당 토큰만 Jenkins에 등록**하는 것입니다. `cluster-admin` 같은 과도한 권한은 절대 부여하지 않아야 합니다. 배포에 필요한 네임스페이스의 Deployment, Service, ConfigMap에 대한 RBAC만 설정합니다.

---

## 3. GitOps 연계

### 3.1 왜 Jenkins가 직접 배포하지 않는가

앞서 Jenkins에서 `kubectl apply`를 직접 실행하는 방법을 살펴보았습니다. 이 방식은 간단하지만, 규모가 커지면 문제가 생깁니다. Jenkins가 직접 배포하면 **"현재 클러스터의 상태"가 어디에도 기록되지 않습니다.** Jenkins 빌드 로그를 뒤져야 어떤 버전이 배포되어 있는지 알 수 있고, 누군가 `kubectl`로 직접 수정하면 추적이 불가능합니다.

GitOps는 이 문제를 해결합니다. **Git 저장소를 "단일 진실의 원천(Single Source of Truth)"으로 삼고**, 클러스터의 상태를 항상 Git과 동기화하는 방식입니다. Git에 커밋된 매니페스트가 곧 프로덕션의 상태입니다. 변경 이력은 Git 히스토리에 남고, 롤백은 `git revert`로 가능합니다.

### 3.2 Push vs Pull 모델

| 구분 | Push 모델 (Jenkins) | Pull 모델 (ArgoCD) |
|------|--------------------|--------------------|
| **동작** | CI 도구가 클러스터에 배포를 "밀어넣음" | 클러스터 내부 에이전트가 Git을 "가져옴" |
| **크레덴셜 위치** | CI 서버에 K8s 접근 권한 필요 | 클러스터 내부에만 Git 접근 권한 필요 |
| **보안** | 외부 → 내부 접근 (공격 표면 넓음) | 내부 → 외부 접근 (공격 표면 좁음) |
| **Drift 감지** | 불가능 (배포 시점에만 확인) | 상시 감지 (주기적 동기화) |
| **감사 추적** | CI 빌드 로그 | Git 커밋 히스토리 |

Pull 모델이 보안상 더 안전한 이유는, **클러스터 외부에 클러스터 접근 권한을 두지 않기 때문**입니다. ArgoCD는 클러스터 내부에서 실행되며, Git 저장소만 읽습니다. Jenkins가 해킹되어도 클러스터 접근 권한이 유출되지 않습니다.

### 3.3 Jenkins CI + ArgoCD CD 패턴

실무에서 가장 많이 사용되는 패턴은 Jenkins가 CI(빌드, 테스트, 이미지 푸시)를 담당하고, ArgoCD가 CD(배포)를 담당하는 분리 모델입니다. Jenkins는 배포 매니페스트가 있는 Git 저장소에 이미지 태그를 업데이트하는 커밋만 생성하고, ArgoCD가 이 변경을 감지하여 클러스터에 적용합니다.

```mermaid
flowchart LR
    Dev["개발자<br/>코드 커밋"] --> AppRepo["App Repo<br/>(소스코드)"]
    AppRepo --> Jenkins["Jenkins CI<br/>빌드 + 테스트"]
    Jenkins --> Registry["Container<br/>Registry"]
    Jenkins --> |"이미지 태그<br/>업데이트 커밋"| ManifestRepo["Manifest Repo<br/>(K8s YAML)"]
    ManifestRepo --> |"변경 감지<br/>(Pull)"| ArgoCD["ArgoCD"]
    ArgoCD --> |"동기화"| K8s["Kubernetes<br/>Cluster"]
    K8s --> |"상태 비교"| ArgoCD
```

Jenkins 파이프라인에서 매니페스트 저장소를 업데이트하는 코드는 다음과 같습니다.

```groovy
stage('Update Manifest Repo') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'git-credentials',
            usernameVariable: 'GIT_USER',
            passwordVariable: 'GIT_TOKEN'
        )]) {
            sh """
                git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/org/k8s-manifests.git
                cd k8s-manifests

                # kustomize로 이미지 태그 업데이트
                cd overlays/production
                kustomize edit set image my-app=${IMAGE}:${env.BUILD_NUMBER}

                git add .
                git commit -m "deploy: my-app ${env.BUILD_NUMBER}"
                git push origin main
            """
        }
    }
}
```

이 패턴에서 Jenkins는 `kubectl`을 전혀 사용하지 않습니다. 클러스터 접근 권한도 필요 없습니다. Jenkins의 역할은 "이미지를 빌드하고, 매니페스트 저장소에 커밋하는 것"으로 명확히 한정됩니다.

---

## 4. 롤백 전략

배포는 성공하는 것보다 **실패했을 때 빠르게 복구하는 것이 더 중요합니다.** 프로덕션에서 5분간 장애가 발생하면 매출 손실, 사용자 이탈, 신뢰도 하락이 동시에 발생합니다. 롤백 전략은 이 피해를 최소화하기 위한 안전장치입니다.

### 4.1 자동 롤백 조건

자동 롤백은 "사람이 판단하기 전에 시스템이 먼저 대응"하는 메커니즘입니다. 다음 조건 중 하나라도 충족되면 즉시 롤백을 트리거합니다.

| 조건 | 기준 예시 | 감지 방법 |
|------|----------|----------|
| **헬스체크 실패** | Readiness Probe 3회 연속 실패 | Kubernetes 자체 감지 |
| **에러율 급증** | 5xx 에러율 > 1% (기존 대비) | Prometheus + AlertManager |
| **응답시간 증가** | p99 레이턴시 > 2초 (기존 대비 2배) | Grafana Alert |
| **비즈니스 메트릭 이상** | 주문 전환율 30% 하락 | Custom Metric |

핵심은 **절대값이 아니라 "기존 대비 변화율"로 판단**하는 것입니다. 평소 에러율이 0.1%인 서비스에서 0.5%로 올라가면 5배 증가한 것이므로 심각한 신호입니다. 하지만 절대값 1%라는 기준만 보면 정상으로 판단할 수 있습니다.

### 4.2 헬스체크 기반 배포 판단

Kubernetes는 두 가지 프로브를 제공합니다. **Readiness Probe**는 "이 Pod가 트래픽을 받을 준비가 되었는가"를 확인합니다. Readiness Probe를 통과하지 못한 Pod는 Service의 엔드포인트에서 제거되어 트래픽을 받지 않습니다. **Liveness Probe**는 "이 Pod가 살아 있는가"를 확인합니다. 실패하면 Pod를 재시작합니다.

배포 전략에서 중요한 것은 Readiness Probe입니다. 새 버전의 Pod가 Readiness Probe를 통과해야만 트래픽을 받기 시작합니다. 프로브에 단순한 `/health` 엔드포인트뿐 아니라, DB 연결 확인, 캐시 워밍업 완료, 의존 서비스 연결 등을 포함하면 더 안전합니다.

스모크 테스트는 프로브보다 한 단계 더 나아갑니다. 배포 직후 핵심 비즈니스 플로우(로그인, 주문 생성 등)를 실제로 실행하여 기능적 정상 동작을 확인합니다.

### 4.3 Jenkins에서의 롤백 흐름

```groovy
stage('Deploy & Verify') {
    steps {
        script {
            try {
                // 배포 실행
                sh "kubectl set image deployment/my-app my-app=${IMAGE}:${env.BUILD_NUMBER}"
                sh "kubectl rollout status deployment/my-app --timeout=300s"

                // 스모크 테스트
                def smokeResult = sh(
                    script: './scripts/smoke-test.sh',
                    returnStatus: true
                )

                if (smokeResult != 0) {
                    error("스모크 테스트 실패 - 롤백 시작")
                }
            } catch (Exception e) {
                // 자동 롤백
                echo "배포 실패: ${e.message}"
                sh "kubectl rollout undo deployment/my-app"
                sh "kubectl rollout status deployment/my-app --timeout=120s"

                currentBuild.result = 'FAILURE'
                error("롤백 완료 - 이전 버전으로 복구됨")
            }
        }
    }
}
```

### 4.4 롤백 판단 흐름도

```mermaid
flowchart TD
    Deploy["새 버전 배포"] --> RolloutStatus{"kubectl rollout<br/>status 확인"}
    RolloutStatus --> |"타임아웃/실패"| AutoRollback["자동 롤백<br/>kubectl rollout undo"]
    RolloutStatus --> |"성공"| Smoke["스모크 테스트<br/>핵심 API 호출"]
    Smoke --> |"실패"| AutoRollback
    Smoke --> |"성공"| Monitor["메트릭 모니터링<br/>(5~15분)"]
    Monitor --> |"에러율 급증<br/>레이턴시 증가"| AutoRollback
    Monitor --> |"정상"| Complete["배포 완료"]
    AutoRollback --> Notify["알림 발송<br/>Slack / PagerDuty"]
    Notify --> Investigate["원인 분석"]
    Complete --> Cleanup["이전 환경 정리"]
```

---

## 5. Feature Flag

### 5.1 배포와 릴리스의 분리

전통적으로 "배포"와 "릴리스"는 같은 의미였습니다. 코드를 서버에 올리는 순간 사용자가 새 기능을 사용할 수 있었습니다. Feature Flag는 이 두 개념을 분리합니다. **코드는 배포하지만, 기능은 플래그로 비활성화한 상태로 유지**할 수 있습니다. 릴리스는 플래그를 켜는 순간에 발생합니다.

이 분리가 중요한 이유는 **롤백 없이 기능을 끌 수 있기 때문**입니다. 새 결제 시스템에 문제가 생기면, 전체 배포를 롤백하는 대신 해당 기능의 플래그만 끄면 됩니다. 다른 기능들은 영향을 받지 않습니다. 롤백에 비해 위험도가 극히 낮고, 수행 시간도 수초에 불과합니다.

### 5.2 Feature Flag의 활용 패턴

| 패턴 | 설명 | 예시 |
|------|------|------|
| **Release Flag** | 개발 완료 전 코드를 main에 머지 | 대규모 기능 개발 시 장기 브랜치 방지 |
| **Experiment Flag** | A/B 테스트를 위한 사용자 분할 | 새 UI vs 기존 UI 전환율 비교 |
| **Ops Flag** | 운영 중 기능 토글 | 부하 시 추천 엔진 비활성화 |
| **Permission Flag** | 사용자 그룹별 기능 제어 | 베타 테스터에게만 새 기능 공개 |

### 5.3 Feature Flag 도구 비교

| 도구 | 특징 | 적합한 상황 |
|------|------|-----------|
| **LaunchDarkly** | SaaS, 실시간 평가, SDK 풍부 | 엔터프라이즈, 빠른 도입 |
| **Unleash** | 오픈소스, 셀프호스팅 가능 | 보안 민감 환경, 비용 절감 |
| **자체 구현** | DB/Config 기반 단순 플래그 | 소규모 팀, 단순 on/off |

### 5.4 CI/CD와의 통합

Feature Flag는 배포 파이프라인과 결합할 때 진정한 가치를 발휘합니다. Jenkins 파이프라인에서 배포 후 Feature Flag를 자동으로 제어할 수 있습니다.

```groovy
stage('Progressive Rollout') {
    steps {
        script {
            // 1단계: 내부 사용자에게만 활성화
            sh """
                curl -X PATCH https://feature-flags.example.com/api/flags/new-checkout \
                    -H 'Authorization: Bearer ${FF_TOKEN}' \
                    -d '{"rules": [{"segments": ["internal-users"], "enabled": true}]}'
            """

            // 2단계: 메트릭 확인 후 10% 사용자에게 확대
            sleep(time: 10, unit: 'MINUTES')
            sh './scripts/check-metrics.sh'

            sh """
                curl -X PATCH https://feature-flags.example.com/api/flags/new-checkout \
                    -d '{"rolloutPercentage": 10}'
            """
        }
    }
}
```

Feature Flag와 Canary 배포의 차이를 이해하는 것이 중요합니다. Canary는 **인프라 레벨**에서 트래픽을 분할합니다. 새 버전의 Pod로 트래픽 일부를 보냅니다. Feature Flag는 **애플리케이션 레벨**에서 기능을 분할합니다. 같은 버전의 코드가 실행되지만, 사용자에 따라 다른 코드 경로를 탑니다. 둘을 조합하면 더 세밀한 릴리스 제어가 가능합니다. Canary로 인프라 안정성을 확인하고, Feature Flag로 비즈니스 기능을 점진적으로 활성화하는 방식입니다.

---

## 정리: 배포 전략 의사결정 트리

어떤 전략을 선택할지는 서비스의 특성과 팀의 역량에 따라 달라집니다. 미션 크리티컬 서비스라면 Blue-Green + Feature Flag 조합이 안전합니다. 대규모 트래픽 서비스라면 Canary로 점진적 검증이 필요합니다. 내부 도구나 마이크로서비스라면 Rolling Update만으로 충분합니다.

궁극적으로 모든 배포 전략의 목표는 같습니다. **"사용자가 장애를 체감하기 전에 복구한다."** 30초 안에 롤백할 수 있는 시스템을 구축하는 것이 배포 엔지니어링의 핵심입니다.
