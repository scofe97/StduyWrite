# 01-01 §1 — Application 은 Synced 와 OutOfSync 사이를 오간다. Git 의 Target state 나 클러스터의 Live state 가 바뀌면 OutOfSync 가 되고, Sync 가 Live state 를 Target state 로 옮겨 Synced 로 돌린다.
# 본문 근거: 이 노트 ### 1 「구성 드리프트를 Application 단위로 막기」.
# 공식 근거: argo-cd.readthedocs.io stable core_concepts(Target state · Live state · Sync status · Sync),
#            operator-manual/architecture 의 application controller("detects OutOfSync application state and optionally takes corrective action").
# 타입 스펙: type-state — 상태 둘과 전이가 이야기의 전부이고, 전이마다 무엇이 일으키는지가 라벨이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 412
d = D(W, H, "ARGO CD UP AND RUNNING · 01-01 §1",
      "Application 의 Sync status 가 바뀌는 길",
      "Application 은 Live state 와 Target state 가 같은 Synced 상태에서 출발한다. Git 의 Target state 가 바뀌거나 클러스터의 Live state 가 수동으로 바뀌면 "
      "OutOfSync 가 되고, Sync 가 Live state 를 Target state 로 옮기면 다시 Synced 가 된다.",
      "Git 이 바뀌어도 클러스터를 손으로 고쳐도 OutOfSync 가 되고, Sync 를 거쳐야 Synced 로 돌아옵니다")

BW, BH = 224, 100
LX, RX, SY = 100, 556, 124          # 왼쪽 상태 x, 오른쪽 상태 x, 상태 y
LR, RL = LX + BW, RX                # 왼쪽 상태의 오른쪽 모서리, 오른쪽 상태의 왼쪽 모서리


def state(x, title, sub, c):
    d.tone(x, SY, BW, BH, c, 8, "14", 1.4)
    d.t(x + BW / 2, SY + 44, title, 16, c, MONO, "middle", 600)
    d.t(x + BW / 2, SY + 72, sub, 12, MUTED, KR)


state(LX, "Synced", "Live state 가 Target state 와 같음", OK)
state(RX, "OutOfSync", "Live state 가 Target state 와 다름", WARN)

# Synced → OutOfSync: 두 갈래 원인
for y, label in ((SY + 26, "Git 의 Target state 변경"), (SY + 74, "Live state 의 수동 변경")):
    d.path(f"M {LR + 2} {y} L {RL - 4} {y}", MUTED, 1.4, m="ar")
    d.t((LR + RL) / 2, y - 9, label, 12, MUTED, KR, "middle")

# OutOfSync → Synced: Sync
by = SY + BH
d.path(f"M {RX + BW / 2} {by + 2} L {RX + BW / 2} {by + 70} L {LX + BW / 2} {by + 70} L {LX + BW / 2} {by + 4}", ACC, 1.6, m="acc")
d.chip((LR + RL) / 2, by + 70, "Sync", ACC, 13)
d.t((LR + RL) / 2, by + 98, "Live state 를 Target state 로 이동", 12, MUTED, KR, "middle")

d.legend(354, [("차이 없음", OK), ("차이 있음", WARN), ("Sync 전이", ACC)])
d.save("01-01.sync-status-cycle.svg")
