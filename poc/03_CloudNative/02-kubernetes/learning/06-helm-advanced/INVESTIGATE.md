# Ch06: Helm 고급 - 점검 질문

이 문서는 Ch06에서 배운 Helm 차트 개발과 템플릿 설계를 실전 관점에서 점검합니다. 각 질문은 실무에서 자주 마주치는 설계 결정과 디버깅 상황을 다룹니다.

---

## Q1: _helpers.tpl에서 define vs template vs include 차이

### 질문
_helpers.tpl에서 Named Template을 정의할 때 `define`, `template`, `include`를 사용합니다. 각각의 역할과 차이점을 설명하고, 왜 `template` 대신 `include`를 사용해야 하는지 예시와 함께 설명하세요.

### 핵심 포인트

- **define**: Named Template을 정의합니다. 템플릿 이름과 내용을 선언하지만, 실행하지는 않습니다. `_helpers.tpl` 파일에서 재사용 가능한 템플릿 조각을 만들 때 사용합니다.

  ```yaml
  {{- define "myapp.labels" -}}
  app.kubernetes.io/name: {{ .Chart.Name }}
  app.kubernetes.io/instance: {{ .Release.Name }}
  {{- end }}
  ```

- **template**: 정의된 Named Template을 호출하여 렌더링합니다. Go 템플릿 엔진의 기본 기능으로, 레거시 방식입니다. **파이프라인을 지원하지 않으므로** 들여쓰기 제어가 어렵습니다.

  ```yaml
  metadata:
    labels:
      {{ template "myapp.labels" . }}  # 들여쓰기 안 됨
  ```

  **문제**: 위 코드는 렌더링 결과가 들여쓰기되지 않아 YAML 구문 오류가 발생합니다.

- **include**: Helm v3에서 추가된 함수로, `template`과 동일하게 Named Template을 호출하지만 **결과를 문자열로 반환**하므로 파이프라인에서 사용할 수 있습니다. 이를 통해 `nindent`, `quote` 같은 함수를 체인할 수 있습니다.

  ```yaml
  metadata:
    labels:
      {{- include "myapp.labels" . | nindent 4 }}  # 4칸 들여쓰기
  ```

- **왜 include를 사용해야 하는가**: YAML은 들여쓰기에 민감하므로, Named Template의 출력을 적절히 들여쓰기해야 합니다. `template`은 파이프라인을 지원하지 않아 수동으로 공백을 관리해야 하지만, `include`는 `nindent`와 결합하여 자동으로 들여쓰기를 처리합니다.

  ```yaml
  # template 사용 시 (잘못된 예시)
  metadata:
    labels:
  {{ template "myapp.labels" . }}  # 들여쓰기 0칸 - 오류!

  # include 사용 (올바른 예시)
  metadata:
    labels:
      {{- include "myapp.labels" . | nindent 4 }}  # 4칸 들여쓰기
  ```

- **실전 패턴**: 모든 Named Template 호출에 `include` + `nindent`를 조합하여 사용하는 것이 Helm 커뮤니티의 베스트 프랙티스입니다. `helm create`로 생성된 스캐폴딩도 `include`를 기본으로 사용합니다.

  ```yaml
  # _helpers.tpl
  {{- define "myapp.selectorLabels" -}}
  app.kubernetes.io/name: {{ .Chart.Name }}
  app.kubernetes.io/instance: {{ .Release.Name }}
  {{- end }}

  # deployment.yaml
  spec:
    selector:
      matchLabels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    template:
      metadata:
        labels:
          {{- include "myapp.selectorLabels" . | nindent 10 }}
  ```

### 심화 질문

**Q1-1**: Named Template 정의 시 `{{- define "myapp.labels" -}}`에서 양쪽에 `-`를 붙이는 이유는 무엇인가요?

**힌트**: `{{-`는 앞쪽 공백을 제거하고, `-}}`는 뒤쪽 공백(줄바꿈)을 제거합니다. Named Template의 정의 자체는 출력되지 않지만, 공백 제거를 통해 렌더링 결과가 깔끔해집니다.

**Q1-2**: `include` 함수의 두 번째 인자 `.`는 무엇을 의미하나요? 다른 값을 전달할 수 있나요?

**힌트**: `.`는 현재 컨텍스트(스코프)를 의미합니다. Named Template 내부에서 `.Values`, `.Release` 등에 접근하려면 컨텍스트를 전달해야 합니다. 특정 값만 전달하려면 `{{ include "myapp.name" .Values.app }}`처럼 사용할 수 있습니다.

