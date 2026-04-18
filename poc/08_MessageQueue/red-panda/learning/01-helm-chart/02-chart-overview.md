# 01. Chart Overview

Helm 차트 기본 구조와 메타데이터 분석

---

## 차트 구조

```
/Users/simbohyeon/okestro/tps_manifest/helm-charts/redpanda/
├── Chart.yaml          # 차트 메타데이터
├── Chart.lock          # 의존성 잠금 파일
├── values.yaml         # 기본 설정값 (48KB)
├── values-dev.yaml     # 개발환경 오버라이드
├── values.schema.json  # 값 스키마 검증 (883KB)
├── .helmignore         # 패키징 제외 파일
├── README.md           # 차트 문서
├── templates/          # Kubernetes 매니페스트 템플릿
│   ├── _*.go.tpl       # 헬퍼 템플릿 (Go 함수)
│   └── entry-point.yaml # 진입점
├── charts/             # 서브차트
│   └── console/        # Redpanda Console
└── files/              # 추가 설정 파일
```

---

## Chart.yaml 분석

```yaml
apiVersion: v2                    # Helm 3 API 버전
appVersion: v25.3.1               # Redpanda 애플리케이션 버전
name: redpanda
version: 25.3.1                   # Helm 차트 버전
description: Redpanda is the real-time engine for modern apps.
kubeVersion: '>= 1.25.0-0'        # 최소 K8s 버전 요구

dependencies:
- name: console                   # Redpanda Console UI
  condition: console.enabled      # values.yaml로 활성화 제어
  repository: file://../../console/chart
  version: '>=3.3.0-0'

maintainers:
- name: redpanda-data
  url: https://github.com/orgs/redpanda-data/people
```

### 핵심 개념

| 필드 | 설명 |
|------|------|
| `apiVersion: v2` | Helm 3 차트 (v1은 Helm 2용) |
| `appVersion` | 배포되는 애플리케이션 버전 |
| `version` | 차트 자체의 버전 (SemVer) |
| `kubeVersion` | 지원하는 Kubernetes 버전 범위 |
| `dependencies` | 서브차트 의존성 |

---

## 의존성: Redpanda Console

```yaml
dependencies:
- name: console
  condition: console.enabled
```

### 활성화 방법

```yaml
# values.yaml
console:
  enabled: true  # Console UI 배포
```

### 의존성 관리 명령어

```bash
# 의존성 다운로드
helm dependency update

# 의존성 목록 확인
helm dependency list

# 결과
NAME    VERSION   REPOSITORY                    STATUS
console >=3.3.0-0 file://../../console/chart    ok
```

---

## values.schema.json

values.yaml의 스키마 검증용 JSON Schema (883KB)

```bash
# 값 검증 (lint 시 자동 적용)
helm lint ./redpanda -f values-dev.yaml

# 스키마 확인
cat values.schema.json | jq '.properties | keys'
```

### 주요 검증 항목

- 필수 필드 존재 여부
- 타입 검증 (string, number, boolean)
- enum 값 검증
- 범위 검증 (minimum, maximum)

---

## 실습

```bash
cd /Users/simbohyeon/okestro/tps_manifest/helm-charts/redpanda

# 차트 정보 확인
helm show chart .

# 전체 값 확인
helm show values . | head -100

# 의존성 확인
helm dependency list

# 차트 검증
helm lint . -f values-dev.yaml
```

---

## 참고

- [Helm Chart.yaml 구조](https://helm.sh/docs/topics/charts/#the-chartyaml-file)
- [Helm Dependencies](https://helm.sh/docs/helm/helm_dependency/)
