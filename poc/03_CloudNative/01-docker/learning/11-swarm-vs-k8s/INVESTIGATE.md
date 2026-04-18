# Ch11. Docker Swarm vs Kubernetes - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Docker Swarm이 Kubernetes와의 경쟁에서 실패한 근본 원인은 무엇인가?

### 왜 이 질문이 중요한가
기술 선택 시 단순히 "현재 시장 점유율"만 보는 것이 아니라, 왜 특정 기술이 도태되었는지 이해하면 미래 기술 트렌드를 예측하고 비슷한 실수를 피할 수 있다. Swarm의 실패 원인을 분석하면 오케스트레이션 플랫폼에서 진정으로 중요한 요소가 무엇인지 파악할 수 있다.

### 답변
Docker Swarm이 실패한 근본 원인은 크게 세 가지로 정리된다.

첫째, **생태계 부족**이다. Kubernetes는 CNCF(Cloud Native Computing Foundation) 산하에서 Google, Red Hat, IBM 등 여러 벤더가 참여하는 오픈 거버넌스 구조를 가졌다. 반면 Swarm은 Docker Inc. 주도로 개발되어 단일 벤더 의존성이 높았다. 이로 인해 Kubernetes는 Helm, Prometheus, Istio 등 풍부한 서드파티 도구와 통합이 발전했지만, Swarm은 제한적인 생태계에 머물렀다. 실무에서는 오케스트레이션 플랫폼 자체보다 주변 생태계(모니터링, 로깅, 서비스 메시)가 더 중요한 경우가 많다.

둘째, **확장성과 유연성 제한**이다. Swarm은 수백 개 노드 규모까지는 잘 작동하지만, 수천 개 이상의 대규모 클러스터에서는 성능과 안정성 문제가 발생했다. 또한 Kubernetes는 CRD(Custom Resource Definition)를 통해 플랫폼을 확장할 수 있지만, Swarm은 이런 확장 메커니즘이 없어 복잡한 요구사항을 충족하기 어려웠다. 예를 들어 Kubernetes에서는 Operator 패턴으로 데이터베이스 같은 상태 기반 애플리케이션을 자동 관리할 수 있지만, Swarm에서는 불가능하다.

셋째, **클라우드 벤더의 지원 부족**이다. AWS(EKS), Google(GKE), Azure(AKS) 모두 Kubernetes를 관리형 서비스로 제공하며 막대한 투자를 했다. 반면 Swarm을 관리형으로 제공하는 주요 클라우드는 없었다. 클라우드 시대에 관리형 서비스 부재는 치명적이다. 기업들은 직접 인프라를 관리하기보다 클라우드 관리형 서비스를 선호하기 때문이다.

### 실무 적용
새로운 기술을 도입할 때 다음을 확인해야 한다.
- **오픈 거버넌스**: 단일 벤더 주도인가, 다중 벤더 참여인가?
- **생태계 성숙도**: 서드파티 도구, 플러그인, 커뮤니티 활성화 정도
- **클라우드 지원**: 주요 클라우드에서 관리형 서비스로 제공하는가?
- **확장성**: 현재 규모뿐 아니라 향후 10배 성장 시에도 대응 가능한가?

Swarm은 기술적으로 우수했지만 생태계, 거버넌스, 클라우드 지원에서 밀려 도태되었다. 기술 선택은 코드 품질만이 아닌 생태계 전체를 고려해야 한다.

---

## Q2. Swarm의 Raft 합의 알고리즘은 어떻게 작동하며, 왜 3개 또는 5개의 홀수 Manager를 권장하는가?

### 왜 이 질문이 중요한가
분산 시스템에서 합의 알고리즘은 고가용성의 핵심이다. Raft는 Swarm뿐 아니라 etcd(Kubernetes), Consul 등에서도 사용되므로, Raft를 이해하면 다른 분산 시스템의 동작 방식도 파악할 수 있다. 또한 "왜 홀수인가"라는 질문은 분산 시스템 설계의 쿼럼(Quorum) 개념을 이해하는 열쇠다.

### 답변
Raft는 분산 노드들이 일관된 상태를 유지하기 위해 "누가 리더인가"와 "어떤 변경사항을 적용할 것인가"에 대해 합의하는 알고리즘이다.

