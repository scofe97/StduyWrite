<!-- migrated: write/09_cloud/kubernetes/deepdive/05-01.Helm 기초 점검.md (2026-04-19) -->

# Ch05: Helm 기초 - 점검 질문

이 문서는 Ch05에서 배운 Helm 기본 개념을 실전 관점에서 점검합니다. 각 질문은 실무에서 자주 마주치는 상황을 다룹니다.

---

## Q1: Helm v3에서 Tiller를 제거한 이유와 보안 개선

### 질문
Helm v2에서 v3로 넘어오면서 Tiller 컴포넌트를 제거했습니다. Tiller가 무엇이었고, 왜 제거되었으며, 이로 인해 어떤 보안 개선이 이루어졌는지 설명하세요.

### 핵심 포인트

- **Tiller의 역할 (Helm v2)**: Tiller는 클러스터 내부에서 실행되는 서버 컴포넌트로, Helm CLI의 요청을 받아 K8s API 서버와 통신하며 릴리스를 관리했습니다. Helm CLI는 Tiller와 gRPC로 통신하고, Tiller가 실제 리소스를 생성/수정/삭제했습니다.

- **보안 문제**: Tiller는 cluster-admin 권한을 가지고 있었기 때문에, Tiller에 접근할 수 있는 모든 사용자가 사실상 클러스터 전체에 대한 권한을 가지게 되었습니다. RBAC로 사용자를 제한해도 Tiller 레벨에서 권한이 뚫리는 문제가 발생했습니다. 또한 Tiller는 단일 인스턴스로 실행되어 멀티테넌시 환경에서 네임스페이스 격리가 어려웠습니다.

- **제거 배경**: Kubernetes 1.6부터 RBAC가 기본 활성화되면서, Tiller의 강력한 권한이 보안 취약점으로 부각되었습니다. 또한 kubeconfig를 사용하면 Helm CLI가 직접 API 서버와 통신할 수 있으므로, Tiller라는 중간 레이어가 불필요하다는 인식이 확산되었습니다.

- **v3의 개선**: Helm v3는 Tiller를 제거하고 Helm CLI가 kubeconfig의 인증 정보를 사용하여 직접 K8s API 서버와 통신합니다. 사용자의 kubectl 권한이 그대로 Helm에 적용되므로, RBAC가 완벽하게 작동하고 네임스페이스별 권한 분리가 자연스럽게 이루어집니다. 릴리스 정보는 Secret으로 저장되어 네임스페이스 내에서 격리됩니다.

- **운영 부담 감소**: Tiller를 클러스터에 설치/업그레이드/모니터링할 필요가 없어져, Helm이 순수한 클라이언트 도구가 되었습니다. 설치는 `brew install helm` 하나로 끝나며, 클러스터에 추가 컴포넌트가 배포되지 않습니다.

### 심화 질문

**Q1-1**: Helm v2 시절에 Tiller를 네임스페이스별로 분리하여 멀티테넌시를 구현하는 방법이 있었습니다. 이 방식의 한계는 무엇이었나요?

**힌트**: 각 네임스페이스마다 Tiller를 배포하면 네임스페이스 격리는 되지만, Tiller 간 릴리스 이름 충돌, Tiller 버전 불일치, 관리 복잡도 증가 등의 문제가 발생했습니다.

**Q1-2**: Helm v3에서 릴리스 정보를 ConfigMap이 아닌 Secret으로 저장하는 이유는 무엇인가요?

**힌트**: Secret은 RBAC로 접근 제어가 가능하고, etcd에서 암호화 저장을 지원하며, values에 포함된 민감 정보(API 키, 비밀번호 등)를 보호할 수 있습니다.

---

## Q2: helm install vs kubectl apply의 차이 (릴리스 관리, 롤백)

### 질문
`kubectl apply -f manifests/`와 `helm install myapp ./chart`는 둘 다 K8s 리소스를 생성하지만, Helm의 릴리스 관리와 롤백 기능이 어떻게 다른지 설명하세요.

### 핵심 포인트

- **kubectl apply의 동작**: kubectl apply는 매니페스트의 `last-applied-configuration` 어노테이션과 현재 클러스터 상태를 비교하여 변경사항을 적용합니다 (2-way merge). 각 리소스는 독립적으로 관리되며, Deployment, Service, ConfigMap 등의 연관성을 추적하지 않습니다.

