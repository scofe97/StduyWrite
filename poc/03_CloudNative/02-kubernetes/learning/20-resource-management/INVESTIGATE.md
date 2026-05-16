<!-- migrated: write/09_cloud/kubernetes/deepdive/13-01.자원 관리 점검.md (2026-04-19) -->

# Ch20. Resource Management 점검 질문

## Q1: Requests 없이 Limits만 설정하면 어떻게 되는가?

**질문**: Pod 스펙에 `resources.limits`만 설정하고 `resources.requests`를 생략하면, Kubernetes는 어떻게 동작하며, 이것이 스케줄링과 QoS 클래스에 어떤 영향을 미치는가?

**핵심 포인트**:

- Kubernetes는 Limits만 설정된 경우, **Requests를 Limits와 동일한 값으로 자동 설정**한다. 예를 들어 `limits.cpu: 500m`만 지정하면 `requests.cpu: 500m`이 자동으로 부여된다. 이는 Kubernetes API Server의 기본 동작이며, `kubectl get pod -o yaml`로 확인하면 requests 필드가 자동으로 채워져 있는 것을 볼 수 있다.

- 이렇게 자동 설정되면 **Requests = Limits**가 되므로, QoS 클래스는 **Guaranteed**가 된다. 이는 의도하지 않은 결과일 수 있다. 개발자가 "최대 500m까지만 사용하게 하자"는 의도로 Limits만 설정했는데, 실제로는 "500m을 보장해 달라"는 Requests까지 설정된 것이다.

- **스케줄링 영향**: Requests가 Limits와 동일하게 높게 설정되면, 스케줄러는 더 많은 리소스를 확보한 노드를 찾아야 한다. 예를 들어 실제로는 100m만 사용하는 Pod가 500m을 Requests로 요청하면, 노드에 400m의 리소스가 낭비된다. 이는 클러스터 활용률을 떨어뜨리고, 노드를 더 많이 필요로 하게 만든다.

- **올바른 설정 방법**: 대부분의 경우 Requests와 Limits를 모두 명시적으로 설정해야 한다. Requests는 평균 사용량, Limits는 피크 사용량으로 분리하여 Burstable QoS를 활용하는 것이 리소스 효율성 측면에서 유리하다.

- **반대 경우 (Requests만 설정, Limits 생략)**: Limits가 없으면 해당 리소스의 상한선이 없다. CPU는 노드의 전체 CPU를 사용할 수 있고, 메모리도 노드의 전체 메모리를 사용할 수 있다(다른 Pod와 경합). QoS 클래스는 Burstable이 된다.

**심화 질문**: LimitRange에 `default` (Limits 기본값)만 설정하고 `defaultRequest`를 생략하면 어떻게 되는가? LimitRange의 기본값 주입과 Kubernetes의 자동 Requests 설정이 어떤 순서로 적용되는가?

---

## Q2: QoS 클래스가 Pod 퇴거(Eviction) 순서에 미치는 영향

**질문**: 노드에 메모리 압박(MemoryPressure)이 발생했을 때, kubelet은 어떤 기준으로 Pod를 퇴거하며, 같은 QoS 클래스 내에서는 어떤 Pod가 먼저 퇴거되는가?

**핵심 포인트**:

- kubelet은 노드의 가용 메모리가 `eviction-hard` 임계값(기본 `memory.available < 100Mi`) 미만으로 떨어지면 Eviction을 시작한다. 그 전에 `eviction-soft` 임계값에 도달하면 `eviction-soft-grace-period` 동안 대기하다가 Eviction한다. soft eviction은 경고 성격이고, hard eviction은 즉각 실행된다.

- **퇴거 순서**: (1) BestEffort Pod가 가장 먼저 퇴거된다. Requests/Limits가 없으므로 리소스를 보장받지 못한다. (2) Burstable Pod가 그 다음이다. 다만 모든 Burstable Pod가 동시에 퇴거되는 것은 아니다. (3) Guaranteed Pod는 가장 마지막에 퇴거되며, 극단적인 상황(시스템 데몬 보호를 위해)에서만 퇴거된다.

