# 01-03.ip-ttl-hops — 홉별 감소 카운터
# 본문: "라우터는 지날 때마다 1 을 뺀다, 0 이면 그 자리에서 버린다",
#       "고리가 생겨도 무한히 도는 대신 예순몇 홉 안에 사라진다"
# 타입 스펙: type-architecture.md — 호스트와 라우터라는 실재 컴포넌트를 잇고, TTL 칩이 그 위를 흐르는 값이다. 두 밴드는 정상 전달과 경로 고리 두 경우다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 576
d = D(W, H, "IPv4 TTL · HOP COUNTDOWN",
      "TTL — 패킷이 영원히 돌지 못하게 하는 숫자",
      "라우터를 지날 때마다 1 씩 줄고, 0 이 되면 그 자리에서 버려진다",
      lead="라우터를 지날 때마다 1 씩 줄고, 0 이 되면 그 자리에서 버려진다")

# ── 격자 (stride 4) ───────────────────────────────────────
PAD, SLOT_W, NODE_W, NODE_H = 36, 232, 112, 56
CX   = [PAD + j * SLOT_W + SLOT_W // 2 for j in range(4)]      # 152 384 616 848
HALF = NODE_W // 2
ROW_A, ROW_B = (104, 276), (292, 488)
CY_A, CY_B   = 216, 388

def band(y0, y1, label):
    d.box(24, y0, 952, y1 - y0, PAPER2, RULE, 0.9, 8)
    d.t(36, y0 + 20, label, 12, SOFT, KR, "start")

def node(cx, cy, title, sub, c=None, focal=False):
    x, y = cx - HALF, cy - NODE_H // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, NODE_W, NODE_H, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 2, title, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, cy + 16, sub, 11, ACC if focal else MUTED, KR)

def hop(cx1, cx2, y, c=MUTED, mk="ar", dash=None):
    d.path(f"M {cx1+HALF+8} {y} L {cx2-HALF-10} {y}", c, 1.5, m=mk, dash=dash)

# ── ① 정상 전달 ───────────────────────────────────────────
band(*ROW_A, "정상 전달 — 홉을 지날 때마다 1 씩 줄어든다")
for j, (t, s) in enumerate([("호스트 A", "TTL 을 정한다"), ("라우터 1", "다음 홉만"),
                            ("라우터 2", "다음 홉만"), ("호스트 B", "목적지")]):
    node(CX[j], CY_A, t, s, OK if j == 3 else None)
for j, v in enumerate(["TTL 64", "TTL 63", "TTL 62"]):
    hop(CX[j], CX[j + 1], CY_A, INFO, "info")
    d.chip((CX[j] + CX[j + 1]) // 2, CY_A - 40, v, INFO, 12)

# ── ② 고리가 생기면 ───────────────────────────────────────
band(*ROW_B, "경로가 고리를 이루면 — 0 에 닿는 순간 그 자리에서 버린다")
for j, (t, s) in enumerate([("호스트 A", "TTL 64 로 출발"), ("라우터 1", "잘못된 경로"),
                            ("라우터 2", "잘못된 경로")]):
    node(CX[j], CY_B, t, s)
node(CX[3], CY_B, "TTL 0", "여기서 버린다", focal=True)

hop(CX[0], CX[1], CY_B, INFO, "info")
d.chip((CX[0] + CX[1]) // 2, CY_B - 40, "TTL 64", INFO, 12)

# 라우터 1 ⇄ 라우터 2 — 같은 두 대를 오가며 계속 준다
d.path(f"M {CX[1]+HALF+8} {CY_B-12} L {CX[2]-HALF-10} {CY_B-12}", WARN, 1.5, m="warn")
d.path(f"M {CX[2]-HALF-8} {CY_B+12} L {CX[1]+HALF+10} {CY_B+12}", WARN, 1.5, m="warn")
d.t((CX[1] + CX[2]) // 2, CY_B - 40, "63 번 오가는 동안 1 씩 준다", 12, WARN, KR, "middle", 600)

hop(CX[2], CX[3], CY_B, ACC, "acc")
d.chip((CX[2] + CX[3]) // 2, CY_B - 40, "TTL 1 → 0", ACC, 12)

# ICMP 는 되돌아오는 길이라 dashed
Y_ICMP = 452
d.path(f"M {CX[3]} {CY_B+NODE_H//2+8} L {CX[3]} {Y_ICMP} "
       f"L {CX[0]+12} {Y_ICMP}", MUTED, 1.4, m="ar", dash="6 5")
d.t(CX[0] + 24, Y_ICMP - 12, "ICMP Time Exceeded (타입 11) — 버렸다고 보낸 쪽에 알린다", 12, MUTED, KR, "start")

d.legend(508, [("TTL 값", INFO), ("고리", WARN), ("0 → 폐기", ACC)])
d.save("01-03.ip-ttl-hops.svg")
print("ok")
