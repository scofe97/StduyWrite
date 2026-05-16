<!-- migrated: write/09_cloud/kubernetes/deepdive/06-04.Redis Operator 점검.md (2026-04-19) -->

# Ch10: Redis Operator 점검 질문

## Q1: Redis Sentinel vs Cluster 모드 선택 기준

**질문**: 프로덕션 환경에서 Redis Sentinel과 Cluster 모드 중 어떤 것을 선택해야 하는가? 각 모드의 트레이드오프는 무엇인가?

**핵심 포인트**:

- **Sentinel 선택 기준**: 데이터 크기가 10GB 미만이고, 단일 마스터의 쓰기 성능(초당 10만 ops)으로 충분하며, 멀티키 연산(MGET, MSET, 트랜잭션)을 자주 사용하는 경우. 고가용성은 필요하지만 샤딩은 불필요한 세션 스토어, 소규모 캐시에 적합.
- **Cluster 선택 기준**: 데이터 크기가 10GB 이상이거나, 쓰기 부하가 단일 노드를 초과하거나(초당 30만+ ops), 수평 확장이 필요한 경우. 대규모 캐시, 순위표(Leaderboard), 분산 카운터에 적합.
- **멀티키 연산 제약**: Cluster 모드는 멀티키 연산이 제한된다. `MGET key1 key2`는 `key1`과 `key2`가 같은 슬롯에 있어야만 실행 가능. Hash Tag(`{user:1000}:session`, `{user:1000}:cart`)로 같은 슬롯에 강제 배치 가능하지만, 샤딩 효율이 떨어진다.
- **클라이언트 복잡도**: Sentinel은 대부분의 Redis 클라이언트가 지원하지만, Cluster는 클라이언트가 MOVED/ASK 리다이렉션을 처리해야 한다. 일부 언어(Python, Ruby)는 Cluster 클라이언트 성숙도가 낮음.
- **운영 복잡도**: Sentinel은 3개 Pod(마스터 1 + 리플리카 2) + Sentinel 3개 = 총 6개. Cluster는 최소 6개 Pod(마스터 3 + 리플리카 3). Cluster가 리소스 사용량이 많고, 노드 추가 시 슬롯 리밸런싱 필요.
- **읽기 부하 분산**: Sentinel은 리플리카로 읽기를 분산할 수 있지만, 복제 지연(lag)이 있어 Eventually Consistent. Cluster도 리플리카 읽기를 지원하지만, 기본적으로 마스터에서만 읽기.

**심화 질문**: Sentinel 모드에서 마스터가 10GB 메모리 제한에 도달했을 때, Cluster로 마이그레이션하는 과정은 어떻게 되는가? 데이터 다운타임 없이 가능한가?

---

## Q2: Sentinel이 마스터 장애를 감지하고 페일오버하는 과정

**질문**: Redis Sentinel이 마스터 장애를 감지하고 리플리카를 마스터로 승격시키는 상세한 과정은 무엇인가? 쿼럼(quorum)과 투표는 어떻게 작동하는가?

**핵심 포인트**:

