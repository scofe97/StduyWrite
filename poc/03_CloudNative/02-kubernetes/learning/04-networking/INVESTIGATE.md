# Ch04. 네트워킹 - 점검 질문

## Q1. kube-proxy의 iptables 모드와 IPVS 모드 차이

**질문**: kube-proxy가 Service 트래픽을 라우팅할 때 iptables 모드와 IPVS 모드는 어떻게 다르며, 각각 어떤 상황에서 선택해야 하는가?

**핵심 포인트**:

1. **iptables 모드의 동작 원리**
   - Service와 Endpoint 변경 시 리눅스 iptables 규칙 생성/삭제
   - 확률 기반 로드밸런싱 (--probability 0.33 등)
   - O(n) 선형 탐색 (규칙 체인을 순차적으로 평가)
   - 연결 추적(conntrack)으로 세션 유지
   - Pod 수가 많아질수록 규칙 수 증가 → 지연 증가

2. **IPVS 모드의 동작 원리**
   - 리눅스 커널의 IPVS (IP Virtual Server) 사용
   - 해시 테이블 기반 O(1) 조회
   - 다양한 로드밸런싱 알고리즘 (rr, lc, dh, sh, sed, nq)
   - 대규모 클러스터에서 성능 우수 (10,000+ Service도 낮은 지연)
   - ipvsadm 커널 모듈 필요

3. **성능 차이**
   | 측면 | iptables | IPVS |
   |------|----------|------|
   | Service 100개 | 밀리초 지연 | 마이크로초 지연 |
   | Service 10,000개 | 초 단위 지연 | 밀리초 지연 |
   | 규칙 업데이트 | O(n) | O(1) |
   | CPU 사용량 | 높음 (규칙 평가) | 낮음 (해시 조회) |
   | 메모리 사용량 | 규칙 수에 비례 | 해시 테이블 고정 |

4. **선택 기준**
   - **iptables 선택**: 소규모 클러스터 (<1000 Service), 기본 설정 유지, 특수 iptables 규칙 활용
   - **IPVS 선택**: 대규모 클러스터, 낮은 지연 필수, 고급 로드밸런싱 알고리즘 필요
   - **전환 시점**: Service 응답 시간이 증가하거나 kube-proxy CPU 사용률 높을 때

**심화 질문**:
- IPVS 모드에서도 iptables를 사용하는 이유는? (NodePort, Masquerading, NetworkPolicy는 여전히 iptables 사용)
- iptables 모드에서 백엔드 Pod 선택의 확률 분포는 정확히 균등한가? (초기 Pod은 낮은 확률, 마지막 Pod은 1.0 확률 → 시간이 지나면 수렴)
- IPVS의 'sh' 알고리즘(Source Hashing)과 SessionAffinity의 차이는? (sh는 소스 IP 해싱, SessionAffinity는 conntrack 기반)

---

## Q2. ClusterIP Service의 내부 로드밸런싱 동작 과정

**질문**: ClusterIP Service에 요청을 보냈을 때, kube-proxy가 어떻게 여러 Pod 중 하나를 선택하고 트래픽을 전달하는가?

**핵심 포인트**:

1. **요청 흐름 (iptables 모드)**
   ```
   클라이언트 Pod (10.244.1.5)
       ↓ curl http://backend:80
   커널 네트워크 스택
       ↓ 목적지: 10.96.5.10:80 (Service ClusterIP)
   iptables PREROUTING 체인
       ↓ KUBE-SERVICES 규칙 매칭
   KUBE-SVC-XXXX 체인 (Service 전용)
       ↓ 확률 기반 분기 (33%, 50%, 100%)
   KUBE-SEP-AAA 체인 (개별 Endpoint)
       ↓ DNAT 10.96.5.10:80 → 10.244.2.10:8080
   라우팅 결정
       ↓ Pod 네트워크 (CNI)
   백엔드 Pod (10.244.2.10)
   ```

