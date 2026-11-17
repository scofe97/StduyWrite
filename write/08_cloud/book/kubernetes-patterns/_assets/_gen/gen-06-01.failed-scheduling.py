# 06-01 FailedScheduling 메시지 읽기 — 노드별 탈락 이유가 이유별 개수로 합쳐져 한 줄이 된다
# 본문: 노드 다섯 대가 모두 떨어진 장면(흐름 뼈대 도식은 두 대가 통과한 장면). 노드마다 탈락 이유를 하나씩 내고,
#   스케줄러가 같은 이유끼리 세어 「개수 이유」 문자열을 사전 순으로 정렬해 한 줄로 합친다(FitError.Error, sort.Strings).
#   그래서 메시지 줄 순서는 affinity(1) → Insufficient(2) → untolerated(2) 이다. 읽는 쪽은 가장 큰 덩어리부터 고친다.
# 타입 스펙: type-data-flow — 왼쪽 노드별 값이 가운데에서 이유별로 합쳐져 오른쪽 메시지로 나가는 흐름이
#   본문의 "다섯 개 이유가 한 줄로 합쳐진다"와 그대로 맞는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W = 1000
AX, AW = 24, 196          # 노드 열
BX, BW = 268, 190         # 이유별 묶음 열
CX, CW = 478, 470         # 메시지 열
Y0, STRIDE, CH = 152, 64, 52

def rc(k): return Y0 + k * STRIDE + CH // 2

NODES = [("node-1", "affinity/selector 불일치", INFO),
         ("node-2", "Insufficient memory", BAD), ("node-3", "Insufficient memory", BAD),
         ("node-4", "untolerated taint", WARN), ("node-5", "untolerated taint", WARN)]
GROUPS = [  # (이유, 개수, 색, 노드 행 범위, 메시지 줄) — 메시지 안 순서는 문자열 정렬 순
    ("node affinity/selector", 1, INFO, (0, 0), "1 node(s) didn't match Pod's node affinity/selector,"),
    ("Insufficient memory", 2, BAD, (1, 2), "2 Insufficient memory,"),
    ("untolerated taint", 2, WARN, (3, 4), "2 node(s) had untolerated taint {…}."),
]
BOT = Y0 + 4 * STRIDE + CH   # 460

d = D(W, 660, "KUBERNETES PATTERNS · 06-01",
      "FailedScheduling 메시지는 노드별 탈락 이유를 세어 합친 한 줄입니다",
      "노드 다섯 대가 모두 떨어진 장면입니다. node-1 은 affinity 와 selector 불일치, node-2 와 node-3 은 Insufficient memory, "
      "node-4 와 node-5 는 untolerated taint 로 탈락합니다. 스케줄러가 이유별 개수를 세어 문자열 순으로 정렬한 뒤 0/5 nodes are available 로 시작하는 한 줄을 만들고, "
      "읽는 쪽은 큰 덩어리부터 requests 조정, toleration 추가, 노드 라벨 확인으로 고칩니다.",
      lead="통과한 노드가 하나도 없는 경우 · 메시지 안 이유는 개수 순이 아니라 문자열 순으로 정렬됩니다")

d.t(AX, 112, "노드별 탈락 이유", 12, SOFT, KR, "start", 600)
d.t(BX, 112, "이유별 개수", 12, SOFT, KR, "start", 600)
d.t(CX, 112, "이벤트 메시지 한 줄 (줄바꿈은 표시용)", 12, SOFT, KR, "start", 600)

for k, (n, why, c) in enumerate(NODES):
    y = Y0 + k * STRIDE
    d.tone(AX, y, AW, CH, c, 6, "12", 1.0)
    d.t(AX + 12, y + 22, n, 13, c, MONO, "start", 600)
    d.t(AX + 12, y + 40, why, 12, INK, MONO if why[0].isascii() and "불" not in why else KR, "start")

BUS = AX + AW + 20
# 메시지 상자
d.box(CX, Y0 - 28, CW, BOT - Y0 + 28, PAPER2, RULE, 0.9, 6)
d.t(CX + 14, Y0 - 6, "0/5 nodes are available:", 11, INK, MONO, "start", 600)

for (name, cnt, c, (r0, r1), msg) in GROUPS:
    cy = (rc(r0) + rc(r1)) // 2
    h = (rc(r1) - rc(r0)) + CH
    d.tone(BX, cy - h // 2, BW, h, c, 6, "12", 1.0)
    d.t(BX + 12, cy - 4, f"× {cnt}", 16, c, MONO, "start", 600)
    d.t(BX + 12, cy + 16, name, 12, INK, MONO, "start")
    # 노드 → 묶음: 버스 라인 후 가운데로 직각 진입
    for r in range(r0, r1 + 1):
        d.line(AX + AW + 2, rc(r), BUS, rc(r), c, 1.4)
    if r0 != r1:
        d.line(BUS, rc(r0), BUS, rc(r1), c, 1.4)
    d.path(f"M {BUS} {cy} L {BX-5} {cy}", c, 1.4, m={BAD: "bad", WARN: "warn", INFO: "info"}[c])
    # 묶음 → 메시지 줄
    d.path(f"M {BX+BW+3} {cy} L {CX-5} {cy}", c, 1.4, m={BAD: "bad", WARN: "warn", INFO: "info"}[c])
    d.t(CX + 14, cy + 4, msg, 11, c, MONO, "start", 600)

# 처방 — 큰 덩어리부터
SY = BOT + 36
d.t(24, SY, "처방 — 가장 큰 덩어리부터", 12, SOFT, KR, "start", 600)
FIX = [("Insufficient memory", "requests 줄이기 · 노드 추가", BAD),
       ("untolerated taint", "Pod 에 toleration 추가", WARN),
       ("affinity/selector", "노드 라벨 확인", INFO)]
for i, (a, b, c) in enumerate(FIX):
    x = 24 + i * 312
    d.tone(x, SY + 16, 296, 64, c, 6, "12", 1.0)
    d.t(x + 14, SY + 40, a, 12, c, MONO, "start", 600)
    d.t(x + 14, SY + 64, b, 14, INK, KR, "start", 600)

d.legend(SY + 112, [("자원", BAD), ("taint", WARN), ("affinity·selector", INFO)])
d.save("06-01.failed-scheduling.svg")
print("ok failed-scheduling")
