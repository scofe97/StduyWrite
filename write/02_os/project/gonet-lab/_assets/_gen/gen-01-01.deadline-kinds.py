# 01-01.deadline-kinds — deadline 을 한 번만 걸 때와 받을 때마다 밀 때
# 본문 요구(01-01 §4): 한 번만 건 deadline 은 입력이 계속 와도 처음 정한 시각에 끊고, 받을 때마다 민 deadline 은
#           마지막 입력 뒤 30초가 조용히 지나야 끊는다 — 막대의 끝이 무엇에 묶이는지가 논지다.
# 타입 스펙: type-gantt — 시간 막대. 맨 위 줄은 입력 시점, 아래 두 줄이 두 방식의 연결 수명. 가상 시나리오(입력 5·20·35초).
# 사실 출처: go doc net.Conn (deadline 은 절대 시각), 본문 §4.
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, KR, MONO

W, H = 960, 420
TX0, PX, LX = 220, 8.5, 24    # 0초 x, 1초당 px (80초 = 680px)
d = D(W, H, "GANTT · 01-01 DEADLINE KINDS", "deadline 을 한 번 걸 때와 계속 밀 때",
      "입력이 5·20·35초에 오는 가상 연결에 30초 deadline 을 건 두 방식을 비교한 도식. 접속 때 한 번만 걸면 30초에 "
      "끊겨 35초의 입력을 받지 못한다. 받을 때마다 지금부터 30초 뒤로 밀면 마지막 입력인 35초에서 30초가 지난 65초에 끊긴다.",
      lead="가상 시나리오입니다. 입력은 5·20·35초에 오고, 제한은 30초입니다.")
def x(t): return TX0 + t * PX
for t, lab in [(0, "0초 · 접속"), (30, "30초"), (65, "65초"), (80, "80초")]:
    d.t(x(t), 116, lab, 12, SOFT, KR, "start" if t == 0 else "middle")
    d.line(x(t), 128, x(t), 352, RULE, 0.8, "3 5")
d.line(TX0, 128, x(80), 128, RULE, 0.8)
d.t(LX, 164, "입력", 13, INK, KR, "start", 600)
for t in (5, 20, 35):
    d.tone(x(t) - 5, 150, 10, 20, INFO, 2, "40", 1.2)
    d.t(x(t), 188, f"{t}초", 12, INFO, MONO, "middle")
def row(y, name, sub, end, c, text):
    d.t(LX, y + 20, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 38, sub, 12, MUTED, KR, "start")
    d.tone(TX0, y + 10, end * PX, 24, c, 4, "12", 1.0)
    d.t(TX0 + 12, y + 27, text, 12, c, KR, "start")
row(216, "한 번만 건 deadline", "접속 때 30초 뒤로", 30, BAD, "30초에 끊김")
d.t(x(35) + 8, 243, "35초 입력을 못 받음", 12, BAD, KR, "start")
row(288, "받을 때마다 민 deadline", "받을 때마다 30초 뒤로", 65, OK, "마지막 입력 뒤 30초가 지나 끊김")
d.legend(372, [("입력", INFO), ("idle timeout", OK), ("수명 제한이 돼 버림", BAD)])
d.save("01-01.deadline-kinds.svg")
print("ok deadline")
