---
title: etcd 헬스와 유지보수 — 상태 판독과 compaction·defrag·quota
tags: [kubernetes, etcd, etcdctl, compaction, defrag, quota, NOSPACE, snapshot, kubeadm]
status: draft
source:
  - https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
  - https://etcd.io/docs/v3.5/tutorials/how-to-check-cluster-status/
  - https://etcd.io/docs/v3.5/op-guide/maintenance/
  - https://etcd.io/docs/v3.5/dev-guide/limit/
  - https://github.com/kubernetes/kubernetes/blob/v1.31.0/cmd/kubeadm/app/phases/etcd/local.go
  - https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/
related:
  - ../api/API%20%EC%84%9C%EB%B2%84%20%ED%97%AC%EC%8A%A4%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8.md
  - ../../../../05_data/book/designing-data-intensive-applications/10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md
  - ../../../book/production-kubernetes/02-01.Deployment%20Models%20%E2%80%94%20%EB%B0%B0%ED%8F%AC%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%9D%B8%ED%94%84%EB%9D%BC%20%EA%B5%AC%EC%B6%95.md
updated: 2026-11-11
---

# etcd 헬스와 유지보수 — 상태 판독과 compaction·defrag·quota

---

> etcd 는 살아 있어도 디스크 한도를 넘으면 쓰기를 멈춥니다. 그래서 점검은 "응답하는가"에서 끝나지 않고, 멤버끼리 같은 상태인지와 DB 크기가 한도에서 얼마나 떨어져 있는지까지 읽어야 합니다.

## 학습 목표

> 이 문서를 읽고 나면 아래 다섯 가지를 스스로 해낼 수 있습니다.

1. `etcdctl endpoint health`·`endpoint status`·`endpoint hashkv` 가 각각 무엇을 확인하는지 구분할 수 있습니다.
2. revision 이 쌓이는 이유와 compaction 이 그것을 어떻게 줄이는지 설명할 수 있습니다.
3. compaction 뒤에도 DB 파일이 줄지 않는 이유와 defrag 를 멤버마다 차례로 돌려야 하는 이유를 말할 수 있습니다.
4. quota 를 넘었을 때 생기는 NOSPACE 알람과 복구 순서를 적을 수 있습니다.
5. snapshot 을 저장하고 그 파일이 쓸 만한지 확인하는 명령을 적을 수 있습니다.

다루지 않는 범위가 있습니다. etcd 가 왜 홀수 멤버로 합의하는지는 [합의와 코디네이션 서비스](../../../../05_data/book/designing-data-intensive-applications/10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md)가 설명합니다. 컨트롤 플레인과 etcd 를 어떻게 배치하는지는 [배포 모델과 고가용성 인프라 구축](../../../book/production-kubernetes/02-01.Deployment%20Models%20%E2%80%94%20%EB%B0%B0%ED%8F%AC%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%9D%B8%ED%94%84%EB%9D%BC%20%EA%B5%AC%EC%B6%95.md)이 설명합니다. 복원 절차도 이 문서 밖입니다.



## 1. etcd 가 멈추면 생기는 일

> 쿠버네티스의 모든 오브젝트는 etcd 에 저장되므로, etcd 가 쓰기를 못 하면 클러스터는 아무것도 바꾸지 못합니다.

Deployment 를 만들든 Pod 를 지우든, API 서버는 결과를 etcd 에 씁니다. 공식 문서는 etcd 가 리더를 잃는 상황을 이렇게 적습니다. 자원이 모자라 heartbeat 시간 제한을 넘기면 클러스터가 불안정해지고, 리더가 없는 동안에는 아무것도 바꿀 수 없으며 새 Pod 도 스케줄되지 않습니다.[^k8s-etcd]

그래서 공식 문서는 운영 조건을 몇 가지 정해 둡니다.[^k8s-etcd]

- 멤버 수는 홀수로 두고, 운영 환경에서는 다섯 개를 권합니다.
- 자원 다툼을 피하려고 etcd 를 전용 머신이나 격리된 환경에서 돌립니다.
- 운영에 쓰는 최소 버전은 3.4.29 이상, 3.5.11 이상입니다.

