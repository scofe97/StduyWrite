# 타입 스펙: type-process
# 클러스터 업그레이드·ETCD 백업·복구 — 컨트롤 플레인(레인) × 복구 단계(열) 격자
# upgrade-order 와 같은 격자 골격을 쓴다(같은 형태에 같은 타입). 칸마다 그 시점에 도는 것과 하는 일만 둔다.
# 근거: kubernetes.io v1.37 「Operating etcd clusters for Kubernetes」 Restoring an etcd cluster,
#       etcd v3.7 「Disaster recovery」 Restoring with updated membership (2026-11-16 확인), kind 실습(2026-11-16)
import sys
sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

LANES = [("CP1", "stacked etcd"), ("CP2", "stacked etcd"), ("CP3", "stacked etcd")]
STEPS = ["정상", "API 중지", "etcd 중지", "restore", "etcd 기동", "API 기동"]
FOCAL_STEP = 3

C_RUN, C_DO, C_STOP, C_NEW = INFO, WARN, BAD, OK


def cells_for(name):
    return [
        ("etcd + API", "옛 데이터", C_RUN),
        ("etcd", "API 내림", C_DO),
        ("—", "etcd 내림", C_STOP),
        ("--name " + name, "새 data-dir", C_DO),
        ("etcd", "새 멤버십", C_NEW),
        ("etcd + API", "복귀", C_NEW),
    ]


CELLS = [cells_for(k.lower()) for k, _ in LANES]
CHECK = ["리더 있음", "쓰기 멈춤", "etcd 0대", "같은 snap.db", "과반 2/3", "API 복귀"]

W = 920
TOP = 96
LABEL_W = 140
RIGHT = 28
N_S, N_L = len(STEPS), len(LANES)
SLOT_W = (W - LABEL_W - RIGHT) // N_S
SLOT_W -= SLOT_W % 4                           # 124
HEAD_H = 36
LANE_H = 72
CHECK_H = 52
NODE_W = SLOT_W - 16
NODE_H = LANE_H - 16
GRID_X = LABEL_W
LEG_Y = TOP + HEAD_H + N_L * LANE_H + CHECK_H + 20
H = LEG_Y + 48


def has_kr(txt):
    return any('가' <= ch <= '힣' for ch in txt)


d = D(W, H, "ETCD · SNAPSHOT RESTORE",
      "같은 스냅샷으로 세 멤버를 새로 연다",
      "컨트롤 플레인 세 대의 stacked etcd 를 스냅샷 하나로 복구할 때 단계마다 노드별 상태가 어떻게 바뀌는지 보입니다",
      lead="API 서버를 모두 내린 뒤 etcd 를 내리고, 멤버마다 자기 이름으로 같은 파일을 풀어 새 클러스터로 다시 엽니다")


def col_x(j):
    return GRID_X + j * SLOT_W


def lane_y(i):
    return TOP + HEAD_H + i * LANE_H


for j, name in enumerate(STEPS):
    cx = col_x(j) + SLOT_W // 2
    c = ACC if j == FOCAL_STEP else MUTED
    d.t(col_x(j) + 8, TOP + 22, str(j), 12, c, MONO, "start", 600)
    d.t(cx + 6, TOP + 22, name, 13, c, KR if has_kr(name) else MONO, "middle", 600)
d.line(12, TOP + HEAD_H, W - 12, TOP + HEAD_H, RULE, 0.8)

for i, (key, role) in enumerate(LANES):
    y = lane_y(i)
    d.t(16, y + LANE_H // 2 - 2, key, 15, INK, MONO, "start", 600)
    d.t(16, y + LANE_H // 2 + 16, role, 12, SOFT, MONO, "start")
    for j in range(N_S):
        top, act, col = CELLS[i][j]
        x = col_x(j) + 8
        ny = y + 8
        if j == FOCAL_STEP and i == 0:
            d.tone(x, ny, NODE_W, NODE_H, ACC, 6, "12", 1.4)
        else:
            d.tone(x, ny, NODE_W, NODE_H, col, 6, "14", 1.0)
        d.t(x + NODE_W // 2, ny + 24, top, 13, INK, MONO, "middle", 600)
        d.t(x + NODE_W // 2, ny + 44, act, 12, col, KR if has_kr(act) else MONO, "middle")

for j in range(N_S - 1):
    ax = col_x(j + 1) - 4
    d.arrow([(ax - 12, TOP + 18), (ax, TOP + 18)], MUTED, "ar", 1.2)

cy = lane_y(N_L) + 8
d.line(12, cy - 8, W - 12, cy - 8, RULE, 0.8)
d.t(16, cy + 24, "클러스터", 13, MUTED, KR, "start", 600)
for j, txt in enumerate(CHECK):
    d.t(col_x(j) + SLOT_W // 2, cy + 24, txt, 13, ACC if j == FOCAL_STEP else MUTED,
        KR if has_kr(txt) else MONO, "middle")

d.legend(LEG_Y, [("옛 클러스터", C_RUN), ("이 단계에서 손댐", C_DO), ("멈춤", C_STOP), ("새 클러스터", C_NEW)])

d.save("클러스터 업그레이드·ETCD 백업·복구.restore-members.svg")
