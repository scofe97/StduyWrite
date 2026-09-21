# 02-02.netfilter-hooks-flow — 훅마다 바뀌는 필드 (DNAT 가 라우팅보다 먼저인 이유)
# 본문 요구: 어느 훅에서 어느 필드가 바뀌는지 · 라우팅 이전에는 목적지를, 이후에는 출발지만
# 장면: 클러스터 밖 → NodePort 30080. 외부에서 ClusterIP 로 직접 보내는 조합은 성립하지 않아
#      (ClusterIP 는 클러스터 밖에서 라우팅되지 않는다) 2026-08-28 NodePort 로 교정했다.
# 타입 스펙: type-dp-security-matrix.md 의 값 대조 행 — 단계마다 같은 필드를 세로로 맞춰
#           '무엇이 바뀌었나'가 칸 색으로 드러나게 한다. 두 구간은 type-nested 의 경계 띠.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

# 2026-09-18 카드 여섯 사이 통로가 12px 뿐이라 한 줄이 통째로 붙어 보였다. 캔버스를 넓히면
#            본문에서 글자가 그만큼 작아지므로(스타일 계약 §캔버스 폭) 폭은 1000 에 두고,
#            카드를 138 → 108 로 줄여 48px 통로를 얻는다. 줄어든 폭에 값이 안 들어가므로
#            주소와 포트를 두 줄로 나눠 적고(같은 값, 줄만 나눔), 긴 부제 하나도 두 줄로 접는다.
# 2026-09-18 2차 — 카드 사이는 48 이 됐지만 링 테두리와 가운데 카드가 24px, src·dst 두 줄이
#            24px 로 남아 실제로 좁아 보이는 자리가 그대로였다. 폭을 더 줄이면 POST_ROUTING 이
#            안 들어가므로 열을 줄였다. 끝 칸 '패킷이 떠남' 은 src·dst 가 POST_ROUTING 과 글자
#            하나까지 같아 값 행렬에 아무것도 더하지 않는다. 다섯 열로 줄이고 카드를 128 로 잡아
#            링 안쪽 16 + 통로 48 을 확보했다. src·dst 사이도 48 로 벌린다.
W, H = 1000, 616
d = D(W, H, "NETFILTER HOOKS · WHICH FIELD CHANGES",
      "훅마다 패킷의 어느 필드가 바뀌는가 — DNAT 가 라우팅보다 먼저인 이유",
      "라우팅 이전에는 목적지를 바꿀 수 있고, 이후에는 출발지만 바뀐다. 같은 필드를 세로로 맞춰 보면 어디서 바뀌는지 드러난다.",
      lead="라우팅 이전에는 목적지를 바꿀 수 있고, 이후에는 출발지만 바뀐다")

