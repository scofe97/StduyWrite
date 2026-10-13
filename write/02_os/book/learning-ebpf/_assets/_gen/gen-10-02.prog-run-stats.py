# 타입 스펙: type-swimlane — 레인 [사용자 공간 · bpf() · 커널] 위쪽 갈래(BPF_PROG_RUN)와 레인 [사용자 공간 · 커널] 아래쪽 갈래(bpf_stats)를 위아래로 쌓는다. 단계 넷씩.
# 사실 출처: Linux v7.2 include/uapi/linux/bpf.h L366~392(BPF_PROG_TEST_RUN: prog_fd · data_in · repeat → retval · duration), L1703~1725(attr.test), L830~842(BPF_ENABLE_STATS),
#   Documentation/admin-guide/sysctl/kernel.rst L111~122(bpf_stats_enabled), Documentation/bpf/bpf_prog_run.rst L25~51(유형 목록 · 부수 효과 없음),
#   추출본 ebpf10.txt 845~852행(run_time_ns 316876 run_cnt 4 → 316876 / 4 ≈ 79219 ns).
# Layout conventions: 단계 w=172·h=44, x=148·352·556·760(stride 204), 레인 h=64, 위 갈래 선 y=100·164·228·292, 아래 갈래 선 y=324·388·452. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 536
d = D(W, H, "LEARNING EBPF · 10-02 §4",
      "BPF_PROG_RUN 은 repeat 번 돌려 반환값을, bpf_stats 는 횟수와 시간을 준다",
      "위 갈래는 사용자 공간이 가짜 패킷과 repeat 를 bpf() 로 넘겨 커널에서 실행하고 retval 과 duration 을 받는다. 아래 갈래는 sysctl 로 통계를 켜고 bpftool 이 run_time_ns 와 run_cnt 를 읽는다.",
      "위는 시험, 아래는 측정")

XS = (148, 352, 556, 760)
SW, SH = 172, 44


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


def step(i, y, title, sub, c, focal=False):
    x = XS[i]
    d.tone(x, y, SW, SH, c, 6, "14" if focal else "12", 1.6 if focal else 1.2)
    d.t(x + SW / 2, y + 19, title, 12, INK, fam(title), "middle", 600)
    d.t(x + SW / 2, y + 36, sub, 12, MUTED, fam(sub))


def elbow(i, y1, j, y2, c, mk):
    x1 = XS[i] + SW + 2
    x2 = XS[j] - 6
    xm = (XS[i] + SW + XS[j]) // 2
    if y1 == y2:
        d.arrow([(x1, y1), (x2, y2)], c, mk, 1.5)
    else:
        d.arrow([(x1, y1), (xm, y1), (xm, y2), (x2, y2)], c, mk, 1.5)


# 위 갈래 — 레인 셋
for y in (100, 164, 228, 292):
    d.line(24, y, W - 24, y, RULE, 0.8)
for y, name in ((144, "사용자 공간"), (196, "bpf()"), (260, "커널")):
    d.t(24, y + 4, name, 12, MUTED, KR if name != "bpf()" else MONO, "start")
d.t(24, 120, "BPF_PROG_RUN", 12, ACC, MONO, "start", 600)
UA, BA, KA = 110, 174, 238
step(0, UA, "BPF_PROG_RUN", "data_in · repeat", INFO)
step(1, BA, "bpf()", "attr.test", WARN)
step(2, KA, "가짜 ctx 로 실행", "패킷 안 버려짐", OK)
step(3, UA, "retval · duration", "XDP_PASS", INFO)
elbow(0, UA + 22, 1, BA + 22, MUTED, "ar")
elbow(1, BA + 22, 2, KA + 22, MUTED, "ar")
elbow(2, KA + 22, 3, UA + 22, MUTED, "ar")

# 아래 갈래 — 레인 둘
for y in (324, 388, 452):
    d.line(24, y, W - 24, y, RULE, 0.8)
for y, name in ((368, "사용자 공간"), (420, "커널")):
    d.t(24, y + 4, name, 12, MUTED, KR, "start")
d.t(24, 344, "bpf_stats", 12, ACC, MONO, "start", 600)
UB, KB = 334, 398
step(0, UB, "sysctl -w", "bpf_stats_enabled=1", INFO)
step(1, KB, "프로그램 실행마다", "run_cnt · run_time_ns", OK)
step(2, UB, "bpftool prog list", "run_time_ns · run_cnt", INFO)
step(3, UB, "316876 ÷ 4", "≈ 79µs / 회", ACC, True)
elbow(0, UB + 22, 1, KB + 22, MUTED, "ar")
elbow(1, KB + 22, 2, UB + 22, MUTED, "ar")
elbow(2, UB + 22, 3, UB + 22, MUTED, "ar")

d.legend(H - 56, [("사용자 공간", INFO), ("bpf()", WARN), ("커널", OK), ("회당 시간", ACC)])
d.save("10-02.prog-run-stats.svg")