---

## Q2: values.yaml 설계 원칙 (flat vs nested, 기본값 전략)

### 질문
Helm 차트의 values.yaml을 설계할 때 flat 구조와 nested 구조 중 어떤 것을 선택해야 하는지, 기본값을 어떻게 제공해야 하는지 설명하세요. 실전 예시와 함께 장단점을 비교해주세요.

### 핵심 포인트

- **Flat 구조**: 모든 설정을 최상위 레벨에 나열합니다. 간단하지만 관련성이 떨어지는 값들이 섞입니다.

  ```yaml
  # Flat 구조
  imageRepository: nginx
  imageTag: "1.25.0"
  imagePullPolicy: IfNotPresent
  serviceType: ClusterIP
  servicePort: 80
  ingressEnabled: false
  ingressHost: example.com
  replicaCount: 3
  ```

  **장점**: 오버라이드가 간단 (`--set imageTag=1.26.0`)
  **단점**: 관련 설정 파악 어려움, 이름 충돌 가능성

- **Nested 구조**: 관련 설정을 객체로 그룹화합니다. 가독성과 확장성이 좋습니다.

  ```yaml
  # Nested 구조 (권장)
  image:
    repository: nginx
    tag: "1.25.0"
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: 80

  ingress:
    enabled: false
    className: nginx
    hosts:
      - host: example.com
        paths:
          - path: /
            pathType: Prefix

  replicaCount: 3
  ```

  **장점**: 논리적 그룹화, 서브차트와 이름 충돌 방지, 확장 용이
  **단점**: 오버라이드가 다소 복잡 (`--set image.tag=1.26.0`)

- **권장 전략**: **Nested 구조를 기본으로 사용**하되, 최상위에 자주 변경되는 값 (replicaCount, environment 등)을 배치합니다. Bitnami, Helm 공식 차트도 이 패턴을 따릅니다.

- **기본값 제공 원칙**:
  1. **합리적인 기본값**: 대부분의 경우 수정 없이 사용 가능하도록 (예: `replicaCount: 1`)
  2. **빈 값 허용**: 선택적 기능은 비활성화 기본값 (예: `ingress.enabled: false`)
  3. **Chart.appVersion 활용**: `image.tag`를 비워두고 템플릿에서 `{{ .Values.image.tag | default .Chart.AppVersion }}`로 폴백
  4. **주석 추가**: 각 필드의 의미와 예시를 주석으로 설명

  ```yaml
  image:
    # 컨테이너 이미지 저장소
    repository: nginx
    # 이미지 태그 (비어있으면 Chart.appVersion 사용)
    # @default -- Chart.appVersion
    tag: ""
    # 이미지 풀 정책 (Always, IfNotPresent, Never)
    pullPolicy: IfNotPresent

  # Pod 복제본 수 (프로덕션에서는 최소 2개 권장)
  replicaCount: 1
  ```

- **환경별 values 분리**: 기본 values.yaml은 개발 환경 기준으로, 프로덕션은 별도 파일로 관리합니다.

  ```bash
  # 개발: 기본값 사용
  helm install myapp ./chart

  # 프로덕션: 오버라이드
  helm install myapp ./chart -f values-prod.yaml
  ```

  **values-prod.yaml**:
  ```yaml
  replicaCount: 3

  resources:
    limits:
      memory: 2Gi
      cpu: 1000m

  ingress:
    enabled: true
    hosts:
      - host: prod.example.com
  ```

- **서브차트 values 통합**: 의존성 차트의 values도 nested 구조로 포함합니다.

  ```yaml
  # 메인 앱 설정
  image:
    repository: myapp

  # PostgreSQL 서브차트 설정
  postgresql:
    enabled: true
    auth:
      database: myapp_db
      username: myapp
      password: ""  # Secret으로 주입 권장
  ```

### 심화 질문

**Q2-1**: values.yaml에서 민감한 정보 (DB 비밀번호, API 키)를 어떻게 관리해야 하나요?

**힌트**: values.yaml에 평문 저장은 위험합니다. 방법: (1) values에 빈 값 + Secret을 별도 생성 후 참조, (2) Sealed Secrets, (3) External Secrets Operator, (4) Vault Integration. 프로덕션에서는 GitOps + Sealed Secrets 조합이 일반적입니다.

**Q2-2**: 여러 환경(dev/staging/prod)에서 values를 공유하면서도 환경별 차이를 관리하는 베스트 프랙티스는 무엇인가요?

