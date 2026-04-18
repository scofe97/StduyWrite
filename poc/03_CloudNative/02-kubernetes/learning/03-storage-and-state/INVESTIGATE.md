# Ch03. 스토리지와 상태 관리 - 점검 질문

## Q1. emptyDir vs hostPath vs PVC 선택 기준

**질문**: 컨테이너에서 로그 파일을 저장해야 할 때, emptyDir, hostPath, PVC 중 어떤 것을 선택해야 하며, 그 판단 기준은 무엇인가?

**핵심 포인트**:

1. **데이터 수명주기 요구사항**
   - emptyDir: Pod 생명주기와 동일 (Pod 삭제 시 함께 삭제)
   - hostPath: 노드 생명주기와 동일 (Pod 삭제 후에도 유지, 노드 종속)
   - PVC: 독립적 생명주기 (Pod과 노드에서 분리, 영구 보존)

2. **노드 이동성**
   - emptyDir: Pod과 함께 이동 (데이터는 새로 시작)
   - hostPath: 노드에 고정 (다른 노드로 이동 시 데이터 접근 불가)
   - PVC: 클라우드 스토리지 사용 시 노드 간 이동 가능 (ReadWriteMany 또는 재마운트)

3. **사용 사례별 최적 선택**
   - 로그 수집 파이프라인 (사이드카): emptyDir (임시 버퍼)
   - 노드 모니터링 (/proc, /sys 접근): hostPath
   - 애플리케이션 데이터베이스: PVC
   - 빌드 캐시 (단일 노드): hostPath + nodeSelector
   - 공유 미디어 파일: PVC (ReadWriteMany)

4. **보안 및 운영 고려사항**
   - hostPath는 PodSecurityPolicy로 제한 필요 (호스트 침투 위험)
   - emptyDir은 메모리 기반(medium: Memory) 옵션으로 성능 향상 가능
   - PVC는 StorageClass를 통해 암호화, 백업 정책 적용 가능

**심화 질문**:
- emptyDir의 sizeLimit을 초과하면 어떻게 되는가? (Pod Eviction 트리거)
- hostPath의 type 필드(Directory, DirectoryOrCreate, File 등)는 언제 사용하는가?
- ReadWriteOnce PVC를 사용하는 Pod이 다른 노드로 이동할 때 재마운트 시간은?

---

## Q2. 동적 프로비저닝의 동작 과정

**질문**: PVC를 생성했을 때 StorageClass가 실제 클라우드 스토리지를 어떻게 자동으로 생성하는가? 이 과정에서 실패할 수 있는 지점은?

**핵심 포인트**:

1. **프로비저닝 시퀀스**
   ```
   PVC 생성
   → kube-controller-manager가 PVC 감지
   → StorageClass의 provisioner 확인
   → 외부 프로비저너(CSI 드라이버)에게 요청
   → 클라우드 API 호출 (예: AWS CreateVolume)
   → PV 오브젝트 자동 생성
   → PVC와 PV 바인딩
   → volumeBindingMode에 따라 즉시/지연 바인딩
   ```

2. **volumeBindingMode 차이**
   - Immediate: PVC 생성 즉시 볼륨 생성 → 노드 스케줄링 후 가용 영역 불일치 가능
   - WaitForFirstConsumer: Pod 스케줄링 후 해당 노드의 가용 영역에 볼륨 생성 (권장)

3. **실패 가능 지점**
   - 클라우드 API 할당량 초과 (EBS 볼륨 개수 제한)
   - 가용 영역 불일치 (노드는 us-east-1a, 볼륨은 us-east-1b)
   - StorageClass의 provisioner가 클러스터에 설치되지 않음 (CSI 드라이버 누락)
   - 권한 부족 (IAM 역할에서 ec2:CreateVolume 권한 없음)
   - 네트워크 타임아웃 (클라우드 API 응답 지연)

4. **디버깅 방법**
   ```bash
   # PVC 상태 확인
   kubectl describe pvc my-pvc
   # Events 섹션에서 오류 메시지 확인:
   # - ProvisioningFailed
   # - WaitForFirstConsumer

   # StorageClass 확인
   kubectl get storageclass fast-ssd -o yaml

   # 프로비저너 로그 확인 (CSI 드라이버)
   kubectl logs -n kube-system -l app=ebs-csi-controller
   ```

**심화 질문**:
- Immediate 모드에서 생성된 볼륨을 다른 가용 영역의 노드에서 사용하려면? (불가능, PVC 재생성 필요)
- PVC가 Pending 상태로 멈춘 경우 타임아웃은 언제 발생하는가? (무한 대기, 수동 삭제 필요)
- 동적 프로비저닝에서 PV 이름은 누가 결정하는가? (프로비저너가 자동 생성, pvc-{uuid} 형식)