- **Helm의 릴리스 개념**: Helm은 여러 리소스를 하나의 "릴리스"로 묶어 관리합니다. 릴리스는 이름, 버전(REVISION), 상태(deployed/failed/superseded)를 가지며, Secret으로 저장됩니다. 하나의 릴리스에 포함된 모든 리소스가 원자적으로 관리됩니다.

- **롤백의 차이**: kubectl은 Deployment에 대해서만 `kubectl rollout undo`를 지원하며, Service나 ConfigMap은 수동으로 이전 버전을 재적용해야 합니다. Helm은 `helm rollback` 하나로 모든 리소스(Deployment, Service, ConfigMap, Ingress 등)를 이전 REVISION 상태로 복원합니다.

- **히스토리 추적**: kubectl은 배포 히스토리를 저장하지 않으므로 Git 커밋 기록에 의존해야 합니다. Helm은 각 REVISION을 Secret으로 저장하여 `helm history`로 언제든 조회할 수 있고, 특정 버전의 values와 manifest를 `helm get values --revision N`으로 추출할 수 있습니다.

- **3-way merge**: Helm v3는 이전 릴리스, 새 차트 렌더링, 클러스터 실제 상태를 비교하는 3-way merge를 사용합니다. 이는 수동 변경(kubectl scale, kubectl edit 등)을 감지하고 conflict를 처리하는 데 유리합니다.

- **멀티 리소스 일관성**: Helm upgrade 중 일부 리소스가 실패하면 전체 업그레이드가 실패로 표시되고, 롤백으로 일관된 상태로 복구할 수 있습니다. kubectl apply는 각 파일이 독립적으로 성공/실패하므로 부분 적용 상태가 될 수 있습니다.

### 심화 질문

**Q2-1**: Helm 릴리스가 "deployed" 상태인데도 실제 Pod가 CrashLoopBackOff 상태일 수 있습니다. Helm의 "성공" 기준은 무엇인가요?

**힌트**: Helm은 K8s API 서버에 리소스를 제출하는 것까지만 책임지며, Pod의 실행 상태는 확인하지 않습니다. `helm install --wait` 플래그를 사용하면 Pod가 Ready 상태가 될 때까지 대기합니다.

**Q2-2**: `kubectl apply`의 `last-applied-configuration`과 Helm의 릴리스 정보는 충돌할 수 있나요? Helm으로 설치한 리소스를 kubectl apply로 수정하면 어떻게 되나요?

**힌트**: Helm과 kubectl을 혼용하면 Helm의 3-way merge가 혼란스러워질 수 있습니다. Helm으로 관리하는 리소스는 helm upgrade로만 변경하는 것이 권장됩니다.

---

## Q3: helm upgrade --install 플래그의 의미와 CI/CD에서의 활용

### 질문
`helm upgrade --install` 명령어는 어떤 상황에서 사용되며, CI/CD 파이프라인에서 왜 유용한지 설명하세요.

### 핵심 포인트

- **동작 방식**: `helm upgrade --install <release> <chart>`는 릴리스가 존재하면 upgrade를 실행하고, 존재하지 않으면 install을 실행합니다. 즉, 명령어 하나로 설치와 업그레이드를 모두 처리합니다.

- **CI/CD의 멱등성 요구**: CI/CD 파이프라인은 여러 번 실행되어도 동일한 결과를 내야 합니다(멱등성). `helm install`은 릴리스가 이미 존재하면 실패하고, `helm upgrade`는 릴리스가 없으면 실패하므로, 파이프라인 스크립트에서 조건 분기가 필요합니다. `--install`은 이를 단순화합니다.

- **배포 스크립트 단순화**: 기존 방식은 `helm list`로 릴리스 존재 여부를 확인한 뒤 분기 처리해야 했습니다:

  ```bash
  # 복잡한 방식
  if helm list | grep -q myapp; then
    helm upgrade myapp ./chart
  else
    helm install myapp ./chart
  fi

  # 단순화
  helm upgrade --install myapp ./chart -f values.yaml
  ```

- **재시도 안전성**: 배포가 중간에 실패하더라도 동일한 명령어를 재실행하면 이어서 진행됩니다. 네트워크 장애 등으로 파이프라인이 중단되어도 재시도가 안전합니다.

- **실전 CI/CD 예시**:

  ```yaml
  # GitLab CI
  deploy:
    script:
      - helm repo update
      - helm upgrade --install myapp bitnami/nginx \
          -f values-${CI_ENVIRONMENT_NAME}.yaml \
          --set image.tag=${CI_COMMIT_SHORT_SHA} \
          --namespace ${CI_ENVIRONMENT_NAME} \
          --create-namespace \
          --wait --timeout 5m
  ```

