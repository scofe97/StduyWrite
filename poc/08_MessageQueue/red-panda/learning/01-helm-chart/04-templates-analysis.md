# 03. Templates Analysis

Helm 템플릿 파일 분석 및 Go 템플릿 문법

---

## 템플릿 파일 구조

```
templates/
├── entry-point.yaml          # 진입점 (모든 리소스 include)
├── _*.go.tpl                 # 헬퍼 템플릿 (실제 리소스 정의)
│   ├── _statefulset.go.tpl   # StatefulSet
│   ├── _configmap.go.tpl     # ConfigMap
│   ├── _secrets.go.tpl       # Secret
│   ├── _service.*.go.tpl     # Services
│   ├── _rbac.go.tpl          # RBAC
│   └── _helpers.go.tpl       # 공통 헬퍼 함수
└── _helpers.tpl              # 추가 헬퍼
```

---

## 주요 템플릿 역할

| 파일 | 생성 리소스 | 역할 |
|------|------------|------|
| _statefulset.go.tpl | StatefulSet | Redpanda 브로커 Pod 정의 |
| _configmap.go.tpl | ConfigMap | redpanda.yaml, bootstrap.yaml |
| _secrets.go.tpl | Secret | SASL 사용자, TLS 인증서 |
| _service.internal.go.tpl | Service (ClusterIP) | 클러스터 내부 통신 |
| _service.nodeport.go.tpl | Service (NodePort) | 외부 접근 (개발용) |
| _service.loadbalancer.go.tpl | Service (LoadBalancer) | 외부 접근 (프로덕션) |
| _rbac.go.tpl | SA, Role, RoleBinding | 권한 설정 |
| _poddisruptionbudget.go.tpl | PDB | 가용성 보장 |

---

## Go 템플릿 문법

### 기본 문법

```yaml
# 값 참조
{{ .Values.statefulset.replicas }}

# 조건문
{{- if .Values.tls.enabled }}
  tls: enabled
{{- end }}

# 조건문 (else)
{{- if .Values.auth.sasl.enabled }}
  sasl: enabled
{{- else }}
  sasl: disabled
{{- end }}

# 반복문
{{- range $i := until (int .Values.statefulset.replicas) }}
  - broker-{{ $i }}
{{- end }}

# 변수 할당
{{- $fullname := include "redpanda.fullname" . }}
```

### 헬퍼 함수 호출

```yaml
# include - 다른 템플릿 호출
{{ include "redpanda.fullname" . }}
{{ include "redpanda.labels" . | nindent 4 }}

# tpl - 문자열을 템플릿으로 렌더링
{{ tpl .Values.someTemplate . }}

# required - 필수 값 검증
{{ required "storage.size is required" .Values.storage.persistentVolume.size }}
```

### 공통 함수

```yaml
# 들여쓰기
{{ .Values.labels | nindent 4 }}     # 4칸 들여쓰기 + 줄바꿈
{{ .Values.labels | indent 4 }}      # 4칸 들여쓰기

# 기본값
{{ .Values.image.tag | default .Chart.AppVersion }}

# 문자열 조작
{{ .Values.name | lower }}
{{ .Values.name | upper }}
{{ .Values.name | quote }}           # 따옴표로 감싸기
{{ .Values.name | trim }}

# 타입 변환
{{ int .Values.replicas }}
{{ toString .Values.port }}
```

---

## StatefulSet 템플릿 분석

### _statefulset.go.tpl 핵심 구조

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {{ include "redpanda.fullname" . }}
  labels:
    {{- include "redpanda.labels" . | nindent 4 }}
spec:
  serviceName: {{ include "redpanda.fullname" . }}
  replicas: {{ .Values.statefulset.replicas }}
  selector:
    matchLabels:
      {{- include "redpanda.selectorLabels" . | nindent 6 }}
  template:
    spec:
      containers:
        - name: redpanda
          image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
          ports:
            - name: kafka
              containerPort: {{ .Values.listeners.kafka.port }}
          resources:
            limits:
              cpu: {{ .Values.resources.cpu.cores }}
              memory: {{ .Values.resources.memory.container.max }}
          volumeMounts:
            - name: datadir
              mountPath: /var/lib/redpanda/data
  volumeClaimTemplates:
    - metadata:
        name: datadir
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: {{ .Values.storage.persistentVolume.size }}
```

---

## ConfigMap 템플릿 분석

### redpanda.yaml 생성

```yaml
{{- define "redpanda.configmap" -}}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "redpanda.fullname" . }}-config
data:
  redpanda.yaml: |
    redpanda:
      data_directory: /var/lib/redpanda/data
      kafka_api:
        - address: 0.0.0.0
          port: {{ .Values.listeners.kafka.port }}
      admin:
        - address: 0.0.0.0
          port: {{ .Values.listeners.admin.port }}
{{- end -}}
```

---

## 실습

```bash
cd /Users/simbohyeon/okestro/tps_manifest/helm-charts/redpanda

# 전체 템플릿 렌더링
helm template test . -f values-dev.yaml

# 특정 리소스만 확인
helm template test . -f values-dev.yaml | grep -A 50 "kind: StatefulSet"

# 디버그 모드 (변수 값 확인)
helm template test . -f values-dev.yaml --debug

# 특정 템플릿 파일 내용 확인
cat templates/_statefulset.go.tpl | head -100
```

---

## 참고

- [Helm Template Functions](https://helm.sh/docs/chart_template_guide/function_list/)
- [Go Template Package](https://pkg.go.dev/text/template)
