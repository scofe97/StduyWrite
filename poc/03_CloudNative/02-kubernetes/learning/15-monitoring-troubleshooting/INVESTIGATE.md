# Ch15. Kubernetes 모니터링과 트러블슈팅 - 점검 질문

## Q1: 메트릭 vs 로그 vs 트레이스의 역할 차이

**질문**: 관측 가능성의 세 가지 기둥은 각각 어떤 문제를 해결하는 데 적합하며, 실무에서 어떻게 조합하여 사용하는가?

**핵심 포인트**:

- **메트릭(Metrics)**은 "무엇이 일어나고 있는가?"를 숫자로 보여준다. CPU 사용률이 90%를 넘는지, QPS(초당 요청 수)가 평소보다 2배 증가했는지 등 시스템의 전체적인 건강 상태를 파악하는 데 사용한다. 시계열 데이터베이스에 저장되어 시간에 따른 트렌드를 분석할 수 있으며, 임계값 기반 알림(예: CPU > 80%)을 설정할 수 있다. 하지만 메트릭만으로는 "왜" 문제가 발생했는지 알 수 없다.

- **로그(Logs)**는 "왜 실패했는가?"를 텍스트로 기록한다. 특정 HTTP 요청이 500 에러를 반환했을 때, 에러 스택 트레이스, 요청 파라미터, 사용자 ID 등 상세한 컨텍스트를 제공한다. 로그는 이벤트 중심이며, 시간 순서대로 무슨 일이 일어났는지 추적할 수 있다. 하지만 로그는 양이 많고, 전체 시스템 상태를 한눈에 파악하기 어렵다. 또한 디버깅 중에만 의미가 있으며, 사전 예방적 알림에는 부적합하다.

- **트레이스(Traces)**는 "어디에서 시간을 소비하는가?"를 분산 시스템에서 추적한다. 하나의 사용자 요청이 API Gateway → Auth Service → Payment Service → Database를 거치는 동안 각 구간에서 얼마나 시간이 걸렸는지 Span으로 기록한다. 예를 들어 전체 응답 시간이 2초인데, Payment Service에서 1.8초가 소요되었다면 그곳이 병목임을 알 수 있다. 트레이스는 마이크로서비스 아키텍처에서 필수적이지만, 구현 비용이 높고 (모든 서비스에 계측 필요), 샘플링을 해야 하므로 모든 요청을 추적하지는 못한다.

- **실무 조합 시나리오**: 대시보드에서 메트릭으로 "HTTP 5xx 에러율이 급증"을 감지 → 알림 수신 → 로그에서 에러 메시지 확인 → 트레이스로 어느 서비스에서 타임아웃이 발생했는지 파악 → 해당 서비스의 메트릭(CPU, 메모리)을 다시 확인하여 리소스 부족 여부 판단. 이처럼 세 가지 데이터는 상호 보완적이다.

**심화 질문**: Exemplars는 메트릭과 트레이스를 어떻게 연결하는가? Prometheus에서 특정 메트릭 값(예: 응답 시간 P99)을 클릭하면 해당 요청의 트레이스 ID로 바로 이동하는 기능을 구현하려면 무엇이 필요한가?

---

## Q2: Prometheus의 Pull 기반 수집 모델과 Push 모델(StatsD) 차이

**질문**: Prometheus는 왜 Pull 모델을 선택했으며, Push 모델과 비교했을 때 각각의 장단점은 무엇인가?

**핵심 포인트**:

- **Pull 모델(Prometheus)**은 모니터링 시스템이 타겟의 `/metrics` 엔드포인트에 주기적으로 HTTP 요청을 보내 메트릭을 가져온다. Prometheus가 스크랩 타겟 목록을 관리하고, Service Discovery(Kubernetes API, Consul, EC2 등)로 동적으로 타겟을 발견한다. 타겟이 다운되면 Prometheus가 즉시 감지할 수 있으며 (스크랩 실패 → `up` 메트릭 0), 중앙에서 스크랩 주기와 타임아웃을 제어할 수 있다.