**힌트**: Base values (공통) + Environment-specific values (환경별) 패턴을 사용합니다. Helmfile이나 ArgoCD의 values 병합 기능을 활용하면 DRY 원칙을 유지하면서 환경별 설정을 관리할 수 있습니다.

---

## Q3: Helm Hook의 weight와 delete-policy 동작

### 질문
Helm Hook의 `helm.sh/hook-weight`와 `helm.sh/hook-delete-policy` 어노테이션의 동작 원리를 설명하고, 실전 시나리오 (DB 백업 → 마이그레이션 순서 제어, Hook 재실행 시 충돌 방지)에서 어떻게 활용하는지 보여주세요.

### 핵심 포인트

- **helm.sh/hook-weight**: Hook의 실행 순서를 제어합니다. 값은 정수이며, **낮은 숫자가 먼저 실행**됩니다. 기본값은 0입니다. 동일한 weight를 가진 Hook은 알파벳순으로 실행됩니다.

  ```yaml
  # 1단계: DB 백업 (weight: -5)
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: db-backup-job
    annotations:
      "helm.sh/hook": pre-upgrade
      "helm.sh/hook-weight": "-5"

  # 2단계: 애플리케이션 중지 (weight: 0, 기본값)
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: app-stop-job
    annotations:
      "helm.sh/hook": pre-upgrade
      "helm.sh/hook-weight": "0"

  # 3단계: DB 마이그레이션 (weight: 5)
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: db-migrate-job
    annotations:
      "helm.sh/hook": post-upgrade
      "helm.sh/hook-weight": "5"
  ```

  **실행 흐름**: 백업 → 앱 중지 → (Helm 업그레이드) → 마이그레이션

- **helm.sh/hook-delete-policy**: Hook 리소스를 언제 삭제할지 지정합니다. 정책을 지정하지 않으면 Hook은 클러스터에 영구 보존됩니다.

  | 정책 | 동작 시점 |
  |------|----------|
  | `before-hook-creation` | 새 Hook 실행 전에 이전 Hook 삭제 (가장 많이 사용) |
  | `hook-succeeded` | Hook이 성공(Completed)하면 삭제 |
  | `hook-failed` | Hook이 실패하면 삭제 (디버깅 어려워 비추천) |

  **실전 권장**: `before-hook-creation` - Job 이름 충돌을 방지하고, 재배포 시 이전 Hook을 자동 정리합니다.

  ```yaml
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: {{ .Release.Name }}-db-migrate
    annotations:
      "helm.sh/hook": post-upgrade
      "helm.sh/hook-weight": "1"
      "helm.sh/hook-delete-policy": before-hook-creation
  ```

- **재실행 시나리오**: 업그레이드가 실패하고 재시도할 때, `before-hook-creation` 정책이 없으면 Job 이름 충돌로 실패합니다.

  ```bash
  # 첫 번째 시도 (마이그레이션 실패)
  helm upgrade myapp ./chart
  # Job "myapp-db-migrate" created (failed)

  # 두 번째 시도 (정책 없으면)
  helm upgrade myapp ./chart
  # Error: Job "myapp-db-migrate" already exists

  # before-hook-creation 정책이 있으면
  helm upgrade myapp ./chart
  # Job "myapp-db-migrate" deleted (이전 것)
  # Job "myapp-db-migrate" created (새로 생성)
  ```

- **다중 정책 지정**: 쉼표로 구분하여 여러 정책을 동시 적용할 수 있습니다.

  ```yaml
  annotations:
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
  ```

  이 경우: (1) 새 Hook 실행 전 삭제, (2) 성공 시에도 삭제 (디버깅이 필요 없는 경우)

- **weight 범위**: 공식 문서에는 제한이 없지만, 관례적으로 -10 ~ 10 사이를 사용합니다. 극단적인 값 (예: -9999)은 가독성을 해칩니다.

- **복잡한 시나리오 예시**: 블루-그린 배포에서 Hook 순서 제어

  ```yaml
  # 1. 트래픽 드레인 (pre-upgrade, weight: -10)
  # 2. DB 백업 (pre-upgrade, weight: -5)
  # 3. (Helm 업그레이드 - Green 버전 배포)
  # 4. 헬스체크 (post-upgrade, weight: 0)
  # 5. 트래픽 전환 (post-upgrade, weight: 5)
  # 6. Blue 버전 정리 (post-upgrade, weight: 10)
  ```

### 심화 질문

**Q3-1**: Hook Job이 실패하면 Helm 업그레이드는 어떻게 되나요? 릴리스 상태는 어떻게 표시되나요?

