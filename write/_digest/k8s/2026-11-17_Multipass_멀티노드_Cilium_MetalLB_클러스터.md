> 출처: 외부 AI 대화 · 2026-11-17 · Multipass 기반 Multi-Node Kubernetes 클러스터 확장 구축 가이드 (Cilium eBPF + MetalLB + 커널 패킷 검증) · 분야: k8s-keywords · 미검증

## 요점

한 줄: Multipass VM 3대에 kube-proxy 없는 kubeadm 클러스터를 세우고, Cilium eBPF 와 MetalLB L2 위에서 트래픽·보안 정책과 노드 장애를 시험하는 구축 가이드입니다.

- 구성: Ubuntu 24.04 VM 3대(`k8s-cp`, `k8s-worker1`, `k8s-worker2`), K8s v1.32, Cilium 1.17.1, MetalLB v0.14.9 입니다.
- 노드 공통 준비는 cloud-init 파일 하나로 부팅 때 끝냅니다. 커널 모듈, sysctl, swap 끄기, containerd, kubeadm·kubelet·kubectl 설치가 들어갑니다.
- kube-proxy 는 처음부터 깔지 않습니다. `kubeadm init` 에서 kube-proxy 애드온 단계를 건너뛰므로 iptables 의 `KUBE-SERVICES` 체인이 생기지 않습니다.
- kube-proxy 가 없으면 ClusterIP `10.96.0.1` 로는 API 서버에 닿지 못합니다. 그래서 Cilium 에이전트에 컨트롤 플레인 노드의 실제 주소와 6443 포트를 직접 줍니다.
- 서비스 주소 변환은 iptables 체인 대신 BPF 맵에서 합니다. 리포트는 워커에 `KUBE-SERVICES` 가 없는지와 BPF 서비스 맵에 ClusterIP 가 올라왔는지를 확인 방법으로 듭니다.
- 클라우드가 없으면 `LoadBalancer` 서비스의 `EXTERNAL-IP` 가 `<pending>` 에 머뭅니다. MetalLB 가 VM 브리지 대역의 남는 주소를 풀로 받아 ARP 응답으로 알립니다.
- 머리말은 Gateway API·Ingress 기반 L7 진입까지 다룬다고 예고하지만 본문에는 그 절이 없습니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| Multipass | 명령 한 줄로 Ubuntu VM 을 띄우는 Canonical 의 VM 도구. `launch`·`exec`·`transfer`·`stop`·`delete --purge` 로 다룸 | |
| cloud-init 노드 부트스트랩 | 첫 부팅 때 패키지·파일·명령을 적용하는 설정. 여기서는 `overlay`·`br_netfilter` 모듈, sysctl, swap 끄기를 맡음 | [커널이 패킷을 판정하는 층](../../08_cloud/book/networking-and-kubernetes/02-02.커널이 패킷을 판정하는 층 — Netfilter·Conntrack·라우팅.md) (일부: `br_netfilter` 를 sysctl 보다 먼저 올리는 이유 한 문단, cloud-init 명세·swap 없음) |
| containerd `SystemdCgroup` | kubelet 과 컨테이너 런타임의 cgroup 드라이버를 systemd 로 맞추는 설정 | [컨테이너 런타임 인터페이스·crictl](../../08_cloud/docs/kubernetes/architecture/컨테이너 런타임 인터페이스·crictl.md) |
| kubeadm init·join (`--print-join-command`) | 컨트롤 플레인을 세우고, 토큰과 CA 해시가 든 조인 명령을 뽑아 워커를 붙이는 절차 | [노드 추가·제거](../../08_cloud/docs/kubernetes/operations/노드 추가·제거.md) |
| Cilium kube-proxy 대체 (`kubeProxyReplacement`·`k8sServiceHost`) | kube-proxy 를 빼고 에이전트가 API 서버 실제 주소로 붙어 서비스 로드밸런싱을 eBPF 로 하는 모드. `kubeadm init --skip-phases=addon/kube-proxy` 와 짝 | [Cilium 은 kube-proxy 를 eBPF 로 대신한다](../../08_cloud/book/cilium-up-and-running/06-01.Cilium 은 kube-proxy 를 eBPF 로 대신하고 외부 서비스에 IP 와 경로를 붙인다.md) (일부: kind 설치 기준, kubeadm 단계 생략 없음) |
| Cilium cluster-pool IPAM | operator 가 `clusterPoolIPv4PodCIDRList` 대역을 노드별 PodCIDR 로 나눠 주는 Cilium 기본 IPAM | [Cilium IPAM 모드](../../08_cloud/book/cilium-up-and-running/04-01.Cilium IPAM 모드는 Pod 대역을 누가 나눠 주는지로 갈린다.md) |
| BPF 서비스 맵 vs `KUBE-SERVICES` | 서비스→백엔드 변환을 iptables 체인 대신 eBPF 맵 조회로 하는 구조 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| Hubble (Relay·UI) | 노드별 흐름 기록을 Relay 로 모아 CLI·UI 로 보는 Cilium 관측 계층 | [Hubble 은 노드마다 흐름을 모아 Relay 로 묶는다](../../08_cloud/book/cilium-up-and-running/15-01.Hubble 은 노드마다 흐름을 모아 Relay 로 묶고 L7 가시성과 지표로 내보낸다.md) |
| MetalLB L2 (`IPAddressPool`·`L2Advertisement`) | 주소 풀을 CRD 로 주고, 한 노드가 ARP 로 그 IP 를 자기 것이라 답하는 베어메탈 LoadBalancer | [Service 5유형](../../08_cloud/book/networking-and-kubernetes/05-02.Service 5유형 — ClusterIP에서 LoadBalancer까지.md) (일부: 책 예제는 ConfigMap 옛 형식, CRD 전환은 한 줄) |
| `externalTrafficPolicy` Cluster·Local | 다른 노드로 넘길 때 SNAT 로 출발지 IP 를 잃는 Cluster 와, 로컬 Pod 로만 보내 출발지를 지키는 Local 의 차이 | [외부 노출](../../08_cloud/book/kubernetes-in-action/11-02.외부 노출 — NodePort·LoadBalancer·트래픽 정책.md) |
| CiliumNetworkPolicy·identity | IP 대신 라벨에서 만든 identity 로 허용을 판정하는 Cilium 정책 | [Cilium 정책은 identity 로 허용을 판정한다](../../08_cloud/book/cilium-up-and-running/12-01.Cilium 정책은 라벨에서 만든 identity 로 허용을 판정하고 정책이 붙으면 기본 거부가 된다.md) |
| 노드 장애 축출 (`not-ready`·`unreachable` taint) | 노드가 응답하지 않으면 taint 가 붙고, 기본 `tolerationSeconds=300` 뒤 Pod 가 축출되는 흐름 | [ReplicaSet 컨트롤러](../../08_cloud/book/kubernetes-in-action/14-02.ReplicaSet 컨트롤러 — reconciliation·장애복구·삭제.md) (일부: 장애 복구 절의 보강 상자, `node-monitor-grace-period` 없음) |