**Raft의 핵심 개념**은 다음과 같다.
- **Leader**: 한 명만 존재하며, 모든 쓰기 요청을 처리하고 로그를 다른 노드에 복제한다.
- **Follower**: Leader의 로그를 복제하고, Leader가 죽으면 선거에 참여한다.
- **Candidate**: Leader 선출 시 자신을 후보로 등록한 노드.
- **Term**: 논리적 시간 개념으로, 새 Leader가 선출될 때마다 증가한다.

**Leader 선출 과정**은 이렇게 진행된다.
1. Leader가 일정 시간(heartbeat timeout) 동안 응답하지 않으면 Follower가 Candidate가 된다.
2. Candidate는 자신의 Term을 1 증가시키고, 다른 노드에 투표 요청(RequestVote)을 보낸다.
3. 과반수(Quorum)의 투표를 받으면 Leader가 된다.
4. 동일 Term에 여러 Candidate가 나타나면 투표가 분산되어 선출 실패할 수 있다. 이 경우 랜덤 타임아웃 후 재시도한다.

**왜 홀수 Manager를 권장하는가?** 핵심은 **쿼럼(과반수)**이다.
- Raft는 과반수의 노드가 동의해야 변경사항을 커밋한다.
- 예: 3개 Manager 중 2개(과반수)가 살아있으면 클러스터 운영 가능.
- 예: 5개 Manager 중 3개(과반수)가 살아있으면 운영 가능.

**홀수 vs 짝수 비교**:
- **3개**: 1개 장애 허용, 쿼럼 2개 필요
- **4개**: 1개 장애 허용, 쿼럼 3개 필요 (3개와 동일한 장애 허용치, 비용만 증가)
- **5개**: 2개 장애 허용, 쿼럼 3개 필요
- **6개**: 2개 장애 허용, 쿼럼 4개 필요 (5개와 동일한 장애 허용치, 비용만 증가)

결론: 짝수는 홀수보다 노드가 하나 더 필요하지만 장애 허용치는 같다. 따라서 비용 효율적인 홀수를 권장한다.

**쿼럼 계산 공식**: `(N/2) + 1` (내림)
- 3개: (3/2) + 1 = 2
- 5개: (5/2) + 1 = 3
- 7개: (7/2) + 1 = 4

### 실무 적용
프로덕션 환경에서 Manager 배치 전략은 다음과 같다.
- **3개 Manager**: 대부분의 소중형 환경에 적합. 1개 AZ 장애 허용.
- **5개 Manager**: 대규모 환경 또는 높은 가용성 요구. 2개 AZ 장애 허용.
- **7개 이상**: 거의 불필요. 합의 과정이 느려져 오히려 성능 저하.

실제 배치 시 각 Manager를 서로 다른 가용성 영역(AZ)에 배치해야 한다. 같은 AZ에 3개를 모두 두면, AZ 장애 시 전체 클러스터가 다운된다. 또한 네트워크 지연이 중요하므로, 지리적으로 너무 멀리 떨어진 리전 간 Swarm 클러스터는 권장하지 않는다.

---

## Q3. Swarm과 Kubernetes의 서비스 디스커버리 및 로드 밸런싱 메커니즘은 어떻게 다른가?

### 왜 이 질문이 중요한가
서비스 디스커버리와 로드 밸런싱은 마이크로서비스 아키텍처의 핵심 요소다. Swarm과 Kubernetes가 이를 다르게 구현한 방식을 이해하면, 각 플랫폼의 설계 철학과 실무 트레이드오프를 파악할 수 있다. 또한 네트워크 문제 디버깅 시 내부 동작을 알아야 근본 원인을 찾을 수 있다.

### 답변
**Swarm의 서비스 디스커버리**는 다음과 같이 작동한다.
1. **내장 DNS**: Swarm은 서비스 이름을 DNS로 자동 등록한다. 예를 들어 `web-fe` 서비스를 배포하면, 컨테이너는 `web-fe`라는 호스트명으로 접근할 수 있다.
2. **VIP(Virtual IP) 기반 로드 밸런싱**: 서비스 이름을 DNS 조회하면 단일 VIP가 반환된다. 이 VIP는 Swarm이 관리하며, 요청이 VIP로 들어오면 IPVS(IP Virtual Server)가 백엔드 복제본 중 하나로 라운드로빈 방식으로 분산한다.
3. **Routing Mesh**: Swarm의 모든 노드는 Ingress 네트워크를 통해 퍼블리시된 포트로 들어온 요청을 적절한 복제본으로 라우팅한다. 예를 들어 `web-fe`가 포트 5001로 퍼블리시되면, 클러스터의 어떤 노드 IP:5001로 접근해도 실제 복제본으로 연결된다.

