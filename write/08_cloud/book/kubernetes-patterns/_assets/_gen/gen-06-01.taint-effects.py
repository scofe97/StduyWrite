# 06-01 taint effect 셋 — 새 Pod·이미 도는 Pod·toleration 있는 Pod 에 각각 무엇을 하는가
# 본문: NoSchedule 은 새 배치만, PreferNoSchedule 은 점수만, NoExecute 는 이미 도는 Pod 까지 내보낸다.
# 타입 스펙: type-dp-security-matrix — 행(effect) × 열(Pod 의 처지) 격자에서 칸마다 결과가 갈리는 비교이고,
#   차단·허용·조건부가 색으로 한눈에 읽혀야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W = 960
RX, RW = 24, 212
CX0, CW, GAP = 248, 224, 12
HY = 104
Y0, RH, RG = 156, 76, 12
def cxk(j): return CX0 + j * (CW + GAP)

d = D(W, Y0 + 3 * (RH + RG) + 64, "KUBERNETES PATTERNS · 06-01",
      "effect 셋은 이미 도는 Pod 를 다르게 다룹니다",
      "행은 taint 의 effect 셋이고 열은 Pod 의 처지 셋입니다. NoSchedule 은 새 Pod 의 배치만 막고 이미 도는 Pod 는 그대로 두며, "
      "PreferNoSchedule 은 새 Pod 의 점수만 낮춥니다. NoExecute 만 이미 도는 Pod 를 축출하고, toleration 에 tolerationSeconds 300 이 있으면 300초 뒤에 축출합니다.",
      lead="이미 도는 Pod 를 내보내는 effect 는 NoExecute 하나뿐입니다")

COLS = [("새 Pod", "toleration 없음"), ("이미 도는 Pod", "toleration 없음"), ("toleration 있는 Pod", "tolerationSeconds: 300")]
for j, (a, b) in enumerate(COLS):
    d.t(cxk(j) + CW // 2, HY, a, 13, INK, KR, "middle", 600)
    d.t(cxk(j) + CW // 2, HY + 20, b, 11, MUTED, KR if any('가'<=ch<='힣' for ch in b) else MONO)
d.line(RX, HY + 34, W - 24, HY + 34, RULE, 0.8)

ROWS = [("NoSchedule", "새 배치만 막음"), ("PreferNoSchedule", "가능하면 피함"), ("NoExecute", "장애 노드 기본 300초")]
CELLS = [
    [("배치 안 함", "필터에서 탈락", BAD, KR), ("그대로 실행", "영향 없음", OK, KR), ("배치 가능", "필터 통과", OK, KR)],
    [("가능하면 피함", "점수에서 불리", WARN, KR), ("그대로 실행", "영향 없음", OK, KR), ("배치 가능", "불이익 없음", OK, KR)],
    [("배치 안 함", "필터에서 탈락", BAD, KR), ("축출", "노드에서 내보냄", ACC, KR), ("300초 뒤 축출", "tolerationSeconds: 300", WARN, KR)],
]
for i, (en, sub) in enumerate(ROWS):
    y = Y0 + i * (RH + RG)
    d.box(RX, y, RW, RH, PAPER2, RULE, 0.9, 6)
    d.t(RX + 14, y + 32, en, 13, INK, MONO, "start", 600)
    d.t(RX + 14, y + 54, sub, 12, MUTED, KR, "start")
    for j, (t1, t2, c, f) in enumerate(CELLS[i]):
        foc = (c == ACC)
        d.tone(cxk(j), y, CW, RH, c, 6, "16" if foc else "12", 1.4 if foc else 1.0)
        d.t(cxk(j) + 14, y + 32, t1, 14, c, KR, "start", 600)
        d.t(cxk(j) + 14, y + 54, t2, 12, MUTED, KR if any('가'<=ch<='힣' for ch in t2) else MONO, "start")

LY = Y0 + 3 * (RH + RG) + 8
d.legend(LY, [("배치·유지 가능", OK), ("조건부·불리", WARN), ("배치 막음", BAD), ("축출", ACC)])
d.save("06-01.taint-effects.svg")
print("ok taint-effects")