2. **iptables 규칙 상세**
   ```bash
   # Service 규칙 (진입점)
   -A KUBE-SERVICES -d 10.96.5.10/32 -p tcp --dport 80 -j KUBE-SVC-XXXX

   # 백엔드 분기 (3개 Pod 가정)
   -A KUBE-SVC-XXXX -m statistic --mode random --probability 0.33333 -j KUBE-SEP-AAA
   -A KUBE-SVC-XXXX -m statistic --mode random --probability 0.50000 -j KUBE-SEP-BBB
   -A KUBE-SVC-XXXX -j KUBE-SEP-CCC  # 남은 확률 100%

   # 개별 Endpoint DNAT
   -A KUBE-SEP-AAA -p tcp -j DNAT --to-destination 10.244.1.10:8080
   -A KUBE-SEP-BBB -p tcp -j DNAT --to-destination 10.244.2.15:8080
   -A KUBE-SEP-CCC -p tcp -j DNAT --to-destination 10.244.3.20:8080
   ```

3. **로드밸런싱 특성**
   - **요청 레벨 밸런싱**: 매 요청마다 독립적으로 Pod 선택
   - **확률 기반**: 장기적으로는 균등 분배, 단기적으로는 불균형 가능
   - **연결 추적**: 같은 TCP 연결 내 패킷은 같은 Pod으로 (conntrack)
   - **세션 유지**: SessionAffinity: ClientIP 설정 시 같은 클라이언트 IP는 같은 Pod

4. **kube-proxy의 역할**
   - API 서버를 watch하여 Service/Endpoints 변경 감지
   - 변경 시 iptables 규칙 업데이트 (--sync-period 기본 30초)
   - 규칙 적용 후 실제 트래픽 전달은 커널이 처리 (kube-proxy는 관여 안 함)

**심화 질문**:
- Service ClusterIP는 실제 네트워크 인터페이스에 할당되는가? (아니오, 가상 IP이며 iptables 규칙으로만 존재)
- Pod이 자기 자신의 Service로 요청을 보내면 어떻게 되는가? (hairpin mode 활성화 시 가능, 아니면 루프)
- Endpoint가 0개일 때 Service로 요청하면? (타임아웃, iptables 규칙이 DROP으로 처리)

---

## Q3. Ingress Controller와 Ingress 리소스의 관계

**질문**: Ingress 리소스를 생성하면 Ingress Controller가 어떻게 이를 감지하고 트래픽 라우팅을 구성하는가?

**핵심 포인트**:

1. **역할 분리**
   - **Ingress 리소스**: 라우팅 규칙을 선언한 YAML (Kind: Ingress)
   - **Ingress Controller**: 규칙을 실제 구현하는 Pod (nginx, Traefik, HAProxy 등)
   - 비유: Ingress 리소스는 "설계도", Ingress Controller는 "건설 팀"

2. **동작 과정**
   ```
   1. 사용자: kubectl apply -f ingress.yaml
       ↓
   2. API 서버: Ingress 리소스 저장
       ↓
   3. Ingress Controller (nginx Pod):
      - API 서버를 watch
      - 새 Ingress 감지
       ↓
   4. nginx.conf 생성:
      server {
        listen 80;
        server_name myapp.local;
        location / {
          proxy_pass http://frontend-service:80;
        }
        location /api {
          proxy_pass http://backend-service:80;
        }
      }
       ↓
   5. nginx reload (설정 적용)
       ↓
   6. 트래픽 처리:
      외부 → LoadBalancer → Ingress Controller Pod → Service → Pod
   ```

3. **ingressClassName을 통한 선택**
   ```yaml
   # IngressClass 정의 (Controller 등록)
   apiVersion: networking.k8s.io/v1
   kind: IngressClass
   metadata:
     name: nginx
   spec:
     controller: k8s.io/ingress-nginx

   # Ingress 리소스에서 Controller 선택
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: my-ingress
   spec:
     ingressClassName: nginx  # 이 Controller가 처리
     rules:
     - host: myapp.local
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: frontend
               port:
                 number: 80
   ```

4. **여러 Ingress Controller 공존**
   - 클러스터에 nginx, Traefik, AWS ALB Controller 동시 설치 가능
   - ingressClassName으로 어떤 Controller가 처리할지 지정
   - 지정하지 않으면 default IngressClass 사용
   - 하나의 Ingress 리소스는 하나의 Controller만 처리

