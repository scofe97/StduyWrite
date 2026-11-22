# 타입 스펙: type-tree
# 3절 wfapi 의 계층과 FlowNode — run → stage → flow node 3단계 계층과 조회 엔드포인트
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER2, KR, MONO

W, H = 920, 460

d = D(W, H, "JENKINS · WFAPI HIERARCHY",
      "wfapi 의 계층과 FlowNode",
      "run, stage, flow node 의 3단계 계층 구조와 계층별 탐색 경로",
      lead="run → stage → flow node 3단계 계층과 엔드포인트 탐색 경로")

# ── 왼쪽 사양 카드 (계층명 및 조회 경로) ────────────────────────────────────
X0_CARD = 36
W_CARD = 264

# Tier 0 사양
d.box(X0_CARD, 112, W_CARD, 60, PAPER2, RULE, 1.0)
d.t(X0_CARD + 12, 128, "TIER 0 · RUN", 9, SOFT, MONO, "start", 600)
d.t(X0_CARD + 12, 146, "GET /job/{name}/{buildNumber}/", 10.5, INFO, MONO, "start")
d.t(X0_CARD + 12, 161, "  wfapi/describe", 10.5, INFO, MONO, "start")

# Tier 1 사양
d.box(X0_CARD, 220, W_CARD, 60, PAPER2, RULE, 1.0)
d.t(X0_CARD + 12, 236, "TIER 1 · STAGE", 9, SOFT, MONO, "start", 600)
d.t(X0_CARD + 12, 254, "execution/node/{nodeId}/", 10.5, INFO, MONO, "start")
d.t(X0_CARD + 12, 269, "  wfapi/describe", 10.5, INFO, MONO, "start")

# Tier 2 사양
d.box(X0_CARD, 328, W_CARD, 60, PAPER2, RULE, 1.0)
d.t(X0_CARD + 12, 344, "TIER 2 · FLOW NODE", 9, SOFT, MONO, "start", 600)
d.t(X0_CARD + 12, 362, "stageFlowNodes[]", 11, INFO, MONO, "start")
d.t(X0_CARD + 12, 377, "flow node", 12, MUTED, KR, "start")

# 영역 구분 수직 점선
d.line(320, 104, 320, 396, RULE, 0.8, dash="4 4")

# ── 오른쪽 계층 트리 연결선 (노드보다 먼저 렌더링) ───────────────────────────
# Root (cx=632) → Stage 1 (cx=500), Stage 2 (cx=764)
d.path("M 632 166 L 632 194 L 500 194 L 500 226", MUTED, sw=1.0)
d.path("M 632 194 L 764 194 L 764 226", MUTED, sw=1.0)

# Stage 1 (cx=500) → FlowNode 1 (cx=416), FlowNode 2 (cx=584)
d.path("M 500 274 L 500 302 L 416 302 L 416 334", MUTED, sw=1.0)
d.path("M 500 302 L 584 302 L 584 334", MUTED, sw=1.0)

# ── 오른쪽 계층 트리 노드 ──────────────────────────────────────────────────
# Root 노드: Run (단 하나의 focal 적용)
d.box(544, 118, 176, 48, PAPER2, ACC, 1.2)
d.t(632, 140, "run", 14, ACC, KR, "middle", 600)
d.t(632, 156, "status · stages[]", 11, MUTED, MONO, "middle")

# Stage 1 노드: stage · id: 5
d.box(412, 226, 176, 48, PAPER2, RULE, 1.0)
d.t(500, 248, "stage · id: 5", 13, INK, KR, "middle", 600)
d.t(500, 264, "stageFlowNodes[]", 11, MUTED, MONO, "middle")

# Stage 2 노드: stage · id: 8
d.box(676, 226, 176, 48, PAPER2, RULE, 1.0)
d.t(764, 248, "stage · id: 8", 13, INK, KR, "middle", 600)
d.t(764, 264, "status", 11, MUTED, MONO, "middle")

# FlowNode 1: Git
d.box(340, 334, 152, 48, PAPER2, RULE, 0.8)
d.t(416, 356, "Git", 13, INK, KR, "middle", 600)
d.t(416, 372, "flow node", 12, MUTED, KR, "middle")

# FlowNode 2: Shell Script
d.box(508, 334, 152, 48, PAPER2, RULE, 0.8)
d.t(584, 356, "Shell Script", 13, INK, KR, "middle", 600)
d.t(584, 372, "flow node", 12, MUTED, KR, "middle")

# ── 범례 (Legend) ───────────────────────────────────────────────────────────
d.legend(412, [("run", ACC), ("조회 경로", INFO), ("Stage / FlowNode", MUTED)])

d.save("08-02.wfapi-hierarchy.svg")
