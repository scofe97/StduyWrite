# -*- coding: utf-8 -*-
"""01-01 §5 도식 — 자원 메트릭 파이프라인의 두 흐름.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
타입은 type-sequence (Layout conventions): 라이프라인 5개 이하, 메시지 12개 이하,
accent 는 headline 응답 1개, return 은 점선 + 채운 화살촉. 한글은 스타일 계약대로 12px 이상.
"""
import pathlib

TITLE    = "데이터는 위로 올라오고 요청은 아래로 내려갑니다"
SUBTITLE = "metrics-server 의 수집과 kubectl top 의 조회는 서로 다른 시점에 일어나는 별개 흐름입니다"
EYEBROW  = "RESOURCE METRICS PIPELINE"

ACTORS = ["컨테이너 런타임", "kubelet", "metrics-server", "API 서버", "kubectl top · HPA"]
ASUB   = ["cgroup · CRI", "cAdvisor 내장", "메모리 보관", "집계 계층", "소비자"]

# (from, to, y, kind, label)  kind: call | ret | head
MSGS = [
    (2, 1, 224, "call", "GET /metrics/resource", True),
    (1, 0, 264, "call", "cgroup · CRI 조회", False),
    (0, 1, 304, "ret",  "컨테이너별 사용량", False),
    (1, 2, 344, "ret",  "노드 · 파드 사용량", False),
    (4, 3, 408, "call", "GET metrics.k8s.io", True),
    (3, 2, 448, "call", "집계 계층이 위임", False),
    (2, 3, 488, "ret",  "메모리 캐시에서 응답", False),
    (3, 4, 528, "head", "CPU · 메모리 사용량", False),
]
# (라이프라인, 시작 y, 끝 y)
ACTIVATIONS = [(1, 224, 344), (0, 264, 304), (3, 408, 528), (2, 448, 488)]
PHASE = [(376, "여기까지가 상시 수집입니다. 아래는 사람이 물어볼 때 일어납니다.")]

VB_W = 1000
ACTOR_W, ACTOR_GAP, ACTOR_Y, ACTOR_H = 160, 20, 128, 52
LEFT = (VB_W - (len(ACTORS) * ACTOR_W + (len(ACTORS) - 1) * ACTOR_GAP)) // 2
cx = lambda j: LEFT + j * (ACTOR_W + ACTOR_GAP) + ACTOR_W // 2
LL_TOP = ACTOR_Y + ACTOR_H
LL_BOT = 556
NOTE_Y = 588
VB_H = 612

assert len(ACTORS) <= 5, "라이프라인 5개 이하"
assert len(MSGS) <= 12, "메시지 12개 이하"
assert sum(1 for m in MSGS if m[3] == "head") <= 2, "accent 메시지는 최대 2개"
for v in (VB_W, VB_H, ACTOR_Y, ACTOR_H, LL_BOT, NOTE_Y):
    assert v % 4 == 0, f"4의 배수가 아님: {v}"
ys = sorted(m[2] for m in MSGS)
assert all(b - a >= 24 for a, b in zip(ys, ys[1:])), "메시지 간격 24px 이상"

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}" role="img" aria-labelledby="t1 d1">')
o.append('<title id="t1">자원 메트릭 파이프라인의 수집 흐름과 조회 흐름</title>')
o.append('<desc id="d1">위쪽 네 메시지는 metrics-server 가 kubelet 을 주기적으로 조회해 사용량을 메모리에 채우는 상시 수집 흐름입니다. 아래쪽 네 메시지는 사람이 kubectl top 을 쳤을 때 API 서버가 집계 계층으로 metrics-server 에 위임해 그 값을 돌려주는 조회 흐름입니다. 마지막 응답이 강조돼 있습니다.</desc>')
o.append("""<style>
svg{--paper:#0D1117;--paper2:#161B22;--ink:#F5F5F3;--muted:#8B98A9;--soft:#5E6B7E;--rule:rgba(191,192,192,0.22);--accent:#F08A59;--accent12:rgba(240,138,89,0.12)}
.kr{font-family:'Geist','Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif}
.mn{font-family:'Geist Mono','Noto Sans Mono CJK KR',monospace}
.eyebrow{fill:var(--soft);font-size:9px;letter-spacing:.14em}
.h1{fill:var(--ink);font-size:20px;font-weight:600}
.sub{fill:var(--muted);font-size:12px}
.actor{fill:var(--ink);font-size:13px;font-weight:600}
.asub{fill:var(--muted);font-size:10px}
.msg{fill:var(--muted);font-size:12px}
.msgm{fill:var(--muted);font-size:11px}
.msga{fill:var(--accent);font-size:12px;font-weight:600}
.phase{fill:var(--soft);font-size:12px}
.note{fill:var(--muted);font-size:12px}
.ll{stroke:rgba(245,245,243,0.20);stroke-width:1;stroke-dasharray:3,3}
.hair{stroke:var(--rule);stroke-width:1}
</style>""")
o.append('<defs>')
o.append('<marker id="f" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0 0 L9 3.5 L0 7 z" fill="#8B98A9"/></marker>')
o.append('<marker id="fa" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0 0 L9 3.5 L0 7 z" fill="#F08A59"/></marker>')
o.append('</defs>')
o.append(f'<rect width="{VB_W}" height="{VB_H}" fill="var(--paper)"/>')
o.append(f'<text class="mn eyebrow" x="{LEFT}" y="44">{EYEBROW}</text>')
o.append(f'<text class="kr h1" x="{LEFT}" y="76">{TITLE}</text>')
o.append(f'<text class="kr sub" x="{LEFT}" y="98">{SUBTITLE}</text>')