- **같은 QoS 클래스 내 우선순위**: Burstable Pod 간에는 **Requests 대비 실제 메모리 사용량의 비율**이 높은 Pod부터 퇴거한다. 예를 들어 Pod A가 Requests 128Mi에 실제 256Mi를 사용(200%)하고, Pod B가 Requests 256Mi에 실제 300Mi를 사용(117%)하면, Pod A가 먼저 퇴거된다. Requests를 크게 초과한 Pod가 "더 나쁜 시민"으로 간주되는 것이다.

- **PriorityClass와의 관계**: QoS 클래스는 Eviction 순서의 첫 번째 기준이지만, PriorityClass가 설정되면 이를 함께 고려한다. 높은 Priority의 BestEffort Pod가 낮은 Priority의 Burstable Pod보다 나중에 퇴거될 수 있다. 다만 실무에서는 PriorityClass와 QoS를 함께 관리하는 것이 복잡하므로, 중요한 워크로드는 Guaranteed + 높은 PriorityClass를 함께 사용하는 것이 권장된다.

- **Eviction vs OOMKill**: Eviction은 kubelet이 Pod 단위로 수행하는 "graceful 종료"(SIGTERM → 유예 시간 → SIGKILL)이며, Pod가 다른 노드에 재스케줄링될 수 있다. OOMKill은 Linux Kernel이 컨테이너 단위로 수행하는 "즉시 종료"(SIGKILL)이며, 같은 노드에서 재시작된다. Eviction은 노드 전체의 메모리 부족 시, OOMKill은 개별 컨테이너의 cgroup 메모리 한도 초과 시 발생한다.

**심화 질문**: `--eviction-hard` 임계값을 `memory.available < 500Mi`로 높이면 클러스터 안정성에 어떤 영향이 있는가? 노드당 500Mi가 항상 예약되므로 Pod에 할당 가능한 메모리가 줄어드는 트레이드오프는 어떻게 판단하는가?

---

## Q3: CPU Throttling이 애플리케이션 응답 시간에 미치는 영향

**질문**: CPU Limits에 의해 throttling이 발생하면, 애플리케이션의 응답 시간에 어떤 패턴으로 영향을 미치며, throttling을 감지하고 대응하는 방법은 무엇인가?

**핵심 포인트**:

- CPU throttling은 CFS(Completely Fair Scheduler)의 bandwidth control에 의해 발생한다. 기본 CFS period는 100ms이며, CPU Limits가 `200m`이면 100ms 주기 동안 20ms의 CPU 시간을 사용할 수 있다. 20ms를 모두 소진하면 나머지 80ms 동안 CPU를 사용하지 못하고 대기한다.

- **응답 시간 영향**: throttling이 발생하면 평균 응답 시간보다 **tail latency(p95, p99)**가 크게 증가한다. 대부분의 요청은 20ms 내에 처리되어 정상이지만, throttle 구간에 걸린 요청은 최대 80ms를 추가로 대기해야 한다. 이는 사용자 경험에 직접적인 영향을 미친다. 특히 동기적으로 여러 API를 호출하는 마이크로서비스에서는 각 구간의 tail latency가 누적되어 전체 응답 시간이 폭발적으로 증가한다.

- **GC(Garbage Collection) 영향**: Java, Go 같은 GC 언어에서는 throttling이 GC 시간을 늘린다. GC는 CPU를 집중적으로 사용하는 작업인데, throttling으로 CPU가 제한되면 GC가 평소보다 5~10배 오래 걸릴 수 있다. 이 기간 동안 애플리케이션의 모든 요청이 일시 중지(Stop-the-World)된다.

- **감지 방법**: Prometheus의 `container_cpu_cfs_throttled_periods_total` 메트릭으로 throttle된 주기 수를 추적한다. throttling 비율 = `throttled_periods / total_periods * 100`이다. 이 비율이 25%를 넘으면 CPU Limits를 증가시키는 것을 고려해야 한다. 5%를 넘으면 관찰을 시작하고, 10%를 넘으면 경고 알림을 설정한다.

- **대응 전략**: (1) CPU Limits 증가 - 가장 직접적인 해결책. (2) CPU Limits 제거 - Google 등 대규모 운영 환경에서 사용하는 전략. Requests만 설정하여 스케줄러가 적절히 배치하고, Limits를 없애 throttling을 방지한다. 다만 Noisy Neighbor 위험이 있으므로, 노드의 워크로드 구성을 잘 관리해야 한다. (3) 애플리케이션 최적화 - CPU 사용을 줄이는 코드 최적화, 비동기 처리 도입.

