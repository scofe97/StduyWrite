# 06-03 절 지도 — 셸 명령 줄에서 argv 배열과 환경 목록이 생성되어 새 프로그램으로 전달되는 흐름
# 근거: TLPI 6.6, 6.7 (06.txt 557-1131 줄), execve(2) "Limits on size of arguments and environment"
#      "When the program is executed, the command-line arguments ... are made available via two arguments to main()"
#      "When a new process is created, it inherits a copy of its parent's environment"
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 460
d = D(W, H, "TLPI · 06-03 절 지도",
      "명령행 인자와 환경 목록의 전달 흐름",
      "셸이 파싱한 인자 배열과 부모의 환경 목록 사본이 execve 시스템 콜을 거쳐 새 프로세스의 main 진입점까지 전달되는 과정",
      "실제 인자 necho hello world 와 환경 변수 SHELL=/bin/bash 가 전달되는 데이터 흐름")

# 1. 왼쪽: 셸 명령 입력 및 파싱 (입력 단계)
SX, SY, SW, SH = 24, 104, 246, 280
d.box(SX, SY, SW, SH, PAPER2, RULE, 1.0, 6)
d.t(SX + SW / 2, SY + 24, "1. 셸 명령 입력 · 파싱", 14, INK, KR, "middle", 600)
d.t(SX + SW / 2, SY + 44, "$ necho hello world", 12, INFO, MONO)
d.line(SX + 12, SY + 56, SX + SW - 12, SY + 56, RULE, 0.8)

shell_rows = [
    ("명령 파싱", "공백 기준 3단어 분리"),
    ("argv[0]", "\"necho\" (프로그램 이름)"),
    ("argv[1]", "\"hello\" (첫째 인자)"),
    ("argv[2]", "\"world\" (둘째 인자)"),
    ("부모 환경", "SHELL=/bin/bash 외")
]
for i, (head, val) in enumerate(shell_rows):
    iy = SY + 72 + i * 33
    d.box(SX + 12, iy - 11, SW - 24, 26, PAPER, RULE, 0.8, 4)
    d.t(SX + 22, iy + 6, head, 11, SOFT, MONO if "[" in head else KR, "start", 500)
    d.t(SX + SW - 20, iy + 6, val, 11, INK, MONO if '"' in val or '=' in val or '/' in val else KR, "end")

# 2. 중앙: 커널 execve 전달 및 스택 적재 (전달 단계)
KX, KY, KW, KH = 316, 104, 248, 280
d.tone(KX, KY, KW, KH, ACC, 6, "12", 1.2)
d.t(KX + KW / 2, KY + 24, "2. execve 시스템 콜 · 적재", 14, INK, KR, "middle", 600)
d.t(KX + KW / 2, KY + 44, "execve(path, argv, envp)", 12, ACC, MONO)
d.line(KX + 12, KY + 56, KX + KW - 12, KY + 56, RULE, 0.8)

kernel_rows = [
    ("상한 점검", "RLIMIT_STACK 의 1/4"),
    ("argc 산출", "인자 개수 3 기록"),
    ("argv 배열", "3개 포인터 + NULL"),
    ("envp 배열", "환경 포인터 + NULL"),
    ("문자열 복사", "인자·NAME=value"),
    ("적재 위치", "스택 바로 위 영역")
]
for i, (head, val) in enumerate(kernel_rows):
    iy = KY + 72 + i * 33
    d.box(KX + 12, iy - 11, KW - 24, 26, PAPER, RULE, 0.8, 4)
    d.t(KX + 22, iy + 6, head, 11, ACC, KR, "start", 500)
    d.t(KX + KW - 20, iy + 6, val, 11, INK, KR, "end")

# 3. 오른쪽: C 프로그램 실행 진입점 (수신 및 조작 단계)
PX, PY, PW, PH = 610, 104, 246, 280
d.box(PX, PY, PW, PH, PAPER2, RULE, 1.0, 6)
d.t(PX + PW / 2, PY + 24, "3. C 런타임 및 main 진입", 14, INK, KR, "middle", 600)
d.t(PX + PW / 2, PY + 44, "main(argc, argv)", 12, OK, MONO)
d.line(PX + 12, PY + 56, PX + PW - 12, PY + 56, RULE, 0.8)

prog_rows = [
    ("인자 순회", "argv[0]~argv[2] 확인"),
    ("전역 변수", "extern char **environ"),
    ("단건 조회", "getenv(\"SHELL\")"),
    ("안전 등록", "setenv(\"GREET\", \"hi\", 1)"),
    ("포인터 편입", "putenv(str) 주의"),
    ("외부 확인", "/proc/PID/cmdline")
]
for i, (head, val) in enumerate(prog_rows):
    iy = PY + 72 + i * 33
    d.box(PX + 12, iy - 11, PW - 24, 26, PAPER, RULE, 0.8, 4)
    d.t(PX + 22, iy + 6, head, 11, OK, KR, "start", 500)
    d.t(PX + PW - 20, iy + 6, val, 10, INK, MONO if '(' in val or '/' in val or '*' in val else KR, "end")

# 화살표 연결 (셸 → 커널)
d.arrow([(SX + SW + 4, SY + 80), (KX - 6, KY + 80)], ACC, "acc", 1.4)
d.t((SX + SW + KX) / 2, SY + 70, "호출", 11, ACC, KR)

d.arrow([(SX + SW + 4, SY + 190), (KX - 6, KY + 190)], MUTED, "ar", 1.2)
d.t((SX + SW + KX) / 2, SY + 180, "복사", 11, MUTED, KR)

# 화살표 연결 (커널 → C 프로그램)
d.arrow([(KX + KW + 4, KY + 80), (PX - 6, PY + 80)], OK, "ok", 1.4)
d.t((KX + KW + PX) / 2, KY + 70, "진입", 11, OK, KR)

d.arrow([(KX + KW + 4, KY + 190), (PX - 6, PY + 190)], MUTED, "ar", 1.2)
d.t((KX + KW + PX) / 2, KY + 180, "전달", 11, MUTED, KR)

d.legend(410, [("셸 파싱 및 입력", INFO), ("커널 전달 및 스택 적재", ACC), ("C 프로그램 수신 및 조작", OK)])
d.save("06-03.chapter-overview.svg")
print("ok 06-03.chapter-overview.svg")
