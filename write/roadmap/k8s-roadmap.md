---
title: Kubernetes 학습 로드맵
tags: [roadmap, kubernetes, k8s, cloud-native, operations]
status: final
related:
  - README.md
  - os-roadmap.md
  - network-roadmap.md
  - ../08_cloud/kubernetes/README.md
updated: 2026-09-12
---

# Kubernetes 학습 로드맵
---

> 오브젝트를 배포하는 데서 시작해 연결, 자원, 내부 구조, 확장, 운영 장애 순서로 Kubernetes를 학습합니다.

![오브젝트 배포에서 클러스터 운영까지 이어지는 Kubernetes 학습 순서](_assets/k8s-roadmap.svg)

## 학습 순서

> Kubernetes에서 직접 보이는 오브젝트와 운영 경로를 다룹니다. Linux 커널 구현과 네트워크 데이터패스는 연결된 로드맵에서 이어갑니다.

| 단계 | 우선순위 | 주제 | 키워드 | 학습 문서 | 완료 기준 |
|---|:---:|---|---|---|---|
| 1. 오브젝트 | 필수 | 선수지식 · API·Pod 생애주기 | API resource·manifest<br>metadata·spec·status<br>Pod phase·container state·event<br>namespace·label | [Kubernetes in Action](../08_cloud/book/kubernetes-in-action/README.md) · [Kubernetes MOC](../08_cloud/kubernetes/README.md) | `kubectl describe pod`에서 Pod가 멈춘 생애주기 지점을 찾습니다. |
| 1. 오브젝트 | 필수 | 실습·진단 · 설정·상태 확인 | ConfigMap·Secret·Downward API<br>env·projected volume<br>liveness/readiness/startup probe<br>lifecycle hook | [Kubernetes in Action](../08_cloud/book/kubernetes-in-action/README.md) | 설정 주입 방식과 probe의 목적을 구분하고 재시작 원인을 설명합니다. |
| 2. 워크로드 | 필수 | 핵심 · Deployment·ReplicaSet | reconciliation·Pod template·revision<br>RollingUpdate·`maxSurge/maxUnavailable`<br>rollback | [Kubernetes in Action](../08_cloud/book/kubernetes-in-action/README.md) | rollout이 멈춘 원인을 readiness, 자원, 배포 전략에서 찾습니다. |
| 2. 워크로드 | 필수 | 실습 · 상태·노드·배치 작업 | StatefulSet·ordinal·headless Service<br>DaemonSet·Job·CronJob<br>init container·sidecar | [Kubernetes in Action](../08_cloud/book/kubernetes-in-action/README.md) | 워크로드 성격에 맞는 컨트롤러를 선택하고 소유 관계를 설명합니다. |
| 3. 연결 | 필수 | 핵심·진단 · Service·DNS | ClusterIP·NodePort·LoadBalancer<br>selector·EndpointSlice<br>CoreDNS·Service FQDN | [Service와 EndpointSlice](../08_cloud/kubernetes/04_networking/04-04.Service%EC%99%80%20EndpointSlice.md) · [DNS와 CoreDNS](../08_cloud/kubernetes/04_networking/04-05.DNS%EC%99%80%20CoreDNS.md) | Service 장애를 DNS, selector, endpoint 중 어느 층에서 확인할지 가릅니다. |
| 3. 연결 | 필수 | 실습·진단 · 외부 진입·정책 | Ingress·IngressClass<br>Gateway·HTTPRoute·TLS Secret<br>NetworkPolicy·default deny | [Ingress와 Gateway API](../08_cloud/kubernetes/04_networking/04-06.Ingress%EC%99%80%20Gateway%20API.md) · [NetworkPolicy](../08_cloud/kubernetes/04_networking/04-07.NetworkPolicy.md) | 외부 요청의 라우팅 규칙과 허용 정책을 오브젝트 수준에서 확인합니다. |
| 3. 연결 | 추천 | 핵심 · 네트워크 데이터패스 | CNI·Pod CIDR·veth<br>overlay·kube-proxy·iptables<br>eBPF·Cilium | [네트워크 로드맵](network-roadmap.md) · [Pod 네트워크와 Linux 기반](../08_cloud/kubernetes/04_networking/04-02.Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20Linux%20%EA%B8%B0%EB%B0%98.md) | 오브젝트가 정상일 때 패킷 경로의 다음 확인 지점을 찾습니다. |
| 4. 자원·저장 | 필수 | 선수지식 · requests·limits·스케줄링 | CPU/memory request·limit·QoS<br>taint·toleration·affinity<br>topology spread·PriorityClass·eviction | [스케줄링과 노드 선택](../08_cloud/kubernetes/05_scheduling/05-01.%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%EA%B3%BC%20%EB%85%B8%EB%93%9C%20%EC%84%A0%ED%83%9D.md) · [토폴로지 분산과 중단 정책](../08_cloud/kubernetes/05_scheduling/05-02.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EB%B6%84%EC%82%B0%EA%B3%BC%20%EC%A4%91%EB%8B%A8%20%EC%A0%95%EC%B1%85.md) | Pending 원인을 자원, 배치 조건, 축출 정책으로 나눕니다. |
| 4. 자원·저장 | 필수 | 핵심·진단 · 볼륨 | Volume·PV·PVC·StorageClass<br>CSI·access mode·reclaim policy<br>dynamic provisioning·snapshot | [Kubernetes in Action](../08_cloud/book/kubernetes-in-action/README.md) | PVC가 Pending인 원인을 StorageClass, zone, 접근 모드에서 찾습니다. |
| 4. 자원·저장 | 추천 | 실습 · 오토스케일링 | HPA·VPA·Cluster Autoscaler<br>KEDA·metrics-server·custom metric | [오토스케일링](../08_cloud/kubernetes/05_scheduling/05-03.%EC%98%A4%ED%86%A0%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | 부하 신호와 확장 대상을 맞춰 수평·수직·노드 확장을 구분합니다. |
| 5. 내부 구조 | 필수 | 핵심 · Control Plane·노드 | API Server·etcd·Scheduler<br>Controller Manager·kubelet<br>CRI·CNI·CSI·containerd | [Kubernetes MOC](../08_cloud/kubernetes/README.md) · [클러스터 업그레이드와 etcd 백업·복구](../08_cloud/kubernetes/06_architecture/06-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | `kubectl apply` 이후 각 구성 요소가 맡는 결정을 순서대로 설명합니다. |
| 5. 내부 구조 | 필수 | 실습·진단 · API 보안·etcd | authentication·authorization·admission<br>TLS·PKI·watch<br>quorum·Raft·backup/restore | [TLS와 API 접근 보안](../08_cloud/kubernetes/06_architecture/06-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) · [etcd 백업·복구](../08_cloud/kubernetes/06_architecture/06-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | Control Plane 장애에서 멈추는 결정과 계속 실행되는 워크로드를 구분합니다. |
| 6. 보안·확장 | 필수 | 핵심·실습 · RBAC·Pod 보안 | Role/RoleBinding·ClusterRole<br>ServiceAccount·SecurityContext<br>capability·seccomp·admission policy | [Kubernetes Patterns](../08_cloud/book/kubernetes-patterns/README.md) · [Container Security](../08_cloud/book/container-security/README.md) · [OS 로드맵](os-roadmap.md) | 주체, 권한 범위, 실행 권한을 각각 최소화합니다. |
| 6. 보안·확장 | 추천 | 핵심 · Controller·Operator | reconciliation loop·work queue<br>CRD·custom resource·controller<br>finalizer·OwnerReference·status subresource | [Kubernetes Patterns](../08_cloud/book/kubernetes-patterns/README.md) · [Kubernetes: Up and Running](../08_cloud/book/kubernetes-up-and-running/README.md) | 원하는 상태와 현재 상태의 차이를 반복 조정하는 컨트롤러를 설명합니다. |
| 7. 운영 | 필수 | 선수지식·진단 · 이벤트·로그·지표 | `kubectl describe`·events<br>current/previous logs·JSONPath<br>metrics-server·kube-state-metrics·node exporter | [모니터링과 트러블슈팅](../08_cloud/kubernetes/09_operations/09-01.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EA%B3%BC%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.md) · [JSONPath와 kubectl](../08_cloud/kubernetes/09_operations/09-03.JSONPath%EC%99%80%20kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | 이벤트, 로그, 지표를 같은 시간축으로 연결해 재시작 원인을 좁힙니다. |
| 7. 운영 | 필수 | 실습·진단 · OOMKilled·CPU throttling | cgroup v2·`memory.max/events`<br>RSS·page cache·JVM native memory<br>`cpu.stat`·exit code 137 | [OOMKilled 사례 분석](../08_cloud/kubernetes/09_operations/09-02.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) · [cgroup v2 깊이](../02_os/kernel/01-02.cgroup%20v2%20%EA%B9%8A%EC%9D%B4.md) · [OS 로드맵](os-roadmap.md) | Java OOM, cgroup OOMKilled, CPU 제한에 따른 지연을 구분합니다. |
| 7. 운영 | 필수 | 실습·진단 · 종료·복구 | SIGTERM·PID 1·PreStop<br>readiness·`terminationGracePeriodSeconds`<br>finalizer·PDB·NodeNotReady | [커널과 컨테이너](../02_os/kernel/01-01.%EC%BB%A4%EB%84%90%EA%B3%BC%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) · [Kubernetes 장애 기록](../troubleshooting/kubernetes/README.md) | Pod 종료 지연과 강제 종료를 애플리케이션, 오브젝트, 커널 신호로 나눕니다. |



## 책 읽기 흐름

> 단계 표에 연결된 책을 처음 읽는 시점과 집중할 범위를 표시합니다.

![Kubernetes 책 읽기 흐름](_assets/k8s-books.svg)
