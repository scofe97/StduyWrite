# 06-02 §3 — cgroups v1 의 계층 여럿과 v2 의 계층 하나를 실제 트리 모양으로 견준다.
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
# 축약: 왼쪽의 그룹 a·b 와 태스크 하나는 출력에 없는 예시라 점선으로 그렸다. v1 컨트롤러 열둘 중 셋만
#       계층 예시에 놓았다 — 논점은 개수가 아니라 계층의 수다. systemctl 출력의 bpfilter_umh 줄은 생략.
# 타입 스펙: type-tree — 부모 → 자식 관계. 왼쪽은 작은 트리 셋, 오른쪽은 큰 트리 하나.
#           accent 는 컨트롤러 여덟이 모두 붙는 v2 의 루트 "/" 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 644
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §3",
      "v1 은 컨트롤러마다 트리, v2 는 트리 하나에 컨트롤러 전부",
      "v1 은 CPU 계정·메모리·블록 IO 처럼 컨트롤러가 그때그때 붙으며 계층이 따로 생겼고, 시스템의 "
      "모든 태스크가 계층마다 한 칸씩 들었다. v2 는 계층이 하나다. 루트 / 에 컨트롤러 여덟이 붙고, "
      "그 아래 user.slice·system.slice·docker 같은 그룹이 systemd 단위 이름 그대로 매달린다.",
      "systemd 의 slice 가 바로 이 트리의 가지입니다")

PY, PB = 112, 504          # 두 패널의 위·아래
LX0, LX1 = 24, 412         # v1 패널
RX0, RX1 = 436, 856        # v2 패널

# ── v1 ─────────────────────────────────────────────
d.box(LX0, PY, LX1 - LX0, PB - PY, PAPER2, WARN, 1.2, 8)
d.t(LX0 + 16, PY + 28, "cgroups v1", 15, WARN, MONO, "start", 600)
d.t(LX0 + 136, PY + 28, "계층 여럿", 13, INK, KR, "start", 600)

TS = 128
CXS = [LX0 + 68 + i * TS for i in range(3)]
hier = [("CPU 계정", "2.6.24"), ("메모리", "2.6.25"), ("블록 IO", "2.6.33")]
CY, CH = PY + 60, 48
RY = CY + CH + 28                 # 루트 "/"
KY = RY + 56                      # 자식 a·b
TASK_IN = [0, 1, 0]               # 태스크가 드는 자식 (예)
TY_ = KY + 84                     # 태스크 상자

# 연결선 먼저
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

# 두 패널 사이
d.arrow([(LX1 + 4, (PY + PB) / 2), (RX0 - 4, (PY + PB) / 2)], MUTED, "ar", 1.4)

# ── v2 ─────────────────────────────────────────────
d.box(RX0, PY, RX1 - RX0, PB - PY, PAPER2, RULE, 1.0, 8)
d.t(RX0 + 16, PY + 28, "cgroups v2", 15, ACC, MONO, "start", 600)
d.t(RX0 + 136, PY + 28, "계층 하나", 13, INK, KR, "start", 600)

FX0, FX1, FY, FH = RX0 + 16, RX1 - 16, PY + 44, 92
d.o.append(f'<rect x="{FX0}" y="{FY}" width="{FX1 - FX0}" height="{FH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(FX0 + 14, FY + 24, "/", 15, ACC, MONO, "start", 600)
d.t(FX1 - 14, FY + 24, "623 tasks · 5.8G", 12, MUTED, MONO, "end")
ctrls = ["CPU", "Memory", "I/O", "PID", "cpuset", "device", "rdma", "HugeTLB"]
for i, c in enumerate(ctrls):
    cx = FX0 + 56 + (i % 4) * 92
    cy = FY + 50 + (i // 4) * 26
    d.chip(cx, cy, c, OK, 11)

# 트리 행 (level, 이름, 수치)
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
# 가지: 각 노드에서 부모 레일로 가로선, 레일은 부모 바로 아래부터 마지막 자식까지
for i, (lv, name, val) in enumerate(tree):
    y = ys[i] - 4
    rail = TXB - 12 + IND * (lv - 1)
    d.line(rail, y, rail + 8, y, MUTED, 1.0)
    # 부모 찾기
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

# ── 아래: 메모리 컨트롤러의 대상 ─────────────────────
NY = PB + 20
d.tone(24, NY, W - 48, 44, INFO)
d.t(44, NY + 27, "Memory 컨트롤러의 대상", 12.5, INK, KR, "start", 600)
d.t(236, NY + 27, "사용자 공간 메모리 · dentry · inode · TCP 소켓 버퍼", 12, MUTED, KR, "start")

d.legend(NY + 44 + 20, [("v1 계층", WARN), ("v2 컨트롤러", OK), ("계층 하나 · 태스크", ACC),
                        ("5장 VFS 와 닿는 자리", INFO)])
d.save("06-02.cgroups-v1-v2.svg")
print("ok 06-02.cgroups-v1-v2", NY + 64)
