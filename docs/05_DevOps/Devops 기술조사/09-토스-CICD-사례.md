# 토스(Toss) CI/CD 및 DevOps 사례

> 작성일: 2025-01-14
> 출처: 토스 기술 블로그 (toss.tech)
> 목적: 토스의 CDC 파이프라인, 배포 파이프라인 운영 사례 정리

---

## 1. 토스 DevOps 조직 구조

### 1.1 역할 분담

| 조직 | 역할 |
|-----|------|
| **SE (System Engineer)** | 하드웨어, 커널 관리 |
| **DevOps** | 소프트웨어 영역 운영, 자동화 플랫폼 구축 |
| **SRE** | 서비스 이슈/장애 근본 원인 분석, 문제 정의 |

### 1.2 인프라 환경

- **운영 환경**: IDC (자체 데이터센터) + AWS
- **컨테이너**: 여러 개의 Kubernetes 클러스터
- **Service Mesh**: Istio
- **모니터링**: Prometheus, Thanos, Grafana

---

## 2. 대규모 CDC Pipeline 운영 (토스증권)

> 출처: [대규모 CDC Pipeline 운영을 위한 Debezium 개선 여정](https://toss.tech/article/cdc_pipeline)
> 저자: 김용우 (토스증권 Data Engineer)
> 발행일: 2024년 7월 18일

### 2.1 CDC 활용 현황

토스증권에서는 다양한 분야에서 CDC(Change Data Capture)를 활용:

| 활용 분야 | 목적 |
|----------|------|
| **분석계 데이터** | Data Analyst용 실시간 데이터 |
| **학습 데이터** | ML Engineer용 모델 학습 데이터 |
| **서비스 데이터** | 토스 앱 서비스용 실시간 동기화 |

**핵심 기술**: Debezium (오픈소스 CDC 플랫폼)

### 2.2 기존 문제점

```
┌─────────────────────────────────────────────────────────────────┐
│                    CDC Pipeline 운영 문제점                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 파이프라인 상태 파악 불가                                     │
│     - 문제 발생 시 짐작만 가능                                    │
│     - 데이터 사용자 보고 후에야 문제 인지                          │
│                                                                 │
│  2. Snapshot 처리의 어려움                                       │
│     - 대용량 테이블 초기 생성에 11-12시간 소요                     │
│     - Single Thread 처리로 인한 병목                              │
│     - 장애 시 복구 시간 과다                                      │
│                                                                 │
│  3. 확장의 부담                                                  │
│     - 새 Pipeline 추가가 운영 짐으로 작용                         │
│     - CDC 활용 확대 꺼려짐                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 개선 방향

**핵심 지표: Source-to-Target Latency**

원천 데이터베이스 → Target System까지 Event 전달 시간

**개선 영역**:
1. Connector 개선
2. Debezium 소스 코드 수정
3. 운영 방식 변경

### 2.4 CDC 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    CDC Pipeline 아키텍처                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                               │
│  │   Source DB  │  (MySQL, PostgreSQL 등)                       │
│  │  (원천 DB)   │                                               │
│  └──────┬───────┘                                               │
│         │ Binary Log / WAL                                      │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │   Debezium   │  Change Data Capture                          │
│  │  (CDC Tool)  │                                               │
│  └──────┬───────┘                                               │
│         │ CDC Events                                            │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │    Kafka     │  Event Streaming                              │
│  │   Connect    │                                               │
│  └──────┬───────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │ Target System│  (Data Warehouse, 분석 시스템 등)              │
│  └──────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.5 운영 지표

CDC Pipeline 운영을 위한 4가지 핵심 지표:

| 지표 | 설명 |
|-----|------|
| **Source-to-Target Latency** | 원천 DB → Target 시스템 도달 시간 |
| **처리량 (Throughput)** | 단위 시간당 처리 이벤트 수 |
| **에러율** | 실패한 이벤트 비율 |
| **Lag** | 처리 지연 정도 |

### 2.6 성과

- CDC Pipeline 성능 및 데이터 처리 속도/양 파악 가능
- 새로운 Pipeline 추가에 문제없이 대응
- 더 많은 실시간 CDC Pipeline 관리 기반 마련

---

## 3. 배포 Pipeline 운영 (토스뱅크)

> 출처: [유연하고 안전하게 배포 Pipeline 운영하기](https://toss.tech/article/slash23-devops)
> 저자: 김동석 (토스뱅크 DevOps Engineer)
> 발행일: SLASH 23 (2023년)

### 3.1 규모

| 구분 | 개수 |
|-----|------|
| 서비스 빌드/배포 Pipeline | 281개 |
| 작업 자동화 Pipeline | 76개 |
| 기타 Pipeline | 47개 |
| **총합** | **400개 이상** |

**배포 빈도**: 하루 수십~수백 번 (MSA 환경)

### 3.2 기술 스택

| 구분 | 기술 |
|-----|------|
| **파이프라인 도구** | GoCD |
| **IaC** | YAML + Helm Template |
| **버전 관리** | Git |
| **CI 도구** | GitHub Actions |

### 3.3 문제점과 해결책

#### 문제 1: 가시성 부족

**문제**: 웹 UI에서 수백 개 파이프라인 관리 어려움

**해결**: Pipeline as Code
- YAML 파일 기반 설정
- gocd-yaml-config-plugin 도입
- 모든 Pipeline 설정이 한 폴더에서 확인 가능

```yaml
# Pipeline as Code 예시
pipelines:
  service-a-deploy:
    group: production
    materials:
      repo:
        git: https://github.com/org/service-a.git
        branch: main
    stages:
      - build:
          jobs:
            build:
              tasks:
                - exec:
                    command: ./gradlew build
```

#### 문제 2: 생산성 저하

**문제**: 복사-붙여넣기로 인한 오류 발생

**해결**: GoCD Template
- 공통 설정을 템플릿으로 추출
- 변수로 개별 파이프라인 설정

```yaml
# Template 활용 예시
pipelines:
  service-a-deploy:
    template: standard-deploy  # 공통 템플릿 참조
    parameters:
      SERVICE_NAME: service-a
      REPLICA_COUNT: 3
```

#### 문제 3: 확장성 제약

**문제**: 정적 YAML의 한계

**해결**: Helm Template 도입
- 프로그래밍 가능한 템플릿
- 조건문 활용으로 테스트 검증
- 다른 도구 전환 시 Values 파일 재사용

```yaml
# Helm Template 활용
{{- range .Values.services }}
pipelines:
  {{ .name }}-deploy:
    {{- if .isTest }}
    group: test
    {{- else }}
    group: production
    {{- end }}
    stages:
      - build:
          jobs:
            {{- include "common.buildJob" . | nindent 12 }}
{{- end }}
```

#### 문제 4: 복잡성으로 인한 오류

**문제**: 설정 변경 시 의도하지 않은 영향

**해결**: CI 도입
- GitHub Actions 기반 자동 검증
- 의도하지 않은 변경 감지 및 차단
- Kubernetes Object도 동일 방식 적용

```yaml
# GitHub Actions CI 예시
name: Pipeline Validation

on:
  pull_request:
    paths:
      - 'pipelines/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Render templates
        run: helm template ./pipelines

      - name: Validate YAML
        run: yamllint ./pipelines

      - name: Check diff
        run: |
          # 의도하지 않은 변경 감지
          ./scripts/check-pipeline-diff.sh
```

### 3.4 개선 결과

```
┌─────────────────────────────────────────────────────────────────┐
│              Pipeline 운영 성숙도 진화                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Level 1: Web UI 기반                                           │
│           ↓                                                     │
│  Level 2: Pipeline as Code (YAML)                               │
│           ↓ + Versionable                                       │
│  Level 3: GoCD Template                                         │
│           ↓ + Reusable                                          │
│  Level 4: Helm Template                                         │
│           ↓ + Programmable                                      │
│  Level 5: CI 검증 추가                                          │
│           → Testable                                            │
│                                                                 │
│  결과: "Code처럼 유연하고 안전하게 Pipeline 운영"                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.5 핵심 원칙

> "Pipeline 설정을 중앙화하는 것이 효율적이라고 판단하였고,
> 여러 스쿼드가 사용하는 Pipeline 설정을 한 곳에 모아두고
> DevOps Engineer가 주도적으로 운영하고 있습니다."

---

## 4. 프론트엔드 모노레포 파이프라인 최적화 (토스)

> 출처: [200여개 서비스 모노레포의 파이프라인 최적화](https://toss.tech/article/monorepo-pipeline)
> 소속: 토스 프론트엔드 챕터

### 4.1 모노레포 규모

| 항목 | 수치 |
|-----|------|
| **서비스 수** | 200개 이상 |
| **기여자 수** | 50~60명 |
| **일 평균 머지 PR** | 60개 이상 |
| **저장소 크기** | 40GB 초과 |
| **목표 배포 시간** | 코드 푸시 → 배포 **5분** |

### 4.2 문제점

```
┌─────────────────────────────────────────────────────────────────┐
│                    모노레포 빌드 시간 문제                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  빌드 계산:                                                      │
│  (변경된 서비스 수) × (환경 수) × (빌드 시간)                     │
│                                                                 │
│  예시:                                                          │
│  3개 서비스 × 3개 환경(dev/staging/live) × 5분 = 45분           │
│                                                                 │
│  순차 빌드 시 총 45분 소요 → 개발 생산성 저하                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 최적화 기법

#### 기법 1: CI/CD 병렬화 (5배 개선)

**문제**: 순차 빌드로 인한 긴 대기 시간

**해결**: CircleCI 동적 설정으로 각 파이프라인을 독립된 컴퓨팅 환경에서 병렬 실행

```
Before: 3서비스 × 3환경 = 9빌드 → 순차 45분
After:  1분(트리거) + 5분(병렬) = 약 6분

서비스 수와 무관하게 약 6분 내 완료!
```

**핵심 포인트**: "각 파이프라인을 독립된 컴퓨팅 환경에서 수행하는 것이 가장 중요"

#### 기법 2: Daily Docker Base Image (Job당 36분 이상 개선)

**문제**: 40GB 레포를 매번 checkout하면서 타임아웃 발생

**해결**: 매일 오전 7시 모노레포를 사전 복제한 도커 이미지 생성

```
┌─────────────────────────────────────────────────────────────────┐
│                Daily Docker Base Image 전략                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Daily Build Job - 오전 7시]                                    │
│  ┌────────────────────────────────────────┐                     │
│  │ git clone --depth 50                   │                     │
│  │ git fetch --depth 1000                 │                     │
│  │ yarn install                           │                     │
│  │ → Docker Image로 저장 (AWS ECR)         │                     │
│  └────────────────────────────────────────┘                     │
│                                                                 │
│  [일반 CI Job]                                                   │
│  ┌────────────────────────────────────────┐                     │
│  │ Daily Image 기반으로 시작               │                     │
│  │ git fetch (변경분만) → 22초             │                     │
│  │ vs 전체 checkout → 36분                │                     │
│  └────────────────────────────────────────┘                     │
│                                                                 │
│  절감 효과: Job당 약 36분 절감                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 기법 3: SSR Standalone Docker Image (20배 개선)

**문제**: Next.js의 `output: 'standalone'` 기능이 `node_modules` 의존

**해결**: Yarn PnP API 활용해 런타임에 필요한 파일만 추출 후 zip 번들화

| 항목 | Before | After | 개선 |
|-----|--------|-------|------|
| Docker 이미지 크기 | 4GB | 200MB | **20배** |
| K8s Pod 시작 시간 | - | 대폭 단축 | - |
| 배포 요구사항 | git, yarn 필요 | 불필요 | 간소화 |

### 4.4 기술 스택

| 구분 | 기술 |
|-----|------|
| **CI/CD** | CircleCI (동적 설정) |
| **패키지 관리** | Yarn PnP |
| **컨테이너 레지스트리** | AWS ECR |
| **오케스트레이션** | Kubernetes |
| **프레임워크** | Next.js |

### 4.5 성과 요약

| 최적화 방법 | 개선 효과 |
|-----------|----------|
| CI/CD 병렬화 | 배포 시간 **5배** 개선 |
| Daily Docker Base Image | Job당 **36분 이상** 절감 |
| SSR Standalone | Pod 시작 **20배** 개선 |

### 4.6 모노레포의 장점

토스가 모노레포를 선택한 이유:

1. **빠른 서비스 생성**: 레포 생성/CI/CD 설정 없이 스캐폴딩 한 번으로 완료
2. **쉬운 코드 공유**: 동적으로 패키지 연결, NPM Publish 불필요
3. **일관된 개발 경험**: 동일한 도구와 설정 공유

---

## 5. 토스 DevOps Best Practices 정리

### 5.1 Pipeline as Code 원칙

| 특성 | 설명 | 도구/방법 |
|-----|------|----------|
| **Versionable** | Git으로 버전 관리 | Git + YAML |
| **Reusable** | 템플릿으로 재사용 | GoCD Template |
| **Programmable** | 조건부 로직 가능 | Helm Template |
| **Testable** | 자동 검증 가능 | GitHub Actions |

### 5.2 CDC Pipeline 운영 원칙

| 원칙 | 설명 |
|-----|------|
| **지표 기반 운영** | Source-to-Target Latency 등 핵심 지표 모니터링 |
| **가시성 확보** | 파이프라인 상태를 명확히 파악 |
| **확장성 준비** | 새 파이프라인 추가에 유연하게 대응 |
| **소스 코드 수정** | 필요 시 오픈소스(Debezium) 직접 개선 |

### 5.3 대규모 운영 교훈

1. **중앙화된 관리**: 분산된 설정을 한 곳에 모아 관리
2. **자동화된 검증**: CI를 통한 사전 오류 방지
3. **점진적 개선**: 단계별 성숙도 향상
4. **측정 가능한 지표**: 데이터 기반 의사결정

---

## 6. 관련 SLASH 세션

### SLASH 23
- "고객 불안을 0으로 만드는 토스의 Istio Zero Trust" (성준영, 한경수)

### SLASH 22
- "토스팀 인프라 자동화의 시작" (김정남)
- "잃어버린 개발자의 시간을 찾아서: 매일 하루를 아끼는 DevOps 이야기" (박서진)
- "어떻게 안정적인 서비스를 빠르게, 자주 출시할 것인가?" (하태호)

### SLASH 21
- "토스의 서버 인프라 모니터링"

---

## 7. 참고 자료

- [대규모 CDC Pipeline 운영을 위한 Debezium 개선 여정 (토스 테크)](https://toss.tech/article/cdc_pipeline)
- [유연하고 안전하게 배포 Pipeline 운영하기 (토스 테크)](https://toss.tech/article/slash23-devops)
- [200여개 서비스 모노레포의 파이프라인 최적화 (토스 테크)](https://toss.tech/article/monorepo-pipeline)
- [토스 개발자 컨퍼런스 SLASH 23](https://toss.im/slash-23)
- [Debezium Architecture Documentation](https://debezium.io/documentation/reference/stable/architecture.html)
- [Implement CDC & Streaming Analytics Using Kafka & Debezium (Confluent)](https://www.confluent.io/blog/cdc-and-streaming-analytics-using-debezium-kafka/)