- **SDOWN (Subjectively Down)**: 각 Sentinel은 마스터에게 1초마다 PING을 보낸다. `down-after-milliseconds`(기본 30초) 동안 응답이 없으면 해당 Sentinel은 마스터를 SDOWN으로 표시. 이것은 주관적 판단(한 Sentinel만의 의견).
- **ODOWN (Objectively Down)**: Sentinel은 다른 Sentinel들에게 `SENTINEL is-master-down-by-addr` 명령을 보내 마스터 상태를 물어본다. `quorum` 개수 이상의 Sentinel이 SDOWN에 동의하면 ODOWN(객관적 장애)으로 전환. 예: quorum=2이면 Sentinel 2개 이상이 동의해야 페일오버 시작.
- **리더 선출**: ODOWN 상태가 되면 Sentinel들이 투표하여 페일오버를 수행할 리더 Sentinel을 선출. 과반수(majority) 이상의 표를 받은 Sentinel이 리더. 예: Sentinel 3개 중 2개 이상 동의.
- **리플리카 선택**: 리더 Sentinel이 리플리카 중 하나를 새 마스터로 선택. 선택 기준: (1) 마스터와 연결이 끊긴 시간이 짧을수록 우선, (2) 리플리카 우선순위(slave-priority), (3) 복제 오프셋이 클수록 우선, (4) 사전순으로 빠른 RunID.
- **마스터 승격**: 선택된 리플리카에게 `SLAVEOF NO ONE` 명령을 보내 마스터로 승격. 승격된 리플리카는 `INFO replication`에서 `role:master`로 변경.
- **나머지 리플리카 재설정**: 리더 Sentinel이 나머지 리플리카들에게 `SLAVEOF <새 마스터 IP> 6379` 명령을 보내 새 마스터를 따르도록 설정. 이 과정을 `parallel-syncs` 설정에 따라 병렬로 수행(기본 1개씩).
- **페일오버 완료**: 모든 리플리카가 새 마스터를 따르면 페일오버 완료. Sentinel들은 내부 상태를 업데이트하고, 클라이언트가 `SENTINEL get-master-addr-by-name` 요청 시 새 마스터 주소 반환.

**심화 질문**: Sentinel 자체가 장애(예: Sentinel 2개가 죽음)나면 어떻게 되는가? quorum=2인데 Sentinel 1개만 남으면 페일오버가 불가능한가?

---

## Q3: Redis Cluster의 해시 슬롯 분배와 리밸런싱

**질문**: Redis Cluster는 16384개 슬롯을 어떻게 마스터에 분배하는가? 노드를 추가하거나 제거할 때 슬롯 리밸런싱은 어떻게 수행되는가?

**핵심 포인트**:

- **슬롯 할당**: 클러스터 초기화 시 `redis-cli --cluster create`가 16384개 슬롯을 마스터 수로 균등 분배. 예: 마스터 3개 → 각각 5461, 5462, 5461 슬롯. 슬롯 범위는 `CLUSTER NODES` 명령으로 확인 가능.
- **키-슬롯 매핑**: 키를 CRC16 해시로 변환하고 16384로 나눈 나머지가 슬롯 번호. 예: `CRC16("user:1000") % 16384 = 12345`. 슬롯 12345를 담당하는 마스터가 해당 키를 저장.
- **Hash Tag**: 키에 `{}`를 사용하면 괄호 안의 문자열만 해시 계산. `{user:1000}:session`과 `{user:1000}:cart`는 같은 슬롯에 배치되어 멀티키 연산 가능.
- **노드 추가 시 리밸런싱**: 새 마스터 추가 시 `redis-cli --cluster reshard`로 기존 마스터들로부터 슬롯을 이동. 예: 마스터 3개 → 4개 추가 시 각 마스터가 약 1365개 슬롯씩 새 마스터에게 이전. 슬롯 이동 중에도 서비스는 계속되며, 클라이언트는 ASK 리다이렉션으로 이동 중인 키에 접근.
- **슬롯 이동 과정**: (1) 대상 마스터에게 `CLUSTER SETSLOT <slot> IMPORTING <source-node-id>` 전송, (2) 소스 마스터에게 `CLUSTER SETSLOT <slot> MIGRATING <target-node-id>` 전송, (3) 소스 마스터에서 `MIGRATE` 명령으로 키를 대상으로 전송, (4) 슬롯 이동 완료 시 `CLUSTER SETSLOT <slot> NODE <target-node-id>` 전송하여 매핑 업데이트.
- **리밸런싱 중 클라이언트**: 슬롯이 이동 중일 때 클라이언트가 소스 마스터에 요청하면 `-ASK <slot> <target-ip:port>` 응답. 클라이언트는 대상 마스터에게 `ASKING` 명령 후 재요청. 이동 완료 후에는 `-MOVED` 응답으로 영구 리다이렉션.

**심화 질문**: 노드 추가 시 슬롯 리밸런싱 중에 해당 슬롯의 쓰기 요청이 들어오면 어떻게 처리되는가? 데이터 일관성은 보장되는가?

