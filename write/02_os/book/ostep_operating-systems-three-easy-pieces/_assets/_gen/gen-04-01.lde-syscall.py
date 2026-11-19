# 04-01 「제한된 직접 실행 프로토콜」 — 부팅 때 trap table 등록부터 프로세스 시작, 시스템 콜, 프로세스 종료까지의 전 과정.
# 본문 근거: 이 노트 「2. 사용자 모드와 시스템 콜」.
# 값 근거: 개념 도식이라 값은 없다. 원서 그림 6.2 (Limited Direct Execution Protocol) 의 부팅·시작·시스템 콜·종료 네 구간을 시간순 한 장으로 합쳤다.
# 공식 근거: OSTEP 6장 §6.2 — 하드웨어는 trap 때 돌아올 곳을 저장하고 return-from-trap 때 복원한다(저장 방식은 CPU 마다 다르다. 책은 x86 의 일례로 커널 스택을 든다).
# 타입 스펙: type-sequence — 참여자 셋(프로그램 · 하드웨어 · 운영체제)의 시간순 메시지. 점선 경계로 네 구간을 가른다.
#
# 메시지 라벨(msg·selfmsg)은 dd.py 가 MONO 로 그리므로 ASCII 만 담고, 한글 설명은 sub 에 둔다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, RULE, KR, MONO, PAPER2

W, H = 920, 1712

d = Seq(W, H, "OSTEP · 04-01 LDE",
        "부팅 때 길을 깔아 두고 trap 과 return-from-trap 으로 제어를 넘긴다",
        "위쪽부터 부팅 때 trap table 등록, 프로세스 시작 때 return-from-trap 으로 main() 진입, "
        "실행 중 trap 과 return-from-trap 으로 시스템 콜 처리, "
        "종료 때 exit() trap 과 자원 정리까지 제한된 직접 실행 프로토콜의 네 구간을 한 시퀀스로 보여준다.",
        lead="부팅부터 프로세스 시작, 시스템 콜, 종료까지 이어지는 네 구간이다.")

d.lanes([("프로그램", "user mode"),
         ("하드웨어", "CPU"),
         ("운영체제", "kernel mode")], lane_w=200)
d.rails(1624)

px = d.LX["프로그램"]
hx = d.LX["하드웨어"]
ox = d.LX["운영체제"]

# ── 1. 부팅 때 ─────────────────────────────────────────────────────────────
d.t(36, 176, "부팅 때 — 커널 모드에서 한 번", 13, MUTED, KR, "start", 600)
d.msg("운영체제", "하드웨어", "initialize trap table", 224, INFO, mk="info", sub="특권 명령으로 핸들러 주소를 등록")
d.selfmsg("하드웨어", "remember handler address", 288, MUTED, sub="syscall 핸들러 주소를 기억")

d.line(24, 336, W - 48, 336, RULE, 0.8, "4 4")

# ── 2. 프로세스 시작 ─────────────────────────────────────────────────────────
d.t(36, 368, "프로세스 시작 — 첫 return-from-trap", 13, MUTED, KR, "start", 600)

