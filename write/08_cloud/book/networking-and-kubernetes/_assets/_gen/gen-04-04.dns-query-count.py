# 04-04.dns-query-count — 이름 하나가 내보내는 DNS 질의 수
# 본문 요구: `## 이름 하나의 질의 횟수` 의 확인된 것 — demo-db 는 curl 5(2026-09)·getent 2(2026-11-08), github.com 은 8·8,
#           github.com. 은 2·2, demo-db.polylab.svc.cluster.local 은 8·8. curl 로 세 번 재면 demo-db 는 5·2·2, github.com 은 8·10·10 으로 흔들렸다.
# 타입 스펙: type-bar 의 dumbbell 변형 — 범주(이름)마다 같은 축 위에 두 측정(2026-09 curl · 2026-11-08 getent)의 점과 둘 사이 거리.
#           curl 세 번 범위는 가는 띠로 깐다. coral focal 은 두 도구가 갈라진 demo-db 의 getent 점 하나.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, KR, MONO

W, H = 1000, 600
X0, X1 = 380, 940
UNIT = (X1 - X0) / 10.0


def sx(v):
    return X0 + v * UNIT


d = D(W, H, "BAR · 04-04 DNS QUERIES",
      "리졸버가 다르면 같은 이름의 질의 수가 달라집니다",
      "이름 하나가 내보내는 DNS 질의 수. demo-db 는 2026-09 curl 로 5개, 2026-11-08 getent 로 2개였고 curl 을 세 번 재면 5, 2, 2 로 흔들렸다. "
      "github.com 은 두 도구 모두 8개였고 curl 은 8, 10, 10 이었다. github.com. 은 2개, demo-db.polylab.svc.cluster.local 은 8개였다.",
      lead="총 질의 수는 A 와 AAAA 를 더한 값이고 ndots:5 라서 점이 다섯 개 미만이면 검색 경로를 먼저 붙입니다")

ROWS = [
    # 이름, curl(2026-09), getent(2026-11-08), curl 세 번 범위
    ("demo-db", 5, 2, (2, 5)),
    ("github.com", 8, 8, (8, 10)),
    ("github.com.", 2, 2, None),
    ("demo-db.polylab.svc.cluster.local", 8, 8, None),
]
Y0, YS = 168, 90
AXY = Y0 + 3 * YS + 62

for v in range(0, 11):
    x = sx(v)
    d.line(x, 122, x, AXY, RULE, 0.6, "2 4")
    d.line(x, AXY, x, AXY + 6, MUTED, 1.0)
    d.t(x, AXY + 22, str(v), 12, MUTED, MONO, "middle")
d.line(X0, AXY, X1, AXY, MUTED, 1.2)
d.t(X1, AXY + 44, "총 질의 수 (A + AAAA)", 12, MUTED, KR, "end")

for i, (name, c, g, rng) in enumerate(ROWS):
    y = Y0 + i * YS
    d.t(24, y + 4, ddx.fit(name, 13, X0 - 24 - 20, name), 13, INK, MONO, "start", 600)
    d.line(X0, y, X1, y, SOFT, 0.9)
    if rng:
        lo, hi = rng
        d.tone(sx(lo), y - 6, (hi - lo) * UNIT, 12, MUTED, 5, "26", 0.8)
        d.t((sx(lo) + sx(hi)) / 2, y - 20, f"curl 세 번 {lo}~{hi}", 12, MUTED, KR, "middle")
    if c != g:
        d.line(sx(min(c, g)), y, sx(max(c, g)), y, INK, 1.6)
    focal = (c != g)
    d.o.append(f'<circle cx="{sx(c)}" cy="{y}" r="8" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>')
    gc = ACC if focal else INK
    d.o.append(f'<circle cx="{sx(g)}" cy="{y}" r="{8 if focal else 5}" fill="{gc}" stroke="{gc}" stroke-width="1.4"/>')
    if c != g:
        d.t(sx(c), y - 20, str(c), 13, MUTED, MONO, "middle", 600)
        d.t(sx(g), y + 32, str(g), 13, ACC, MONO, "middle", 600)
    else:
        d.t(sx(g), y + 32, str(g), 13, INK, MONO, "middle", 600)

d.legend(556, [("빈 점 2026-09 curl", MUTED), ("찬 점 2026-11-08 getent", INK), ("두 도구가 갈린 이름", ACC)])
d.save("04-04.dns-query-count.svg")
print("ok dns-query-count")
