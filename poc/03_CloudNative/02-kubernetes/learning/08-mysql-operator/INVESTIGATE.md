<!-- migrated: write/09_cloud/kubernetes/deepdive/06-02.MySQL Operator 점검.md (2026-04-19) -->

# Ch08. MySQL Operator 점검 질문

## Q1. InnoDB Cluster에서 Group Replication의 역할과 동작 원리

**질문:** Group Replication이 전통적인 비동기 복제와 어떻게 다르며, Paxos 기반 합의 알고리즘이 데이터 일관성을 어떻게 보장하는가?

**핵심 포인트:**

- **비동기 복제의 한계**: 전통적인 MySQL Replication은 Primary가 binlog를 Secondary로 전송하고, Secondary가 비동기로 적용한다. Primary가 죽으면 Secondary는 "어디까지 적용했는지" 확실히 모르므로 데이터 손실 가능성이 있다. 또한 Secondary를 Primary로 승격시킬 때 수동 개입이 필요하다.

- **Group Replication의 동작 원리**: 트랜잭션이 Primary에서 실행되면, 변경 내용이 binlog event로 그룹에 브로드캐스트된다. 각 멤버는 이 이벤트를 받아서 검증하고(충돌 감지), 과반수(Quorum)가 승인하면 커밋된다. 이후 모든 멤버가 동일한 순서로 트랜잭션을 적용한다. 이 과정은 Paxos 기반의 합의 프로토콜로 조율된다.

- **충돌 감지 메커니즘**: Multi-Primary 모드에서는 여러 멤버가 동시에 쓰기를 받을 수 있다. 같은 행을 수정하면 충돌이 발생하는데, Group Replication은 First-Commit-Wins 정책을 사용한다. 먼저 커밋된 트랜잭션이 승리하고, 나중 트랜잭션은 롤백된다. Single-Primary 모드에서는 하나의 Primary만 쓰기를 받으므로 이런 충돌이 발생하지 않는다.

- **Quorum의 중요성**: 과반수 승인이 필요하므로, 3개 클러스터에서 2개가 살아있으면 계속 쓰기가 가능하다. 하지만 2개가 죽으면 Quorum이 깨지고, 남은 1개는 읽기 전용 모드로 전환된다. 이는 스플릿 브레인(네트워크 파티션으로 두 그룹이 각각 Primary를 선출하는 상황)을 방지한다.

**심화 질문:**

- 5개 클러스터와 3개 클러스터의 장애 허용도 차이는 무엇인가? (힌트: 5개는 2개 장애 허용, 3개는 1개 장애 허용)
- Group Replication의 Flow Control은 무엇이며, 느린 멤버가 전체 클러스터 성능에 어떤 영향을 미치는가?

---

## Q2. MySQL Router가 필요한 이유 (애플리케이션 연결 투명성)

**질문:** 애플리케이션이 MySQL Router 없이 직접 MySQL Pod에 연결하면 안 되는 이유는 무엇이며, Router의 6446/6447 포트는 각각 어떤 역할을 하는가?

**핵심 포인트:**

- **Primary IP 추적 문제**: Group Replication에서 Primary는 언제든지 바뀔 수 있다. Pod가 죽거나, 네트워크 파티션이 발생하거나, 수동으로 Primary를 전환하면 Secondary 중 하나가 새 Primary가 된다. 애플리케이션이 직접 Pod에 연결하면 "현재 Primary가 누구인가?"를 계속 추적해야 한다. 이는 애플리케이션의 책임이 아니다.

- **6446 포트 (Read-Write)**: 이 포트로 연결하면 Router가 현재 Primary로만 라우팅한다. 쓰기 트랜잭션이나 강한 일관성이 필요한 읽기는 이 포트를 사용한다. Primary가 바뀌면 Router가 자동으로 새 Primary로 연결을 전환한다.

- **6447 포트 (Read-Only)**: 이 포트로 연결하면 Router가 Primary + Secondary 중에서 라운드 로빈으로 라우팅한다. 읽기 전용 쿼리의 부하를 Secondary로 분산시켜서 Primary의 부담을 줄인다. 최종 일관성(Eventual Consistency)이 허용되는 쿼리(예: 대시보드, 통계)에 적합하다.

- **연결 풀 관리**: Router는 애플리케이션과 MySQL 사이에서 연결 풀을 관리한다. 애플리케이션이 수백 개의 연결을 열어도 Router는 MySQL에는 적은 수의 연결만 유지할 수 있다. 이는 MySQL의 `max_connections` 제한을 완화한다.

