# 타입 스펙: type-process
# 클러스터 업그레이드·ETCD 백업·복구 — 노드(레인) × 업그레이드 단계(열) 격자
# 축약: process 스펙의 IN/OUT 칩·tool 줄은 쓰지 않는다. 칸마다 그 시점의 버전과 하는 일만 둔다.
# 같은 노드를 단계마다 다시 그려, 칸 사이의 버전 차이로 진행과 버전 스큐를 보인다.
# 근거: kubernetes.io v1.37 「Upgrading kubeadm clusters」·「Upgrading Linux nodes」·「Version Skew Policy」 (2026-11-16 확인)
import sys
sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

OLD, NEW = "v1.36", "v1.37"

LANES = [("CP1", "첫 컨트롤 플레인"), ("CP2", "추가 컨트롤 플레인"), ("CP3", "추가 컨트롤 플레인"),
         ("W1", "워커"), ("W2", "워커")]
STEPS = ["시작", "CP1", "CP2", "CP3", "워커 W1", "워커 W2"]
FOCAL_STEP = 1

C_OLD, C_DO, C_NEW = INFO, WARN, OK
WAIT = (OLD, "대기", C_OLD)
DONE = (NEW, "완료", C_NEW)
CELLS = {
    0: [WAIT] * 5,
    1: [(NEW, "apply → kubelet", C_DO), WAIT, WAIT, WAIT, WAIT],
    2: [DONE, (NEW, "node → kubelet", C_DO), WAIT, WAIT, WAIT],
    3: [DONE, DONE, (NEW, "node → kubelet", C_DO), WAIT, WAIT],
    4: [DONE, DONE, DONE, (NEW, "node → kubelet", C_DO), WAIT],
    5: [DONE, DONE, DONE, DONE, (NEW, "node → kubelet", C_DO)],
}
# 맨 아래 점검 줄: 그 단계가 지키는 스큐 조건
CHECK = ["API 서버 같음", "API 서버 1단 차", "API 서버 1단 차", "addon 갱신", "kubelet ≤ API", "kubelet ≤ API"]

# 좌표 공식 (process §2 의 골격을 본문 폭에 맞춰 늘림, 모두 4의 배수)
W = 920
TOP = 96
LABEL_W = 120
RIGHT = 28
N_S, N_L = len(STEPS), len(LANES)
SLOT_W = (W - LABEL_W - RIGHT) // N_S
SLOT_W -= SLOT_W % 4                           # 128
HEAD_H = 36
LANE_H = 72
CHECK_H = 52
NODE_W = SLOT_W - 12                           # 열이 여섯이라 칸 여백을 줄여 동작 라벨이 칸 안에 들게 한다
NODE_H = LANE_H - 16
GRID_X = LABEL_W
LEG_Y = TOP + HEAD_H + N_L * LANE_H + CHECK_H + 20
H = LEG_Y + 48


def has_kr(txt):
    return any('가' <= ch <= '힣' for ch in txt)


d = D(W, H, "KUBERNETES · KUBEADM UPGRADE",
      "컨트롤 플레인 한 대씩, 그다음 워커",
      "v1.36 클러스터를 v1.37 로 올릴 때 단계마다 노드별 버전이 어떻게 바뀌는지 보입니다",
      lead="같은 노드를 단계마다 다시 그렸습니다. 칸 색이 바뀌는 자리가 그 단계에서 손대는 노드입니다")


def col_x(j):
    return GRID_X + j * SLOT_W


def lane_y(i):
    return TOP + HEAD_H + i * LANE_H


for j, name in enumerate(STEPS):
    cx = col_x(j) + SLOT_W // 2
    c = ACC if j == FOCAL_STEP else MUTED
    d.t(col_x(j) + 12, TOP + 22, str(j), 12, c, MONO, "start", 600)
    d.t(cx + 6, TOP + 22, name, 13, c, KR if has_kr(name) else MONO, "middle", 600)
d.line(12, TOP + HEAD_H, W - 12, TOP + HEAD_H, RULE, 0.8)

for i, (key, role) in enumerate(LANES):
    y = lane_y(i)
    d.t(16, y + LANE_H // 2 - 2, key, 15, INK, MONO, "start", 600)
    d.t(16, y + LANE_H // 2 + 16, role, 12, SOFT, KR, "start")
    if i == 2:
        d.line(12, y + LANE_H, W - 12, y + LANE_H, RULE, 0.8, "4 4")
    for j in range(N_S):
        ver, act, col = CELLS[j][i]
        x = col_x(j) + 6
        ny = y + 8
        if j == FOCAL_STEP and i == 0:
            d.tone(x, ny, NODE_W, NODE_H, ACC, 6, "12", 1.4)
        else:
            d.tone(x, ny, NODE_W, NODE_H, col, 6, "14", 1.0)
        d.t(x + NODE_W // 2, ny + 24, ver, 15, INK, MONO, "middle", 600)
        d.t(x + NODE_W // 2, ny + 44, act, 12, col if col != C_OLD else MUTED,
            KR if has_kr(act) else MONO, "middle")

for j in range(N_S - 1):
    ax = col_x(j + 1) - 4
    d.arrow([(ax - 16, TOP + 18), (ax, TOP + 18)], MUTED, "ar", 1.2)

cy = lane_y(N_L) + 8
d.line(12, cy - 8, W - 12, cy - 8, RULE, 0.8)
d.t(16, cy + 24, "스큐 점검", 13, MUTED, KR, "start", 600)
for j, txt in enumerate(CHECK):
    d.t(col_x(j) + SLOT_W // 2, cy + 24, txt, 13, ACC if j == FOCAL_STEP else MUTED,
        KR if has_kr(txt) else MONO, "middle")

d.legend(LEG_Y, [("이전 버전", C_OLD), ("이 단계에서 교체", C_DO), ("교체 끝", C_NEW)])

d.save("클러스터 업그레이드·ETCD 백업·복구.upgrade-order.svg")
