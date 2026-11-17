> 출처: NotebookLM · 2026-11-16 · 쿠버네티스 네트워킹 — Service 타입과 NetworkPolicy (영상 「Kubernetes FULL COURSE Part 10 Kubernetes Networking – Services, Policies & Demos」 자막 분석) · 분야: k8s-keywords, network-keywords · 미검증

## 요점

한 줄: Service 는 바뀌는 Pod IP 앞에 고정 가상 IP 와 DNS 이름을 세우고, NetworkPolicy 는 기본 전부 허용인 클러스터를 라벨 단위 허용 목록으로 잠급니다. 둘 다 IP 가 아니라 라벨 셀렉터로 설계합니다.

- 두 문제:
  - Pod 는 스케일·장애 복구·롤링 업데이트 때 다른 노드에서 새 IP 로 다시 뜹니다. 그래서 Pod IP 를 직접 적어 통신할 수 없습니다.
  - 정책이 없으면 다른 네임스페이스까지 모든 Pod 가 서로 제한 없이 통신합니다.
- Service 추적: `selector` 에 맞는 Pod 목록을 Endpoints·EndpointSlice 로 계속 갱신합니다. 클라이언트는 고정 IP 나 이름만 부릅니다.
- 세 타입의 누적 구조:
  - ClusterIP(기본): 클러스터 안에서만 닿는 가상 IP 로, 서비스 간 내부 통신의 표준입니다.
  - NodePort: ClusterIP 위에 모든 노드의 같은 포트(30000–32767)를 엽니다. 어느 노드로 들어와도 건강한 Pod 로 갑니다.
  - LoadBalancer: NodePort 위에 외부 로드밸런서 IP 를 붙입니다. 쿠버네티스에 내장돼 있지 않아 클라우드나 베어메탈용 컨트롤러가 필요합니다.
- 포트 세 단계: 바깥 `nodePort` → Service 의 `port` → 컨테이너가 듣는 `targetPort` 순으로 넘어갑니다. 한 Service 에 포트를 여럿 두어 같은 Pod 의 다른 컨테이너로 나눌 수 있습니다.
- kube-proxy 의 실제 역할: 요청을 받아 중계하지 않습니다. API 서버의 Service·엔드포인트 변경을 보고 커널 NAT 규칙(iptables·IPVS·nftables)을 고쳐 두면 커널이 목적지를 바꿉니다.
- 비정상 Pod 제외: kube-proxy 가 요청마다 헬스 체크를 하는 게 아닙니다. Readiness Probe 를 통과한 Pod 만 EndpointSlice 에 올라가 트래픽이 갑니다.
- NetworkPolicy 평가:
  - 네임스페이스 범위 리소스입니다. Pod 가 한 정책의 `podSelector` 에 걸리는 순간 `policyTypes` 에 적힌 방향이 허용 목록 모드로 바뀝니다.
  - `podSelector: {}` 에 허용 규칙을 비워 두면 그 네임스페이스의 모든 트래픽이 막힙니다(Default Deny).
  - `from`·`to` 의 항목은 서로 OR 입니다. `namespaceSelector` 와 `podSelector` 를 대시 하나로 묶으면 AND 가 돼, 대시 하나 차이로 뜻이 뒤집힙니다.
