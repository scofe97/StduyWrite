# 타입 스펙: type-layers — sys_enter_execve 레코드를 오프셋 순으로 쌓은 층 아홉(여덟 필드 + 패딩 4바이트), 오른쪽에 대응하는 my_syscalls_enter_execve 필드. 앞 네 층은 접근 금지 음영.
# 사실 출처: 추출본 ebpf7.txt 425~437행(format 파일: offset 0·2·3·4·8·16·24·32 와 size), 464~475행(구조체),
#   예제 저장소 chapter7/hello.bpf.c (HEAD 91ded4a) 의 struct my_syscalls_enter_execve(syscall_nr long · filename_ptr void * · argv_ptr long · envp_ptr long),
#   linux v7.2 kernel/trace/bpf_trace.c 1490행(off < sizeof(void *) 이면 접근 거부 = 앞 8바이트의 네 공통 필드).
# Layout conventions: 층 높이 40·stride 48, 왼쪽 상자 300 폭·오른쪽 상자 240 폭, 오프셋 태그는 왼쪽 열. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 640
d = D(W, H, "LEARNING EBPF · 07-01 §4", "레코드 앞 8바이트의 공통 필드 넷은 프로그램이 읽지 못한다",
      "sys_enter_execve 의 format 은 오프셋 0 부터 common_type, common_flags, common_preempt_count, common_pid 를 두고 8 에 __syscall_nr, 16 에 filename, 24 에 argv, 32 에 envp 를 둔다. 앞 네 필드는 읽을 수 없고, 구조체의 syscall_nr 는 long 이라 4바이트 여백을 덮어 filename_ptr 이 16 에 놓인다.",
      "format 파일과 구조체가 같은 오프셋에 겹칩니다")

TOP, ST, LH = 128, 48, 40
LXX, LW = 84, 300
RXX, RW = 476, 240
ROWS = [
    ("0", "common_type", "2바이트", "common_type", "u16", BAD),
    ("2", "common_flags", "1바이트", "common_flags", "u8", BAD),
    ("3", "common_preempt_count", "1바이트", "common_preempt_count", "u8", BAD),
    ("4", "common_pid", "4바이트", "common_pid", "int", BAD),
    ("8", "__syscall_nr", "4바이트", "syscall_nr", "long", INFO),
    ("12", "(여백)", "4바이트", None, None, None),
    ("16", "filename", "8바이트", "filename_ptr", "void *", ACC),
    ("24", "argv", "8바이트", "argv_ptr", "long", INFO),
    ("32", "envp", "8바이트", "envp_ptr", "long", INFO),
]
d.t(LXX + LW / 2, 112, "format 파일", 13, MUTED, KR, "middle", 600)
d.t(RXX + RW / 2, 112, "my_syscalls_enter_execve", 12, MUTED, MONO, "middle", 600)
d.t(24, 112, "오프셋", 12, SOFT, KR, "start", 600)
for i, (off, ln, sz, rn, rt, c) in enumerate(ROWS):
    y = TOP + i * ST
    d.t(24, y + 26, off, 13, SOFT, MONO, "start", 600)
    if c is None:
        d.o.append(f'<rect x="{LXX}" y="{y}" width="{LW}" height="{LH}" rx="6" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
        d.t(LXX + 14, y + 26, ln, 12, MUTED, KR, "start")
        d.t(LXX + LW - 14, y + 26, sz, 12, MUTED, KR, "end")
        d.line(LXX + LW + 2, y + LH / 2, RXX - 2, y + LH / 2, RULE, 1.2, "4 4")
        continue
    if c == ACC:
        d.tone(LXX, y, LW, LH, ACC, 6, "1F", 1.4)
    else:
        d.tone(LXX, y, LW, LH, c, 6, "12", 1.2)
    d.t(LXX + 14, y + 26, ln, 12, c, MONO, "start", 600)
    d.t(LXX + LW - 14, y + 26, sz, 12, MUTED, KR, "end")
    # long syscall_nr 은 __syscall_nr 4바이트와 뒤 여백 4바이트를 한 칸으로 덮으므로 두 층에 걸친다
    rh, ty = (ST + LH, y + 50) if rn == "syscall_nr" else (LH, y + 26)
    d.box(RXX, y, RW, rh, PAPER2, RULE, 0.9, 6)
    d.t(RXX + 14, ty, rn, 12, INK, MONO, "start", 600)
    d.t(RXX + RW - 14, ty, rt, 12, MUTED, MONO, "end")
    d.line(LXX + LW + 2, y + LH / 2, RXX - 2, y + LH / 2, RULE, 1.2)
# 접근 금지 괄호
by0, by1 = TOP, TOP + 3 * ST + LH
d.line(RXX + RW + 12, by0, RXX + RW + 12, by1, BAD, 1.6)
d.line(RXX + RW + 4, by0, RXX + RW + 12, by0, BAD, 1.6)
d.line(RXX + RW + 4, by1, RXX + RW + 12, by1, BAD, 1.6)
d.chip(RXX + RW + 132, (by0 + by1) / 2 - 12, "접근 ✗", BAD, 12)
d.chip(RXX + RW + 132, (by0 + by1) / 2 + 16, "invalid bpf_context access", BAD, 10)

d.legend(H - 56, [("접근 금지 공통 필드", BAD), ("읽는 필드", ACC), ("그 밖의 필드", INFO)])
d.save("07-01.type-layers.svg")
