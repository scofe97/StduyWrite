# 01-01 §2 — 원서가 "The Linux Story (So Far)" 에서 세 구간으로 자른 30년.
# 원문: 1991년 8월 25일 comp.os.minix 메일을 공개 기록상의 시작으로 본다. "after less than three years,
#       Linux 1.0.0 was released with over 176,000 LOCs". 1990년대에 첫 상용 배포판 Red Hat Linux 가 나온다.
#       2000~2010 은 Google·Amazon·IBM 의 채택과 "the peak of the distro wars" 다.
#       2010년대 이후는 데이터센터·클라우드의 일꾼이 되고, 저자는 배포판 전쟁이 끝난 원인으로
#       2014/15년부터의 컨테이너 부상을 든다. 2021년에 서른 살이 됐다.
# 원문이 1.0.0 의 연도를 적지 않으므로 이 도식도 연도를 적지 않고 "3년 안" 으로만 둔다.
# 타입 스펙: type-timeline — 사건이 시간 위에 놓이고 세대가 바꾼 것을 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, RULE, KR, MONO

W, H = 880, 428
d = D(W, H, "LEARNING MODERN LINUX · 01-01 §2",
      "취미 프로젝트에서 데이터센터의 일꾼까지",
      "원서가 1장에서 세 구간으로 자른 리눅스 약사. 배포판 전쟁이 정점을 찍은 구간과, "
      "저자가 그 전쟁을 끝냈다고 지목한 컨테이너의 등장 시점을 함께 표시한다.",
      "색이 붙은 점이 저자가 전쟁을 끝냈다고 지목한 힘입니다")

X0 = 84
SPAN = W - X0 - 84
BY = 184

events = [
    (0.00, "1991-08-25", "comp.os.minix 메일", MUTED, True),
    (0.16, "3년이 채 되기 전", "Linux 1.0.0 · 176,000 LOC 넘김", INFO, False),
    (0.32, "1990년대", "Red Hat Linux — 첫 상용", INFO, True),
    (0.54, "2000~2010", "구글 · 아마존 · IBM 이 올라탐", INFO, False),
    (0.76, "2014~15", "컨테이너의 부상", ACC, True),
    (0.96, "2021", "서른 살", OK, False),
]

# 배포판 전쟁 구간 음영 — 원문은 2000~2010 을 정점으로 적고 2010년대에 끝났다고 본다.
sx, ex = X0 + SPAN * 0.44, X0 + SPAN * 0.76
d.tone(sx, BY - 14, ex - sx, 28, INFO, r=4, op="10", sw=0.0)
d.t((sx + ex) / 2, BY + 84, "배포판 전쟁 — 정점에서 소멸까지", 12, INFO, KR, "middle", 600)

d.line(X0, BY, X0 + SPAN, BY, RULE, 1.0)
for frac, label, sub, c, above in events:
    x = X0 + SPAN * frac
    r = 6 if c is ACC else 4
    d.o.append(f'<circle cx="{x}" cy="{BY}" r="{r}" fill="{c}"/>')
    ly = BY - 24 if above else BY + 24
    d.line(x, BY + (-8 if above else 8), x, ly + (6 if above else -6), c, 0.8)
    d.t(x, ly + (0 if above else 14), label, 12.5, INK, KR, "middle", 600)
    d.t(x, ly + (-18 if above else 32), sub, 12, MUTED, KR)

cy = BY + 108
d.tone(X0 - 68, cy, W - 32 - 16, 60, INFO)
d.t(X0 - 50, cy + 26, "전쟁이 끝난 자리에 남은 것은 두 계열이다", 13, INK, KR, "start", 600)
d.t(X0 - 50, cy + 46, "저자는 요즘 상용 시스템 대부분이 Red Hat 계열 아니면 Debian 계열이라고 적습니다.",
    12, MUTED, KR, "start")

d.legend(376, [("원서가 짚은 사건", INFO), ("전쟁을 끝낸 힘", ACC), ("현재", OK)])
d.save("01-01.linux-timeline.svg")
print("ok 01-01.linux-timeline")
