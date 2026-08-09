# Flow DSL 명세 (v0.4)

## 제1원칙 — 시각화를 통한 이해

**이 프로젝트의 목적은 흐름도를 그리는 것이 아니라, 흐름도를 통해 이론을 이해시키는 것입니다.** 모든 판단은 여기서 갈립니다. 어떤 필드를 채울지, 문장을 어떻게 쓸지, 무엇을 노드 창에 넣고 무엇을 패널로 보낼지 — 전부 "이게 독자의 이해를 늘리는가"로 결정합니다. 정확하지만 읽히지 않는 표현보다, 정확하면서 읽히는 표현을 찾을 때까지 고쳐 씁니다.

따라오는 작성 규칙입니다. 문체 규약의 정본은 `writing-method`의 [보강 러너](../../../.claude/skills/writing-method/references/runners/augment.md)이며, 여기서는 이 프로젝트에 적용되는 형태만 적습니다.

**1. 합니다체로 씁니다.** `detail`·`narration`·`info`·`inOut` 등 독자가 읽는 모든 문자열에 적용합니다. 노드 `label`과 메커니즘 데이터(테이블 셀, describe 줄)는 실제 시스템의 식별자이므로 예외입니다.

**2. 키워드가 아니라 완전한 문장으로 씁니다.** "nat 테이블 조회"는 무엇을 조회해서 어떻게 된다는 것인지 알려주지 않습니다. "라우팅을 결정하기 전에 nat 테이블을 먼저 확인합니다"처럼 주어와 서술어를 갖춘 문장으로 씁니다. 짧은 `info` 줄도 마찬가지입니다.

**3. "왜"를 담습니다.** 무슨 일이 일어나는지만 적으면 암기 대상이 되고, 왜 그래야 하는지를 적으면 이해 대상이 됩니다. "PREROUTING 훅에서 DNAT가 일어납니다"보다 "목적지를 바꾸는 일은 경로를 정하기 전에 끝나야 하므로, DNAT는 라우팅 이전 단계인 PREROUTING에 자리합니다"가 낫습니다.

**4. 전문용어는 처음 나올 때 풀어 씁니다.** 입문자가 읽는다고 가정합니다. `skb`, `netns`, `conntrack` 같은 약어는 첫 등장에서 무엇의 줄임말이고 무슨 역할인지 한 번 밝히고, 그 뒤로는 그냥 씁니다. 용어를 피하라는 뜻이 아닙니다 — 용어를 배우게 하되 모르는 채 지나가지 않게 합니다.

**5. 인과의 주체를 바꾸지 않습니다.** 문장을 다듬다 주어가 바뀌면 문장은 매끄러워져도 사실이 달라집니다. "커널이 패킷을 큐에 넣습니다"와 "패킷이 큐에 쌓입니다"는 다른 진술입니다. 누가 무엇을 하는지 확인하고 씁니다.

**6. 클릭 없이도 흐름이 읽히게 합니다.** 노드 창(`info`·`inOut`·메커니즘 배지)만 훑어도 전체 이야기가 통하게 쓰고, 패널은 그 이야기의 근거와 세부를 담습니다. 패널을 열어야만 무슨 일인지 알 수 있다면 창이 제 몫을 못 한 것입니다.

---

살아있는 흐름도를 선언하는 JSON DSL입니다. Upload Labs의 표현 문법(창형 노드·모양 포트·흐르는 입자·병목)을 학습 시각화용으로 옮겼고, 저장 구조는 React Flow 호환 `parentId` 평면 구조를 따라 이후 드래그 GUI(B단계)로 이식할 수 있게 했다.

기계 검증은 [flow.schema.json](flow.schema.json)이 담당한다. 이 문서는 각 필드의 의미와 렌더링 규칙의 정본이다.

---

## 최상위 구조

```json
{
  "meta":   { ... },
  "nodes":  [ ... ],
  "edges":  [ ... ],
  "trace":  { ... },
  "stream": { ... }
}
```