**Kubernetes의 서비스 디스커버리**는 더 복잡하고 유연하다.
1. **Service 리소스**: Kubernetes는 Service라는 추상화 계층을 통해 Pod 그룹에 안정적인 엔드포인트를 제공한다.
2. **DNS**: CoreDNS가 서비스 이름을 ClusterIP로 해석한다. 예: `web-fe.default.svc.cluster.local` → `10.96.0.1`
3. **로드 밸런싱 옵션**:
   - **ClusterIP**: 클러스터 내부용 VIP (기본값)
   - **NodePort**: 각 노드의 특정 포트로 외부 접근 허용
   - **LoadBalancer**: 클라우드 제공자의 외부 로드 밸런서 프로비저닝
   - **Headless Service**: VIP 없이 개별 Pod IP 직접 반환 (StatefulSet 용)
4. **kube-proxy**: 각 노드에서 실행되며, iptables 또는 IPVS를 통해 Service IP를 실제 Pod IP로 변환한다.

**핵심 차이점**:
- **유연성**: Kubernetes는 Service 타입, Headless Service, ExternalName 등 다양한 옵션을 제공한다. Swarm은 VIP 기반 단일 방식.
- **외부 노출**: Swarm은 Routing Mesh로 간단하게 외부 노출. Kubernetes는 NodePort, LoadBalancer, Ingress 등 여러 방법.
- **복잡도**: Swarm은 설정 없이 자동 동작. Kubernetes는 Service, Ingress, NetworkPolicy 등 여러 리소스 조합 필요.

### 실무 적용
Swarm의 간단한 접근은 소규모 환경에 적합하다. 예를 들어 마이크로서비스 3~5개 정도면 Swarm의 자동 DNS + VIP로 충분하다. 하지만 다음 상황에서는 Kubernetes가 필수적이다.
- **세밀한 트래픽 제어**: Canary 배포, Blue-Green 배포 시 Kubernetes의 Service + Ingress 조합이 훨씬 유연하다.
- **StatefulSet**: 데이터베이스처럼 안정적인 네트워크 ID가 필요한 경우, Kubernetes의 Headless Service가 필수다.
- **서비스 메시**: Istio, Linkerd 같은 서비스 메시는 Kubernetes 기반으로 설계되어 Swarm에서는 사용 불가하다.

디버깅 팁: Swarm에서 "서비스에 연결 안 됨" 문제 발생 시 `docker service ps <서비스>`로 복제본이 Running 상태인지 확인하고, `docker network inspect <네트워크>`로 VIP 할당 여부를 확인한다. Kubernetes에서는 `kubectl get endpoints <서비스>`로 실제 Pod IP가 등록되었는지 확인한다.

---

## Q4. Swarm과 Kubernetes의 스케줄링 전략은 어떻게 다르며, 각각 어떤 배치 제약을 지원하는가?

### 왜 이 질문이 중요한가
스케줄링은 오케스트레이터가 "어느 노드에 컨테이너를 배치할 것인가"를 결정하는 핵심 기능이다. 잘못된 배치는 리소스 낭비, 성능 저하, 장애 전파로 이어진다. Swarm과 Kubernetes의 스케줄링 차이를 이해하면, 각 플랫폼의 한계를 파악하고 적절한 워크로드를 배치할 수 있다.

### 답변
**Swarm의 스케줄링 전략**은 비교적 단순하다.
1. **기본 전략**: Spread (노드 간 균등 분산). Swarm은 가용 리소스(CPU, 메모리)가 가장 많은 노드에 컨테이너를 배치한다.
2. **Placement Constraints**: 서비스 배포 시 제약 조건을 지정할 수 있다.
   - `node.role == manager`: Manager 노드에만 배치
   - `node.labels.disk == ssd`: SSD 라벨이 있는 노드에만 배치
   - `node.hostname == node1`: 특정 노드에 고정
3. **Placement Preferences**: 소프트 제약으로, 가능하면 선호하지만 필수는 아니다. 예: `spread: node.labels.datacenter` (여러 데이터센터에 분산)
4. **리소스 제한**: `deploy.resources.limits`와 `reservations`로 CPU/메모리 요구사항 지정 가능.

