# 08-01 §6 — 호스트 간 시계 오차가 스팬 순서를 뒤집어 보이게 한다.
# 원문 근거: "DNS requests are often very short, often far less than one millisecond. If your
#            request spans multiple hosts, even a few nanoseconds of difference in your clocks can
#            lead to some misleading results; for example, spans that start on the server before
#            they leave the client!"
# 타입 스펙: type-gantt — 스팬은 시작과 길이를 가진 막대이고, 막대의 상대 위치가 곧 인과의
#           주장이다. 그 위치가 시계 오차로 어긋나는 것이 이 그림의 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 578
d = D(W, H, "LEARNING COREDNS · 08-01 §6",
      "스팬이 시계 오차로 어긋나 보이는 자리",
      "위는 시계가 맞을 때의 스팬 배치이고, 아래는 호스트 시계가 조금 어긋났을 때다. "
      "요청이 1밀리초에도 못 미치면 나노초 단위 오차가 순서를 뒤집어 보이게 한다.",
      "주황이 클라이언트를 떠나기 전에 시작한 것처럼 보이는 스팬입니다")

X0, X1 = 250, 830
LBLX = 236


def band(y, title, rows, focal_idx=None):
    d.t(20, y - 14, title, 12, INK, KR, "start", 600)
    for i, (name, x, w, c) in enumerate(rows):
        yy = y + i * 40
        d.t(LBLX, yy + 15, name, 11, MUTED, MONO, "end")
        if focal_idx is not None and i == focal_idx:
            d.tone(x, yy, w, 22, ACC, 4, "20", 1.4)
        else:
            d.tone(x, yy, w, 22, c, 4, "20", 1.2)


d.line(X0, 108, X1, 108, RULE, 0.8)
d.t(X0, 100, "시간", 11, SOFT, KR, "start")

band(132, "시계가 맞을 때", [
    ("client", 280, 470, OK),
    ("coredns", 340, 350, OK),
    ("upstream", 430, 190, OK),
])

d.line(X0, 268, X1, 268, RULE, 0.8)

band(292, "서버 시계가 조금 빠를 때", [
    ("client", 280, 470, MUTED),
    ("coredns", 262, 350, MUTED),
    ("upstream", 352, 190, MUTED),
], focal_idx=1)

# 어긋남 표시 — 클라이언트가 보낸 시각에 세로선을 세우면 서버 스팬이 그 왼쪽에서 시작한다
d.path("M 280 288 L 280 402", ACC, 1.2, dash="4 4")

d.box(20, 414, 840, 84, PAPER, RULE, 0.8)
d.t(36, 438, "점선이 클라이언트가 보낸 시각이고, 서버 스팬이 그 왼쪽에서 시작한다", 12, ACC, KR, "start", 600)
d.t(36, 462, "그래도 추적은 쓸모 있는 신호를 준다고 저자들이 적는다", 12, INK, KR, "start", 600)
d.t(36, 484, "다만 스팬의 절대 시각을 인과의 근거로 삼지 않는 것이 이 주의를 아는 실무적 형태다",
     11, MUTED, KR, "start")

d.legend(518, [("어긋나 보이는 스팬", ACC), ("시계가 맞을 때", OK)])
d.save("08-01.trace-clock.svg")