**힌트**: Hook이 실패하면 전체 릴리스가 "failed" 상태가 되지만, 이미 생성된 리소스는 롤백되지 않습니다. 수동으로 `helm rollback`을 실행하거나 `--atomic` 플래그를 사용하여 자동 롤백을 설정할 수 있습니다.

**Q3-2**: Hook의 타임아웃은 어떻게 설정하나요? Job이 무한 대기하는 것을 방지하려면?

**힌트**: Helm은 Hook Job의 완료를 기다리지만, 기본 타임아웃은 5분입니다. `helm upgrade --timeout 10m` 플래그로 조정 가능합니다. Job 자체의 타임아웃은 `.spec.activeDeadlineSeconds`로 설정합니다.

---

## Q4: 차트 의존성의 condition과 alias 활용 시나리오

### 질문
Chart.yaml의 `dependencies` 섹션에서 `condition`과 `alias` 필드는 어떤 역할을 하나요? 실전 시나리오 (개발에서는 PostgreSQL 포함, 프로덕션에서는 외부 DB 사용)에서 이를 어떻게 활용하는지 설명하세요.

### 핵심 포인트

- **condition**: values.yaml의 특정 키를 참조하여 서브차트 활성화 여부를 결정합니다. 여러 조건을 쉼표로 연결하면 OR 연산으로 동작합니다 (하나라도 true면 활성화).

  ```yaml
  # Chart.yaml
  dependencies:
    - name: postgresql
      version: 12.5.0
      repository: https://charts.bitnami.com/bitnami
      condition: postgresql.enabled
  ```

  ```yaml
  # values.yaml
  postgresql:
    enabled: true  # true면 PostgreSQL 서브차트 활성화
    auth:
      database: myapp_db
  ```

  ```bash
  # 오버라이드로 비활성화
  helm install myapp ./chart --set postgresql.enabled=false
  ```

- **alias**: 서브차트를 참조할 때 사용할 이름을 변경합니다. 동일한 차트를 여러 번 포함하거나, values.yaml에서 더 명확한 이름을 사용하고 싶을 때 유용합니다.

  ```yaml
  # Chart.yaml
  dependencies:
    - name: postgresql
      version: 12.5.0
      repository: https://charts.bitnami.com/bitnami
      alias: database  # values에서 "database"로 참조
      condition: database.enabled

    - name: postgresql
      version: 12.5.0
      repository: https://charts.bitnami.com/bitnami
      alias: analytics-db  # 두 번째 PostgreSQL 인스턴스
      condition: analytics-db.enabled
  ```

  ```yaml
  # values.yaml
  database:  # alias로 인해 "postgresql" 대신 "database" 사용
    enabled: true
    auth:
      database: main_db

  analytics-db:  # 두 번째 인스턴스
    enabled: false
    auth:
      database: analytics_db
  ```

- **실전 시나리오: 환경별 의존성 제어**

  **개발 환경**: 차트에 PostgreSQL 포함 (간편한 로컬 테스트)
  ```yaml
  # values-dev.yaml
  postgresql:
    enabled: true
    primary:
      persistence:
        enabled: false  # 개발에서는 persistence 불필요

  externalDatabase:
    enabled: false
  ```

  **프로덕션**: 외부 관리형 DB 사용 (RDS, Cloud SQL 등)
  ```yaml
  # values-prod.yaml
  postgresql:
    enabled: false  # 서브차트 비활성화

  externalDatabase:
    enabled: true
    host: prod-db.us-west-2.rds.amazonaws.com
    port: 5432
    database: myapp_prod
    username: myapp
    # password는 Secret으로 주입
  ```

  **deployment.yaml에서 조건부 연결 정보**:
  ```yaml
  env:
  {{- if .Values.postgresql.enabled }}
  - name: DB_HOST
    value: {{ .Release.Name }}-postgresql
  - name: DB_PORT
    value: "5432"
  {{- else if .Values.externalDatabase.enabled }}
  - name: DB_HOST
    value: {{ .Values.externalDatabase.host }}
  - name: DB_PORT
    value: {{ .Values.externalDatabase.port | quote }}
  {{- end }}
  ```

- **다중 조건 (OR 연산)**:

  ```yaml
  dependencies:
    - name: postgresql
      condition: postgresql.enabled, global.database.enabled
  ```

  `postgresql.enabled: true` 또는 `global.database.enabled: true` 중 하나라도 true면 활성화됩니다.