kubeadm 은 기본적으로 etcd 를 컨트롤 플레인 노드의 static pod 로 띄웁니다.[^k8s-etcd] 이 문서의 명령은 그 구성을 기준으로 합니다.

멈추는 원인은 리더 상실만이 아닙니다. 멤버가 모두 살아 있고 리더도 있는데 쓰기가 거부될 수 있습니다. DB 가 정해진 한도(quota)를 넘었을 때입니다(§5). 이 상황은 "응답하는가"만 보는 점검으로는 잡히지 않습니다. 그래서 아래 절들은 응답 여부, 멤버 간 일치, DB 크기를 차례로 읽습니다.



## 2. 멤버 상태 판독

> `endpoint health` 는 쓰기가 되는지, `endpoint status` 는 누가 리더이고 DB 가 얼마나 큰지, `endpoint hashkv` 는 멤버끼리 데이터가 같은지를 봅니다.

etcd Pod 가 `Running` 이라는 사실만으로는 쓰기가 되는지, 멤버끼리 같은 데이터를 갖는지 알 수 없습니다. 그래서 `etcdctl` 로 멤버에 직접 묻습니다. kubeadm 클러스터의 etcd 는 TLS 로만 받으므로 인증서 세 개를 넘겨야 합니다. 경로는 etcd Pod 정의에서 읽을 수 있다고 공식 문서가 안내합니다.[^k8s-etcd] 아래 예시는 인증서 인자를 줄였으니 실제로는 `--cacert`·`--cert`·`--key` 를 붙입니다.

### 쓰기가 되는가 — endpoint health

`endpoint health` 는 멤버마다 실제로 제안(proposal)을 하나 커밋해 보고 걸린 시간을 알려 줍니다.[^etcd-status]

```bash
etcdctl --endpoints=$ENDPOINTS endpoint health
```

```bash
10.240.0.17:2379 is healthy: successfully committed proposal: took = 3.345431ms
```

"committed proposal" 이 나왔다는 것은 그 멤버를 거쳐 합의가 이뤄졌다는 뜻입니다. 단순히 포트가 열린 것보다 강한 신호입니다.

### 리더와 DB 크기 — endpoint status

`endpoint status` 는 멤버마다 한 줄씩 상태를 보여 줍니다. `-w table` 을 붙이면 표로 나옵니다.[^etcd-status]

```bash
etcdctl --endpoints=$ENDPOINTS endpoint status -w table
```

표에는 열이 열 개 있습니다. ENDPOINT, ID, VERSION, DB SIZE, IS LEADER, IS LEARNER, RAFT TERM, RAFT INDEX, RAFT APPLIED INDEX, ERRORS 입니다. 공식 예시에서는 멤버 셋 가운데 하나만 `IS LEADER` 가 `true` 입니다. 셋 모두 `RAFT TERM` 은 4, `RAFT INDEX` 는 16726 으로 같습니다.[^etcd-status]

etcd 문서는 각 열의 뜻을 따로 정의하지 않습니다. 그래서 아래 판독은 열 이름과 Raft 의 일반 개념에서 읽은 것입니다.

| 열 | 점검에서 보는 것 |
|---|---|
| `IS LEADER` | 정확히 한 멤버만 `true` 인가. 없거나 둘이면 이상입니다 |
| `RAFT TERM` | 멤버끼리 같은가. 지난 점검보다 크게 늘었다면 그 사이 리더 선출이 여러 번 있었다는 뜻입니다 |
| `RAFT INDEX` | 멤버끼리 같거나 가까운가. 한 멤버만 뒤처지면 그 멤버가 따라오지 못하는 중입니다 |
| `DB SIZE` | quota(§5)에서 얼마나 떨어져 있는가 |
| `ERRORS` | 비어 있는가. 알람이 켜지면 여기에 나타납니다 |

`--cluster` 를 쓰면 `--endpoints` 에 하나만 적어도 멤버 목록을 받아 모든 멤버를 조회합니다.[^etcd-status]

### 멤버끼리 데이터가 같은가 — endpoint hashkv

`endpoint hashkv` 는 멤버마다 저장된 키-값의 해시를 계산합니다. 정상이라면 모든 멤버의 HASH 가 같습니다.[^etcd-status]

```bash
etcdctl --endpoints=$ENDPOINTS endpoint hashkv --cluster --write-out=table
```