`meta.mode`가 `"trace"`면 `trace` 블록이 필수, `"stream"`이면 `stream` 블록이 필수다.

## meta

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `title` | string | ✅ | 다이어그램 제목. 헤더에 표시 |
| `subtitle` | string | | 부제 (예: "eth0 수신부터 Pod 도달까지") |
| `mode` | `"trace"` \| `"stream"` | ✅ | trace = 개체 1개 추적, stream = 연속 흐름 (v0.1 렌더러는 trace만 완성, stream은 스텁) |
| `direction` | `"LR"` \| `"TB"` | | 주 흐름 방향. 기본 `LR`(좌→우). 리눅스 user↔kernel처럼 계층이 상하인 흐름은 `TB` |

## nodes

노드는 **평면 배열**이다. 중첩은 `parentId` 참조로만 표현한다 (React Flow 모델).

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `id` | string | ✅ | 고유 식별자. 엣지·trace가 참조 |
| `parentId` | string \| null | | 부모 그룹의 id. 없거나 null이면 최상위 |
| `type` | string | ✅ | `"group"`이면 컨테이너, 그 외는 **자유 문자열**입니다. 렌더링에 관여하지 않는 의미 라벨이며, 도메인별 권장 어휘는 [`vocabulary.json`](vocabulary.json)의 `domains`에 있습니다. 메커니즘 이름(예약어)은 쓸 수 없습니다 — 자세한 이유는 [VOCABULARY.md](../VOCABULARY.md) |
| `role` | 닫힌 enum | | DFD·플로차트식 역할. **정본은 [`vocabulary.json`](vocabulary.json)의 `roles`** 입니다. 시각 변형은 아래 §역할별 시각 |
| `lane` | string | | 이 노드가 **누구의 행위인가**. `meta.lanes`에 선언한 id 를 씁니다. 왕복이 있는 흐름(§레인)에서만 쓰고, 없으면 생략합니다 |
| `label` | string | ✅ | 표시 이름 |
| `sublabel` | string | | 창 내부에 표시하는 보조 설명 한 줄 |
| `collapsed` | boolean | | `type: "group"` 전용. true면 접힌 상태로 시작 |
| `ports` | object | | `{ "in": [Port], "out": [Port] }`. 생략 시 kind `"data"` 인 in/out 포트 1개씩 자동 생성 |
| `icon` | string | | 제목바 좌측 기호 1자. 기술 문서 톤에 맞는 절제된 기하 기호를 씁니다(컬러 이모지는 플랫폼마다 모양이 달라 피합니다). 생략 시 role 기본값: process ▣ · store ▤ · external ◇ · decision ◈ |
| `info` | string[] | | **창 내부에 상시 표시하는 설명 1~2줄.** 이 노드가 하는 일을 입문자가 읽고 이해할 수 있는 완전한 문장으로 씁니다 (제1원칙 2·3항). 예: `["라우팅을 정하기 전에 nat 테이블을 먼저 확인합니다.", "여기서 목적지를 바꿔야 이후 경로 계산이 맞습니다."]` |
> 패킷 상태는 손으로 적지 않습니다. 렌더러가 `trace.steps`의 `layerOps`를 순서대로 적용해 **각 노드 시점의 계층 스택을 자동 계산**하고, 창 아래쪽에 전체 필드를 표시합니다. 이 노드에서 바뀐 필드만 강조되고, 벗겨진 계층은 별도로 알립니다. 작성자는 `layerOps`만 정확히 쓰면 됩니다.
| `detail` | string | | 상세 패널에 표시하는 설명 문단. "이 노드가 무엇이고 왜 존재하는가" |
| `mechanisms` | Mechanism[] | | 이 노드의 내부 동작(§메커니즘). 상세 패널에서 실데이터로 렌더링됨 |

**Port**: `{ "id": string, "kind": string, "label"?: string }`

### 포트 kind → 모양·색 매핑