**Kubernetes의 스케줄링**은 훨씬 정교하다.
1. **기본 스케줄러**: kube-scheduler가 다단계 필터링과 스코어링을 수행한다.
   - **필터링**: 노드 리소스, 노드 셀렉터, Affinity, Taint/Toleration 등으로 부적합 노드 제거
   - **스코어링**: 남은 노드들을 여러 기준(리소스 밸런스, Pod 분산, 이미지 존재 등)으로 점수 매겨 최적 노드 선택
2. **NodeSelector**: 노드 라벨 기반 간단한 배치. 예: `disktype: ssd`
3. **Affinity/Anti-Affinity**:
   - **Node Affinity**: 특정 노드 라벨에 대한 선호도 (required/preferred)
   - **Pod Affinity**: 같은 노드/AZ에 배치 (예: DB와 App 동일 노드)
   - **Pod Anti-Affinity**: 다른 노드/AZ에 배치 (예: 같은 서비스 복제본 분산)
4. **Taints and Tolerations**: 노드에 "오염(Taint)"을 설정해 특정 Pod만 배치 허용. 예: GPU 노드는 GPU 워크로드만.
5. **Topology Spread Constraints**: Pod를 AZ, 랙, 노드 등 토폴로지 도메인에 균등 분산.
6. **Custom Scheduler**: 기본 스케줄러 외에 커스텀 스케줄러 추가 가능.

**핵심 차이점**:
- **정교함**: Swarm은 단순한 제약/선호도. Kubernetes는 다층 Affinity, Taint/Toleration, Topology Spread.
- **확장성**: Swarm은 고정 로직. Kubernetes는 커스텀 스케줄러, Scheduler Extender로 확장 가능.
- **스테이트풀 워크로드**: Kubernetes는 StatefulSet + PVC로 안정적인 스토리지 배치 지원. Swarm은 제한적.

### 실무 적용
Swarm에서 배치 제약은 Compose 파일에서 다음과 같이 설정한다.
```yaml
services:
  db:
    deploy:
      placement:
        constraints:
          - node.labels.disktype == ssd
          - node.role == worker
        preferences:
          - spread: node.labels.datacenter
```

Kubernetes에서는 훨씬 복잡하지만 강력하다.
```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - web
        topologyKey: kubernetes.io/hostname
  nodeSelector:
    disktype: ssd
  tolerations:
  - key: gpu
    operator: Equal
    value: "true"
    effect: NoSchedule
```

실무 팁: Swarm은 간단한 배치 요구사항(SSD 노드, 특정 AZ)에 적합하다. 하지만 "DB와 캐시를 같은 노드에, 웹 서버는 다른 AZ에" 같은 복잡한 요구사항은 Kubernetes 없이는 구현 불가하다. 또한 GPU 워크로드는 Kubernetes의 Taint/Toleration + 리소스 쿼터가 필수다.

---

## Q5. Swarm에서 Kubernetes로 마이그레이션할 때의 주요 과제와 전략은 무엇인가?

### 왜 이 질문이 중요한가
많은 조직이 초기에 Swarm으로 시작했다가 규모가 커지면서 Kubernetes로 마이그레이션하는 상황에 직면한다. 마이그레이션은 단순한 기술 전환이 아니라 팀 역량, 운영 프로세스, 도구 체인 전체를 바꾸는 작업이다. 실패 시 다운타임, 데이터 손실, 팀 번아웃으로 이어질 수 있다. 체계적인 마이그레이션 전략을 이해하면 리스크를 최소화할 수 있다.

### 답변
**주요 과제**는 다음과 같다.

1. **개념 차이**: Swarm의 Service는 Kubernetes의 Deployment + Service 조합에 대응한다. Swarm의 Stack은 Helm Chart와 유사하다. 팀이 Kubernetes의 Pod, ReplicaSet, Deployment, Service, Ingress 등 새로운 개념을 익혀야 한다.

2. **설정 파일 변환**: Swarm의 Compose 파일을 Kubernetes Manifest로 변환해야 한다. `kompose`라는 도구가 있지만 완벽하지 않아 수동 수정이 필요하다. 특히 Swarm의 `deploy` 섹션을 Kubernetes의 `resources`, `replicas`, `strategy`로 매핑하는 과정이 복잡하다.

3. **네트워크 차이**: Swarm의 Overlay 네트워크는 Kubernetes의 CNI(Calico, Flannel 등)로 대체된다. Swarm의 Routing Mesh는 Kubernetes의 Service + Ingress로 재구성해야 한다.

