# 타입 스펙: type-data-flow — 줄 둘(syscall kprobe · 함수 kprobe) × 단계 넷 + 공유 출구. 사용자 포인터와 커널 포인터가 서로 다른 헬퍼를 거쳐 같은 data.path 로 모인다.
# 사실 출처: 예제 저장소 chapter7/hello.bpf.c (HEAD 91ded4a) — kprobe_sys_execve 는 bpf_probe_read_user_str(data.path, …, pathname),
#   kprobe_do_execve 는 BPF_CORE_READ(filename, name) 뒤 bpf_probe_read_kernel_str(data.path, …, name), 둘 다 bpf_perf_event_output(ctx, &output, BPF_F_CURRENT_CPU, …),
#   linux v7.2 include/linux/fs.h 2429~2438행(struct filename 의 첫 필드 name), fs/exec.c v6.19 1927행(do_execve)·v7.2 1943~1951행(execve 가 do_execveat_common 을 직접 호출),
#   arch/x86/entry/syscalls/syscall_64.tbl 71행(59 execve). "/bin/ls" 는 execve 에 넘긴 경로의 예시 값이다.
# Layout conventions: 열 4(188 폭, 간격 20) + 출구 열 120, 줄 높이 168 안에 노드 72. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 1000, 480
d = D(W, H, "LEARNING EBPF · 07-01 §2", "두 kprobe 는 다른 헬퍼로 읽어 같은 data.path 를 채운다",
      "__x64_sys_execve 의 pathname 은 사용자 공간 포인터라 bpf_probe_read_user_str 로, do_execve 의 filename 은 커널 구조체라 BPF_CORE_READ 와 bpf_probe_read_kernel_str 로 읽는다. 둘 다 data.path 에 /bin/ls 가 들어가 bpf_perf_event_output 으로 나간다. do_execve 는 v7.0 에서 제거됐다.",
      "읽는 헬퍼가 포인터의 주소 공간을 따라갑니다")

CX = [24, 232, 440, 648]
CW = 188
OXX, OWW = 856, 120
HEAD = ["01 호출 지점", "02 꺼낸 값", "03 읽기 헬퍼", "04 채운 필드"]
for x, h in zip(CX, HEAD):
    d.box(x + CW / 2 - 52, 100, 104, 20, PAPER2, RULE, 0.9, 10)
    d.t(x + CW / 2, 114, h, 12, MUTED, KR, "middle", 600)
d.box(OXX + OWW / 2 - 40, 100, 80, 20, PAPER2, RULE, 0.9, 10)
d.t(OXX + OWW / 2, 114, "05 출구", 12, ACC, KR, "middle", 600)

ROWS = [("syscall kprobe", 148), ("함수 kprobe", 316)]
NH = 72
CELLS = [
    [("__x64_sys_execve", "execve(\"/bin/ls\", …)", INFO, 12),
     ("pathname", "사용자 공간 포인터", INFO, 12),
     ("bpf_probe_read_user_str", "사용자 주소를 읽음", OK, 11),
     ("data.path", "\"/bin/ls\"", INFO, 12)],
    [("do_execve", "v7.0 에서 제거", WARN, 12),
     ("filename->name", "커널 포인터", INFO, 12),
     ("bpf_probe_read_kernel_str", "커널 주소를 읽음", OK, 11),
     ("data.path", "\"/bin/ls\"", INFO, 12)],
]
for k, ((lab, y0), row) in enumerate(zip(ROWS, CELLS)):
    d.t(24, y0 - 8, lab, 13, MUTED, KR, "start", 600)
    for i, (t1, t2, c, sz) in enumerate(row):
        x = CX[i]
        d.tone(x, y0, CW, NH, c, 6, "12", 1.2)
        d.t(x + CW / 2, y0 + 30, t1, sz, c, MONO, "middle", 600)
        d.t(x + CW / 2, y0 + 52, t2, 12, MUTED, _kr(t2))
        if i:
            cy = y0 + NH // 2
            d.arrow([(CX[i - 1] + CW + 2, cy), (x - 6, cy)], c if c != WARN else MUTED, "ok" if c == OK else "info", 1.5)

OY, OH = 148, 316 + NH - 148
d.o.append(f'<rect x="{OXX}" y="{OY}" width="{OWW}" height="{OH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
d.t(OXX + OWW / 2, OY + OH / 2 - 14, "output", 14, ACC, MONO, "middle", 600)
d.t(OXX + OWW / 2, OY + OH / 2 + 8, "perf 버퍼", 12, MUTED, KR)
for y0 in (148, 316):
    d.arrow([(CX[3] + CW + 2, y0 + NH // 2), (OXX - 6, y0 + NH // 2)], ACC, "acc", 1.6)
d.chip(CX[3] + CW / 2, 268, "bpf_perf_event_output", ACC, 11)

d.legend(H - 56, [("값·필드", INFO), ("읽기 헬퍼", OK), ("제거된 함수", WARN), ("출구", ACC)])
d.save("07-01.type-data-flow.svg")
