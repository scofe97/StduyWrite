# §5.4.2 원문 밖 보강 · 라우트 리플렉션 — 리플렉터가 누구에게 되비추는가.
# 출처: RFC 4456 §5 Terminology and Concepts · §6 Operation (Figure 3 의 구성 요소)
# 논지는 "되비추는 방향"이라 노드를 가로로 펴고 화살표를 전부 수평으로 둔다.
# 타입 스펙: type-architecture — 구성요소와 연결. 클러스터 경계로 클라이언트와 논클라이언트를 가른다.
#           type-flowchart 를 검토했으나 판단 단계가 아니라 배선이 논지라 기각.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 1000, 448
d = D(W, H, "RFC 4456 §5 · §6 · ROUTE REFLECTION",
      "리플렉터는 어느 쪽에서 받았는지로 되비출 곳을 정합니다",
      "리플렉터와 그 클라이언트가 클러스터 하나를 이룹니다. 클라이언트에게 받은 경로는 논클라이언트와 다른 클라이언트 모두에게 "
      "되비추고, 논클라이언트에게 받은 경로는 클라이언트에게만 되비춥니다. 그래서 클라이언트끼리는 서로 맺지 않아도 되고 "
      "논클라이언트끼리는 여전히 그물로 맺어야 합니다.",
      lead="클라이언트는 리플렉터 한 대와만 맺고, 논클라이언트는 자기들끼리 그물을 유지합니다")

RY1, RY2 = 152, 280          # 두 행 — 화살표가 수평으로 지나가는 높이
BW, BH = 208, 72

# ── 클러스터 경계 — 라벨은 경계선 위가 아니라 안쪽 여백에 둔다 ────
d.o.append('<rect x="24" y="84" width="536" height="268" rx="10" fill="none" '
           f'stroke="{ACC}55" stroke-width="1.0" stroke-dasharray="5,4"/>')
d.t(48, 104, "CLUSTER", 9, SOFT, MONO, "start")

# ── 리플렉터 — 두 행에 걸치는 세로 상자 ─────────────────────────
RRX, RRY, RRH = 336, RY1 - 36, (RY2 + 36) - (RY1 - 36)
d.tone(RRX, RRY, 200, RRH, ACC, 8)
d.t(RRX + 100, RRY + 74, "리플렉터", 14, ACC, KR, "middle", 600)
d.t(RRX + 100, RRY + 96, "RR", 12, MUTED, MONO)

def node(x, y, title, sub, c):
    d.box(x, y - BH // 2, BW, BH, PAPER2, RULE, 0.9, 6)
    d.t(x + BW // 2, y - 6, title, 13, c, KR, "middle", 600)
    d.t(x + BW // 2, y + 16, sub, 12, MUTED, MONO)

# 화살표를 먼저 그려 상자가 위에 앉게 한다
d.arrow([(256, RY1 - 14), (RRX, RY1 - 14)], OK, "ok", 1.6)            # 클라이언트 → RR
d.arrow([(RRX, RY1 + 14), (256, RY1 + 14)], INFO, "info", 1.6)        # RR → 클라이언트
d.arrow([(256, RY2 + 14), (RRX, RY2 + 14)], OK, "ok", 1.6)
d.arrow([(RRX, RY2 - 14), (256, RY2 - 14)], INFO, "info", 1.6)
d.arrow([(RRX + 200, RY1 - 14), (744, RY1 - 14)], OK, "ok", 1.6)      # RR → 논클라이언트
d.arrow([(744, RY1 + 14), (RRX + 200, RY1 + 14)], INFO, "info", 1.6)  # 논클라이언트 → RR

node(48, RY1, "클라이언트", "RTR-A", INK)
node(48, RY2, "클라이언트", "RTR-B", INK)
node(744, RY1, "논클라이언트", "RTR-D", INK)
node(744, RY2, "논클라이언트", "RTR-E", INK)

# ── 같은 무리 안의 세션 — 방향이 없으므로 선으로 ────────────────
MID = (RY1 + RY2) // 2
d.line(152, RY1 + 36, 152, RY2 - 36, MUTED, 1.0, "4,3")
d.chip(152, MID, "맺지 않아도 됨", MUTED, 11)
d.line(848, RY1 + 36, 848, RY2 - 36, OK, 1.2)
d.chip(848, MID, "그물 유지", OK, 11)

d.legend(392, [("되비추는 쪽으로 나가는 경로", OK), ("리플렉터가 받는 경로", INFO),
               ("클러스터의 중심", ACC), ("없어도 되는 세션", MUTED)])
d.save(str(pathlib.Path(__file__).resolve().parent.parent / "05-02.rr-cluster.svg"))
print("ok")