4. **스토리지**: Swarm의 볼륨은 Kubernetes의 PV(Persistent Volume) + PVC(Persistent Volume Claim)로 변환된다. 특히 클라우드 환경에서는 StorageClass를 이해하고 설정해야 한다.

5. **시크릿/설정**: Swarm Secrets는 Kubernetes Secrets로, Configs는 ConfigMap으로 매핑된다. 하지만 Kubernetes Secrets는 기본적으로 base64 인코딩만 되어 있어 암호화를 위해 Sealed Secrets, Vault 같은 추가 도구가 필요하다.

6. **운영 도구**: Swarm은 `docker stack`, `docker service` 같은 Docker CLI로 관리하지만, Kubernetes는 `kubectl`, Helm, Kustomize 등 새로운 도구 체인을 배워야 한다.

**마이그레이션 전략**은 단계적으로 진행해야 한다.

**1단계: 준비 및 학습 (1~2개월)**
- 팀이 Kubernetes 기초를 학습한다. CKA(Certified Kubernetes Administrator) 자격증 준비 과정이 좋은 출발점이다.
- 개발 환경에서 Kubernetes 클러스터를 구축하고 간단한 앱을 배포해본다.
- Swarm Compose 파일을 Kubernetes Manifest로 변환하는 파일럿 프로젝트를 진행한다.

**2단계: 병렬 운영 (2~3개월)**
- 프로덕션에 Kubernetes 클러스터를 구축한다. 관리형 서비스(EKS, GKE, AKS) 사용을 강력히 권장한다.
- 중요도가 낮은 서비스 1~2개를 Kubernetes로 마이그레이션한다.
- Swarm과 Kubernetes를 병렬로 운영하며, Kubernetes의 모니터링/로깅/알림 체계를 구축한다.

**3단계: 점진적 마이그레이션 (3~6개월)**
- Blue-Green 또는 Canary 방식으로 서비스를 하나씩 옮긴다.
- 데이터베이스 같은 스테이트풀 워크로드는 마지막에 이전한다.
- 각 서비스 이전 후 최소 1~2주 동안 안정성을 모니터링한다.

**4단계: Swarm 클러스터 해체 (1개월)**
- 모든 워크로드가 Kubernetes로 이전되면 Swarm 클러스터를 단계적으로 축소한다.
- 롤백 계획을 유지한 채로 최소 1개월 이상 Kubernetes만으로 운영한다.
- 확신이 생기면 Swarm 클러스터를 완전히 해체한다.

### 실무 적용
실제 마이그레이션 사례에서 자주 겪는 함정은 다음과 같다.
- **빅뱅 방식 시도**: 한 번에 모든 서비스를 옮기려다 대규모 장애 발생. 반드시 점진적으로 진행해야 한다.
- **학습 부족**: Kubernetes를 Swarm처럼 사용하려다 오히려 복잡도만 증가. Kubernetes의 철학과 패턴을 제대로 배워야 한다.
- **관리형 서비스 미사용**: 직접 Kubernetes 클러스터를 운영하려다 etcd, 컨트롤 플레인 관리 부담에 압도됨. 가능하면 EKS/GKE/AKS를 사용해야 한다.

도구 추천: `kompose`로 초기 변환 후 수동 수정, Helm으로 패키징, ArgoCD로 GitOps 배포, Prometheus + Grafana로 모니터링 체계 구축. 마이그레이션 기간은 앱 규모에 따라 6개월~1년 정도 소요된다.

---

## Q6. 소규모 환경에서 Swarm이 여전히 Kubernetes보다 나은 이유는 무엇인가?

### 왜 이 질문이 중요한가
"Kubernetes가 업계 표준"이라는 이유만으로 모든 환경에 Kubernetes를 도입하는 것은 과잉 엔지니어링이다. 기술 선택은 팀 규모, 예산, 운영 역량에 따라 달라져야 한다. Swarm의 장점을 이해하면, 언제 Kubernetes를 건너뛰고 더 간단한 솔루션을 선택해야 하는지 판단할 수 있다.

### 답변
소규모 환경(팀 5명 이하, 서비스 10개 이하, 노드 10개 이하)에서 Swarm이 여전히 나은 이유는 다음과 같다.