**심화 질문**: Linux Kernel 5.4+ 에서 도입된 `cpu.cfs_burst_us` 기능은 throttling을 어떻게 완화하는가? 이 기능이 Kubernetes에서 사용 가능한가?

---

## Q4: LimitRange와 ResourceQuota의 역할 차이

**질문**: LimitRange와 ResourceQuota는 모두 네임스페이스 레벨에서 리소스를 제한하는데, 각각 어떤 문제를 해결하며, 실무에서 어떻게 조합하여 사용하는가?

**핵심 포인트**:

- **LimitRange**는 **개별 Pod/Container 레벨**의 리소스를 통제한다. (1) Requests/Limits를 설정하지 않은 Pod에 기본값을 자동 주입한다 (`default`, `defaultRequest`). (2) 단일 Pod가 사용할 수 있는 리소스의 최소/최대 범위를 강제한다 (`min`, `max`). (3) Limits/Requests 비율을 제한하여 과도한 overcommit을 방지한다 (`maxLimitRequestRatio`). LimitRange는 "각 Pod가 합리적인 범위 내에서 리소스를 사용하도록" 보장한다.

- **ResourceQuota**는 **네임스페이스 전체**의 리소스 총량을 제한한다. (1) 네임스페이스 내 모든 Pod의 Requests/Limits 합계를 제한한다. (2) Pod, Service, ConfigMap 등 오브젝트 수를 제한한다. (3) PVC의 총 스토리지 크기를 제한한다. ResourceQuota는 "한 팀(네임스페이스)이 클러스터 리소스를 독점하지 못하도록" 보장한다.

- **조합이 필요한 이유**: ResourceQuota만 설정하면, 쿼타가 있는 네임스페이스에서는 모든 Pod에 Requests/Limits가 필수가 된다. 이를 생략하면 Pod 생성이 거부된다. 개발자의 편의를 위해 LimitRange로 기본값을 설정하면, Requests/Limits를 명시하지 않아도 자동으로 채워져 ResourceQuota와 충돌하지 않는다.

- **실무 조합 예시**:
  - LimitRange: 컨테이너 기본 CPU 100m/200m (Requests/Limits), 최대 2 core
  - ResourceQuota: 네임스페이스 전체 CPU Requests 8 core, Limits 16 core, Pod 최대 50개
  - 결과: 개발자가 아무 설정 없이 Pod를 배포해도 기본값이 적용되고, 팀 전체가 8 core를 넘길 수 없다

- **적용 순서**: (1) LimitRange의 기본값이 먼저 주입된다. (2) 그 다음 ResourceQuota의 총량 검사가 수행된다. (3) 두 가지 모두 통과해야 Pod가 생성된다.

**심화 질문**: ResourceQuota에 `scopeSelector`를 사용하여 특정 PriorityClass의 Pod만 Quota를 적용하는 방법은? 예를 들어 "low-priority" Pod는 4 core까지, "high-priority" Pod는 16 core까지 허용하는 설정은?

---

## Q5: "Requests = Limits"로 설정하는 것이 항상 좋은가?

**질문**: Guaranteed QoS를 위해 Requests와 Limits를 동일하게 설정하는 것이 항상 최선의 선택인가? 어떤 상황에서 Burstable이 더 적합한가?

**핵심 포인트**:

- **Guaranteed(Requests = Limits)의 장점**: (1) QoS 우선순위가 가장 높아 Eviction 시 마지막에 퇴거된다. (2) 성능이 예측 가능하다. 항상 동일한 리소스가 보장되므로 응답 시간이 안정적이다. (3) CPU throttling이 발생하지 않는다 (Requests 이상을 사용해도 Limits가 동일하므로). (4) 리소스 계획이 단순하다. 사용량이 곧 예약량이므로 노드 활용률을 쉽게 계산할 수 있다.