- **tags vs condition**: tags는 여러 서브차트를 그룹으로 제어할 때 사용합니다.

  ```yaml
  # Chart.yaml
  dependencies:
    - name: postgresql
      tags:
        - database
    - name: redis
      tags:
        - cache
    - name: rabbitmq
      tags:
        - queue

  # values.yaml
  tags:
    database: true  # postgresql 활성화
    cache: false    # redis 비활성화
    queue: true     # rabbitmq 활성화
  ```

  **condition이 tags보다 우선순위가 높습니다**: 둘 다 있으면 condition이 먼저 평가됩니다.

### 심화 질문

**Q4-1**: 서브차트의 리소스 이름은 어떻게 생성되나요? 동일한 차트를 alias로 두 번 포함하면 이름 충돌이 발생하지 않나요?

**힌트**: 서브차트 리소스는 `{{ .Release.Name }}-{{ .Chart.Name }}` 형식으로 이름이 생성됩니다. alias를 사용하면 `.Chart.Name`이 alias로 대체되므로 충돌하지 않습니다. 예: `myapp-database`, `myapp-analytics-db`.

**Q4-2**: 부모 차트에서 서브차트의 특정 values만 오버라이드하고, 나머지는 서브차트의 기본값을 유지하려면 어떻게 하나요?

**힌트**: 부모 values.yaml에서 오버라이드할 키만 명시하면 됩니다. Helm은 재귀적으로 values를 병합하므로, 명시하지 않은 키는 서브차트의 기본값이 유지됩니다.

---

## Q5: helm template으로 렌더링 결과 검증하는 워크플로우

### 질문
`helm template` 명령어를 CI/CD 파이프라인에서 어떻게 활용하여 차트 변경사항을 검증하고, 렌더링 결과를 리뷰하는 워크플로우를 설계하세요. GitOps와의 통합 방법도 포함해주세요.

### 핵심 포인트

- **helm template의 역할**: 클러스터 접근 없이 로컬에서 템플릿을 렌더링합니다. API 서버와 통신하지 않으므로 빠르고, kubeconfig 없이도 실행 가능합니다.

  ```bash
  # 기본 렌더링
  helm template myapp ./chart -f values-prod.yaml

  # 특정 네임스페이스 시뮬레이션
  helm template myapp ./chart -n production

  # 특정 템플릿만 렌더링
  helm template myapp ./chart -s templates/deployment.yaml
  ```

