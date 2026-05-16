<!-- migrated: write/09_cloud/kubernetes/deepdive/06-01.Operator 패턴 점검.md (2026-04-19) -->

# Ch07: Operator 패턴 - 점검 질문

## 질문 1: CRD와 ConfigMap의 차이 - 왜 CRD를 만들어야 하는가?

### 핵심 포인트

- **ConfigMap은 데이터 저장소**, CRD는 **API 확장**: ConfigMap은 key-value 데이터를 저장하는 용도이고, CRD는 Kubernetes API에 새로운 리소스 타입을 추가하는 것이다. `kubectl get configmap`은 범용 조회지만, `kubectl get postgrescluster`는 타입별 조회가 가능하다.

- **스키마 검증 유무**: ConfigMap은 어떤 데이터든 자유롭게 넣을 수 있다 (검증 없음). CRD는 OpenAPI v3 스키마로 필드 타입, 필수 여부, 범위를 강제한다. 잘못된 값을 넣으면 API Server가 거부한다.

- **버전 관리**: ConfigMap은 버전 개념이 없다. CRD는 v1alpha1, v1beta1, v1 등으로 API 버전을 관리하고, 버전 간 변환(conversion webhook)도 지원한다.

- **RBAC 통합**: ConfigMap은 "모든 ConfigMap"에 대한 권한만 설정 가능하다. CRD는 리소스별로 세밀한 권한 부여가 가능하다 (예: `postgrescluster`에는 read-only, `rediscluster`에는 full access).

- **Controller 연동**: ConfigMap을 사용하려면 Controller가 데이터를 직접 파싱해야 한다. CRD는 API Server가 watch 이벤트를 제공하고, typed client를 생성할 수 있어 개발이 쉽다.

- **Admission Webhook 지원**: CRD는 생성/수정 시 validating/mutating webhook을 적용할 수 있다 (예: `spec.replicas`가 홀수인지 검증, 기본값 자동 추가). ConfigMap은 불가능하다.

### 심화 질문

- ConfigMap으로도 "애플리케이션 설정"을 관리할 수 있는데, 왜 Operator는 CRD를 사용하는가? (힌트: 운영 작업은 "설정"이 아니라 "리소스 생명주기 관리"이다)
- CRD에 status subresource를 추가하는 이유는? (힌트: `spec`은 desired state, `status`는 actual state - Reconcile 결과 저장)
- CRD를 삭제하면 해당 타입의 모든 Custom Resource도 삭제되는가? (힌트: finalizer가 없으면 즉시 삭제, 있으면 Controller가 정리 후 삭제)

---

## 질문 2: Reconciliation Loop의 동작 원리 - Watch → Queue → Reconcile

### 핵심 포인트

- **Watch 메커니즘**: Controller는 API Server에 HTTP long-polling 또는 WebSocket으로 연결하고, 특정 리소스(예: PostgresCluster)의 변경 이벤트를 실시간으로 받는다. API Server는 etcd의 변경을 감지하면 즉시 이벤트를 보낸다.

- **Workqueue의 역할**: 이벤트를 바로 처리하지 않고 큐에 넣는 이유는 **동시성 제어**와 **재시도**이다. 여러 리소스가 동시에 변경되어도 순차 처리하고, 에러 발생 시 exponential backoff로 재시도한다.

- **Reconcile 로직**: 큐에서 하나씩 꺼내서 처리한다. etcd에서 desired state를 읽고(`spec.replicas: 3`), 클러스터에서 actual state를 확인(`현재 Pod 2개`), 차이를 해소한다(`Pod 1개 추가`). 멱등성이 핵심이다.

- **재시도 전략**: 네트워크 오류, API rate limit, 일시적 장애 등으로 실패하면 5초 → 10초 → 20초 → 40초 간격으로 재시도한다. 영구 오류(리소스 삭제됨)는 재시도하지 않는다.

- **Edge-driven vs Level-driven**: Kubernetes Controller는 **Level-driven**이다. "Pod가 추가되었다"(edge)가 아니라 "현재 총 몇 개인가"(level)를 확인한다. 이벤트를 놓쳐도 다음 reconcile에서 상태를 맞춘다.

- **Requeue 조건**: Reconcile 함수는 `(ctrl.Result, error)`를 반환한다. `error != nil`이면 자동 재시도, `Result.Requeue = true`이면 명시적 재시도, `Result.RequeueAfter = 5분`이면 일정 시간 후 재확인 (예: 백업 완료 대기).

### 심화 질문