- **Guaranteed의 단점**: (1) **리소스 낭비**가 가장 큰 문제다. API 서버가 평균 200m CPU를 사용하지만 피크 시 500m을 사용한다면, Guaranteed로 설정하면 500m을 항상 예약해야 한다. 나머지 300m은 대부분의 시간 동안 낭비된다. (2) **노드 활용률 저하**: 모든 Pod가 Guaranteed이면, 노드의 Allocatable 리소스가 빠르게 소진되어 더 많은 노드가 필요하다. 이는 클라우드 비용 증가로 직결된다. (3) **스케일링 제한**: HPA(Horizontal Pod Autoscaler)로 스케일 아웃할 때, Guaranteed Pod는 더 많은 노드 리소스를 필요로 하므로 스케일링 속도가 느려진다.

- **Burstable(Requests < Limits)의 장점**: (1) **오버커밋(Overcommit)** 가능. 노드의 Allocatable보다 더 많은 Pod를 스케줄링할 수 있다(Requests 합계 기준). 대부분의 Pod가 항상 피크를 사용하지 않으므로, 통계적으로 안전하다. (2) **비용 효율성**: 같은 노드에 더 많은 Pod를 배치하여 인프라 비용을 절감한다. (3) **버스트 트래픽 대응**: 일시적으로 Requests 이상의 리소스를 사용할 수 있어, 트래픽 급증 시 유연하게 대응한다.

- **워크로드별 권장**:
  - **Guaranteed가 적합**: 데이터베이스(MySQL, PostgreSQL), 캐시(Redis), 메시지 브로커(Kafka) 등 Stateful 워크로드. 성능 일관성이 핵심이고, 퇴거 시 데이터 유실 위험이 있는 워크로드.
  - **Burstable이 적합**: Stateless API 서버, 웹 프론트엔드, 배치 작업. 트래픽에 따라 사용량이 변하고, 퇴거 시 재스케줄링으로 복구 가능한 워크로드.

- **하이브리드 전략**: CPU는 Burstable(Requests < Limits 또는 Limits 미설정), 메모리는 Guaranteed(Requests = Limits)로 설정하는 전략도 있다. CPU throttling은 성능 저하만 유발하지만, 메모리 초과는 OOMKill을 유발하므로 메모리는 보수적으로 설정하는 것이다. 다만 이 경우 QoS 클래스는 Burstable이 된다(모든 리소스가 Requests = Limits여야 Guaranteed).

**심화 질문**: 클라우드 환경에서 Cluster Autoscaler와 리소스 설정의 관계는? Requests가 높으면 새 노드를 빨리 프로비저닝하지만 비용이 증가한다. Requests를 낮추면 비용은 절감되지만 노드 과부하 위험이 있다. 이 트레이드오프를 어떻게 최적화하는가?

---

## Q6: 노드의 Allocatable vs Capacity 차이

**질문**: `kubectl describe node`에서 보이는 Capacity와 Allocatable은 어떻게 다르며, 이 차이가 리소스 스케줄링에 어떤 영향을 미치는가?

**핵심 포인트**:

- **Capacity**는 노드의 물리적(또는 가상) 총 리소스다. 예를 들어 4 core CPU, 16GB RAM을 가진 노드의 Capacity는 `cpu: 4`, `memory: 16Gi`다. 이는 하드웨어가 제공하는 원시 리소스 양이다.

- **Allocatable**은 Pod에 실제로 할당 가능한 리소스다. Capacity에서 시스템 예약분을 뺀 값이다. 시스템 예약분에는 (1) kubelet, kube-proxy 등 Kubernetes 시스템 데몬이 사용하는 `kube-reserved`, (2) OS 커널, sshd, systemd 등이 사용하는 `system-reserved`, (3) Eviction 임계값(`eviction-hard`)을 위한 예약분이 포함된다.

- **계산 공식**: `Allocatable = Capacity - kube-reserved - system-reserved - eviction-threshold`. 예를 들어 16GB 노드에서 kube-reserved 1GB, system-reserved 1GB, eviction-threshold 100Mi이면, Allocatable은 약 13.9GB다.

- **스케줄링 영향**: kube-scheduler는 **Allocatable을 기준으로 Pod를 배치**한다. Capacity가 아닌 Allocatable에서 기존 Pod의 Requests 합계를 뺀 잔여 리소스를 확인한다. 따라서 Allocatable이 Capacity보다 작으므로, 실제로 배치할 수 있는 Pod 수가 줄어든다. 이를 고려하지 않으면 "노드에 16GB 있으니 2GB Pod를 8개 배치할 수 있다"고 생각하지만, 실제로는 6~7개만 가능할 수 있다.

