# Kubernetes와 Linux 커널 아키텍처 분석 — AI 요약

> 출처: Gemini · 2026-11-14 · [플레이북] 1. Kubernetes와 Linux 커널 아키텍처 분석 · 분야: k8s · 미검증

## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
|---|---|---|
| Linux Namespaces | PID·네트워크·마운트 등 시스템 자원의 가시성을 프로세스별로 논리 격리하는 커널 기능 | [namespace와 루트 디렉토리](../../08_cloud/book/container-security/04-01.namespace와 루트 디렉토리 — 격리를 만드는 두 장치.md) |
| cgroups v2 | 단일 계층 구조로 CPU·메모리·I/O 하드웨어 자원의 상한을 프로세스 그룹 단위로 통제 | [네임스페이스와 cgroup으로 보는 컨테이너 격리](../../08_cloud/book/kubernetes-in-action/02-03.네임스페이스와 cgroup으로 보는 컨테이너 격리.md) |
| OOM Killer & Exit Code 137 | cgroup memory.max 초과 시 oom_score 기반으로 SIGKILL(9)을 전송해 즉시 강제 종료 (128+9) | [cgroup 사례 — Endowus OOMKilled](../../02_os/kernel/01-06.cgroup 사례 — Endowus OOMKilled.md) |
| CFS Bandwidth Control | 100ms 기본 주기 내 할당 quota 소진 시 다음 주기까지 프로세스를 강제 대기(Throttling) | [CPU — 아키텍처·스케줄러](../../02_os/book/systems-performance/06-02.CPU — 아키텍처·스케줄러.md) |
| OverlayFS | 불변 lowerdir(이미지)과 쓰기 가능 upperdir(컨테이너)을 병합하는 Union 파일시스템 | [OverlayFS와 user namespace](../../02_os/kernel/01-07.OverlayFS와 user namespace — Netflix UID 격리.md) |
| veth pair | 격리된 Pod 네트워크 네임스페이스와 호스트 브리지를 양방향 가상 케이블로 연결 | [소켓·인터페이스·veth·브리지](../../08_cloud/book/networking-and-kubernetes/02-01.커널이 패킷을 주고받는 자리 — 소켓·인터페이스·veth·브리지.md) |
| CRI (Container Runtime Interface) | kubelet이 containerd·runc 등 다양한 컨테이너 런타임을 제어하기 위한 표준 gRPC 규격 | [노드 압박 축출과 디스크 관리](../../08_cloud/docs/kubernetes/02-01.노드 압박 축출과 디스크 관리 — DiskPressure는 무엇을 보고 켜지는가.md) |
| Self-Healing & Control Loop | etcd의 목표 상태와 현재 상태를 지속 비교해 비정상 Pod를 자동 복구하는 조정 루프 | [Reconciliation Loop의 계보](../../99_ETC/2026-04-19_Reconciliation Loop의 계보 — 제어이론에서 GitOps까지.md) |
| High Availability & Cascade Failure | SPOF 없는 다중 복제 구조 및 트래픽 폭증 시 Pod 전멸을 방어하는 Rate Limit·QoS 설계 | [Deployment Models — 배포 모델과 고가용성 인프라 구축](../../08_cloud/book/production-kubernetes/02-01.Deployment Models — 배포 모델과 고가용성 인프라 구축.md) |
| AWS Nitro & MicroVM | 전용 하드웨어 칩 오프로딩으로 하이퍼바이저 부하를 줄여 VM 격리 보안과 고성능을 양립 | [클라우드 컴퓨팅 — 하드웨어 가상화](../../02_os/book/systems-performance/11-02.클라우드 컴퓨팅 — 하드웨어 가상화.md) |



## 요점

- 쿠버네티스는 선언적 목표 상태 관리와 조정을 담당하고 실제 프로세스 격리·자원 통제는 호스트 커널이 집행함
- `kubelet` → `containerd` → `runc`를 거쳐 커널 cgroups에 상한이 기록되며 물리적 통제권은 커널에 있음
- 메모리 상한(`memory.max`) 초과 시 커널 OOM Killer가 `SIGKILL(9)`로 강제 종료하며 종료 코드 137(128+9) 반환
- `limits.cpu`는 커널 CFS 대역폭 제어기(`cpu.max`)에 매핑되며 100ms 주기 내 quota 소진 시 CPU 쓰로틀링 발생
- `kubectl top`은 주기 평균치만 표시하므로 P99 지연 분석 시 노드의 `cpu.stat` 원천 메트릭(`nr_throttled`) 확인 필수
- 자가 치유(Self-Healing) 루프는 개별 컨테이너 종료를 복구하지만 트래픽 폭증형 연쇄 장애(Cascade Failure)를 막지 못함
- 연쇄 장애 방지를 위해 Ingress Rate Limiting, 호출단 Circuit Breaker, HPA, 적절한 자원 산정 병행 필수
- VM(AWS Nitro)은 하드웨어 수준의 멀티테넌트 보안 격리를 담당하고 컨테이너는 빠른 기동과 실행 효율을 제공해 상호 보완함



## 경고

- ⚠ "Linux 6.6+에서 CFS가 EEVDF로 대체됨" — 최신 커널 사실이나 Ubuntu 22.04 LTS 등은 여전히 CFS가 기본입니다 (원문 42줄, 558줄). — 확인됨: [Linux v6.6 kernel/sched/fair.c](https://raw.githubusercontent.com/torvalds/linux/v6.6/kernel/sched/fair.c) (v6.5 에는 EEVDF 가 없고 v6.6 에 있음, Ubuntu 22.04 서술은 미확인)
- ⚠ "AWS Nitro는 가상화 오버헤드가 1% 미만" — 전용 칩 오프로딩 장점이나 I/O 패턴에 따라 체감 오버헤드 차이 존재 (원문 76줄, 635줄) — 미확인: 벤더 수치라 공식 문서 대상 아님
- ⚠ "노드 OOM 방지를 위해 Guaranteed QoS(requests==limits) 설정이 표준" — 자원 집적도 및 비용 최적화와 상충되어 일괄 표준은 아님 (원문 600줄) — 미확인: 운영 설계 의견, 공식 단정 근거 없음
- ⚠ "CPU Throttling 방지를 위해 limits를 빼고 requests만 설정 권장" — 지연 개선되나 노이즈 이웃(Noisy Neighbor) 간섭 위험 존재 (원문 614줄) — 미확인: 운영 판단 사항, 공식 근거 없음