### kubelet 의 probe

kubeadm v1.31 은 etcd static pod 의 probe 를 다음처럼 겁니다.[^kubeadm-etcd] liveness 는 `/livez`, readiness 와 startup 은 `/readyz` 입니다. API 서버와 같은 이름의 엔드포인트입니다. 엔드포인트별 뜻은 [API 서버 헬스 엔드포인트](../api/API%20%EC%84%9C%EB%B2%84%20%ED%97%AC%EC%8A%A4%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8.md)를 참고합니다. 따라서 `kube-system` 의 `etcd-<노드>` Pod 재시작 횟수도 함께 봅니다.



## 3. revision 과 compaction

> etcd 는 키를 덮어쓰지 않고 새 revision 을 쌓으므로, 오래된 revision 을 버리는 compaction 이 없으면 저장 공간이 계속 늘어납니다.

etcd 는 키를 바꿀 때마다 이전 값을 지우지 않고 새 revision 으로 남깁니다. watch 가 "revision N 이후의 변경"을 받을 수 있는 것도 이 이력 덕분입니다. 대신 이력이 끝없이 쌓이면 공간을 다 씁니다. compaction 은 어느 revision 이전의, 이미 새 값으로 대체된 이력을 버립니다.[^etcd-maint]

```bash
etcdctl compact 3
```

이렇게 compaction 한 뒤 그보다 이른 revision 을 읽으려 하면 실패합니다.[^etcd-maint]

