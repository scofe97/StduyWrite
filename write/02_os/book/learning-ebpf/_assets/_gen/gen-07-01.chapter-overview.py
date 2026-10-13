# 타입 스펙: type-architecture — 왼쪽은 execve 한 번이 지나는 커널 경로의 네 지점, 가운데는 거기 붙은 프로그램 여섯, 오른쪽은 모두가 모이는 perf 버퍼 output 하나.
# 사실 출처: 추출본 ebpf7.txt 153~158행(bpftool perf show: prog_id 392·394·396·397·398, 예제 실행 출력) · 162~175행(프로그램 개요),
#   예제 저장소 lizrice/learning-ebpf chapter7/hello.bpf.c (HEAD 91ded4a) 의 SEC 여섯과 함수 이름,
#   linux v7.2 arch/x86/entry/syscall_64.c 89·94행(syscall_enter_from_user_mode → do_syscall_x64), fs/exec.c 1943~1951행(execve → do_execveat_common)·1748행(trace_sched_process_exec),
#   fs/exec.c v6.19 1927행(static int do_execve, v7.0 부터 없음), bpftool-perf.rst(perf show 는 raw_tracepoint·tracepoint·kprobe 만 나열).
# Layout conventions: 지점 상자 272×(56|128), 프로그램 상자 288×56, 줄 stride 72(y=124 시작), output 상자 200 폭 전 줄에 걸침. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 640
d = D(W, H, "LEARNING EBPF · 07-01",
      "execve 한 번이 지나는 길에 프로그램 여섯이 붙는다",
      "execve 는 sys_enter_execve tracepoint, __x64_sys_execve, 커널 함수 do_execve, sched_process_exec tracepoint 를 차례로 지나고, 각 지점에 붙은 프로그램 여섯이 모두 같은 perf 버퍼 output 으로 값을 보낸다. do_execve 는 v7.0 에서 없어졌다.",
      "지점마다 유형이 다르고 출구는 하나입니다")

SX, SW = 32, 272
PX, PW = 368, 288
OX, OW = 728, 200
NH = 56
ROWS = [124 + 72 * i for i in range(6)]
d.t(SX, 108, "커널 지점", 12, SOFT, KR, "start", 600)
d.t(PX, 108, "붙은 프로그램", 12, SOFT, KR, "start", 600)
d.t(OX, 108, "출구", 12, SOFT, KR, "start", 600)

# 지점 상자: (첫 줄, 줄 수, 이름, 설명, 색)
STATIONS = [
    (0, 1, "sys_enter_execve", "syscall 진입 tracepoint", INFO),
    (1, 1, "__x64_sys_execve", "x86-64 syscall 함수", INFO),
    (2, 2, "do_execve", "v7.0 에서 제거", ACC),
    (4, 2, "sched_process_exec", "exec 처리 중 tracepoint", INFO),
]
for r0, n, name, sub, c in STATIONS:
    y = ROWS[r0]
    h = NH + 72 * (n - 1)
    d.tone(SX, y, SW, h, c, 6, "1F" if c == ACC else "12", 1.4 if c == ACC else 1.2)
    d.t(SX + SW / 2, y + h / 2 - 2, name, 14, c, MONO, "middle", 600)
    d.t(SX + SW / 2, y + h / 2 + 18, sub, 13, MUTED, KR)

PROGS = [
    ("tp_sys_enter_execve", "prog_id 396"),
    ("kprobe_sys_execve", "prog_id 392"),
    ("kprobe_do_execve", "prog_id 394"),
    ("fentry_execve", "perf 목록에 없음"),
    ("tp_btf_exec", "prog_id 397·398"),
    ("raw_tp_exec", "prog_id 397·398"),
]
st_of = [0, 1, 2, 2, 3, 3]
oy0, oy1 = ROWS[0], ROWS[5] + NH
d.tone(OX, oy0, OW, oy1 - oy0, WARN, 6, "12", 1.2)
d.t(OX + OW / 2, (oy0 + oy1) / 2 - 12, "output", 14, WARN, MONO, "middle", 600)
d.t(OX + OW / 2, (oy0 + oy1) / 2 + 10, "PERF_EVENT_ARRAY", 12, MUTED, MONO)
d.t(OX + OW / 2, (oy0 + oy1) / 2 + 30, "perf 버퍼", 13, MUTED, KR)

for i, (nm, sub) in enumerate(PROGS):
    y = ROWS[i]
    d.tone(PX, y, PW, NH, OK, 6, "12", 1.2)
    d.t(PX + PW / 2, y + 24, nm, 13, OK, MONO, "middle", 600)
    d.t(PX + PW / 2, y + 44, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
    d.arrow([(SX + SW + 2, y + NH // 2), (PX - 6, y + NH // 2)], INFO if st_of[i] != 2 else ACC, "info" if st_of[i] != 2 else "acc", 1.5)
    d.arrow([(PX + PW + 2, y + NH // 2), (OX - 6, y + NH // 2)], MUTED, "ar", 1.4)

d.legend(H - 56, [("커널 지점", INFO), ("붙은 프로그램", OK), ("현재 없는 함수", ACC), ("공유 출구", WARN)])
d.save("07-01.chapter-overview.svg")
