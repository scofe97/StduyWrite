# 06-01 §4 부모 프로세스와 프로세스 트리 — init(PID 1) 사슬과 고아 입양
# 근거: TLPI 6.2 (06.txt 132-156 줄)
#      "Each process has a parent—the process that created it. A process can find out the process ID of its parent using the getppid() system call."
#      "init, the ancestor of all processes. (This “family tree” can be viewed using the pstree(1) command.)"
#      "If a child process becomes orphaned because its “birth” parent terminates, then the child is adopted by the init process, and subsequent calls to getppid() in the child return 1"
#      "The parent of any process can be found by looking at the PPid field provided in the Linux-specific /proc/PID/status file."
# 타입 스펙: type-tree
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 450
d = D(W, H, "TLPI · 06-01 §4",
      "부모 프로세스 사슬과 부모 종료 시 init 입양 전후 비교",
      "프로세스는 init(PID 1)을 뿌리로 하는 트리를 이루며, 부모가 먼저 종료되면 자식은 가장 가까운 subreaper 조상에, 없으면 init에 입양됩니다.",
      "부모 생존 시 정상 사슬(getppid()=1200)과 부모 bash 종료 후 init 직속 입양(getppid()=1) 구조")

CARD_W, CARD_H = 404, 280
Y0 = 104

# 1. 왼쪽 카드: 부모 생존 시 정상 부모 사슬
L_X = 24
d.box(L_X, Y0, CARD_W, CARD_H, PAPER2, RULE, 1.0, 6)
d.t(L_X + 16, Y0 + 24, "정상 상태 · 직계 부모 사슬", 13, INK, KR, "start", 600)
d.line(L_X + 16, Y0 + 34, L_X + CARD_W - 16, Y0 + 34, RULE, 0.8)

# 왼쪽 트리 노드들 (수직 사슬)
LX = L_X + CARD_W / 2
NW, NH = 220, 46

# init (PID 1)
d.box(LX - NW / 2, Y0 + 44, NW, NH, PAPER, RULE, 1.0, 6)
d.t(LX, Y0 + 63, "init (PID 1)", 12, INK, MONO, "middle", 600)
d.t(LX, Y0 + 80, "PPID 0 · 전체 프로세스의 조상", 11, MUTED, KR)

# 화살표 1 -> sshd
d.arrow([(LX, Y0 + 44 + NH), (LX, Y0 + 102)], MUTED, "ar", 1.2)

# sshd (PID 840)
d.box(LX - NW / 2, Y0 + 104, NW, NH, PAPER, RULE, 1.0, 6)
d.t(LX, Y0 + 123, "sshd (PID 840)", 12, INK, MONO, "middle", 600)
d.t(LX, Y0 + 140, "PPid: 1 (init 의 직속 자식)", 11, MUTED, KR)

# 화살표 sshd -> bash
d.arrow([(LX, Y0 + 104 + NH), (LX, Y0 + 162)], MUTED, "ar", 1.2)

# bash (PID 1200) — focal ACC
d.tone(LX - NW / 2, Y0 + 164, NW, NH, ACC, 6, "15", 1.2)
d.t(LX, Y0 + 183, "bash (PID 1200)", 12, ACC, MONO, "middle", 600)
d.t(LX, Y0 + 200, "PPid: 840 (worker 의 부모)", 11, INK, KR)

# 화살표 bash -> worker
d.arrow([(LX, Y0 + 164 + NH), (LX, Y0 + 222)], ACC, "acc", 1.2)

# worker (PID 1250)
d.box(LX - NW / 2, Y0 + 224, NW, NH, PAPER, RULE, 1.0, 6)
d.t(LX, Y0 + 243, "worker (PID 1250)", 12, INK, MONO, "middle", 600)
d.t(LX, Y0 + 260, "getppid() → 1200 (PPid: 1200)", 11, OK, MONO)


# 2. 오른쪽 카드: 부모 종료 후 init 입양
R_X = 452
d.box(R_X, Y0, CARD_W, CARD_H, PAPER2, RULE, 1.0, 6)
d.t(R_X + 16, Y0 + 24, "부모 bash 종료 후 · init(PID 1) 입양", 13, INK, KR, "start", 600)
d.line(R_X + 16, Y0 + 34, R_X + CARD_W - 16, Y0 + 34, RULE, 0.8)

RX = R_X + CARD_W / 2
# init (PID 1)
d.tone(RX - NW / 2, Y0 + 44, NW, NH, ACC, 6, "18", 1.4)
d.t(RX, Y0 + 63, "init (PID 1)", 12, ACC, MONO, "middle", 600)
d.t(RX, Y0 + 80, "subreaper 가 없을 때 새 부모", 11, INK, KR)

# 자식 둘로 분기하는 직교 버스
BUS_Y = Y0 + 104
d.line(RX, Y0 + 44 + NH, RX, BUS_Y, ACC, 1.2)

# 좌측 sshd (PID 840)
SX = R_X + 100
SW = 160
d.line(SX, BUS_Y, RX, BUS_Y, RULE, 1.0)
d.arrow([(SX, BUS_Y), (SX, Y0 + 120)], MUTED, "ar", 1.2)
d.box(SX - SW / 2, Y0 + 122, SW, 44, PAPER, RULE, 1.0, 6)
d.t(SX, Y0 + 141, "sshd (PID 840)", 12, INK, MONO, "middle", 600)
d.t(SX, Y0 + 158, "PPid: 1 유지", 11, MUTED, KR)

# 우측 종료된 bash (PID 1200) — 점선 박스 및 해제 표시
BX = R_X + CARD_W - 100
BW = 160
d.line(RX, BUS_Y, BX, BUS_Y, RULE, 1.0, "3 3")
d.arrow([(BX, BUS_Y), (BX, Y0 + 120)], BAD, "bad", 1.2, "3 3")
d.box(BX - BW / 2, Y0 + 122, BW, 44, PAPER, BAD, 1.0, 6)
d.t(BX, Y0 + 141, "bash (1200) [종료]", 12, BAD, MONO, "middle", 600)
d.t(BX, Y0 + 158, "부모 프로세스 소멸", 11, BAD, KR)

# 끊어진 링크 표시 (bash -> worker)
d.path(f"M {BX} {Y0 + 166} V {Y0 + 200}", BAD, 1.2, dash="3 3")
d.t(BX + 12, Y0 + 188, "관계 끊김", 11, BAD, KR, "start")

# 입양 연결 화살표: init 버스에서 worker 로 직접 직교 연결
WX = RX
d.path(f"M {RX} {BUS_Y} V {Y0 + 218}", OK, 1.5, m="ok")
d.chip(RX - 68, Y0 + 192, "새 부모로 자동 입양", OK, 11)

# worker (PID 1250) [입양 완료]
WW = 230
d.tone(WX - WW / 2, Y0 + 224, WW, 48, OK, 6, "18", 1.4)
d.t(WX, Y0 + 244, "worker (PID 1250) [입양 완료]", 12, OK, MONO, "middle", 600)
d.t(WX, Y0 + 262, "getppid() → 1 (PPid: 1 로 갱신)", 11, INK, MONO)

d.legend(406, [("정상 프로세스", MUTED), ("입양 주체 (init)", ACC), ("종료된 부모", BAD), ("입양된 자식", OK)])
out = "06-01.process-tree-adoption.svg"
d.save(out)
print("ok", out)