- **Push 모델(StatsD, Graphite)**은 애플리케이션이 메트릭을 모니터링 시스템에 직접 보낸다. 애플리케이션 코드에서 `statsd.increment('requests')` 같은 API를 호출하여 UDP/TCP로 메트릭을 전송한다. 모니터링 시스템은 수동적으로 메트릭을 받기만 한다. 단기 실행 작업(Batch Job, Cron)에 유리한데, Job이 10초간 실행되고 종료되면 Pull 모델로는 메트릭을 놓칠 수 있지만 Push는 종료 전 메트릭을 보내면 된다.

- **Pull 모델 장점**: (1) 타겟 상태 모니터링 가능 (타겟이 죽었는지 살았는지), (2) 중앙 집중식 설정 (애플리케이션은 메트릭 노출만 하면 됨, Prometheus 주소 몰라도 됨), (3) 백프레셔 제어 (Prometheus가 감당할 수 있는 속도로 스크랩), (4) 여러 Prometheus가 같은 타겟을 스크랩 가능 (HA 구성).

- **Pull 모델 단점**: (1) 방화벽/NAT 뒤의 타겟 스크랩 어려움 (Prometheus가 접근 불가), (2) 단기 실행 작업 메트릭 놓칠 수 있음, (3) 스크랩 주기가 길면 메트릭 손실 (30초마다 스크랩하는데 10초 간격으로 발생한 이벤트는 누락 가능).

- **Push 모델 장점**: (1) 방화벽/NAT 환경에서도 동작 (애플리케이션이 밖으로 연결), (2) 단기 작업 메트릭 보존, (3) 실시간 전송 (지연 없음).

- **Push 모델 단점**: (1) 타겟 상태 모니터링 불가 (메트릭이 안 오는 게 타겟 다운인지 네트워크 문제인지 구분 어려움), (2) 모니터링 시스템 주소를 모든 애플리케이션이 알아야 함 (설정 복잡), (3) DDoS 공격 가능 (악의적 클라이언트가 대량 메트릭 전송 → 모니터링 시스템 과부하).

- **Prometheus의 Push Gateway**: 단기 실행 작업을 위해 Prometheus는 Push Gateway를 제공한다. Batch Job이 메트릭을 Push Gateway에 Push → Prometheus가 Push Gateway를 Pull한다. 하지만 Push Gateway는 단기 작업 전용이며, 장기 실행 서비스에는 사용하지 말아야 한다 (타겟 상태 추적 불가).

**심화 질문**: Kubernetes 환경에서 Istio 같은 Service Mesh를 사용할 때, Envoy Sidecar의 메트릭은 Pull로 수집하는가 Push인가? 수천 개의 Pod가 있을 때 Prometheus의 스크랩 부하를 줄이려면 어떤 전략을 사용해야 하는가?

---

## Q3: ServiceMonitor CR의 동작 원리 (Prometheus가 타겟을 발견하는 방식)

**질문**: ServiceMonitor Custom Resource를 생성하면 Prometheus가 어떻게 이를 감지하고 스크랩 타겟을 추가하는가?

**핵심 포인트**:

- **Prometheus Operator**는 Kubernetes Controller 패턴을 구현한 Operator다. Prometheus CR, ServiceMonitor CR, PrometheusRule CR을 감시하며, 변경사항을 감지하면 Prometheus 설정 파일(`prometheus.yml`)을 자동으로 업데이트하고 Prometheus를 리로드한다.

- **ServiceMonitor 생성 흐름**: 사용자가 `kubectl apply -f servicemonitor.yaml` 실행 → Kubernetes API에 ServiceMonitor CR 저장 → Prometheus Operator가 Watch API로 변경 감지 → Operator가 ServiceMonitor의 `spec.selector`로 매칭되는 Service를 조회 → Service의 Endpoints를 가져와 스크랩 타겟 목록 생성 → Prometheus ConfigMap 업데이트 → Prometheus Pod에 SIGHUP 시그널 전송 (설정 리로드).