```bash
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

손으로 돌리지 않아도 됩니다. etcd 는 자동 compaction 을 두 방식으로 제공합니다.[^etcd-maint]

| 모드 | 설정 예 | 동작 |
|---|---|---|
| `periodic` (기본) | `--auto-compaction-retention=1h` | 지정한 시간만큼의 이력을 남기고 그보다 오래된 것을 버립니다 |
| `revision` | `--auto-compaction-retention=1000` | 5분마다 최신 revision 에서 1000 을 뺀 지점까지 버립니다 |

kube-apiserver 도 `--etcd-compaction-interval`(기본 5분) 마다 스스로 compaction 을 요청합니다.[^apiserver] 그래서 kubeadm 클러스터에서 compaction 은 대개 이미 돌고 있습니다. 점검에서 확인할 것은 다음 절의 결과, 곧 DB 파일 크기입니다.



## 4. compaction 뒤의 defrag

> compaction 은 공간을 비워 둘 뿐 파일을 줄이지 않으므로, 파일 크기를 실제로 줄이려면 defrag 를 멤버마다 돌립니다.

compaction 으로 버린 이력의 자리는 DB 파일 안에 빈칸으로 남습니다. etcd 는 그 빈칸을 다음 쓰기에 재사용하지만 파일 시스템에 돌려주지는 않습니다. 그래서 compaction 이 잘 돌아도 `DB SIZE` 는 그대로일 수 있습니다. defrag 는 빈칸을 정리해 그 공간을 파일 시스템에 돌려줍니다.[^etcd-maint]

```bash
etcdctl defrag                    # 지정한 엔드포인트 하나
etcdctl defrag --cluster          # 모든 멤버
etcdctl defrag --data-dir <경로>  # etcd 가 꺼져 있을 때 데이터 디렉터리에 직접
```

defrag 에는 조심할 성질이 둘 있습니다.[^etcd-maint]

- 멤버 단위로 돕니다. 한 멤버에서 돌린 결과가 다른 멤버로 복제되지 않습니다.
- 도는 동안 그 멤버는 읽기도 쓰기도 받지 않습니다.

두 성질을 합치면 운영 방식이 정해집니다. 모든 멤버를 한꺼번에 돌리면 그동안 클러스터 전체가 막힐 수 있습니다. 그러니 한 멤버씩 차례로 돌리고, 한 멤버가 끝나 `endpoint health` 가 돌아온 것을 확인한 뒤 다음으로 넘어갑니다.

쿠버네티스 공식 문서는 defrag 를 비싼 작업이라 보고 가능한 한 드물게 돌리라고 합니다. 동시에 어느 멤버도 quota 를 넘지 않게 하라고 적고, CronJob 으로 돌릴 수 있는 `etcd-defrag` 같은 도구를 권합니다.[^k8s-etcd]



## 5. quota 와 NOSPACE 알람

> DB 가 `--quota-backend-bytes` 를 넘으면 NOSPACE 알람이 켜지고, 클러스터는 읽기와 삭제만 받는 상태로 바뀝니다.

etcd 는 DB 크기에 상한을 둡니다. `--quota-backend-bytes` 로 정하며 기본값은 2 GiB 입니다. 공식 문서가 권하는 최대치는 8 GiB 이고, 그보다 크게 잡으면 etcd 가 시작할 때 경고를 냅니다.[^etcd-limit]

quota 를 넘으면 클러스터 전체에 NOSPACE 알람이 켜집니다. 그때부터 클러스터는 유지보수 모드에 들어가 키 읽기와 삭제만 받습니다.[^etcd-maint] 쓰기를 못 하니 쿠버네티스 쪽에서는 아무것도 바꾸지 못합니다. §1 에서 말한 "살아 있는데 멈춘" 상태가 이것입니다.

```bash
etcdctl alarm list
```

```bash
memberID:13803658152347727308 alarm:NOSPACE
```

### 알람에서 빠져나오는 순서

공식 문서의 복구 순서는 세 단계로 나뉩니다. 공간을 비우고 그 공간을 파일 시스템에 돌려준 뒤 알람을 끕니다.[^etcd-maint]

1. `endpoint status --write-out=json` 에서 현재 revision 을 읽습니다.
2. 그 revision 으로 `etcdctl compact <revision>` 을 돌려 이력을 버립니다.
3. `etcdctl defrag` 로 빈 공간을 파일 시스템에 돌려줍니다.
4. `etcdctl alarm disarm` 으로 알람을 끕니다.
5. 시험 삼아 키 하나를 `put` 해 `OK` 가 나오는지 봅니다.

순서가 중요합니다. 공간을 비우기 전에 알람부터 끄면 곧바로 다시 켜집니다.

### 넘기 전에 보는 지표

알람이 켜지기 전에 알아채려면 두 지표를 봅니다.[^etcd-maint]

| 지표 | 뜻 |
|---|---|
| `etcd_mvcc_db_total_size_in_bytes` | DB 파일의 전체 크기 |
| `etcd_mvcc_db_total_size_in_use_in_bytes` | 그 가운데 실제로 쓰는 크기 |

두 값의 차이가 defrag 로 돌려받을 수 있는 공간입니다. 전체 크기가 quota 에 다가가는데 쓰는 크기는 작다면 defrag 할 때입니다. 둘 다 quota 에 다가가면 데이터 자체가 많은 것이니 정리할 오브젝트를 찾거나 quota 를 다시 정해야 합니다. 이 두 이름은 v3.4 부터이고 그 전에는 `etcd_debugging_` 으로 시작했습니다.

공식 문서에는 하나 더 적혀 있습니다. Put·Txn·LeaseGrant 요청이 공간 부족 오류(ErrGRPCNoSpace)를 돌려받았는데도 실제로는 기록됐을 수 있습니다.[^etcd-maint] 알람 직후 오류를 받은 쓰기가 반영됐는지는 다시 읽어 확인합니다.



## 6. snapshot 저장과 확인

> 백업은 파일이 있다는 것만으로 끝나지 않고, 그 파일이 읽히는지 확인해야 쓸모가 있습니다.

etcd 를 잃으면 클러스터 상태 전체를 잃습니다. 그래서 공식 문서는 정기적인 snapshot 백업을 권하고, 저장 명령을 이렇게 보입니다.[^k8s-etcd]

```bash
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=<trusted-ca-file> --cert=<cert-file> --key=<key-file> \
  snapshot save <backup-file-location>
