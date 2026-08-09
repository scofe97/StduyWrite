// Flow DSL JSON -> 자체 완결 HTML 빌더.
//
// 사용법:
//	go run tools/build.go examples/src/k8s-packet-flow.json
//	# -> examples/k8s-packet-flow.html 생성
//
// renderer/template.html 의 마커 3곳에 CSS·JS·JSON 을 인라인한다:
//	/*__FLOW_STYLE__*/     <- renderer/flow-style.css
//	/*__FLOW_RENDERER__*/  <- renderer/flow-renderer.js
//	/*__FLOW_DATA__*/null  <- 입력 JSON
//
// 주입 전 의존성 없는 구조 검증을 수행한다 (스키마 정본: schema/flow-schema.md).
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// 어휘·제약의 정본은 schema/vocabulary.json 이다. 여기서는 그 파일이 정의하지 않는
// 구조적 어휘(DSL 문법 자체에 속하는 것)만 상수로 둔다.
var (
	decorations = set("one-to-one", "one-to-many", "optional")
	layerOpKind = set("set", "push", "pop", "lock", "unlock")
)

// vocabulary.json 에서 읽어 채운다
var (
	kinds     map[string]bool
	roles     map[string]bool
	mechTypes map[string]bool
	reserved  map[string]bool
	connRules []map[string]any
)

var warnings []string

func warn(format string, a ...any) {
	warnings = append(warnings, fmt.Sprintf(format, a...))
}

// loadVocabulary 는 어휘집을 읽어 전역 집합을 채운다.
// 값을 코드에 복사해두지 않으므로 어휘를 늘릴 때 Go 를 건드릴 필요가 없다.
func loadVocabulary(base string) {
	path := filepath.Join(base, "schema", "vocabulary.json")
	raw, err := os.ReadFile(path)
	if err != nil {
		fail("어휘집을 읽을 수 없습니다: %s\n  이 파일은 role·kind·연결 제약의 정본입니다 (%v)", path, err)
	}
	var v map[string]any
	if err := json.Unmarshal(raw, &v); err != nil {
		fail("어휘집 JSON 파싱 실패: %s (%v)", path, err)
	}

	keysOf := func(key string) map[string]bool {
		m := map[string]bool{}
		for k := range obj(v[key]) {
			if k == "_" {
				continue // 설명용 키
			}
			m[k] = true
		}
		return m
	}
	kinds = keysOf("kinds")
	roles = keysOf("roles")

	mechTypes = map[string]bool{}
	for _, t := range arr(v["mechanismTypes"]) {
		if s, ok := t.(string); ok {
			mechTypes[s] = true
		}
	}
	reserved = map[string]bool{}
	for _, t := range arr(obj(v["reservedTypes"])["values"]) {
		if s, ok := t.(string); ok {
			reserved[s] = true
		}
	}
	for _, r := range arr(v["connectionRules"]) {
		if m := obj(r); m != nil {
			connRules = append(connRules, m)
		}
	}

	if len(kinds) == 0 || len(roles) == 0 {
		fail("어휘집에 kinds 또는 roles 가 비어 있습니다: %s", path)
	}
}

func set(ss ...string) map[string]bool {
	m := map[string]bool{}
	for _, s := range ss {
		m[s] = true
	}
	return m
}

func fail(format string, a ...any) {
	fmt.Fprintf(os.Stderr, "검증 실패: "+format+"\n", a...)
	os.Exit(1)
}

func str(m map[string]any, key string) string {
	s, _ := m[key].(string)
	return s
}
func obj(v any) map[string]any {
	m, _ := v.(map[string]any)
	return m
}
func arr(v any) []any {
	a, _ := v.([]any)
	return a
}