---

## Q3. reclaimPolicy의 운영 영향

**질문**: PVC를 삭제했을 때 reclaimPolicy(Retain/Delete/Recycle)에 따라 실제로 어떤 일이 발생하며, 프로덕션 환경에서 어떤 정책을 선택해야 하는가?

**핵심 포인트**:

1. **각 정책의 동작**
   - Delete: PVC 삭제 → PV 삭제 → 클라우드 스토리지 삭제 (EBS 볼륨 완전 제거)
   - Retain: PVC 삭제 → PV는 Released 상태로 유지 → 클라우드 스토리지는 유지 (수동 정리 필요)
   - Recycle: 데이터 삭제 후 PV 재사용 (deprecated, 사용 안 함)

2. **운영 시나리오별 선택**
   - 개발/테스트 환경: Delete (자동 정리, 비용 절감)
   - 프로덕션 DB: Retain (실수 삭제 방지, 백업 가능)
   - 임시 작업 (ETL, 배치): Delete
   - 규정 준수 필요 (금융, 의료): Retain + 암호화 + 감사 로그

3. **Retain 정책의 수동 정리 과정**
   ```bash
   # PVC 삭제 후 PV 상태 확인
   kubectl get pv
   # NAME      STATUS     CLAIM
   # pv-123    Released   default/my-pvc

   # PV 삭제 (클라우드 스토리지는 유지됨)
   kubectl delete pv pv-123

   # AWS EBS 볼륨 확인 및 수동 삭제
   aws ec2 describe-volumes --filters Name=tag:kubernetes.io/created-for/pvc/name,Values=my-pvc
   aws ec2 delete-volume --volume-id vol-abc123
   ```

4. **재사용 가능성**
   - Delete: 재사용 불가 (스토리지 완전 삭제)
   - Retain: 새로운 PV 정의로 기존 볼륨 재사용 가능 (데이터 복구)
   ```yaml
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: pv-recovered
   spec:
     capacity:
       storage: 10Gi
     accessModes:
       - ReadWriteOnce
     awsElasticBlockStore:
       volumeID: vol-abc123  # 기존 볼륨 ID
   ```

**심화 질문**:
- reclaimPolicy를 동적으로 변경할 수 있는가? (PV의 .spec.persistentVolumeReclaimPolicy 패치 가능)
- 실수로 Delete 정책의 PVC를 삭제했을 때 데이터 복구 방법은? (클라우드 스냅샷에서 복구, 사전 스냅샷 필요)
- StatefulSet의 volumeClaimTemplates로 생성된 PVC는 StatefulSet 삭제 시 자동 삭제되는가? (아니오, 수동 삭제 필요)

---

## Q4. StatefulSet vs Deployment 선택 기준

**질문**: 어떤 워크로드에 StatefulSet을 사용해야 하며, Deployment로 충분한 경우는 언제인가? 각각의 트레이드오프는?

**핵심 포인트**:

1. **StatefulSet이 필수인 경우**
   - 각 인스턴스가 고유한 영구 스토리지 필요 (예: Kafka 브로커, 각 브로커는 독립 파티션)
   - 안정적인 네트워크 ID 필요 (예: Zookeeper, 클러스터 멤버십에서 hostname 사용)
   - 순서 보장 필요 (예: MySQL 마스터-슬레이브, 마스터 먼저 초기화)
   - Peer discovery 필요 (예: Cassandra, 노드 간 gossip 프로토콜)

2. **Deployment로 충분한 경우**
   - 상태를 외부 저장 (예: 세션을 Redis에 저장하는 웹 서버)
   - 모든 인스턴스가 동일 (예: REST API 서버, 캐시 없는 순수 계산)
   - 빠른 스케일링 필요 (예: 이벤트 기반 오토스케일링)
   - 로드밸런싱으로 충분 (클라이언트가 특정 인스턴스 지정 불필요)

3. **트레이드오프**
   | 측면 | Deployment | StatefulSet |
   |------|------------|-------------|
   | 배포 속도 | 빠름 (병렬) | 느림 (순차) |
   | 스케일링 | 즉시 (parallel) | 순차 (하나씩) |
   | 롤링 업데이트 | 빠름 | 느림 (순서 보장) |
   | 복잡도 | 낮음 | 높음 (Headless Service 필요) |
   | 스토리지 비용 | 낮음 (공유 가능) | 높음 (각 인스턴스 독립) |