**심화 질문**:
- Ingress Controller가 다운되면 트래픽은 어떻게 되는가? (502/503 오류, Controller를 Deployment로 배포하여 자동 복구)
- Ingress 리소스를 업데이트하면 트래픽 중단이 발생하는가? (nginx는 graceful reload 지원, 기존 연결 유지)
- 여러 Ingress 리소스에서 같은 호스트를 사용하면? (먼저 생성된 것이 우선, 또는 Controller 설정에 따라 병합)

---

## Q4. NetworkPolicy의 기본 동작

**질문**: NetworkPolicy가 없을 때와 있을 때 Pod 간 통신은 어떻게 다르며, 정책의 기본 논리(allow vs deny)는 무엇인가?

**핵심 포인트**:

1. **기본 상태: 모든 트래픽 허용**
   ```bash
   # NetworkPolicy가 없으면
   kubectl run pod-a --image=nginx
   kubectl run pod-b --image=nginx
   kubectl exec pod-a -- curl pod-b  # ✅ 성공
   ```
   - 클러스터 내 모든 Pod은 서로 통신 가능
   - 네임스페이스 경계도 없음 (default에서 production으로 접근 가능)
   - 보안 문제: 공격자가 하나의 Pod을 장악하면 전체 클러스터 탐색 가능

2. **정책 적용 시: 화이트리스트 모델**
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: backend-policy
   spec:
     podSelector:
       matchLabels:
         app: backend
     policyTypes:
     - Ingress
     ingress: []  # 빈 규칙 = 모든 Ingress 차단
   ```
   - **podSelector에 매칭되는 Pod에만** 정책 적용
   - policyTypes에 Ingress/Egress 명시하면 해당 방향은 **기본 차단**
   - ingress/egress 규칙에 **명시적으로 허용**한 것만 통과

3. **정책 적용 논리**
   | 상황 | Ingress 트래픽 | Egress 트래픽 |
   |------|---------------|--------------|
   | NetworkPolicy 없음 | 모두 허용 | 모두 허용 |
   | policyTypes: [Ingress] | 규칙 매칭만 허용 | 모두 허용 (Egress 미지정) |
   | policyTypes: [Egress] | 모두 허용 (Ingress 미지정) | 규칙 매칭만 허용 |
   | policyTypes: [Ingress, Egress]<br/>ingress: []<br/>egress: [] | 모두 차단 | 모두 차단 |

4. **여러 정책의 조합**
   - 같은 Pod에 여러 NetworkPolicy 적용 시 **OR 연산** (합집합)
   - 예: 정책 A가 frontend 허용, 정책 B가 monitoring 허용 → 둘 다 허용
   - Deny 규칙은 없음 (모든 정책은 allow만 표현)

**심화 질문**:
- NetworkPolicy를 지원하지 않는 CNI 플러그인에서 정책을 만들면? (무시됨, Calico/Cilium 등 필요)
- podSelector: {}는 모든 Pod을 의미하는가? (그렇다, 같은 네임스페이스 내 모든 Pod)
- Ingress와 Egress 정책이 모두 있을 때 트래픽 순서는? (Egress는 출발지에서 평가, Ingress는 목적지에서 평가)

---

## Q5. headless Service의 DNS 동작 차이

**질문**: 일반 ClusterIP Service와 headless Service(clusterIP: None)의 DNS 동작은 어떻게 다르며, 각각 어떤 상황에서 사용하는가?

**핵심 포인트**:

1. **일반 ClusterIP Service의 DNS**
   ```bash
   # Service 생성
   kubectl create deployment nginx --image=nginx --replicas=3
   kubectl expose deployment nginx --port=80

   # DNS 조회
   kubectl run dnstest --image=busybox:1.28 -it --rm -- nslookup nginx
   # Name:      nginx.default.svc.cluster.local
   # Address 1: 10.96.5.10  ← ClusterIP 하나만 반환
   ```
   - DNS는 Service의 ClusterIP 반환
   - 클라이언트는 ClusterIP로 요청 → kube-proxy가 Pod 선택
   - 클라이언트는 백엔드 Pod을 알 수 없음 (추상화됨)

2. **headless Service의 DNS**
   ```bash
   # headless Service 생성
   kubectl expose deployment nginx --name=nginx-headless --cluster-ip=None --port=80

   # DNS 조회
   kubectl run dnstest --image=busybox:1.28 -it --rm -- nslookup nginx-headless
   # Name:      nginx-headless.default.svc.cluster.local
   # Address 1: 10.244.1.5 nginx-xxx-aaa.nginx-headless.default.svc.cluster.local
   # Address 2: 10.244.2.10 nginx-xxx-bbb.nginx-headless.default.svc.cluster.local
   # Address 3: 10.244.3.15 nginx-xxx-ccc.nginx-headless.default.svc.cluster.local
   ```
   - DNS는 **모든 Ready Pod의 IP 목록** 반환
   - ClusterIP 없음 (kube-proxy 규칙 생성 안 함)
   - 클라이언트가 직접 Pod 선택 (애플리케이션 레벨 로드밸런싱)

3. **StatefulSet과의 조합**
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: mysql-headless
   spec:
     clusterIP: None
     selector:
       app: mysql
   ---
   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     name: mysql
   spec:
     serviceName: mysql-headless  # headless Service 지정
     replicas: 3
   ```
   - 각 Pod에 대한 **안정적인 DNS 이름** 생성:
     - `mysql-0.mysql-headless.default.svc.cluster.local`
     - `mysql-1.mysql-headless.default.svc.cluster.local`
     - `mysql-2.mysql-headless.default.svc.cluster.local`
   - Pod이 재시작되어도 DNS 이름 유지 (IP는 변경될 수 있음)