- **주의사항**: `--install`과 함께 `--reset-values`를 사용하면 위험합니다. 기존 릴리스의 values를 모두 무시하고 새로 설정하므로, 이전에 `--set`으로 추가한 값이 사라질 수 있습니다. 항상 `-f values.yaml`로 모든 설정을 명시하는 것이 안전합니다.

### 심화 질문

**Q3-1**: `helm upgrade --install --atomic` 플래그는 무엇을 하나요? CI/CD에서 왜 유용한가요?

**힌트**: `--atomic`은 업그레이드 실패 시 자동으로 이전 버전으로 롤백합니다. `--wait`와 함께 사용하면 Pod가 Ready 상태가 되지 않으면 자동 롤백되어, CI/CD가 항상 안정된 상태를 유지합니다.

**Q3-2**: GitOps(ArgoCD, Flux)를 사용하면 `helm upgrade --install`을 CI/CD에서 직접 실행하지 않습니다. 어떤 방식으로 배포되나요?

**힌트**: GitOps는 Git 레포지토리의 Helm 차트/values를 모니터링하고, 변경 시 자동으로 클러스터에 적용합니다. CI/CD는 Git에 커밋만 하고, 실제 배포는 클러스터 내 컨트롤러가 수행합니다.

---

## Q4: Values 우선순위 (chart defaults → -f values.yaml → --set)

### 질문
Helm에서 values는 여러 소스에서 제공될 수 있습니다. 차트의 기본 values.yaml, `-f` 플래그로 지정한 파일, `--set` 플래그의 우선순위를 설명하고, 실전에서 이를 어떻게 활용하는지 예시를 들어주세요.

### 핵심 포인트

- **우선순위 (낮음 → 높음)**:
  1. **차트의 values.yaml**: 차트에 포함된 기본값 (가장 낮은 우선순위)
  2. **-f values1.yaml**: 첫 번째 values 파일
  3. **-f values2.yaml**: 두 번째 values 파일 (여러 개 지정 시 나중 파일이 우선)
  4. **--set key=value**: 명령줄 플래그 (가장 높은 우선순위)

- **병합 방식**: 값은 재귀적으로 병합됩니다. 중첩된 맵의 경우 상위 우선순위가 특정 키만 덮어쓰고, 나머지는 유지됩니다:

  ```yaml
  # 차트 기본값
  resources:
    limits:
      memory: 512Mi
      cpu: 500m
    requests:
      memory: 256Mi

  # -f prod-values.yaml
  resources:
    limits:
      memory: 2Gi

  # 최종 병합 결과
  resources:
    limits:
      memory: 2Gi    # 덮어씀
      cpu: 500m      # 유지
    requests:
      memory: 256Mi  # 유지
  ```

- **실전 활용 패턴**:
  - **base-values.yaml**: 모든 환경 공통 설정 (로깅 레벨, 포트 등)
  - **prod-values.yaml**: 프로덕션 전용 (replica, resources)
  - **--set**: CI/CD에서 동적 값 주입 (image tag, build number)

  ```bash
  helm upgrade --install myapp ./chart \
    -f base-values.yaml \        # 공통
    -f prod-values.yaml \         # 환경별
    --set image.tag=${GIT_SHA}    # 동적
  ```

- **복잡한 값 설정**: `--set`으로 배열이나 중첩 맵을 설정할 때 복잡해집니다:

  ```bash
  # 배열
  --set ingress.hosts[0].host=example.com
  --set ingress.hosts[0].paths[0]=/

  # 중첩 맵
  --set resources.limits.memory=2Gi

  # 쉼표 포함 값 (이스케이프)
  --set key="value1\,value2"
  ```

  이런 경우 `-f values.yaml`이 가독성이 좋습니다.

- **주의사항**: `helm upgrade --reuse-values`를 사용하면 이전 릴리스의 values를 재사용하면서 새로운 `--set`을 추가합니다. 하지만 차트의 새 기본값이 무시될 수 있으므로 권장하지 않습니다. 항상 `-f`로 모든 설정을 명시하는 것이 안전합니다.

### 심화 질문

**Q4-1**: `helm upgrade --reset-values`는 언제 사용하나요? 위험성은 무엇인가요?