# 운영체제: 프로세스 생성 및 준비 (Figure 6.2 의 5단계 준비)
bw = 216
bx = ox - bw / 2
d.box(bx, 396, bw, 144, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.t(ox, 416, "OS @ run · 프로세스 준비", 11, INFO, KR, "middle", 600)
d.line(bx + 12, 428, bx + bw - 12, 428, RULE, 0.6)
d.t(ox, 448, "Create entry for process list", 10, INK, MONO, "middle")
d.t(ox, 468, "Allocate memory for program", 10, INK, MONO, "middle")
d.t(ox, 488, "Load program into memory", 10, INK, MONO, "middle")
d.t(ox, 508, "Setup user stack with argv", 10, INK, MONO, "middle")
d.t(ox, 528, "Fill kernel stack with reg/PC", 10, INK, MONO, "middle")

d.msg("운영체제", "하드웨어", "return-from-trap", 580, INFO, mk="info", sub="특권 명령 · 사용자 모드로 전환 시작")
d.selfmsg("하드웨어", "restore regs", 636, MUTED, sub="사용자 모드로 전환 (방식은 CPU 마다)")
d.msg("하드웨어", "프로그램", "jump to main", 696, OK, mk="ok", sub="main() 주소로 점프")

d.state("프로그램", "Run main()", 748, OK)
d.t(px, 772, "프로그램 실행 시작", 11, MUTED, KR, "middle")

d.line(24, 804, W - 48, 804, RULE, 0.8, "4 4")

# ── 3. 실행 중 — 시스템 콜 한 번 ─────────────────────────────────────────────
d.t(36, 836, "실행 중 — 시스템 콜 한 번", 13, MUTED, KR, "start", 600)
d.msg("프로그램", "하드웨어", "Call system call · trap", 880, ACC, mk="acc", sub="시스템 콜 번호를 정해진 자리에 두고 실행")
d.selfmsg("하드웨어", "save regs", 936, MUTED, sub="저장 · 커널 모드로 (방식은 CPU 마다)")
d.msg("하드웨어", "운영체제", "jump to trap handler", 996, INFO, mk="info", sub="등록해 둔 주소로 이동")

# 운영체제 레인은 오른쪽 끝이라 selfmsg 라벨이 화면 밖으로 잘린다. 루프와 라벨을 레일 왼쪽에 그린다.
loop_y = 1044
d.path(f"M {ox - 10} {loop_y} L {ox - 58} {loop_y} L {ox - 58} {loop_y + 20} L {ox - 13} {loop_y + 20}", MUTED, 1.4, m="ar")
d.t(ox - 68, loop_y + 6, "Handle trap · do work", 11, MUTED, MONO, "end", 400)
d.t(ox - 68, loop_y + 23, "번호를 확인하고 실행", 11, MUTED, KR, "end")

d.msg("운영체제", "하드웨어", "return-from-trap", 1112, INFO, mk="info", sub="특권 명령")
d.selfmsg("하드웨어", "restore regs", 1168, MUTED, sub="사용자 모드로 복귀 (방식은 CPU 마다)")
d.msg("하드웨어", "프로그램", "jump to PC after trap", 1228, OK, mk="ok", sub="trap 다음 줄에서 이어 실행")
d.t(px, 1264, "...", 12, MUTED, MONO, "middle")

d.line(24, 1288, W - 48, 1288, RULE, 0.8, "4 4")

# ── 4. 프로세스 종료 ─────────────────────────────────────────────────────────
d.t(36, 1320, "프로세스 종료 — exit() trap 과 자원 정리", 13, MUTED, KR, "start", 600)

d.state("프로그램", "return from main", 1356, MUTED)
d.t(px, 1380, "main() 에서 stub 코드로 복귀", 11, MUTED, KR, "middle")

d.msg("프로그램", "하드웨어", "trap (via exit())", 1420, ACC, mk="acc", sub="stub 코드가 exit() 시스템 콜 호출")
d.msg("하드웨어", "운영체제", "jump to trap handler", 1476, INFO, mk="info", sub="종료 핸들러로 이동")

# 운영체제: 메모리 해제 및 목록 제거
d.box(bx, 1516, bw, 76, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.t(ox, 1536, "OS @ exit · 자원 정리", 11, INFO, KR, "middle", 600)
d.line(bx + 12, 1548, bx + bw - 12, 1548, RULE, 0.6)
d.t(ox, 1568, "Free memory of process", 10, INK, MONO, "middle")
d.t(ox, 1584, "Remove from process list", 10, INK, MONO, "middle")

# ── 범례 및 저장 ─────────────────────────────────────────────────────────────
d.legend(1664, [("커널 쪽 동작", INFO), ("trap 진입", ACC), ("하드웨어 처리", MUTED), ("복귀", OK)])
d.save("04-01.lde-syscall.svg")
print("ok 04-01 lde-syscall")
