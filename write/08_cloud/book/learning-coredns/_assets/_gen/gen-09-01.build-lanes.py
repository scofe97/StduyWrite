# 09-01 §3 — 두 빌드 길이 무엇을 주고받는가.
# 원문 근거: "Building with Docker works, but it has one big drawback: it is really slow when
#            doing iterative development. Because the build is using Docker, it starts with a
#            fresh container every time and needs to download all of the packages again."
#            / "you will need Go 1.12 or later, Git, and Make"
# 타입 스펙: type-swimlane — 두 길이 레인이고 같은 목적지(표준 바이너리)에 서로 다른 준비와
#           대가로 닿는다. 레인마다 걸음 수가 달라도 되는 것이 이 타입의 성질이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING COREDNS · 09-01 §3",
      "두 빌드 길이 무엇을 주고받는가",
      "Docker 길은 기계에 아무것도 깔지 않는 대신 매번 처음부터 받는다. 로컬 길은 환경을 "
      "갖추는 대신 반복이 빠르다.",
      "주황이 반복 개발에서 갈리는 자리입니다")

LX, LW, LH = 160, 700, 130
LANES = [("DOCKER", "기계에 Docker 만", 118), ("LOCAL", "Go · Git · Make", 274)]
for nm, sub, y in LANES:
    d.box(LX, y, LW, LH, PAPER, RULE, 0.8, 6)
    d.t(20, y + 38, nm, 9, SOFT, MONO, "start", 600)
    d.t(20, y + 60, sub, 12, MUTED, KR, "start")

SW, SG, SX0 = 205, 20, 180
XS = [SX0 + i * (SW + SG) for i in range(3)]


def step(x, y, t1, t2, c=INK, tone=None):
    if tone:
        d.tone(x, y, SW, 72, tone, 6, "12", 1.4)
    else:
        d.box(x, y, SW, 72, PAPER2, RULE, 1.0)
    d.t(x + SW / 2, y + 28, t1, 13, c, KR, "middle", 600)
    d.t(x + SW / 2, y + 50, t2, 11, MUTED, MONO)


step(XS[0], 148, "이미지로 소스를 받는다", "-u 를 붙인다")
step(XS[1], 148, "이미지로 빌드한다", "-u 를 뗀다")
step(XS[2], 148, "매번 다시 받는다", "반복이 느리다", ACC, ACC)

step(XS[0], 304, "Go 를 /usr/local 에", "1.12 이상 · 예제는 1.12.4")
step(XS[1], 304, "아무 데나 clone", "go modules · GOPATH 무관")
step(XS[2], 304, "캐시가 남는다", "반복이 빠르다", OK, OK)

for row_y in (184, 340):
    d.arrow([(XS[0] + SW, row_y), (XS[1] - 2, row_y)], MUTED, "ar", 1.4)
    d.arrow([(XS[1] + SW, row_y), (XS[2] - 2, row_y)], MUTED, "ar", 1.4)

d.box(20, 426, 840, 62, PAPER, RULE, 0.8)
d.t(36, 450, "나오는 바이너리는 같다 — 둘 다 손대지 않은 표준 바이너리다", 12, INK, KR, "start", 600)
d.t(36, 472, "Docker 로 빌드하면 맥에서 돌려도 리눅스 바이너리가 나온다 · 빌드하는 컨테이너가 리눅스이기 때문이다",
     11, MUTED, KR, "start")

d.legend(508, [("반복에서 드는 값", ACC), ("반복에서 아끼는 값", OK)])
d.save("09-01.build-lanes.svg")