- **셀렉터 매칭**: ServiceMonitor의 `spec.selector`는 라벨 셀렉터다. 예를 들어 `matchLabels: {app: nginx}`이면, `app=nginx` 라벨을 가진 모든 Service를 찾는다. 그런 다음 각 Service의 Endpoints를 조회하여 실제 Pod IP 목록을 얻는다. 즉, ServiceMonitor → Service → Endpoints → Pod IP 순서로 타겟을 발견한다.

- **Prometheus의 ServiceMonitor 선택**: 모든 ServiceMonitor가 Prometheus에 적용되는 것은 아니다. Prometheus CR의 `spec.serviceMonitorSelector`가 ServiceMonitor의 라벨과 일치해야 한다. kube-prometheus-stack의 기본 설정은 `release: kube-prometheus` 라벨을 가진 ServiceMonitor만 선택한다. 따라서 사용자가 만든 ServiceMonitor에도 이 라벨을 추가해야 한다.

- **자동 업데이트**: Service의 Endpoints가 변경되면 (Pod 추가/삭제), Prometheus Operator가 자동으로 감지하여 스크랩 타겟을 업데이트한다. 예를 들어 Deployment를 3 → 5 replica로 늘리면, 새 Pod 2개가 Service Endpoints에 추가되고, 몇 초 후 Prometheus가 새 타겟을 스크랩하기 시작한다.

- **네임스페이스 제한**: ServiceMonitor는 `spec.namespaceSelector`로 특정 네임스페이스만 스캔할 수 있다. `any: true`로 설정하면 모든 네임스페이스를 탐색하지만, 보안상 특정 네임스페이스만 허용하는 것이 좋다.

**심화 질문**: PodMonitor는 ServiceMonitor와 어떻게 다른가? Service 없이 Pod의 메트릭을 직접 스크랩하는 시나리오는 언제 필요한가? Headless Service를 사용하는 StatefulSet의 메트릭은 어떻게 수집하는가?

---

## Q4: CrashLoopBackOff 상태의 원인 분류와 디버깅 순서

**질문**: Pod가 CrashLoopBackOff 상태일 때, 어떤 순서로 원인을 파악하고 해결해야 하는가?

**핵심 포인트**:

- **CrashLoopBackOff 의미**: 컨테이너가 시작 후 즉시 종료(Exit Code 0이 아님)되고, Kubernetes가 재시작을 시도하지만 계속 실패하여 백오프(지수적 대기: 10초, 20초, 40초...) 상태에 있다는 뜻이다. "Loop"는 반복을 의미하며, "BackOff"는 재시작 간격이 점점 길어짐을 뜻한다.

- **원인 분류 (1) 애플리케이션 크래시**: 코드 버그(NullPointerException, Segmentation Fault), 설정 오류(환경변수 누락, DB 연결 문자열 오타), 의존성 문제(라이브러리 버전 충돌). 로그에서 에러 메시지를 확인하면 대부분 파악 가능하다.

- **원인 분류 (2) Liveness Probe 실패**: 애플리케이션은 정상 실행 중이지만, Liveness Probe가 계속 실패하여 Kubernetes가 컨테이너를 강제 종료한다. 예를 들어 `/healthz` 엔드포인트가 500 에러를 반환하거나, `initialDelaySeconds`가 너무 짧아서 애플리케이션 초기화 전에 Probe가 실행되는 경우다.

- **원인 분류 (3) 의존성 누락**: ConfigMap, Secret, Volume이 마운트되지 않았거나, 외부 서비스(DB, Redis)에 연결할 수 없는 경우. 예를 들어 `env.valueFrom.secretKeyRef`로 참조한 Secret이 존재하지 않으면 Pod 생성 자체가 실패하지만, 일부 경우 컨테이너가 시작 후 의존성을 확인하다가 크래시한다.