- **장애 시 재연결**: Primary가 죽으면 Router는 새 Primary 선출을 기다렸다가 자동으로 재연결한다. 애플리케이션은 일시적인 연결 실패를 경험하지만, DNS나 IP를 변경할 필요가 없다. Connection Retry 로직만 구현하면 된다.

**심화 질문:**

- Router가 SPOF(Single Point of Failure)가 되지 않는가? Router를 3개로 스케일 아웃하면 어떻게 되는가? (힌트: Router는 Stateless이므로 여러 개 배포 가능, Service LoadBalancer가 분산)
- 6447 포트로 읽기를 분산할 때 Replication Lag가 1초라면, 사용자가 방금 입력한 데이터를 못 볼 수 있는가? 이를 어떻게 해결하는가?

---

## Q3. Primary 장애 시 자동 페일오버 과정 (Operator의 개입 범위)

**질문:** Primary Pod가 삭제되면 누가 새 Primary를 선출하는가? Operator는 이 과정에서 무엇을 하는가?

**핵심 포인트:**

- **Group Replication의 자율 선출**: Primary Pod가 죽으면 나머지 Secondary들이 Group Replication 프로토콜로 새 Primary를 선출한다. 이 과정은 MySQL 자체 기능이고, Operator가 개입하지 않는다. 보통 5~10초 안에 완료된다.

- **Operator의 역할 - StatefulSet 복구**: Operator는 Pod가 삭제되었음을 감지하고, StatefulSet Controller와 협력해서 새 Pod를 생성한다. 하지만 이 Pod는 빈 상태로 시작하므로 클러스터에 재합류하는 데 추가 시간이 걸린다.

- **Operator의 역할 - 클러스터 재구성**: 새 Pod가 시작되면 Operator는 MySQL Shell을 호출해서 이 Pod를 클러스터에 추가한다. 이 과정에서 데이터 동기화(Clone 또는 Incremental Recovery)가 발생한다. Primary가 아니라 Secondary로 합류한다.

- **Router 자동 갱신**: MySQL Router는 Group Replication의 메타데이터 테이블(`performance_schema.replication_group_members`)을 주기적으로 폴링해서 현재 Primary를 추적한다. Primary가 바뀌면 Router는 자동으로 새 Primary로 연결을 전환한다. Operator가 개입할 필요 없다.

- **Operator가 개입하는 경우**: Quorum이 깨져서 클러스터 전체가 읽기 전용 모드로 들어가면, Operator는 `force-quorum-using-partition-of` 명령을 실행해서 특정 멤버를 기준으로 클러스터를 재구성한다. 이는 수동 개입이 필요할 수 있다.

**심화 질문:**

- Primary 선출 중에 쓰기 트랜잭션이 들어오면 어떻게 되는가? (힌트: 5~10초 동안 쓰기가 실패하고, 애플리케이션은 재시도해야 함)
- StatefulSet Pod가 재생성될 때 PV는 어떻게 재사용되는가? 데이터가 보존되는가?

---

## Q4. InnoDBCluster CR의 주요 spec 필드와 기본값

**질문:** InnoDBCluster CR에서 `instances`, `router.instances`, `version`, `tlsUseSelfSigned`, `datadirVolumeClaimTemplate` 필드는 각각 무엇을 제어하며, 프로덕션 환경에서 권장되는 설정은 무엇인가?

**핵심 포인트:**

- **`instances`**: MySQL 인스턴스 개수. StatefulSet의 replicas로 변환된다. 기본값은 1이지만, HA를 위해서는 최소 3이 권장된다. 홀수로 설정해야 Quorum 계산이 명확하다 (3, 5, 7 등). 짝수(2, 4, 6)는 스플릿 브레인 위험이 있다.

- **`router.instances`**: MySQL Router 개수. Deployment의 replicas로 변환된다. 기본값은 1이지만, Router가 SPOF가 되지 않도록 2~3으로 설정하는 것이 좋다. Router는 Stateless이므로 여러 개 배포해도 문제없다.

- **`version`**: MySQL 버전. `8.0.35`, `8.4.0` 같은 형식이다. 최신 패치 버전을 사용하되, 메이저 업그레이드(8.0 → 8.4)는 테스트 후 진행해야 한다. 기본값은 `latest`지만 프로덕션에서는 명시적 버전 지정이 권장된다.

- **`tlsUseSelfSigned`**: 자체 서명 인증서 사용 여부. `true`로 설정하면 Operator가 자동으로 인증서를 생성하고, MySQL 인스턴스 간 통신이 TLS로 암호화된다. 프로덕션에서는 `false`로 설정하고 `tlsCASecretName`으로 실제 CA 인증서를 제공해야 한다.