4. **사용 시나리오**
   | 상황 | Service 타입 | 이유 |
   |------|-------------|------|
   | REST API (stateless) | ClusterIP | 로드밸런싱 필요, Pod 추상화 |
   | Kafka 클러스터 | headless | 클라이언트가 특정 브로커 선택 필요 |
   | MySQL 복제 | headless | 쓰기는 마스터, 읽기는 슬레이브 지정 |
   | Elasticsearch | headless | 노드 디스커버리 (클러스터 형성) |
   | Redis Sentinel | headless | Sentinel이 모든 마스터/슬레이브 추적 |

**심화 질문**:
- headless Service에서 SessionAffinity는 의미가 있는가? (없음, ClusterIP가 없으므로 kube-proxy 관여 안 함)
- DNS가 여러 IP를 반환할 때 클라이언트는 어떤 순서로 시도하는가? (DNS 라이브러리에 따라 다름, glibc는 라운드로빈)
- Ready가 아닌 Pod도 DNS에 포함되는가? (아니오, Readiness Probe 성공한 Pod만 포함)

---

## Q6. minikube에서 LoadBalancer 타입 사용 방법

**질문**: 로컬 개발 환경인 minikube에서 LoadBalancer 타입 Service를 사용하려면 어떻게 하며, 클라우드 환경과 어떤 차이가 있는가?

**핵심 포인트**:

1. **기본 동작: Pending 상태**
   ```bash
   # LoadBalancer Service 생성
   kubectl create deployment nginx --image=nginx
   kubectl expose deployment nginx --type=LoadBalancer --port=80

   kubectl get service nginx
   # NAME    TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)
   # nginx   LoadBalancer   10.96.5.10     <pending>     80:31234/TCP
   ```
   - minikube는 클라우드 프로바이더가 아니므로 외부 IP 할당 불가
   - NodePort는 자동 할당됨 (31234)
   - `<pending>` 상태로 무한 대기

2. **minikube tunnel 사용**
   ```bash
   # 별도 터미널에서 실행 (sudo 권한 필요)
   minikube tunnel
   # Status:
   #   machine: minikube
   #   pid: 12345
   #   route: 10.96.0.0/12 -> 192.168.49.2
   #   minikube: Running
   #   services: [nginx]
   #     nginx: 127.0.0.1

   # 원래 터미널에서 확인
   kubectl get service nginx
   # NAME    TYPE           EXTERNAL-IP   PORT(S)
   # nginx   LoadBalancer   127.0.0.1     80:31234/TCP

   # 로컬에서 접근
   curl http://127.0.0.1
   # 200 OK
   ```

3. **minikube tunnel의 동작 원리**
   - minikube VM의 네트워크를 호스트로 라우팅 (IP 터널)
   - Service의 ClusterIP를 EXTERNAL-IP로 할당 (보통 127.0.0.1로 매핑)
   - 호스트의 iptables/pf 규칙으로 트래픽 포워딩
   - 프로세스 종료 시 라우팅 제거 (정리 필요 시 `sudo pkill -f minikube-tunnel`)