- **원인 분류 (4) 권한 문제**: 컨테이너가 root가 아닌 사용자로 실행되는데 (securityContext.runAsNonRoot), 파일 시스템 권한이 없어서 로그 파일을 쓸 수 없거나, Port 1024 미만을 바인딩하려다 실패하는 경우.

- **디버깅 순서**:
  1. `kubectl get pod <name>` - 재시작 횟수(RESTARTS) 확인
  2. `kubectl describe pod <name>` - Events 섹션에서 "Back-off restarting failed container" 메시지, Exit Code 확인
  3. `kubectl logs <name>` - 현재 컨테이너 로그 (애플리케이션이 무엇을 출력했는지)
  4. `kubectl logs <name> --previous` - 이전 컨테이너 로그 (재시작 전 마지막 에러)
  5. Exit Code 분석: 0 (정상 종료), 1 (일반 에러), 137 (SIGKILL, OOMKilled), 139 (Segmentation Fault)
  6. Liveness Probe 확인: `kubectl get pod <name> -o yaml | grep liveness` - initialDelaySeconds, timeoutSeconds가 적절한지

**심화 질문**: Pod가 CrashLoopBackOff인데 로그에 아무것도 출력되지 않는다면 (빈 로그)? 이는 컨테이너가 로그를 쓰기 전에 종료된다는 뜻인데, 이럴 때 디버깅하는 방법은? `kubectl debug`로 같은 이미지의 셸을 실행하여 수동으로 명령어를 테스트하는 방법은?

---

## Q5: OOMKilled vs Eviction 차이와 리소스 설정 전략

**질문**: Pod가 메모리 부족으로 종료될 때 OOMKilled와 Eviction의 차이는 무엇이며, 각각 어떻게 대응해야 하는가?

**핵심 포인트**:

- **OOMKilled (Out Of Memory Killed)**는 컨테이너가 자신의 메모리 limits를 초과했을 때 Linux Kernel의 OOM Killer가 프로세스를 강제 종료하는 것이다. Kubernetes가 개입하지 않으며, cgroup의 메모리 제한을 커널이 강제한다. Pod의 `status.containerStatuses[].lastState.terminated.reason`이 "OOMKilled", Exit Code가 137 (SIGKILL)이다. 이는 특정 컨테이너의 문제이며, 다른 Pod에는 영향을 주지 않는다.

- **Eviction (퇴출)**은 노드 전체의 메모리가 부족할 때 kubelet이 우선순위가 낮은 Pod를 강제로 삭제하여 노드를 보호하는 것이다. 노드의 가용 메모리가 `eviction-hard` 임계값(기본 100Mi) 미만으로 떨어지면, kubelet이 BestEffort → Burstable → Guaranteed 순서로 Pod를 종료한다. Eviction된 Pod는 다른 노드에 재스케줄링될 수 있다 (Deployment/ReplicaSet인 경우).

- **OOMKilled 대응**: (1) 메모리 limits 증가 - `resources.limits.memory: 512Mi → 1Gi`, (2) 애플리케이션 메모리 최적화 - 메모리 누수 수정, 캐시 크기 조정, (3) Heap 크기 조정 (Java의 경우 `-Xmx`를 limits보다 낮게 설정), (4) Vertical Pod Autoscaler (VPA) 사용 - 자동으로 적절한 limits 제안.

- **Eviction 대응**: (1) 노드 리소스 증가 - 더 큰 인스턴스 타입으로 변경, (2) Pod 수 줄이기 - 일부 Pod를 다른 노드로 이동, (3) requests와 limits 적절히 설정 - requests를 과도하게 낮게 설정하면 노드에 과다 스케줄링됨, (4) PriorityClass 사용 - 중요한 Pod(DB, Auth Service)는 높은 우선순위로 설정하여 Eviction 방지.

