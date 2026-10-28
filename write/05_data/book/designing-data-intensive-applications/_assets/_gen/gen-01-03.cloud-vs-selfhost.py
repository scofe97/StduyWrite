# 01-03 §1 — 누가 만들고 누가 운영하는가. 맞춤 제작에서 SaaS 까지 이어지는 스펙트럼.
# 옛 도식은 이 스펙트럼, 클라우드 장단점 2단 격자, 저장·연산 분리를 한 장에 모았다. 장단점 격자는 본문 §2 가,
#   저장·연산 분리는 §3 이 말로 맡는다. 여기서는 §1 의 스펙트럼만 남기고 본문 §1 자리로 옮겼다.
# 옛 도식의 「통제·투자 최대/최소」는 본문 §1 에 없는 표현이라 뺐다.
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 880
LX, LW = 16, 136
CX0, CW, CGAP = 160, 228, 8
HY, HH = 104, 56
RY0, RSTR, RH = 172, 52, 44
FOCAL = 1

cols = [("맞춤 제작", "bespoke"), ("기성품 셀프 호스팅", "기성품 소프트웨어"), ("클라우드 서비스 · SaaS", "벤더 제품")]
rows = [
    ("누가 만드는가", ["직접 작성", "오픈소스 · 상용 제품", "외부 벤더"]),
    ("누가 운영하는가", ["직접 · 사내", "직접 배포", "외부 벤더"]),
    ("접근 · 설치", ["사내 서버", "on-prem · IaaS VM", "웹 인터페이스 · API"]),
]
AXIS_Y = RY0 + 3 * RSTR + 28
LEG = AXIS_Y + 40
H = LEG + 56

d = D(W, H, "01-03 · BUILD OR BUY", "누가 만들고 누가 운영하는가",
      "맞춤 제작에서 클라우드 서비스까지 만드는 쪽과 운영하는 쪽이 사내에서 벤더로 옮겨 간다. 가운데 기성품 셀프 호스팅이 직접 배포하는 중간 지점이다.",
      "맞춤 제작에서 SaaS 까지 이어지는 연속선")

for k, (name, sub) in enumerate(cols):
    x = CX0 + k * (CW + CGAP)
    d.box(x, HY, CW, HH, PAPER2, RULE, 1.0)
    d.t(x + CW / 2, HY + 25, name, 14, INK, KR, "middle", 600)
    d.t(x + CW / 2, HY + 44, sub, 11, MUTED, MONO if sub.isascii() else KR)

for r, (label, vals) in enumerate(rows):
    y = RY0 + r * RSTR
    d.t(LX, y + 27, label, 13, MUTED, KR, "start", 600)
    for k, v in enumerate(vals):
        x = CX0 + k * (CW + CGAP)
        d.box(x, y, CW, RH, PAPER, RULE, 0.9)
        d.t(x + CW / 2, y + 27, v, 13, INK, MONO if v.isascii() else KR)

fx = CX0 + FOCAL * (CW + CGAP)
d.o.append(f'<rect x="{fx - 4}" y="{HY - 4}" width="{CW + 8}" height="{RY0 + 3 * RSTR - 8 - HY + 8}" rx="8" fill="none" stroke="{ACC}" stroke-width="1.4"/>')

x1, x2 = CX0 + CW / 2, CX0 + 2 * (CW + CGAP) + CW / 2
d.arrow([(x1, AXIS_Y), (x2 - 8, AXIS_Y)], MUTED, "ar", 1.6)
d.t(x1, AXIS_Y - 10, "직접 작성·운영", 12, MUTED, KR, "start")
d.t(x2, AXIS_Y - 10, "벤더가 구현·운영", 12, MUTED, KR, "end")

d.legend(LEG, [("가운데 지점 — 직접 배포하는 기성품", ACC)])
d.save("01-03.cloud-vs-selfhost.svg")