**힌트**: `--reset-values`는 이전 values를 모두 버리고 차트 기본값만 사용합니다. 이전에 `--set`으로 추가한 중요한 설정(예: DB 연결 정보)이 사라질 수 있으므로, 의도적으로 초기화할 때만 사용합니다.

**Q4-2**: Helm 차트의 values.yaml에서 민감 정보(DB 비밀번호 등)를 어떻게 관리하나요? `--set`으로 넘기면 히스토리에 평문으로 남지 않나요?

**힌트**: Helm values는 Secret으로 저장되지만 base64 인코딩일 뿐 암호화가 아닙니다. 민감 정보는 Kubernetes Secret으로 별도 생성하고 차트에서 참조하거나, Sealed Secrets, External Secrets Operator, Vault 등을 사용해야 합니다.

---

## Q5: Helm release와 K8s namespace의 관계

### 질문
Helm 릴리스와 Kubernetes 네임스페이스는 어떤 관계인가요? 동일한 릴리스 이름을 다른 네임스페이스에 설치할 수 있는지, 릴리스 정보는 어디에 저장되는지 설명하세요.

### 핵심 포인트

- **릴리스는 네임스페이스 스코프**: Helm v3에서 릴리스는 특정 네임스페이스에 속합니다. 릴리스 이름은 네임스페이스 내에서만 고유하면 되므로, 다른 네임스페이스에 동일한 이름의 릴리스를 설치할 수 있습니다:

  ```bash
  helm install myapp ./chart -n dev
  helm install myapp ./chart -n prod  # OK - 다른 네임스페이스
  helm install myapp ./chart -n dev   # Error - 동일 네임스페이스에 중복
  ```

- **릴리스 정보 저장 위치**: 릴리스 메타데이터는 해당 네임스페이스의 Secret으로 저장됩니다. `sh.helm.release.v1.<release-name>.v<revision>` 형식의 이름을 가집니다:

  ```bash
  kubectl get secrets -n dev | grep helm
  # sh.helm.release.v1.myapp.v1
  # sh.helm.release.v1.myapp.v2

  kubectl get secrets -n prod | grep helm
  # sh.helm.release.v1.myapp.v1  (dev와 별개)
  ```

- **크로스 네임스페이스 리소스**: 차트가 여러 네임스페이스에 리소스를 생성하더라도, 릴리스 정보는 `helm install -n` 플래그로 지정한 네임스페이스에만 저장됩니다:

  ```yaml
  # templates/namespace-role.yaml
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRole  # 클러스터 레벨 리소스
  metadata:
    name: {{ .Release.Name }}-viewer
  ```

  ```bash
  helm install myapp ./chart -n dev
  # ClusterRole은 생성되지만, 릴리스 Secret은 dev 네임스페이스에만 존재
  ```

- **릴리스 조회**: `helm list`는 기본적으로 현재 kubeconfig의 네임스페이스만 조회합니다. 모든 네임스페이스를 보려면 `-A` 플래그 사용:

  ```bash
  helm list          # 현재 네임스페이스만
  helm list -n prod  # prod 네임스페이스만
  helm list -A       # 모든 네임스페이스
  ```

- **권한 관리**: 사용자가 특정 네임스페이스에 대한 RBAC 권한이 있으면 그 네임스페이스의 릴리스만 관리할 수 있습니다. Helm v3는 kubeconfig의 권한을 그대로 사용하므로, 멀티테넌시 환경에서 자연스럽게 격리됩니다.

### 심화 질문

**Q5-1**: Helm 차트에서 네임스페이스를 하드코딩하면 어떤 문제가 발생하나요?

**힌트**: 템플릿에서 `namespace: production`처럼 고정하면 다른 네임스페이스에 설치할 때 충돌이 발생합니다. 항상 `{{ .Release.Namespace }}`를 사용하여 동적으로 설정해야 합니다.

**Q5-2**: 릴리스를 삭제(`helm uninstall`)하면 차트가 생성한 PersistentVolumeClaim도 삭제되나요?

**힌트**: PVC는 기본적으로 삭제됩니다. 데이터 보존이 필요하면 차트 설계 시 `helm.sh/resource-policy: keep` 어노테이션을 PVC에 추가하거나, `helm uninstall --keep-history`를 사용합니다.

---

## Q6: helm template vs helm install --dry-run의 차이

### 질문
`helm template`과 `helm install --dry-run`은 둘 다 실제 설치 없이 렌더링 결과를 보여줍니다. 두 명령어의 차이점과 각각의 사용 시나리오를 설명하세요.

### 핵심 포인트