func validate(data map[string]any) {
	// --- meta ---
	meta := obj(data["meta"])
	if meta == nil {
		fail("meta 블록 필수")
	}
	if str(meta, "title") == "" {
		fail("meta.title 필수")
	}
	mode := str(meta, "mode")
	if mode != "trace" && mode != "stream" {
		fail("meta.mode 는 trace|stream: %q", mode)
	}
	if d, ok := meta["direction"]; ok {
		if ds, _ := d.(string); ds != "LR" && ds != "TB" {
			fail("meta.direction 은 LR|TB: %v", d)
		}
	}
	// 레인 — 선언 순서가 곧 화면 순서다
	laneIDs := map[string]bool{}
	for i, lv := range arr(meta["lanes"]) {
		l := obj(lv)
		id := str(l, "id")
		if id == "" {
			fail("meta.lanes[%d].id 필수", i)
		}
		if laneIDs[id] {
			fail("meta.lanes id 중복: %s", id)
		}
		laneIDs[id] = true
	}

	// --- nodes ---
	nodes := arr(data["nodes"])
	if len(nodes) == 0 {
		fail("nodes 배열 필수")
	}
	ids := map[string]map[string]any{}
	for _, nv := range nodes {
		n := obj(nv)
		nid := str(n, "id")
		if nid == "" {
			fail("노드 id 누락: %v", nv)
		}
		if _, dup := ids[nid]; dup {
			fail("노드 id 중복: %s", nid)
		}
		ids[nid] = n
		if str(n, "type") == "" {
			fail("노드 type 누락: %s", nid)
		}
		if ln := str(n, "lane"); ln != "" && !laneIDs[ln] {
			fail("노드 %s: lane %q 이 meta.lanes 에 없습니다", nid, ln)
		}
		if reserved[str(n, "type")] {
			fail("노드 %s: type %q 는 메커니즘 이름이라 노드 type 으로 쓸 수 없습니다.\n"+
				"  '노드가 무엇인가'와 '노드가 하는 일'이 헷갈립니다. 도메인 어휘(schema/vocabulary.json)를 쓰고,\n"+
				"  하는 일은 mechanisms 에 적으세요.", nid, str(n, "type"))
		}
		if str(n, "label") == "" {
			fail("노드 label 누락: %s", nid)
		}
		if r, ok := n["role"]; ok && !roles[str(n, "role")] {
			fail("노드 %s role 불명: %v", nid, r)
		}
		for _, side := range []string{"in", "out"} {
			for _, pv := range arr(obj(n["ports"])[side]) {
				p := obj(pv)
				if str(p, "id") == "" {
					fail("노드 %s %s 포트 id 누락", nid, side)
				}
				if !kinds[str(p, "kind")] {
					fail("노드 %s 포트 %s kind 불명: %v", nid, str(p, "id"), p["kind"])
				}
			}
		}
		for _, mv := range arr(n["mechanisms"]) {
			m := obj(mv)
			if !mechTypes[str(m, "type")] {
				fail("노드 %s 메커니즘 type 불명: %v", nid, m["type"])
			}
		}
		if iv, ok := n["info"]; ok {
			lines := arr(iv)
			for _, line := range lines {
				if _, isStr := line.(string); !isStr {
					fail("노드 %s info 는 문자열 배열", nid)
				}
			}
			// 노드 창은 한 줄만 — 부연은 detail 로 보낸다.
			// 창에 문장이 쌓이면 캔버스가 무거워지고 패널과 같은 말을 두 번 하게 된다.
			if len(lines) > 1 {
				fail("노드 %s: info 는 한 줄까지입니다 (현재 %d줄)\n"+
					"  노드 창은 '무엇을 하는가' 한 문장만 싣고, 왜·부연은 detail 로 옮기세요.", nid, len(lines))
			}
		}
		// 폐기된 필드를 조용히 무시하지 않고 알린다 (패킷 상태는 layerOps 로 자동 계산됨)
		for _, dead := range []string{"inOut", "state"} {
			if _, ok := n[dead]; ok {
				fail("노드 %s: %s 는 폐기된 필드입니다. 패킷 상태는 trace.steps 의 layerOps 로 자동 계산됩니다", nid, dead)
			}
		}
	}

	// parentId 참조·타입·순환 검사
	for _, nv := range nodes {
		n := obj(nv)
		if p, ok := n["parentId"]; ok && p != nil {
			ps, _ := p.(string)
			parent, exists := ids[ps]
			if !exists {
				fail("노드 %s parentId 불명: %v", str(n, "id"), p)
			}
			if str(parent, "type") != "group" {
				fail("노드 %s 의 부모 %s 는 group 타입이 아님", str(n, "id"), ps)
			}
		}
	}
	for _, nv := range nodes {
		n := obj(nv)
		seen := map[string]bool{}
		cur := n
		for {
			p, ok := cur["parentId"]
			if !ok || p == nil {
				break
			}
			cid := str(cur, "id")
			if seen[cid] {
				fail("parentId 순환: %s", str(n, "id"))
			}
			seen[cid] = true
			cur = ids[p.(string)]
		}
	}

	// --- edges ---
	edges := arr(data["edges"])
	if data["edges"] == nil {
		fail("edges 배열 필수")
	}
	eids := map[string]bool{}
	for _, ev := range edges {
		e := obj(ev)
		eid := str(e, "id")
		if eid == "" {
			fail("엣지 id 누락: %v", ev)
		}
		if eids[eid] {
			fail("엣지 id 중복: %s", eid)
		}
		eids[eid] = true
		for _, side := range []string{"source", "target"} {
			if _, ok := ids[str(e, side)]; !ok {
				fail("엣지 %s %s 불명: %v", eid, side, e[side])
			}
		}
		if !kinds[str(e, "kind")] {
			fail("엣지 %s kind 불명: %v", eid, e["kind"])
		}
		if d, ok := e["decoration"]; ok && !decorations[str(e, "decoration")] {
			fail("엣지 %s decoration 불명: %v", eid, d)
		}
		// 포트 참조 검사 (지정된 경우만, 그룹 대상은 경계 포트라 제외)
		for side, pside := range map[string]string{"source": "out", "target": "in"} {
			portKey := side + "Port"
			pid, ok := e[portKey]
			if !ok {
				continue
			}
			node := ids[str(e, side)]
			if str(node, "type") == "group" {
				continue
			}
			found := false
			for _, pv := range arr(obj(node["ports"])[pside]) {
				if str(obj(pv), "id") == pid {
					found = true
				}
			}
			if !found {
				fail("엣지 %s %s=%v 가 노드 %s 의 %s 포트에 없음", eid, portKey, pid, str(e, side), pside)
			}
		}
	}

	// --- trace ---
	if mode == "trace" {
		tr := obj(data["trace"])
		if tr == nil {
			fail("mode=trace 인데 trace 블록 없음")
		}
		ent := obj(tr["entity"])
		if !kinds[str(ent, "kind")] {
			fail("trace.entity.kind 불명: %v", ent["kind"])
		}
		layerIDs := map[string]bool{}
		for _, lv := range arr(ent["layers"]) {
			l := obj(lv)
			lid := str(l, "id")
			if lid == "" || str(l, "name") == "" {
				fail("entity.layers 항목에 id/name 필수: %v", lv)
			}
			if layerIDs[lid] {
				fail("entity.layers id 중복: %s", lid)
			}
			layerIDs[lid] = true
		}
		steps := arr(tr["steps"])
		if len(steps) == 0 {
			fail("trace.steps 는 1개 이상")
		}
		knownLayers := map[string]bool{}
		for k := range layerIDs {
			knownLayers[k] = true
		}
		for i, sv := range steps {
			s := obj(sv)
			if _, ok := ids[str(s, "at")]; !ok {
				fail("trace.steps[%d].at 불명: %v", i, s["at"])
			}
			if str(s, "narration") == "" {
				fail("trace.steps[%d].narration 누락", i)
			}
			if v, ok := s["via"]; ok && !eids[str(s, "via")] {
				fail("trace.steps[%d].via 불명: %v", i, v)
			}
			for _, dead := range []string{"stateChanges", "entityLabel"} {
				if _, ok := s[dead]; ok {
					fail("trace.steps[%d]: %s 는 폐기된 필드입니다 (큐 게이지·개체 라벨 제거됨)", i, dead)
				}
			}
			for j, ov := range arr(s["layerOps"]) {
				op := obj(ov)
				kind := str(op, "op")
				if !layerOpKind[kind] {
					fail("trace.steps[%d].layerOps[%d].op 불명: %v", i, j, op["op"])
				}
				switch kind {
				case "set":
					lid := str(op, "layer")
					if lid == "" || str(op, "field") == "" {
						fail("trace.steps[%d].layerOps[%d] set 은 layer/field/value 필수", i, j)
					}
					if _, ok := op["value"]; !ok {
						fail("trace.steps[%d].layerOps[%d] set 은 value 필수", i, j)
					}
					if !knownLayers[lid] {
						fail("trace.steps[%d].layerOps[%d] layer 불명: %s", i, j, lid)
					}
				case "push":
					l := obj(op["layer"])
					lid := str(l, "id")
					if lid == "" || str(l, "name") == "" {
						fail("trace.steps[%d].layerOps[%d] push 는 layer{id,name} 필수", i, j)
					}
					knownLayers[lid] = true
				default: // pop, lock, unlock
					lid := str(op, "layer")
					if lid == "" {
						fail("trace.steps[%d].layerOps[%d] %s 는 layer(id 문자열) 필수", i, j, kind)
					}
					if !knownLayers[lid] {
						fail("trace.steps[%d].layerOps[%d] layer 불명: %s", i, j, lid)
					}
				}
			}
			if me, ok := s["mechanismEvent"]; ok {
				for _, idv := range arr(obj(me)["select"]) {
					if _, isStr := idv.(string); !isStr {
						fail("trace.steps[%d].mechanismEvent.select 는 문자열 배열", i)
					}
				}
			}
		}
	}

	// --- stream (참조 무결성만) ---
	st := obj(data["stream"])
	for eid := range obj(st["rates"]) {
		if !eids[eid] {
			fail("stream.rates 엣지 불명: %s", eid)
		}
	}
	for nid := range obj(st["capacities"]) {
		if _, ok := ids[nid]; !ok {
			fail("stream.capacities 노드 불명: %s", nid)
		}
	}

	validateConnections(ids, edges)
}

