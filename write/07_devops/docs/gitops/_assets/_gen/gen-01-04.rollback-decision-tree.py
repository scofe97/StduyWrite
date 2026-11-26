# 타입 스펙: type-tree
# 3절 상황별 복구 수단 선택 — 장애 유형과 동기화 설정별 결정 트리
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 920, 568

d = D(W, H, "GITOPS · ROLLBACK DECISION TREE",
      "장애 유형과 동기화 설정별 복구 수단 결정 트리",
      "데이터 비가역성, 점진 배포 지표 실패, auto-sync 여부에 따라 여섯 복구 수단 중 하나로 분기하는 결정 트리",
      lead="무엇이 잘못됐나 · 데이터가 바뀌었나 · auto-sync 가 켜졌나를 차례로 따져 여섯 수단 중 하나를 고릅니다")

NH = 52
W_INT = 152
W_LEAF = 184

# ── 좌표 정의 (전부 4의 배수) ───────────────────────────────
# Col 0 (Root)
X0, W0, Y0 = 24, 136, 230
CY0 = 256

# Col 1 (Tier 1: 무엇이 잘못됐나 / 데이터가 바뀌었나)
X1 = 216
Y1A, Y1B, Y1C = 104, 180, 358
CY1A, CY1B, CY1C = Y1A + NH // 2, Y1B + NH // 2, Y1C + NH // 2  # 130, 206, 384

# Col 2 (Tier 2: Leaf 2개 + 그룹 2개)
X2 = 432
Y2A, Y2B = 104, 180
Y2C1, Y2C2 = 290, 426
CY2A, CY2B, CY2C1, CY2C2 = Y2A + NH // 2, Y2B + NH // 2, Y2C1 + NH // 2, Y2C2 + NH // 2  # 130, 206, 316, 452