- CNI 의존: 정책을 강제하지 못하는 CNI 에서는 `kubectl apply` 가 성공해도 아무것도 막히지 않습니다. 정책을 강제하는 CNI 나 정책 컨트롤러가 있어야 합니다.
- L4 의 경계: Service 와 NetworkPolicy 는 IP·포트·라벨까지만 봅니다. 호스트·경로 라우팅은 Ingress·Gateway API, HTTP 메서드 차단과 mTLS 는 Cilium L7 정책이나 Service Mesh 몫입니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| Service 고정 VIP·DNS | 바뀌는 Pod IP 를 숨기고 변하지 않는 주소와 이름으로 묶는 추상화 | [Service 기초](../../08_cloud/book/kubernetes-in-action/11-01.Service 기초 — 파드 통신·ClusterIP·세션 어피니티.md) |
| selector·EndpointSlice | 라벨에 맞는 Pod 주소를 컨트롤 플레인이 모아 kube-proxy 에 넘기는 목록 | [StatefulSet·Endpoints·EndpointSlices](../../08_cloud/book/networking-and-kubernetes/05-01.StatefulSet·Endpoints·EndpointSlices — 서비스의 재료.md) |
| Readiness 와 엔드포인트 제외 | 준비되지 않은 Pod 를 목록에서 빼 트래픽이 가지 않게 하는 장치 | [엔드포인트·DNS·토폴로지·readiness](../../08_cloud/book/kubernetes-in-action/11-03.엔드포인트·DNS·토폴로지·readiness.md) |
| ClusterIP | 클러스터 안에서만 닿는 가상 IP 를 주는 기본 타입 | [Service 5유형](../../08_cloud/book/networking-and-kubernetes/05-02.Service 5유형 — ClusterIP에서 LoadBalancer까지.md) |
| NodePort | 모든 노드의 같은 고포트를 열어 바깥 요청을 Pod 로 넘기는 타입 | [외부 노출](../../08_cloud/book/kubernetes-in-action/11-02.외부 노출 — NodePort·LoadBalancer·트래픽 정책.md) |
| LoadBalancer·베어메탈 LB | 외부 LB IP 를 NodePort 앞에 붙이고, 클라우드가 없으면 MetalLB 같은 컨트롤러가 IP 를 알리는 구성 | [Service 5유형](../../08_cloud/book/networking-and-kubernetes/05-02.Service 5유형 — ClusterIP에서 LoadBalancer까지.md), [L2 Announcements](../../08_cloud/book/cilium-up-and-running/10-01.L2 Announcements 는 ARP 응답으로 서비스 IP 를 같은 L2 망에 알린다.md) |
| nodePort·port·targetPort | 노드 포트 → Service 포트 → 컨테이너 포트로 이어지는 세 단계 매핑 | [Service 기초](../../08_cloud/book/kubernetes-in-action/11-01.Service 기초 — 파드 통신·ClusterIP·세션 어피니티.md), [Service 5유형](../../08_cloud/book/networking-and-kubernetes/05-02.Service 5유형 — ClusterIP에서 LoadBalancer까지.md) |
| 다중 포트 Service | 한 Service 에 이름 붙은 포트를 여럿 두어 컨테이너별로 나누는 정의 | [Service 기초](../../08_cloud/book/kubernetes-in-action/11-01.Service 기초 — 파드 통신·ClusterIP·세션 어피니티.md) |
| kube-proxy 규칙 동기화 | 데이터 경로에 서지 않고 Service 변경을 커널 NAT 규칙으로 옮기는 노드 에이전트 | [CNI와 kube-proxy](../../08_cloud/book/networking-and-kubernetes/04-02.CNI와 kube-proxy — Pod 네트워크의 배선공과 로드밸런서.md) |
| 크로스 노드·externalTrafficPolicy | 다른 노드의 Pod 로 넘길 때 홉과 SNAT 가 생기고, Local 로 두면 소스 IP 를 지키는 대신 대가가 따르는 설정 | [외부 노출](../../08_cloud/book/kubernetes-in-action/11-02.외부 노출 — NodePort·LoadBalancer·트래픽 정책.md) |
| NetworkPolicy 격리 트리거 | Pod 가 정책에 선택되는 순간 그 방향을 기본 차단으로 뒤집고 허용만 더하는 규칙 | [NetworkPolicy와 DNS](../../08_cloud/book/networking-and-kubernetes/04-03.NetworkPolicy와 DNS — 클러스터 안의 방화벽과 이름.md) |
| Default Deny | 빈 `podSelector` 로 네임스페이스 전체를 잠근 뒤 필요한 경로만 여는 패턴 | [NetworkPolicy와 DNS](../../08_cloud/book/networking-and-kubernetes/04-03.NetworkPolicy와 DNS — 클러스터 안의 방화벽과 이름.md) |
| peer OR·AND 함정 | 대시 하나로 네임스페이스·Pod 셀렉터가 OR 에서 AND 로 바뀌는 YAML 문법 | [NetworkPolicy와 DNS](../../08_cloud/book/networking-and-kubernetes/04-03.NetworkPolicy와 DNS — 클러스터 안의 방화벽과 이름.md) |
| 정책 강제 CNI | 라벨을 주소 규칙으로 번역하는 CNI 나 컨트롤러가 없으면 정책이 오브젝트로만 남는 문제 | [NetworkPolicy와 DNS](../../08_cloud/book/networking-and-kubernetes/04-03.NetworkPolicy와 DNS — 클러스터 안의 방화벽과 이름.md) |
| Cilium identity 정책 | 라벨로 만든 identity 로 허용을 판정하고 L7 규칙까지 거는 eBPF 정책 엔진 | [Cilium 정책](../../08_cloud/book/cilium-up-and-running/12-01.Cilium 정책은 라벨에서 만든 identity 로 허용을 판정하고 정책이 붙으면 기본 거부가 된다.md) |
| Ingress·Gateway API·Service Mesh | L4 Service 위에서 호스트·경로 라우팅과 mTLS 를 맡는 L7 층 | [Ingress와 Service Mesh](../../08_cloud/book/networking-and-kubernetes/05-03.Ingress와 Service Mesh — L7의 두 층.md) |
| 마이크로세그멘테이션 | 경계 방어 대신 서비스 사이마다 최소 권한으로 경로를 여는 제로 트러스트 설계 | |



