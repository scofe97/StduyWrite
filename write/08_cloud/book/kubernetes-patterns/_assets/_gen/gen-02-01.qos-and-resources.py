# 02-01 §QoS 3등급 — 조합이 생사 순서를 정한다
# 본문: requests·limits 를 어떻게 적었는가(행)가 등급을 정하고, 그 등급이 축출에서
#   무엇을 뜻하는가(열)로 이어진다. 본문이 정정하는 두 가지를 그림도 같이 정정해야 한다 —
#   ① requests 만 적고 limits 를 생략한 흔한 경우도 Burstable 이다("서로 다름"이 아니다).
#   ② kubelet 은 QoS 등급으로 축출 순서를 정하지 않는다. 1번 기준은 "request 를 넘겼는가"다.
#   근거: kubernetes/website node-pressure-eviction.md — "The kubelet does not use the pod's
#   QoS class to determine the eviction order." + pod-qos.md 의 3등급 판정 조건.
# 타입 스펙: type-dp-security-matrix — 행(선언 조합) × 열(판정·결과)의 격자로,
#   "어느 조합이 어떤 결과가 되는가"를 셀로 읽게 한다. 화살표 사슬로 그리면
#   등급 → 순서가 확정 인과처럼 보이므로 격자를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

# ── §2 Layout formulas (좌표는 전부 여기서 산출한다) ────────────────────────
LEFT_PAD, RIGHT_PAD = 12, 24
COMP_COL_W, COMP_ROLE_GAP = 216, 12
ROLE_COL_W, ROLE_COL_GAP = 196, 16
HEADER_H, ROW_H, ROW_STRIDE = 56, 60, 68

ROLES = [
    ("QoS 등급", "자동 판정"),
    ("축출에서 뜻하는 것", "kubelet 의 1번 기준"),
    ("한도를 넘기면", "압축 가능 · 불가"),
]
ROWS = [
    ("requests · limits 없음", "아무것도 안 적음"),
    ("requests 만 적음", "limits 생략 — 가장 흔함"),
    ("requests ≠ limits", "limits 를 더 크게"),
    ("메모리 requests = limits", "CPU limit 은 비움"),
    ("CPU · 메모리 모두 같음", "둘 다 request = limit"),
]

N_ROLES, N_ROWS = len(ROLES), len(ROWS)
W = (LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP
     + N_ROLES * ROLE_COL_W + (N_ROLES - 1) * ROLE_COL_GAP + RIGHT_PAD)
HEADER_Y = 96
def row_y(k): return HEADER_Y + HEADER_H + 16 + k * ROW_STRIDE
ROWS_BOTTOM = row_y(N_ROWS - 1) + ROW_H
LEGEND_Y = ROWS_BOTTOM + 44
H = LEGEND_Y + 48

COMP_COL_X = LEFT_PAD
def role_col_x(j): return LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + j * (ROLE_COL_W + ROLE_COL_GAP)
def role_col_cx(j): return role_col_x(j) + ROLE_COL_W // 2

d = D(W, H, "KUBERNETES PATTERNS · 02-01",
      "무엇을 적었는가가 등급을 정하고, 등급은 축출 순서의 추정치일 뿐입니다",
      "requests 와 limits 를 어떻게 적었는지가 행이고 그 결과가 열입니다. "
      "requests 만 적고 limits 를 생략한 가장 흔한 경우도 Burstable 입니다. "
      "kubelet 은 QoS 등급으로 축출 순서를 정하지 않고 request 를 넘겼는지를 먼저 봅니다.",
      lead="등급은 순서를 결정하지 않습니다 — 1번 기준은 자기 request 를 넘겼는가입니다")

# ── 헤더행 ──────────────────────────────────────────────────────────────
d.box(COMP_COL_X, HEADER_Y, COMP_COL_W, HEADER_H, PAPER2, RULE, 0.9, 6)
d.t(COMP_COL_X + COMP_COL_W // 2, HEADER_Y + 24, "무엇을 적었는가", 13, INK, KR, "middle", 600)
d.t(COMP_COL_X + COMP_COL_W // 2, HEADER_Y + 42, "Pod 의 모든 컨테이너 기준", 12, SOFT, KR)

for j, (name, code) in enumerate(ROLES):
    d.box(role_col_x(j), HEADER_Y, ROLE_COL_W, HEADER_H, PAPER2, RULE, 0.9, 6)
    d.t(role_col_cx(j), HEADER_Y + 24, name, 13, INK, KR, "middle", 600)
    d.t(role_col_cx(j), HEADER_Y + 42, code, 12, SOFT, KR)

# ── 데이터행 ────────────────────────────────────────────────────────────
# (등급, 등급색), (축출 의미, 색), (초과 시, 색), focal 여부
CELLS = [
    (("Best-Effort", BAD),   ("request 가 없어 항상 초과", BAD),   ("메모리는 죽습니다", BAD),   False),
    (("Burstable", WARN),    ("request 안이면 늦게 나갑니다", OK), ("CPU 는 스로틀", WARN),      True),
    (("Burstable", WARN),    ("넘긴 만큼 먼저 나갑니다", BAD),     ("limit 까지 자랍니다", WARN), False),
    (("Burstable", WARN),    ("메모리는 넘길 수 없습니다", OK),    ("CPU 만 스로틀", OK),        False),
    (("Guaranteed", INFO),   ("마지막에 나갑니다", OK),            ("CFS 스로틀을 떠안습니다", WARN), False),
]

for k, (label, sub) in enumerate(ROWS):
    y = row_y(k)
    d.box(COMP_COL_X, y, COMP_COL_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(COMP_COL_X + 14, y + 26, label, 13, INK, KR, "start")
    d.t(COMP_COL_X + 14, y + 45, sub, 12, SOFT, KR, "start")

    (grade, gc), (evict, ec), (over, oc), focal = CELLS[k]
    for j, (txt, c) in enumerate(((grade, gc), (evict, ec), (over, oc))):
        x = role_col_x(j)
        if focal and j == 0:
            d.tone(x, y, ROLE_COL_W, ROW_H, ACC, 4, "12", 1.4)
            d.t(role_col_cx(j), y + 25, txt, 13, ACC, KR, "middle", 600)
            d.t(role_col_cx(j), y + 44, "이 책의 권장이 여기입니다", 12, ACC, KR)
        else:
            d.tone(x, y, ROLE_COL_W, ROW_H, c, 4, "10", 0.9)
            d.t(role_col_cx(j), y + (34 if len(txt) < 14 else 27), txt,
                13, c, KR, "middle", 600 if j == 0 else 400)
            if len(txt) >= 14:
                d.t(role_col_cx(j), y + 45, "", 12, c, KR)

# ── 바닥 주석 ───────────────────────────────────────────────────────────
d.line(LEFT_PAD, ROWS_BOTTOM + 18, W - RIGHT_PAD, ROWS_BOTTOM + 18, RULE, 0.8)
d.t(LEFT_PAD, LEGEND_Y - 4,
    "kubelet 이 보는 순서는 ① request 초과 여부 ② Pod Priority ③ 초과량입니다. 등급은 그 결과의 추정치로만 씁니다.",
    12, MUTED, KR, "start")
d.legend(LEGEND_Y + 8, [("가장 먼저", BAD), ("중간", WARN), ("늦게", OK), ("권장 조합", ACC)])

d.save("02-01.qos-and-resources.svg")
print("ok qos-and-resources")
