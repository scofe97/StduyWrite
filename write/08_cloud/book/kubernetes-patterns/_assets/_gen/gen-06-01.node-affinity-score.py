# 06-01 node affinity 의 hard 와 soft — required 가 거르고 preferred 가 점수를 더한다
# 본문: Ex 6-4. 노드 셋(numberCores 2·4·8, 마지막은 control-plane-node)에 required numberCores Gt 3 과
#   preferred weight 1 metadata.name NotIn control-plane-node 를 적용한 결과. 다른 점수는 같다고 둔다.
# 타입 스펙: type-process — 후보 → 필터 → 점수 → 선택으로 이어지는 단계 흐름이고, 노드 행마다 결과가 갈린다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W = 900
X = (24, 240, 456, 712)
WD = (176, 176, 216, 164)
Y0, STRIDE, CH = 176, 80, 64
def rc(k): return Y0 + k * STRIDE + CH // 2
def right(j): return X[j] + WD[j]
BOT = Y0 + 2 * STRIDE + CH

d = D(W, BOT + 76, "KUBERNETES PATTERNS · 06-01",
      "required 가 거르고 preferred 가 점수를 더합니다",
      "후보 노드 셋은 numberCores 라벨이 2, 4, 8 이고 마지막이 control-plane-node 입니다. required numberCores Gt 3 이 numberCores 2 인 node-a 를 거르고, "
      "남은 node-b 와 control-plane-node 중 preferred metadata.name NotIn control-plane-node 에 맞는 node-b 가 weight 1 점을 얻어 선택됩니다.",
      lead="다른 점수 플러그인의 값은 같다고 둡니다")

HEAD = [("후보 노드", "numberCores 라벨"), ("required — 필터", "numberCores Gt 3"),
        ("preferred — 점수", "metadata.name NotIn"), ("선택", "점수 합이 가장 높은 노드")]
for j, (a, b) in enumerate(HEAD):
    d.t(X[j], 108, a, 12, SOFT, KR, "start", 600)
    d.t(X[j], 126, b, 11, MUTED, KR if any('가'<=ch<='힣' for ch in b) else MONO, "start")
d.t(X[2], 142, "control-plane-node · weight 1", 11, MUTED, MONO, "start")

ROWS = [("node-a", "numberCores=2", False, "탈락", "2 Gt 3 거짓"),
        ("node-b", "numberCores=4", True, "통과", "4 Gt 3 참"),
        ("control-plane-node", "numberCores=8", True, "통과", "8 Gt 3 참")]
for k, (n, lab, ok, st, why) in enumerate(ROWS):
    y = Y0 + k * STRIDE
    d.box(X[0], y, WD[0], CH, PAPER2, RULE, 0.9, 6)
    d.t(X[0] + 12, y + 26, n, 13, INK, MONO, "start", 600)
    d.t(X[0] + 12, y + 46, lab, 12, MUTED, MONO, "start")
    c = OK if ok else BAD
    d.tone(X[1], y, WD[1], CH, c, 6, "12", 1.0)
    d.t(X[1] + 12, y + 26, st, 13, c, KR, "start", 600)
    d.t(X[1] + 12, y + 46, why, 12, INK, MONO, "start")
    d.path(f"M {right(0)+3} {rc(k)} L {X[1]-5} {rc(k)}", c, 1.4, m="ok" if ok else "bad")

# 점수 열 — 필터를 통과한 둘
for k, (pt, sub, c, foc) in ((1, ("+1", "NotIn 조건 일치", "hit", True)), (2, ("+0", "NotIn 조건 불일치", "miss", False))):
    y = Y0 + k * STRIDE
    if c == "hit":
        d.tone(X[2], y, WD[2], CH, ACC, 6, "16", 1.4)
    else:
        d.box(X[2], y, WD[2], CH, PAPER2, RULE, 0.9, 6)
    d.t(X[2] + 12, y + 28, pt, 18, ACC if c == "hit" else MUTED, MONO, "start", 600)
    d.t(X[2] + 12, y + 50, sub, 12, INK if c == "hit" else MUTED, KR, "start")
    d.path(f"M {right(1)+3} {rc(k)} L {X[2]-5} {rc(k)}", OK, 1.4, m="ok")

# 선택
y = Y0 + STRIDE
d.tone(X[3], y, WD[3], CH, ACC, 6, "16", 1.4)
d.t(X[3] + 12, y + 28, "node-b", 14, ACC, MONO, "start", 600)
d.t(X[3] + 12, y + 50, "바인딩 대상", 12, INK, KR, "start")
d.path(f"M {right(2)+3} {rc(1)} L {X[3]-5} {rc(1)}", ACC, 1.4, m="acc")

d.legend(BOT + 28, [("required 탈락", BAD), ("required 통과", OK), ("선택", ACC)])
d.save("06-01.node-affinity-score.svg")
print("ok node-affinity-score")
