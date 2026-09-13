# 09-03 §3·§4 — overcommit 세 정책이 같은 요청에 다르게 답한다. 본문 실증 두 케이스를 같은 줄에 놓았다.
# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가. 행은 판단 축, 열은 정책 값.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 672
LX, LW = 24, 224
CW, GAP = 224, 12
C0 = LX + LW + 16
HY, RH, RS = 116, 44, 52

COLS = [("0  GUESS", "기본값"), ("1  ALWAYS", "항상 허용"), ("2  NEVER", "strict accounting")]
CX = [C0 + j * (CW + GAP) for j in range(3)]

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-03 §3·§4",
       "얼마나 봐 줄지를 값 하나가 정합니다",
       "리눅스는 메모리를 어느 정도 의도적으로 over-commit 한다. vm.overcommit_memory 값에 따라 같은 요청이 통과하거나 거절되고, 거절되는 자리도 다르다. 0 은 커널이 나중에 OOM killer 로 수습하고, 2 는 malloc 단계에서 미리 막는다.",
       "값 2 로 끄면 가용 메모리가 급감해 GUI 로그인조차 안 될 수 있습니다")

d.box(LX, HY, LW, RH, PAPER2, RULE, 0.9)
d.t(LX + LW / 2, HY + 27, "vm.overcommit_memory", 12, SOFT, MONO)
for j, (name, sub) in enumerate(COLS):
    focal = j == 0
    if focal:
        d.tone(CX[j], HY, CW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(CX[j], HY, CW, RH, PAPER2, RULE, 0.9)
    d.t(CX[j] + CW / 2, HY + 20, name, 12, ACC if focal else INK, MONO, "middle", 600)
    d.t(CX[j] + CW / 2, HY + 37, sub, 13, ACC if focal else MUTED, KR)

ROWS = [
    ("판단 기준", [("RAM + swap 휴리스틱", MUTED), ("판단하지 않습니다", MUTED), ("CommitLimit", MUTED)]),
    ("단일 대형 요청", [("거절합니다", WARN), ("통과시킵니다", OK), ("거절합니다", WARN)]),
    ("작은 요청 수만 건", [("통과시킵니다", OK), ("통과시킵니다", OK), ("한도에서 막습니다", WARN)]),
    ("모자랄 때 어디서 실패하나", [("나중에 OOM killer", BAD), ("나중에 OOM killer", BAD), ("지금 malloc 이", WARN)]),
    ("본문 실증 결과", [("약 1,758MB 쓰고 Killed", BAD), ("—", MUTED), ("약 820MB 에서 malloc 실패", WARN)]),
]

for i, (axis, cells) in enumerate(ROWS):
    y = HY + RH + 8 + i * RS
    d.box(LX, y, LW, RH, PAPER2, RULE, 0.9)
    d.t(LX + 16, y + 27, axis, 13, INK, KR, "start")
    for j, (txt, c) in enumerate(cells):
        if c is MUTED:
            d.box(CX[j], y, CW, RH, PAPER2, RULE, 0.9)
            d.t(CX[j] + CW / 2, y + 27, txt, 13, SOFT, KR)
        else:
            d.tone(CX[j], y, CW, RH, c, 6, "18", 1.1)
            d.t(CX[j] + CW / 2, y + 27, txt, 13, c, KR)

BOT = HY + RH + 8 + len(ROWS) * RS
d.t(LX, BOT + 30, "값 2 의 한도는 (전체 RAM − huge TLB) × overcommit_ratio/100 + swap 입니다. ratio 기본값은 50 입니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 54, "820MB 가 1GB 한도보다 작은 이유는 코드가 root 프로세스용 예비 메모리를 남기기 때문입니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 78, "확인은 /proc/meminfo 의 CommitLimit 과 Committed_AS 로 합니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("통과", OK), ("거절 · 제약", WARN), ("사후 수습", BAD), ("기본값", ACC)])
d.save("09-03.overcommit-policies.svg")
print("ok 09-03.overcommit-policies")