- 동일한 리소스에 대해 여러 이벤트가 빠르게 발생하면 Workqueue는 어떻게 처리하는가? (힌트: deduplication - 중복 이벤트는 하나로 합쳐진다)
- Reconcile 중에 리소스가 삭제되면 어떻게 되는가? (힌트: `client.IgnoreNotFound(err)`로 처리, 삭제된 리소스는 무시)
- 여러 Worker goroutine이 동시에 Reconcile을 실행하는데, 같은 리소스를 두 번 처리할 위험은 없는가? (힌트: Workqueue가 동일 key는 한 번만 처리하도록 보장)

---

## 질문 3: Operator 성숙도 Level 1~5 - 각 단계에서 어떤 자동화가 추가되는가?

### 핵심 포인트

- **Level 1 (Basic Install)**: CRD를 적용하면 Controller가 기본 리소스(Pod, Service)를 생성한다. 사용자는 `spec.replicas`, `spec.image` 정도만 설정하고, 나머지는 수동으로 관리한다. Helm Chart를 CRD로 감싼 형태가 대표적이다.

- **Level 2 (Seamless Upgrades)**: `spec.version: "12.0"` → `"13.0"`으로 변경하면 Controller가 롤링 업데이트를 자동 실행한다. 데이터 마이그레이션 스크립트가 필요한 경우 Job을 자동 생성하여 실행한다. 백업/복원은 여전히 수동이다.

- **Level 3 (Full Lifecycle)**: 백업, 복원, 모니터링이 자동화된다. `spec.backup.schedule: "0 2 * * *"`로 CronJob 자동 생성, `spec.restore.from: backup-20230601`로 복원 요청 시 자동 실행. Prometheus ServiceMonitor도 자동 생성하여 메트릭 수집을 자동 설정한다.

- **Level 4 (Deep Insights)**: Prometheus 메트릭을 분석하여 이상 징후를 탐지한다. 예: 쿼리 응답 시간이 평소보다 3배 느리면 알림 발송, 디스크 사용률 80% 도달 시 경고. 로그를 파싱하여 에러 패턴을 인식하고 Slack/PagerDuty로 알림을 보낸다.

- **Level 5 (Auto Pilot)**: 완전 자율 운영. Primary DB 장애 시 자동으로 Standby를 승격시킨다. 디스크 부족 시 PVC 크기를 자동 확장한다. 트래픽 증가를 감지하면 레플리카를 자동 추가한다. 사람의 개입 없이 24/7 운영이 가능하다.

- **현실적 목표**: 대부분의 Operator는 Level 2~3에 머문다. Level 5는 비즈니스 로직에 따라 판단이 달라지고 (자동 스케일링 시 비용 증가), 예상치 못한 동작의 위험이 있어 신중하게 접근한다.

### 심화 질문

- Level 3과 Level 4의 가장 큰 차이는 무엇인가? (힌트: Level 3은 "사용자가 요청한 작업 실행", Level 4는 "시스템이 스스로 문제 감지")
- Level 5에서 자동 Failover를 구현하려면 Controller가 무엇을 모니터링해야 하는가? (힌트: Pod liveness probe, 네트워크 파티션, quorum 상태)
- Operator 성숙도가 높을수록 항상 좋은가? (힌트: 복잡도 증가, 예측 불가능성, 디버깅 난이도 상승)

---

## 질문 4: Operator SDK vs Kubebuilder - 차이와 선택 기준

### 핵심 포인트

- **공통점**: 둘 다 Controller Runtime 라이브러리를 사용한다. CRD 생성, Reconcile 로직, RBAC 설정, Deployment 매니페스트 생성 등 핵심 기능은 동일하다. 프로젝트 구조도 거의 같다 (`api/`, `controllers/`, `config/`).

- **Operator SDK의 장점**: Red Hat이 유지 보수하고, **3가지 개발 방식**(Go, Ansible, Helm)을 제공한다. 기존 Ansible playbook이나 Helm Chart가 있으면 빠르게 Operator로 전환할 수 있다. OLM 통합이 더 긴밀하다 (CSV 자동 생성).

- **Kubebuilder의 장점**: Kubernetes SIG가 유지 보수하고, **순수 Go 개발**에 특화되어 있다. 코드가 더 간결하고, 최신 Controller Runtime 기능을 빠르게 반영한다. 공식 문서가 더 상세하다.

- **Ansible 기반 Operator**: 기존 Ansible로 VM을 관리하던 팀이 K8s로 전환할 때 유용하다. playbook을 재사용할 수 있지만, 복잡한 로직(conditional reconcile, status update)은 어렵다. Level 1~2 Operator에 적합하다.

- **Helm 기반 Operator**: Helm Chart를 CRD로 감싸는 방식이다. 단순 배포만 자동화하고, Day-2 Operation은 지원하지 않는다. Level 1 Operator에만 적합하다.