타입을 모양으로 구분하는 방식은 Upload Labs에서 가져왔습니다. 연결(엣지)의 `kind`는 양끝 포트와 일치해야 합니다.

**정본은 [`vocabulary.json`](vocabulary.json)의 `kinds`** 입니다. 현재 4종(`packet` ■파랑 · `signal` ▲앰버 · `data` ●초록 · `error` ◆빨강)이며, 값·모양·색은 그 파일에서 확인하세요.

### 역할별 시각 (DFD·플로차트 차용)

| role | 시각 변형 |
|---|---|
| `process` (기본) | 표준 창형 노드 — 제목바 + 본문 |
| `store` | 위아래 이중 가로선(열린 박스) — DFD 데이터저장소 |
| `external` | 점선 테두리 — 시스템 경계 밖 개체 |
| `decision` | 제목바에 ◇ 마크 — 분기점. out 포트 2개 이상 권장 |

### 메커니즘 (Mechanism) — 노드 내부 동작

노드가 패킷/데이터에 *무엇을 하는지*를 구조화한다. 상세 패널(우측 슬라이드)에서 타입별 전용 UI로 렌더링되고, trace 스텝의 `mechanismEvent`가 "이번 통과에서 매칭/선택된 항목"을 하이라이트한다.

`Mechanism = { "type": <타입>, "title"?: string, ...타입별 데이터 }`

| type | 의미 | 데이터 형태 | 패널 렌더 | 실전 예 |
|---|---|---|---|---|
| `table-lookup` | 테이블에서 규칙 매칭 | `rows: [{id, cells: [string], note?}]`, `columns?: [string]` | 표 + 매칭 행 하이라이트 | 라우팅 테이블, iptables 체인, ARP, conntrack |
| `weighted-select` | 가중치/확률 선택 | `candidates: [{id, label, weight}]` | 후보 + 가중치 바 + 선택 표시 | KUBE-SERVICES 확률 매칭, ECMP, LB |
| `rewrite` | 헤더 필드 재작성 | `changes: [{layer, field, from, to}]` | before → after 목록 | DNAT/SNAT, TTL 감소 |
| `crypt` | 암호화/복호화 | `mode: "encrypt"\|"decrypt"`, `cipher?`, `note?`, `layers?: [layerId]` | 잠기는/풀리는 계층 + 암호군 | TLS, IPsec |
| `k8s-resolve` | K8s 리소스 매핑 | `lines: [{id?, text, indent?}]` | kubectl describe 풍 모노스페이스 블록 + 선택 행 하이라이트 | Service→EndpointSlice→Pod, CoreDNS, label selector |
| `encap` / `decap` | 계층 씌우기/벗기기 | `layer: {id, name, fields}` | (v0.2 일반 렌더) | VXLAN, IPIP |
| `filter` | 통과/차단 판정 | `rules: [{id, text, verdict}]` | (v0.2 일반 렌더) | 방화벽, NetworkPolicy |
| `queue` | 버퍼링 | (state.queue 재사용) | 큐 게이지 | 소켓 큐, qdisc |

전용 렌더 구현은 v0.2 기준 5종(`table-lookup`·`weighted-select`·`rewrite`·`crypt`·`k8s-resolve`)이고, 나머지는 키-값 일반 렌더로 표시된다. 한 노드에 여러 메커니즘을 배열로 나열할 수 있다 (예: KUBE-SERVICES = k8s-resolve + weighted-select + rewrite).

### 레인 — 왕복과 행위 주체

한 방향으로만 흐르지 않는 흐름이 있습니다. TLS 핸드셰이크는 두 당사자가 메시지를 주고받고, `write()` 시스템 콜은 커널로 내려갔다가 **성공을 먼저 돌려주고** 디스크 기록은 뒤늦게 이어집니다. 이런 흐름을 한 줄로 그리면 "여러 단계를 순서대로 거친다"로 잘못 읽히고, 무엇보다 **누가 하는 일인지가 사라집니다**.

