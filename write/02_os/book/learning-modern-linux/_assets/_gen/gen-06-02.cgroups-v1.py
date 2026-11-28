# 06-02 §3 ### v1 — 계층마다 컨트롤러가 붙고 같은 태스크가 계층마다 한 칸씩 드는 모양.
#   개요는 06-02.cgroups-v1-v2.svg. 이 도식은 ### v1 절 끝에 둔다(2026-11-29).
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
# 타입 스펙: type-tree — 부모 → 자식 관계. 작은 트리 셋과 그 모두에 한 칸씩 드는 태스크 하나.
#           accent 는 태스크가 든 칸(점) 하나.
# 축약: 그룹 a·b 와 태스크 하나는 출력에 없는 예시라 점선으로 그렸다. 컨트롤러 열둘 중 셋만 놓았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 508
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §3 · v1",
      "v1 은 계층마다 컨트롤러가 붙고 태스크는 계층마다 한 칸",
      "CPU 계정·메모리·블록 IO 컨트롤러가 각자 계층을 갖고, 계층마다 루트 아래 그룹이 있다. "
      "같은 태스크 하나가 세 계층에 한 칸씩 든다.",
      "여럿으로 갈리는 축은 프로세스가 아니라 컨트롤러입니다")

PY, PB = 100, 440
LX0, LX1 = 24, 856
d.box(LX0, PY, LX1 - LX0, PB - PY, PAPER2, WARN, 1.2, 8)
d.t(LX0 + 16, PY + 28, "cgroups v1", 15, WARN, MONO, "start", 600)
d.t(LX0 + 136, PY + 28, "계층 여럿", 13, INK, KR, "start", 600)

CXS = [LX0 + (LX1 - LX0) * (2 * i + 1) / 6 for i in range(3)]
hier = [("CPU 계정", "2.6.24"), ("메모리", "2.6.25"), ("블록 IO", "2.6.33")]
CY, CH = PY + 60, 48
RY = CY + CH + 28
KY = RY + 56
TASK_IN = [0, 1, 0]
TY_ = KY + 84

for i, cx in enumerate(CXS):
    d.line(cx, CY + CH, cx, RY, MUTED, 1.0)
    d.line(cx, RY + 24, cx, RY + 40, MUTED, 1.0)
    d.line(cx - 30, RY + 40, cx + 30, RY + 40, MUTED, 1.0)
    for dx in (-30, 30):
        d.line(cx + dx, RY + 40, cx + dx, KY, MUTED, 1.0)
    kx = cx + (-30 if TASK_IN[i] == 0 else 30)
    d.line(kx, KY + 26, kx, TY_, SOFT, 1.0, "4 3")

for i, (cx, (name, ver)) in enumerate(zip(CXS, hier)):
    d.tone(cx - 54, CY, 108, CH, WARN)
    d.t(cx, CY + 21, name, 12, INK, KR, "middle", 600)
    d.t(cx, CY + 38, ver, 11, MUTED, MONO)
    d.box(cx - 20, RY, 40, 24, PAPER, MUTED, 1.0, 4)
    d.t(cx, RY + 17, "/", 13, INK, MONO, "middle", 600)
    for j, dx in enumerate((-30, 30)):
        d.o.append(f'<rect x="{cx + dx - 22}" y="{KY}" width="44" height="26" rx="4" fill="{PAPER}" '
                   f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
        d.t(cx + dx, KY + 18, "ab"[j], 12, SOFT, MONO)
        if j == TASK_IN[i]:
            d.o.append(f'<circle cx="{cx + dx}" cy="{KY + 26}" r="4" fill="{ACC}" stroke="none"/>')
    d.t(cx, CY - 8, f"계층 {i + 1}", 11, SOFT, KR)

d.o.append(f'<rect x="{LX0 + 20}" y="{TY_}" width="{LX1 - LX0 - 40}" height="36" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t((LX0 + LX1) / 2, TY_ + 23, "태스크 하나 (예) — 계층마다 한 칸", 12, MUTED, KR)
d.t(LX0 + 16, PB - 16, "그룹 a · b 와 태스크는 출력에 없는 예", 11, SOFT, KR, "start")

LY = PB + 16
d.legend(LY, [("v1 계층", WARN), ("태스크가 든 칸", ACC)])
d.save("06-02.cgroups-v1.svg")
print("ok 06-02.cgroups-v1", LY)