- **선택 기준**: 기존 Ansible/Helm 자산이 많으면 Operator SDK, 순수 Go 개발이면 Kubebuilder (약간 더 가볍고 최신). 복잡한 비즈니스 로직이 필요하면 Go 기반을 사용해야 한다.

### 심화 질문

- Ansible 기반 Operator의 한계는 무엇인가? (힌트: Ansible은 상태를 저장하지 않는다 - CR의 status subresource 업데이트가 어렵다)
- Helm 기반 Operator로 백업 자동화를 구현할 수 있는가? (힌트: 불가능 - Helm은 배포만 담당, Reconcile 로직을 추가할 수 없다)
- Operator SDK와 Kubebuilder를 동시에 사용할 수 있는가? (힌트: 가능 - 둘 다 Controller Runtime 기반이라 코드 호환됨)

---

## 질문 5: Operator가 해결하는 Day-2 Operation 예시

### 핵심 포인트

- **백업 자동화**: CronJob을 자동 생성하여 매일 새벽 2시에 pg_dump 실행, S3에 업로드, 7일 이상 데이터 삭제. `spec.backup.schedule`, `spec.backup.retention`으로 선언하면 Controller가 CronJob + PVC + Secret(S3 자격증명) 생성.

- **장애 복구 (Failover)**: Primary DB Pod가 liveness probe 실패 시, Controller가 자동으로 Standby를 승격시킨다. Service의 selector를 변경하여 트래픽을 새 Primary로 라우팅한다. 기존 Primary는 복구 후 Standby로 재구성한다.

- **버전 업그레이드**: `spec.version: "9.6"` → `"12.0"`으로 변경 시, Controller가 다음을 수행한다: (1) 백업 실행, (2) 데이터 마이그레이션 Job 실행, (3) 새 버전 이미지로 Pod 재시작, (4) 헬스 체크 확인.

- **스케일링 자동화**: `spec.replicas: 3` → `5`로 변경하면 StatefulSet이 자동으로 Pod 2개를 추가한다. Controller는 새 Pod가 Ready 상태가 될 때까지 대기하고, Replication 설정을 자동 업데이트한다.

- **인증서 갱신**: Cert Manager Operator는 TLS 인증서의 만료일을 모니터링하고, 30일 전에 Let's Encrypt에 자동으로 갱신 요청을 보낸다. 새 인증서를 Secret에 저장하고, Pod를 재시작하여 적용한다.

- **모니터링 통합**: Prometheus Operator의 ServiceMonitor CRD를 자동 생성하여 애플리케이션 메트릭을 수집한다. Grafana 대시보드도 ConfigMap으로 자동 생성할 수 있다.

### 심화 질문

- 백업 실패 시 Operator는 어떻게 재시도하는가? (힌트: CronJob의 `backoffLimit`, Controller가 status를 모니터링하여 알림)
- Failover 과정에서 데이터 손실을 방지하려면 무엇을 확인해야 하는가? (힌트: Synchronous replication, quorum 상태, WAL 적용 완료)
- 버전 업그레이드 중 문제가 발생하면 어떻게 롤백하는가? (힌트: 백업 복원, 이전 버전 이미지로 StatefulSet 업데이트)

---

## 질문 6: OLM 없이 Operator를 설치하는 방법과 OLM의 장점

### 핵심 포인트

- **수동 설치 방법**: (1) CRD YAML을 `kubectl apply`, (2) Operator Controller의 Deployment YAML 적용, (3) RBAC (ServiceAccount, Role, RoleBinding) 생성. 총 5~10개의 YAML 파일을 순서대로 적용해야 한다. 예: `kubectl apply -f crd.yaml -f rbac.yaml -f deployment.yaml`.

- **OLM 설치 방법**: Subscription 리소스 1개만 생성하면 된다. OLM이 CatalogSource에서 CSV(ClusterServiceVersion)를 가져와 CRD, Deployment, RBAC을 자동 생성한다. 예: `kubectl apply -f subscription.yaml`.

- **업그레이드 관리**: 수동 설치는 CRD 변경 → Controller 재배포 순서를 사람이 관리해야 한다. OLM은 CSV의 `replaces` 필드를 보고 자동으로 순서를 지킨다. 롤백도 이전 CSV로 자동 전환 가능하다.

- **의존성 해결**: Operator A가 Operator B를 필요로 하는 경우, 수동 설치는 사람이 확인해야 한다. OLM은 CSV의 `required` 필드를 보고 자동으로 B를 먼저 설치한다.

- **멀티 테넌트**: OLM은 `installMode`로 AllNamespaces (클러스터 전역) vs OwnNamespace (네임스페이스별) 설치를 지원한다. 수동 설치는 RBAC을 네임스페이스별로 수동 설정해야 한다.

