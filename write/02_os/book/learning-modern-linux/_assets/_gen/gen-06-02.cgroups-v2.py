# 06-02 §3 ### v2 — v2 의 단일 트리를 본문 systemctl status·systemd-cgtop 출력의 실제 값으로 그린다.
#   개요는 06-02.cgroups-v1-v2.svg. 이 도식은 ### v2 절의 두 출력 뒤에 둔다(2026-11-29).
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
# 타입 스펙: type-tree — 부모 → 자식 관계. 큰 트리 하나. accent 는 컨트롤러 여덟이 모두 붙는 루트 "/" 하나.
# 축약: systemctl 출력의 bpfilter_umh 줄은 생략했다. 두 출력을 한 트리에 합쳤고 그 사실을 도식 아래 한 줄에 밝힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 612
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §3 · v2",
      "v2 는 트리 하나에 컨트롤러 전부",
      "루트 / 에 컨트롤러 여덟이 붙고, 그 아래 user.slice·system.slice·docker 같은 그룹이 "
      "systemd 단위 이름 그대로 매달린다. 메모리 컨트롤러는 dentry·inode 까지 다룬다.",
      "systemd 의 slice 가 바로 이 트리의 가지입니다")

PY, PB = 100, 472
RX0, RX1 = 24, 856
d.box(RX0, PY, RX1 - RX0, PB - PY, PAPER2, RULE, 1.0, 8)
d.t(RX0 + 16, PY + 28, "cgroups v2", 15, ACC, MONO, "start", 600)
d.t(RX0 + 136, PY + 28, "계층 하나", 13, INK, KR, "start", 600)

FX0, FX1, FY, FH = RX0 + 16, RX1 - 16, PY + 44, 72
d.o.append(f'<rect x="{FX0}" y="{FY}" width="{FX1 - FX0}" height="{FH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(FX0 + 14, FY + 24, "/", 15, ACC, MONO, "start", 600)
d.t(FX1 - 14, FY + 24, "623 tasks · 5.8G", 12, MUTED, MONO, "end")
ctrls = ["CPU", "Memory", "I/O", "PID", "cpuset", "device", "rdma", "HugeTLB"]
for i, c in enumerate(ctrls):
    d.chip(FX0 + 60 + i * 98, FY + 52, c, OK, 11)

tree = [(1, "user.slice", ""),
        (2, "user-1000.slice", ""),
        (3, "user@1000.service", ""),
        (4, "gvfs-goa-volume-monitor.service", ""),
        (5, "14497", "프로세스"),
        (1, "system.slice", "122 · 1.6G"),
        (2, "ModemManager.service", "3 · 748.0K"),
        (1, "docker", "48.3M")]
T0, TSTR = FY + FH + 28, 26
TXB, IND = FX0 + 22, 20
ys = [T0 + i * TSTR for i in range(len(tree))]
for i, (lv, name, val) in enumerate(tree):
    y = ys[i] - 4
    rail = TXB - 12 + IND * (lv - 1)
    d.line(rail, y, rail + 8, y, MUTED, 1.0)
    p = next((k for k in range(i - 1, -1, -1) if tree[k][0] == lv - 1), None)
    top = (FY + FH) if p is None else ys[p] + 4
    d.line(rail, top, rail, y, MUTED, 1.0)
for i, (lv, name, val) in enumerate(tree):
    x = TXB + IND * (lv - 1)
    if val == "프로세스":
        d.o.append(f'<circle cx="{x + 4}" cy="{ys[i] - 4}" r="4" fill="{ACC}" stroke="none"/>')
        d.t(x + 14, ys[i], name, 12, INK, MONO, "start", 600)
        d.t(x + 64, ys[i], "프로세스", 11, MUTED, KR, "start")
    else:
        d.t(x, ys[i], name, 12, INK if lv == 1 else MUTED, MONO, "start", 600 if lv == 1 else 400)
        if val:
            d.t(FX1 - 14, ys[i], val, 12, MUTED, MONO, "end")
d.t(RX0 + 16, PB - 16, "트리 = systemctl status · 수치 = systemd-cgtop", 11, SOFT, KR, "start")

NY = PB + 20
d.tone(24, NY, W - 48, 44, INFO)
d.t(44, NY + 27, "Memory 컨트롤러의 대상", 12.5, INK, KR, "start", 600)
d.t(236, NY + 27, "사용자 공간 메모리 · dentry · inode · TCP 소켓 버퍼", 12, MUTED, KR, "start")

d.legend(NY + 44 + 20, [("v2 컨트롤러", OK), ("계층 하나 · 태스크", ACC), ("5장 VFS 와 닿는 자리", INFO)])
d.save("06-02.cgroups-v2.svg")
print("ok 06-02.cgroups-v2", NY + 64)
