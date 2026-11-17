# 06-01 흐름 뼈대 도식 — Pod 하나가 생성부터 시간이 흐른 뒤까지 거치는 여섯 단계
# 본문: nodeSelector 와 requests 를 가진 Pod 하나가 노드 다섯 대를 지나며 단계마다 걸러지고,
#   남은 노드끼리 점수를 겨뤄 한 곳에 묶이는 과정. 같은 Pod 를 단계 열마다 다시 그려 이동을 보인다.
# 타입 스펙: type-process — 왼쪽에서 오른쪽으로 단계가 이어지고 노드 행마다 결과가 갈리는 형태가
#   "누가 무엇을 보고 걸러내는가"를 그대로 보인다. 계층(layers)이나 격자(matrix)로는 탈락 지점의 순서가 사라진다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W = 1000
X = (24, 172, 336, 556, 680, 836)        # 생성 · 대기 · 필터 · 점수 · 바인딩 · 시간이 흐른 뒤
WD = (128, 128, 200, 104, 136, 136)
Y0, STRIDE, CH = 140, 72, 64
ROWS = 5
BOT = Y0 + (ROWS - 1) * STRIDE + CH       # 492

def rc(k): return Y0 + k * STRIDE + CH // 2   # 행 중심
def cx(j): return X[j] + WD[j] // 2
def right(j): return X[j] + WD[j]

d = D(W, BOT + 76, "KUBERNETES PATTERNS · 06-01",
      "새 Pod 하나가 노드에 묶이기까지",
      "requests cpu 500m, memory 1Gi 와 nodeSelector disktype=ssd 를 가진 Pod 하나가 노드 다섯 대를 지나는 여섯 단계입니다. "
      "필터 단계에서 node-1 은 메모리 부족, node-2 는 control-plane taint, node-3 은 selector 불일치로 떨어지고 "
      "node-4 와 node-5 가 점수 단계로 넘어갑니다. 점수가 높은 node-5 에 바인딩되며 이후 시간이 흐르면 축출이나 재조정이 일어납니다.",
      lead="노드 다섯 대를 끝까지 따라갑니다 · 점수 60 과 85 는 예시 값")

heads = ("1 생성", "2 대기", "3 필터", "4 점수", "5 바인딩", "6 시간이 흐른 뒤")
for j, h in enumerate(heads):
    d.t(cx(j), 120, h, 12, SOFT, KR, "middle", 600)

TALL_H = BOT - Y0
mid = Y0 + TALL_H // 2                    # 행 2 중심과 같다

# 1 생성
d.tone(X[0], Y0, WD[0], TALL_H, INFO, 6, "10", 1.0)
d.t(cx(0), mid - 56, "새 Pod", 14, INFO, KR, "middle", 600)
d.t(cx(0), mid - 28, "requests", 12, MUTED, KR)
d.t(cx(0), mid - 10, "cpu 500m", 12, INK, MONO)
d.t(cx(0), mid + 8, "memory 1Gi", 12, INK, MONO)
d.t(cx(0), mid + 36, "nodeSelector", 12, MUTED, MONO)
d.t(cx(0), mid + 54, "disktype=ssd", 12, INK, MONO)
d.t(cx(0), mid + 82, "nodeName: —", 12, MUTED, MONO)
# 2 대기
d.tone(X[1], Y0, WD[1], TALL_H, INFO, 6, "10", 1.0)
d.t(cx(1), mid - 40, "스케줄 큐", 14, INFO, KR, "middle", 600)
d.t(cx(1), mid - 14, "priority 순 정렬", 12, INK, KR)
d.t(cx(1), mid + 24, "schedulingGates", 12, MUTED, MONO)
d.t(cx(1), mid + 42, "있으면 대기", 12, MUTED, KR)

# 3 필터 — 노드 다섯
NODES = [
    ("node-1", "탈락", "Insufficient memory", "allocatable 800Mi", BAD, MONO),
    ("node-2", "탈락", "untolerated taint", "control-plane:NoSchedule", BAD, MONO),
    ("node-3", "탈락", "selector 불일치", "disktype=hdd", BAD, KR),
    ("node-4", "통과", "자원 충분", "disktype=ssd", OK, KR),
    ("node-5", "통과", "자원 충분", "disktype=ssd", ACC, KR),
]
for k, (n, st, why, det, c, f) in enumerate(NODES):
    y = Y0 + k * STRIDE
    foc = (k == 4)
    d.tone(X[2], y, WD[2], CH, c, 6, "16" if foc else "12", 1.4 if foc else 1.0)
    d.t(X[2] + 12, y + 20, n, 13, c, MONO, "start", 600)
    d.t(X[2] + WD[2] - 12, y + 20, st, 12, c, KR, "end", 600)
    d.t(X[2] + 12, y + 38, why, 12, INK, f, "start")
    d.t(X[2] + 12, y + 55, det, 12, MUTED, MONO if det[0].islower() else KR, "start")

# 4 점수 — 통과한 둘
for k, (sc, c, foc) in ((3, ("60", OK, False)), (4, ("85", ACC, True))):
    y = Y0 + k * STRIDE
    d.tone(X[3], y, WD[3], CH, c, 6, "16" if foc else "12", 1.4 if foc else 1.0)
    d.t(cx(3), y + 22, "점수", 12, MUTED, KR)
    d.t(cx(3), y + 50, sc, 20, c, MONO, "middle", 600)

# 5 바인딩
y4 = Y0 + 4 * STRIDE
d.tone(X[4], y4, WD[4], CH, ACC, 6, "16", 1.4)
d.t(cx(4), y4 + 20, "Binding", 13, ACC, MONO, "middle", 600)
d.t(cx(4), y4 + 38, "nodeName=node-5", 12, INK, MONO)
d.t(cx(4), y4 + 55, "kubelet 이 기동", 12, MUTED, KR)

# 6 시간이 흐른 뒤
d.tone(X[5], y4, WD[5], CH, WARN, 6, "12", 1.0)
d.t(cx(5), y4 + 20, "시간이 흐른 뒤", 13, WARN, KR, "middle", 600)
d.t(cx(5), y4 + 38, "NoExecute 축출", 12, INK, KR)
d.t(cx(5), y4 + 55, "descheduler 재조정", 12, MUTED, KR)

# ── 화살표 (전부 직각) ──────────────────────────────────────────────────
d.path(f"M {right(0)+3} {mid} L {X[1]-5} {mid}", INFO, 1.4, m="info")
BUS = right(1) + 18
d.line(right(1) + 2, mid, BUS, mid, INFO, 1.4)
d.line(BUS, rc(0), BUS, rc(4), INFO, 1.4)
for k in range(ROWS):
    d.path(f"M {BUS} {rc(k)} L {X[2]-5} {rc(k)}", INFO, 1.4, m="info")
d.path(f"M {right(2)+3} {rc(3)} L {X[3]-5} {rc(3)}", OK, 1.4, m="ok")
d.path(f"M {right(2)+3} {rc(4)} L {X[3]-5} {rc(4)}", ACC, 1.4, m="acc")
d.path(f"M {right(3)+3} {rc(4)} L {X[4]-5} {rc(4)}", ACC, 1.4, m="acc")
d.path(f"M {right(4)+3} {rc(4)} L {X[5]-5} {rc(4)}", ACC, 1.4, m="acc")

d.legend(BOT + 28, [("입력·대기", INFO), ("탈락", BAD), ("통과", OK),
                    ("선택된 노드", ACC), ("시간이 흐른 뒤", WARN)])
d.save("06-01.chapter-overview.svg")
print("ok chapter-overview")
