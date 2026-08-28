# 01-02.tls-key-lineage — 키는 만들어진 자리를 떠나지 않는다
# 본문 요구(01-02 §5 "세션 키의 계보"): 본문이 이 도식이 왜 따로 있는지를 먼저 적는다 —
#           "시간 순서로는 재료 셋이 하나로 모이는 장면이 보이지 않는다. 세로선을 따라 내려가는
#           그림에는 셋이 하나로 합쳐진다를 그릴 자리가 없기 때문"이다. 그래서 시퀀스에서 계보만
#           떼어 낸 장이고, 세 갈래가 한 칸으로 모이는 팬인이 이 그림의 존재 이유다.
#           그리고 "위 세 칸이 재료이고 각 칸의 아래 줄이 그 재료가 망을 어떻게 건넜는지"이며,
#           "master secret 과 세션 키에는 화살표가 들어오기만 하고 나가지 않는다"가 결론이다 —
#           아래 두 칸에서 나가는 선을 하나도 그리지 않은 것이 곧 그 주장이라, 선을 더하면
#           본문이 틀려진다.
# 타입 스펙: type-data-flow.md — 여럿이 하나로 몰리는 팬인. 위 셋은 망을 건너는 입력이고
#           아래 둘은 그 자리에서 만들어지는 산출이다. 칸 오른쪽 칩이 노출 상태를 맡는다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 980, 558
SRC_Y, SRC_W, SRC_H = 118, 286, 96
MID_X = 472.0                       # 아래 두 칸이 공유하는 세로 중심

d = D(W, H, "KEY LINEAGE · 01-02 TLS",
      "세션 키의 계보 — 키는 만들어진 자리를 떠나지 않는다",
      "TLS 1.2 세션 키의 계보. client random·server random·premaster secret 세 재료가 "
      "master secret 하나로 합쳐지고 거기서 세션 키가 나온다. 위 세 재료는 망을 건너지만 "
      "master secret과 세션 키에는 화살표가 들어오기만 하고 나가지 않는다.",
      lead="화살표가 들어오기만 하고 나가지 않는 칸이 곧 망을 건너지 않는 값입니다.")

d.t(12, 102, "재료 셋 — 망을 건넌다", 10, SOFT, MONO, "start")

# (x, 이름, 누가·무엇, 어떻게 건넜나, 색, 노출 칩, 합류점 x)
SRCS = [(12,  "client random",    "클라이언트 난수",   "평문으로 그냥 건넜다",   INFO, "노출", 332.0),
        (316, "server random",    "서버 난수",        "평문으로 그냥 건넜다",   INFO, "노출", MID_X),
        (620, "premaster secret", "클라이언트가 생성", "공개키로 봉해져 건넜다", ACC,  "봉인", 612.0)]

for x, name, who, how, c, seal, join in SRCS:
    cx = x + SRC_W / 2
    d.tone(x, SRC_Y, SRC_W, SRC_H, c, 6, "12", 1.2)
    d.t(cx, SRC_Y + 30, name, 13, c, MONO, "middle", 600)
    d.t(cx, SRC_Y + 52, who, 11, INK)
    d.t(cx, SRC_Y + 74, how, 10, MUTED)
    d.chip(x + 254, SRC_Y + 15, seal, c, 8)
    # 셋이 한 칸으로 모인다 — 합류점을 벌려 세 갈래가 각자 들어오는 것이 보이게
    d.arrow([(cx, SRC_Y + 98), (cx, 248), (join, 248), (join, 275)],
            c, "acc" if c is ACC else "info", 1.5)

DERIVED = [(192.0, 278, 560, OK,  "master secret", "셋이 합쳐진 값 — 양쪽이 각자 계산한다", 1.5, "14", 508),
           (242.0, 412, 460, ACC, "session key",   "실제 암·복호에 쓰는 키",              1.7, "16", 408)]

for i, (x, y, w, c, name, sub, sw, op, chip_dx) in enumerate(DERIVED):
    d.tone(x, y, w, 76, c, 6, op, sw)
    d.t(MID_X, y + 32, name, 15, c, MONO, "middle", 600)
    d.t(MID_X, y + 54, sub, 11, INK)
    d.chip(x + chip_dx, y + 14, "안 건넌다", c, 8)
    if i == 0:
        d.arrow([(MID_X, y + 78), (MID_X, 409)], c, "ok", 1.6)

d.t(W - 54, 320.0, "도청자가 위 셋을 다 주워도", 10, BAD, KR, "end")
d.t(W - 54, 336.0, "봉인 하나를 못 열면 여기 못 온다", 10, BAD, KR, "end")
d.legend(514, [("평문으로 건넘", INFO), ("공개키로 봉해져 건넘", ACC), ("망을 건너지 않음", OK)])
d.save("01-02.tls-key-lineage.svg")
print("ok tls-key-lineage")