- **helm template의 동작**: 클라이언트 측에서만 차트를 렌더링합니다. K8s API 서버와 통신하지 않으므로 kubeconfig 없이도 실행 가능합니다. `.Capabilities` (K8s 버전, API 버전)는 기본값을 사용합니다.

  ```bash
  helm template myapp ./chart -f values.yaml > output.yaml
  # API 서버 접근 불필요, 빠름
  # 결과를 파일로 저장 가능
  ```

- **helm install --dry-run의 동작**: 실제 설치 과정을 시뮬레이션하며 K8s API 서버와 통신합니다. API 서버의 validation을 거치고, `.Capabilities`를 클러스터에서 가져오며, 기존 리소스와의 충돌 여부를 확인합니다.

  ```bash
  helm install myapp ./chart --dry-run --debug
  # API 서버와 통신, 실제 클러스터 정보 사용
  # validation 에러 감지 가능
  ```

- **차이점 비교**:

  | 특징 | helm template | helm install --dry-run |
  |------|---------------|------------------------|
  | **API 서버 접근** | 없음 | 있음 (kubeconfig 필요) |
  | **.Capabilities** | 기본값 (최신 K8s 가정) | 실제 클러스터 정보 |
  | **리소스 validation** | 없음 (문법만 확인) | 있음 (API 서버가 검증) |
  | **속도** | 빠름 | 느림 (네트워크 통신) |
  | **오프라인 사용** | 가능 | 불가능 |
  | **Lookup 함수** | 작동 안 함 | 작동 (클러스터 조회) |

- **사용 시나리오**:
  - **helm template**: CI/CD에서 매니페스트 생성, GitOps 레포지토리에 커밋, 렌더링 결과 리뷰
  - **helm install --dry-run**: 실제 배포 전 최종 검증, API 변경 감지 (deprecated API 등)

- **Lookup 함수 차이**: Helm 템플릿은 `{{ lookup }}` 함수로 클러스터의 기존 리소스를 조회할 수 있습니다:

  ```yaml
  # 기존 Secret이 있으면 재사용, 없으면 생성
  {{- $secret := lookup "v1" "Secret" .Release.Namespace "myapp-secret" }}
  {{- if $secret }}
  data:
    password: {{ $secret.data.password }}
  {{- else }}
  data:
    password: {{ randAlphaNum 16 | b64enc }}
  {{- end }}
  ```

  `helm template`에서는 lookup이 항상 빈 값을 반환하지만, `--dry-run`에서는 실제 클러스터를 조회합니다.

- **Hooks 처리**: `helm template`은 Hooks를 일반 리소스처럼 출력하지만, `--dry-run`은 Hook 실행을 시뮬레이션합니다 (실제로 실행하지는 않음).

### 심화 질문

**Q6-1**: GitOps(ArgoCD)에서 Helm 차트를 배포할 때 `helm template`의 결과를 Git에 커밋하는 방식과, 차트 자체를 Git에 넣고 ArgoCD가 렌더링하는 방식의 장단점은 무엇인가요?

**힌트**: 렌더링 결과 커밋은 변경사항 리뷰가 쉽지만 Git이 커지고, 차트 직접 사용은 Git이 가볍지만 렌더링 결과를 미리 보기 어렵습니다. 하이브리드 방식으로 PR에서만 렌더링 결과를 코멘트로 추가하는 방법도 있습니다.

**Q6-2**: `helm install --dry-run`을 CI/CD 파이프라인에서 실행할 때, 클러스터에 접근 권한이 없으면 어떻게 하나요?

**힌트**: 권한이 없으면 `helm template` + `kubectl apply --dry-run=client` 조합을 사용하거나, 별도의 검증 클러스터를 구축합니다. 또는 Kubeval, Kubeconform 같은 정적 분석 도구를 사용합니다.

---

## 종합 점검

이 6가지 질문을 통해 다음을 확인할 수 있습니다:

- **아키텍처 이해**: Helm v3의 Tiller 제거와 3-way merge 메커니즘
- **실전 워크플로우**: CI/CD에서의 `--install`, values 우선순위 활용
- **멀티테넌시**: 네임스페이스와 릴리스의 관계, 권한 격리
- **도구 선택**: template vs dry-run의 적절한 사용

다음 Ch06에서는 이러한 개념을 바탕으로 직접 Helm 차트를 작성하고, 템플릿 언어를 사용하여 재사용 가능한 패키지를 설계하는 방법을 배웁니다.
