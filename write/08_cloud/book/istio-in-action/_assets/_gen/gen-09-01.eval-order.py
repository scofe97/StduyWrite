# 09-01 §5 정책이 평가되는 순서.
# 본문(저자 9.3.10 · 그림 9.11): CUSTOM 이 먼저, 다음 DENY, 다음 ALLOW. 아무것도 맞지 않으면
#       catch-all 유무가 결정하고, catch-all 이 없으면 ALLOW 정책의 존재 여부로 갈린다.
# 공식 레퍼런스의 다섯 단계도 같은 결론이다. 저자는 catch-all DENY 를 두면 이 흐름이 단순해진다고 적는다.
# 타입 스펙: type-flowchart — 판단 논리. 타원(시작·끝) · 마름모(판단, ≤3 출구) · 사각형(행동).
#           예는 오른쪽, 아니오는 아래, 모든 갈래에 라벨, accent 는 갈래 하나에만.
# 셋째 마름모는 "하나도 없나"로 묻는다 — 공식 순서가 "ALLOW 정책이 없으면 허용"이라 그래야
# 예=오른쪽 관례와 논리가 함께 맞는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 964
d = D(W, H, "ISTIO IN ACTION · 09-01 §5",
      "우선순위 필드 대신 액션의 종류가 순서를 정한다",
      "CUSTOM · DENY · ALLOW 순으로 보고, 아무것도 맞지 않으면 ALLOW 정책이 하나라도 있는지가 결정한다. "
      "색이 붙은 갈래가 §4 의 gotcha 이고, catch-all DENY 를 깔면 그 갈래를 만나지 않는다.",
      "catch-all 을 두면 CUSTOM · DENY 뒤에 ALLOW 하나만 챙기면 됩니다")

def oval(x, y, w, h, label):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 20)
    d.t(x + w / 2, y + h / 2 + 5, label, 13, INK, KR, "middle", 600)

def step(x, y, w, h, label, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + h / 2 + 5, label, 13, ACC if focal else INK, KR, "middle", 600)

def diamond(cx, cy, l1, l2):
    d.o.append(f'<path d="M {cx-150} {cy} L {cx} {cy-52} L {cx+150} {cy} L {cx} {cy+52} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(cx, cy - 4, l1, 12, INK, KR, "middle", 600)
    d.t(cx, cy + 16, l2, 12, INK, KR, "middle", 600)

CA, CB = 340, 830

oval(CA - 130, 116, 260, 44, "요청이 프록시에 닿는다")
diamond(CA, 240, "CUSTOM 이 맞고", "거부로 판정했나")
step(CB - 150, 212, 300, 56, "거부한다")
diamond(CA, 400, "DENY 가", "맞았나")
step(CB - 150, 372, 300, 56, "거부한다")
diamond(CA, 560, "ALLOW 정책이", "하나도 없나")
step(CB - 150, 532, 300, 56, "허용한다")
diamond(CA, 720, "그중 하나가", "맞았나")
oval(CB - 130, 698, 260, 44, "허용한다")
oval(CA - 130, 828, 260, 44, "거부한다")

d.arrow([(CA, 160), (CA, 186)], MUTED, "ar", 1.4)
d.arrow([(CA, 292), (CA, 346)], MUTED, "ar", 1.4)
d.arrow([(CA, 452), (CA, 506)], MUTED, "ar", 1.4)
d.arrow([(CA, 612), (CA, 666)], MUTED, "ar", 1.4)
d.arrow([(CA, 772), (CA, 826)], ACC, "acc", 1.5)
d.arrow([(CA + 150, 240), (CB - 152, 240)], MUTED, "ar", 1.4)
d.arrow([(CA + 150, 400), (CB - 152, 400)], MUTED, "ar", 1.4)
d.arrow([(CA + 150, 560), (CB - 152, 560)], MUTED, "ar", 1.4)
d.arrow([(CA + 150, 720), (CB - 132, 720)], MUTED, "ar", 1.4)

for y in (228, 388, 548, 708):
    d.t((CA + CB) / 2, y, "예", 12, MUTED, KR, "middle", 600)
d.t(CA + 22, 322, "아니오", 12, MUTED, KR, "start", 600)
d.t(CA + 22, 482, "아니오", 12, MUTED, KR, "start", 600)
d.t(CA + 22, 642, "아니오", 12, MUTED, KR, "start", 600)
d.t(CA + 22, 802, "아니오", 12, ACC, KR, "start", 600)

d.t(32, 900, "마지막 갈래가 §4 의 gotcha 다 — ALLOW 는 있는데 맞는 것이 없어 거부된다", 11, SOFT, KR, "start")
d.legend(920, [("허용도 거부도 적지 않은 요청이 막히는 갈래", ACC)])
d.save("09-01.eval-order.svg")