## 자료와 실습

- 실습:
  - 1단계 노드 부트스트랩: cloud-init 파일 하나가 `overlay`·`br_netfilter` 모듈과 sysctl(브리지 트래픽의 iptables 통과, IP 포워딩), swap 끄기를 맡습니다. 같은 파일이 containerd(`SystemdCgroup = true`)와 kubeadm·kubelet·kubectl v1.32 를 깔고 `apt-mark hold` 로 묶습니다. 완료: 세 노드에서 `cloud-init status --wait` 가 끝납니다.
  - 2단계 VM 3대: `multipass launch 24.04 --name <노드> --cpus 2 --memory 2.5G --disk 20G --cloud-init <파일>` 을 노드마다 돌립니다. 완료: `multipass list` 에 세 노드와 주소가 보입니다. 함정: 리포트의 노드 주소는 예시입니다(경고 참고).
  - 3단계 kubeadm init·join: `kubeadm init` 에 `--apiserver-advertise-address`·`--pod-network-cidr`·`--service-cidr`·`--skip-phases=addon/kube-proxy` 를 줍니다. kubeconfig 는 `multipass transfer` 로 호스트에 가져옵니다. 워커는 `kubeadm token create --print-join-command` 결과로 조인합니다. 완료: CNI 가 없어 세 노드 모두 `NotReady` 이고 `kube-system` 에 kube-proxy DaemonSet 이 없습니다. 함정: 대역 겹침과 조인 명령 변수 펼치기(경고 참고).
  - 4단계 Cilium·Hubble: Helm 차트 `cilium/cilium --version 1.17.1` 에 `kubeProxyReplacement=true` 와 `k8sServiceHost=<CP 주소>`·`k8sServicePort=6443` 을 줍니다. Pod 대역은 `ipam.operator.clusterPoolIPv4PodCIDRList` 로 정하고 Hubble Relay·UI 를 켭니다. 완료: `cilium` DaemonSet rollout 이 끝나 노드가 Ready 가 됩니다. 워커의 `iptables-save -t nat` 에는 `KUBE-SERVICES` 가 없고, BPF 서비스 맵에는 `10.96.0.1`·`10.96.0.10` 이 있습니다. 함정: 맵 조회 명령 이름(경고 참고).
  - 5단계 MetalLB L2: v0.14.9 `metallb-native.yaml` 을 적용하고 `IPAddressPool`(브리지 대역의 남는 구간)과 `L2Advertisement` 를 선언합니다. 완료: `type: LoadBalancer` 서비스가 `<pending>` 대신 풀의 주소를 받습니다. 함정: 리포트도 풀 구간을 `multipass list` 대역에 맞추라고 적습니다.
  - 시나리오 A `externalTrafficPolicy`: `traefik/whoami` 2개를 LoadBalancer 로 노출해 반복 호출하고, `Cluster` 와 `Local` 에서 응답의 클라이언트 주소를 비교합니다. 완료: `Cluster` 에서는 워커 노드 주소, `Local` 에서는 원래 클라이언트 주소가 보이고 Pod 없는 노드로는 가지 않습니다. 함정: 헤더 서술과 curl 표기(경고 참고).
  - 시나리오 B CiliumNetworkPolicy: `app: whoami` 로 들어오는 TCP 80 을 `role: frontend` 라벨에만 허용합니다. 완료: `role=frontend` Pod 의 curl 은 응답을 받고, `role=rogue` Pod 의 `curl -m 3` 은 드롭돼 시간 초과로 끝납니다.
  - 시나리오 C Hubble: `cilium hubble port-forward` 뒤 `hubble observe --pod whoami --follow` 를 돌리거나 `cilium hubble ui` 를 엽니다. 완료: whoami Pod 의 L3/L4 흐름이 실시간으로 나옵니다.
  - 시나리오 D 노드 장애: `multipass stop k8s-worker2` 뒤 `kubectl get nodes -w` 와 `kubectl get pods -o wide -w` 를 함께 봅니다. 완료: worker2 가 `NotReady` 가 되고 그 노드의 Pod 가 worker1 에 다시 뜨며, `multipass start` 뒤 노드가 돌아옵니다. 함정: 리포트가 적은 전환 시간과 재스케줄 시점(경고 참고).



