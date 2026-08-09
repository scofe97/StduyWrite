# 참고 프로젝트와 차용 요소

> **정정 이력.** 이전 판에서 Upload Labs의 포트 모양 매핑을 "네모=File, 세모=Money, 원=Steam"으로 적었으나, [공식 위키 노드 페이지](https://www.upload-labs.com/en/wiki/nodes)를 직접 확인한 결과 **그런 매핑은 명시돼 있지 않습니다**. 검색 요약에서 온 미검증 정보였습니다. 위키가 확인해 주는 것은 "색 있는 점을 드래그해 연결한다"와 "출력→입력, 좌→우 흐름"까지입니다. 우리의 모양별 kind 구분(■packet ▲signal ●data ◆error)은 그 아이디어에서 출발한 **우리 설계**이지 원작 규격의 복제가 아닙니다.

flow-editor가 무엇을 어디서 가져왔고(Phase A), 무엇을 가져올 예정인지(Phase B~) 기록한다. 새 참고 자료가 생기면 여기에 추가한다.

## 게임 계열 — "살아있는 흐름"의 감각

| 프로젝트 | 차용 요소 | 반영 상태 |
|---|---|---|
| **Upload Labs** (EnigmaDev) | 창형 노드(제목바+아이콘+내부 상태) · 색 있는 점을 드래그해 연결 · 좌→우 자원 흐름 · 비율 분기(Allocator: 1입력 2출력) · Node Group · **클릭 → 우측 상세 패널** | ✅ 핵심 문법 전부 |
| **Node Factory** | 데이터가 흐르며 변형되는 노드 명명(Harvester→Tokenizer→…) | ✅ 메커니즘 타입 어휘에 영향 |
| **Factorio / Shapez 2** | 벨트 위 아이템 정체 = 병목이 즉시 보임 | ✅ 큐 게이지 + 병목 색전환 |
| **Opus Magnum / Exapunks** (Zachtronics) | 사이클 카운터 · 실행 주체가 물리적으로 이동 | ✅ trace 개체 이동 + 스텝 카운터 |
| **Mindustry** | 자원 종류별 다른 색 입자가 같은 도관을 흐름 | ✅ kind별 입자 모양·색 |
| **k8sgames.com** | 리소스 클릭 → status/YAML/describe 표시 · label selector 기반 연결선 | ✅ `k8s-resolve` describe 풍 패널 |

## 관측 도구 계열 — 실무 시각화 문법

| 프로젝트 | 차용 요소 | 반영 상태 |
|---|---|---|
| **Kiali** (Istio) | **stream 모드의 시각 스펙 그 자체**: 입자 모양=결과(원=성공, 빨간 마름모=에러 — 우리 kind 체계와 이미 일치), 입자 **밀도=요청량**, 입자 **속도=응답속도**, 엣지 색=건강도(초록/주황/빨강), 회색 엣지=유휴 | 🔜 stream 모드 구현 시 이 매핑을 그대로 채택 |
| **KubeView** | 노드 상태색 3단(초록=정상/빨강=이상/회색=미정) · K8s 객체 관계 그래프(Deployment→RS→Pod 소유 체인) · SSE 실시간 갱신 | 🔜 stream 모드 노드 `health` 필드 후보 / 실시간 연동은 Phase C 아이디어 |

## 에디터 라이브러리 계열 — Phase B(드래그 GUI) 기반

| 프로젝트 | 차용 요소 | 반영 상태 |
|---|---|---|
| **React Flow** | `parentId` 평면 구조의 서브그래프/중첩/그룹 · Drag/Resize/Connect | ✅ 저장 포맷을 이미 호환으로 설계. Phase B 기반 라이브러리 1순위 후보 |
| **React Flow** — 연결 검증 | `IsValidConnection = (edge: Edge \| Connection) => boolean` 이 드래그 중 호출돼 `false`면 연결 거부. `isConnectable`로 연결 수 제한. [예제 모음](https://medium.com/react-digital-garden/react-flow-examples-2cbb0bab4404)에서 타입 그룹별 연결 필터링(Electricity/Fire/Water끼리만), 동적 그룹핑, `getIntersectingNodes` 교차 판정, 노드 툴바 확인 | ✅ 이 API를 전제로 `vocabulary.json`에 `severity` 2단을 설계. Phase B에서 `error`→드롭 거부, `warn`→경고 배지 |
| **n8n** | **INPUT / 파라미터 / OUTPUT 3분할 패널** — 들어온 데이터와 나간 데이터를 나란히 놓고 비교 | ✅ 패널 [패킷 변형]을 2열 대조로 구현. 양쪽 전체를 싣고 달라진 줄만 강조 |
| **n8n** (미채택) | Table·JSON·Schema **뷰 전환 탭** · **paired item** 계보 추적(출력 항목이 어느 입력에서 왔는지 메타데이터로 연결, 재정렬·필터 후에도 원본까지 역추적) | 🔜 Phase B 후보. 우리 대응물은 "이 필드가 어느 노드에서 마지막으로 바뀌었나" 역추적 |
| **n8n** | **좌측 팔레트 → 캔버스 드래그 배치** UX · 노드 타입 4분류(trigger⚡/action/core/cluster) · 엣지 위 + 버튼으로 노드 삽입 | 🔜 Phase B 편집 UX의 원형 — 팔레트 항목 = 우리 메커니즘 타입 × role 조합 |
| **Rete.js / litegraph.js** | 대안 라이브러리 (Blueprint 스타일) | 참고만 |
| **Blender Geometry Nodes / UE Blueprint** | 서브그래프 경계 포트 (접힌 그룹의 엣지 흡수) | ✅ v0.1 접기/펼치기 |

## Phase B에 넘길 결정 메모

- 편집 캔버스는 React Flow 기반이 유력 — 데이터 마이그레이션 불필요(`parentId` 호환 설계 완료)
- 팔레트(n8n식)의 분류 축: role(process/store/external/decision) × mechanism 타입 × 도메인 프리셋(K8s/리눅스/TLS)
- stream 모드 시각은 Kiali 매핑(밀도=율, 속도=지연, 색=건강)을 정본으로
- 실시간 데이터 연동(KubeView SSE식)은 Phase C — "그려진 흐름도에 라이브 메트릭 흘리기"