// validateConnections 는 어휘집의 connectionRules 를 적용한다.
// severity=error 는 빌드를 멈추고, warn 은 메시지만 남기고 통과시킨다.
// 도메인 관습(캡슐화·양방향 통신 등)에는 정당한 예외가 있어 전부 막으면 도구가 목적을 방해하기 때문이다.
func validateConnections(ids map[string]map[string]any, edges []any) {
	inDeg, outDeg := map[string]int{}, map[string]int{}
	inKinds := map[string][]string{} // 노드로 들어온 엣지들의 kind
	for _, ev := range edges {
		e := obj(ev)
		s, t := str(e, "source"), str(e, "target")
		outDeg[s]++
		inDeg[t]++
		inKinds[t] = append(inKinds[t], str(e, "kind"))
	}

	report := func(sev, ruleID, msg, why string) {
		if sev == "error" {
			fail("%s\n  규칙: %s\n  %s", msg, ruleID, why)
		}
		warn("%s\n  규칙: %s (경고)\n  %s", msg, ruleID, why)
	}

	num := func(m map[string]any, key string) (int, bool) {
		f, ok := m[key].(float64)
		return int(f), ok
	}

	for _, rule := range connRules {
		sev := str(rule, "severity")
		if sev == "" {
			sev = "warn"
		}
		ruleID, why := str(rule, "id"), str(rule, "why")
		applies := obj(rule["applies"])
		wantRole := str(applies, "role")
		wantEdgeKind := str(applies, "edgeKind")
		_, anyNode := applies["any"]

		for nid, n := range ids {
			if str(n, "type") == "group" {
				continue // 그룹은 컨테이너라 연결 차수를 따지지 않는다
			}
			role := str(n, "role")
			if role == "" {
				role = "process"
			}
			// 이 규칙이 이 노드에 적용되는지
			switch {
			case wantRole != "":
				if role != wantRole {
					continue
				}
			case wantEdgeKind != "":
				// 엣지 kind 기준 규칙은 아래 notAfter 에서 따로 처리
			case anyNode:
				// 모든 노드에 적용
			default:
				continue
			}

			in, out := inDeg[nid], outDeg[nid]

			if wantEdgeKind != "" {
				// 이 kind 로 들어온 엣지가, 금지된 kind 다음에 오지는 않는지
				notAfter := map[string]bool{}
				for _, v := range arr(rule["notAfter"]) {
					if s, ok := v.(string); ok {
						notAfter[s] = true
					}
				}
				hasWanted, hasBanned := false, ""
				for _, k := range inKinds[nid] {
					if k == wantEdgeKind {
						hasWanted = true
					}
					if notAfter[k] {
						hasBanned = k
					}
				}
				if hasWanted && hasBanned != "" {
					report(sev, ruleID,
						fmt.Sprintf("노드 %s: %s 와 %s 입력이 같이 들어옵니다", nid, hasBanned, wantEdgeKind), why)
				}
				continue
			}

			// requireEither: 여러 방법 중 하나만 만족하면 통과 (분기를 갈래로 보이거나, 메커니즘으로 보이거나)
			if req := obj(rule["requireEither"]); req != nil {
				satisfied := false
				if v, ok := num(req, "minOut"); ok && out >= v {
					satisfied = true
				}
				if !satisfied {
					want := map[string]bool{}
					for _, m := range arr(req["mechanisms"]) {
						if s, ok := m.(string); ok {
							want[s] = true
						}
					}
					for _, mv := range arr(n["mechanisms"]) {
						if want[str(obj(mv), "type")] {
							satisfied = true
							break
						}
					}
				}
				if !satisfied {
					report(sev, ruleID,
						fmt.Sprintf("노드 %s(%s): 출력이 %d개이고 선택을 보여주는 메커니즘도 없습니다", nid, role, out), why)
				}
				continue
			}

			if v, ok := num(rule, "minOut"); ok && out < v {
				report(sev, ruleID, fmt.Sprintf("노드 %s(%s): 출력 연결이 %d개입니다 (최소 %d)", nid, role, out, v), why)
			}
			if v, ok := num(rule, "maxOut"); ok && out > v {
				report(sev, ruleID, fmt.Sprintf("노드 %s(%s): 출력 연결이 %d개입니다 (최대 %d)", nid, role, out, v), why)
			}
			if v, ok := num(rule, "minIn"); ok && in < v {
				report(sev, ruleID, fmt.Sprintf("노드 %s(%s): 입력 연결이 %d개입니다 (최소 %d)", nid, role, in, v), why)
			}
			if v, ok := num(rule, "maxIn"); ok && in > v {
				report(sev, ruleID, fmt.Sprintf("노드 %s(%s): 입력 연결이 %d개입니다 (최대 %d)", nid, role, in, v), why)
			}
			if v, ok := num(rule, "minDegree"); ok && in+out < v {
				report(sev, ruleID, fmt.Sprintf("노드 %s: 연결이 하나도 없습니다", nid), why)
			}
		}
	}
}

