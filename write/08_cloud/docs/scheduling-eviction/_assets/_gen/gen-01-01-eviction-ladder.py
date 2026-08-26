# -*- coding: utf-8 -*-
"""01-01 전체 요약 도식 — 압박 신호에서 파드 축출까지의 다섯 단.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
타입은 type-layers (Layout conventions): 4~6층, 층 높이 56~72px, 폭 800~880px in 1000px viewBox,
인덱스 태그 mono, 층 이름 14~16px, focal 은 한 층에만. 한글은 스타일 계약대로 12px 이상.
"""
import pathlib

TITLE    = "파드를 죽이기 전에 지울 것부터 지웁니다"
SUBTITLE = "kubelet 이 압박을 감지해 파드를 고르기까지 거치는 다섯 단"
EYEBROW  = "SIGNAL -> THRESHOLD -> CONDITION -> RECLAIM -> EVICT"

# (태그, 층 이름, 오른쪽 주석, 본문 절)
LAYERS = [
    ("S1", "축출 신호 측정",   "memory · nodefs · imagefs · containerfs · pid", "2절"),
    ("S2", "임계 비교",       "hard 는 즉시 · soft 는 유예 뒤",                "4절"),
    ("S3", "노드 컨디션 부착", "MemoryPressure · DiskPressure · PIDPressure",   "4절"),
    ("S4", "노드 레벨 회수",   "죽은 컨테이너 수거 · 안 쓰는 이미지 삭제",       "5절 · 6절"),
    ("S5", "파드 축출",       "requests 초과 · Priority · 초과 폭 순",         "5절"),
]
FOCAL = 3   # S4 — 이 문서의 논점

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
o.append('<title id="t1">압박 신호에서 파드 축출까지의 다섯 단</title>')
o.append('<desc id="d1">kubelet 이 자원 신호를 재고, 임계와 견주고, 노드 컨디션을 달고, 노드 레벨 자원을 회수한 뒤, 그래도 모자랄 때 파드를 고르는 다섯 단계를 위에서 아래로 쌓은 계층 도식입니다. 네 번째 단인 노드 레벨 회수가 강조돼 있습니다.</desc>')
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
o.append(f'<text class="kr note" x="{STACK_X}" y="{NOTE_Y + 8}">S4 가 이 문서의 논점입니다. 압박이 왔다고 파드가 곧바로 죽는 것이 아닙니다.</text>')
o.append("</svg>")

out = pathlib.Path(__file__).resolve().parents[1] / "01-01-eviction-ladder.svg"
out.write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"wrote {out.name}  viewBox={VB_W}x{VB_H}")
