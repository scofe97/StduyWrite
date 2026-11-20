> 출처: NotebookLM · 2026-11-16 · Chaos Mesh 로 Kubernetes 앱의 장애 내구성 검증하기 (컨퍼런스 발표 자막 분석) · 분야: k8s-keywords, devops-keywords · 미검증

## 요점

한 줄: 클라우드 DB 의 페일오버를 시험 코드로 재현하기 어려워, 장애를 Chaos Mesh 리소스로 선언하고 Workflow 로 겹치는 시점을 고정해 매일 밤 돌렸더니 리더 확인 지연이 10분 쓰기 불능으로 번지는 버그를 찾았다는 사례입니다.

- 왜 Chaos Mesh 인가: 앱 시험 코드로는 여러 파드 동시 종료, 커널 수준 네트워크 단절·지연, 겹치는 장애의 정확한 시점을 만들기 어렵고 코드가 급격히 복잡해집니다.
- 카오스 엔지니어링 루프: 정상 상태 가설 → 결함 주입 → 관측 → 약점 수정 → 같은 실험으로 회귀 확인입니다.
- 주입 경로 둘:
  - 파드 종료(`PodKill`·`PodFailure`)는 controller manager 가 Kubernetes API 로 바로 처리합니다.
  - 네트워크·부하(`NetworkChaos`·`StressChaos`)는 노드마다 도는 특권 `chaos-daemon` 이 gRPC 로 요청을 받아 대상 파드 네임스페이스에서 `tc`·cgroups 를 조작합니다.
- 원복 보장: 실험 상태가 etcd 에 남고 Finalizer 가 붙어, 데몬이 커널 규칙을 되돌린 뒤에야 리소스가 지워진다고 합니다. 대상 파드에 사이드카를 붙이지 않습니다.
- Workflow: `Serial`·`Parallel`·`Suspend`·`StatusCheck` 노드로 두 장애가 겹치는 순간을 고정합니다.
- 대상 시스템: Zone A 에 Primary·Replica 1, Zone B 에 Replica 2 를 두고, 여러 DB 가 공유하는 DB Operator·Failover Controller 는 Lease 로 리더를 정하는 Active-Standby 입니다.
- 네 갈래 시나리오:
  - 파드 종료 시점: Primary 단독, 유지보수 모드 중(페일오버가 없어야 정상), Operator·Failover Controller 리더와 동시 종료입니다. 리더 파드는 Lease 의 현재 홀더를 읽어 고릅니다.
  - 네트워크: Primary 완전 격리, 복제 400 ms 지연 중 격리입니다. 감시 경로와 복제 경로를 함께 끊고 탐지 시간(약 1분) 넘게 유지해야 페일오버가 일어납니다.
  - 겹침: 스펙 축소 중 Primary 부하·종료, Failover Controller → API 서버 출구만 4.2초 지연(90초) 중 Primary 종료입니다.
  - Zone 장애 근사: Zone A 파드를 격리하고 30초 간격으로 네 번 죽입니다. 공유 관리 파드에 영향이 커서 단독으로 돌립니다.
- 찾은 버그:
  - 승격 직전 `isLeader` 확인이 API 지연으로 실패하자 일시 오류인데도 재시도 없이 페일오버를 중단했습니다.
  - 곧바로 10분짜리 Anti-Flap 보호가 걸려 Standby 리더도 승격하지 못했고, 클러스터가 10분 동안 쓰기 불능이었습니다.
  - 일시 실패는 최대 120초 재확인하고, Lease 를 확실히 잃었을 때만 중단하게 고쳐 야간 회귀에 넣었습니다.