- **CI/CD 파이프라인 통합**: PR 생성 시 자동으로 렌더링 결과를 검증하고 코멘트로 추가합니다.

  ```yaml
  # GitHub Actions 예시
  name: Helm Template Validation
  on: [pull_request]

  jobs:
    validate:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3

        - name: Install Helm
          uses: azure/setup-helm@v3

        - name: Render templates
          run: |
            helm template myapp ./chart -f values-prod.yaml > rendered.yaml

        - name: Validate YAML syntax
          run: |
            yamllint rendered.yaml

        - name: Check for deprecated APIs
          run: |
            # Kubeconform으로 K8s API 스키마 검증
            kubeconform -strict -summary rendered.yaml

        - name: Comment rendered output
          uses: actions/github-script@v6
          with:
            script: |
              const fs = require('fs');
              const rendered = fs.readFileSync('rendered.yaml', 'utf8');
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: `## Rendered Manifests\n\`\`\`yaml\n${rendered.slice(0, 10000)}\n\`\`\``
              });
  ```

- **GitOps 통합 (ArgoCD)**: 두 가지 접근 방식이 있습니다.

  **방법 1: 차트 직접 사용** (권장)
  - Git 레포지토리에 Helm 차트와 values 파일 저장
  - ArgoCD가 직접 `helm template` 실행 후 적용
  - 장점: Git이 가볍고 차트 업데이트가 쉬움
  - 단점: ArgoCD UI에서 렌더링 결과를 미리 보기 전까지 확인 어려움

  **방법 2: 렌더링 결과 커밋**
  - CI/CD에서 `helm template` 실행 후 결과를 Git에 커밋
  - ArgoCD는 렌더링된 매니페스트를 직접 적용
  - 장점: 변경사항 리뷰가 쉬움 (diff 확인)
  - 단점: Git 저장소 크기 증가, values 변경 시마다 커밋 필요

  **하이브리드**: 차트는 직접 사용하되, PR에서만 렌더링 결과를 코멘트로 추가하여 리뷰 지원.

- **렌더링 결과 비교 (Diff)**: values 변경이 어떤 리소스에 영향을 미치는지 확인합니다.

  ```bash
  # 기존 values
  helm template myapp ./chart -f values-prod.yaml > old.yaml

  # 새 values
  helm template myapp ./chart -f values-prod-new.yaml > new.yaml

  # Diff
  diff -u old.yaml new.yaml
  # 또는 더 나은 시각화
  dyff between old.yaml new.yaml
  ```

- **환경별 렌더링 검증**: 모든 환경의 values 파일이 유효한지 확인합니다.

  ```bash
  # 스크립트 예시
  for env in dev staging prod; do
    echo "Validating $env environment..."
    helm template myapp ./chart -f values-$env.yaml | kubeconform -strict
  done
  ```

- **실전 워크플로우**:

  ```mermaid
  graph LR
      A[개발자 PR 생성] --> B[CI: helm template]
      B --> C[yamllint 검증]
      C --> D[kubeconform 스키마 검증]
      D --> E[렌더링 결과 PR 코멘트]
      E --> F[리뷰어 확인]
      F --> G{승인?}
      G -->|Yes| H[Merge]
      G -->|No| A
      H --> I[ArgoCD가 감지]
      I --> J[helm template 실행]
      J --> K[클러스터 적용]
  ```

### 심화 질문

**Q5-1**: `helm template`과 `helm install --dry-run`의 차이는 무엇이며, CI/CD에서 어느 것을 사용해야 하나요?

**힌트**: `helm template`은 클러스터 접근이 불필요하고 빠르지만, `.Capabilities`나 `lookup` 함수가 작동하지 않습니다. `--dry-run`은 클러스터 정보를 사용하지만 kubeconfig가 필요합니다. CI/CD에서는 보통 `helm template` + `kubeconform`을 사용합니다.

**Q5-2**: 렌더링된 매니페스트에서 민감한 정보 (Secret의 data)가 노출되는 것을 방지하려면 어떻게 해야 하나요?

**힌트**: Secret 데이터는 템플릿에 하드코딩하지 말고, External Secrets Operator나 Sealed Secrets를 사용하여 참조만 렌더링되도록 합니다. 또는 CI/CD에서 Secret 부분을 필터링하여 코멘트합니다.

---

## Q6: Library Chart vs Application Chart 차이

### 질문
Helm의 Library Chart와 Application Chart의 차이를 설명하고, Library Chart를 언제 사용해야 하는지 실전 예시와 함께 보여주세요.

### 핵심 포인트

- **Application Chart**: 배포 가능한 리소스 (Deployment, Service 등)를 포함하는 일반적인 차트입니다. `helm install`로 클러스터에 설치할 수 있습니다.

  ```yaml
  # Chart.yaml
  apiVersion: v2
  name: myapp
  version: 1.0.0
  type: application  # 기본값
  ```

- **Library Chart**: 리소스를 직접 생성하지 않고, Named Template만 제공하는 차트입니다. 다른 차트에서 `dependencies`로 포함하여 재사용합니다.

  ```yaml
  # Chart.yaml
  apiVersion: v2
  name: common-lib
  version: 0.1.0
  type: library  # Library Chart 선언
  ```

  **주요 특징**:
  - `templates/` 디렉토리에 리소스가 아닌 `_*.tpl` 파일만 포함
  - `helm install`로 직접 설치 불가능
  - 다른 차트의 의존성으로만 사용

- **Library Chart 구조 예시**:

  ```
  common-lib/
  ├── Chart.yaml (type: library)
  └── templates/
      ├── _labels.tpl      # 표준 라벨 함수
      ├── _resources.tpl   # 리소스 템플릿
      └── _validation.tpl  # 검증 함수
  ```

  **_labels.tpl**:
  ```yaml
  {{- define "common.labels.standard" -}}
  app.kubernetes.io/name: {{ include "common.names.name" . }}
  app.kubernetes.io/instance: {{ .Release.Name }}
  app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
  app.kubernetes.io/managed-by: {{ .Release.Service }}
  helm.sh/chart: {{ include "common.names.chart" . }}
  {{- end }}

  {{- define "common.labels.matchLabels" -}}
  app.kubernetes.io/name: {{ include "common.names.name" . }}
  app.kubernetes.io/instance: {{ .Release.Name }}
  {{- end }}
  ```

- **Library Chart 사용 (Application Chart에서)**:

  ```yaml
  # myapp/Chart.yaml
  dependencies:
    - name: common-lib
      version: 0.1.0
      repository: https://charts.example.com
  ```

  ```bash
  helm dependency update ./myapp
  ```

  **myapp/templates/deployment.yaml**:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: {{ .Release.Name }}
    labels:
      {{- include "common.labels.standard" . | nindent 4 }}
  spec:
    selector:
      matchLabels:
        {{- include "common.labels.matchLabels" . | nindent 6 }}
  ```

