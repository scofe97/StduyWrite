# 06-01 §1 프로그램과 프로세스의 구분 — 디스크 파일 하나에서 독립된 프로세스 둘이 뜨는 구조
# 근거: TLPI 6.1 (06.txt 13-79 줄)
#      "a process is an abstract entity, defined by the kernel, to which system resources are allocated in order to execute a program"
#      "A program is a file containing a range of information that describes how to construct a process at run time."
#      "One program may be used to construct many processes"
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 440
d = D(W, H, "TLPI · 06-01 §1",
      "프로그램 파일 하나에서 독립된 프로세스 둘이 뜨는 구조",
      "디스크의 실행 파일은 정적 명세이고, 프로세스는 커널이 PID와 독립된 주소 공간 및 자원을 부여한 동적 실체입니다.",
      "디스크 파일 /usr/bin/myprog 을 두 번 실행해 fork 로 PID 1042 와 PID 1043 이 생기고 execve 로 같은 프로그램이 적재되는 과정")

# 1. 왼쪽: 디스크의 프로그램 파일 (정적 명세)
DX, DY, DW, DH = 24, 104, 260, 260
d.box(DX, DY, DW, DH, PAPER2, RULE, 1.0, 6)
d.t(DX + DW / 2, DY + 26, "디스크 파일 (정적 명세)", 14, INK, KR, "middle", 600)
d.t(DX + DW / 2, DY + 46, "/usr/bin/myprog (ELF)", 12, INFO, MONO)
d.line(DX + 12, DY + 58, DX + DW - 12, DY + 58, RULE, 0.8)

file_items = [
    ("ELF 바이너리 헤더", "형식 식별 메타정보"),
    ("기계어 인스트럭션", "알고리즘 구현 (.text)"),
    ("진입점 주소", "시작 위치 (0x00401000)"),
    ("초기화 데이터·상수", "변수 초기값·리터럴"),
    ("심볼·재배치 테이블", "함수·변수 주소 해석"),
    ("공유 라이브러리 정보", "라이브러리·링커 경로")
]
for i, (head, sub) in enumerate(file_items):
    iy = DY + 76 + i * 29
    d.box(DX + 10, iy - 12, DW - 20, 25, PAPER, RULE, 0.8, 4)
    d.t(DX + 18, iy + 4, head, 11, INK, KR, "start", 500)
    d.t(DX + DW - 18, iy + 4, sub, 11, MUTED, KR, "end")

# 2. 가운데: fork() 로 PID 를 받고 execve() 로 적재
CX = 396
BOX_W, BOX_H = 104, 56
d.arrow([(DX + DW + 6, DY + DH / 2), (CX - BOX_W / 2 - 4, DY + DH / 2)], MUTED, "ar", 1.4)
d.box(CX - BOX_W / 2, DY + DH / 2 - BOX_H / 2, BOX_W, BOX_H, PAPER2, RULE, 1.0, 6)
d.t(CX, DY + DH / 2 - 8, "fork · execve", 12, INK, KR, "middle", 600)
d.t(CX, DY + DH / 2 + 12, "PID 부여·적재", 11, MUTED, KR)

# 분기 화살표 (직교 경로)
P1_Y = 104
P2_Y = 244
PW, PH = 320, 120
PX = 536

# CX -> P1
d.path(f"M {CX + BOX_W / 2 + 4} {DY + DH / 2 - 12} H {PX - 36} Q {PX - 20} {DY + DH / 2 - 12} {PX - 20} {DY + DH / 2 - 28} V {P1_Y + PH / 2 + 16} Q {PX - 20} {P1_Y + PH / 2} {PX - 8} {P1_Y + PH / 2}",
       ACC, 1.4, m="acc")
d.t(PX - 56, P1_Y + PH / 2 + 20, "1차 실행", 11, ACC, KR, "end")

# CX -> P2
d.path(f"M {CX + BOX_W / 2 + 4} {DY + DH / 2 + 12} H {PX - 36} Q {PX - 20} {DY + DH / 2 + 12} {PX - 20} {DY + DH / 2 + 28} V {P2_Y + PH / 2 - 16} Q {PX - 20} {P2_Y + PH / 2} {PX - 8} {P2_Y + PH / 2}",
       INFO, 1.4, m="info")
d.t(PX - 56, P2_Y + PH / 2 - 12, "2차 실행", 11, INFO, KR, "end")

# 3. 오른쪽: 프로세스 1 (PID 1042)
d.tone(PX, P1_Y, PW, PH, ACC, 6, "18", 1.4)
d.t(PX + 16, P1_Y + 24, "프로세스 1 (동적 실체)", 13, INK, KR, "start", 600)
d.chip(PX + PW - 56, P1_Y + 22, "PID 1042", ACC, 11)
d.line(PX + 12, P1_Y + 38, PX + PW - 12, P1_Y + 38, RULE, 0.8)
d.t(PX + 16, P1_Y + 58, "가상 메모리", 11, MUTED, KR, "start")
d.t(PX + 88, P1_Y + 58, "Text(공유) · Data·Heap·Stack(독립)", 11, INK, MONO, "start")
d.t(PX + 16, P1_Y + 80, "커널 구조체", 11, MUTED, KR, "start")
d.t(PX + 88, P1_Y + 80, "task_struct · 가상 메모리 테이블", 11, INK, MONO, "start")
d.t(PX + 16, P1_Y + 102, "할당된 자원", 11, MUTED, KR, "start")
d.t(PX + 88, P1_Y + 102, "FD 테이블 (0,1,2) · CWD · 시그널", 11, INK, MONO, "start")

# 4. 오른쪽: 프로세스 2 (PID 1043)
d.tone(PX, P2_Y, PW, PH, INFO, 6, "18", 1.4)
d.t(PX + 16, P2_Y + 24, "프로세스 2 (동적 실체)", 13, INK, KR, "start", 600)
d.chip(PX + PW - 56, P2_Y + 22, "PID 1043", INFO, 11)
d.line(PX + 12, P2_Y + 38, PX + PW - 12, P2_Y + 38, RULE, 0.8)
d.t(PX + 16, P2_Y + 58, "가상 메모리", 11, MUTED, KR, "start")
d.t(PX + 88, P2_Y + 58, "Text(공유) · Data·Heap·Stack(독립)", 11, INK, MONO, "start")
d.t(PX + 16, P2_Y + 80, "커널 구조체", 11, MUTED, KR, "start")
d.t(PX + 88, P2_Y + 80, "task_struct · 가상 메모리 테이블", 11, INK, MONO, "start")
d.t(PX + 16, P2_Y + 102, "할당된 자원", 11, MUTED, KR, "start")
d.t(PX + 88, P2_Y + 102, "FD 테이블 (0,1,2) · CWD · 시그널", 11, INK, MONO, "start")

d.legend(390, [("정적 명세 (디스크)", MUTED), ("1차 인스턴스 (PID 1042)", ACC), ("2차 인스턴스 (PID 1043)", INFO)])
out = "06-01.program-vs-process.svg"
d.save(out)
print("ok", out)
