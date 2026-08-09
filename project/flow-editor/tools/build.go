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

var (
	kinds       = set("packet", "signal", "data", "error")
	roles       = set("process", "store", "external", "decision")
	decorations = set("one-to-one", "one-to-many", "optional")
	mechTypes   = set("table-lookup", "weighted-select", "rewrite", "crypt", "k8s-resolve", "encap", "decap", "filter", "queue")
	layerOpKind = set("set", "push", "pop", "lock", "unlock")
)

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
			for _, line := range arr(iv) {
				if _, isStr := line.(string); !isStr {
					fail("노드 %s info 는 문자열 배열", nid)
				}
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
	fmt.Println("내장 검증: passed")
	fmt.Println("생성:", outPath)
}
