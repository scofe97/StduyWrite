# 타입 스펙: type-layers — 위에서 아래로 사용자 공간 라이브러리 · 시스템 콜·LSM 훅 · cgroup · 소켓 · 흐름 분해·LWT · TC · NIC 드라이버 일곱 층. 층마다 프로그램 유형과 필요한 권한을 옆 라벨로. focal 은 반환값으로 거부하는 LSM 층.
# 사실 출처: 커널 v7.2 include/linux/bpf_types.h L39~40(KPROBE ctx pt_regs)·L5~13(SOCKET_FILTER·SCHED_CLS·XDP ctx),
#   kernel/bpf/syscall.c L2840~2869(is_net_admin_prog_type)·L2871~2885(is_perfmon_prog_type, LSM·KPROBE 포함)·L69~70(sysctl_unprivileged_bpf_disabled 기본 2)·L3030~3041(적재 때 권한 검사, SOCKET_FILTER·CGROUP_SKB 는 unprivileged_bpf_disabled=0 일 때만 CAP_BPF 예외), kernel/bpf/Kconfig L73~75(BPF_UNPRIV_DEFAULT_OFF default y),
#   kernel/bpf/token.c L12~15(CAP_SYS_ADMIN 대체), tools/lib/bpf/libbpf.c L10081~10098(uprobe+·usdt+ = KPROBE)·L13281~13289(섹션 이름 형식), docs.kernel.org/bpf/prog_lsm.html(file_mprotect).
# Layout conventions: 레이어 높이 48·stride 56·폭 848, 모든 좌표 4의 배수. accent 는 LSM 한 층에만(스펙 범위 56~72 보다 낮은 48 은 01-01 개관과 같은 값).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 568
d = D(W, H, "LEARNING EBPF · 07-02", "붙는 자리 일곱 층이 컨텍스트와 필요한 권한을 가른다",
      "모든 층에 CAP_BPF 가 필요하고 트레이싱 쪽 층은 CAP_PERFMON, 네트워크 쪽 층은 CAP_NET_ADMIN 이 더 따라옵니다. SOCKET_FILTER 와 CGROUP_SKB 는 unprivileged_bpf_disabled=0 일 때만 CAP_BPF 예외입니다.",
      "위쪽일수록 사용자 공간에 가깝고 아래쪽일수록 NIC 에 가깝습니다")

LX, LW, LH, STRIDE, Y0 = 36, 848, 48, 56, 100
PERF = "CAP_PERFMON + CAP_BPF"
NET = "CAP_NET_ADMIN + CAP_BPF"
EXC_CG = "CGROUP_SKB 만 · disabled=0 이면 CAP_BPF 예외"
EXC_SK = "SOCKET_FILTER 만 · disabled=0 이면 CAP_BPF 예외"
layers = [
    ("L7", "사용자 공간", "KPROBE · uprobe · USDT", PERF, INFO, None),
    ("L6", "시스템 콜·LSM 훅", "LSM · file_mprotect", PERF, ACC, None),
    ("L5", "cgroup", "CGROUP_SOCK · CGROUP_SKB · CGROUP_SYSCTL", NET, OK, EXC_CG),
    ("L4", "소켓", "SOCKET_FILTER · SOCK_OPS · SK_SKB", NET, OK, EXC_SK),
    ("L3", "흐름 분해·LWT", "FLOW_DISSECTOR · LWT_*", NET, OK, None),
    ("L2", "TC", "SCHED_CLS · __sk_buff", NET, OK, None),
    ("L1", "NIC 드라이버", "XDP · xdp_md", NET, OK, None),
]
for i, (tag, name, sub, cap, c, extra) in enumerate(layers):
    y = Y0 + i * STRIDE
    focal = c == ACC
    d.tone(LX, y, LW, LH, c, r=6, op="1F" if focal else "12", sw=1.4 if focal else 1.2)
    d.t(LX + 16, y + 30, name, 14, INK, KR, "start", 600)
    d.t(LX + 232, y + 30, sub, 12, INK, MONO, "start")
    if extra:
        d.t(LX + LW - 16, y + 30, extra, 12, MUTED, KR, "end")

d.legend(H - 56, [("트레이싱 · CAP_PERFMON", INFO), ("LSM · 반환값으로 거부", ACC), ("네트워크 · CAP_NET_ADMIN", OK)])
d.save("07-02.chapter-overview.svg")