**1. 극단적인 단순성**
- Swarm은 Docker에 내장되어 있어 별도 설치가 불필요하다. `docker swarm init` 한 줄로 클러스터가 구성된다.
- Compose 파일에 `deploy` 섹션만 추가하면 오케스트레이션이 가능하다. Kubernetes는 Deployment, Service, Ingress, ConfigMap 등 여러 YAML 파일을 작성해야 한다.
- 예: Swarm은 Compose 파일 30줄로 3-tier 앱 배포 가능. Kubernetes는 최소 100줄 이상의 Manifest 필요.

**2. 낮은 학습 곡선**
- 이미 Docker Compose를 사용하고 있다면, Swarm으로의 전환은 1~2일이면 충분하다.
- Kubernetes는 Pod, ReplicaSet, Deployment, Service, Ingress, ConfigMap, Secret, PV, PVC, Namespace, RBAC 등 수십 개의 개념을 익혀야 하며, CKA 수준의 지식을 얻기까지 최소 3~6개월이 걸린다.

**3. 운영 오버헤드 최소화**
- Swarm은 Manager 노드만 관리하면 된다. etcd, 컨트롤 플레인, CNI, CSI 같은 복잡한 컴포넌트가 없다.
- Kubernetes는 etcd 백업, 컨트롤 플레인 업그레이드, CNI 플러그인 관리 등 운영 부담이 크다. 관리형 서비스(EKS 등)를 사용하지 않으면 운영 인력이 최소 1명 이상 필요하다.

**4. 리소스 효율성**
- Swarm의 컨트롤 플레인은 매우 가벼워 Manager 노드에서도 사용자 앱을 실행할 수 있다.
- Kubernetes는 컨트롤 플레인(kube-apiserver, kube-scheduler, kube-controller-manager, etcd)이 상당한 리소스를 소비한다. 소규모 클러스터에서는 전체 리소스의 20~30%를 컨트롤 플레인이 차지할 수 있다.

**5. 비용**
- Swarm은 무료이며 추가 인프라 비용이 없다.
- Kubernetes 관리형 서비스는 컨트롤 플레인만 월 $70~$150 비용이 발생한다. 소규모 스타트업에는 부담이 될 수 있다.

**언제 Swarm을 선택해야 하는가?**
- 팀이 5명 이하이고 Kubernetes 전문가가 없다.
- 서비스가 10개 이하이고 복잡한 배포 전략(Canary, Blue-Green)이 불필요하다.
- 이미 Docker Compose로 개발 환경을 관리하고 있다.
- 예산이 제한적이어서 관리형 Kubernetes 비용이 부담스럽다.
- 빠른 프로토타이핑이 목표이며, 향후 Kubernetes로 마이그레이션할 계획이 있다.

### 실무 적용
실제 사례로, 5명 규모의 스타트업이 초기에 Swarm으로 시작해 2년간 안정적으로 운영하다가, 팀이 20명으로 성장하고 서비스가 30개를 넘어서면서 Kubernetes로 마이그레이션한 경우가 많다. 초기부터 Kubernetes를 도입했다면 학습과 운영 부담으로 제품 개발 속도가 느려졌을 것이다.

"적합한 도구를 적합한 시기에" 사용하는 것이 핵심이다. Swarm은 여전히 소규모 환경에서 최고의 선택지 중 하나다. Kubernetes는 필요해지는 시점에 도입해도 늦지 않다.

---

## Q7. Kubernetes의 복잡성은 어디서 오며, 이는 필수적인가 아니면 우발적인가?

### 왜 이 질문이 중요한가
"Kubernetes는 너무 복잡하다"는 불만이 끊이지 않는다. 하지만 이 복잡성이 분산 시스템의 본질적(필수적) 복잡성인지, 아니면 나쁜 설계로 인한 우발적 복잡성인지 구분해야 한다. 이를 이해하면 Kubernetes의 복잡성을 받아들일 것인지, 더 간단한 대안을 찾을 것인지 합리적으로 판단할 수 있다.

### 답변
Kubernetes의 복잡성은 **필수적 복잡성**(본질적)과 **우발적 복잡성**(부차적)이 혼재되어 있다.

**필수적 복잡성 (피할 수 없는 것)**

1. **분산 시스템의 본질**: Kubernetes는 수천 개 노드와 수만 개 컨테이너를 관리하는 분산 시스템이다. CAP 정리, 합의 알고리즘, 네트워크 파티션, 장애 감지 같은 분산 시스템 문제는 본질적으로 어렵다.