- **`datadirVolumeClaimTemplate`**: PVC 템플릿. StatefulSet의 `volumeClaimTemplates`로 변환된다. `storage` 크기, `storageClassName`, `accessModes`를 지정한다. 프로덕션에서는 SSD 기반 StorageClass를 사용하고, 용량은 데이터 크기의 2~3배로 여유 있게 설정한다.

- **`podSpec.resources`**: Pod의 CPU/메모리 제한. InnoDB Buffer Pool 크기는 메모리의 70~80%로 설정된다. 예를 들어 메모리가 2Gi면 Buffer Pool은 약 1.5Gi다. CPU는 쿼리 복잡도에 따라 다르지만, 보통 1~2 코어면 충분하다.

**심화 질문:**

- `instances`를 3에서 5로 변경하면 어떻게 되는가? 클러스터 재시작이 필요한가? (힌트: Operator가 Rolling Update로 Pod를 추가)
- `tlsUseSelfSigned: true`로 설정하면 애플리케이션도 TLS로 연결해야 하는가, 아니면 Router가 TLS를 종료하는가?

---

## Q5. K8s StatefulSet 기반 MySQL vs Operator 기반 MySQL 차이

**질문:** Operator 없이 StatefulSet + Headless Service로 MySQL을 배포하는 것과 MySQL Operator를 사용하는 것의 차이는 무엇이며, Operator가 제공하는 추가 가치는 무엇인가?

**핵심 포인트:**

- **StatefulSet만 사용하는 경우**: StatefulSet은 안정적인 네트워크 ID(Pod 이름)와 PV를 제공한다. 하지만 MySQL의 Replication 설정, Primary/Secondary 구성, 장애 복구는 모두 수동으로 해야 한다. `mycluster-0`을 Primary로, `mycluster-1`, `mycluster-2`를 Secondary로 설정하려면 각 Pod에 접속해서 `CHANGE MASTER TO` 명령을 실행해야 한다.

- **Operator가 제공하는 자동화**: Operator는 InnoDBCluster CR을 감시하고, 필요한 모든 리소스(StatefulSet, Service, Secret, ConfigMap)를 생성한다. 더 중요한 것은 Day-2 Operation이다. Primary Pod가 죽으면 Operator는 즉시 감지하고, 클러스터 재구성이 필요하면 MySQL Shell을 호출해서 처리한다. 백업 스케줄, 모니터링 메트릭, TLS 인증서 갱신도 자동으로 처리된다.

- **선언적 관리의 이점**: StatefulSet 방식은 "어떻게(How)"에 집중한다. "이 명령을 실행해서 이 상태로 만든다." Operator 방식은 "무엇을(What)"에 집중한다. "3개 인스턴스 클러스터를 원한다." 상태가 틀어지면 Operator가 알아서 재조정(Reconcile)한다.

- **복잡도 트레이드오프**: Operator를 사용하면 MySQL 관리는 쉬워지지만, Operator 자체를 관리해야 한다. Operator가 버그가 있거나, 업그레이드 중 문제가 생기면 디버깅이 어렵다. StatefulSet만 사용하면 투명하지만, 운영 부담이 크다.

- **팀 역량에 따른 선택**: K8s와 MySQL을 모두 잘 아는 팀이라면 StatefulSet 방식도 가능하다. 하지만 소규모 팀이거나, 여러 DB를 관리해야 한다면 Operator가 훨씬 효율적이다.

**심화 질문:**

- Operator가 죽으면 기존 MySQL 클러스터는 어떻게 되는가? (힌트: 클러스터는 계속 동작하지만, 장애 복구나 스케일 아웃은 불가능)
- Operator 없이 StatefulSet으로 MySQL을 배포하고, 나중에 Operator로 마이그레이션할 수 있는가?

---

## Q6. mysqlsh로 클러스터 상태 확인하는 방법

**질문:** MySQL Shell을 사용해서 InnoDB Cluster의 상태를 확인하고, Primary/Secondary 역할, 복제 지연, Quorum 상태를 파악하는 명령은 무엇인가?

**핵심 포인트:**

- **MySQL Shell 접속**: Pod 안에서 mysqlsh를 실행한다. `--uri` 옵션으로 연결 정보를 지정한다.
  ```bash
  kubectl exec -it mycluster-0 -- mysqlsh --uri root@localhost:3306
  ```

- **클러스터 객체 가져오기**: `dba.getCluster()`로 현재 클러스터 객체를 가져온다.
  ```javascript
  var cluster = dba.getCluster()
  ```

