# 06-01 §2 — 인증서 발급에서 연결 상한까지 시간 축 한 장.
# 타입 스펙: type-timeline — 0~60분을 같은 눈금으로 두고, 레인마다 한 가지 대상이
#           언제까지 허용되는지를 막대로 그린다. 눈금은 설계값(5분 인증서 · 60분 상한)이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 880, 452
d = D(W, H, "LAMPSON LAB · 06-01 §2",
      "인증서 발급에서 연결 상한까지",
      "인증서는 5분 뒤 새 연결을 거부하지만, 이미 열린 연결은 호스트가 60분에 끊을 때까지 남는다.",
      "눈금은 설계값이다 — 새 연결·열린 연결은 AC-19·20, 끊김은 EP-11 이 확인했고 나머지 두 줄은 README 서술이다")

X0, XE = 208, 832          # 0분 ~ 60분
def x(m): return X0 + (XE - X0) * m / 60.0

LANES = [128, 184, 240, 296, 352]
labels = ["인증서", "새 연결", "열린 연결", "연결 위 새 세션", "분리된 프로세스"]
for y, lab in zip(LANES, labels):
    d.t(24, y + 28, lab, 12, INK, KR, "start", 600)

# 세로 기준선: 만료(5분)와 연결 상한(60분)
d.line(x(5), 104, x(5), 400, RULE, 0.8, "3 4")
d.line(x(60), 104, x(60), 400, ACC, 1.2)
d.t(x(0), 112, "발급 · 접속", 12, MUTED, KR, "middle")
d.t(x(5) + 8, 112, "만료 5분", 12, MUTED, KR, "start")
d.t(x(60) - 8, 112, "호스트가 연결을 끊음 60분", 12, ACC, KR, "end")

def bar(m0, m1, y, txt, kind):
    w = x(m1) - x(m0)
    if kind == "ok":
        d.tone(x(m0), y, w, 40, OK, 6, "18", 1.1)
    elif kind == "bad":
        d.tone(x(m0), y, w, 40, BAD, 6, "18", 1.1)
    elif kind == "acc":
        d.tone(x(m0), y, w, 40, ACC, 6, "18", 1.4)
    else:
        d.box(x(m0), y, w, 40, PAPER2, RULE, 1.0, 6)
    c = {"ok": OK, "bad": BAD, "acc": ACC}.get(kind, MUTED)
    d.t(x(m0) + 10, y + 25, txt, 12, c, KR, "start", 600 if kind != "n" else 400)

bar(0, 5, LANES[0], "5분", "n")
bar(0, 5, LANES[1], "허용", "ok")
bar(5, 60, LANES[1], "거부  Certificate invalid: expired", "bad")
bar(0, 60, LANES[2], "인증서가 만료돼도 유지", "acc")
bar(5, 60, LANES[3], "ControlMaster 로 새 세션이 계속 열림", "ok")

# 분리된 프로세스: 연결 상한 뒤에도 이어진다
y = LANES[4] + 20
d.arrow([(x(0), y), (XE + 30, y)], MUTED, "ar", 1.6, "5 4")
d.t(x(0) + 10, y - 10, "PID 1 밑으로 분리된 프로세스는 연결 상한 뒤에도 남음", 12, MUTED, KR, "start")

# 눈금
AY = 416
d.line(X0, AY, XE, AY, RULE, 1.0)
for m in (0, 5, 15, 30, 45, 60):
    d.line(x(m), AY - 4, x(m), AY + 4, SOFT, 1.0)
    d.t(x(m), AY + 20, f"{m}분", 12, MUTED, MONO, "middle")
d.save("06-01.expiry-timeline.svg")
