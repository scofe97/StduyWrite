# 02-02 §3 — USE 방법의 흐름: 자원마다 에러 → 사용률 → 포화를 묻고 다음 자원으로 돈다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리와 되돌아가는 고리.
#           원서 그림 2.12(p.32)를 가로로 폈다(dd-lint 가 비스듬한 화살표를 막으므로 노드를 한 줄에 놓고 ㄷ자로 돈다).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 928, 560
YA, YB, YC = 196, 340, 440           # 판단 줄 · 발견 줄 · 조사 줄 (중심 y)
BW, BH, DW, DH = 112, 56, 116, 76

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-02 §3",
       "자원마다 세 질문, 그리고 다음 자원",
       "자원 목록을 만든 뒤 자원 하나마다 에러·높은 사용률·포화를 차례로 묻는다. 셋 다 아니면 다음 자원으로, 하나라도 예면 그 발견을 조사한 뒤 돌아온다.",
       "원서 그림 2.12 를 가로로 편 흐름")

def box(cx, cy, l1, l2=None, c=None):
    if c: d.tone(cx - BW / 2, cy - BH / 2, BW, BH, c, 6)
    else: d.box(cx - BW / 2, cy - BH / 2, BW, BH, PAPER2, RULE, 1.0, 6)
    if l2:
        d.t(cx, cy - 4, l1, 13, INK, KR, "middle", 600); d.t(cx, cy + 15, l2, 13, INK, KR, "middle", 600)
    else:
        d.t(cx, cy + 5, l1, 13, INK, KR, "middle", 600)

def diamond(cx, cy, l1, l2, c=INFO):
    d.o.append(f'<path d="M {cx} {cy - DH / 2} L {cx + DW / 2} {cy} L {cx} {cy + DH / 2} L {cx - DW / 2} {cy} Z" '
               f'fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy - 3, l1, 13, INK, KR, "middle", 600); d.t(cx, cy + 15, l2, 13, INK, KR, "middle", 600)

XS = [84, 228, 384, 540, 696, 852]
box(XS[0], YA, "자원 목록", "만들기")
box(XS[1], YA, "자원 하나", "고르기")
diamond(XS[2], YA, "에러가", "있나?", ACC)
diamond(XS[3], YA, "사용률이", "높은가?")
diamond(XS[4], YA, "포화가", "있나?")
diamond(XS[5], YA, "모든 자원", "확인했나?", MUTED)

def harrow(x1, x2, y, lab=None):
    d.arrow([(x1, y), (x2, y)], MUTED, "ar", 1.4)
    if lab: d.t((x1 + x2) / 2, y - 8, lab, 12, SOFT, KR, "middle")

harrow(XS[0] + BW / 2, XS[1] - BW / 2 - 4, YA)
harrow(XS[1] + BW / 2, XS[2] - DW / 2 - 4, YA)
for k in (2, 3, 4):
    harrow(XS[k] + DW / 2, XS[k + 1] - DW / 2 - 4, YA, "아니오")

# 예 → 발견
fx1, fx2 = XS[2] - 60, XS[4] + 60
d.tone(fx1, YB - 24, fx2 - fx1, 48, WARN, 6)
d.t((fx1 + fx2) / 2, YB + 5, "문제 발견 — 병목 후보", 13, INK, KR, "middle", 600)
for k in (2, 3, 4):
    d.arrow([(XS[k], YA + DH / 2), (XS[k], YB - 28)], WARN, "warn", 1.4)
    d.t(XS[k] + 8, YA + DH / 2 + 22, "예", 12, WARN, KR, "start")

# 발견 → 조사 → 다음 자원으로 되돌아감
box(XS[3], YC, "다른 방법론으로", "조사")
d.arrow([(XS[3], YB + 24), (XS[3], YC - BH / 2 - 4)], WARN, "warn", 1.4)
d.arrow([(XS[3] - BW / 2, YC), (XS[1], YC), (XS[1], YA + BH / 2 + 4)], SOFT, "soft", 1.2, "4 4")
d.t(XS[1] + 8, YC - 10, "필요하면 다음 자원", 12, SOFT, KR, "start")

# 모든 자원? 아니오 → 위로 돌아 자원 하나 고르기 / 예 → 끝
ytop = YA - DH / 2 - 28
d.arrow([(XS[5], YA - DH / 2), (XS[5], ytop), (XS[1], ytop), (XS[1], YA - BH / 2 - 4)], MUTED, "ar", 1.2)
d.t((XS[1] + XS[5]) / 2, ytop - 8, "아니오 — 다음 자원", 12, SOFT, KR, "middle")
box(XS[5], YB, "끝 — 다른", "방법론으로", OK)
d.arrow([(XS[5], YA + DH / 2), (XS[5], YB - BH / 2 - 4)], OK, "ok", 1.4)
d.t(XS[5] + 8, YA + DH / 2 + 22, "예", 12, OK, KR, "start")

d.legend(YC + 52, [("가장 먼저 묻는 질문", ACC), ("문제 발견", WARN), ("모두 통과", OK)])
d.save("02-02.use-method-flow.svg")
