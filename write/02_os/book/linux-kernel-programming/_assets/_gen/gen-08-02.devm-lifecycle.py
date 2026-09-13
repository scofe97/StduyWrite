# 08-02 §7 — devm_ 로 받은 메모리는 언제 자동으로 풀리고, 어디서 쓰면 어긋나는가.
# 본문이 요구한 형태: "드라이버 detach 시(또는 모듈 제거 시) 자동으로 버퍼를 해제한다" + "init·probe() 에서만 쓰도록 설계됐다".
# 타입 스펙: type-state — 주체 하나(드라이버가 쥔 버퍼)의 상태 전이와 가드. 아래 갈래가 가드를 어긴 경로다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 568
SW, SH, SY = 208, 76, 168
SX = [24, 272, 520, 768]
LX = [x + SW / 2 for x in SX]

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-02 §7",
       "probe 에서 받으면 detach 에서 풀립니다",
       "devm_kmalloc·devm_kzalloc 으로 받은 버퍼는 커널의 resource management 프레임워크가 드라이버 detach 또는 모듈 제거 시점에 자동으로 해제한다. 개발자가 해제 코드를 쓰지 않아도 되므로 에러 경로의 누수가 사라진다. 다만 그 자동 해제 시점은 probe 에 묶여 있다.",
       "자동 해제 시점이 probe 에 묶여 있어, probe 밖에서 쓰면 의도와 어긋납니다")

STATES = [
    ("probe() 진입", "devres 가 추적을 시작합니다", OK),
    ("버퍼 보유", "드라이버가 장치를 다루는 동안", OK),
    ("detach · 모듈 제거", "프레임워크가 신호를 받습니다", WARN),
    ("자동 해제", "해제 코드를 쓸 일이 없습니다", OK),
]

for i, (name, sub, c) in enumerate(STATES):
    focal = i == 3
    if focal:
        d.tone(SX[i], SY, SW, SH, ACC, 8, "12", 1.4)
    else:
        d.tone(SX[i], SY, SW, SH, c, 8, "14", 1.1)
    d.t(SX[i] + SW / 2, SY + 32, name, 13, ACC if focal else c, KR, "middle", 600)
    d.t(SX[i] + SW / 2, SY + 54, sub, 13, MUTED, KR)
    if i < 3:
        d.arrow([(SX[i] + SW + 4, SY + SH / 2), (SX[i + 1] - 6, SY + SH / 2)],
                ACC if i == 2 else MUTED, "acc" if i == 2 else "ar", 1.4)

d.chip(LX[0] + 124, SY + SH / 2 - 26, "devm_kzalloc()", OK, 13)
d.chip(LX[2] + 124, SY + SH / 2 - 26, "자동", ACC, 13)

# 가드를 어긴 경로 — probe 밖에서 쓴 경우
GY = 344
d.tone(SX[1], GY, SW * 2 + 64, SH, BAD, 8, "12", 1.4)
d.t(SX[1] + 20, GY + 32, "probe 밖에서 devm_ 을 쓴 경우", 13, BAD, KR, "start", 600)
d.t(SX[1] + 20, GY + 54, "해제 시점이 여전히 detach 라, 필요한 시점에 안 풀립니다", 13, MUTED, KR, "start")
d.path(f"M {LX[0]} {SY + SH} L {LX[0]} {GY + SH / 2} L {SX[1] - 6} {GY + SH / 2}", BAD, 1.4, m="bad", dash="5 5")
d.chip(LX[0], GY - 16, "가드 위반", BAD, 13)

d.t(24, 468, "devm_kfree() 로 손수 해제할 수는 있습니다. 다만 그렇게 해야 한다면 애초에 managed API 가 잘못된 선택이라는 신호입니다.", 13, MUTED, KR, "start")
d.t(24, 492, "managed API 는 GPL 라이선스 모듈에만 export 됩니다. devm_kzalloc() 은 devm_kmalloc() 의 얇은 래퍼입니다.", 13, SOFT, KR, "start")

d.legend(H - 40, [("정상 경로", OK), ("전이 시점", WARN), ("자동 해제 — 이 절의 논점", ACC), ("가드 위반", BAD)])
d.save("08-02.devm-lifecycle.svg")
print("ok 08-02.devm-lifecycle")
