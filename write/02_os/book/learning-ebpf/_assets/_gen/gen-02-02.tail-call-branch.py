# 타입 스펙: type-flowchart — sys_enter 한 번이 prog array 항목에 따라 어느 프로그램으로 넘어가고 무엇을 찍는지의 분기.
# 사실 출처: 원서 Ch.2 17~21쪽 · 예제 저장소 chapter2/hello-tail.py (HEAD 91ded4a) — BPF_PROG_ARRAY(syscall, 500), 반복문으로 0~499 를 ignore_opcode 로 채운 뒤
#   59 → hello_exec, 222~226 → hello_timer. hello_timer 는 222 "Creating a timer", 226 "Deleting a timer", 그 밖 "Some other timer operation".
#   hello() 의 마지막 줄 bpf_trace_printk("Another syscall: %d") 는 tail call 이 실패할 때만 닿는다(linux v7.2 include/uapi/linux/bpf.h 줄 2199~2206).
#   syscall 번호는 linux v7.2 arch/x86/entry/syscalls/syscall_64.tbl : 59 execve · 222 timer_create · 223 timer_settime · 224 timer_gettime · 225 timer_getoverrun · 226 timer_delete.
#   색: tail call 대상 셋(hello_exec·hello_timer·ignore_opcode)은 모두 "프로그램" 색, 출력 색은 hello() 의 Another syscall 한 줄만.
# Layout conventions: 흐름은 위→아래, 마름모는 출구 셋 이하(둘로 나눠 중첩), 모서리 직각. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 848
d = D(W, H, "LEARNING EBPF · 02-02 §4",
      "sys_enter 하나가 항목에 따라 갈라진다",
      "hello() 가 opcode 로 syscall 배열을 조회해 tail call 하고, 항목이 없을 때만 호출자가 계속 실행되어 Another syscall 을 찍는다.",
      "prog array 항목 등록 여부와 시스템 콜 번호별 분기")

CX = 380
def rect(cx, cy, w, h, title, sub, c, mono=True):
    d.tone(cx - w//2, cy - h//2, w, h, c, 6, "12", 1.2)
    d.t(cx, cy - 4, title, 13, c, MONO if mono else KR, "middle", 600)
    d.t(cx, cy + 16, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)

def oval(cx, cy, w, h, title, c):
    d.o.append(f'<rect x="{cx-w//2}" y="{cy-h//2}" width="{w}" height="{h}" rx="{h//2}" fill="{c}22" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 5, title, 13, c, MONO, "middle", 600)

def diamond(cx, cy, hw, hh, title, c):
    pts = f"{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{c}22" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 5, title, 12, c, KR if any("가" <= ch <= "힣" for ch in title) else MONO, "middle", 600)

# 위쪽 사슬
oval(CX, 116, 200, 40, "sys_enter", INFO)
rect(CX, 204, 240, 56, "hello()", "opcode = ctx->args[1]", OK)
rect(CX, 300, 240, 56, "syscall.call(ctx, opcode)", "→ bpf_tail_call", ACC)
d.arrow([(CX, 138), (CX, 174)], MUTED, "ar", 1.4)
d.arrow([(CX, 234), (CX, 270)], MUTED, "ar", 1.4)
d.arrow([(CX, 330), (CX, 366)], MUTED, "ar", 1.4)

# 마름모 1 — 항목 있음?
D1 = 404
diamond(CX, D1, 88, 36, "항목 있음?", INK)
# 없음 → 오른쪽 → 아래
FX = 696
d.arrow([(CX + 90, D1), (FX - 116, D1)], BAD, "bad", 1.5)
d.chip(CX + 136, D1 - 18, "없음", BAD, 12)
rect(FX, D1, 220, 56, "tail call 실패", "index ≥ 500 · 호출자 계속", BAD, False)
rect(FX, 500, 220, 48, "Another syscall: N", "bpf_trace_printk", WARN)
d.arrow([(FX, D1 + 30), (FX, 474)], BAD, "bad", 1.5)

# 있음 → 아래 마름모 2
D2 = 604
d.arrow([(CX, D1 + 38), (CX, D2 - 40)], OK, "ok", 1.5)
d.chip(CX + 40, (D1 + D2) // 2, "있음", OK, 12)
diamond(CX, D2, 88, 36, "항목이 가리킨 프로그램", INK)

# 59 → hello_exec (왼쪽)
EX = 100
d.arrow([(CX - 90, D2), (EX + 86, D2)], OK, "ok", 1.5)
d.chip(CX - 144, D2 - 18, "59 · execve", MUTED, 12)
d.tone(EX - 80, D2 - 36, 160, 72, OK, 6, "12", 1.2)
d.t(EX, D2 - 8, "hello_exec", 13, OK, MONO, "middle", 600)
d.t(EX, D2 + 14, "Executing a program", 12, MUTED, MONO)

# 그 밖 → ignore_opcode (오른쪽)
d.arrow([(CX + 90, D2), (FX - 116, D2)], OK, "ok", 1.5)
d.chip(CX + 136, D2 - 18, "그 밖 0~499", MUTED, 12)
rect(FX, D2, 220, 56, "ignore_opcode", "출력 없음", OK)

# 222~226 → hello_timer (아래)
TY = 732
d.arrow([(CX, D2 + 38), (CX, TY - 48)], OK, "ok", 1.5)
d.chip(CX + 52, D2 + 62, "222~226", MUTED, 12)
d.tone(CX - 160, TY - 44, 320, 88, OK, 6, "12", 1.2)
d.t(CX, TY - 22, "hello_timer", 13, OK, MONO, "middle", 600)
for i, ln in enumerate(("222 timer_create → Creating a timer",
                        "226 timer_delete → Deleting a timer",
                        "223~225 → Some other timer operation")):
    d.t(CX, TY - 2 + 18 * i, ln, 12, MUTED, MONO)

d.legend(H - 56, [("진입·호출", INFO), ("프로그램", OK), ("tail call", ACC), ("출력", WARN), ("실패", BAD)])
d.save("02-02.tail-call-branch.svg")