`meta.lanes`로 행위 주체를 선언하고 노드마다 `lane`을 달면 교차축이 주체별로 고정됩니다. UML 시퀀스 다이어그램과 같은 읽기 방식입니다.

```json
"meta": {
  "direction": "LR",
  "lanes": [ { "id": "client", "label": "CLIENT" }, { "id": "server", "label": "SERVER" } ]
},
"nodes": [ { "id": "server-hello", "lane": "server", ... } ]
```

- 흐름축(`rank`)은 그대로 **시간**을 나타내고, 교차축이 **주체**가 됩니다
- 레인을 가로지르는 엣지가 곧 왕복입니다. 화살표로 방향이 드러납니다
- `meta.lanes`가 없으면 배치는 종전과 완전히 같습니다. 한 방향 흐름(K8s 패킷 등)에는 쓰지 않습니다

### 연결 제약

노드가 몇 개까지 연결될 수 있는지, 어떤 조합이 자연스러운지는 [`vocabulary.json`](vocabulary.json)의 `connectionRules`가 정의합니다. 규칙은 두 등급입니다.

- **`error`** — 어기면 흐름도가 성립하지 않습니다. 빌드가 실패하고, Phase B 에디터에서는 드롭 자체가 거부됩니다.
- **`warn`** — 대개 맞지만 예외가 있는 도메인 관습입니다. 메시지만 남기고 빌드는 통과하며, 에디터에서는 경고 배지가 됩니다.

전부 막지 않는 이유는 캡슐화·양방향 통신처럼 정당한 예외가 있기 때문입니다. 배경과 사례는 [VOCABULARY.md](../VOCABULARY.md)에 있습니다.

### 그룹과 접기

- `type: "group"` 노드는 자식들을 감싸는 컨테이너로 그려진다. 제목바 클릭으로 접기/펼치기 토글.
- 접힌 그룹은 단일 노드 크기로 축약되고, 내부로 드나들던 엣지는 그룹 **경계 포트**로 흡수된다 (원래 kind의 모양·색 유지).
- 데이터에는 원래 endpoint가 그대로 남는다 — 렌더러가 "유효 endpoint"(가장 바깥 접힌 조상)를 계산해 그린다.
- 순환 parentId는 금지. 렌더러가 로드 시 검증하고 에러를 표시한다.