func mustRead(path string) string {
	b, err := os.ReadFile(path)
	if err != nil {
		fail("파일 읽기 실패: %s (%v)", path, err)
	}
	return string(b)
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("사용법: go run tools/build.go examples/src/<이름>.json")
		os.Exit(1)
	}
	src := os.Args[1]

	// go run 은 임시 바이너리로 실행되므로 CWD 기준으로 flow-editor 루트를 잡는다
	wd, err := os.Getwd()
	if err != nil {
		fail("작업 디렉토리 확인 실패: %v", err)
	}
	// flow-editor 루트 탐색: CWD 또는 CWD 상위에서 renderer/template.html 을 찾음
	base := wd
	for i := 0; i < 3; i++ {
		if _, err := os.Stat(filepath.Join(base, "renderer", "template.html")); err == nil {
			break
		}
		base = filepath.Dir(base)
	}
	tplPath := filepath.Join(base, "renderer", "template.html")
	cssPath := filepath.Join(base, "renderer", "flow-style.css")
	jsPath := filepath.Join(base, "renderer", "flow-renderer.js")

	raw := mustRead(src)
	var data map[string]any
	if err := json.Unmarshal([]byte(raw), &data); err != nil {
		fail("JSON 파싱 실패: %v", err)
	}
	loadVocabulary(base)
	validate(data)

	tpl := mustRead(tplPath)
	for _, marker := range []string{"/*__FLOW_STYLE__*/", "/*__FLOW_RENDERER__*/", "/*__FLOW_DATA__*/null"} {
		if !strings.Contains(tpl, marker) {
			fail("템플릿에 주입 마커 없음: %s", marker)
		}
	}

	// 원본 JSON 그대로 주입 (재직렬화하면 map 키가 알파벳순으로 바뀌어 필드 표시 순서가 깨짐)
	// + </script> 조기 종료 방지
	payload := strings.ReplaceAll(raw, "</", "<\\/")

	out := tpl
	out = strings.Replace(out, "/*__FLOW_STYLE__*/", mustRead(cssPath), 1)
	out = strings.Replace(out, "/*__FLOW_RENDERER__*/", mustRead(jsPath), 1)
	out = strings.Replace(out, "/*__FLOW_DATA__*/null", payload, 1)

	stem := strings.TrimSuffix(filepath.Base(src), filepath.Ext(src))
	outPath := filepath.Join(base, "examples", stem+".html")
	if err := os.WriteFile(outPath, []byte(out), 0o644); err != nil {
		fail("출력 쓰기 실패: %v", err)
	}
	if len(warnings) > 0 {
		fmt.Printf("경고 %d건 — 의도한 것이면 그대로 두어도 됩니다\n", len(warnings))
		for _, w := range warnings {
			fmt.Println("  · " + w)
		}
	}
	fmt.Println("내장 검증: passed")
	fmt.Println("생성:", outPath)
}
