# 06-02 §3 — cgroups v1 에서 v2 로, 무엇이 구조적으로 달라졌는가.
# 원문("cgroup v1"): "With cgroup v1, the community had an ad hoc approach, adding new cgroups and
#       controllers as needed. The following v1 cgroups and controllers exist (ordered from oldest to
#       newest; note that the docs are all over the place and inconsistent)" — CFS bandwidth control
#       (2.6.24), CPU accounting (2.6.24), cpusets (2.6.24), Memory resource controller (2.6.25),
#       Device whitelist (2.6.26), freezer (2.6.28), Network classifier (2.6.29), Block IO (2.6.33),
#       perf_event (2.6.39), Network priority (3.3), HugeTLB (3.5), Process number (4.3).
# 원문("cgroup v2"): "cgroup v2 is a total rewrite of cgroups with the lessons learned from v1. This is
#       true both in terms of consistent configuration and use of the cgroups as well as the (centralized
#       and uniform) documentation. Unlike the per-process cgroup v1 design, cgroup v2 has only single
#       hierarchy, and all controllers are managed the same way."
#       v2 컨트롤러 여덟 — CPU, Memory, I/O, PID, cpuset, device(eBPF 위에 구현), rdma, HugeTLB.
#       "certain distros, such as Arch, Fedora 31+, and Ubuntu 21.10, that already have v2 by default."
# 타입 스펙: type-state — 같은 대상의 앞뒤 상태를 나란히 두고 무엇이 달라졌는지만 보인다.
#           accent 는 단 하나의 구조 변화, 곧 계층이 하나로 합쳐진 것.
#           축약: v1 컨트롤러 열둘 중 셋만 계층 예시에 적었다 — 논점이 개수가 아니라 계층의 수다.
# 주의: 원문은 v1 을 "the per-process cgroup v1 design" 이라 적지만 v1 의 다중 계층은 프로세스별이 아니라
#       *계층별* 이다. 커널 cgroup-v1 문서는 "A hierarchy is a set of cgroups arranged in a tree, such that
#       every task in the system is in exactly one of the cgroups in the hierarchy, and a set of subsystems"
#       이고 "At any one time there may be multiple active hierarchies of task cgroups. Each hierarchy is a
#       partition of all tasks in the system" 이라 적는다. 그래서 도식은 계층마다 컨트롤러 묶음을 달고,
#       모든 태스크가 각 계층에 한 칸씩 든다고 그린다 — 원문 표현을 그림으로 굳히지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 592
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §3",
      "필요할 때마다 붙이던 것을 한 계층으로 다시 썼다",
      "v1 은 프로세스마다 계층이 따로였고 컨트롤러가 그때그때 붙었다. v2 는 계층이 하나이고 "
      "모든 컨트롤러가 같은 방식으로 관리된다.",
      "저자는 v2 에 집중하라고 적습니다")

PW, PX1, PX2 = 400, 24, 456
PY, PH = 156, 268

d.box(PX1, PY, PW, PH, PAPER2, WARN, 1.2, 8)
d.t(PX1 + 20, PY + 32, "cgroups v1", 16, WARN, MONO, "start", 600)
d.t(PX1 + 20, PY + 56, "필요할 때마다 새로 붙였다", 12, MUTED, KR, "start")

for i, (y, label, ver) in enumerate([
        (PY + 84, "계층 1 — cpu · cpuacct", "모든 태스크가 여기 한 칸씩"),
        (PY + 132, "계층 2 — memory", "모든 태스크가 여기 한 칸씩"),
        (PY + 180, "계층 3 — blkio · net_prio", "모든 태스크가 여기 한 칸씩")]):
    d.box(PX1 + 24, y, PW - 48, 38, PAPER, MUTED, 1.1, 5)
    d.t(PX1 + 40, y + 24, label, 11.5, INK, KR, "start")
    d.t(PX1 + PW - 40, y + 24, ver, 11, SOFT, MONO, "end")

d.t(PX1 + 20, PY + 244, "계층이 여럿이고 각 계층이 시스템의 모든 태스크를 나눕니다", 11.5, MUTED, KR, "start")

d.arrow([(432, PY + PH / 2), (448, PY + PH / 2)], MUTED, "ar", 1.5)

d.o.append(f'<rect x="{PX2}" y="{PY}" width="{PW}" height="{PH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
d.t(PX2 + 20, PY + 32, "cgroups v2", 16, ACC, MONO, "start", 600)
d.t(PX2 + 20, PY + 56, "v1 의 교훈으로 완전히 다시 썼다", 12, ACC, KR, "start")

d.box(PX2 + 24, PY + 84, PW - 48, 134, PAPER, ACC, 1.3, 6)
d.t(PX2 + PW / 2, PY + 110, "계층 하나", 14, ACC, KR, "middle", 600)
d.t(PX2 + PW / 2, PY + 132, "컨트롤러 전부가 그 하나에 붙는다", 11.5, MUTED, KR)
ctrls = ["CPU", "Memory", "I/O", "PID", "cpuset", "device", "rdma", "HugeTLB"]
for i, c in enumerate(ctrls):
    cx = PX2 + 66 + (i % 4) * 90
    cy = PY + 164 + (i // 4) * 30
    d.chip(cx, cy, c, OK, 10.5)

d.t(PX2 + 20, PY + 244, "Arch · Fedora 31+ · Ubuntu 21.10 은 이미 기본이 v2",
    11.5, MUTED, KR, "start")

d.tone(24, 448, W - 48, 62, INFO)
d.t(44, 476, "메모리 컨트롤러가 다루는 것에 dentry 와 inode 가 들어 있습니다", 12.5, INK, KR, "start", 600)
d.t(44, 498, "5장에서 본 VFS 자료구조 이름이 그대로 자원 제한의 대상으로 나오는 자리입니다.",
    11.5, MUTED, KR, "start")

d.legend(534, [("그때그때 붙인 쪽", WARN), ("v2 컨트롤러", OK), ("구조가 바뀐 자리", ACC)])
d.save("06-02.cgroups-v1-v2.svg")
print("ok 06-02.cgroups-v1-v2")