- **QoS (Quality of Service) 클래스**: Kubernetes는 Pod를 세 가지 QoS로 분류하여 Eviction 우선순위를 결정한다. (1) **Guaranteed**: requests == limits인 경우, 가장 마지막에 Eviction, (2) **Burstable**: requests < limits인 경우, 중간 우선순위, (3) **BestEffort**: requests/limits 없음, 가장 먼저 Eviction.

- **리소스 설정 전략**: 프로덕션에서는 모든 Pod에 requests와 limits를 설정해야 한다. requests는 평균 사용량의 80~90%, limits는 최대 사용량의 110~120%로 설정한다. requests가 너무 낮으면 노드 과다 할당, limits가 너무 낮으면 OOMKilled 빈발한다. 메트릭을 기반으로 조정: `kubectl top pod`로 실제 사용량 측정 → 2주 치 데이터로 P95, P99 값 확인.

**심화 질문**: Memory limits를 설정하지 않으면 (무제한) 어떤 일이 발생하는가? 한 Pod가 노드의 메모리를 모두 소진하면 다른 Pod도 영향을 받는가? 노드의 `allocatable` 메모리와 `capacity` 메모리의 차이는 무엇인가?

---

## Q6: Grafana에서 PromQL로 유용한 쿼리 5가지

**질문**: 실무에서 가장 자주 사용하는 PromQL 쿼리는 무엇이며, 각각 어떤 인사이트를 제공하는가?

**핵심 포인트**:

- **쿼리 1: Pod CPU 사용률 Top 10**
  ```promql
  topk(10,
    rate(container_cpu_usage_seconds_total{namespace="production"}[5m])
  )
  ```
  이 쿼리는 프로덕션 네임스페이스에서 CPU를 가장 많이 사용하는 10개 Pod를 보여준다. `rate()`는 5분간 평균 변화율을 계산하며, `container_cpu_usage_seconds_total`은 Counter 메트릭이므로 rate를 사용해야 한다. CPU 병목을 찾거나, 리소스 최적화 대상을 선정할 때 유용하다.

- **쿼리 2: Pod 메모리 사용률 (limits 대비 백분율)**
  ```promql
  container_memory_usage_bytes{namespace="production"}
  /
  container_spec_memory_limit_bytes{namespace="production"} * 100
  ```
  메모리 limits의 80%를 넘는 Pod는 OOMKilled 위험이 있다. 대시보드에서 이 값이 90%를 넘으면 빨간색으로 표시하도록 Threshold를 설정한다. limits가 없는 Pod는 분모가 0이 되어 결과가 나오지 않으므로, `container_spec_memory_limit_bytes > 0` 필터를 추가해야 한다.

- **쿼리 3: HTTP 5xx 에러율 (초당)**
  ```promql
  sum(rate(http_requests_total{status=~"5.."}[1m])) by (service)
  /
  sum(rate(http_requests_total[1m])) by (service) * 100
  ```
  각 서비스별로 전체 요청 중 5xx 에러가 차지하는 비율을 백분율로 보여준다. `status=~"5.."`는 정규식으로 500, 502, 503 등 모든 5xx 상태를 매칭한다. 이 값이 1%를 넘으면 알림을 발생시키는 PrometheusRule을 설정할 수 있다.

- **쿼리 4: Pod 재시작 횟수 증가 (최근 1시간)**
  ```promql
  increase(kube_pod_container_status_restarts_total{namespace="production"}[1h]) > 0
  ```
  지난 1시간 동안 재시작된 Pod를 찾는다. `increase()`는 Counter의 총 증가량을 반환하므로, 재시작이 없으면 0, 1번 재시작하면 1이 반환된다. 이 쿼리 결과를 Grafana Table 패널로 표시하면, 불안정한 Pod를 한눈에 파악할 수 있다.

