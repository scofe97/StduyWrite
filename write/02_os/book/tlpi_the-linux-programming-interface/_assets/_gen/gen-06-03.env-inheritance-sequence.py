# 06-03 §3 환경 변수의 상속과 단방향 전달 (one-way and once-only)
# 근거: TLPI 6.7 (06.txt 700-717 줄)
#      "When a new process is created, it inherits a copy of its parent's environment."
#      "Since the child gets a copy of its parent's environment at the time it is created, this transfer of information is one-way and once-only."
#      "After the child process has been created, either process may change its own environment, and these changes are not seen by the other process."
# 타입 스펙: type-sequence
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 460
s = Seq(W, H, "TLPI · 06-03 §3",
        "환경 목록의 상속과 단방향 전달 (one-way and once-only)",
        "자식 프로세스는 생성 시점에 부모의 환경 사본을 한 번만 복사받으며 이후 어느 쪽이 환경을 고쳐도 상대방에게 보이지 않습니다.",
        "부모 PID 1000 에서 TARGET=alpha 를 export 한 뒤 자식 PID 1001 이 값을 바꿔도 부모에 영향이 없는 흐름")

# 레인 설정 (부모 셸 vs 자식 프로세스)
LX = s.lanes([
    ("부모 프로세스", "PID 1000 · bash"),
    ("자식 프로세스", "PID 1001 · subshell / myprog")
], y0=104, lane_w=240)

# 레일 끝 y
Y_BOT = 390
s.rails(Y_BOT)

# 1. 부모 환경 변수 정의 및 export
s.selfmsg("부모 프로세스", "TARGET=alpha 설정 및 export", 170, INFO, "환경 목록에 TARGET=alpha 등록")
s.state("부모 프로세스", "TARGET=alpha", 200, INFO)

# 2. fork & exec 생성 호출
s.msg("부모 프로세스", "자식 프로세스", "fork() 시스템 콜 (환경 목록 복사)", 230, ACC, "acc", None, "부모 환경 사본 1회 전달")

# 3. 자식 시작 시점 상태
s.state("자식 프로세스", "TARGET=alpha (사본)", 260, ACC)

# 4. 자식 내부에서 환경 변수 수정 (레인 안쪽으로 루프 배치)
cx = s.LX["자식 프로세스"]
s.path(f"M {cx-10} {295-10} L {cx-48} {295-10} L {cx-48} {295+10} L {cx-13} {295+10}", OK, 1.4, m="ok")
s.t(cx - 56, 295 - 4, "TARGET=beta 수정 (setenv)", 11, OK, MONO, "end")
s.t(cx - 56, 295 + 13, "자식 메모리의 환경 목록만 갱신", 11, MUTED, KR, "end")
s.state("자식 프로세스", "TARGET=beta", 325, OK)

# 5. 자식 프로세스 종료
s.msg("자식 프로세스", "부모 프로세스", "exit(0) 종료 (자식 주소공간 소멸)", 350, MUTED, "ar", "3 3", "부모 환경에 전달되는 변경사항 없음")

# 6. 부모의 최종 상태 확인
s.state("부모 프로세스", "TARGET=alpha (불변)", 375, INFO)

s.legend(415, [("부모 환경 상태", INFO), ("복사 및 생성 전달", ACC), ("자식 독립 수정", OK)])
s.save("06-03.env-inheritance-sequence.svg")
print("ok 06-03.env-inheritance-sequence.svg")
