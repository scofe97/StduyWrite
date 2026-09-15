# 03-04 §4 시나리오 2 — 원문 Figure 3.45·3.46. 버퍼가 유한해 버려진 패킷을 다시 보내므로 제공 부하 λ'in 이 λin 보다 크다.
# 본문 근거: "확실히 잃어버린 것만 재전송하면 제공 부하 R/2 에서 처리량 R/3 · 성급히 재전송하면 R/4 로 수렴 ·
#   버퍼가 빈 것을 알고 보내면 처리량 = λin". 끝값 R/3·R/4 는 원문 수치이고 중간 모양은 원문 그림처럼 개략이다.
# 타입 스펙: type-line — 제공 부하에 따른 처리량 세 곡선. 위쪽 띠의 토폴로지는 문맥이다.
import sys; sys.path.insert(0, ".")
from _cc_common import *

W, H = 1000, 560
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §4",
      "시나리오 2 — 유한 버퍼는 재전송을 부르고 재전송이 용량을 먹습니다",
      "원문 Figure 3.45·3.46. 같은 제공 부하 R/2 에서 처리량은 가정에 따라 R/2·R/3·R/4 로 갈린다.",
      "가로축은 재전송을 포함한 제공 부하 λ'in 입니다. 세 곡선의 끝값이 원문 수치입니다")

ty = 150
host(d, 90, ty - 22, "A"); host(d, 90, ty + 22, "B")
router(d, 300, ty, "R", "버퍼 유한 · 넘치면 버림", BAD)
fan_in(d, [112, 112], [ty - 22, ty + 22], 240, ty, 282)
link(d, 318, ty, 440, ty, ACC, "용량 R", -10)
host(d, 520, ty - 22, "C"); host(d, 520, ty + 22, "D")
fan_out(d, 440, ty, 480, [ty - 22, ty + 22], 496)
d.t(560, ty - 14, "버려진 패킷은 다시 보냄 · 그래서 실제 송출은", 11, MUTED, KR, "start")
d.t(560, ty + 4, "원래 데이터 λin 에 재전송을 더한 제공 부하 λ'in", 11, MUTED, KR, "start")
d.t(560, ty + 22, "라우터가 나르는 것 중 일부는 이미 도착한 패킷의 사본", 11, BAD, KR, "start")

xt = [(0, "0"), (0.5, "R/4"), (1, "R/2")]
yt = [(0, "0"), (0.5, "R/4"), (2 / 3, "R/3"), (1, "R/2")]
c = Chart(d, 24, 196, 952, 300, "λ'in (재전송을 포함한 제공 부하)", "처리량 λout", xt, yt)
xs = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
c.series([(x, x) for x in xs], OK)                                   # (a) 이상
c.series([(x, x * (1 - x / 3)) for x in xs], ACC, focal=True)        # (b) 끝값 R/3
c.series([(x, x * (1 - x / 2)) for x in xs], BAD, dash="5 4")        # (c) 끝값 R/4
c.note(0.62, 0.72, "(a) 버퍼가 빈 것을 알고 보냄 = λin", OK, "end")
c.note(0.98, 0.76, "(b) 확실히 잃은 것만 재전송 → R/3", ACC, "end")
c.note(0.98, 0.42, "(c) 성급한 재전송 → R/4", BAD, "end")

d.legend(H - 44, [("이상 — 손실 없음", OK), ("잃은 것만 재전송 — 두 번째 대가", ACC), ("성급한 재전송 — 세 번째 대가", BAD)])
d.save("03-04.cc-scenario2.svg")
print("ok cc-scenario2")
