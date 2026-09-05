# 01-01 §6 — CoreDNS 가 쿠버네티스 기본 DNS 가 되기까지의 연표.
# 원문 근거: Kubernetes 2015 오픈소스화 → CNCF 설립 / CoreDNS 2016 작성 / 2017 CNCF 제출 /
#            Kubernetes 1.13(2018-12) 기본 DNS / 2019-01-24 graduated.
# 2015 칸은 CNCF 설립만 둔다 — 책이 적은 "2015년 오픈소스화"는 공식문서 기준 2014년이라
# 잘못된 날짜를 도식으로 옮기지 않는다(본문 §6 원문 정오 블록이 그 차이를 적는다).
# 좌표는 연 단위 실제 간격으로 산출한다 — 마지막 두 사건이 붙어 보이는 것이 이 연표의 논지다.
# 연도만 아는 사건은 그 해의 중점에 놓는다(1월 1일로 못 박지 않는다).
# 눈금 연도 라벨은 마지막에 paper 마스크와 함께 그려, 지나가는 드롭선이 글자를 가르지 않게 한다.
# 타입 스펙: type-timeline — 사건이 시간 위에 놓이고 간격 자체가 의미를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, INFO, KR, MONO

W, H = 1000, 460
d = D(W, H, "LEARNING COREDNS · 01-01 §6",
      "포크에서 쿠버네티스 기본값까지",
      "가로축은 실제 연 간격이다. 쿠버네티스 1.13 이 CoreDNS 를 기본 DNS 로 삼은 것과 "
      "CNCF 졸업이 52일 간격으로 붙어 있는 것이 이 연표에서 눈에 들어와야 할 지점이다.",
      "마지막 두 점이 붙어 있는 것은 축소가 아니라 실제 간격입니다")

X0, SPAN, BASE = 60, 880, 244
T0, T1 = 2015.0, 2019.4
def px(t):
    return X0 + SPAN * (t - T0) / (T1 - T0)

d.line(X0, BASE, X0 + SPAN, BASE, RULE, 1.0)
for y in range(2015, 2020):
    d.line(px(y), BASE, px(y), BASE + 9, RULE, 1.0)

events = [
    (2015.5, "up",   "CNCF 설립",              "쿠버네티스를 관리하려고",     INFO, 4),
    (2016.5, "down", "Caddy 를 포크",          "Miek Gieben 이 CoreDNS 작성", INFO, 4),
    (2017.5, "up",   "CNCF 에 제출",           "월은 공식 발표에 없다",              INFO, 4),
    (2018.923, "up", "쿠버네티스 1.13 기본 DNS", "GA 로 승격",                ACC,  6),
    (2019.063, "down", "CNCF graduated",       "성숙도 최상위",               INFO, 4),
]
for t, side, name, sub, color, r in events:
    x = px(t)
    ink = ACC if color is ACC else INK
    if side == "up":
        d.line(x, BASE - r, x, BASE - 56, RULE, 1.0)
        d.t(x, BASE - 70, name, 14, ink, KR, "middle", 600)
        d.t(x, BASE - 50, sub, 13, MUTED)
    else:
        d.line(x, BASE + r, x, BASE + 64, RULE, 1.0)
        d.t(x, BASE + 82, name, 14, ink, KR, "middle", 600)
        d.t(x, BASE + 102, sub, 13, MUTED)
    d.o.append(f'<circle cx="{x}" cy="{BASE}" r="{r}" fill="{color}" stroke="{PAPER}" stroke-width="1.2"/>')

# 눈금 연도 — 드롭선 위에 마스크와 함께 얹는다
for y in range(2015, 2020):
    x = px(y)
    d.o.append(f'<rect x="{x - 22}" y="{BASE + 14}" width="44" height="18" fill="{PAPER}"/>')
    d.t(x, BASE + 28, str(y), 12, SOFT, MONO)

d.legend(392, [("설치 기반을 폭발시킨 사건", ACC)])
d.save("01-01.cncf-timeline.svg")