- **실전 활용 시나리오**:

  **시나리오 1: 조직 표준 라벨/어노테이션**
  - 모든 차트에서 동일한 라벨 규칙 적용
  - Library Chart에 `common.labels`, `common.annotations` 정의
  - 각 애플리케이션 차트가 이를 재사용

  **시나리오 2: 공통 헬퍼 함수**
  - 이름 생성 (`fullname`, `chart`), 이미지 URL 생성, 리소스 검증
  - Library Chart에 정의하고 여러 프로젝트에서 공유

  **시나리오 3: 기업 보안 정책**
  - Security Context, Network Policy 템플릿을 Library Chart로 제공
  - 각 팀이 이를 의존성으로 추가하여 보안 표준 준수

- **Bitnami Common Chart**: 실제 사용 중인 Library Chart 예시

  ```yaml
  # Bitnami 차트들이 공통으로 사용하는 라이브러리
  dependencies:
    - name: common
      version: 2.x.x
      repository: https://charts.bitnami.com/bitnami
  ```

  **제공 함수**: `common.names.fullname`, `common.labels.standard`, `common.images.image` 등

- **Library Chart vs _helpers.tpl 복사**: _helpers.tpl을 모든 차트에 복사하는 대신 Library Chart로 중앙 관리하면 업데이트가 간편합니다. Library Chart 버전만 올리면 모든 의존 차트가 최신 함수 사용 가능.

### 심화 질문

**Q6-1**: Library Chart의 Named Template이 Application Chart의 동일 이름 템플릿과 충돌하면 어떻게 되나요?

**힌트**: 나중에 정의된 템플릿이 우선합니다. Application Chart가 Library Chart를 덮어쓸 수 있으므로, Library Chart의 템플릿 이름은 네임스페이스를 사용하는 것이 좋습니다 (예: `common.labels` vs `myapp.labels`).

**Q6-2**: Library Chart를 private repository에 퍼블리시하려면 어떻게 하나요?

**힌트**: ChartMuseum, Harbor, Nexus 같은 차트 레포지토리를 구축하거나, OCI Registry (GitHub Container Registry, AWS ECR)를 사용합니다. `helm package` → `helm push` 워크플로우로 퍼블리시합니다.

---

## Q7: 차트 버전 관리 전략 (SemVer, appVersion vs version)

### 질문
Chart.yaml의 `version`과 `appVersion` 필드의 차이를 설명하고, 차트 버전 관리 전략 (언제 major/minor/patch를 올려야 하는지)을 SemVer 원칙에 따라 제시하세요.

### 핵심 포인트

- **version**: Helm 차트 자체의 버전입니다. 템플릿, values.yaml, Chart.yaml 등이 변경될 때 증가합니다. SemVer(Semantic Versioning) 형식을 따라야 합니다 (예: `1.2.3`).

- **appVersion**: 차트가 배포하는 애플리케이션의 버전입니다. 주로 컨테이너 이미지 태그와 동일하게 설정합니다. SemVer일 필요는 없지만, 권장됩니다.

  ```yaml
  # Chart.yaml
  apiVersion: v2
  name: myapp
  version: 2.1.0        # 차트 버전
  appVersion: "1.5.2"   # 애플리케이션 버전 (문자열)
  ```

- **SemVer 원칙 (MAJOR.MINOR.PATCH)**:

  | 버전 | 증가 조건 | 예시 |
  |------|----------|------|
  | **MAJOR** | 호환되지 않는 변경 (Breaking Change) | 필수 values 추가, 리소스 이름 변경, API 버전 업그레이드 |
  | **MINOR** | 하위 호환되는 기능 추가 | 새 템플릿 추가, 선택적 values 추가 |
  | **PATCH** | 버그 수정, 문서 업데이트 | 템플릿 오타 수정, 기본값 조정 |

