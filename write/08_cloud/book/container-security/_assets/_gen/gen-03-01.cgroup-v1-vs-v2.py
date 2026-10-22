# 타입 스펙: type-architecture — 두 존(v1 · v2)에 같은 프로세스를 하나씩 두고, v1 은 컨트롤러마다 다른 그룹으로 화살표가 갈라지고 v2 는 그룹 하나로 모이게 해 소속 구조의 차이를 보인다. focal 은 v2 의 ourgroup.
# 사실 출처: 노트 L189(mygroup · yourgroup · ourgroup 경로), L213(stat -fc %T 출력 tmpfs · cgroup2fs)
# Layout conventions: 존 폭 456(x=24·504), 존 y=100~388, 프로세스 노드 104×56, 대상 노드 폭 248, v1 대상 y=168·264(높이 56), v2 대상 y=184(높이 120). 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 984, 484


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "ARCHITECTURE · 03-01 §6",
      "v1 은 컨트롤러마다 다른 그룹에 속하고 v2 는 그룹 하나에 속합니다",
      "cgroups v1 에서는 한 프로세스가 /sys/fs/cgroup/memory/mygroup 과 /sys/fs/cgroup/pids/yourgroup 에 동시에 속한다. "
      "cgroups v2 에서는 /sys/fs/cgroup/ourgroup 하나에 들어가 그 그룹에 걸린 모든 컨트롤러의 통제를 함께 받는다. "
      "stat -fc %T /sys/fs/cgroup/ 출력이 tmpfs 면 v1, cgroup2fs 면 v2 이다.",
      lead="같은 프로세스가 어느 그룹에 속하는지가 두 버전을 가릅니다.")

ZY, ZH, ZW = 100, 288, 456


def zone(x, name, sub):
    d.o.append(f'<rect x="{x}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="5 5"/>')
    d.t(x + 16, ZY + 26, name, 12, INK, MONO, "start", 600)
    d.t(x + 16, ZY + 44, sub, 12, MUTED, KR, "start")


def proc(x, cy):
    d.box(x, cy - 28, 104, 56)
    d.t(x + 52, cy - 4, "프로세스", 13, INK, KR, "middle", 600)
    d.t(x + 52, cy + 16, "PID 하나", 12, MUTED, KR, "middle")


def target(x, y, h, path, sub, c):
    fit(path, 12, 248 - 16)
    d.tone(x, y, 248, h, c, 6, "14" if c != ACC else "1F", 1.6 if c == ACC else 1.1)
    d.t(x + 124, y + 24, path, 12, c, MONO, "middle", 600)
    d.t(x + 124, y + 44, sub, 12, MUTED, KR, "middle")


# v1
LX = 24
zone(LX, "CGROUPS V1", "컨트롤러마다 계층이 따로")
proc(LX + 24, 244)
t1c, t2c = 196, 292
bx = LX + 24 + 104 + 20          # 버스 x = 172
d.line(LX + 24 + 104, 244, bx, 244, SOFT, 1.3)
d.line(bx, t1c, bx, t2c, SOFT, 1.3)
d.arrow([(bx, t1c), (LX + 172 + 24 - 4, t1c)], SOFT, "soft", 1.3)
d.arrow([(bx, t2c), (LX + 172 + 24 - 4, t2c)], SOFT, "soft", 1.3)
target(LX + 172 + 24, 168, 56, "/sys/fs/cgroup/memory/mygroup", "memory 컨트롤러가 거는 한도", INFO)
target(LX + 172 + 24, 264, 56, "/sys/fs/cgroup/pids/yourgroup", "pids 컨트롤러가 거는 한도", INFO)
d.t(LX + ZW / 2, ZY + 244, "stat -fc %T /sys/fs/cgroup/", 11, MUTED, MONO, "middle")
d.chip(LX + ZW / 2, ZY + 268, "tmpfs", INFO, 11, 8)

# v2
RX = 504
zone(RX, "CGROUPS V2", "계층 하나로 통합")
proc(RX + 24, 244)
d.arrow([(RX + 24 + 104 + 2, 244), (RX + 172 + 24 - 4, 244)], ACC, "acc", 1.5)
target(RX + 172 + 24, 184, 120, "/sys/fs/cgroup/ourgroup", "모든 컨트롤러 통제", ACC)
for cx, label in ((RX + 172 + 24 + 52, "memory"), (RX + 172 + 24 + 124, "pids"), (RX + 172 + 24 + 192, "…")):
    d.chip(cx, 184 + 88, label, MUTED, 11, 7)
d.t(RX + ZW / 2, ZY + 244, "stat -fc %T /sys/fs/cgroup/", 11, MUTED, MONO, "middle")
d.chip(RX + ZW / 2, ZY + 268, "cgroup2fs", ACC, 11, 8)

d.legend(424, [("v1 · 계층마다 그룹", INFO), ("v2 · 그룹 하나", ACC)])
d.save(str(ASSETS / "03-01.cgroup-v1-vs-v2.svg"))
print("ok 03-01 cgroup-v1-vs-v2")
