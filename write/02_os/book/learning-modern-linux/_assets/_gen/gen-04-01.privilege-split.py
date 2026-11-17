# 04-01 §6 — root 의 특권을 capability 단위로 나누고, 웹 서버에는 한 단위만 준다.
# 근거: capabilities(7) "Privileged processes bypass all kernel permission checks",
#       "Starting with Linux 2.2, Linux divides the privileges traditionally associated with superuser
#       into distinct units, known as capabilities", 각 단위의 뜻은 같은 매뉴얼의 목록
#       (CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_KILL, CAP_NET_BIND_SERVICE "port numbers less than 1024",
#       CAP_SYS_MODULE, CAP_SYS_ADMIN).
# 타입 스펙: type-tree — 뿌리 하나(root 의 특권)에서 잎(단위)으로 갈라지는 계층.
#           accent 는 웹 서버가 받는 잎 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING MODERN LINUX · 04-01 §6",
      "root 의 특권을 capability 단위로 나눈다",
      "리눅스 2.2부터 슈퍼유저의 특권은 따로 켜고 끌 수 있는 단위로 나뉜다. "
      "80 포트를 여는 웹 서버에는 그중 한 단위만 있으면 된다.",
      "프로세스에는 필요한 단위만 줍니다")

leaves = [
    ("CAP_CHOWN", "파일 소유자 바꾸기"),
    ("CAP_DAC_OVERRIDE", "파일 권한 검사 우회"),
    ("CAP_KILL", "시그널 권한 검사 우회"),
    ("CAP_NET_BIND_SERVICE", "1024 미만 포트 열기"),
    ("CAP_SYS_MODULE", "커널 모듈 적재"),
    ("CAP_SYS_ADMIN", "마운트 같은 관리 작업"),
]
FOCAL = 3
LX, LW, LH, STRIDE, LY0 = 330, 300, 48, 56, 112
ly = lambda i: LY0 + i * STRIDE
mid = (ly(0) + ly(len(leaves) - 1) + LH) / 2

RX, RW, RH = 24, 240, 100
d.box(RX, mid - RH / 2, RW, RH, PAPER2, INFO, 1.2, 8)
d.t(RX + RW / 2, mid - 12, "root", 17, INFO, MONO, "middle", 600)
d.t(RX + RW / 2, mid + 12, "UID 0", 12, MUTED, MONO)
d.t(RX + RW / 2, mid + 32, "모든 권한 검사 통과", 12, MUTED, KR)

SPX = 296
d.line(RX + RW, mid, SPX, mid, MUTED, 1.3)
d.line(SPX, ly(0) + LH / 2, SPX, ly(len(leaves) - 1) + LH / 2, MUTED, 1.3)

for i, (cap, what) in enumerate(leaves):
    y = ly(i)
    focal = (i == FOCAL)
    d.arrow([(SPX, y + LH / 2), (LX - 2, y + LH / 2)], ACC if focal else MUTED,
            "acc" if focal else "ar", 1.3)
    if focal:
        d.tone(LX, y, LW, LH, ACC, r=6, sw=1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(LX + 16, y + 21, cap, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(LX + 16, y + 39, what, 12, MUTED, KR, "start")

WX, WW, WH = 690, 246, 100
fy = ly(FOCAL) + LH / 2
d.box(WX, fy - WH / 2, WW, WH, PAPER2, OK, 1.2, 8)
d.t(WX + WW / 2, fy - 12, "웹 서버 프로세스", 15, OK, KR, "middle", 600)
d.t(WX + WW / 2, fy + 12, "80 포트 열기", 12, MUTED, KR)
d.t(WX + WW / 2, fy + 32, "이 단위 하나만", 12, MUTED, KR)
d.arrow([(LX + LW, fy), (WX - 2, fy)], ACC, "acc", 1.4)

d.legend(472, [("슈퍼유저의 특권 전체", INFO), ("웹 서버에 필요한 한 단위", ACC), ("받는 프로세스", OK)])
d.save("04-01.privilege-split.svg")
print("ok 04-01.privilege-split")