- **차트 버전 증가 예시**:

  **MAJOR 증가 (1.x.x → 2.0.0)**:
  - 기존 values 키 이름 변경 (예: `service.type` → `service.serviceType`)
  - 필수 values 추가 (기존 차트 사용자가 values 수정 필요)
  - 리소스 이름 생성 방식 변경 (기존 리소스와 충돌 가능)
  - K8s API 버전 업그레이드 (예: `apps/v1beta1` → `apps/v1`)

  **MINOR 증가 (1.0.x → 1.1.0)**:
  - Ingress 템플릿 추가 (기본 `enabled: false`)
  - HPA, PodDisruptionBudget 같은 선택적 리소스 추가
  - 새 헬퍼 함수 추가 (_helpers.tpl)

  **PATCH 증가 (1.0.0 → 1.0.1)**:
  - 템플릿 YAML 문법 오류 수정
  - 기본값 조정 (예: `replicaCount: 1` → `replicaCount: 2`, 동작 변경 없음)
  - README 업데이트

- **appVersion 관리**:
  - 애플리케이션 이미지가 업데이트되면 `appVersion`도 함께 업데이트
  - 차트 버전과 독립적으로 관리 (차트 변경 없이 앱 버전만 올릴 수 있음)

  ```yaml
  # 예시: 앱 버전만 올림
  version: 1.2.0        # 차트는 동일
  appVersion: "1.5.3"   # 앱 버전 증가

  # 차트도 함께 수정
  version: 1.3.0        # MINOR 증가 (새 기능 추가)
  appVersion: "1.6.0"   # 앱도 업그레이드
  ```

- **템플릿에서 appVersion 활용**:

  ```yaml
  image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
  ```

  values.yaml에서 `image.tag`를 비워두면 Chart.appVersion이 기본값으로 사용됩니다.

- **실전 워크플로우**:

  ```bash
  # 1. 애플리케이션 새 버전 릴리스
  # appVersion 업데이트, 차트 버전 PATCH 증가
  sed -i 's/appVersion: "1.5.2"/appVersion: "1.5.3"/' Chart.yaml
  sed -i 's/version: 1.2.0/version: 1.2.1/' Chart.yaml

  # 2. 차트에 Ingress 추가 (새 기능)
  # 차트 버전 MINOR 증가
  sed -i 's/version: 1.2.1/version: 1.3.0/' Chart.yaml

  # 3. Breaking Change (values 키 변경)
  # 차트 버전 MAJOR 증가
  sed -i 's/version: 1.3.0/version: 2.0.0/' Chart.yaml

  # 4. 차트 패키징 및 퍼블리시
  helm package ./myapp
  helm push myapp-2.0.0.tgz oci://registry.example.com/charts
  ```

- **의존성 버전 제약**: 다른 차트가 내 차트를 의존성으로 사용할 때 버전 범위 지정 가능

  ```yaml
  dependencies:
    - name: myapp
      version: ~1.2.0  # 1.2.x (PATCH만 허용)
      # 또는
      version: ^1.2.0  # 1.x.x (MINOR, PATCH 허용, MAJOR 고정)
      # 또는
      version: ">=1.2.0 <2.0.0"  # 명시적 범위
  ```

### 심화 질문

**Q7-1**: 차트 버전과 애플리케이션 버전을 동일하게 유지하는 전략 (version == appVersion)의 장단점은 무엇인가요?

**힌트**: 장점은 버전 관리가 단순해지고, 사용자가 혼란을 덜 느낍니다. 단점은 앱 변경 없이 차트만 수정할 때도 appVersion이 증가하여 의미가 모호해집니다. Bitnami는 분리 전략을 사용합니다.

**Q7-2**: 차트 레포지토리에 여러 버전이 있을 때, `helm install`은 어떤 버전을 선택하나요?

**힌트**: 버전 지정 없으면 가장 높은 SemVer 버전을 선택합니다. `helm install myapp repo/myapp --version 1.2.0`으로 특정 버전 지정 가능. `helm search repo myapp --versions`로 모든 버전 조회 가능합니다.

---

## 종합 점검

이 7가지 질문을 통해 다음을 확인할 수 있습니다:

- **템플릿 설계**: define/template/include 차이, Named Template 활용
- **Values 아키텍처**: Nested 구조, 기본값 전략, 환경별 분리
- **Hook 제어**: weight/delete-policy로 배포 라이프사이클 관리
- **의존성 관리**: condition/alias로 서브차트 제어, 환경별 활성화
- **검증 워크플로우**: helm template + CI/CD 통합, GitOps 패턴
- **Library Chart**: 재사용 가능한 템플릿 중앙 관리
- **버전 관리**: SemVer 원칙, version vs appVersion 구분

다음 Ch07에서는 이러한 차트를 프로덕션 환경에서 운영하는 방법, Chart Museum 구축, ArgoCD 통합, 보안 강화 (Sealed Secrets, OPA)를 다룹니다.