- **쿼리 5: Persistent Volume 사용률 (디스크 풀 임박)**
  ```promql
  kubelet_volume_stats_used_bytes{namespace="production"}
  /
  kubelet_volume_stats_capacity_bytes{namespace="production"} * 100
  ```
  PVC의 디스크 사용률을 보여준다. 85%를 넘으면 경고, 95%를 넘으면 긴급 알림을 보낸다. 디스크가 풀 나면 데이터베이스 쓰기 실패, 로그 기록 불가 등 치명적인 문제가 발생하므로, 사전에 PVC 크기를 늘리거나 데이터를 정리해야 한다.

**심화 질문**: `rate()` vs `irate()` 차이는? `rate()`는 평균 변화율, `irate()`는 즉시 변화율인데, 각각 언제 사용하는가? Grafana 변수(Variable)를 사용하여 네임스페이스를 동적으로 선택하는 쿼리는 어떻게 작성하는가?

---

## Q7: AlertManager의 grouping, inhibition, silencing 개념

**질문**: AlertManager의 세 가지 핵심 기능은 각각 어떤 문제를 해결하며, 실무 설정 예시는?

**핵심 포인트**:

- **Grouping (그룹핑)**은 유사한 알림을 하나의 메시지로 묶어서 알림 폭주(Alert Storm)를 방지한다. 예를 들어 노드 하나가 다운되면 그 노드의 20개 Pod가 모두 알림을 발생시킨다. Grouping 없이는 Slack에 20개 메시지가 동시에 도착하지만, `group_by: ['node']`로 설정하면 "Node xyz has 20 alerts" 같은 하나의 메시지로 통합된다. `group_wait: 10s`는 첫 알림 후 10초 대기하여 추가 알림을 수집하고, `group_interval: 5m`는 같은 그룹에 대해 5분마다 업데이트를 보낸다.

- **Inhibition (억제)**은 특정 알림이 발생하면 다른 알림을 숨긴다. 예를 들어 "Node Down" 알림이 발생하면, 그 노드의 모든 Pod에 대한 "Pod Not Ready" 알림은 의미가 없으므로 억제한다. 설정 예시: `source_match: {alertname: NodeDown}`, `target_match: {alertname: PodNotReady}`, `equal: ['node']` - 같은 노드에 대한 알림만 억제. 이는 근본 원인(Root Cause)만 알림 받고, 파생 문제는 숨기는 전략이다.

- **Silencing (침묵)**은 특정 기간 동안 알림을 임시로 무시한다. 계획된 유지보수(Planned Maintenance), 배포 중, 알려진 이슈 등의 상황에서 사용한다. AlertManager UI 또는 `amtool`로 Silence를 생성하며, 라벨 매처로 조건을 지정한다. 예: `namespace=staging` 라벨을 가진 모든 알림을 2시간 동안 Silence → 스테이징 환경 배포 중 알림 방지. Silence는 만료되면 자동으로 제거되며, 히스토리가 기록된다.

- **실무 설정 예시 (Grouping)**:
  ```yaml
  route:
    group_by: ['alertname', 'cluster', 'namespace']
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 12h
  ```
  같은 alertname + cluster + namespace를 가진 알림을 그룹핑한다. 첫 알림 후 30초 대기(추가 알림 수집), 5분마다 그룹 업데이트, 같은 알림은 12시간마다 재전송.

- **실무 설정 예시 (Inhibition)**:
  ```yaml
  inhibit_rules:
    # Node Down이 발생하면 해당 노드의 Pod 알림 억제
    - source_match:
        alertname: NodeDown
      target_match_re:
        alertname: (PodNotReady|PodCrashLooping)
      equal: ['node']

    # Critical 알림이 있으면 같은 서비스의 Warning 억제
    - source_match:
        severity: critical
      target_match:
        severity: warning
      equal: ['service']
  ```

