# 타입 스펙: type-flowchart
# 사실 출처: internal/bundle/bundle.go:421-505, docs/design.md 「Manifest」
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 670
d = D(
    W, H,
    "FLOWCHART · MANIFEST TYPE INFERENCE",
    "매니페스트 type·kind 및 진입점 결정 알고리즘",
    "flats.json의 명시적 선언을 우선하며 생략 시 번들 파일 구성에 따라 결정론적으로 타입을 추론합니다",
    "type 명시? ──No──> Markdown 문서 조건? ──No──> kind: server 선언? ──No──> index.html 확인"
)

def diamond(cx, cy, w, h, stroke=RULE, fill=PAPER2):
    pts = f"M {cx} {cy - h/2} L {cx + w/2} {cy} L {cx} {cy + h/2} L {cx - w/2} {cy} Z"
    d.o.append(f'<path d="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')

# X 중심축
AXIS_X = 280
BRANCH_X = 680

# 1. 시작 노드 (Oval)
d.box(AXIS_X - 110, 104, 220, 38, fill=PAPER2, stroke=INFO, sw=1.2, r=19)
d.t(AXIS_X, 128, "업로드 파일 묶음 수신", 12, INK, KR, "middle", 600)

d.arrow([(AXIS_X, 142), (AXIS_X, 164)], c=MUTED, m="ar", sw=1.2)

# 2. 판정 1: flats.json 에 type 있음?
diamond(AXIS_X, 204, 230, 80, stroke=RULE, fill=PAPER2)
d.t(AXIS_X, 198, "flats.json 의", 11, INK, KR, "middle", 600)
d.t(AXIS_X, 214, "type 필드 명시됨?", 11, INK, KR, "middle", 600)

# 판정 1 -> Yes (오른쪽): 명시된 type
d.arrow([(AXIS_X + 115, 204), (BRANCH_X - 110, 204)], c=INFO, m="info", sw=1.4)
d.chip((AXIS_X + 115 + BRANCH_X - 110) / 2, 192, "Yes (명시)", c=INFO, size=10)

d.box(BRANCH_X - 110, 178, 220, 52, fill=PAPER2, stroke=INFO, sw=1.0)
d.t(BRANCH_X, 199, "지정된 type 검증 및 파싱", 11, INFO, KR, "middle", 600)
d.t(BRANCH_X, 217, "flat · docs · page · design", 10, MUTED, MONO, "middle")

# 판정 1 -> No (아래): 추론 진입
d.arrow([(AXIS_X, 244), (AXIS_X, 280)], c=MUTED, m="ar", sw=1.2)
d.chip(AXIS_X + 32, 262, "No (생략)", c=MUTED, size=9)

# 3. 판정 2: type·kind 부재 & index.html·서버 entry 부재 시 Markdown 존재? (bundle.go:438-450)
diamond(AXIS_X, 320, 250, 86, stroke=RULE, fill=PAPER2)
d.t(AXIS_X, 308, "type·kind 없음", 10.5, INK, KR, "middle", 600)
d.t(AXIS_X, 321, "index.html·서버 entry 없음", 10, INK, KR, "middle", 600)
d.t(AXIS_X, 334, "Markdown 파일 존재?", 10.5, INK, KR, "middle", 600)

# 판정 2 -> Yes (오른쪽): docs
d.arrow([(AXIS_X + 125, 320), (BRANCH_X - 110, 320)], c=OK, m="ok", sw=1.4)
d.chip((AXIS_X + 125 + BRANCH_X - 110) / 2, 308, "Yes", c=OK, size=10)

d.tone(BRANCH_X - 110, 294, 220, 52, OK, 6, "14", 1.2)
d.t(BRANCH_X, 315, "type: docs (문서 플랫)", 11, OK, MONO, "middle", 600)
d.t(BRANCH_X, 333, "내장 docs 앱으로 자동 렌더링", 10, INK, KR, "middle")

# 판정 2 -> No (아래): type = flat 기본값
d.arrow([(AXIS_X, 363), (AXIS_X, 396)], c=MUTED, m="ar", sw=1.2)
d.chip(AXIS_X + 24, 378, "No", c=MUTED, size=9)

# 4. 판정 3: flats.json 에 kind: server 선언? (bundle.go:477-479)
diamond(AXIS_X, 436, 230, 80, stroke=RULE, fill=PAPER2)
d.t(AXIS_X, 430, "flats.json 에", 11, INK, KR, "middle", 600)
d.t(AXIS_X, 446, "kind: server 선언됨?", 11, INK, KR, "middle", 600)

# 판정 3 -> Yes (오른쪽): flat (server)
d.arrow([(AXIS_X + 115, 436), (BRANCH_X - 110, 436)], c=OK, m="ok", sw=1.4)
d.chip((AXIS_X + 115 + BRANCH_X - 110) / 2, 424, "Yes", c=OK, size=10)

d.tone(BRANCH_X - 110, 410, 220, 52, OK, 6, "14", 1.2)
d.t(BRANCH_X, 431, "type: flat · kind: server", 11, OK, MONO, "middle", 600)
d.t(BRANCH_X, 449, "server.js · main.wasm 구동", 10, INK, KR, "middle")

# 판정 3 -> No (아래): kind: static 기본값
d.arrow([(AXIS_X, 476), (AXIS_X, 512)], c=MUTED, m="ar", sw=1.2)
d.chip(AXIS_X + 24, 494, "No", c=MUTED, size=9)

# 5. 판정 4: 루트에 index.html 또는 static entry 존재?
diamond(AXIS_X, 552, 230, 80, stroke=RULE, fill=PAPER2)
d.t(AXIS_X, 546, "루트에 index.html", 11, INK, KR, "middle", 600)
d.t(AXIS_X, 562, "또는 static entry 존재?", 11, INK, KR, "middle", 600)

# 판정 4 -> Yes (오른쪽): flat (static)
d.arrow([(AXIS_X + 115, 552), (BRANCH_X - 110, 552)], c=ACC, m="acc", sw=1.4)
d.chip((AXIS_X + 115 + BRANCH_X - 110) / 2, 540, "Yes", c=ACC, size=10)

d.tone(BRANCH_X - 110, 526, 220, 52, ACC, 6, "14", 1.2)
d.t(BRANCH_X, 547, "type: flat · kind: static", 11, ACC, MONO, "middle", 600)
d.t(BRANCH_X, 565, "정적 웹사이트 (entry: index.html)", 10, INK, KR, "middle")

# 판정 4 -> No (바닥): 실패 노드
d.arrow([(AXIS_X, 592), (AXIS_X, 616)], c=BAD, m="bad", sw=1.2)
d.chip(AXIS_X + 24, 604, "No", c=MUTED, size=9)

d.tone(AXIS_X - 140, 618, 280, 36, BAD, 6, "14", 1.2)
d.t(AXIS_X, 640, "검증 실패: index.html 부재 (ValidationError)", 11, BAD, KR, "middle", 600)

out_path = Path(__file__).parent.parent / "01-02-type-inference.svg"
d.save(str(out_path))
print(f"Generated: {out_path}")