4. **클라우드 환경과의 차이**
   | 측면 | minikube tunnel | AWS EKS (ELB) |
   |------|----------------|---------------|
   | EXTERNAL-IP | 127.0.0.1 (로컬호스트) | 실제 퍼블릭 IP/DNS |
   | 외부 접근 | 불가능 (같은 머신에서만) | 인터넷에서 접근 가능 |
   | 비용 | 무료 | 시간당 과금 |
   | HA | 없음 (단일 머신) | 다중 AZ, 자동 페일오버 |
   | TLS 종료 | 직접 설정 | ALB에서 자동 처리 |
   | 헬스체크 | kube-proxy | ELB 헬스체크 |

**심화 질문**:
- minikube tunnel 없이 NodePort로 접근하려면? (minikube ip 확인 후 http://<minikube-ip>:31234 접근)
- 여러 LoadBalancer Service를 만들면 각각 다른 EXTERNAL-IP를 받는가? (minikube tunnel은 모두 127.0.0.1로 매핑, 포트로 구분)
- Docker Desktop Kubernetes는 LoadBalancer를 어떻게 처리하는가? (자동으로 localhost에 매핑, tunnel 불필요)

---

## Q7. Pod-to-Pod, Pod-to-Service, External-to-Service 트래픽 경로 차이

**질문**: 같은 목적지(백엔드 Pod)로 가는 트래픽이라도 출발지에 따라 경로가 어떻게 달라지는가?

**핵심 포인트**:

1. **Pod-to-Pod 직접 통신**
   ```
   frontend Pod (10.244.1.5)
       ↓ curl http://10.244.2.10:8080 (백엔드 Pod IP 직접 사용)
   CNI 네트워크 (Calico/Flannel)
       ↓ 오버레이/언더레이 네트워크
   backend Pod (10.244.2.10)
   ```
   - kube-proxy 관여 안 함
   - NAT 없음 (출발지 IP 유지)
   - 가장 빠른 경로 (iptables 규칙 평가 없음)
   - **문제**: Pod IP는 임시적, Service 사용이 권장

2. **Pod-to-Service 통신**
   ```
   frontend Pod (10.244.1.5)
       ↓ curl http://backend:80 (Service DNS 이름)
   CoreDNS
       ↓ backend.default.svc.cluster.local → 10.96.5.10
   iptables (KUBE-SERVICES)
       ↓ 10.96.5.10:80 → DNAT → 10.244.2.10:8080
   CNI 네트워크
       ↓
   backend Pod (10.244.2.10)
       - 보이는 출발지 IP: 10.244.1.5 (원본 유지)
   ```
   - DNS 조회 → Service ClusterIP
   - kube-proxy iptables로 Pod 선택
   - 출발지 IP 유지 (SNAT 없음)

3. **External-to-Service (NodePort)**
   ```
   외부 클라이언트 (203.0.113.5)
       ↓ curl http://node-ip:30080
   Node의 30080 포트
       ↓ iptables (KUBE-NODEPORTS)
   SNAT (masquerade)
       ↓ 출발지 IP를 노드 IP로 변경 (10.244.0.1)
   DNAT
       ↓ 목적지 IP를 Pod IP로 변경 (10.244.2.10:8080)
   CNI 네트워크
       ↓
   backend Pod (10.244.2.10)
       - 보이는 출발지 IP: 10.244.0.1 (노드 IP)
       - ❌ 클라이언트 IP 손실!
   ```
   - **SNAT 발생**: externalTrafficPolicy: Cluster (기본값)
   - 클라이언트 IP 보존하려면: `externalTrafficPolicy: Local`

4. **External-to-Service (LoadBalancer + Ingress)**
   ```
   외부 클라이언트 (203.0.113.5)
       ↓ curl http://myapp.example.com/api
   클라우드 로드밸런서 (ELB)
       ↓ X-Forwarded-For 헤더 추가
   Ingress Controller Pod (10.244.1.20)
       ↓ /api 경로 매칭 → backend Service
   iptables (KUBE-SERVICES)
       ↓ 10.96.5.10:80 → 10.244.2.10:8080
   backend Pod (10.244.2.10)
       - 보이는 출발지 IP: 10.244.1.20 (Ingress Controller)
       - X-Forwarded-For: 203.0.113.5 (원본 클라이언트 IP)
   ```
   - Ingress Controller가 프록시 역할
   - 클라이언트 IP는 HTTP 헤더에서 확인

**심화 질문**:
- externalTrafficPolicy: Local의 단점은? (Pod이 없는 노드로 요청 시 실패, 로드밸런서가 헬스체크로 감지 필요)
- Pod-to-Service에서 SNAT이 발생하지 않는 이유는? (같은 클러스터 네트워크 내부이므로 라우팅 가능)
- Ingress Controller가 백엔드로 전달할 때 Service를 거치는가? (그렇다, Ingress는 Service를 백엔드로 지정)

---

## Q8. DNS 기반 서비스 디스커버리의 캐싱 문제와 해결

**질문**: CoreDNS를 통한 서비스 디스커버리에서 DNS 캐싱으로 인해 발생할 수 있는 문제는 무엇이며, 어떻게 해결하는가?

**핵심 포인트**:

1. **DNS TTL과 캐싱**
   ```bash
   # CoreDNS의 기본 TTL 확인
   kubectl get configmap -n kube-system coredns -o yaml
   # data:
   #   Corefile: |
   #     cluster.local:53 {
   #       kubernetes cluster.local in-addr.arpa ip6.arpa {
   #         ttl 30  ← 기본 30초
   #       }
   #     }
   ```
   - Service IP는 변경되지 않으므로 긴 TTL 문제 없음
   - **headless Service의 Pod IP 목록**은 변경됨 → 캐싱 문제 발생

2. **문제 시나리오: Pod IP 변경**
   ```bash
   # headless Service를 통한 StatefulSet 접근
   kubectl scale statefulset mysql --replicas=5

   # 클라이언트가 DNS 조회 (10.244.1.5, 10.244.2.10, 10.244.3.15)
   # 클라이언트의 DNS 캐시에 저장 (TTL 30초)

   # Pod 재시작으로 IP 변경
   kubectl delete pod mysql-2
   # 새 IP: 10.244.4.20

   # 클라이언트는 여전히 10.244.3.15로 시도 → 연결 실패
   # 30초 후 DNS 재조회로 자동 복구
   ```

3. **애플리케이션 레벨 대응**
   - **재시도 로직**: DNS 조회 실패 시 즉시 재조회
   - **TTL 준수**: 애플리케이션이 DNS 캐시를 직접 관리할 때 TTL 존중
   - **연결 풀**: 연결 실패 시 해당 IP를 풀에서 제거하고 재연결
   ```java
   // Java 예시: DNS 캐시 TTL 설정
   java.security.Security.setProperty("networkaddress.cache.ttl", "10");  // 10초
   ```

4. **CoreDNS 설정 조정**
   ```yaml
   # TTL 단축 (빠른 업데이트, 높은 부하)
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: coredns
     namespace: kube-system
   data:
     Corefile: |
       cluster.local:53 {
         kubernetes cluster.local in-addr.arpa ip6.arpa {
           ttl 5  ← 5초로 단축
         }
       }
   ```
   - **트레이드오프**: TTL 단축 → DNS 쿼리 증가 → CoreDNS 부하 증가
   - **권장**: 기본 30초 유지, 애플리케이션에서 재시도 처리

5. **클라이언트 라이브러리의 캐싱**
   - **Go**: 기본적으로 캐싱 안 함 (매번 DNS 조회)
   - **Java**: JVM이 DNS 캐싱 (networkaddress.cache.ttl 설정 필요)
   - **Python**: getaddrinfo()는 시스템 리졸버 사용 (glibc 캐싱)
   - **Node.js**: dns.lookup()은 캐싱, dns.resolve()는 캐싱 안 함

**심화 질문**:
- Service ClusterIP의 DNS TTL을 길게 설정해도 안전한 이유는? (ClusterIP는 Service 삭제 전까지 변경 안 됨)
- CoreDNS Pod이 재시작되면 DNS 쿼리가 실패하는가? (2개 이상의 레플리카로 HA 구성, Service로 로드밸런싱)
- ExternalName Service의 DNS 동작은 일반 Service와 어떻게 다른가? (CNAME 레코드 반환, 외부 DNS 이름으로 리다이렉트)