2. **다양한 워크로드 지원**: Kubernetes는 스테이트리스 웹 서버, 스테이트풀 데이터베이스, 배치 작업, 크론잡, 데몬셋, GPU 워크로드 등을 모두 지원해야 한다. 이를 위해 Deployment, StatefulSet, Job, CronJob, DaemonSet 같은 다양한 추상화가 필요하다.

3. **확장성과 유연성의 트레이드오프**: Kubernetes는 CRD(Custom Resource Definition)를 통해 무한히 확장 가능하지만, 이는 기본 개념만으로도 수십 개의 리소스 타입을 배워야 함을 의미한다.

4. **보안과 멀티테넌시**: 엔터프라이즈 환경에서는 Namespace, RBAC, NetworkPolicy, PodSecurityPolicy 같은 복잡한 보안 메커니즘이 필수다.

**우발적 복잡성 (설계로 인한 것)**

1. **YAML 지옥**: Kubernetes는 모든 것을 YAML로 정의하며, YAML 문법은 들여쓰기에 민감하고 오류가 발생하기 쉽다. JSON이나 더 나은 DSL을 선택할 수 있었지만 YAML을 고수했다.

2. **과도한 추상화**: Pod, ReplicaSet, Deployment의 3단계 계층 구조는 필요 이상으로 복잡하다. 대부분의 사용자는 Deployment만 사용하는데, ReplicaSet을 알아야 하는 이유는 불분명하다.

3. **비일관적 API**: Service의 `selector`와 Deployment의 `matchLabels`는 동일한 개념인데 이름이 다르다. `kubectl get`과 `kubectl describe`의 출력 형식이 일관성이 없다.

4. **문서와 학습 경로 부족**: 공식 문서는 참조(reference) 수준이며, 초보자를 위한 체계적인 학습 경로가 부족하다. Swarm은 "The Docker Book" 한 권으로 충분하지만, Kubernetes는 수십 권의 책과 수백 개의 블로그를 봐야 한다.

5. **도구 파편화**: Kubernetes 자체는 기본 기능만 제공하고, 실제 운영을 위해서는 Helm(패키징), Kustomize(설정 관리), ArgoCD(배포), Prometheus(모니터링), Istio(서비스 메시) 등 수십 개의 서드파티 도구가 필요하다. 각 도구마다 학습 곡선이 있다.

**복잡성은 필수적인가?**

부분적으로 그렇다. 대규모 분산 시스템을 관리하려면 일정 수준의 복잡성은 피할 수 없다. 하지만 Kubernetes는 우발적 복잡성도 상당히 많다. 예를 들어:
- **Nomad**(HashiCorp)는 Kubernetes와 유사한 기능을 제공하지만 훨씬 간단한 API를 가졌다.
- **Docker Swarm**은 소규모 환경에서 충분한 기능을 제공하면서도 극히 단순하다.
- **K3s**, **MicroK8s** 같은 경량 Kubernetes 배포판은 불필요한 컴포넌트를 제거해 복잡성을 줄였다.

### 실무 적용
Kubernetes의 복잡성을 다루는 전략은 다음과 같다.

**1. 추상화 계층 추가**: 팀이 직접 Kubernetes Manifest를 작성하지 않고, Helm Chart 또는 내부 PaaS를 통해 배포하게 한다. 예를 들어 Heroku는 Kubernetes 위에 구축되었지만, 사용자는 `git push`만 하면 된다.

**2. 관리형 서비스 사용**: EKS, GKE, AKS를 사용하면 etcd, 컨트롤 플레인, 네트워크 플러그인 같은 복잡한 부분을 클라우드 벤더가 관리해준다.

**3. 필요한 기능만 사용**: 초기에는 Deployment, Service, Ingress만 사용하고, 필요할 때 StatefulSet, ConfigMap, Secret 등을 점진적으로 도입한다.

**4. 규모에 따른 선택**: 소규모(노드 10개 이하)에서는 Swarm, 중규모(노드 10~100개)에서는 관리형 Kubernetes, 대규모(노드 100개 이상)에서는 완전한 Kubernetes + GitOps + 서비스 메시를 도입한다.

결론: Kubernetes의 복잡성은 부분적으로 필수적이지만, 우발적 복잡성도 많다. 모든 환경에 Kubernetes가 필요한 것은 아니며, 팀 역량과 워크로드 규모에 맞는 적절한 도구를 선택해야 한다.