4. **하이브리드 패턴**
   - Redis: StatefulSet (마스터-슬레이브) + Deployment (읽기 전용 레플리카)
   - Kafka: StatefulSet (브로커) + Deployment (Connect 워커)
   - 웹 앱: Deployment (애플리케이션) + StatefulSet (세션 스토어)

**심화 질문**:
- StatefulSet의 podManagementPolicy를 Parallel로 설정하면 Deployment와 동일해지는가? (순서는 무시되지만 고유 네트워크 ID는 유지)
- 읽기 전용 워크로드(예: Elasticsearch 데이터 노드)도 StatefulSet을 사용해야 하는가? (네트워크 ID와 스토리지 바인딩이 필요하면 사용)
- StatefulSet의 replicas를 0으로 줄이면 PVC는 어떻게 되는가? (유지됨, 스케일 업 시 재연결)

---

## Q5. StatefulSet의 Pod 순서 보장이 필요한 이유

**질문**: StatefulSet이 Pod을 순차적으로 생성/삭제하는 이유는 무엇이며, 이 순서를 어기면 어떤 문제가 발생하는가?

**핵심 포인트**:

1. **순서 보장의 실제 시나리오**
   - MySQL 복제: 마스터(mysql-0)가 먼저 초기화되어야 슬레이브(mysql-1, mysql-2)가 복제 시작
   - Kafka: 브로커 ID와 Pod 인덱스를 매핑, kafka-0이 controller 역할
   - Elasticsearch: 마스터 노드(es-0, es-1, es-2) 먼저 클러스터 형성 후 데이터 노드 추가
   - Zookeeper: 쿼럼 형성을 위해 과반수 노드가 먼저 준비되어야 함

2. **초기화 의존성**
   ```yaml
   initContainers:
   - name: wait-for-master
     image: busybox
     command:
     - sh
     - -c
     - |
       # mysql-1, mysql-2는 mysql-0이 Ready일 때까지 대기
       until nslookup mysql-0.mysql-headless; do
         echo "Waiting for mysql-0..."
         sleep 2
       done
   ```

3. **순서를 어겼을 때 문제**
   - 데이터 불일치: 슬레이브가 먼저 시작되어 잘못된 마스터에 연결
   - 스플릿 브레인: 여러 노드가 동시에 마스터 역할 시도
   - 복제 실패: 마스터가 준비되지 않은 상태에서 슬레이브가 복제 시도
   - 클러스터 형성 실패: Zookeeper에서 동시 시작 시 리더 선출 실패

4. **순서 보장 메커니즘**
   - Pod-0이 Running and Ready 상태가 되어야 Pod-1 생성
   - 삭제 시 역순 (Pod-2 → Pod-1 → Pod-0)
   - `.spec.podManagementPolicy: OrderedReady` (기본값)
   - Parallel 정책으로 순서 무시 가능 (단, 네트워크 ID는 유지)

**심화 질문**:
- ReadinessProbe가 실패하면 다음 Pod 생성이 영구적으로 블록되는가? (그렇다, 수동 개입 필요)
- StatefulSet의 partition 필드는 순서 보장과 어떤 관계인가? (카나리 업데이트, partition 이상 인덱스만 업데이트)
- 순서 보장이 필요하지 않은 StatefulSet에서 Parallel 정책 사용 시 장점은? (배포 속도 향상, 여전히 고유 ID 유지)

---

## Q6. volumeClaimTemplates와 일반 PVC의 차이

**질문**: StatefulSet의 volumeClaimTemplates는 일반 PVC와 어떻게 다르며, 왜 StatefulSet에서는 volumeClaimTemplates를 사용해야 하는가?

**핵심 포인트**:

1. **일반 PVC의 문제점**
   ```yaml
   # ❌ 잘못된 예시
   spec:
     replicas: 3
     template:
       spec:
         volumes:
         - name: data
           persistentVolumeClaim:
             claimName: shared-pvc  # 모든 Pod이 같은 PVC 사용!
   ```
   - 모든 레플리카가 하나의 PVC를 공유 → 데이터 충돌
   - ReadWriteOnce 볼륨은 하나의 노드만 마운트 가능 → 스케줄링 제약
   - 각 인스턴스의 고유 데이터 구분 불가

2. **volumeClaimTemplates의 동작**
   ```yaml
   volumeClaimTemplates:
   - metadata:
       name: data
     spec:
       accessModes: ["ReadWriteOnce"]
       storageClassName: fast-ssd
       resources:
         requests:
           storage: 10Gi
   ```
   - 각 Pod마다 고유한 PVC 자동 생성 (data-mysql-0, data-mysql-1, ...)
   - Pod 재시작 시 같은 PVC에 재연결 (상태 유지)
   - 스케일 업 시 새 PVC 자동 생성, 스케일 다운 시 PVC 유지 (수동 삭제 필요)

