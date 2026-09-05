# 08-01 §5 — consolidate 가 시간 창 하나 안의 같은 오류를 한 줄로 접는다.
# 원문 근거: "errors also allows you to consolidate multiple error messages that match the same
#            regular expression. That way, if CoreDNS is experiencing continuous errors when
#            forwarding queries, for example, you won't be inundated with error messages."
#            / 접힌 출력: "5 errors like '^.* network is unreachable$' occurred in last 10m"
#            / "You should also take care not to consolidate too much"
# 타입 스펙: type-timeline — 시간 축 위의 사건들과 그것을 덮는 창 하나가 논지다.
#           창의 폭(DURATION)과 사건 간격의 관계는 축이 있어야만 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, KR, MONO

W, H = 880, 484
d = D(W, H, "LEARNING COREDNS · 08-01 §5",
      "같은 오류 다섯이 시간 창 하나로 접힌다",
      "상류가 끊기면 같은 오류가 계속 쏟아진다. consolidate 는 DURATION 만큼의 창을 두고 "
      "그 안에서 REGEXP 에 맞는 것들을 세어 한 줄로 내놓는다.",
      "주황이 접힌 뒤 남는 유일한 줄입니다")

AX_Y, X0, X1 = 196, 90, 800
d.line(X0, AX_Y, X1, AX_Y, MUTED, 1.0)

# 창 — DURATION 10m
d.tone(X0, 132, X1 - X0, 112, BAD, 6, "0E", 1.2)
d.t(X0 + 14, 154, "consolidate 10m", 11, BAD, MONO, "start", 600)

# 사건 다섯 — 창 길이(10m)와 건수(5)만 원서 값이다. 도착 시각은 원서에 없으므로
# 눈금 값을 지어내지 않고, 고르지 않게만 놓아 "고르게 온다"는 인상을 주지 않는다.
EV = [140, 238, 402, 498, 688]
for i, x in enumerate(EV, 1):
    d.tone(x - 5, AX_Y - 5, 10, 10, BAD, 5, "FF", 1.0)
    d.t(x, AX_Y - 18, "network is", 10, BAD, MONO)
    d.t(x, AX_Y - 5, "unreachable", 10, BAD, MONO)
    d.t(x, AX_Y + 26, f"#{i}", 10, SOFT, MONO)

d.t(X0 + 14, 222, "0m", 10, SOFT, MONO, "start")
d.t(X1 - 14, 222, "10m", 10, SOFT, MONO, "end")
d.t(440, 266, "창 길이와 건수는 원서 값이고, 도착 시각은 원서에 없어 눈금을 매기지 않았다", 11, SOFT, KR)

# 접힌 결과
d.path(f"M 440 280 L 440 312", ACC, 1.5, m="acc")
d.tone(180, 314, 520, 56, ACC, 6, "14", 1.5)
d.t(440, 338, "5 errors like '^.* network is unreachable$'", 12, ACC, MONO)
d.t(440, 358, "occurred in last 10m", 12, ACC, MONO)

d.box(20, 386, 840, 40, PAPER, RULE, 0.8)
d.t(36, 411, "너무 넓게 접으면 접힌 줄에 정규식만 남아 원래 오류가 무엇에 대한 것이었는지 알 수 없다",
     12, MUTED, KR, "start")

d.legend(434, [("접히기 전의 오류", BAD), ("접힌 뒤 남는 한 줄", ACC)])
d.save("08-01.error-fold.svg")
