---
title: jenkins-agent-strategy
tags: []
status: draft
related: []
updated: 2026-04-19
---

# Jenkins Agent 전략: 고정 Pod vs 동적 Pod
---
> GCP 3노드 K8s 클러스터(4vCPU/8GB × 3)에서 Jenkins Master 1 + Agent 2 구성을 고정 Pod와 동적 Pod 중 어떤 방식으로 운영할지 결정하기 위한 비교 분석이다.

## 환경 전제

현재 클러스터에는 Jenkins 외에도 여러 워크로드가 함께 돌아간다:

- Redpanda(메시징), PostgreSQL(DB)
- Grafana, Prometheus, Loki, Tempo, Alloy(모니터링)
- ArgoCD(배포), nginx-ingress
- Spring Boot, React(앱 워크로드)

총 리소스는 12vCPU/24GB이고, 위 워크로드가 상당 부분을 점유하고 있다. 빌드 빈도는 하루 수 회 수준이며, 동시 빌드가 발생할 가능성은 낮다.

## 고정 Pod 방식

Jenkins Agent Pod 2개를 Deployment 또는 StatefulSet으로 상시 배포하고, Jenkins가 JNLP로 연결하여 빌드를 실행하는 방식이다.

### 동작 흐름

빌드가 없어도 Agent Pod 2개가 항상 떠 있다. Jenkins Controller가 각 Agent에 라벨 기반으로 작업을 분배한다. Pod가 죽으면 K8s가 자동으로 재생성한다.

### 장점

즉시 빌드가 가능하다는 점이 가장 큰 장점이다. Pod 생성 대기 시간(보통 10~30초)이 없으므로 빌드 트리거 후 곧바로 실행된다. 설정이 단순하고, Kubernetes Plugin 없이 기본 Jenkins JNLP Agent만으로 구성할 수 있다. Agent의 로컬 캐시(Gradle `.gradle/`, npm `node_modules/`)가 PVC에 유지되므로 빌드 속도가 일정하다.

### 단점

빌드가 없는 시간에도 리소스를 점유한다. Agent 하나에 CPU 500m/MEM 1GB를 할당하면 2개 기준 CPU 1코어/MEM 2GB가 상시 소비된다. 12vCPU/24GB 클러스터에서 8%의 CPU와 8%의 메모리를 빌드 외 시간에 낭비하는 셈이다. GCP 크레딧 기반 운영에서는 다른 워크로드의 가용 리소스가 줄어드는 직접적 영향이 있다.

## 동적 Pod 방식

Jenkins Kubernetes Plugin을 사용하여 빌드 요청 시에만 Agent Pod를 생성하고, 빌드 완료 후 삭제하는 방식이다.

### 동작 흐름

Jenkinsfile에서 `podTemplate`을 정의하면, 빌드 트리거 시 K8s API를 통해 Pod가 생성된다. Pod 안에 필요한 컨테이너(gradle, docker, node 등)를 sidecar로 구성할 수 있다. 빌드가 끝나면 Pod가 자동 삭제된다.

### 장점

빌드가 없으면 리소스 소비가 0이다. 하루 수 회 빌드하는 현재 패턴에서는 Agent가 실제로 떠 있는 시간이 하루 30분~1시간 정도에 불과하므로, 고정 방식 대비 리소스를 90% 이상 절약할 수 있다.

파이프라인별로 다른 Agent 스펙을 정의할 수 있다는 점도 유용하다. Gradle 빌드에는 CPU 1코어/MEM 2GB, 프론트엔드 빌드에는 CPU 500m/MEM 1GB처럼 작업 특성에 맞는 리소스를 할당할 수 있다. 고정 방식에서는 가장 무거운 작업 기준으로 Agent를 프로비저닝해야 한다.

### 단점

Pod 생성에 10~30초가 소요된다. 이미지가 노드에 캐시되어 있으면 10초 이내지만, 첫 실행이나 이미지 업데이트 시에는 pull 시간이 추가된다.

빌드 캐시가 Pod와 함께 사라진다. Gradle이나 npm의 의존성을 매번 다운로드하면 빌드 시간이 길어진다. PVC를 마운트하여 캐시를 유지하면 해결 가능하지만, 설정이 추가된다.

Kubernetes Plugin 설정과 `podTemplate` 작성이 필요하므로 초기 구성이 고정 방식보다 복잡하다.

## 비교

| 기준 | 고정 Pod | 동적 Pod |
|------|----------|----------|
| 빌드 시작 지연 | 없음 | 10~30초 |
| 유휴 시 리소스 | CPU 1코어/MEM 2GB 상시 | 0 |
| 빌드 캐시 | 자동 유지 | PVC 마운트 필요 |
| 초기 설정 난이도 | 낮음 (JNLP) | 중간 (K8s Plugin + podTemplate) |
| Agent 스펙 유연성 | 고정 | 파이프라인별 커스텀 |
| 장애 복원 | K8s 자동 재생성 | 빌드 시 새 Pod 생성 |
| 동시 빌드 확장 | 2개 고정 | 리소스 한도 내 자유 |

## 판단

현재 환경에서는 **동적 Pod 방식이 더 적합하다**. 이유는 세 가지다.

첫째, 리소스 여유가 부족하다. 12vCPU/24GB에 Redpanda, 모니터링 스택, 앱 워크로드가 함께 돌아가므로, 빌드 외 시간에 1코어/2GB를 상시 점유하는 것은 부담이 크다.

둘째, 빌드 빈도가 낮다. 하루 수 회 수준이면 Agent가 실제로 필요한 시간은 하루 1시간 미만이다. 23시간을 유휴 상태로 리소스를 잡아두는 것은 GCP 크레딧 관점에서도 비효율적이다.

셋째, 10~30초의 Pod 생성 지연은 CI/CD 파이프라인에서 체감 차이가 미미하다. Gradle 빌드 자체가 수 분 걸리므로 30초 추가는 전체 파이프라인 시간의 5~10%에 불과하다.

캐시 문제는 PVC를 마운트하여 `.gradle/caches`와 `node_modules`를 유지하면 해결된다. `podTemplate`에 `volumeMount`를 추가하는 작업이 한 번 필요하지만, 이후에는 고정 방식과 동일한 빌드 속도를 얻을 수 있다.
