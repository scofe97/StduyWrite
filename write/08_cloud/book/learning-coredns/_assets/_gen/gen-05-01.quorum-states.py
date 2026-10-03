# 05-01 §4 — etcd 셋 중 하나를 잃어도 과반이 남아 계속 동작하고, 둘을 잃으면 쿼럼을 잃는다.
# 본문 근거: 이 노트 §4 쿼럼 문단(원서 요지 — 절반을 넘는 인스턴스가 살아 통신하면 읽기·쓰기를 받고, 셋 중 하나를 잃어도 동작).
#            원서 영문을 대조하지 못해 영문 인용은 싣지 않는다.
# 타입 스펙: type-state — 살아 있는 대수가 줄어드는 세 상태와 그 사이의 전이가 논지다.
#           셋째 상태의 "쓰기 불가"는 쿼럼 정의에서 나온 귀결이라 원문의 "계속 동작" 의 반대만 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 05-01 §4",
      "셋 중 하나를 잃어도 과반이 남는다",
      "etcd 는 절반을 넘는 인스턴스가 살아 서로 통신하는 동안 읽기와 쓰기를 받는다. "
      "세 대면 과반은 둘이므로 한 대 장애는 견디고, 두 대가 죽으면 쿼럼을 잃는다.",
      "주황 상자가 원문이 짚는 경우입니다")

states = [
    ("세 대 모두 정상", 3, "읽기 · 쓰기 계속", OK),
    ("한 대를 잃음", 2, "읽기 · 쓰기 계속", OK),
    ("두 대를 잃음", 1, "쿼럼 상실 · 쓰기 불가", BAD),
]
XS = [20, 315, 610]
BW, BY, BH = 250, 124, 240

for i, (title, alive, verdict, vc) in enumerate(states):
    x = XS[i]
    if i == 1:
        d.tone(x, BY, BW, BH, ACC, 8, "12", 1.4)
    else:
        d.box(x, BY, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, BY + 30, title, 14, ACC if i == 1 else INK, KR, "start", 600)
    for n in range(3):
        cx, cy = x + 65 + n * 60, BY + 90
        up = n < alive
        c = OK if up else BAD
        d.o.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="{c}22" stroke="{c}" stroke-width="1.2"/>')
        if up:
            d.t(cx, cy + 4, "etcd", 12, c, MONO)
        else:
            d.line(cx - 9, cy - 9, cx + 9, cy + 9, c, 1.6)
            d.line(cx - 9, cy + 9, cx + 9, cy - 9, c, 1.6)
    d.t(x + BW / 2, BY + 150, f"살아 있음 {alive}/3", 15, INK, KR, "middle", 600)
    d.t(x + BW / 2, BY + 174, "과반 기준 2", 12, MUTED, KR)
    cw = 200
    d.o.append(f'<rect x="{x + (BW - cw) / 2}" y="{BY + 194}" width="{cw}" height="28" rx="4" '
               f'fill="{vc}22" stroke="{vc}" stroke-width="1.1"/>')
    d.t(x + BW / 2, BY + 213, verdict, 13, vc, KR)
    if i < 2:
        gx = x + BW
        d.path(f"M {gx + 4} {BY + 90} L {XS[i + 1] - 4} {BY + 90}", MUTED, 1.4, m="ar")
        d.t((gx + XS[i + 1]) / 2, BY - 10, "1대 장애", 12, MUTED, KR)

d.t(20, 404, "쿼럼 · 절반을 넘는 수가 살아 있고 서로 통신하는 상태", 13, MUTED, KR, "start")

d.legend(420, [("원문의 예 · 하나를 잃어도 동작", ACC), ("살아 있는 인스턴스", OK), ("잃은 인스턴스", BAD)])
d.save("05-01.quorum-states.svg")