BW, BH = 128, 92            # 11px 라벨 수용
GUTTER = 56                                                      # src·dst 행 라벨 자리 (링 밖 · 링 테두리와 16px)
# 통로는 균일하지 않다 — 링 경계가 지나는 두 자리만 '링 안쪽 16 + 통로 48' 이라 64 다.
X0, CORRIDOR = 88, [48, 64, 64, 48]
XL = [X0]
for g in CORRIDOR: XL.append(XL[-1] + BW + g)                    # 88 264 456 648 824
CX = [x + BW // 2 for x in XL]                                   # 152 328 520 712 888
NODE_CY, SRC_Y, DST_Y, CELL_H = 250, 366, 458, 44                # 세 줄 사이 통로 48px
NODES = [("요청 도착", "외부에서 도착"), ("PRE_ROUTING", "nat 에서 DNAT"),
         ("라우팅 판단", "바뀐 dst 로 조회"), ("FORWARD", "filter 판정"),
         ("POST_ROUTING", "nat 에서 MASQUERADE")]
SRC = ["203.0.113.9:51000"] * 4 + ["노드 IP:51000"]
DST = ["노드 IP:30080"] + ["10.244.1.66:8080"] * 4
CHANGED = {("dst", 1), ("src", 4)}                               # 그 칸에서 바뀐다

def split_port(v):
    """주소:포트를 두 줄로 나눈다 — 값은 그대로 두고 줄만 나눈다."""
    i = v.rfind(":")
    return (v[:i], v[i:]) if i > 0 else (v, "")

def wrap2(txt, size, avail):
    """한 줄에 안 들어가면 공백에서 두 줄로 접는다. 셋 이상은 만들지 않는다."""
    if ddx.textw(txt, size) <= avail:
        return [txt]
    parts = txt.split(" ")
    for k in range(len(parts) - 1, 0, -1):
        a, b = " ".join(parts[:k]), " ".join(parts[k:])
        if ddx.textw(a, size) <= avail and ddx.textw(b, size) <= avail:
            return [a, b]
    raise AssertionError(f"두 줄로도 안 들어감: '{txt}'")

ddx.band(d, 104, 544, "라우팅 판단 기준 · 앞은 목적지, 뒤는 출발지", x=12, w=980)
# band 가 배경 사각을 칠하므로 이 줄은 반드시 band 뒤에 그린다
d.t(36, 156, "장면 · 클러스터 밖 클라이언트 → NodePort 30080 → DNAT 뒤 Pod IP · 이 노드는 중계", 12, SOFT, KR, "start")
BTOP = 186
# 링은 감싼 카드에서 16px 떨어지고, 링 밖 가운데 카드(라우팅 판단)와는 48px 을 둔다.
# 링과 카드는 모두 띠(12~992) 안에 둔다. accent 는 '바뀌는 칸' 한 축에만 쓰므로 라우팅 이전 링은 warn 이다.
for x0, x1, lab, c in [(XL[0] - 16, XL[1] + BW + 16, "라우팅 이전 · 목적지 변경 가능", WARN),
                       (XL[3] - 16, XL[4] + BW + 16, "라우팅 이후 · 출발지만 변경", INFO)]:
    d.o.append(f'<rect x="{x0}" y="{BTOP}" width="{x1-x0}" height="{DST_Y+CELL_H//2+40-BTOP}" rx="8" '
               f'fill="{c}08" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, x0, BTOP, lab, 11, c, off=16)

for cx, (l, s) in zip(CX, NODES):
    d.box(cx - BW // 2, NODE_CY - BH // 2, BW, BH, PAPER2, RULE, 1.1, 6)
    d.t(cx, NODE_CY - 12, ddx.fit(l, 12, BW - 14, l), 12, INK,
        MONO if all(ord(ch) < 128 or ch == '_' for ch in l) else KR, "middle", 600)
    lines = wrap2(s, 11, BW - 12)
    for k, ln in enumerate(lines):
        d.t(cx, NODE_CY + (12 if len(lines) == 1 else 6 + k * 17), ln, 11, MUTED,
            MONO if all(ord(ch) < 128 or ch == '·' for ch in ln) else KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} {NODE_CY} L {b-BW//2-7} {NODE_CY}", MUTED, 1.4, m="ar")

d.t(GUTTER, SRC_Y + 4, "src", 11, SOFT, MONO, "end")
d.t(GUTTER, DST_Y + 4, "dst", 11, SOFT, MONO, "end")
for i, cx in enumerate(CX):
    for key, y, vals in (("src", SRC_Y, SRC), ("dst", DST_Y, DST)):
        hit = (key, i) in CHANGED
        c = ACC if hit else RULE
        d.o.append(f'<rect x="{cx-BW//2}" y="{y-CELL_H//2}" width="{BW}" height="{CELL_H}" rx="5" '
                   f'fill="{ACC+"14" if hit else PAPER}" stroke="{c}" stroke-width="{1.4 if hit else 1.0}"/>')
        host, port = split_port(vals[i])
        vc = ACC if hit else MUTED
        d.t(cx, y - 5, ddx.fit(host, 11, BW - 12, f"{key}{i}"), 11, vc,
            MONO if all(ord(ch) < 128 for ch in host) else KR)
        if port: d.t(cx, y + 13, port, 11, vc, MONO)
        # src 는 위, dst 는 아래에 붙인다 — 두 행이 붙어 있어 같은 쪽에 두면 겹친다
        if hit: d.t(cx, y - CELL_H // 2 - 8 if key == "src" else y + CELL_H // 2 + 16,
                    "변경 지점", 12, ACC, KR)

# DNAT 가 라우팅 판단 앞(PRE_ROUTING)에 있어야 하는 이유는 본문 산문이 맡는다
d.legend(560, [("바뀌는 자리", ACC), ("라우팅 이전", WARN), ("라우팅 이후", INFO)])
d.save("02-02.netfilter-hooks-flow.svg")
print("ok netfilter-hooks-flow")
