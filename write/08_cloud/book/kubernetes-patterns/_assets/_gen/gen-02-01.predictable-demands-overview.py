# 02-01 전체 요약 도식 — 선언 두 갈래가 배치와 생사를 정한다
# 본문: 개발자가 Pod 정의에 적는 선언이 두 갈래(런타임 의존성 · 자원 프로파일)로 갈리고,
#   각 갈래가 오른쪽에서 서로 다른 결과를 만든다. 런타임 의존성은 다시 둘로 나뉘는데
#   이 구분이 이 장에서 가장 헷갈리는 지점이다 — 볼륨·hostPort 는 스케줄 자체를 막고,
#   ConfigMap·Secret 은 스케줄은 통과시킨 뒤 기동을 막는다. 가로줄 아래 두 상자는
#   이 흐름에 겹쳐 걸리는 별개 축이다.
# 타입 스펙: type-data-flow — 왼쪽 출발점에서 갈라져 오른쪽 결과로 흐르는 형태가
#   본문의 "두 갈래가 각각 다른 결과를 만든다"와 그대로 맞는다. 계층(layers)으로 그리면
#   갈래가 안 보이고, 격자(matrix)로 그리면 흐름의 방향이 사라진다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

# ── 좌표는 stride 로만 잡는다 (전부 4의 배수) ──────────────────────────────
W, H = 900, 696
COL_X = (24, 268, 552)          # 출발 · 갈래 · 결과 3열
COL_W = (196, 236, 300)
ROW_STRIDE = 96                 # 갈래 행 간격
TOP = 120
BOX_H = 72
GROUP_GAP = 32                  # 두 갈래 묶음 사이에 라벨이 들어갈 자리

def cx(j): return COL_X[j] + COL_W[j] // 2

# 갈래 k 의 y — 자원 프로파일 묶음(k>=2)은 라벨 자리만큼 아래로 민다
def branch_y(k): return TOP + k * ROW_STRIDE + (GROUP_GAP if k >= 2 else 0)

d = D(W, H, "KUBERNETES PATTERNS · 02-01",
      "선언 두 갈래가 배치와 생사를 정합니다",
      "개발자가 Pod 정의에 미리 적는 선언이 두 갈래로 갈립니다. 런타임 의존성은 다시 둘로 나뉘어 "
      "볼륨과 hostPort 는 스케줄 자체를 막고 ConfigMap 과 Secret 은 스케줄은 통과시킨 뒤 기동을 막습니다. "
      "자원 프로파일에서는 requests 가 노드 선택에 쓰이고 requests 와 limits 의 조합이 QoS 등급을 정합니다.",
      lead="선언하지 않으면 스케줄러는 컨테이너를 속이 안 보이는 상자로 다룹니다")

# ── 출발점 — 갈래 4개의 세로 중앙에 맞춘다 ──────────────────────────────
START_Y = (branch_y(0) + branch_y(3) + BOX_H) // 2 - BOX_H // 2
d.tone(COL_X[0], START_Y, COL_W[0], BOX_H, WARN, 6, "14", 1.2)
d.t(cx(0), START_Y + 30, "Pod 정의에 선언", 14, WARN, KR, "middle", 600)
d.t(cx(0), START_Y + 52, "개발자가 미리 적습니다", 12, MUTED, KR)

# ── 갈래 4개 (런타임 의존성 2 · 자원 프로파일 2) ─────────────────────────
BRANCHES = [
    (0, "volume · hostPort",   "노드가 제공해야 합니다", BAD,
        "스케줄 자체를 막습니다",   "놓을 노드가 없습니다", BAD),
    (1, "ConfigMap · Secret",  "네임스페이스에 있어야",  WARN,
        "스케줄은 되고 기동을 막습니다", "노드에는 올라갑니다", WARN),
    (2, "requests",            "최소 보장 · 합산 대상",  INFO,
        "스케줄러가 노드를 고릅니다", "limits 는 보지 않습니다", INFO),
    (3, "requests + limits",   "조합이 등급을 정합니다", ACC,
        "QoS 등급 · 죽는 순서",     "kubelet 이 죽입니다", ACC),
]

FAN_X = COL_X[1] - 44          # 갈래가 갈라지는 세로 기둥
SRC_X = COL_X[0] + COL_W[0]

for i, (k, name, sub, c, res, res_sub, rc) in enumerate(BRANCHES):
    y = branch_y(k)
    # 갈래 상자
    d.tone(COL_X[1], y, COL_W[1], BOX_H, c, 6, "10", 1.0)
    d.t(cx(1), y + 30, name, 14, c, KR if any('가' <= ch <= '힣' for ch in name) else MONO, "middle", 600)
    d.t(cx(1), y + 52, sub, 12, MUTED, KR)
    # 결과 상자 (focal 은 QoS 한 곳)
    focal = (k == 3)
    if focal:
        d.tone(COL_X[2], y, COL_W[2], BOX_H, ACC, 6, "16", 1.4)
    else:
        d.box(COL_X[2], y, COL_W[2], BOX_H, PAPER2, RULE, 0.9, 6)
    d.t(cx(2), y + 30, res, 14, rc if focal else INK, KR, "middle", 600)
    d.t(cx(2), y + 52, res_sub, 12, MUTED if not focal else ACC, KR)
    # 출발 → 갈래: 기둥까지 나갔다가 각 행 높이로 휘어 들어간다
    sy, ty = START_Y + BOX_H // 2, y + BOX_H // 2
    d.path(f"M {SRC_X+6} {sy} C {FAN_X} {sy}, {FAN_X} {ty}, {COL_X[1]-8} {ty}",
           c, 1.4, m="acc" if focal else "ar")
    # 갈래 → 결과
    d.path(f"M {COL_X[1]+COL_W[1]+6} {y+BOX_H//2} L {COL_X[2]-8} {y+BOX_H//2}",
           c, 1.5, m="acc" if focal else "ar")

# ── 갈래 묶음 라벨 ──────────────────────────────────────────────────────
d.t(COL_X[1], branch_y(0) - 14, "런타임 의존성 — 무엇이 갖춰져야 하는가", 12, SOFT, KR, "start")
d.t(COL_X[1], branch_y(2) - 14, "자원 프로파일 — 얼마나 필요한가", 12, SOFT, KR, "start")

# ── 겹쳐 걸리는 두 축 ───────────────────────────────────────────────────
AX_Y = branch_y(3) + BOX_H + 28
d.line(24, AX_Y, W - 48, AX_Y, RULE, 0.8)
d.t(24, AX_Y + 20, "여기에 겹쳐 걸리는 두 축", 12, SOFT, KR, "start")

AXES = [
    (268, "Pod Priority · 선점", "스케줄 순서 · QoS 와 별개 축입니다"),
    (568, "Quota · LimitRange", "네임스페이스 총량과 기본값을 강제합니다"),
]
for x, name, sub in AXES:
    d.box(x, AX_Y + 32, 284, 56, PAPER2, RULE, 0.9, 6)
    d.t(x + 142, AX_Y + 54, name, 13, INK, KR, "middle", 600)
    d.t(x + 142, AX_Y + 74, sub, 12, MUTED, KR)

d.legend(AX_Y + 108, [("스케줄을 막음", BAD), ("기동을 막음", WARN),
                      ("배치 입력", INFO), ("생사 순서", ACC)])

d.save("02-01.predictable-demands-overview.svg")
print("ok predictable-demands-overview")
