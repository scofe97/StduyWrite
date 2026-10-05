# 01-01 §5 다중 원인 — 정상 사건 셋이 겹치는 창에서만 성능 문제가 생긴다(가상 예시).
# 타입 스펙: type-gantt — 막대 길이가 곧 사건이 이어진 구간이고, 구간들의 시간 겹침이 논지다.
#           축약: 날짜 대신 단위 없는 상대 눈금 t0~t6 을 쓴다. 원서는 사건 이름을 들지 않아 이름은 가상이다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 920, 456
LX, TX, PITCH = 24, 216, 112          # 라벨 열 · 시간축 시작 · 눈금 간격
Y0, ROW, BH = 144, 48, 28

def tx(t): return TX + t * PITCH

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-01 §5 · SEC 1.5.3",
       "정상 사건 셋이 겹칠 때만 문제가 된다 (가상 예시)",
       "원서 1.5.3 의 장면을 시간축에 옮긴 가상 예시. 사건 셋은 각각 평소에도 일어나는 정상 사건이고, 성능 문제는 세 막대가 겹치는 창에서만 생긴다. 사건 이름은 설명을 위해 붙였다.",
       "하나씩 떼어 보면 셋 다 정상이라 어느 것도 근본 원인이 아닙니다")

# 겹치는 창
s, e = 3, 4
for x in (tx(s), tx(e)):
    d.line(x, Y0 - 12, x, Y0 + 4 * ROW - 8, ACC, 1.4, "4 4")
d.t((tx(s) + tx(e)) / 2, Y0 - 20, "겹치는 창", 13, ACC, KR, "middle", 600)

ROWS = [
    ("배치 작업", 1, 4, MUTED),
    ("캐시 갱신", 2.5, 4.5, MUTED),
    ("트래픽 피크", 3, 5.5, MUTED),
    ("성능 문제", s, e, BAD),
]
for i, (name, a, b, c) in enumerate(ROWS):
    y = Y0 + i * ROW
    d.t(TX - 16, y + 19, name, 13, c if c is BAD else INK, KR, "end", 600)
    if c is BAD:
        d.tone(tx(a), y, tx(b) - tx(a), BH, c, 4, "33", 1.2)
    else:
        d.tone(tx(a), y, tx(b) - tx(a), BH, MUTED, 4, "26", 1.0)
        d.t(tx(a) + 10, y + 19, "정상", 12, MUTED, KR, "start")

YA = Y0 + 4 * ROW + 12
d.line(TX, YA, tx(6), YA, RULE, 1.0)
for k in range(7):
    d.line(tx(k), YA, tx(k), YA + 6, RULE, 1.0)
    d.t(tx(k), YA + 22, f"t{k}", 12, SOFT, MONO, "middle")
d.t(TX - 32, YA + 22, "시간", 12, SOFT, KR, "end")

d.legend(YA + 48, [("정상 사건", MUTED), ("성능 문제", BAD), ("세 사건이 겹치는 창", ACC)])
d.save("01-01.multiple-causes-overlap.svg")
