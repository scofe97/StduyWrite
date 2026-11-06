---
title: "kubelet 통계 API — stats-summary·nodes-stats RBAC"
tags: [kubernetes, kubelet, summary-api, rbac, nodes-proxy, metrics-server]
status: draft
source:
  - https://v1-36.docs.kubernetes.io/docs/reference/instrumentation/node-metrics/
  - https://kubernetes.io/docs/reference/kubelet-api/stats.v1alpha1/  # (2026-11-06 확인)
  - https://v1-36.docs.kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/
  - https://v1-36.docs.kubernetes.io/docs/reference/access-authn-authz/rbac/
  - https://v1-36.docs.kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/
  - https://raw.githubusercontent.com/kubernetes-sigs/metrics-server/v0.7.2/manifests/base/rbac.yaml
  - https://raw.githubusercontent.com/kubernetes-sigs/metrics-server/v0.7.2/README.md
updated: 2026-11-06
---

# kubelet 통계 API — stats-summary·nodes-stats RBAC

---

> 임시 참고 문서 — 정본은 나중에 따로 만듭니다.

노드에서 CPU·메모리·디스크를 직접 읽는 길은 kubelet 의 Summary API 입니다. 이 문서는 그 API 를 API 서버 프록시 경로로 읽는 법, 응답 필드의 뜻, 그리고 접근 권한에서 `nodes/stats` 와 `nodes/proxy` 가 왜 다른 무게인지를 정리합니다. 파이프라인 전체(cAdvisor → kubelet → metrics-server → `kubectl top`)는 이미 있는 문서가 설명하므로 여기서는 반복하지 않고 [관련 문서](#관련-문서)로 넘깁니다.

## 1. Summary API 를 프록시 경로로 읽기

> kubelet 은 노드·볼륨·파드·컨테이너 수준의 통계를 Summary API 로 내놓습니다. 클러스터 밖에서는 API 서버의 프록시를 거쳐 읽습니다.

### 어떤 문제가 생기나

`kubectl top` 은 CPU 와 메모리만 보여 줍니다. 노드의 에페메럴 스토리지, 파드가 쓰는 볼륨, 컨테이너의 쓰기 레이어 크기는 `kubectl top` 에 없습니다. metrics-server 가 가져가는 값이 자원 지표 몇 가지로 한정되기 때문입니다. 디스크가 차서 파드가 쫓겨나는 상황을 조사하려면 kubelet 이 재고 있는 원본 통계를 직접 열어야 합니다.

### 동작 원리

kubelet 은 통계를 모아 Summary API 로 내보냅니다. 노드 안의 kubelet 은 자기 포트에서 HTTPS 로 듣고 있어서 노드 밖에서 바로 닿기 어렵습니다. 그래서 API 서버가 `/api/v1/nodes/<노드 이름>/proxy/` 아래 경로를 kubelet 으로 그대로 전달해 줍니다. 공식 문서는 이렇게 말합니다.

> "You can send a proxied request to the stats summary API via the Kubernetes API server."

경로의 `proxy` 뒤쪽이 kubelet 쪽 경로입니다. 즉 kubelet 의 `/stats/summary` 가 API 서버에서는 `/api/v1/nodes/<노드>/proxy/stats/summary` 로 보입니다. 데이터 출처는 기본적으로 kubelet 안에 내장된 cAdvisor 입니다. `PodAndContainerStatsFromCRI` 기능 게이트를 켜고 CRI 가 통계를 지원하는 런타임을 쓰면 파드·컨테이너 수준 값은 CRI 에서 가져옵니다.

### 최소 예제

```bash
# 노드 이름 확인
kubectl get nodes -o name

# 프록시 경로로 Summary API 읽기 (<노드> 자리에 노드 이름)
kubectl get --raw "/api/v1/nodes/<노드>/proxy/stats/summary" | head -c 600

# 노드 수준만 보고 싶으면 jq 로 자른다
kubectl get --raw "/api/v1/nodes/<노드>/proxy/stats/summary" \
  | jq '.node | {cpu, memory, fs}'
```

`kubectl proxy` 를 띄우고 curl 로 같은 경로를 읽어도 됩니다.

```bash
kubectl proxy --port=8001 &
curl -s http://localhost:8001/api/v1/nodes/<노드>/proxy/stats/summary | head -c 600
```

### 흔한 함정

- 노드 이름을 틀리면 404 가 아니라 프록시 오류가 납니다. `kubectl get nodes` 에 나오는 이름을 그대로 씁니다.
- 이 경로를 읽는 권한은 아래 3절의 `nodes/proxy` 입니다. 지표를 읽을 뿐인데 필요한 권한은 훨씬 큽니다.
- 응답 값은 호출 시점의 표본입니다. 누적 값(`usageCoreNanoSeconds`)은 두 번 읽어 차이를 시간으로 나눠야 사용률이 됩니다.

### 공식 문서 근거

- [node-metrics](https://v1-36.docs.kubernetes.io/docs/reference/instrumentation/node-metrics/): `kubectl get --raw "/api/v1/nodes/minikube/proxy/stats/summary"` 가 같은 요청의 예로 실려 있습니다.



## 2. 응답에서 읽을 필드

> 응답은 `node` 하나와 `pods` 배열로 나뉩니다. 각 단위가 `cpu`·`memory`·파일시스템 계열 필드를 갖습니다.

### 어떤 문제가 생기나

JSON 을 열어 보면 `usageNanoCores`, `usageCoreNanoSeconds`, `workingSetBytes`, `usageBytes`, `rssBytes` 처럼 비슷한 이름이 늘어서 있습니다. 어느 값이 `kubectl top` 의 숫자이고 어느 값이 OOM 판단에 가까운지 모르고 읽으면 엉뚱한 값으로 결론을 냅니다.

### 동작 원리

최상위는 노드(`node`)와 파드 목록(`pods`)입니다. 노드 객체는 `nodeName`, `cpu`, `memory`, `network`, `fs`, `runtime` 등을 갖습니다. 파드 객체는 `podRef`, `containers`, 파드 cgroup 전체의 `cpu`·`memory`, `network`, `volume`, `ephemeral-storage` 를 갖습니다. 컨테이너는 `name`, `cpu`, `memory`, 쓰기 레이어 크기를 담는 `rootfs`, 로그 크기를 담는 `logs` 를 갖습니다. 값 하나하나의 뜻은 참조 문서가 이렇게 정의합니다.

| 필드 | 위치 | 공식 설명(요지) |
|------|------|----------------|
| `usageNanoCores` | `cpu` | 모든 코어를 합친 CPU 사용량을 표본 구간 평균으로 낸 값 |
| `usageCoreNanoSeconds` | `cpu` | 객체가 생긴 뒤 누적한 CPU 사용량 |
| `usageBytes` | `memory` | 접근 시점과 상관없이 쓰고 있는 메모리 전체 |
| `workingSetBytes` | `memory` | 최근 접근한 메모리·더티 메모리·커널 메모리를 포함. `usageBytes` 이하 |
| `rssBytes` | `memory` | 익명 메모리와 스왑 캐시 |
| `availableBytes` | `memory` | 메모리 한도에서 `workingSetBytes` 를 뺀 값. 한도가 없으면 생략 |
| `usedBytes`·`availableBytes`·`capacityBytes` | `fs` | 파일시스템의 사용·여유·전체 용량. `usedBytes` 는 대상(예: 컨테이너 rootfs)이 쓴 양이라 용량에서 여유를 뺀 값과 다를 수 있음 |
| `inodes`·`inodesUsed`·`inodesFree` | `fs` | inode 전체·사용·여유 |

참조 문서가 정의한 두 줄은 다음과 같습니다.

> "`usageNanoCores`: Total CPU usage (sum of all cores) averaged over the sample window."

> "`workingSetBytes`: The amount of working set memory. This includes recently accessed memory, dirty memory, and kernel memory. WorkingSetBytes is <= UsageBytes"

### 최소 예제

응답의 모양은 아래와 같습니다. 값은 설명용으로 지어낸 것이고, 실제 응답에는 `systemContainers`, `io`, `swap` 같은 필드가 더 있습니다.

```json
{
  "node": {
    "nodeName": "worker-1",
    "cpu":    { "usageNanoCores": 250000000, "usageCoreNanoSeconds": 98000000000 },
    "memory": { "usageBytes": 3000000000, "workingSetBytes": 2400000000, "availableBytes": 5600000000 },
    "fs":     { "capacityBytes": 100000000000, "usedBytes": 41000000000, "inodesFree": 6000000 }
  },
  "pods": [
    {
      "podRef": { "name": "web-0", "namespace": "demo" },
      "containers": [
        { "name": "app",
          "cpu": { "usageNanoCores": 12000000 },
          "memory": { "workingSetBytes": 80000000 },
          "rootfs": { "usedBytes": 4000000 },
          "logs": { "usedBytes": 1000000 } }
      ],
      "ephemeral-storage": { "usedBytes": 6000000 }
    }
  ]
}
```

파드별 메모리 상위 다섯을 뽑는 예입니다.

```bash
kubectl get --raw "/api/v1/nodes/<노드>/proxy/stats/summary" \
  | jq -r '.pods[] | [.podRef.namespace, .podRef.name, .memory.workingSetBytes] | @tsv' \
  | sort -k3 -n -r | head -5
```

### 흔한 함정

- 메모리는 `usageBytes` 가 아니라 `workingSetBytes` 를 봅니다. 앞의 값에는 회수 가능한 캐시가 들어 있어 실제 압박보다 커 보입니다. 두 값의 관계는 위 정의에 "WorkingSetBytes is <= UsageBytes" 로 적혀 있습니다.
- `usageNanoCores` 는 1코어가 10억 나노코어이니 `250000000` 은 0.25코어입니다.
- 컨테이너 `rootfs.usedBytes` 는 쓰기 레이어, `logs.usedBytes` 는 로그 크기입니다. 파드가 디스크를 먹는 원인을 가릴 때 이 둘과 볼륨을 따로 봅니다.
- `v1alpha1` 이라는 이름은 이 스키마의 API 버전입니다. 필드가 바뀔 수 있다는 뜻으로 읽고, 스크립트에 박아 둘 때는 쓰는 필드를 최소로 합니다.

### 공식 문서 근거

- [stats.v1alpha1](https://kubernetes.io/docs/reference/kubelet-api/stats.v1alpha1/) (2026-11-06 확인): `CPUStats`·`MemoryStats`·`FsStats`·`PodStats` 의 필드 정의.



## 3. nodes/stats 와 nodes/proxy 의 차이

> kubelet 은 요청 경로를 보고 `nodes` 의 하위 리소스를 정합니다. `/stats/*` 는 `nodes/stats` 이고, 목록에 없는 나머지는 전부 `nodes/proxy` 로 떨어집니다.

### 어떤 문제가 생기나

모니터링 에이전트에 "노드 통계 읽기" 권한만 주려는데, 경로가 `.../proxy/stats/summary` 라서 `nodes/proxy` 를 열어 주는 경우가 많습니다. 그런데 `nodes/proxy` 는 통계 읽기에 그치지 않습니다. 컨테이너 안에서 명령을 실행하는 kubelet API 까지 같이 열립니다.

### 동작 원리

kubelet 이 인가를 API 서버에 위임하는 구성(`--authorization-mode=Webhook`)에서는 kubelet 이 요청마다 `SubjectAccessReview` 를 부릅니다. 이때 동사는 HTTP 메서드(GET·HEAD → `get`, POST → `create`)에서, 리소스는 항상 `nodes`, 하위 리소스는 요청 경로에서 정해집니다.

| kubelet 경로 | resource | subresource |
|---|---|---|
| `/stats/*` | nodes | stats |
| `/metrics/*` | nodes | metrics |
| `/logs/*` | nodes | log |
| `/spec/*` | nodes | spec |
| `/checkpoint/*` | nodes | checkpoint |
| 나머지 전부 | nodes | proxy |

그래서 `nodes/stats` 는 통계 경로만 열고, `nodes/proxy` 는 나머지를 전부 엽니다. 공식 문서의 경고는 강합니다.

> "`nodes/proxy` permission grants access to all other kubelet APIs. This includes APIs that can be used to execute commands in any container running on the node."

더 놓치기 쉬운 문장이 이어집니다. 일부 엔드포인트는 HTTP GET 으로 웹소켓을 업그레이드해 쓰는데, 그 요청은 `get` 동사로 인가됩니다.

> "This means that **get** permission on `nodes/proxy` is not a read-only permission, and authorizes executing commands in any container running on the node."

즉 `nodes/proxy` 에 `get` 만 줘도 읽기 전용이 아닙니다.

문서는 세분화 인가도 설명합니다. 문서 기준으로 Kubernetes v1.36 부터 안정(stable)이고 기본으로 켜져 있습니다. `/pods`·`/runningPods`·`/configz`·`/healthz` 를 `nodes/proxy` 로 떨어뜨리기 전에 `nodes/pods`·`nodes/configz`·`nodes/healthz` 하위 리소스로 먼저 검사합니다. 이 기능이 없는 버전에서는 파드 목록을 읽는 데도 `nodes/proxy` 가 필요했다는 뜻입니다.

### 최소 예제

통계 계열 하위 리소스만 읽는 ClusterRole 과 바인딩입니다. 하위 리소스는 RBAC 에서 `리소스/하위리소스` 형태로 씁니다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-stats-reader
rules:
- apiGroups: [""]
  resources: ["nodes/stats", "nodes/metrics"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-stats-reader
subjects:
- kind: ServiceAccount
  name: collector
  namespace: demo
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: node-stats-reader
```

`nodes/proxy` 를 잠그는 쪽 점검은 다음처럼 합니다.

```bash
kubectl auth can-i get nodes/proxy --as=system:serviceaccount:demo:collector
kubectl auth can-i get nodes/stats --as=system:serviceaccount:demo:collector
```

### 흔한 함정

- `nodes/stats` 만 준 계정이 `.../proxy/stats/summary` 를 부르면 막힐 수 있습니다. 이 URL 은 API 서버 입장에서 `nodes` 의 `proxy` 하위 리소스 요청이기 때문입니다(RBAC 문서가 `.../pods/{name}/log` 를 `pods/log` 로 대응시키는 규칙의 같은 적용입니다). `nodes/stats` 는 kubelet 이 자기 경로를 인가할 때, 또는 kubelet 에 직접 붙는 클라이언트에 필요한 권한입니다. 어느 쪽 권한이 필요한지는 호출 경로가 정합니다.
- API 서버가 kubelet 에 붙을 때 쓰는 클라이언트 인증서 사용자도 위 하위 리소스에 인가돼 있어야 합니다. 문서가 `verb=*` 로 `proxy`·`stats`·`log`·`spec`·`metrics` 를 나열합니다.
- `nodes/proxy` 를 "읽기 전용 모니터링 권한"으로 문서화하거나 Helm 차트 기본값에 넣으면 위 경고가 그대로 노출 면적이 됩니다.

### 공식 문서 근거

- [Kubelet authentication/authorization](https://v1-36.docs.kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/): 경로-하위 리소스 표, 경고 문장 두 개, 세분화 인가 절.
- [RBAC](https://v1-36.docs.kubernetes.io/docs/reference/access-authn-authz/rbac/): "use a slash (`/`) to delimit the resource and subresource."



## 4. metrics-server 와의 관계

> metrics-server 는 kubelet 에서 자원 지표를 가져와 Metrics API 로 내놓는 애드온입니다. 0.6.x 부터는 `/stats/summary` 가 아니라 `/metrics/resource` 를 읽습니다.

### 어떤 문제가 생기나

옛 글은 "metrics-server 는 kubelet Summary API 를 읽는다"고 설명합니다. 지금 클러스터에서 권한을 설계하면서 이 문장을 믿으면, `nodes/stats` 를 열어 줬는데 실제로는 `nodes/metrics` 가 필요한 상황에서 헤맵니다.

### 동작 원리

공식 문서의 노트가 변경점을 못 박아 둡니다.

> "Beginning with `metrics-server` 0.6.x, `metrics-server` queries the `/metrics/resource` kubelet endpoint, and not `/stats/summary`."

`/metrics/*` 는 3절 표에서 `nodes/metrics` 에 대응합니다. metrics-server v0.7.2 의 RBAC 매니페스트도 `nodes/metrics` 에 `get` 을 주고 `pods`·`nodes` 에 `get`·`list`·`watch` 를 줍니다. 읽어 온 값은 API 서버가 Metrics API 로 서빙하고, HPA·VPA·`kubectl top` 이 그것을 씁니다. kubelet 쪽 요건으로 README 는 "Nodes must have Webhook authentication and authorization enabled." 라고 적습니다.

### 최소 예제

```bash
# metrics-server 가 서빙하는 Metrics API (kubectl top 이 읽는 곳)
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes" | head -c 400

# kubelet 이 직접 내는 자원 지표 (프로메테우스 텍스트 형식)
kubectl get --raw "/api/v1/nodes/<노드>/proxy/metrics/resource" | head -20
```

### 흔한 함정

- Summary API 는 metrics-server 의 입력이 아니어도 계속 있습니다. 디스크·볼륨 같은 Summary 전용 정보를 읽는 도구는 여전히 `/stats/summary` 를 부릅니다.
- metrics-server 의 `--kubelet-insecure-tls` 는 README 가 "For testing purposes only" 라고 못 박은 옵션입니다.
- "kubelet 에서 읽는다"를 근거로 metrics-server 에 `nodes/proxy` 를 주지 않습니다. 필요한 것은 `nodes/metrics` 입니다.

### 공식 문서 근거

- [node-metrics](https://v1-36.docs.kubernetes.io/docs/reference/instrumentation/node-metrics/): 0.6.x 노트.
- [resource-metrics-pipeline](https://v1-36.docs.kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/): "The API server serves Metrics API for use by HPA, VPA, and by the `kubectl top` command."
- [metrics-server v0.7.2 rbac.yaml](https://raw.githubusercontent.com/kubernetes-sigs/metrics-server/v0.7.2/manifests/base/rbac.yaml): `nodes/metrics` 의 `get`.



## 확인하지 못한 것

- 실제 클러스터에서 위 명령과 RBAC 를 돌려 보지 않았습니다. JSON 은 필드 구조를 보이려고 지어낸 값입니다.
- `nodes/stats` 만 가진 사용자가 API 서버의 `.../proxy/stats/summary` 를 부르면 막힌다는 3절 함정은 열어 본 RBAC 문서의 하위 리소스 규칙(`.../pods/{name}/log` → `pods/log`)에서 이끌어 낸 것입니다. 노드 프록시 경로를 이 규칙에 대응시킨 문장은 열어 본 문서에 없었습니다.
- 응답 최상위 `Summary` 타입의 정의는 참조 문서에서 열지 못했습니다. `node`·`pods` 구성은 `PodStats`·`NodeStats` 정의에서 확인한 범위입니다.
- 세분화 인가가 Kubernetes v1.36 에서 안정이라는 표기는 열어 본 시점의 문서 문장 그대로이며, 버전별 기본값은 따로 확인하지 못했습니다.
- RBAC 문서의 `system:kubelet-api-admin` 클러스터롤 설명과 `kubectl auth can-i` 절은 열어 본 범위에 없었습니다.



## 관련 문서

- [자원 모니터링 파이프라인 — kubelet이 재는 것과 kubectl top이 읽는 것](../../08_cloud/docs/kubernetes/cluster-administration/01-01.자원%20모니터링%20파이프라인%20—%20kubelet이%20재는%20것과%20kubectl%20top이%20읽는%20것.md) — cAdvisor → kubelet → metrics-server → `kubectl top` 흐름
