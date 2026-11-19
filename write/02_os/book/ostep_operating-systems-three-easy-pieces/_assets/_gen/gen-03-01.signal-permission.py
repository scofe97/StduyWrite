# 03-01 「시그널」 — 일반 사용자는 대개 자기 프로세스에만 시그널을 보낼 수 있고 슈퍼유저는 대개 다른 사용자의 프로세스에도 보낼 수 있다.
# 본문 근거: 이 노트 「5. 시그널과 사용자로 프로세스 제어하기」 — 사용자와 슈퍼유저.
# 값 근거: 개념 도식이라 값은 없다.
# 공식 근거: OSTEP 5장 §5.5·5.6 — 일반 사용자는 대개 자기 프로세스만 통제하고, 슈퍼유저는(Linux 에서는 CAP_KILL 이 근거, kill(2)) 시스템을 악용하는 프로세스를 그 프로세스를 띄우지 않았더라도 죽일 수 있다.
# 타입 스펙: type-dp-security-matrix — 행은 시그널을 보내는 쪽, 열은 받는 프로세스의 주인. 칸마다 허용 여부.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 920, 460
d = D(W, H, "OSTEP · 03-01 §5",
      "시그널은 누가 보내느냐에 따라 닿는 프로세스가 갈린다",
      "일반 사용자는 자기 프로세스에는 시그널을 보낼 수 있지만 다른 사용자의 프로세스에는 대개 보낼 수 없다. "
      "슈퍼유저는 자기 프로세스에는 시그널을 보낼 수 있고 다른 사용자의 프로세스에도 대개 보낼 수 있다.",
      lead="일반 사용자는 대개 자기 프로세스만 통제합니다.")

RX, CX1, CX2, CW, CH = 24, 220, 540, 300, 100
Y_H, Y1, Y2 = 108, 156, 276

d.t(CX1 + CW / 2, Y_H + 22, "자기 프로세스", 13, INK, KR, "middle", 600)
d.t(CX2 + CW / 2, Y_H + 22, "다른 사용자의 프로세스", 13, INK, KR, "middle", 600)
for y, nm in ((Y1, "일반 사용자"), (Y2, "슈퍼유저")):
    d.box(RX, y, 180, CH, PAPER2, RULE, 1.0)
    d.t(RX + 90, y + 56, nm, 13, INK, KR, "middle", 600)

cells = [(Y1, CX1, "보낼 수 있음", OK), (Y1, CX2, "대개 보낼 수 없음", BAD),
         (Y2, CX1, "보낼 수 있음", OK), (Y2, CX2, "대개 보낼 수 있음", WARN)]
for y, x, txt, c in cells:
    d.tone(x, y, CW, CH, c, 6, "14", 1.2)
    d.t(x + CW / 2, y + 40, txt, 14, c, KR, "middle", 600)
    d.t(x + CW / 2, y + 66, "kill() 로 SIGINT 등", 11, MUTED, KR)

d.legend(H - 40, [("보낼 수 있음", OK), ("대개 보낼 수 있음", WARN), ("대개 보낼 수 없음", BAD)])
d.save("03-01.signal-permission.svg")
print("ok 03-01 signal-permission")
