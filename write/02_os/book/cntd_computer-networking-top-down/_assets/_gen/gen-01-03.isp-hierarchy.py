# 01-03 §3 — 원문의 네트워크 구조 5. 계층은 돈이 흐르는 방향이고, 피어링과 콘텐츠 제공자 망이 그 계층을 우회한다.
# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 으로 계층을 묶고,
#           수직 화살표는 고객→제공자(돈이 위로), 수평 점선은 정산 없는 피어링이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 980, 608
ZL, ZR = 24, 620
CX0, CW = 656, 300

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-03 §3",
      "네트워크의 네트워크 — 구조 5",
      "원문이 구조 1에서 5까지 쌓아 올린 결과. 계층은 성능이 아니라 경제와 정책이 만든 것이고, 위로 갈수록 돈을 받는다. 콘텐츠 제공자는 자기 망을 지어 그 계층을 건너뛴다.",
      "원문의 표현대로 이 진화의 상당 부분은 성능이 아니라 경제와 국가 정책이 이끌었습니다")

d.box(ZL, 100, ZR - ZL, 396, PAPER2, RULE, 0.8, 8)
d.t(ZL + 14, 120, "ISP 계층", 11, SOFT, KR, "start", 600)

def unit(x, y, w, h, name, sub, c=None):
    if c: d.tone(x, y, w, h, c, 6)
    else: d.box(x, y, w, h, PAPER, RULE, 1.0, 6)
    d.t(x + w / 2, y + 26, name, 12, c if c else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 45, sub, 11, MUTED, KR)
    return x, y, w, h

T1A = unit(112, 140, 188, 60, "tier-1 ISP", "약 열두 곳")
T1B = unit(332, 140, 188, 60, "tier-1 ISP", "아무에게도 안 냅니다")
RGA = unit(88, 264, 172, 60, "지역 ISP", "성·국가 단위도 있습니다")
RGB = unit(316, 264, 172, 60, "지역 ISP", "여럿이 경쟁합니다")
ACA = unit(52, 388, 150, 60, "접속 ISP", "가정·기업·대학")
ACB = unit(238, 388, 150, 60, "접속 ISP", "멀티호밍 가능")
ACC_ = unit(424, 388, 150, 60, "접속 ISP", "콘텐츠 제공자도 고객")

def pay(a, b):
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    d.arrow([(ax + aw / 2, ay), (ax + aw / 2, by + bh + 4)], MUTED, "ar", 1.3)

pay(RGA, T1A); pay(RGB, T1B); pay(ACA, RGA); pay(ACB, RGA); pay(ACC_, RGB)

# 피어링 — 같은 계층끼리, 정산 없음
d.path(f"M {T1A[0] + T1A[2]} 170 L {T1B[0] - 4} 170", OK, 1.4, m="ok", dash="5 5")
d.t((T1A[0] + T1A[2] + T1B[0]) / 2, 162, "피어링", 11, OK, KR)

d.box(CX0, 100, CW, 396, PAPER2, RULE, 0.8, 8)
d.t(CX0 + 14, 120, "콘텐츠 제공자 망", 11, SOFT, KR, "start", 600)
CP = unit(CX0 + 24, 140, CW - 48, 84, "구글 사설 TCP/IP 망", "데이터센터 20여 곳 · 공개 인터넷과 분리")
d.t(CX0 + CW / 2, 214, "IXP 안에도 작은 데이터센터를 둡니다", 11, MUTED, KR)
IXP = unit(CX0 + 24, 300, CW - 48, 60, "IXP", "600곳 이상 · 여럿이 모여 피어링", ACC)

d.arrow([(CX0 + CW / 2, 224), (CX0 + CW / 2, 296)], MUTED, "ar", 1.3)
d.path(f"M {CX0 + 24} 330 L {ACC_[0] + ACC_[2] + 8} 330 L {ACC_[0] + ACC_[2] + 8} 400", ACC, 1.6, m="acc")
d.t(CX0 - 96, 322, "상위 계층을 건너뜁니다", 11, ACC, KR)
d.path(f"M {CX0 + CW / 2} 140 L {CX0 + CW / 2} 128 L {T1B[0] + T1B[2] + 6} 128 L {T1B[0] + T1B[2] + 6} 158",
       MUTED, 1.3, m="ar", dash="4 4")
d.t(CX0 - 40, 122, "닿지 않는 곳은 tier-1 에 값을 냅니다", 11, MUTED, KR, "end")

d.t(ZL, 520, "2020년 기준 Amazon·Google·IBM·Microsoft 는 tier-1 을 거치지 않고 인터넷의 76% 에 닿습니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("계층을 우회하는 자리", ACC), ("정산 없는 피어링", OK), ("고객이 제공자에게", MUTED)])
d.save("01-03.isp-hierarchy.svg")