---

## Q4: Kubernetes Service와 Redis Sentinel discovery의 통합

**질문**: Kubernetes에서 Redis Sentinel을 배포할 때, Service와 Sentinel discovery를 어떻게 통합하는가? 클라이언트는 Service DNS와 Sentinel을 어떻게 함께 사용하는가?

**핵심 포인트**:

- **Sentinel Service**: OpsTree Operator는 `redis-sentinel-sentinel` Service(ClusterIP, 26379 포트)를 생성. 이 Service는 3개 Sentinel Pod를 로드밸런싱. 클라이언트는 이 Service DNS를 Sentinel 주소로 사용.
- **Headless Service**: `redis-sentinel-additional` Headless Service는 StatefulSet Pod의 고정 DNS 이름 제공. 예: `redis-sentinel-0.redis-sentinel-additional.default.svc.cluster.local`. Sentinel이 마스터 주소를 반환할 때 이 DNS 이름 사용.
- **클라이언트 연결 흐름**: (1) 클라이언트가 `redis-sentinel-sentinel:26379`에 연결, (2) Sentinel Service가 3개 Sentinel 중 하나로 라우팅, (3) Sentinel이 `SENTINEL get-master-addr-by-name mymaster` 응답으로 `redis-sentinel-1.redis-sentinel-additional:6379` 반환, (4) 클라이언트가 이 주소로 Redis 연결.
- **페일오버 시 Service 업데이트**: Sentinel이 페일오버를 수행하면 마스터 주소가 변경됨. 하지만 Kubernetes Service는 업데이트되지 않음(Service는 여전히 모든 Pod를 가리킴). 클라이언트는 Sentinel에게 다시 물어봐서 새 마스터를 발견.
- **읽기 부하 분산**: `redis-sentinel` Service는 마스터 + 리플리카 모두를 가리킴. 읽기 전용 클라이언트는 이 Service를 사용하여 리플리카로 분산 가능. 하지만 복제 지연이 있어 강한 일관성이 필요한 읽기에는 부적합.
- **Sentinel 고가용성**: Sentinel Service가 3개 Pod를 로드밸런싱하므로, Sentinel 1개가 죽어도 클라이언트는 계속 연결 가능. 클라이언트 라이브러리는 `SentinelAddrs`에 여러 주소를 설정하여 Sentinel 장애에 대비 가능.

**심화 질문**: Sentinel이 페일오버를 수행한 후, Kubernetes Service Endpoint가 업데이트되지 않아도 문제없는 이유는 무엇인가? 클라이언트가 Sentinel discovery를 사용하기 때문인가?

---

## Q5: Redis Operator가 관리하는 Day-2 Operation

**질문**: Redis Operator는 초기 배포 이후 어떤 Day-2 Operation을 자동화하는가? 스케일링, 버전 업그레이드, 백업/복원은 어떻게 수행되는가?

**핵심 포인트**:

- **리플리카 스케일링**: Sentinel CR의 `spec.kubernetesConfig.redisSecret` 필드를 수정하여 리플리카 수를 증가 가능. 예: Redis StatefulSet replicas를 3 → 5로 변경. Operator가 자동으로 새 리플리카 Pod를 생성하고, Sentinel이 새 리플리카를 마스터에 연결(`SLAVEOF`).
- **마스터 스케일링 (Cluster만 해당)**: Cluster CR의 `clusterSize`를 3 → 4로 변경하면 Operator가 새 마스터 Pod를 추가하고, `redis-cli --cluster reshard`로 슬롯 재분배. 하지만 이 과정은 수동 개입이 필요할 수 있음(Operator 버전에 따라 자동화 수준 다름).
- **버전 업그레이드**: CR의 `kubernetesConfig.image`를 `redis:7.0.12` → `redis:7.2.0`으로 변경. Operator가 StatefulSet Rolling Update 수행. Sentinel 모드는 리플리카 → 마스터 순서로 업그레이드하여 다운타임 최소화. Cluster 모드는 각 샤드의 리플리카 → 마스터 순서.
- **백업**: OpsTree Operator는 백업 자동화를 제공하지 않음. 사용자가 직접 CronJob으로 `redis-cli --rdb /backup/dump.rdb` 실행하거나, Velero로 PVC 스냅샷 생성 필요.
- **복원**: PVC를 새 Redis CR에 연결하거나, `redis-cli --rdb` 파일을 Pod에 복사 후 Redis 재시작. Operator는 복원 로직을 제공하지 않으므로 수동 작업.
- **모니터링**: Operator가 Redis Exporter를 사이드카로 배포하면, Prometheus가 메트릭 수집. Grafana 대시보드로 메모리 사용률, 초당 명령 수, 복제 지연 등 모니터링 가능.
- **장애 복구**: Sentinel 모드는 마스터 Pod 삭제 시 Sentinel이 자동 페일오버. Cluster 모드는 마스터 Pod 삭제 시 리플리카가 자동 승격. Operator는 CR 상태를 업데이트하지만, 실제 페일오버는 Redis/Sentinel 프로토콜이 수행.

**심화 질문**: Redis Operator가 백업/복원을 자동화하지 않는 이유는 무엇인가? Velero나 CronJob을 사용할 때의 트레이드오프는 무엇인가?

---

## Q6: Standalone Redis (Deployment)와 Operator 관리 Redis의 차이

**질문**: StatefulSet으로 Standalone Redis를 직접 배포하는 것과, Redis Operator로 Sentinel/Cluster를 배포하는 것의 차이는 무엇인가? Operator 없이도 고가용성을 달성할 수 있는가?

**핵심 포인트**:

- **Standalone 배포 (StatefulSet)**: Redis 이미지를 StatefulSet으로 배포하고, PVC로 데이터 보존, Service로 노출. 간단하지만 단일 장애점(SPOF). 마스터 Pod가 죽으면 StatefulSet이 자동으로 재시작하지만, 재시작 동안(수십 초) 서비스 중단.
- **Sentinel 없이 고가용성**: StatefulSet으로 마스터 1 + 리플리카 2를 배포하고, 수동으로 `redis-cli SLAVEOF`로 복제 설정 가능. 하지만 마스터 장애 시 자동 페일오버가 없음. 운영자가 수동으로 리플리카를 마스터로 승격해야 함.
- **Operator의 장점**: (1) CR로 선언적 관리 - `kind: Redis` 하나로 StatefulSet, Service, ConfigMap 자동 생성, (2) 자동 페일오버 - Sentinel/Cluster 프로토콜로 장애 감지 및 복구, (3) Day-2 Operation - 스케일링, 업그레이드, 모니터링 통합.
- **Operator의 복잡도**: CR, Operator Pod, RBAC, CRD 등 추가 리소스 필요. 간단한 개발 환경에서는 과도한 복잡도일 수 있음. 디버깅 시 Operator 로그와 Redis 로그를 모두 확인해야 함.
- **StatefulSet vs Deployment**: Redis는 StatefulSet으로 배포해야 함. 이유: (1) Pod 이름이 고정(`redis-0`, `redis-1`)되어 Headless Service DNS로 접근 가능, (2) PVC가 Pod에 바인딩되어 Pod 재시작 시에도 데이터 보존, (3) 순차 시작/종료로 복제 관계 유지.
- **언제 Operator 없이 배포하는가**: 개발/테스트 환경에서 간단한 캐시만 필요한 경우. Standalone Redis를 Deployment + emptyDir로 배포하고, 데이터 손실을 감수. 프로덕션에서는 Operator 또는 관리형 서비스(AWS ElastiCache, GCP Memorystore) 사용 권장.

**심화 질문**: Redis Operator 없이 Helm Chart(Bitnami)로 Sentinel을 배포할 때, 페일오버는 자동으로 동작하지만 Day-2 Operation이 수동인 이유는 무엇인가? Operator와 Helm의 역할 차이는 무엇인가?
