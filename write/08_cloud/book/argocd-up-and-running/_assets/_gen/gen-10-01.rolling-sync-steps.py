# 10-01 §3 — ApplicationSet 은 Application 4개를 한꺼번에 만들고, RollingSync 는 라벨로 가른 단계마다 Healthy 를 기다리며 sync 한다. maxUpdate 는 한 단계 안에서 동시에 sync 하는 개수를 제한한다.
# 본문 근거: 이 노트 ### 3 「ApplicationSet 과 Progressive Sync — 한꺼번에 만들고 단계별로 sync 한다」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 argocd-cmd-params-cm 의 applicationsetcontroller.enable.progressive.syncs 를 켠 뒤 ApplicationSet 을 적용했다.
#            Application 4개가 한꺼번에 OutOfSync/Missing 으로 만들어졌고 database 가 먼저 sync 되었다.
#            api-1 은 26초 뒤, api-2 는 17초 뒤(maxUpdate 1 이라 하나씩), frontend 는 17초 뒤에 시작했다(16:18:40 → 16:19:06 → :23 → :40).
#            켜기 전에는 같은 ApplicationSet 이 Application 4개를 만들기만 하고 sync 를 시작하지 않았다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/applicationset/Progressive-Syncs.md(RollingSync, steps, matchExpressions, maxUpdate, 켜는 방법).
# 타입 스펙: type-architecture — 왼쪽 ApplicationSet 에서 오른쪽 단계로 가는 한 방향 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 352
d = D(W, H, "ARGO CD UP AND RUNNING · 10-01 §3",
      "RollingSync 의 단계별 sync",
      "ApplicationSet golist 가 Application 4개를 OutOfSync 상태로 한꺼번에 만든다. 그 뒤 RollingSync 가 단계 1 database, 단계 2 backend 라벨의 api-1 과 api-2, 단계 3 frontend 순서로 sync 한다. "
      "각 단계는 앞 단계가 모두 Healthy 가 된 뒤 시작하고, 단계 2 는 maxUpdate 1 이라 api-1 이 Healthy 가 된 뒤에 api-2 를 시작한다.",
      "만들기는 한꺼번에, sync 는 단계마다")

# 왼쪽 ApplicationSet
AX, AY, AW, AH = 24, 99, 170, 110
d.tone(AX, AY, AW, AH, ACC, 6, "14", 1.4)
d.t(AX + AW / 2, AY + 38, "ApplicationSet", 13, INK, MONO, "middle", 600)
d.t(AX + AW / 2, AY + 60, "golist", 13, INK, MONO, "middle", 600)
d.t(AX + AW / 2, AY + 88, "4개 동시 생성", 12, MUTED)

SW, SH = 130, 56
SX = [250, 480, 710]
for x, h in zip(SX, ["단계 1", "단계 2", "단계 3"]):
    d.t(x + SW / 2, 112, h, 12, MUTED, KR, "middle", 600)

def box(x, y, name, sub):
    d.tone(x, y, SW, SH, INFO, 6, "14", 1.1)
    d.t(x + SW / 2, y + 24, name, 13, INK, MONO, "middle", 600)
    d.t(x + SW / 2, y + 44, sub, 12, MUTED)

box(SX[0], 126, "database", "label database")
box(SX[1], 126, "api-1", "label backend")
box(SX[1], 226, "api-2", "label backend")
box(SX[2], 176, "frontend", "label frontend")

# ApplicationSet → 단계 1
d.path(f"M {AX + AW + 2} 154 L {SX[0] - 2} 154", MUTED, 1.4, m="ar")
# 단계 1 → api-1
d.path(f"M {SX[0] + SW + 2} 154 L {SX[1] - 2} 154", OK, 1.4, m="ar")
d.chip((SX[0] + SW + SX[1]) / 2, 136, "26초", OK, size=12)
# api-1 → api-2 (maxUpdate 1)
cx = SX[1] + SW / 2
d.path(f"M {cx} {126 + SH + 2} L {cx} {226 - 2}", WARN, 1.4, m="ar")
d.chip(cx + 62, 204, "maxUpdate 1", WARN, size=12)
d.chip(cx - 42, 204, "17초", OK, size=12)
# api-2 → frontend
d.path(f"M {SX[1] + SW + 2} 254 L {SX[2] - 30} 254 L {SX[2] - 30} 212 L {SX[2] - 2} 212", OK, 1.4, m="ar")
d.chip(SX[1] + SW + 28, 272, "17초", OK, size=12)

d.legend(310, [("ApplicationSet", ACC), ("생성된 Application", INFO), ("Healthy 후 시작", OK), ("한 번에 하나", WARN)])
d.save("10-01.rolling-sync-steps.svg")