for j, (a, sub) in enumerate(zip(ACTORS, ASUB)):
    x = cx(j) - ACTOR_W // 2
    o.append(f'<rect x="{x}" y="{ACTOR_Y}" width="{ACTOR_W}" height="{ACTOR_H}" rx="6" fill="var(--paper2)" stroke="rgba(245,245,243,0.10)" stroke-width="0.8"/>')
    o.append(f'<text class="kr actor" x="{cx(j)}" y="{ACTOR_Y + 24}" text-anchor="middle">{a}</text>')
    o.append(f'<text class="mn asub" x="{cx(j)}" y="{ACTOR_Y + 41}" text-anchor="middle">{sub}</text>')
    o.append(f'<line class="ll" x1="{cx(j)}" y1="{LL_TOP}" x2="{cx(j)}" y2="{LL_BOT}"/>')

for j, y0, y1 in ACTIVATIONS:
    o.append(f'<rect x="{cx(j) - 4}" y="{y0}" width="8" height="{y1 - y0}" fill="rgba(245,245,243,0.06)" stroke="var(--soft)" stroke-width="0.8"/>')

for py, ptext in PHASE:
    o.append(f'<line class="hair" x1="{LEFT}" y1="{py}" x2="{VB_W - LEFT}" y2="{py}" stroke-dasharray="4,3"/>')
    o.append(f'<text class="kr phase" x="{LEFT}" y="{py + 20}">{ptext}</text>')

for src, dst, y, kind, label, mono in MSGS:
    x0, x1 = cx(src), cx(dst)
    d = 1 if x1 > x0 else -1
    sx, ex = x0 + d * 5, x1 - d * 9
    dash = ' stroke-dasharray="5,3"' if kind in ("ret", "head") else ''
    col = "var(--accent)" if kind == "head" else "var(--muted)"
    mk = "fa" if kind == "head" else "f"
    w = "1.4" if kind == "head" else "1"
    o.append(f'<path d="M{sx} {y} L{ex} {y}" stroke="{col}" stroke-width="{w}"{dash} fill="none" marker-end="url(#{mk})"/>')
    cls = "msga" if kind == "head" else ("mn msgm" if mono else "kr msg")
    o.append(f'<text class="{cls if kind != "head" else "kr " + cls}" x="{(x0 + x1) // 2}" y="{y - 8}" text-anchor="middle">{label}</text>')

o.append(f'<line class="hair" x1="{LEFT}" y1="{LL_BOT + 16}" x2="{VB_W - LEFT}" y2="{LL_BOT + 16}"/>')
o.append(f'<text class="kr note" x="{LEFT}" y="{NOTE_Y + 8}">metrics-server 는 값을 메모리에만 둡니다. 그래서 이 그림에는 과거를 되짚는 경로가 없습니다.</text>')
o.append("</svg>")

out = pathlib.Path(__file__).resolve().parents[1] / "01-01-metrics-sequence.svg"
out.write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"wrote {out.name}  viewBox={VB_W}x{VB_H}  lifelines={[cx(j) for j in range(len(ACTORS))]}")