# Col 3 (Tier 3: Leaf 4개)
X3 = 712
Y3_1, Y3_2, Y3_3, Y3_4 = 256, 324, 392, 460
CY3 = [y + NH // 2 for y in (Y3_1, Y3_2, Y3_3, Y3_4)]  # 282, 350, 418, 486

# ── 연결선 (노드보다 먼저 그린다 · 직각 버스) ──────────────
BX0 = 180
d.line(X0 + W0, CY0, BX0, CY0, MUTED, 1.2)
d.line(BX0, CY1A, BX0, CY1C, MUTED, 1.2)
for cy, col, mk in ((CY1A, ACC, "acc"), (CY1B, WARN, "warn"), (CY1C, INFO, "info")):
    d.arrow([(BX0, cy), (X1 - 2, cy)], col, mk, 1.3)

# Tier 1 -> Tier 2
d.arrow([(X1 + W_INT, CY1A), (X2 - 2, CY2A)], ACC, "acc", 1.4)
d.arrow([(X1 + W_INT, CY1B), (X2 - 2, CY2B)], WARN, "warn", 1.3)

BX1 = 396
d.line(X1 + W_INT, CY1C, BX1, CY1C, INFO, 1.2)
d.line(BX1, CY2C1, BX1, CY2C2, INFO, 1.2)
d.arrow([(BX1, CY2C1), (X2 - 2, CY2C1)], INFO, "info", 1.3)
d.arrow([(BX1, CY2C2), (X2 - 2, CY2C2)], INFO, "info", 1.3)

# Tier 2 -> Tier 3
BX2 = 608
d.line(X2 + W_INT, CY2C1, BX2, CY2C1, MUTED, 1.2)
d.line(BX2, CY3[0], BX2, CY3[1], MUTED, 1.2)
d.arrow([(BX2, CY3[0]), (X3 - 2, CY3[0])], OK, "ok", 1.3)
d.arrow([(BX2, CY3[1]), (X3 - 2, CY3[1])], WARN, "warn", 1.3)

d.line(X2 + W_INT, CY2C2, BX2, CY2C2, INFO, 1.2)
d.line(BX2, CY3[2], BX2, CY3[3], INFO, 1.2)
d.arrow([(BX2, CY3[2]), (X3 - 2, CY3[2])], INFO, "info", 1.3)
d.arrow([(BX2, CY3[3]), (X3 - 2, CY3[3])], INFO, "info", 1.3)

# ── 분기 라벨 (선 위로 8px 띄움) ───────────────────────────
d.t(BX2 + 8, CY3[0] - 8, "auto-sync ON", 11, OK, MONO, "start", 600)
d.t(BX2 + 8, CY3[1] - 8, "auto-sync OFF", 11, WARN, MONO, "start", 600)
d.t(BX2 + 8, CY3[2] - 8, "Helm", 12, INFO, MONO, "start", 600)
d.t(BX2 + 8, CY3[3] - 8, "K8s", 12, INFO, MONO, "start", 600)

# ── 노드: Col 0 Root ──────────────────────────────────────
d.box(X0, Y0, W0, NH, PAPER2, MUTED, 1.0, 6)
d.t(X0 + W0 // 2, Y0 + 22, "배포 장애", 13, INK, KR, "middle", 600)
d.t(X0 + W0 // 2, Y0 + 40, "v1 -> v2 이상", 12, MUTED, KR, "middle")

# ── 노드: Col 1 Tier 1 ────────────────────────────────────
d.box(X1, Y1A, W_INT, NH, PAPER2, MUTED, 1.0, 6)
d.t(X1 + W_INT // 2, Y1A + 22, "DB 비가역 변경", 13, INK, KR, "middle", 600)
d.t(X1 + W_INT // 2, Y1A + 40, "DROP · 타입", 12, MUTED, KR, "middle")

d.box(X1, Y1B, W_INT, NH, PAPER2, MUTED, 1.0, 6)
d.t(X1 + W_INT // 2, Y1B + 22, "점진 지표 실패", 13, INK, KR, "middle", 600)
d.t(X1 + W_INT // 2, Y1B + 40, "5xx > 5%", 12, MUTED, MONO, "middle")

d.box(X1, Y1C, W_INT, NH, PAPER2, MUTED, 1.0, 6)
d.t(X1 + W_INT // 2, Y1C + 22, "앱 코드 오류", 13, INK, KR, "middle", 600)
d.t(X1 + W_INT // 2, Y1C + 40, "DB 호환 유지", 12, MUTED, KR, "middle")

# ── 노드: Col 2 Tier 2 (Leaf 2 + 내부 2) ─────────────────
# Leaf: Roll Forward [Focal ACC]
d.tone(X2, Y2A, W_LEAF, NH, ACC, 6, "16", 1.4)
d.t(X2 + W_LEAF // 2, Y2A + 22, "Roll Forward", 13, ACC, MONO, "middle", 600)
d.t(X2 + W_LEAF // 2, Y2A + 40, "v3 수정 배포", 12, INK, KR, "middle")

# Leaf: Rollouts abort
d.tone(X2, Y2B, W_LEAF, NH, WARN, 6, "14", 1.0)
d.t(X2 + W_LEAF // 2, Y2B + 22, "Rollouts abort", 13, WARN, MONO, "middle", 600)
d.t(X2 + W_LEAF // 2, Y2B + 40, "100% v1 · Git v2", 12, INK, MONO, "middle")

# Group: GitOps (Argo CD)
d.box(X2, Y2C1, W_INT, NH, PAPER2, RULE, 1.0, 6)
d.t(X2 + W_INT // 2, Y2C1 + 22, "GitOps", 13, INK, MONO, "middle", 600)
d.t(X2 + W_INT // 2, Y2C1 + 40, "Argo CD", 12, MUTED, MONO, "middle")

# Group: 비GitOps
d.box(X2, Y2C2, W_INT, NH, PAPER2, RULE, 1.0, 6)
d.t(X2 + W_INT // 2, Y2C2 + 22, "비GitOps", 13, INK, KR, "middle", 600)
d.t(X2 + W_INT // 2, Y2C2 + 40, "푸시 · 단독", 12, MUTED, KR, "middle")

# ── 노드: Col 3 Tier 3 (Leaf 4) ──────────────────────────
leaves = [
    (Y3_1, OK,   "git revert",           "새 커밋 · Synced"),
    (Y3_2, WARN, "argocd app rollback",  "ID 지정 · OutOfSync"),
    (Y3_3, INFO, "helm rollback",        "Rev 3 -> Rev 4"),
    (Y3_4, INFO, "kubectl rollout undo", "Rev 2 -> 3 (RS1)"),
]
for y, col, cmd, sub in leaves:
    d.tone(X3, y, W_LEAF, NH, col, 6, "14", 1.0)
    d.t(X3 + W_LEAF // 2, y + 22, cmd, 12, col, MONO, "middle", 600)
    d.t(X3 + W_LEAF // 2, y + 40, sub, 12, INK, KR if any('가'<=c<='힣' for c in sub) else MONO, "middle")

# ── 범례 ─────────────────────────────────────────────────
LEG_Y = 524
d.legend(LEG_Y, [
    ("Git 정합 유지", OK),
    ("사후 Git 정리", WARN),
    ("비GitOps 복구", INFO),
    ("롤백 금지 (Roll Forward)", ACC),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-04.rollback-decision-tree.svg")
d.save(out_path)
print("ok gen-01-04.rollback-decision-tree")