- 야간 운영: 아홉 시나리오(데몬 불필요 4·필요 4·Zone 단독 1)를 새벽 빌드 통과 뒤 그룹별로 돌립니다(그룹당 15~55분).
- 실행과 판정 분리: Workflow 는 장애 실행기로만 쓰고, 정상 여부는 Pytest 가 판정합니다(Primary 하나뿐인지, 복제 상태, 실제 읽기·쓰기 성공).
- 시험 코드 세 원칙: 성공·실패와 상관없이 임시 DB 삭제, Chaos 리소스 명시 삭제, Workflow `Timeout` 은 정상 흐름·`Aborted` 만 실패로 보고 실패 시 상태 덤프·로그 보관과 이슈 자동 생성입니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| 카오스 엔지니어링 | 결함을 일부러 넣어 정상 상태 가설이 버티는지 반복 확인하는 방법 | [신뢰성과 내결함성](../../05_data/book/designing-data-intensive-applications/02-03.신뢰성과 내결함성.md) (일부: 정의와 내결함성 연결, 가설·관측·회귀 루프와 도구 없음) |
| Chaos Mesh 두 주입 경로 | 파드 종료는 API 로, 네트워크·부하는 특권 데몬이 커널을 조작해 넣는 구조 | |
| 특권 DaemonSet | 노드마다 한 개씩 떠서 다른 파드의 네임스페이스에 들어가 일하는 인프라 파드 | [Daemon Service](../../08_cloud/book/kubernetes-patterns/09-01.Daemon Service — 노드마다 도는 인프라 Pod.md) (일부: 노드마다 도는 DaemonSet, 특권으로 남의 네임스페이스를 조작하는 경우 없음) |
| `tc`·netem | 인터페이스 큐(qdisc)에 지연·손실·차단 규칙을 거는 Linux 트래픽 제어 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) (일부: TC 훅과 qdisc 확인, netem 지연 주입 없음) |
| 네트워크 네임스페이스·nsenter | 파드마다 따로인 네트워크 공간과 그 안에 들어가 명령을 실행하는 도구 | [커널이 패킷을 주고받는 자리](../../08_cloud/book/networking-and-kubernetes/02-01.커널이 패킷을 주고받는 자리 — 소켓·인터페이스·veth·브리지.md) |
| Finalizer 원복 보장 | 정리 작업이 끝날 때까지 리소스 삭제를 막아 두는 표시 | [Application 관리하기](../../07_devops/book/argocd-up-and-running/04-01.Application 관리하기 — 소스·대상·Helm·Kustomize 와 삭제·finalizer.md) (일부: Argo CD 삭제 finalizer, 커널 규칙 원복 뒤 삭제 없음) |
| Chaos Workflow 시점 고정 | 병렬·대기 노드로 두 장애가 겹치는 순간을 매번 같게 만드는 실험 정의 | |
| Lease 리더 선출 | Lease 객체를 잡은 파드 하나만 리더로 일하는 Active-Standby 방식 | [Singleton Service](../../08_cloud/book/kubernetes-patterns/10-01.Singleton Service — 한 번에 하나만 활성이되 고가용.md) |
| Failover·Split-Brain·펜싱 | 리더 장애 때 승격하되 옛 리더가 계속 쓰지 못하게 막는 문제 | [노드 장애 처리와 복제 로그](../../05_data/book/designing-data-intensive-applications/06-02.노드 장애 처리와 복제 로그.md) |
| Anti-Flap | 짧은 간격의 연속 페일오버를 막으려 한 번 실패 뒤 일정 시간 승격을 막는 보호 | |
| 일시 오류와 리더십 상실 구분 | 조회 실패는 재시도하고, Lease 를 확실히 잃었을 때만 작업을 중단하는 판정 | |
| 주입 실패 거짓 통과 | 결함이 안 들어갔는데 Workflow 가 완료로 끝나 시험이 통과하는 함정 | |
| 주입 대상 함정 | 컨테이너 미지정 시 첫 컨테이너 선택, 런타임 설정 불일치, 다중 네임스페이스 셀렉터 AND, 재시작으로 격리 이탈 | |
| 실행과 판정 분리 | 장애 실행은 Workflow, 정상 판정은 별도 시험 코드가 맡는 구조 | |
| Zone 장애 근사 | 한 가용 영역의 파드를 격리하고 반복 종료해 영역 장애를 흉내 내는 실험 | [Deployment Models](../../08_cloud/book/production-kubernetes/02-01.Deployment Models — 배포 모델과 고가용성 인프라 구축.md) (일부: 가용 영역에 걸친 HA 배치, 영역 장애를 흉내 내는 실험 없음) |



## 자료와 실습