## 자료와 실습

- 자료:
  - [Service (Kubernetes 문서)](https://kubernetes.io/docs/concepts/services-networking/service/): 타입별 동작과 `port`·`targetPort`·`nodePort` 필드 명세입니다.
  - [Network Policies (Kubernetes 문서)](https://kubernetes.io/docs/concepts/services-networking/network-policies/): 셀렉터의 AND·OR 조합과 Default Deny 표준 예시입니다.
  - [Virtual IPs and Service Proxies (Kubernetes 문서)](https://kubernetes.io/docs/reference/networking/virtual-ips/): 프록시 모드별 패킷 처리와 `externalTrafficPolicy` 명세입니다.
  - [kubernetes-network-policy-recipes](https://github.com/ahmetb/kubernetes-network-policy-recipes): Default Deny·네임스페이스 간 허용 등 표준 정책 시나리오 14개와 도식입니다.
  - [Cracking Kubernetes Node Proxy (aka kube-proxy)](https://arthurchiao.art/blog/cracking-k8s-node-proxy/): kube-proxy 가 만드는 `KUBE-SVC`·`KUBE-SEP` 같은 체인을 실제 규칙 덤프로 해부한 블로그 글입니다.
  - 『Networking and Kubernetes』: 리포트는 2장(Linux 네트워킹)·4장(CNI)·5장(Service 와 kube-proxy)을 권합니다. [정독 노트](../../08_cloud/book/networking-and-kubernetes/README.md) 에서는 04-0x·05-0x 편입니다. 손으로 따라 할 편은 [네트워크 실습](../../08_cloud/book/networking-and-kubernetes/04-04.Kubernetes 네트워크 실습 — CNI 부재부터 정책·DNS까지.md) 입니다.
  - 『Kubernetes in Action』 2판: 리포트는 5장(Service)·13장(NetworkPolicy)을 권합니다. 정독 노트에서 Service 는 11-01~11-03 편입니다.
  - 『Zero Trust Networks』 2판 1~3장·7장: 경계 보안의 한계와 서비스 간 최소 권한 통제의 원론입니다.
  - 코드: recipes 저장소의 `01-deny-all-traffic-to-an-application.md`~`14-deny-external-egress-traffic.md` 로 정책별 차단 경계를 비교합니다. `metallb/metallb` 의 `controller/`(외부 IP 풀 할당)와 `speaker/`(ARP 응답·BGP 광고)도 봅니다.
  - 코드(심화): kubernetes `pkg/proxy/iptables/proxier.go` 의 `syncProxyRules`(Service·EndpointSlice 를 iptables 체인으로 바꿈)를 봅니다. cilium `pkg/policy/`(L3·L4·L7 정책 엔진)도 봅니다.
- 실습:
  - Level 1: `kubectl create deployment demo-deploy --image=nginx --port=80 --replicas=3` 뒤 `kubectl expose` 로 ClusterIP 를 만듭니다. 엔드포인트 목록을 `watch` 로 띄워 두고 1 → 10 → 3 으로 스케일하며, `busybox` Pod 에서 `wget -qO- demo-deploy` 로 이름 통신을 봅니다. 함정은 `--port=80` 을 빠뜨려 `expose` 가 노출할 포트를 못 찾는 것입니다. 완료: Pod 를 지워도 `CLUSTER-IP` 가 그대로이고 엔드포인트 IP 개수만 레플리카 수에 맞게 바뀝니다.
  - Level 2: Calico 나 Cilium 을 켠 kind·minikube 에서 `default` 네임스페이스에 `default-deny-ingress` 를 겁니다. `client`·`unauthorized` Pod 둘에서 `wget --timeout=3` 으로 막힌 것을 본 뒤, `run: client` 의 TCP 80 만 허용하는 정책을 더합니다. 함정은 정책을 강제하지 않는 기본 CNI 에서 실습해 모든 트래픽이 그대로 통과하는 것입니다. 완료: `client` 는 `index.html` 을 받고 `unauthorized` 는 시간 초과로 끝납니다.
  - Level 3: 워커 둘인 kind 에서 `nodeSelector` 로 Pod 를 Worker-2 에만 두고, Pod 가 없는 Worker-1 의 NodePort 로 `curl` 합니다. Worker-1 에서 `iptables-save | grep <NodePort>`(또는 `cilium bpf lb list`)와 `tcpdump` 로 노드 사이를 넘는 패킷을 봅니다. 함정은 기본값 `externalTrafficPolicy: Cluster` 에서 SNAT 로 클라이언트 IP 가 Worker-1 IP 로 덮이는 것입니다. 완료: `Cluster`·`Local` 에서 요청 성공 여부와 NGINX 로그의 클라이언트 IP 차이를 NAT 체인 흐름과 패킷 로그로 설명합니다.



## 경고

- ⚠ Endpoints API: Level 1 은 `kubectl get endpoints` 를 씁니다. 정독 노트 기준 Endpoints API 는 1.33 에서 deprecated 됐으니 `kubectl get endpointslices` 로 함께 봅니다.
- ⚠ 책 장 번호: 리포트는 『Kubernetes in Action』 2판 5장을 Service, 13장을 NetworkPolicy 로 적었습니다. 정독 노트에서 Service 는 11장입니다. 『Networking and Kubernetes』·『Zero Trust Networks』 장 범위도 목차로 대조하지 않았습니다.
- ⚠ 영상 비유의 한계: 영상은 kube-proxy 가 건강한 Pod 를 골라 준다고 비유했습니다. 리포트가 커널 NAT 와 EndpointSlice 컨트롤러로 바로잡았고, 위 요점은 바로잡은 쪽을 따릅니다.
- ⚠ 부하 분산 방식: 리포트는 Service 분산을 라운드 로빈으로 적었습니다. iptables 모드는 확률 규칙으로 무작위 선택이라 모드마다 다릅니다.
- ⚠ 자막 교정: 자동 자막의 오인식(`cube control`, `cider range`, `node balancers` 등)은 리포트가 고쳤습니다.