- **OLM 없이 설치해야 하는 경우**: (1) 프로덕션에서 자동 업그레이드를 원하지 않음 (수동 승인), (2) Air-gapped 환경 (외부 레지스트리 접근 불가), (3) 커스터마이징이 많이 필요 (CRD에 커스텀 필드 추가 등).

### 심화 질문

- OLM의 InstallPlan은 무엇이고, 왜 필요한가? (힌트: 실제 설치 작업을 정의하고, 사용자가 승인할 수 있게 함)
- Subscription의 `channel`은 무엇인가? (힌트: stable, beta, alpha 등 릴리스 트랙, 자동 업그레이드 범위 제어)
- OLM을 사용하면 Operator 개발자는 무엇을 추가로 제공해야 하는가? (힌트: CSV, CatalogSource에 등록할 메타데이터)

---

## 질문 7: Operator Anti-pattern - 피해야 할 설계 실수

### 핵심 포인트

- **너무 많은 책임**: 하나의 Operator가 DB 배포 + 백업 + 모니터링 + 로깅 + 네트워크 정책을 모두 관리하려고 하면 복잡도가 폭발한다. **단일 책임 원칙**을 지켜야 한다. 예: DB Operator는 DB 생명주기만, 백업은 별도 Backup Operator에 위임.

- **상태 관리 실패**: Reconcile 로직에서 외부 API를 호출하거나 외부 DB에 상태를 저장하면 문제가 발생한다. Kubernetes는 etcd의 상태를 "진실의 원천(source of truth)"로 삼는다. 외부 상태와 etcd가 불일치하면 복구가 어렵다.

- **비멱등성 로직**: Reconcile 함수를 여러 번 호출해도 결과가 같아야 한다. 예를 들어 "Pod 1개 추가"가 아니라 "총 3개여야 함"으로 판단해야 한다. 비멱등성 로직은 재시도 시 중복 생성 문제를 일으킨다.

- **즉시 실행(Imperative) 로직**: Operator는 선언적이어야 한다. 사용자가 `spec.backup: "now"`처럼 즉시 실행을 요청하면 이벤트가 중복 발생할 수 있다. 대신 `spec.backup.trigger: "manual-20230601"`처럼 고유 ID를 사용하고, status에 실행 여부를 기록한다.

- **과도한 watch**: 모든 Pod, Service를 watch하면 API Server에 부담을 준다. Owner Reference를 사용하여 내가 생성한 리소스만 watch해야 한다. 예: PostgresCluster가 생성한 StatefulSet만 watch, 다른 Operator의 리소스는 무시.

- **에러 처리 부실**: 일시적 에러(네트워크 장애)와 영구 에러(잘못된 설정)를 구분하지 않으면 무한 재시도가 발생한다. 영구 에러는 status에 기록하고 재시도를 중단해야 한다.

### 심화 질문

- Operator가 외부 API를 호출해야 한다면 어떻게 설계해야 하는가? (힌트: Idempotency token 사용, 외부 상태를 CR status에 동기화)
- Reconcile 중에 etcd에 변경사항을 저장하지 않고 메모리에만 두면 어떤 문제가 발생하는가? (힌트: Pod 재시작 시 상태 손실, 다른 Controller와 충돌)
- Owner Reference를 설정하지 않으면 어떤 문제가 발생하는가? (힌트: CR 삭제 시 생성한 리소스가 orphan으로 남음, Garbage Collector가 정리 못함)

---

## 종합 점검

다음 시나리오를 읽고 어떻게 설계할지 생각해보자:

**시나리오**: Redis 클러스터를 Kubernetes에 배포하고, 다음 기능을 자동화하려고 한다.

1. 초기 배포 시 Master 1개 + Replica 2개 구성
2. 매일 새벽 3시 RDB 백업을 S3에 저장
3. Master 장애 시 Replica를 자동 승격
4. Prometheus로 메트릭 수집
5. 메모리 사용률 80% 도달 시 maxmemory 설정 자동 증가

**점검 질문**:

- 이 기능을 Operator로 구현하기에 적합한가? 아니면 Helm + 수동 스크립트로 충분한가?
- CRD의 spec에는 어떤 필드가 필요한가? (예: `spec.replicas`, `spec.backup.schedule`)
- Operator 성숙도 Level 몇을 목표로 해야 하는가?
- Reconcile 로직에서 가장 복잡한 부분은 무엇인가? (힌트: Master Failover 시 Sentinel 상태 확인, Replica 승격, ConfigMap 업데이트)
- 메모리 사용률 모니터링은 Controller가 직접 해야 하는가, 아니면 Prometheus Alert를 받아야 하는가?
- OLM을 사용할 것인가? 아니면 수동 설치가 나은가?

이 질문들에 답할 수 있다면 Operator 패턴을 이해한 것이다. 다음 단계는 실제 코드를 작성해보는 것이다.