- **클러스터 상태 확인**: `cluster.status()`는 JSON 형식으로 상세한 상태 정보를 반환한다.
  ```javascript
  cluster.status()
  ```
  출력 예시:
  ```json
  {
    "clusterName": "mycluster",
    "defaultReplicaSet": {
      "name": "default",
      "primary": "mycluster-0.mycluster-instances:3306",
      "status": "OK",
      "topology": {
        "mycluster-0.mycluster-instances:3306": {
          "role": "HA",
          "status": "ONLINE"
        },
        "mycluster-1.mycluster-instances:3306": {
          "role": "HA",
          "status": "ONLINE",
          "replicationLag": "00:00:00.123"
        }
      }
    }
  }
  ```

- **복제 지연 확인**: `topology` 섹션의 `replicationLag` 필드를 보면 Secondary가 Primary보다 얼마나 뒤처져 있는지 알 수 있다. 이 값이 크면 읽기 부하가 과도하거나, 네트워크가 느리거나, Secondary의 디스크 I/O가 느린 것이다.

- **Quorum 상태 확인**: `status`가 `OK`이고 모든 멤버가 `ONLINE`이면 Quorum이 정상이다. `NO_QUORUM`이나 `OFFLINE` 멤버가 있으면 장애 상황이다.

- **SQL로 직접 확인**: MySQL Shell 없이 일반 mysql 클라이언트로도 확인 가능하다.
  ```sql
  SELECT MEMBER_HOST, MEMBER_ROLE, MEMBER_STATE
  FROM performance_schema.replication_group_members;
  ```

**심화 질문:**

- `cluster.status({extended: 1})`을 실행하면 어떤 추가 정보를 볼 수 있는가? (힌트: 네트워크 통신량, 트랜잭션 처리량 등)
- Group Replication이 `ERROR` 상태일 때, `cluster.rejoinInstance()`로 복구할 수 있는 경우와 없는 경우는 무엇인가?

---

## Q7. minikube에서 MySQL HA 테스트의 한계

**질문:** minikube는 단일 노드 환경이므로 실제 프로덕션의 멀티 노드 클러스터와 어떤 차이가 있으며, 어떤 장애 시나리오를 테스트할 수 없는가?

**핵심 포인트:**

- **단일 노드의 한계**: minikube는 하나의 VM 또는 컨테이너로 동작한다. 3개 MySQL Pod가 모두 같은 물리 머신에서 돌아간다. 프로덕션에서는 Pod들이 다른 노드에 분산되도록 `podAntiAffinity`를 설정하지만, minikube에서는 의미가 없다.

- **노드 장애 테스트 불가**: 프로덕션에서는 "노드 하나가 통째로 죽으면 어떻게 되는가?"를 테스트해야 한다. 노드가 죽으면 그 위의 모든 Pod가 동시에 죽는다. minikube는 노드가 하나뿐이므로 이 시나리오를 테스트할 수 없다. 노드가 죽으면 모든 Pod가 죽는다.

- **네트워크 파티션 시뮬레이션 어려움**: 프로덕션에서는 네트워크 파티션(일부 노드 간 통신 단절)이 발생할 수 있다. minikube에서는 `iptables`로 Pod 간 트래픽을 차단해서 시뮬레이션할 수 있지만, 복잡하고 불완전하다.

- **Storage 장애 테스트 불가**: minikube의 PV는 호스트 파일시스템을 사용한다. 프로덕션에서는 EBS, PD 같은 클라우드 스토리지를 사용하는데, 이들의 레이턴시나 IOPS 제한, 장애 모드가 다르다. minikube에서는 "디스크가 가득 찼을 때", "I/O 오류가 발생했을 때" 같은 시나리오를 테스트하기 어렵다.

- **리소스 경합 테스트 불가**: 프로덕션에서는 여러 워크로드가 노드의 CPU/메모리를 경쟁한다. minikube는 전용 환경이므로 이런 경합이 적다. "다른 Pod가 노드의 메모리를 다 써버렸을 때 MySQL이 어떻게 되는가?" 같은 테스트는 불가능하다.

- **minikube의 유용성**: 그럼에도 minikube는 "기본 동작 확인"에는 충분하다. Operator 설치, CR 작성, 클러스터 생성, Router 연결, Pod 삭제 복구 같은 Happy Path를 빠르게 검증할 수 있다. 프로덕션 배포 전에 로컬에서 먼저 실습하는 용도로 적합하다.

**심화 질문:**

- kind(Kubernetes IN Docker)나 k3d를 사용하면 멀티 노드 환경을 로컬에서 시뮬레이션할 수 있는가? (힌트: 가능하지만 리소스 소모가 크다)
- Chaos Engineering 도구(Chaos Mesh, Litmus)를 minikube에 설치해서 네트워크 파티션, Pod 장애를 시뮬레이션할 수 있는가?