```

저장한 파일은 `etcdutl` 로 확인합니다. HASH, REVISION, TOTAL KEYS, TOTAL SIZE 가 표로 나옵니다.[^k8s-etcd]

```bash
etcdutl --write-out=table snapshot status snapshot.db
```

`etcdctl snapshot status` 도 같은 일을 했지만 v3.5 부터 폐기 예정이고 v3.6 에서 빠집니다.[^k8s-etcd] 점검에서는 파일 크기와 날짜만 보지 않고 이 명령의 결과를 남깁니다. TOTAL KEYS 가 0 이거나 명령이 실패하면 그 백업은 복원에 쓸 수 없습니다.



## 7. 점검 질문

> 위 내용을 실제 점검 상황에 대 봅니다.

### Q1. 모두 healthy 인데 쓰기가 거부될 때

`etcdctl alarm list` 와 `endpoint status` 의 `DB SIZE`·`ERRORS` 를 봅니다. NOSPACE 알람이 켜진 상태라면 멤버는 살아 있지만 쓰기를 받지 않습니다. 복구는 §5 의 순서대로 compaction → defrag → `alarm disarm` 입니다.

### Q2. compaction 뒤에도 DB SIZE 가 그대로일 때

고장이 아닙니다. compaction 은 파일 안에 빈칸을 만들 뿐 파일을 줄이지 않습니다. 줄이려면 defrag 가 필요하고, 멤버마다 차례로 돌립니다. 두 `etcd_mvcc_db_total_size_*` 지표의 차이로 돌려받을 공간을 미리 가늠할 수 있습니다.

### Q3. defrag 를 한 번에 돌려도 되는가

defrag 는 도는 동안 그 멤버의 읽기·쓰기를 막습니다. 모든 멤버를 한꺼번에 돌리면 그동안 클러스터 전체가 막힐 수 있습니다. 한 멤버씩 돌리고 `endpoint health` 를 확인한 뒤 다음으로 넘어가는 편이 안전합니다.

### Q4. 백업 파일이 있으면 점검이 끝났는가

아직입니다. `etcdutl snapshot status` 로 파일이 읽히는지, REVISION 과 TOTAL KEYS 가 정상 범위인지를 확인해야 합니다. 파일이 있다는 것은 저장이 시도됐다는 뜻일 뿐입니다.



## 관련 문서

> etcd 를 다른 쪽에서 다루는 문서입니다.

- [API 서버 헬스 엔드포인트](../api/API%20%EC%84%9C%EB%B2%84%20%ED%97%AC%EC%8A%A4%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8.md) — API 서버 `/readyz` 의 `etcd` 검사가 실패할 때 출발점
- [합의와 코디네이션 서비스](../../../../05_data/book/designing-data-intensive-applications/10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) — 홀수 멤버와 정족수가 왜 필요한가
- [배포 모델과 고가용성 인프라 구축](../../../book/production-kubernetes/02-01.Deployment%20Models%20%E2%80%94%20%EB%B0%B0%ED%8F%AC%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%9D%B8%ED%94%84%EB%9D%BC%20%EA%B5%AC%EC%B6%95.md) — etcd 를 컨트롤 플레인과 어떻게 배치하는가

[^k8s-etcd]: Kubernetes — Operating etcd clusters for Kubernetes. 운영 버전, 홀수 멤버, 리더 상실의 영향, kubeadm static pod, defrag 권고, snapshot 저장·확인. <https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/>

[^etcd-status]: etcd — How to check Cluster status. `endpoint status`·`endpoint health`·`endpoint hashkv` 와 출력 예시. <https://etcd.io/docs/v3.5/tutorials/how-to-check-cluster-status/>

[^etcd-maint]: etcd — Maintenance. compaction·자동 compaction·defrag·space quota·NOSPACE 알람과 복구·관련 지표. <https://etcd.io/docs/v3.5/op-guide/maintenance/>

[^etcd-limit]: etcd — System limits. 저장 한도 기본 2 GiB, 권장 최대 8 GiB. <https://etcd.io/docs/v3.5/dev-guide/limit/>

[^kubeadm-etcd]: kubernetes/kubernetes v1.31.0 — `cmd/kubeadm/app/phases/etcd/local.go`. etcd static pod 의 LivenessProbe `/livez`, ReadinessProbe·StartupProbe `/readyz`. <https://github.com/kubernetes/kubernetes/blob/v1.31.0/cmd/kubeadm/app/phases/etcd/local.go>

[^apiserver]: Kubernetes — kube-apiserver 명령행 레퍼런스. `--etcd-compaction-interval` 기본 5m0s, 0 이면 API 서버의 compaction 요청을 끕니다. <https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/>
