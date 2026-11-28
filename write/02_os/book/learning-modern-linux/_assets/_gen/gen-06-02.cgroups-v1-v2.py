# 06-02 §3 — 큰 그림: v1 은 계층이 여럿(계층마다 컨트롤러 묶음), v2 는 계층 하나에 컨트롤러 전부.
#   세부는 06-02.cgroups-v1.svg(### v1 절)와 06-02.cgroups-v2.svg(### v2 절)로 나눴다(2026-11-29).
# 원문("cgroup v1"): "With cgroup v1, the community had an ad hoc approach, adding new cgroups and
#       controllers as needed. The following v1 cgroups and controllers exist (ordered from oldest to
#       newest; note that the docs are all over the place and inconsistent)" — CFS bandwidth control
#       (2.6.24), CPU accounting (2.6.24), cpusets (2.6.24), Memory resource controller (2.6.25),
#       Device whitelist (2.6.26), freezer (2.6.28), Network classifier (2.6.29), Block IO (2.6.33),
#       perf_event (2.6.39), Network priority (3.3), HugeTLB (3.5), Process number (4.3).
# 원문("cgroup v2"): "cgroup v2 is a total rewrite of cgroups with the lessons learned from v1. ...
#       cgroup v2 has only single hierarchy, and all controllers are managed the same way."
#       v2 컨트롤러 여덟 — CPU, Memory, I/O, PID, cpuset, device(eBPF 위에 구현), rdma, HugeTLB.
# 주의: 원문은 v1 을 "the per-process cgroup v1 design" 이라 적지만 v1 의 다중 계층은 프로세스별이 아니라
#       *계층별* 이다(본문 각주 [^cgv1], 커널 cgroup-v1 문서: "every task in the system is in exactly one of
#       the cgroups in the hierarchy", "Each hierarchy is a partition of all tasks in the system"). 그래서
#       왼쪽은 계층마다 컨트롤러가 붙고, 같은 태스크 하나가 계층마다 한 칸씩 드는 모양으로 그린다.
# 값: 오른쪽 트리의 이름은 본문 `systemctl status` 출력(user.slice → user-1000.slice → user@1000.service →
#       gvfs-goa-volume-monitor.service → 14497), 수치는 본문 `systemd-cgtop` 출력(/ 623 · 5.8G,
#       /system.slice 122 · 1.6G, ModemManager.service 3 · 748.0K, /docker 48.3M)이다. 두 출력을 한 트리에
#       합쳤고 그 사실을 도식 아래 한 줄에 밝힌다. 왼쪽 컨트롤러 이름과 버전은 본문 v1 목록 값이다.
# 타입 스펙: type-tree — 부모 → 자식 관계. 왼쪽 v1 은 작은 트리 셋의 루트, 오른쪽 v2 는 루트 하나. accent 는 v2 의 루트 "/" 하나.
# 축약: 개요라 v1 은 계층 셋의 컨트롤러 이름·버전만, v2 는 루트와 컨트롤러 여덟만 둔다. 트리 모양과 실제 값은 세부 도식에 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 368
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §3",
      "v1 은 계층이 여럿, v2 는 계층 하나에 컨트롤러 전부",
      "v1 은 CPU 계정·메모리·블록 IO 처럼 컨트롤러가 그때그때 붙으며 계층이 따로 생겼다. "
      "v2 는 계층이 하나이고 루트 / 에 컨트롤러 여덟이 모두 붙는다.",
      "가장 큰 구조 변화는 계층의 수입니다")

PY, PB = 100, 304
LX0, LX1 = 24, 412
RX0, RX1 = 436, 856

d.box(LX0, PY, LX1 - LX0, PB - PY, PAPER2, WARN, 1.2, 8)
d.t(LX0 + 16, PY + 28, "cgroups v1", 15, WARN, MONO, "start", 600)
d.t(LX0 + 136, PY + 28, "계층 여럿", 13, INK, KR, "start", 600)
CXS = [LX0 + 68 + i * 128 for i in range(3)]
hier = [("CPU 계정", "2.6.24"), ("메모리", "2.6.25"), ("블록 IO", "2.6.33")]
CY, CH = PY + 72, 48
RY = CY + CH + 28
for i, (cx, (name, ver)) in enumerate(zip(CXS, hier)):
    d.line(cx, CY + CH, cx, RY, MUTED, 1.0)
    d.tone(cx - 54, CY, 108, CH, WARN)
    d.t(cx, CY + 21, name, 12, INK, KR, "middle", 600)
    d.t(cx, CY + 38, ver, 11, MUTED, MONO)
    d.box(cx - 20, RY, 40, 24, PAPER, MUTED, 1.0, 4)
    d.t(cx, RY + 17, "/", 13, INK, MONO, "middle", 600)
    d.t(cx, CY - 8, f"계층 {i + 1}", 11, SOFT, KR)

d.arrow([(LX1 + 4, (PY + PB) / 2), (RX0 - 4, (PY + PB) / 2)], MUTED, "ar", 1.4)

d.box(RX0, PY, RX1 - RX0, PB - PY, PAPER2, RULE, 1.0, 8)
d.t(RX0 + 16, PY + 28, "cgroups v2", 15, ACC, MONO, "start", 600)
d.t(RX0 + 136, PY + 28, "계층 하나", 13, INK, KR, "start", 600)
FX0, FX1, FY, FH = RX0 + 16, RX1 - 16, PY + 44, 92
d.o.append(f'<rect x="{FX0}" y="{FY}" width="{FX1 - FX0}" height="{FH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(FX0 + 14, FY + 24, "/", 15, ACC, MONO, "start", 600)
ctrls = ["CPU", "Memory", "I/O", "PID", "cpuset", "device", "rdma", "HugeTLB"]
for i, c in enumerate(ctrls):
    d.chip(FX0 + 56 + (i % 4) * 92, FY + 50 + (i // 4) * 26, c, OK, 11)

LY = PB + 20
d.legend(LY, [("v1 계층", WARN), ("v2 컨트롤러", OK), ("계층 하나", ACC)])
d.save("06-02.cgroups-v1-v2.svg")
print("ok 06-02.cgroups-v1-v2", LY)