**심화 질문**: AlertManager HA(High Availability)를 구성할 때, 여러 AlertManager 인스턴스가 어떻게 중복 알림을 방지하는가? Gossip 프로토콜의 역할은? Prometheus가 여러 AlertManager에 알림을 보내면 각각이 독립적으로 Grouping/Inhibition을 수행하는가?

---

## Q8: kubectl debug 명령어로 ephemeral container를 사용하는 방법

**질문**: Distroless 이미지처럼 셸이 없는 컨테이너를 디버깅할 때 ephemeral container는 어떻게 동작하며, 어떤 한계가 있는가?

**핵심 포인트**:

- **Ephemeral Container (임시 컨테이너)**는 Kubernetes 1.23부터 정식 기능으로 추가된 디버깅 전용 컨테이너다. 실행 중인 Pod에 새 컨테이너를 추가하여 디버깅 도구를 사용할 수 있다. 기존 컨테이너의 파일시스템, 프로세스, 네트워크 네임스페이스를 공유하므로, 컨테이너 내부 상태를 외부에서 관찰할 수 있다.

- **기본 사용법**: `kubectl debug <pod-name> -it --image=busybox --target=<container-name>`을 실행하면, busybox 이미지로 새 컨테이너를 추가하고 셸에 접속한다. `--target` 옵션은 어느 컨테이너의 네임스페이스를 공유할지 지정한다. 셸에서 `ps aux`를 실행하면 타겟 컨테이너의 프로세스가 보인다.

- **동작 원리**: `kubectl debug`는 Pod Spec의 `ephemeralContainers` 필드에 새 컨테이너 정의를 추가한다. 이는 일반 `spec.containers`와 달리 런타임에 변경 가능하며, Pod 재시작 없이 추가된다. kubelet이 새 컨테이너를 생성하고, 타겟 컨테이너와 동일한 PID/NET 네임스페이스를 사용하도록 설정한다. 디버깅 종료 후 ephemeral container는 자동으로 삭제되지 않으므로, `kubectl delete pod`로 Pod 전체를 삭제해야 제거된다.

- **네임스페이스 공유**: `--target` 옵션을 사용하면 타겟 컨테이너의 PID, IPC, NET 네임스페이스를 공유한다. 즉, 같은 프로세스 ID 공간을 보고, 같은 네트워크 인터페이스(localhost 포함)를 사용한다. 파일시스템은 기본적으로 공유되지 않지만, `/proc/<pid>/root`를 통해 타겟 컨테이너의 파일시스템에 접근할 수 있다.

- **Node 디버깅**: `kubectl debug node/<node-name> -it --image=ubuntu`로 노드 자체를 디버깅할 수 있다. 이는 노드의 호스트 네임스페이스에 접근하는 특권 Pod를 생성한다. `/host` 디렉토리에 노드의 루트 파일시스템이 마운트되며, `chroot /host`로 노드 환경으로 전환할 수 있다. 이는 SSH 없이 노드 문제를 진단하는 강력한 도구다.

- **한계**: (1) Ephemeral container는 리소스 제한(requests/limits)을 설정할 수 없다. (2) 추가 후 삭제가 자동화되지 않아 Pod가 남아 있으면 계속 실행된다 (메모리 소비). (3) 일부 네임스페이스는 공유되지 않는다 (예: User 네임스페이스). (4) 모든 Kubernetes 버전/배포판에서 지원되지 않을 수 있다 (Feature Gate 확인 필요).

**심화 질문**: `kubectl debug`로 복사본 Pod를 생성하는 방법(`--copy-to`)은? 원본 Pod를 건드리지 않고 디버깅용 복사본을 만들어 이미지나 커맨드를 변경하는 시나리오는 언제 유용한가? 프로덕션에서 ephemeral container를 사용할 때 보안 고려사항은?


---

> **[이관 완료]** write/09_cloud/kubernetes/10-01.모니터링과 트러블슈팅.md · deepdive/10-01.모니터링과 트러블슈팅 점검.md (2026-04-19)
