# -*- coding: utf-8 -*-
# 타입 스펙: type-layers
"""kubeconfig·여러 클러스터 접근 §2 도식 — 설정 파일 탐색 순서와 다중 파일 병합 규칙.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
타입은 type-layers: 5개 층, 층 높이 64px, 폭 840px in 1000px viewBox,
인덱스 태그 mono, 층 이름 15px, focal 은 S4 한 층에만.
"""
import pathlib

TITLE    = "설정 파일 탐색 순서와 병합 규칙"
SUBTITLE = "CLI 플래그에서 기본 파일까지의 우선순위와 First-wins 충돌 해결"
EYEBROW  = "FLAG -> ENV VAR -> DEFAULT FILE -> FIRST-WINS -> RUNTIME OVERRIDE"

LAYERS = [
    ("S1", "--kubeconfig 플래그",       "최우선 단일 파일 지정 · 병합 없이 해당 파일만 로드",         "2절"),
    ("S2", "KUBECONFIG 환경 변수",       "콜론 구분 파일 목록 순회 · 앞 파일부터 순서대로 병합",       "2절"),
    ("S3", "~/.kube/config 기본 파일",   "플래그·환경 변수가 없을 때 · 병합 없이 이 파일만 로드",            "2절"),
    ("S4", "First-wins 충돌 해결",       "S2 목록을 합칠 때만 적용 · 먼저 설정한 파일의 값 유지",    "2절"),
    ("S5", "런타임 플래그 오버라이드",   "--context · --cluster · --user · --namespace 덮어쓰기",      "2절"),
]
FOCAL = 3   # S4 — 이 문서의 핵심 병합 규칙

VB_W = 1000
STACK_X, STACK_W = 120, 840
STACK_Y0, LAYER_H = 132, 64
n = len(LAYERS)
layer_y = lambda k: STACK_Y0 + k * LAYER_H
stack_bottom = layer_y(n - 1) + LAYER_H
NOTE_Y = stack_bottom + 32
VB_H = NOTE_Y + 24

for v in (VB_W, VB_H, STACK_X, STACK_W, STACK_Y0, LAYER_H, stack_bottom, NOTE_Y):
    assert v % 4 == 0, f"4의 배수가 아님: {v}"
assert 4 <= n <= 6 and 56 <= LAYER_H <= 72 and 800 <= STACK_W <= 880

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}" role="img" aria-labelledby="t1 d1">')
o.append('<title id="t1">설정 파일 탐색 순서와 병합 규칙</title>')
o.append('<desc id="d1">kubectl 이 설정 파일을 찾는 세 단계 우선순위와 다중 파일 병합 시 첫 번째 파일이 이기는 규칙, 그리고 런타임 플래그 오버라이드를 위에서 아래로 쌓은 계층 도식입니다. 앞의 세 단은 먼저 걸린 하나만 쓰이며, 강조한 네 번째 단 First-wins 는 KUBECONFIG 목록을 합칠 때만 적용됩니다.</desc>')
o.append("""<style>
svg{--paper:#0D1117;--paper2:#161B22;--ink:#F5F5F3;--muted:#8B98A9;--soft:#5E6B7E;--rule:rgba(191,192,192,0.22);--accent:#F08A59;--accent12:rgba(240,138,89,0.12)}
.kr{font-family:'Geist','Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif}
.mn{font-family:'Geist Mono','Noto Sans Mono CJK KR',monospace}
.eyebrow{fill:var(--soft);font-size:9px;letter-spacing:.14em}
.h1{fill:var(--ink);font-size:20px;font-weight:600}
.sub{fill:var(--muted);font-size:12px}
.tag{fill:var(--soft);font-size:11px;letter-spacing:.08em}
.name{fill:var(--ink);font-size:15px;font-weight:600}
.note{fill:var(--muted);font-size:12px}
.sect{fill:var(--soft);font-size:11px}
.dirlab{fill:var(--soft);font-size:12px;letter-spacing:.08em}
.hair{stroke:var(--rule);stroke-width:1}
.dir{stroke:var(--soft);stroke-width:1;fill:none}
</style>""")
o.append(f'<rect width="{VB_W}" height="{VB_H}" fill="var(--paper)"/>')
o.append(f'<text class="mn eyebrow" x="{STACK_X}" y="44">{EYEBROW}</text>')
o.append(f'<text class="kr h1" x="{STACK_X}" y="76">{TITLE}</text>')
o.append(f'<text class="kr sub" x="{STACK_X}" y="98">{SUBTITLE}</text>')

# 왼쪽 여백의 방향 표시 (스택 바깥)
ax = 76
o.append(f'<path class="dir" d="M{ax} {STACK_Y0 + 8} L{ax} {stack_bottom - 16}"/>')
o.append(f'<path class="dir" d="M{ax - 5} {stack_bottom - 24} L{ax} {stack_bottom - 16} L{ax + 5} {stack_bottom - 24}"/>')
o.append(f'<text class="mn dirlab" x="{ax}" y="{STACK_Y0 - 8}" text-anchor="middle">STEP</text>')

# 층
for k, (tag, name, note, sect) in enumerate(LAYERS):
    y = layer_y(k)
    focal = (k == FOCAL)
    fill = "var(--accent12)" if focal else ("var(--paper2)" if k % 2 == 0 else "var(--paper)")
    stroke, sw = ("var(--accent)", "1.4") if focal else ("rgba(245,245,243,0.10)", "0.8")
    o.append(f'<rect x="{STACK_X}" y="{y}" width="{STACK_W}" height="{LAYER_H}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    o.append(f'<text class="mn tag" x="{STACK_X + 16}" y="{y + 38}" fill="{"var(--accent)" if focal else "var(--soft)"}">{tag}</text>')
    o.append(f'<text class="kr name" x="{STACK_X + 60}" y="{y + 32}" fill="{"var(--accent)" if focal else "var(--ink)"}">{name}</text>')
    o.append(f'<text class="kr sect" x="{STACK_X + 60}" y="{y + 50}">본문 {sect}</text>')
    o.append(f'<text class="kr note" x="{STACK_X + STACK_W - 16}" y="{y + 40}" text-anchor="end">{note}</text>')

o.append(f'<line class="hair" x1="{STACK_X}" y1="{stack_bottom + 12}" x2="{STACK_X + STACK_W}" y2="{stack_bottom + 12}"/>')
o.append(f'<text class="kr note" x="{STACK_X}" y="{NOTE_Y + 8}">S1~S3 은 먼저 걸린 하나만 쓰이고, S4 는 S2 목록을 합칠 때만 적용됩니다.</text>')
o.append("</svg>")

out = pathlib.Path(__file__).resolve().parents[1] / "kubeconfig·여러 클러스터 접근.merge-precedence.svg"
out.write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"wrote {out.name}  viewBox={VB_W}x{VB_H}")