- 자료:
  - [Chaos Mesh 문서](https://chaos-mesh.org/docs/): controller manager·`chaos-daemon` 구조와 Workflow 노드 명세입니다.
  - [tc-netem(8)](https://man7.org/linux/man-pages/man8/tc-netem.8.html): 데몬이 지연·손실을 넣을 때 쓰는 커널 명령입니다.
  - [Leases (Kubernetes 문서)](https://kubernetes.io/docs/concepts/architecture/leases/): 관리 파드가 리더를 정하는 `coordination.k8s.io/v1` Lease 명세입니다. 정독 노트는 [Singleton Service](../../08_cloud/book/kubernetes-patterns/10-01.Singleton Service — 한 번에 하나만 활성이되 고가용.md) 입니다.
  - 『Chaos Engineering』(Rosenthal·Jones, 2020): 정상 상태 가설, 폭발 반경 통제, 지속 자동화의 원전입니다.
  - 『Designing Data-Intensive Applications』 복제·분산 시스템 장: 페일오버 함정과 Split-Brain, 네트워크 부분 장애를 봅니다. 정독 노트 [DDIA 2판](../../05_data/book/designing-data-intensive-applications/README.md) 에서는 6장·9장입니다.
  - 『Programming Kubernetes』: Watch·컨트롤러·Finalizer 를 코드 수준에서 봅니다.
  - [Leader Election in Distributed Systems](https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/): Lease 리더 선출이 지연·시계 차이에서 깨지는 경우를 다룹니다.
  - 코드: pumba `pkg/chaos/netem/`(`tc qdisc` 주입·원복)와 chaos-mesh `controllers/common/finalizers/`·`pkg/chaosdaemon/`(Finalizer 와 데몬 gRPC)를 봅니다. tidb-operator `pkg/controller/`·`tests/e2e/`(페일오버 제어와 장애 시험)도 봅니다.
- 실습:
  - Level 1: kind 에 Chaos Mesh 를 `chaosDaemon.runtime=containerd` 로 설치하고 파드 사이에 500 ms 지연을 60초 넣습니다. 함정은 런타임을 기본값으로 둬 주입이 조용히 실패하는 것입니다. 완료: `curl -w` 응답 시간이 주입 중 0.5초 넘게 늘고 리소스 삭제 뒤 원래대로 돌아옵니다.
  - Level 2: `client-go` leaderelection 으로 리더를 뽑는 앱 두 벌에 `Parallel`+`Suspend` Workflow 로 API 방향 3초 지연과 리더 `PodKill` 을 겹칩니다. 함정은 리더 이름을 하드코딩하는 것으로, 실행 때 Lease 의 `holderIdentity` 를 읽어 넣어야 합니다. 완료: Standby 가 무한 대기 없이 리더를 이어받는 것이 Lease 변경으로 보입니다.
  - Level 3: Pytest 하네스로 주입 직후 Event 를 확인하고, 끝난 뒤 읽기·쓰기 정합성을 판정하고, `finally` 에서 모두 정리합니다. 함정은 재시작한 파드가 격리에서 풀려 거짓 통과하는 것으로, `restartCount` 를 함께 봅니다. 완료: 셀렉터를 일부러 틀리면 "주입 실패" 로 떨어지고 진단 로그를 남기며 종료 코드 1 을 냅니다.



## 경고

- ⚠ 시스템 수치: 4.2초 지연, 120초 재확인, 10분 Anti-Flap, 약 1분 탐지, 그룹당 15~55분은 발표 팀 시스템의 값입니다. 일반 기본값이 아닙니다.
- ⚠ Workflow 동작: 내부 주입이 실패해도 Workflow 가 완료로 끝나고 흔적이 Event 에만 남는다는 서술, 여러 네임스페이스에 셀렉터가 AND 로 걸린다는 서술은 Chaos Mesh 문서로 확인하지 않았습니다.
- ⚠ 런타임 기본값: Helm `chaosDaemon.runtime` 기본값이 `docker` 라는 서술은 차트 버전마다 다를 수 있어 values 파일로 확인해야 합니다.
- ⚠ 상태 판정: `Timeout` 은 정상·`Aborted` 만 실패로 보는 규칙은 발표 팀의 결정입니다. Chaos Mesh 상태 의미와 대조하지 않았습니다.
- ⚠ DDIA 장 번호: 리포트는 1판 기준 5장(복제)·8장(분산 시스템)을 적었습니다. 2판 정독 노트에서는 6장·9장입니다.
- ⚠ 『Programming Kubernetes』·『Chaos Engineering』 장 범위: 리포트가 적은 "8장 Custom Resources", "9장 자동화 파이프라인" 은 목차로 대조하지 않아 자료 줄에서 뺐습니다.
- ⚠ 코드 경로: chaos-mesh `netlink_server.go` 같은 파일 경로는 저장소에서 확인하지 않아 폴더 단위로만 적었습니다. 영상 검색 링크는 버렸습니다.
- ⚠ 자막 교정과 이름: 영어 자동 자막의 오인식을 리포트가 고쳤습니다. 발표 회사·발표자 이름은 뺐습니다.