3. **생명주기 관리**
   ```bash
   # StatefulSet 생성
   kubectl apply -f mysql-statefulset.yaml
   # PVC 자동 생성: data-mysql-0, data-mysql-1, data-mysql-2

   # 스케일 다운
   kubectl scale statefulset mysql --replicas=1
   # Pod mysql-2, mysql-1 삭제되지만 PVC는 유지!

   # 스케일 업
   kubectl scale statefulset mysql --replicas=3
   # 기존 PVC data-mysql-1, data-mysql-2 재사용 (데이터 복구)
   ```

4. **네이밍 패턴**
   - PVC 이름: `{volumeClaimTemplates.metadata.name}-{statefulset.metadata.name}-{ordinal}`
   - 예: `data-mysql-0`, `data-mysql-1`
   - Pod 이름과 일대일 매핑 보장

**심화 질문**:
- volumeClaimTemplates의 storageClassName을 변경하면 기존 PVC는 어떻게 되는가? (영향 없음, 새 Pod만 새 StorageClass 사용)
- StatefulSet 삭제 시 volumeClaimTemplates로 생성된 PVC는 자동 삭제되는가? (아니오, orphan PVC 방지 설계)
- 여러 volumeClaimTemplates를 정의할 수 있는가? (가능, 각 Pod이 여러 독립 볼륨 가짐)

---

## Q7. minikube에서 스토리지 프로비저너 동작 방식

**질문**: 로컬 개발 환경인 minikube에서 PVC를 생성하면 실제로 어디에 데이터가 저장되며, 클라우드 환경과 어떤 차이가 있는가?

**핵심 포인트**:

1. **minikube의 기본 StorageClass**
   ```bash
   kubectl get storageclass
   # NAME                 PROVISIONER                RECLAIMPOLICY
   # standard (default)   k8s.io/minikube-hostpath   Delete
   ```
   - Provisioner: `k8s.io/minikube-hostpath` (hostPath 기반)
   - 실제 저장 위치: minikube VM 내부의 `/tmp/hostpath-provisioner/` 디렉토리

2. **데이터 저장 경로**
   ```bash
   # minikube VM에 접속
   minikube ssh

   # PVC 데이터 확인
   ls /tmp/hostpath-provisioner/
   # default-data-mysql-0-pvc-abc123/
   # default-data-mysql-1-pvc-def456/

   # 실제 MySQL 데이터 확인
   ls /tmp/hostpath-provisioner/default-data-mysql-0-pvc-abc123/
   # ibdata1  mysql/  performance_schema/
   ```

3. **클라우드 환경과의 차이**
   | 측면 | minikube | AWS EKS |
   |------|----------|---------|
   | Provisioner | k8s.io/minikube-hostpath | kubernetes.io/aws-ebs |
   | 실제 스토리지 | VM 내부 디렉토리 | EBS 볼륨 (클라우드) |
   | 노드 간 이동 | 불가능 (단일 노드) | 불가능 (ReadWriteOnce) |
   | 데이터 영속성 | VM 재시작 시 유지 | 영구적 |
   | 성능 | 로컬 디스크 속도 | 프로비저닝된 IOPS |

4. **minikube 재시작 시나리오**
   ```bash
   # PVC 생성 및 데이터 저장
   kubectl apply -f mysql-statefulset.yaml
   kubectl exec mysql-0 -- mysql -e "CREATE DATABASE testdb;"

   # minikube 중지
   minikube stop

   # minikube 재시작
   minikube start

   # 데이터 유지 확인
   kubectl exec mysql-0 -- mysql -e "SHOW DATABASES;"
   # testdb ← 여전히 존재!
   ```

5. **제한사항**
   - ReadWriteMany 지원 안 함 (단일 노드이므로 테스트 불가)
   - 네트워크 스토리지 시뮬레이션 안 됨
   - 실제 클라우드 프로비저너 테스트 불가 (CSI 드라이버 누락)

**심화 질문**:
- minikube delete 시 PVC 데이터는 어떻게 되는가? (완전 삭제, VM 자체가 삭제되므로)
- 로컬에서 AWS EBS CSI 드라이버를 테스트하려면? (kind + LocalStack 또는 AWS 계정 필요)
- minikube에서 ReadWriteMany를 테스트하려면? (NFS 서버 컨테이너 + NFS provisioner 설치 필요)
