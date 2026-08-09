# 참고 프로젝트와 차용 요소

flow-editor가 무엇을 어디서 가져왔고(Phase A), 무엇을 가져올 예정인지(Phase B~) 기록한다. 새 참고 자료가 생기면 여기에 추가한다.

## 게임 계열 — "살아있는 흐름"의 감각

| 프로젝트 | 차용 요소 | 반영 상태 |
|---|---|---|
| **Upload Labs** (EnigmaDev) | 창형 노드(제목바+아이콘+내부 상태) · 모양+색 포트(네모=File, 세모=Money, 원=Steam) · 좌→우 자원 흐름 · 비율 분기(Allocator) · Node Group · **클릭 → 우측 상세 패널** | ✅ v0.1~0.2 핵심 문법 전부 |
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
| **React Flow** | `parentId` 평면 구조의 서브그래프/중첩/그룹 · Drag/Resize/Connect · 연결 검증 | ✅ 저장 포맷을 이미 호환으로 설계. Phase B 기반 라이브러리 1순위 후보 |
| **n8n** | **좌측 팔레트 → 캔버스 드래그 배치** UX · 노드 타입 카탈로그(검색·분류) · 엣지 위 + 버튼으로 노드 사이 삽입 | 🔜 Phase B 편집 UX의 원형 — 팔레트 항목 = 우리 메커니즘 타입 × role 조합 |
| **Rete.js / litegraph.js** | 대안 라이브러리 (Blueprint 스타일) | 참고만 |
| **Blender Geometry Nodes / UE Blueprint** | 서브그래프 경계 포트 (접힌 그룹의 엣지 흡수) | ✅ v0.1 접기/펼치기 |

## Phase B에 넘길 결정 메모

- 편집 캔버스는 React Flow 기반이 유력 — 데이터 마이그레이션 불필요(`parentId` 호환 설계 완료)
- 팔레트(n8n식)의 분류 축: role(process/store/external/decision) × mechanism 타입 × 도메인 프리셋(K8s/리눅스/TLS)
- stream 모드 시각은 Kiali 매핑(밀도=율, 속도=지연, 색=건강)을 정본으로
- 실시간 데이터 연동(KubeView SSE식)은 Phase C — "그려진 흐름도에 라이브 메트릭 흘리기"
