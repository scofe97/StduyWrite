# 06-03 §1, §3 argv 및 environ 포인터 배열과 문자열의 메모리 구조 (Figure 6-4, Figure 6-5)
# 근거: TLPI 6.6, 6.7 (06.txt 580-588 줄 Figure 6-4, 773-780·803-813 줄 printenv 출력과 Figure 6-5)
#      Figure 6-4: Values of argc and argv for the command necho hello world
#      Figure 6-5: Example of process environment list data structures
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 500
d = D(W, H, "TLPI · 06-03 §1, §3",
      "argv 포인터 배열과 environ 환경 목록의 메모리 배치",
      "인자 목록(argv)과 환경 목록(environ)은 모두 NULL 포인터로 끝나는 포인터 배열이며 각 원소는 널 종료 문자열을 가리킵니다.",
      "원서 Figure 6-4 의 necho 인자 구조와 Figure 6-5 의 printenv 환경 변수 목록 구조")

# 1. 왼쪽: argv 포인터 배열과 인자 문자열 (Figure 6-4)
AX, AY, AW, AH = 24, 104, 400, 340
d.box(AX, AY, AW, AH, PAPER2, RULE, 1.0, 6)
d.t(AX + AW / 2, AY + 24, "인자 목록: argv 포인터 배열과 문자열", 13, INK, KR, "middle", 600)
d.t(AX + AW / 2, AY + 44, "명령: necho hello world (argc = 3)", 12, INFO, MONO)
d.line(AX + 12, AY + 56, AX + AW - 12, AY + 56, RULE, 0.8)

# argc 표시
d.box(AX + 20, AY + 68, 100, 30, PAPER, RULE, 0.8, 4)
d.t(AX + 70, AY + 82, "argc", 11, SOFT, MONO)
d.t(AX + 70, AY + 93, "3", 12, INFO, MONO, "middle", 600)

# argv 포인터 배열 상자들
argv_entries = [
    ("argv[0]", "포인터", "\"necho\\0\""),
    ("argv[1]", "포인터", "\"hello\\0\""),
    ("argv[2]", "포인터", "\"world\\0\""),
    ("argv[3]", "NULL", "종료 포인터")
]

APY = AY + 110
for i, (idx, ptype, target) in enumerate(argv_entries):
    py = APY + i * 42
    is_null = (ptype == "NULL")
    d.box(AX + 20, py, 110, 32, PAPER, ACC if not is_null else MUTED, 0.9, 4)
    d.t(AX + 30, py + 20, idx, 11, INK, MONO, "start", 600)
    d.t(AX + 115, py + 20, ptype, 10, ACC if not is_null else MUTED, MONO if is_null else KR, "end")
    
    sy = py
    if not is_null:
        d.box(AX + 200, sy, 180, 32, PAPER, OK, 0.9, 4)
        d.t(AX + 290, sy + 20, target, 12, OK, MONO, "middle", 600)
        d.arrow([(AX + 130, py + 16), (AX + 194, sy + 16)], ACC, "acc", 1.4)
    else:
        d.box(AX + 200, sy, 180, 32, PAPER, RULE, 0.8, 4)
        d.t(AX + 290, sy + 20, "(배열 끝: NULL 포인터)", 11, MUTED, KR, "middle")
        d.line(AX + 130, py + 16, AX + 194, sy + 16, MUTED, 1.0, "3 3")

# 2. 오른쪽: environ 포인터 배열과 환경 문자열 (Figure 6-5)
EX, EY, EW, EH = 456, 104, 400, 340
d.box(EX, EY, EW, EH, PAPER2, RULE, 1.0, 6)
d.t(EX + EW / 2, EY + 24, "환경 목록: environ 포인터 배열과 문자열", 13, INK, KR, "middle", 600)
d.t(EX + EW / 2, EY + 44, "전역 변수: extern char **environ", 12, ACC, MONO)
d.line(EX + 12, EY + 56, EX + EW - 12, EY + 56, RULE, 0.8)

# environ 헤더 슬롯
d.box(EX + 20, EY + 68, 110, 30, PAPER, RULE, 0.8, 4)
d.t(EX + 75, EY + 82, "environ", 11, SOFT, MONO)
d.t(EX + 75, EY + 93, "포인터", 11, ACC, KR, "middle")

env_entries = [
    ("environ[0]", "포인터", "LOGNAME=mtk\\0"),
    ("environ[1]", "포인터", "SHELL=/bin/bash\\0"),
    ("environ[2]", "포인터", "HOME=/home/mtk\\0"),
    ("environ[3]", "포인터", "PATH=/usr/local/bin:/usr/bin:/bin:.\\0"),
    ("environ[4]", "포인터", "TERM=xterm\\0"),
    ("environ[5]", "NULL", "종료 포인터")
]

EPY = EY + 110
for i, (idx, ptype, target) in enumerate(env_entries):
    py = EPY + i * 35
    is_null = (ptype == "NULL")
    d.box(EX + 20, py, 110, 27, PAPER, ACC if not is_null else MUTED, 0.9, 4)
    d.t(EX + 28, py + 17, idx, 10, INK, MONO, "start", 600)
    d.t(EX + 118, py + 17, ptype, 10, ACC if not is_null else MUTED, MONO if is_null else KR, "end")
    
    sy = py
    if not is_null:
        d.box(EX + 150, sy, 236, 27, PAPER, INFO, 0.9, 4)
        d.t(EX + 268, sy + 17, target, 10, INFO, MONO, "middle", 500)
        d.arrow([(EX + 130, py + 13), (EX + 144, sy + 13)], ACC, "acc", 1.4)
    else:
        d.box(EX + 150, sy, 236, 27, PAPER, RULE, 0.8, 4)
        d.t(EX + 268, sy + 17, "(배열 끝: NULL 포인터)", 10, MUTED, KR, "middle")
        d.line(EX + 130, py + 13, EX + 144, sy + 13, MUTED, 1.0, "3 3")

# 하단 공통 영역 설명 (프로세스 스택 상단 연속 메모리)
d.t(AX + AW / 2, AY + AH - 12, "인자 개수 argc와 argv[argc]==NULL 종료 보장", 11, MUTED, KR)
d.t(EX + EW / 2, EY + EH - 12, "원소 순서 미정렬 · 마지막 원소 NULL 포인터 종료", 11, MUTED, KR)

d.legend(456, [("포인터 슬롯", ACC), ("인자 문자열 (값)", OK), ("환경 변수 (name=value)", INFO)])
d.save("06-03.argv-environ-memory.svg")
print("ok 06-03.argv-environ-memory.svg")
