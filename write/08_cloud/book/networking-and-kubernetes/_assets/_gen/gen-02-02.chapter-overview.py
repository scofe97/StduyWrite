# 02-02.chapter-overview — 네 단계 흐름 (구조 → 규칙 → 실전 → 대안)
# 본문 요구: 세 기술로 가는 길을 절 순서로 잇는다
# 타입 스펙: type-data-flow.md §2 격자 — 단계 머리를 세우고 그 아래 한 칸씩.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 544
d = D(W, H, "02-02 · CHAPTER MAP",
      "kube-proxy 를 이해하는 세 기술 전체 지도",
      "구조를 알고 규칙 한 줄을 읽으면 확률 분배가 보이고, 그 한계에서 IPVS·eBPF 가 나온다.",
      lead="구조 → 규칙 → 확률 분배 → 그 한계에서 나온 대안")

BW, BH, GAP = 190, 116, 56
CX = [36 + BW // 2 + i * (BW + GAP) for i in range(4)]           # 131 377 623 869
CY = 316
STAGES = ["§1 구조", "§2 규칙", "§3 실전", "§4·§5 대안"]
NODES = [("테이블·체인", "nat · PREROUTING", "KUBE-SERVICES 로", None),
         ("매치·타깃", "조건은 안 바꾼다", "바꾸는 건 -j 하나", None),
         ("확률 분배", "0.333 · 0.5 · 무조건", "mark 0x4000 · DNAT", ACC),
         ("IPVS·eBPF", "해시 표 · 커널 맵", "16만 규칙 = 5시간", INFO)]
EDGE = ["그 안에", "쌓으면", "한계에서"]

ddx.band(d, 104, 496, "규칙 한 줄을 읽을 줄 알면 나머지는 그것이 쌓인 결과다")
for cx, s in zip(CX, STAGES):
    d.t(cx, 216, s, 12, SOFT, KR, "middle", 600)
for cx, (l, sub, tag, c) in zip(CX, NODES):
    x, y = cx - BW // 2, CY - BH // 2
    if c is ACC:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, CY - 24, ddx.fit(l, 14, BW - 18, l), 14, tc, KR, "middle", 600)
    d.t(cx, CY + 2, ddx.fit(sub, 11, BW - 16, sub), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in sub) else KR)
    d.t(cx, CY + 30, ddx.fit(tag, 10, BW - 14, tag), 10, SOFT,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in tag) else KR)
for i, lab in enumerate(EDGE):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.path(f"M {a+6} {CY} L {b-10} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 16, ddx.fit(lab, 11, GAP - 6, f"corridor {lab}"), 11, MUTED, KR)

d.t(36, 468, "확률 분배가 이 편의 한가운데다 — 앞의 둘은 그것을 읽기 위한 준비이고, "
             "뒤의 둘은 그것이 커진 뒤의 이야기다", 12, MUTED, KR, "start")
d.legend(512, [("이 편의 한가운데", ACC), ("한계에서 나온 대안", INFO)])
d.save("02-02.chapter-overview.svg")
print("ok 02-02.chapter-overview")
