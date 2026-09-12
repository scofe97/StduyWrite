# 02-02 §6 — 원문 2.2.6 의 수치 예. 비디오 1000 프레임 + 작은 객체 8개(각 2 프레임)일 때,
# 작은 객체가 전부 도착할 때까지 보내야 하는 프레임 수. 두 값 모두 원문에 적힌 그대로이고 셈도 맞다.
#   인터리빙 있음: (비디오 1 + 작은 것 8) + (비디오 1 + 작은 것 8) = 18
#   인터리빙 없음: 비디오 1000 + 작은 것 16 = 1016
# 타입 스펙: type-bar — 범주별 단일 수치 비교. y축은 0에서 시작하고 눈금 다섯을 둔다.
#           축약: 막대가 둘이다(스펙 권장 4~8). 원문이 비교하는 값이 둘뿐이라 범주를 지어내지 않는다.
#           18 짜리 막대가 거의 보이지 않는 것은 축을 자르지 않았기 때문이며, 그 비율이 이 절의 요점이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
PX0, PX1, PY0, PY1 = 150, 900, 132, 404
YMAX = 1100

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-02 §6",
      "인터리빙이 있고 없고",
      "원문의 수치 예. 큰 비디오 하나와 작은 객체 여덟 개를 한 TCP 연결로 보낼 때, 작은 객체가 전부 도착할 때까지 보내야 하는 프레임 수.",
      "축을 자르지 않았습니다 — 오른쪽 막대가 거의 안 보이는 것이 이 절의 요점입니다")

def ypx(v): return PY1 - (v / YMAX) * (PY1 - PY0)

for g in range(0, YMAX + 1, 220):
    y = ypx(g)
    d.line(PX0, y, PX1, y, RULE, 0.8)
    d.t(PX0 - 12, y + 4, str(g), 12, MUTED, MONO, "end")
d.line(PX0, PY0, PX0, PY1, RULE, 1.0)
d.line(PX0, PY1, PX1, PY1, MUTED, 1.0)
d.t(PX0 - 12, PY0 - 16, "보내야 하는 프레임 수", 12, SOFT, KR, "end")

BARS = [("인터리빙 없음", "비디오 1000 프레임을 다 보낸 뒤에야 차례가 옵니다", 1016, False),
        ("인터리빙 있음", "비디오 프레임 사이사이에 끼워 보냅니다", 18, True)]
BW, PITCH = 230, 380
for i, (name, sub, v, focal) in enumerate(BARS):
    cx = PX0 + 60 + i * PITCH + BW / 2
    x, y = cx - BW / 2, ypx(v)
    h = max(PY1 - y, 2)
    if focal:
        d.tone(x, y, BW, h, ACC, 4)
    else:
        d.box(x, y, BW, h, PAPER2, MUTED, 1.0, 4)
    d.t(cx, (y + 24) if h > 40 else (y - 14), f"{v:,} 프레임", 12, ACC if focal else MUTED, KR, "middle", 600)
    d.t(cx, PY1 + 30, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, PY1 + 52, sub, 12, MUTED, KR)

d.t(20, 492, "HTTP/2 는 각 메시지를 작은 프레임으로 쪼개 같은 TCP 연결 위에서 번갈아 끼워 넣습니다. 헤더 필드가 한 프레임이 되고 본문이 나머지 프레임이 됩니다.",
     11, MUTED, KR, "start")
d.t(20, 514, "이 인터리빙이 원문이 말하는 HTTP/2 의 가장 중요한 단일 개선입니다. 다만 트랜스포트 층의 HOL 블로킹은 그대로 남습니다.",
     11, MUTED, KR, "start")

d.legend(H - 48, [("인터리빙이 만든 값", ACC), ("HTTP/1.1 의 한 연결", MUTED)])
d.save("02-02.frame-interleaving.svg")