## edges

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `id` | string | ✅ | 고유 식별자 |
| `source` / `target` | string | ✅ | 노드 id (그룹도 가능) |
| `sourcePort` / `targetPort` | string | | 포트 id. 생략 시 kind가 맞는 첫 포트에 연결 |
| `kind` | string | ✅ | 포트 kind와 동일 어휘. 엣지 색·입자 모양 결정 |
| `label` | string | | 엣지 서술 (C4식 — "무엇이 왜 흐르는가"). **v0.3부터 캔버스에 그리지 않고 패널(엣지 클릭·연결 섹션)에서만 표시** — Upload Labs처럼 선 위에는 글이 없다 |
| `decoration` | `"one-to-one"` \| `"one-to-many"` \| `"optional"` | | ERD식 끝단 기호. one-to-many는 target 끝에 까치발(crow's foot), optional은 source 끝에 ○ (기호는 캔버스 유지) |
| `ratio` | string | | 분기 비율 (예: `"2:1"`). v0.3부터 패널 전용 — 분기 노드의 연결 섹션과 엣지 패널에서 표시 |

## trace (mode: "trace")

개체 하나가 노드를 순서대로 지나가는 것을 애니메이션한다. UML 시퀀스의 순번 메시지 + 활성 구간 문법을 차용한다.

```json
{
  "entity": {
    "kind": "packet", "label": "HTTP GET 요청",
    "layers": [
      { "id": "eth",  "name": "Ethernet", "fields": { "src": "aa:bb:..", "dst": "cc:dd:.." } },
      { "id": "ip",   "name": "IP",       "fields": { "src": "203.0.113.7", "dst": "192.168.10.11" } },
      { "id": "tcp",  "name": "TCP",      "fields": { "sport": "51344", "dport": "30080" } },
      { "id": "http", "name": "HTTP",     "fields": { "req": "GET /" } }
    ]
  },
  "steps": [
    { "at": "eth0", "narration": "NIC이 프레임을 수신해 링 버퍼에 넣는다", "stateChanges": { "eth0": { "queue": 3 } } },
    { "at": "kube-svc", "via": "e2", "narration": "DNAT — 목적지가 Pod IP로 바뀐다",
      "layerOps": [
        { "op": "set", "layer": "ip",  "field": "dst",   "value": "10.244.1.5" },
        { "op": "set", "layer": "tcp", "field": "dport", "value": "8080" }
      ],
      "mechanismEvent": { "select": ["sep-a", "r-dnat"] } }
  ]
}
```

### entity.layers — 패킷 계층 스택

패킷을 **계층의 순서 목록**으로 모델링한다 (배열 앞 = 바깥 계층). 패킷 인스펙터(하단 상시 영역)에 스택으로 표시되고, `layerOps`가 일어난 필드는 diff 하이라이트된다. `layers`를 생략하면 인스펙터가 숨고 v0.1처럼 라벨만 표시된다.

### steps[].layerOps — 패킷 변형 연산

| op | 형태 | 의미 |
|---|---|---|
| `set` | `{op, layer, field, value}` | 필드 재작성 (DNAT, TTL 감소). 인스펙터에 이전값→새값 diff |
| `push` | `{op, layer: {id,name,fields}}` | 바깥에 계층 씌우기 (VXLAN 캡슐화) |
| `pop` | `{op, layer: <id>}` | 계층 벗기기 (디캡슐화) |
| `lock` | `{op, layer: <id>, note?}` | 계층 암호화 표시 — 🔒 잠기고 필드가 가려짐 (TLS) |
| `unlock` | `{op, layer: <id>}` | 복호화 — 잠금 해제 |

### steps[].mechanismEvent — 메커니즘 하이라이트

`{ "select": [<id>...] }` — 이 스텝의 `at` 노드가 가진 메커니즘들에서, 이번 통과에 매칭/선택된 행·후보·라인의 id 목록. 상세 패널에서 해당 항목이 빛난다. 노드를 나중에 클릭해도 "패킷이 지나갈 때 무엇이 선택됐는지"가 남아 보인다 (가장 최근 통과 기준).

| 필드 | 의미 |
|---|---|
| `entity.kind` | 이동 개체의 모양·색 (포트 kind 어휘) |
| `entity.label` | 추적 대상의 이름 (패널 표시용) |
| `steps[].at` | 이 스텝에서 패킷이 위치한 노드 id. 이 노드의 창에 해당 시점의 계층 상태가 표시됩니다 |
| `steps[].via` | 직전 스텝에서 이 노드로 올 때 탄 엣지 id. 생략 시 두 노드를 잇는 첫 엣지를 자동으로 찾습니다 |
| `steps[].narration` | 패널의 "여기서 일어나는 일" 문단 |
| `steps[].layerOps` | 패킷 계층 변형 연산 목록 (§steps[].layerOps). **노드 창의 계층 스택이 이 값으로 자동 계산됩니다** |
| `steps[].mechanismEvent` | at 노드 메커니즘의 매칭/선택 하이라이트 (§steps[].mechanismEvent) |

같은 노드가 여러 스텝에 등장하면 패널의 "여기서 일어나는 일"에 문단이 순서대로 쌓이고, 노드 창의 계층 상태는 **마지막으로 그 노드를 지난 시점**을 보여줍니다.

## stream (mode: "stream") — 스키마만 정의

tick 엔진을 이후에 붙일 수 있도록 자리를 확보합니다. 현재 렌더러는 이 블록이 있어도 상시 입자(ambient)의 밀도에만 반영합니다.

```json
{
  "rates":      { "edge-id": 2.0 },
  "capacities": { "node-id": 10 }
}
```

- `rates`: 엣지별 초당 개체 수 (입자 밀도에 반영)
- `capacities`: 노드별 처리 용량 (tick 엔진 확장 자리)

## 렌더러 UX — 클릭 탐색 모델

**재생도 순번도 없습니다.** 캔버스는 Upload Labs처럼 항상 살아서 돌아가고(엣지마다 상시 입자가 흐릅니다), 사용자는 궁금한 구간을 클릭해 들여다봅니다. 순서는 좌→우 배치 자체가 알려주므로 번호를 따로 붙이지 않습니다.

- **노드 창 3단 구성**: `info` 설명 문장 → 메커니즘 배지(≡ 테이블 매칭 · % 가중치 선택 · ⇄ 헤더 재작성 · 🔐 암복호화 · ⎈ K8s 매핑 · ⊞ 캡슐화 · ⊟ 디캡슐화 · ⊘ 필터 · ▤ 큐) → **패킷 계층 스택**. 클릭하지 않아도 여기까지만 읽으면 흐름이 통해야 합니다 (제1원칙 6항).
- **패킷 계층 스택**: 그 노드를 지난 뒤의 상태를 계층별 전체 필드로 보여줍니다. 이 노드에서 바뀐 필드는 강조되고, 벗겨진 계층은 "… 헤더는 여기서 벗겨졌습니다"로 알립니다. 잠긴 계층은 필드 대신 암호화 표시가 나옵니다.
- **노드 클릭 → 상세 패널** (우측 슬라이드, ✕/Esc 닫기). 섹션 구성:
  1. 개요 — icon·type·role·`detail`
  2. 여기서 일어나는 일 — 이 노드의 스텝 `narration`(복수 스텝이면 전부)
  3. 패킷 변형 — **들어올 때와 나갈 때를 2열로 대조**(n8n 차용). 양쪽 전체 계층을 싣되 달라진 줄만 강조하고, 벗겨진 계층은 왼쪽에 취소선, 씌워진 계층은 오른쪽에 초록으로 표시합니다. 무엇이 안 바뀌었는지도 보여야 비교가 성립하기 때문입니다. 이어서 "무엇이 바뀌었나"에 변경분 목록을 요약합니다
  4. 내부 동작 — `mechanisms` (이 노드 스텝의 `mechanismEvent` 선택 항목 상시 하이라이트)
  5. 연결 — in/out 엣지 목록 (kind·`label`·`ratio`·상대 노드, 클릭하면 그 노드 패널로 점프)
- **엣지 클릭 → 엣지 패널**: 무엇이 흐르는가(kind)·`label`·`ratio`·decoration 의미·양끝 노드(클릭 점프).
- **캔버스에는 글이 없다**: 엣지 라벨·비율 텍스트를 그리지 않는다. 서술은 전부 패널.
- **남는 조작**: 우하단 플로팅 — 입자 토글·속도. 드래그 팬(5px 이동 후 시작 — 클릭과 구분)·휠 줌·더블클릭 리셋.

## 상시 애니메이션

캔버스는 정지화면이 아니다 — 모든 엣지에 낮은 밀도의 ambient 입자가 항상 흐르고(Upload Labs의 "살아있는 화면"), 주인공 패킷이 경로를 돈다. `prefers-reduced-motion`에서는 ambient·주인공 이동을 끄고 경로 하이라이트로 대체한다.

---

## 최소 예시

```json
{
  "meta": { "title": "예시", "mode": "trace", "direction": "LR" },
  "nodes": [
    { "id": "a", "label": "송신", "type": "process" },
    { "id": "g", "label": "커널", "type": "group" },
    { "id": "b", "parentId": "g", "label": "수신", "type": "process" }
  ],
  "edges": [
    { "id": "e1", "source": "a", "target": "b", "kind": "packet" }
  ],
  "trace": {
    "entity": { "kind": "packet", "label": "패킷" },
    "steps": [
      { "at": "a", "narration": "출발" },
      { "at": "b", "via": "e1", "narration": "도착" }
    ]
  }
}
```
