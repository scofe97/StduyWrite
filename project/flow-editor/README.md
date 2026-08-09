# flow-editor

Upload Labs 스타일의 "살아있는 흐름도" 에디터. 네트워크 통신·리눅스 내부·코드 흐름을 창형 노드 + 모양 포트 + 흐르는 입자로 표현한다. 사용자가 흐름을 요청하면 Claude가 JSON DSL을 작성하고, 렌더러가 애니메이션 캔버스로 그린다.

> **제1원칙 — 시각화를 통한 이해.** 이 프로젝트의 목적은 흐름도를 그리는 것이 아니라 흐름도로 이론을 이해시키는 것이다. 그림이 예쁜지가 아니라 **읽고 이해되는지**로 모든 판단을 내린다. 문장 작성 규칙 6개는 [`schema/flow-schema.md`](schema/flow-schema.md) 최상단이 정본이며, 흐름도를 만들기 전에 반드시 읽는다.

현재는 Phase A(선언형 DSL + 렌더러)이며, 최종 목표는 드래그 GUI 편집기(Phase B)다. 그래서 저장 구조를 React Flow 호환 `parentId` 평면 구조로 고정해 뒀다.

## 새 흐름도 만드는 절차 (Claude용)

1. `schema/flow-schema.md`를 읽는다 — **제1원칙과 문장 작성 규칙**, 필드 의미, 렌더링 규칙의 정본.
2. `examples/src/<이름>.json` 작성. 네트워크 흐름이면 `examples/src/k8s-packet-flow.json`이 참고 원형이다 — 계층 스택(`entity.layers`), DNAT 변형(`layerOps`), 메커니즘(`mechanisms` + `mechanismEvent`), 큐 병목(`stateChanges`), 접힌 그룹, 아이콘을 모두 사용한다.
3. 빌드: `go run tools/build.go examples/src/<이름>.json` → `examples/<이름>.html` 생성. 검증 실패 시 메시지의 필드를 고친다.
4. 브라우저로 열어 확인 (file:// 직접 열기 가능, 서버 불필요).

## 디렉토리

| 경로 | 역할 |
|---|---|
| `schema/flow-schema.md` | **DSL 명세 정본** — 제1원칙·문장 규칙 6개·필드 의미·렌더러 UX 계약 |
| `schema/flow.schema.json` | JSON Schema (외부 도구용 — 빌더는 자체 검증 내장) |
| `renderer/template.html` | HTML 골격. 마커 3곳에 빌드 시 인라인됨 |
| `renderer/flow-style.css` | 스타일 (팔레트·패널·계층 스택·메커니즘 UI) |
| `renderer/flow-renderer.js` | 렌더러 로직 (레이아웃·입자·패널·계층 자동 계산) |
| `examples/src/*.json` | 흐름도 원본 데이터 — K8s 패킷 · TLS 핸드셰이크 · 리눅스 write() |
| `examples/*.html` | 빌드 산출물 (자체 완결 1파일 — 소스 3개+데이터 인라인) |
| `tools/build.go` | 검증 + 인라인 빌더 (Go stdlib만, `go run`으로 실행) |
| `REFERENCES.md` | 참고 프로젝트별 차용 요소와 Phase B~ 결정 메모 |

소스는 분리돼 있지만 **산출물은 단일 자체완결 HTML**이다 — 파일 하나만 복사해도 열린다.

## 예시

| 흐름도 | 무엇을 보여주나 | 처음 쓰인 기능 |
|---|---|---|
| `k8s-packet-flow` | 외부 요청이 NodePort로 들어와 iptables DNAT를 거쳐 Pod 소켓에 닿기까지 | 접기/펼치기 그룹, 확률 분기, 계층 pop |
| `tls-handshake` | 평문 대화가 열쇠 교환 뒤 암호문으로 바뀌기까지 | `crypt` 메커니즘, `layerOps`의 `lock` |
| `linux-syscall-write` | 앱의 write() 한 줄이 유저 공간에서 디스크까지 내려가는 길 | `direction: "TB"` 상하 배치, `filter` 메커니즘 |

## 표현 문법 요약

- **노드** = 창형 UI (아이콘 + 제목바 + 보조설명 + 큐 게이지). `role` 시각 변형: `store`(이중선) `external`(점선) `decision`(◇). `icon` 생략 시 role 기본 이모지
- **포트** = 모양+색 타입: ■packet(파랑) ▲signal(앰버) ●data(초록) ◆error(빨강)
- **엣지** = 베지어 + `label`(서술) + `decoration`(ERD식 1:1/1:N/optional) + `ratio`(분기 비율)
- **그룹** = 접기/펼치기 컨테이너, 깊이 무제한. 접으면 엣지가 경계 포트로 흡수
- **노드 창 3단** = `info` 설명 문장 → 메커니즘 배지(≡ % ⇄ 🔐 ⎈) → **패킷 계층 스택**. **클릭 없이 여기까지만 읽어도 흐름이 통해야 한다**
- **패킷 계층 스택** = 각 노드에 그 시점의 `[Ethernet][IP][TCP][HTTP]` 전체 필드를 표시. 작성자가 손으로 적지 않고 `layerOps`(set/push/pop/lock/unlock)에서 **자동 계산**된다. 그 노드에서 바뀐 필드만 강조되고, 벗겨진 계층은 따로 알린다
- **메커니즘** = 노드 내부 동작 8타입 (`table-lookup` `weighted-select` `rewrite` `crypt` `k8s-resolve` `encap` `decap` `filter` `queue`). 패널에서 실데이터 렌더 + `mechanismEvent` 매칭 항목 하이라이트
- **클릭 탐색** = 재생도 순번도 없음. 순서는 좌→우(또는 위→아래) 배치가 알려준다. 노드/엣지/그룹 클릭 → 우측 패널(520px). 캔버스 엣지에는 텍스트 없음 — 서술은 전부 패널
- **패널 IN/OUT 대조** = [패킷 변형] 섹션이 **들어올 때와 나갈 때를 2열로** 놓고 바뀐 줄만 강조한다(n8n 차용). 벗겨진 계층은 왼쪽에 취소선, 씌워진 계층은 오른쪽에 초록. 무엇이 *안* 바뀌었는지도 보여야 비교가 성립하므로 양쪽 전체를 싣는다
- **아이콘** = 컬러 이모지 대신 절제된 기하 기호(▣ ▤ ◇ ◈ ⎈ ⇌ ⊣ ⊹). 플랫폼마다 모양이 달라지지 않고 기술 문서 톤에 맞는다

## 조작

노드·엣지·그룹 클릭 상세 · Esc/✕/빈 캔버스 클릭으로 패널 닫기 · 드래그 팬(5px 이동부터) · 휠 줌 · 더블클릭/0 화면 리셋 · 그룹 제목 클릭 접기 · 우하단 플로팅: 흐름 입자 토글·속도(+−). `prefers-reduced-motion` 환경에서는 애니메이션 자동 꺼짐.

## 알려진 한계 (v0.5)

- stream 모드 애니메이션 미완 (스키마 + ambient 입자만 — Kiali 매핑은 REFERENCES.md)
- `encap`/`decap`/`filter` 메커니즘은 일반 키-값 렌더 (VXLAN·NetworkPolicy 예시 만들 때 전용 렌더 예정)
- 노드 폭이 268px 고정이라 흐름이 길면 화면을 넘어감 — 최소 가독 배율(1.0×)을 지키고 나머지는 팬으로 본다
- `direction: "TB"` 세로 흐름은 노드가 이미 높아 전체 높이가 길어짐(리눅스 예시 1731px). 간격을 `GAP_RANK_TB`로 줄였지만 한 화면에 다 넣으려면 글씨가 안 읽히므로, 가독 배율을 지키고 팬으로 본다
- 계층 필드가 많으면 노드가 세로로 길어짐. 필드는 학습에 필요한 것만 골라 쓴다
- 백그라운드(가려진) 탭에서는 Chrome이 rAF를 스로틀해 입자가 느려짐 — 탭을 화면에 띄우면 정상
- Phase B(드래그 GUI) 미구현 — 노드 위치는 자동 레이아웃만
