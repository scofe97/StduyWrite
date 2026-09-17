# 개념 노트 「노드 간 경로를 누가 퍼뜨리는가」 · 세션 수가 노드 수의 제곱으로 는다.
# 논지는 "같은 노드 넷이 경로를 주고받는 두 가지 배선"이고, 세는 대상은 피어 세션이다.
# 타입 스펙: type-architecture — 구성요소와 연결. 두 배선을 나란히 놓아 대비한다.
#           type-bar(세션 수 비교)를 검토했으나 숫자만 남고 "누가 누구와 맺는가"가 사라져 기각.
#           세션은 방향이 없는 쌍이므로 arrow 가 아니라 line 으로 긋는다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 400
d = D(W, H, "TROUBLESHOOTING CONCEPT · BGP PEERING",
      "모두와 맺는 배선과 가운데로 모으는 배선",
      "노드는 자기 Pod 대역을 다른 노드에 알려야 노드를 넘는 Pod 통신이 생긴다. 모두가 모두와 맺으면 세션이 "
      "노드 수의 제곱에 비례해 늘고, 몇 대를 반사기로 두면 나머지는 반사기하고만 맺어 노드 수에 비례하는 선까지 내려간다.",
      lead="같은 노드 넷인데 왼쪽은 세션 여섯, 오른쪽은 넷입니다")

# ── 두 구역 — 좌우 대비. 지역 경계는 파선 사각형 ─────────────────────
d.o.append('<rect x="24" y="96" width="420" height="216" rx="8" fill="none" '
           f'stroke="{RULE}" stroke-width="0.8" stroke-dasharray="4,3"/>')
d.o.append('<rect x="476" y="96" width="420" height="216" rx="8" fill="none" '
           f'stroke="{RULE}" stroke-width="0.8" stroke-dasharray="4,3"/>')
d.t(40, 120, "풀메시 · 노드 넷", 13, SOFT, KR, "start", 600)
d.t(492, 120, "반사기 · 노드 넷과 반사기 하나", 13, SOFT, KR, "start", 600)

# ── 왼쪽 — 2 × 2 격자에 노드 넷, 쌍마다 선 하나 ──────────────────────
LN = [(64, 140), (280, 140), (64, 232), (280, 232)]          # box 좌상단
LC = [(x + 60, y + 24) for x, y in LN]                        # 중심
for a, b in [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]:
    d.line(LC[a][0], LC[a][1], LC[b][0], LC[b][1], MUTED, 1.0)
for i, (x, y) in enumerate(LN):
    d.box(x, y, 120, 48, PAPER2, RULE, 0.9, 6)
    d.t(x + 60, y + 22, f"노드 {i + 1}", 13, INK, KR, "middle", 600)
    d.t(x + 60, y + 40, "10.0.%d.0/24" % (i + 1), 11, MUTED, MONO)
d.chip(224, 296, "세션 6", MUTED, 12)

# ── 오른쪽 — 반사기 하나에 나머지가 모인다 ───────────────────────────
RR = (608, 140, 176, 48)
RC = (RR[0] + RR[2] // 2, RR[1] + RR[3] // 2)
RN = [(492, 232), (592, 232), (692, 232), (792, 232)]
for x, y in RN:
    d.line(RC[0], RR[1] + RR[3], x + 44, y, MUTED, 1.0)
d.tone(RR[0], RR[1], RR[2], RR[3], ACC, 6)
d.t(RC[0], RR[1] + 22, "반사기 · 컨트롤 플레인", 13, ACC, KR, "middle", 600)
d.t(RC[0], RR[1] + 40, "routeReflectorClusterID", 11, MUTED, MONO)
for i, (x, y) in enumerate(RN):
    d.box(x, y, 88, 48, PAPER2, RULE, 0.9, 6)
    d.t(x + 44, y + 22, f"노드 {i + 1}", 12, INK, KR, "middle", 600)
    d.t(x + 44, y + 40, "10.0.%d.0/24" % (i + 1), 11, MUTED, MONO)
d.chip(686, 296, "세션 4", MUTED, 12)

d.legend(344, [("피어 세션", MUTED), ("경로를 반사하는 노드", ACC), ("노드의 Pod 대역", INK)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-16.mesh-vs-reflector.svg"))
print("ok")
