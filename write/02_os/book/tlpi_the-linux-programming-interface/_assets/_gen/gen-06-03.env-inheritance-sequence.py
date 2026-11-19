# 06-03 §3 환경 목록의 상속 — 부모가 환경을 정하고 자식을 만든 뒤, 두 프로세스가 각자 값을 고쳐도 서로 보이지 않는 순서.
# 근거: TLPI 6.7 「When a new process is created, it inherits a copy of its parent's environment.」
#      「this transfer of information is one-way and once-only. After the child process has been created, either process may change its own environment, and these changes are not seen by the other process.」
# 값 근거: TARGET 과 alpha·beta·gamma 는 순서를 보이려고 고른 예시 값이다. 실행해서 얻은 값이 아니다.
# 타입 스펙: type-sequence — 참여자 둘(부모 · 자식)의 시간순 사건. 복사는 메시지 하나, 각자의 수정은 레인 옆 자기 호출로 보인다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, WARN, KR, MONO

W, H = 880, 520
s = Seq(W, H, "TLPI · 06-03 §3",
        "자식은 생성 때 환경의 사본을 받고 그 뒤 두 환경은 따로 논다",
        "부모가 TARGET=alpha 를 정한 뒤 fork() 로 자식을 만들면 자식에게 사본이 한 번 전달된다. 이후 부모가 gamma 로, 자식이 beta 로 바꿔도 서로 보이지 않는다.",
        "TARGET 의 값이 시점마다 어떻게 갈라지는지를 보입니다.")

LX = s.lanes([
    ("부모 프로세스", "parent"),
    ("자식 프로세스", "child"),
], y0=104, lane_w=240)
s.rails(470)

s.selfmsg("부모 프로세스", "TARGET=alpha 를 환경에 등록", 186, INFO)
s.state("부모 프로세스", "TARGET=alpha", 222, INFO)

s.msg("부모 프로세스", "자식 프로세스", "fork()", 268, ACC, "acc", None, "자식 생성 · 환경 사본을 한 번 전달")
s.state("자식 프로세스", "TARGET=alpha (사본)", 304, ACC)

s.selfmsg("부모 프로세스", "TARGET=gamma 로 변경", 352, INFO)
s.state("부모 프로세스", "TARGET=gamma", 388, INFO)

cx = s.LX["자식 프로세스"]
s.path(f"M {cx-10} {352-10} L {cx-48} {352-10} L {cx-48} {352+10} L {cx-13} {352+10}", OK, 1.4, m="ok")
s.t(cx - 56, 352 - 4, "TARGET=beta 로 변경", 11, OK, MONO, "end")
s.state("자식 프로세스", "TARGET=beta", 388, OK)

s.t(440, 440, "서로의 변경은 상대 환경에 나타나지 않음", 12, MUTED, KR, "middle", 600)

s.legend(480, [("부모의 환경", INFO), ("복사 · 생성", ACC), ("자식의 환경", OK)])
s.save("06-03.env-inheritance-sequence.svg")
print("ok 06-03 env-inheritance-sequence")
