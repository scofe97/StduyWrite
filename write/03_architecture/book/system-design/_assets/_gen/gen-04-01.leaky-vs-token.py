# 타입 스펙: type-process — 같은 몰림(5건 동시 도착)을 두 레인(토큰 버킷 · 누출 버킷)에 넣고, 시각 칸마다 통과한 요청 수를 개수로 맞대 본다.
# 사실 출처: 추출본 v2.txt 975~979행(토큰 버킷: 토큰이 남은 만큼 통과 · 없으면 버림), 1005~1008행(누출 버킷: 큐가 차면 버림 · 정해진 간격으로 꺼내 처리), 1014~1018행(버킷 크기 = 큐 크기 · 유출 속도),
#   PDF 쪽 56 · 58 그림(요청 5건이 도착해 3건이 통과하고 2건이 버려진다). 크기 3 · 초당 1건 유출은 본문 예시 값이며 나머지는 정의에서 계산했다(통과 = 3, 버림 = 5 − 3 = 2, 유출 시각 1~3초).
# Layout conventions: 레인 이름 열 x=24, 시각 칸 폭 180 · 간격 12(x=172 부터 stride 192), 머리 y=100 높이 32, 레인 y=148·276 높이 112. 요청 칸 20 · 간격 26. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 468
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-01 §4",
      "같은 몰림을 누출 버킷은 일정한 간격으로 내보낸다",
      "5건이 한꺼번에 도착하면 크기 3인 토큰 버킷은 3건을 즉시 통과시키고 2건을 버리며, 큐 크기 3에 초당 1건을 꺼내는 누출 버킷은 3건을 큐에 담고 2건을 버린 뒤 1초에 1건씩 내보낸다.",
      "5건 동시 도착 · 초당 1건 유출")

X0, CW, STRIDE = 172, 180, 192
N = 4
HY = 100
LY = (148, 276)
LH = 112

# 평탄한 출력 레인 — focal
d.tone(164, LY[1] - 4, 768, LH + 8, ACC, 8, "10", 1.4)

for i in range(N):
    d.t(X0 + STRIDE * i + CW / 2, HY + 24, f"{i}초", 14, INK, MONO, "middle", 600)

for ly, name, sub in ((LY[0], "토큰 버킷", "통 크기 3"), (LY[1], "누출 버킷", "큐 3 · 초당 1건")):
    d.t(24, ly + 48, name, 14, INK, KR, "start", 600)
    d.t(24, ly + 72, sub, 13, MUTED, KR, "start")


def sq(x, y, c):
    d.tone(x, y, 20, 20, c, 3, "22", 1.1)


# 토큰 버킷 레인: 0초에 3건이 한꺼번에
for i in range(N):
    x = X0 + STRIDE * i
    if i == 0:
        for k in range(3):
            sq(x + 12 + 26 * k, LY[0] + 16, OK)
        d.t(x + 12, LY[0] + 68, "통과 3", 13, OK, KR, "start", 600)
        d.t(x + 12, LY[0] + 92, "버림 2", 13, BAD, KR, "start", 600)
    else:
        d.t(x + 12, LY[0] + 68, "통과 0", 13, SOFT, KR, "start")

# 누출 버킷 레인: 큐 3 → 2 → 1 → 0
for i in range(N):
    x = X0 + STRIDE * i
    if i == 0:
        for k in range(3):
            sq(x + 12 + 26 * k, LY[1] + 16, INFO)
        d.t(x + 12, LY[1] + 68, "큐 3", 13, INFO, KR, "start", 600)
        d.t(x + 12, LY[1] + 92, "버림 2", 13, BAD, KR, "start", 600)
    else:
        sq(x + 12, LY[1] + 16, OK)
        d.t(x + 12, LY[1] + 68, "통과 1", 13, OK, KR, "start", 600)
        d.t(x + 12, LY[1] + 92, f"큐 {3 - i}", 13, INFO, KR, "start")

d.legend(H - 56, [("통과", OK), ("버림", BAD), ("큐 대기", INFO), ("평탄한 출력", ACC)])
d.save("04-01.leaky-vs-token.svg")
