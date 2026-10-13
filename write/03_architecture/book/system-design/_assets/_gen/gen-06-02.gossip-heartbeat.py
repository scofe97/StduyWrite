# 타입 스펙: type-architecture — s0 의 멤버십 목록(표)과 그 표에서 s2 한 줄이 정체를 드러내 다운 표시로 이어지는 네 단계를 한 화면에 둔다.
# 사실 출처: 추출본 v2.txt 1767~1787행(멤버십 목록·하트비트 카운터·무작위 노드로 전송·다른 노드가 확인하면 다운 표시),
#   PDF 100쪽 그림의 s0 멤버십 목록(0: 10232 · 12:00:01 / 1: 10224 · 12:00:10 / 2: 9908 · 11:58:02 / 3: 10237 · 12:00:20 / 4: 10234 · 12:00:34).
#   12:00:34 − 11:58:02 = 2분 32초.
# Layout conventions: 표 x=24~424(열 x=40·160·320), 헤더 y=124·행 stride 44(y=164~340). 단계 상자 x=520·폭 416·높이 72, stride 108(y=124·232·340·448). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 616
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 06-02 §2",
      "카운터 하나가 멈추면 목록의 한 줄이 먼저 드러난다",
      "노드마다 하트비트 카운터를 올려 무작위 이웃에 퍼뜨리고, 한 줄만 오르지 않으면 다른 노드에 물어 다운으로 표시한다.",
      "s0 의 목록에서 s2 만 9908 에 머물러 있다")

# 표
d.t(24, 116, "s0 의 멤버십 목록", 13, MUTED, KR, "start", 600)
TX, TW = 24, 400
d.box(TX, 124, TW, 36, PAPER2, RULE, 0.9, 4)
for x, txt in ((40, "멤버 ID"), (160, "하트비트 카운터"), (320, "시각")):
    d.t(x, 147, txt, 13, MUTED, KR, "start", 600)
ROWS = (("s0", "10232", "12:00:01"), ("s1", "10224", "12:00:10"),
        ("s2", "9908", "11:58:02"), ("s3", "10237", "12:00:20"), ("s4", "10234", "12:00:34"))
for k, (sid, cnt, tm) in enumerate(ROWS):
    y = 164 + 44 * k
    if sid == "s2":
        d.tone(TX, y, TW, 44, ACC, 4, "12", 1.4)
        c = ACC
    else:
        d.box(TX, y, TW, 44, PAPER2, RULE, 0.9, 4)
        c = INK
    d.t(40, y + 28, sid, 14, c, MONO, "start", 600)
    d.t(160, y + 28, cnt, 14, c, MONO, "start")
    d.t(320, y + 28, tm, 14, c, MONO, "start")

d.chip(224, 420, "12:00:34 − 11:58:02 = 2분 32초", WARN, 12)

# 단계 상자
STEPS = (
    ("하트비트 증가", "자기 카운터 +1 → 무작위 노드로 전송", MUTED),
    ("정체 발견", "s2 · 9908 · 11:58:02", ACC),
    ("다른 노드에 확인", "s2 정보를 실어 s1 · s3 에 전송", INFO),
    ("다운 표시와 전파", "s2 DOWN", WARN),
)
BX, BW, BH = 520, 416, 72
YS = (124, 232, 340, 448)
for k in range(3):
    d.arrow([(BX + BW // 2, YS[k] + BH + 2), (BX + BW // 2, YS[k + 1] - 6)], MUTED, "ar", 1.5)
d.arrow([(426, 274), (BX - 6, 274)], ACC, "acc", 1.8)
for (title, sub, c), y in zip(STEPS, YS):
    if c == MUTED:
        d.box(BX, y, BW, BH, PAPER2, MUTED, 1.2, 6)
    else:
        d.tone(BX, y, BW, BH, c, 6, "12", 1.4 if c == ACC else 1.2)
    d.t(BX + 16, y + 30, title, 15, INK, KR, "start", 600)
    d.t(BX + 16, y + 56, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "start")

d.legend(H - 56, [("정체한 줄", ACC), ("다운 판정", WARN), ("확인 단계", INFO)])
d.save("06-02.gossip-heartbeat.svg")
