# 타입 스펙: type-tree — 뿌리 "프로그램 유형" 하나, 가지 넷(KPROBE · TRACEPOINT · TRACING · XDP), 가지마다 컨텍스트 줄과 반환값·헬퍼 줄을 가진 잎. 좌에서 우로 깊이 3.
# 사실 출처: 추출본 ebpf7.txt 41~97행(컨텍스트 인자·반환값·헬퍼 호환), 예제 저장소 chapter7/hello.bpf.c (HEAD 91ded4a) — kprobe·tracepoint·fentry 프로그램이 bpf_get_current_pid_tgid 를 부름,
#   linux v7.2 tools/lib/bpf/bpf_tracing.h 817행(BPF_KPROBE 의 struct pt_regs *ctx)·672행(BPF_PROG 의 unsigned long long *ctx),
#   kernel/trace/bpf_trace.c 104~110행(kprobe 반환 0 = 이벤트 걸러냄, 1 = 기록), include/uapi/linux/bpf.h 6576~6582행(enum xdp_action)·6587행(struct xdp_md),
#   Documentation/bpf/libbpf/program_types.rst 198~218행(BPF_PROG_TYPE_TRACING 아래 fentry·fexit·tp_btf), v7.2 net/core/filter.c 8600~8654행(xdp_func_proto, 8609행 bpf_xdp_adjust_head)·kernel/bpf/helpers.c 2114~2125행(pid 헬퍼, v6.10~)·kernel/bpf/helpers.c 4994~4998행(유형별 kfunc 등록).
# kfunc 줄은 본문 §1 의 '등록은 프로그램 유형마다 따로' 와 같은 값.
# Layout conventions: 뿌리 180×64, 가지 264×68·stride 100, 잎 400×68, 연결선은 뿌리 오른쪽 척추에서 엘보. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 540
d = D(W, H, "LEARNING EBPF · 07-01 §1", "프로그램 유형이 컨텍스트와 반환값과 헬퍼를 한꺼번에 정한다",
      "kprobe 는 pt_regs 를 받고 0 이나 1 을 돌려 이벤트 기록 여부를 정하며, tracepoint 는 이벤트 레코드를, tracing 은 함수 인자를, XDP 는 xdp_md 를 받고 패킷 처리 방식을 돌려준다. XDP 전용 헬퍼 bpf_xdp_adjust_head 는 kprobe 에서 쓸 수 없다.",
      "유형마다 받는 구조체와 돌려주는 값이 다릅니다")

RX, RY, RW, RH = 20, 236, 180, 64
BX, BW_, BH = 244, 264, 68
LX, LW, LH = 540, 400, 68
YS = [104, 204, 304, 404]
BR = [
    ("BPF_PROG_TYPE_KPROBE", "kprobe·kretprobe", "ctx: struct pt_regs *", "반환 0·1 = 기록 여부", "bpf_xdp_adjust_head ✗ · kfunc 유형별 등록", INFO),
    ("BPF_PROG_TYPE_TRACEPOINT", "tp/…", "ctx: 이벤트 레코드 구조체", "공통 필드 4개 읽기 ✗", "헬퍼 · kfunc 유형별 목록", INFO),
    ("BPF_PROG_TYPE_TRACING", "fentry·fexit·tp_btf", "ctx: u64 인자 배열", "attach type 으로 다시 갈림", "헬퍼 · kfunc 유형별 목록", INFO),
    ("BPF_PROG_TYPE_XDP", "xdp", "ctx: struct xdp_md *", "반환 XDP_PASS·XDP_DROP…", "bpf_xdp_adjust_head ✓ · pid 헬퍼 ✓ (v6.10~)", ACC),
]

cy = [y + BH // 2 for y in YS]
d.line(RX + RW, RY + RH // 2, 224, RY + RH // 2, MUTED, 1.2)
d.line(224, cy[0], 224, cy[-1], MUTED, 1.2)
for y in cy:
    d.line(224, y, BX, y, MUTED, 1.2)
    d.line(BX + BW_, y, LX, y, RULE, 1.2)

d.box(RX, RY, RW, RH, PAPER2, RULE, 1.0)
d.t(RX + RW / 2, RY + 28, "프로그램 유형", 15, INK, KR, "middle", 600)
d.t(RX + RW / 2, RY + 48, "prog_type", 13, MUTED, MONO)

for (title, sub, l1, l2, l3, c), y in zip(BR, YS):
    if c == ACC:
        d.tone(BX, y, BW_, BH, ACC, 6, "1F", 1.4)
    else:
        d.tone(BX, y, BW_, BH, c, 6, "12", 1.2)
    d.t(BX + BW_ / 2, y + 28, title, 12, c, MONO, "middle", 600)
    d.t(BX + BW_ / 2, y + 50, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
    d.box(LX, y, LW, LH, PAPER, RULE, 0.9, 5)
    d.t(LX + 14, y + 24, l1, 12, INK, KR if any("가" <= ch <= "힣" for ch in l1) else MONO, "start", 600)
    d.t(LX + 14, y + 42, l2, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in l2) else MONO, "start")
    d.t(LX + 14, y + 58, l3, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in l3) else MONO, "start")

d.legend(H - 56, [("트레이싱 유형", INFO), ("네트워크 유형", ACC)])
d.save("07-01.type-tree.svg")
