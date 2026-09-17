# 2026-09-14 B(업그레이드 2분 뒤) 문항 · 문제 소개 — 무대.
# 이 클러스터가 어떻게 생겼고 경로가 누구를 거쳐 퍼지는가를 그린다. 사건은 two-route-losses 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 셀렉터가 라벨로 반사기를 고르는 자리가 focal.
#           세션은 방향이 없는 쌍이라 arrow 가 아니라 line 으로 긋는다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 508
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-14 B",
      "경로는 컨트롤 플레인 노드를 거쳐 퍼집니다",
      "kubeadm 으로 여러 해 운영한 큰 클러스터다. 노드가 많아 Calico 를 풀메시 대신 경로 반사기 구성으로 바꿔 두었고, "
      "반사기 역할은 컨트롤 플레인 노드가 맡는다. 어느 노드가 반사기인지는 BGPPeer 리소스의 셀렉터가 노드 라벨로 고른다.",
      lead="어느 노드가 반사기인지를 정하는 것은 노드에 붙은 라벨 하나입니다")

# ── 셀렉터 — 이 도식의 focal ──────────────────────────────────
SX, SY, SW, SH = 300, 100, 400, 68
d.tone(SX, SY, SW, SH, ACC, 8)
d.t(SX + SW // 2, SY + 26, "BGPPeer · 반사기를 고르는 조건", 13, ACC, KR, "middle", 600)
d.t(SX + SW // 2, SY + 50, "peerSelector: node-role.kubernetes.io/master", 12, INK, MONO)
d.arrow([(SX + SW // 2, SY + SH), (SX + SW // 2, 208)], ACC, "acc", 1.6)

# ── 반사기 — 컨트롤 플레인 노드 둘 ────────────────────────────
RR = [(296, 212), (528, 212)]
for i, (x, y) in enumerate(RR):
    d.box(x, y, 176, 68, PAPER2, RULE, 0.9, 6)
    d.t(x + 88, y + 26, f"컨트롤 플레인 {i + 1}", 13, INK, KR, "middle", 600)
    d.t(x + 88, y + 50, "반사기", 12, MUTED, KR)

# ── 워커 — 자기 Pod 대역을 광고한다 ───────────────────────────
WK = [(64, 356), (412, 356), (760, 356)]
for i, (x, y) in enumerate(WK):
    d.box(x, y, 176, 68, PAPER2, RULE, 0.9, 6)
    d.t(x + 88, y + 26, f"워커 {i + 1}", 13, INK, KR, "middle", 600)
    d.t(x + 88, y + 50, "10.244.%d.0/24" % (i + 1), 12, OK, MONO)

# 세션 — 워커마다 반사기 둘과 맺는다
for wx, wy in WK:
    for rx, ry in RR:
        d.line(wx + 88, wy, rx + 88, ry + 68, MUTED, 1.0)

d.chip(500, 316, "iBGP 세션", MUTED, 12)

d.legend(452, [("반사기와 맺은 세션", MUTED), ("라벨로 고르는 조건", ACC), ("노드가 광고하는 Pod 대역", OK)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-14.upgrade-rr-topology.svg"))
print("ok")