## 경고

- ⚠ NotReady 까지의 시간: 리포트는 「약 40초 후 NotReady」 라고 적습니다. v1.32 의 `--node-monitor-grace-period` 기본값은 50s 입니다([kube-controller-manager v1.32 레퍼런스](https://v1-32.docs.kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/), 확인됨). 40s 가 어느 버전까지의 기본값이었는지는 확인하지 않았습니다.
- ⚠ 재스케줄 시점: 리포트는 NotReady 와 동시에 Pod 가 `Terminating` 되고 새 Pod 가 뜬다고 적습니다. 기본으로는 `not-ready`·`unreachable` taint 에 대한 `tolerationSeconds=300` toleration 이 Pod 에 자동으로 붙습니다. 그래서 Pod 는 5분 동안 그 노드에 묶여 있다가 축출됩니다([Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/), 확인됨).
- ⚠ 대역 겹침: `--pod-network-cidr=10.0.0.0/8` 과 Cilium `clusterPoolIPv4PodCIDRList` 의 `10.0.0.0/8` 은 `--service-cidr=10.96.0.0/12` 를 포함합니다. Cilium [Cluster Scope IPAM 문서](https://docs.cilium.io/en/v1.17/network/concepts/ipam/cluster-pool/)는 `10.0.0.0/8` 이 노드 대역과 겹치면 다른 노드와 연결을 잃는다고만 경고하고 서비스 대역 겹침은 다루지 않습니다. 겹침이 실제로 장애를 내는지는 확인하지 못했습니다.
- ⚠ MetalLB 모드 표기: 머리말의 「L2 BGP/ARP」 는 두 모드를 섞은 표기입니다. MetalLB 는 L2(ARP/NDP) 모드와 BGP 모드를 따로 두고, 이 가이드가 쓰는 것은 L2 입니다([MetalLB Concepts](https://metallb.io/concepts/), 확인됨).
- ⚠ Multipass 대역: 리포트의 브리지 대역 `192.168.64.0/24` 와 노드 주소 `.10/.11/.12` 는 예시입니다. Multipass 1.17 부터 macOS 는 가용 영역마다 `192.168.252.0/16` 에서 /24 를 받습니다([Troubleshoot networking](https://canonical.com/multipass/docs/en/latest/how-to-guides/troubleshoot/troubleshoot-networking/), 확인됨). 리포트에는 노드 주소를 고정하는 설정이 없습니다. MetalLB 풀이 주소 배정 범위와 겹칠 위험은 문서로 확인하지 못했습니다.
- ⚠ `stop` 과 `suspend`: 리포트는 `multipass stop` 을 시나리오 D 에서 「전원 강제 차단」, 치트시트에서 「상태 보존 일시 중지」 라고 적습니다. 문서상 Stopped 는 자원을 쓰지 않는 정지 상태이고, 상태와 메모리를 저장하는 것은 Suspended 입니다([Instance states](https://canonical.com/multipass/docs/en/latest/reference/instance-states/), 확인됨). `stop` 은 종료(shutdown)이고 응답 없는 인스턴스를 끄는 `--force` 가 따로 있습니다([multipass stop](https://canonical.com/multipass/docs/en/latest/reference/command-line-interface/stop/), 확인됨).
- ⚠ 클라이언트 주소 서술: `Cluster` 정책의 LoadBalancer 는 기본으로 SNAT 되어 출발지가 노드 IP 로 바뀝니다. `X-Forwarded-For` 는 프록시형 LB 가 진짜 클라이언트 IP 를 넘길 때 쓰는 헤더로만 나옵니다([Using Source IP](https://kubernetes.io/docs/tutorials/services/source-ip/), 확인됨). 그러니 이 구성에서 그 헤더에 노드 IP 가 찍힌다는 서술은 근거가 없고, 바뀌는 것은 whoami 의 `RemoteAddr` 입니다. 시나리오 A 의 `curl [http://…](http://…)` 는 마크다운 잔재이고 실제 명령은 `curl http://<EXTERNAL-IP>` 입니다.
- ⚠ BPF 맵 조회 명령: 리포트의 `cilium bpf lb list` 는 Cilium 1.17 명령 레퍼런스에 `cilium-dbg bpf lb list` 로 있습니다([cmdref](https://docs.cilium.io/en/v1.17/cmdref/cilium-dbg_bpf_lb_list/), 확인됨). 디버그 CLI 는 1.15 에서 이름이 바뀌었습니다.
- ⚠ 조인 명령 변수: 리포트는 호스트에서 `${JOIN_CMD}` 를 따옴표 없이 펼쳐 넘깁니다. bash 는 낱말로 나누지만 macOS 기본 셸 zsh 는 나누지 않아 명령 전체가 한 낱말로 넘어가 `command not found` 가 납니다. 로컬 zsh 로 잰 결과이고 공식 문서와 대조하지 않았습니다. zsh 에서는 `${=JOIN_CMD}` 로 나눠 펼칩니다.
- ⚠ 버전 조합: Cilium 1.17 호환표에는 K8s 1.29~1.32 가 있습니다([Kubernetes Compatibility](https://docs.cilium.io/en/v1.17/network/kubernetes/compatibility/), 확인됨). MetalLB 는 버전별 표 없이 K8s 1.13 이상만 요구합니다([MetalLB Requirements](https://metallb.io/#requirements), 확인됨). 네트워크 애드온 표에는 Cilium 이 Yes 로 있습니다([Network Addon Compatibility](https://metallb.io/installation/network-addons/), 확인됨). kube-proxy 대체 모드와의 조합은 문서에 언급이 없습니다.
- ⚠ 과장 표현: 「대규모 클러스터 표준」, 「엔드투엔드 프로덕션 유사 클러스터」, 「커널 계층까지 완전히 재현」 은 리포트의 표현이고 근거가 없습니다.
- ⚠ 예고만 있고 본문 없음: 머리말의 「Kubernetes Gateway API / Ingress 기반 외부 L7 트래픽 진입」 은 본문에 절이 없습니다.