- **확인 방법**:
  ```bash
  kubectl describe node <node-name>
  # Capacity:
  #   cpu:                4
  #   memory:             16384Mi
  # Allocatable:
  #   cpu:                3800m
  #   memory:             14000Mi
  # Allocated resources:
  #   (Total limits may be over 100 percent...)
  #   Resource           Requests    Limits
  #   cpu                2100m (55%) 4200m (110%)
  #   memory             8Gi (57%)   12Gi (85%)
  ```

- **Allocated resources의 100% 초과**: `kubectl describe node`의 "Allocated resources"에서 Limits 합계가 100%를 넘는 경우가 있다. 이는 오버커밋(Overcommit)을 의미하며, 모든 Pod가 동시에 Limits까지 사용하면 리소스가 부족해진다. Requests 합계는 100%를 넘을 수 없지만(스케줄러가 방지), Limits 합계는 제한이 없다.

**심화 질문**: 관리형 Kubernetes(EKS, GKE, AKS)에서 시스템 예약분은 어떻게 자동 설정되는가? GKE의 경우 노드 크기에 따라 kube-reserved가 달라지는데, 이 값을 커스터마이징하는 것이 적절한 경우는 언제인가?

---

## Q7: VPA와 HPA를 동시에 사용할 수 있는가?

**질문**: Vertical Pod Autoscaler(VPA)와 Horizontal Pod Autoscaler(HPA)를 같은 Deployment에 동시에 적용하면 어떤 문제가 발생하며, 이를 해결하는 방법은 무엇인가?

**핵심 포인트**:

- **기본적으로 VPA와 HPA를 CPU 메트릭으로 동시에 사용하면 충돌**한다. HPA는 CPU 사용률이 목표치(예: 70%)를 넘으면 replica를 늘린다. VPA는 CPU 사용량이 높으면 Requests를 증가시킨다. 두 가지가 동시에 동작하면, VPA가 Requests를 늘려서 CPU 사용률(사용량/Requests)이 낮아지고, HPA가 이를 보고 replica를 줄이고, 그러면 다시 사용률이 올라가는 진동(oscillation)이 발생한다.

- **해결 방법 1: 메트릭 분리**. HPA는 CPU 기반, VPA는 메모리 기반으로 사용한다. 또는 HPA를 커스텀 메트릭(QPS, 요청 수)으로 설정하고, VPA는 CPU/메모리를 관리한다. 메트릭이 겹치지 않으면 충돌하지 않는다.

- **해결 방법 2: VPA를 Off 모드로 사용**. VPA를 `updateMode: "Off"`로 설정하여 추천만 받고, 실제 적용은 수동으로 한다. 이 방법이 가장 안전하며, VPA recommendations를 주기적으로 확인하여 Deployment의 Requests를 수동으로 조정한다.

- **해결 방법 3: Multidimensional Pod Autoscaler (MPA)**. Google이 제안한 접근법으로, VPA와 HPA를 통합 관리하는 컨트롤러다. CPU Requests를 VPA가 조정하면서 동시에 HPA가 replica를 조정할 수 있다. 다만 아직 실험적 기능이다.

- **실무 권장 조합**: 대부분의 경우 HPA를 메인으로 사용하고, VPA는 Off 모드로 추천값만 참고한다. 메모리 최적화가 필요한 워크로드(Java의 JVM Heap)에는 VPA를 메모리에만 적용하고, HPA는 CPU 또는 커스텀 메트릭으로 운영한다.

**심화 질문**: KEDA(Kubernetes Event-Driven Autoscaling)는 HPA/VPA와 어떻게 다른가? KEDA는 이벤트 소스(Kafka lag, Redis queue length)를 기반으로 스케일링하는데, VPA와 함께 사용할 때 주의할 점은 무엇인가?


---

> **[이관 완료]** write/09_cloud/kubernetes/13-01.자원 관리.md · deepdive/13-01.자원 관리 점검.md (2026-04-19)
