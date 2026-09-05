# 02-01 §6 — 명령 한 줄이 커널로 내려갔다 돌아오는 경로.
# 원문("syscalls"): "you and your programs don't usually invoke these syscalls directly but via what we
#       call the C standard library. The standard library provides wrapper functions and is available in
#       various implementations, such as glibc or musl." 래퍼는 "the repetitive low-level handling of the
#       execution of a syscall" 을 맡는다. 저자가 적은 세 걸음은 이렇다 —
#       (1) "the kernel uses a so-called syscall table, effectively an array of function pointers in
#           memory (stored in a variable called sys_call_table)", syscall.h 와 아키텍처별 파일에 정의된다.
#       (2) "With the system_call() function acting like a syscall multiplexer, it first saves the
#           hardware context on the stack, then performs checks (like if tracing is performed), and then
#           jumps to the function pointed to by the respective syscall number index in the sys_call_table."
#       (3) "After the syscall is completed with sysexit, the wrapper library restores the hardware
#           context, and the program execution resumes in user land."
#       그리고 "Notable in the previous steps is the switching between kernel mode and user land mode,
#       an operation that costs time" 라고 못 박는다.
# 타입 스펙: type-data-flow — 존 셋 사이로 데이터가 건너간다(호출 번호와 인자, 그리고 하드웨어 컨텍스트).
#           accent 는 저자가 비용이라 지목한 한 줄.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 02-01 §6",
      "명령 한 줄이 커널로 내려갔다 돌아오는 길",
      "원서가 적은 세 걸음을 존 셋으로 갈라 놓은 것. 앱은 시스템 콜을 직접 부르지 않고 C 표준 라이브러리를 "
      "거치며, 커널로 들어가고 나올 때마다 하드웨어 컨텍스트가 스택을 오간다.",
      "저자는 이 왕복 자체가 시간을 쓴다고 못 박습니다")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)


AX, AW = 24, 208
BX, BW = 288, 264
CX_, CW = 604, 252
TOP, BH = 156, 192

zone(AX - 8, TOP - 20, AW + 16, BH + 24, "USER LAND")
zone(BX - 8, TOP - 20, BW + 16, BH + 24, "C STANDARD LIBRARY")
zone(CX_ - 8, TOP - 20, CW + 16, BH + 24, "KERNEL")

d.box(AX, TOP, AW, BH, PAPER2, RULE, 1.0, 6)
d.t(AX + AW / 2, TOP + 32, "앱 또는 명령", 14, INK, KR, "middle", 600)
d.t(AX + AW / 2, TOP + 56, "touch test.txt", 12, INFO, MONO)
for k, line in enumerate(["파일을 만들라고", "말할 뿐이고", "그 아래는 모른다"]):
    d.t(AX + AW / 2, TOP + 96 + k * 22, line, 12, MUTED, KR)

d.box(BX, TOP, BW, BH, PAPER2, RULE, 1.0, 6)
d.t(BX + BW / 2, TOP + 32, "래퍼 함수", 14, INK, KR, "middle", 600)
d.t(BX + BW / 2, TOP + 56, "glibc · musl", 12, INFO, MONO)
for k, line in enumerate(["반복되는 저수준 처리를 맡는다",
                          "돌아올 때 하드웨어 컨텍스트를",
                          "복원하는 것도 이쪽 몫이다"]):
    d.t(BX + BW / 2, TOP + 96 + k * 22, line, 12, MUTED, KR)

d.box(CX_, TOP, CW, BH, PAPER2, RULE, 1.0, 6)
d.t(CX_ + CW / 2, TOP + 32, "sys_call_table", 14, INK, MONO, "middle", 600)
d.t(CX_ + CW / 2, TOP + 56, "syscall.h · 아키텍처별 파일", 12, INFO, KR)
for k, line in enumerate(["메모리에 놓인 함수 포인터 배열",
                          "system_call() 이 컨텍스트를 저장하고",
                          "번호로 색인해 핸들러로 점프한다"]):
    d.t(CX_ + CW / 2, TOP + 96 + k * 22, line, 12, MUTED, KR)

# 내려가는 길
d.path(f"M {AX + AW} {TOP + 64} L {BX - 10} {TOP + 64}", INFO, 1.5, m="info")
d.t((AX + AW + BX) / 2, TOP + 54, "함수 호출", 12, INFO, KR)
d.path(f"M {BX + BW} {TOP + 64} L {CX_ - 10} {TOP + 64}", ACC, 1.6, m="acc")
d.t((BX + BW + CX_) / 2, TOP + 54, "소프트웨어 인터럽트", 12, ACC, KR)

# 돌아오는 길
d.path(f"M {CX_} {TOP + 152} L {BX + BW + 10} {TOP + 152}", OK, 1.5, m="ok")
d.t((BX + BW + CX_) / 2, TOP + 172, "sysexit", 12, OK, MONO)
d.path(f"M {BX} {TOP + 152} L {AX + AW + 10} {TOP + 152}", OK, 1.5, m="ok")
d.t((AX + AW + BX) / 2, TOP + 172, "컨텍스트 복원", 12, OK, KR)

d.tone(24, 400, W - 32 - 16, 76, ACC)
d.t(44, 428, "유저 랜드와 커널 모드를 오가는 전환 자체가 시간을 쓴다", 14, INK, KR, "start", 600)
d.t(44, 452, "그래서 시스템 콜을 몇 번 부르는가가 성능 이야기가 됩니다. 다음 절의 strace 가 그 횟수를 셉니다.",
    12, MUTED, KR, "start")

d.t(24, 504, "리눅스의 시스템 콜은 CPU 계열에 따라 삼백 개 안팎이거나 그보다 많고, 인자와 반환값은 man 2 로 찾습니다.",
    12, SOFT, KR, "start")
d.legend(524, [("호출", INFO), ("경계를 넘는 순간", ACC), ("복귀", OK)])
d.save("02-01.syscall-path.svg")
print("ok 02-01.syscall-path")
