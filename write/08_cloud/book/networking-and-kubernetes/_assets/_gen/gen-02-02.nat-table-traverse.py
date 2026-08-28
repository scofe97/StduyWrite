# 02-02.nat-table-traverse — 한 요청이 nat 을 지나는 자리는 훅 둘이고, 그 안은 점프로 겹겹이다
# 본문 요구: "규칙을 거는 자리와 실제로 주소를 바꾸는 자리가 서로 다른 체인에 떨어져 있습니다."
#            + "두 체인 사이를 잇는 것이 mark 0x4000 입니다."
#            + "패킷 하나가 nat 테이블을 지나는 동안 어느 규칙에 걸리고 어느 필드가 바뀌는지"
# 타입 스펙: type-swimlane.md — 레인 = 훅(그 자리에서 행위가 벌어지는 주체이자 시점),
#           레인 안 단계 = 그 훅에서 실제로 지나는 체인. 레인을 가로지르는 라우팅 판단이
#           스펙이 말하는 handoff 라 focal 을 건다. §1 의 chain-then-table 과 같은 문법이라
#           독자가 이미 배운 읽는 법을 그대로 쓴다.
# 2026-08-28 재작성: 앞 판(type-process)은 여섯 칸을 한 줄로 세워 (1) 훅이 둘이라는 것,
#           (2) 세 체인이 나란한 단계가 아니라 점프로 들어간 것, (3) 마지막 칸이 다른 시나리오라는 것을
#           모두 감췄다(학습자 피드백 — "실제 구조 흐름이 보이게"). 훅을 레인으로 가르고
#           점프를 계단으로 세워 깊이를 드러낸다.
# 좌표: Layout conventions 타입이라 공식이 없다 — 계단 stride 84(세로)·80(가로), 전부 4의 배수.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 844
d = D(W, H, "nat TABLE · TWO HOOKS, ONE JUMP STACK",
      "한 요청이 nat 을 지나는 자리 — 훅은 둘이고 그 안은 점프로 겹겹이다",
      "위 레인이 라우팅 판단 전의 PREROUTING, 아래가 나가기 직전의 POSTROUTING 이다. "
      "레인 안에서 오른쪽 아래로 내려간 계단이 체인 점프의 깊이이고, 오른쪽 칸이 그 직후의 패킷 상태다.",
      lead="레인 = 훅 · 계단 = 점프해 들어간 깊이 · 오른쪽 = 그 직후 패킷 상태 (kind 실측)")

SX, SW = 692, 276                                  # 상태 칸
BW, BH = 380, 68
STEP_X, STEP_Y = 80, 104                           # 계단 stride (세로 간격 36px 은 꺾인 화살표가 들어갈 최소치)


def cell(x, y, name, rule, result, focal=False, w=BW, h=BH):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); c = ACC
    else:
        d.box(x, y, w, h, PAPER2, INFO, 1.1, 6); c = INFO
    d.t(x + 20, y + 26, ddx.fit(name, 13, w - 40, name), 13, c, MONO, "start", 600)
    d.t(x + 20, y + 46, ddx.fit(rule, 11, w - 40, rule), 11, MUTED,
        MONO if all(ord(ch) < 128 for ch in rule) else KR, "start")
    d.t(x + 20, y + 62, ddx.fit(result, 10, w - 40, result), 10, SOFT, KR, "start")


def state(cy, txt, val, c=MUTED):
    d.box(SX, cy - 30, SW, 60, PAPER2, c, 1.1, 6)
    d.t(SX + 18, cy - 6, txt, 11, c, KR, "start", 600)
    d.t(SX + 18, cy + 16, val, 11, MUTED if c is not ACC else ACC, MONO, "start")


# ── 레인 1 — PREROUTING · nat ──────────────────────────────────────────────
ddx.band(d, 120, 472, "PREROUTING · nat   —   훅 NF_IP_PRE_ROUTING · 라우팅 판단 전")

X0, Y0 = 120, 164
cell(X0, Y0, "KUBE-SERVICES", "-d 10.96.192.224/32", "ClusterIP 에 해당하는 서비스 체인을 고른다")
cell(X0 + STEP_X, Y0 + STEP_Y, "KUBE-SVC-LOLE4…", "! -s 10.244.0.0/16  →  불일치",
     "Pod 출발지라 마킹을 건너뛴다 · 이어서 확률 0.33333")
cell(X0 + STEP_X * 2, Y0 + STEP_Y * 2, "KUBE-SEP-2MJG…", "-j DNAT",
     "여기서 목적지가 실제로 바뀐다", focal=True)

for i in range(2):                                  # 계단 — 점프해 한 겹 들어간다
    xa, ya = X0 + STEP_X * i + 44, Y0 + STEP_Y * i + BH
    xb, yb = X0 + STEP_X * (i + 1) + 44, Y0 + STEP_Y * (i + 1)
    mid = ya + 16                                   # 코리도어 — 아래로만 흐르게 둔다
    d.path(f"M {xa} {ya} L {xa} {mid} L {xb} {mid} L {xb} {yb-4}", MUTED, 1.5, m="ar")
    d.chip((xa + xb) // 2, mid, "-j", INFO)         # 칩 배경이 선을 끊어 점프임을 드러낸다

state(Y0 + 34, "헤더는 그대로", "체인만 갈아탄다")
state(Y0 + STEP_Y + 34, "마크가 안 붙는다", "mark 0x0 유지")
state(Y0 + STEP_Y * 2 + 34, "목적지가 바뀐다", "dst → 10.244.1.66:8080", ACC)

# ── 레인을 갈아타는 자리 ───────────────────────────────────────────────────
d.path(f"M {X0 + STEP_X * 2 + 44} {Y0 + STEP_Y * 2 + BH} L {X0 + STEP_X * 2 + 44} 492 "
       f"L 500 492 L 500 508", ACC, 1.6, m="acc")
d.o.append(f'<rect x="24" y="514" width="952" height="52" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(44, 536, "라우팅 판단", 12, ACC, KR, "start", 600)
d.t(44, 554, "바뀐 목적지로 경로를 다시 정한다 — 여기부터는 다른 훅이다", 11, MUTED, KR, "start")
d.t(956, 536, "두 훅을 잇는 것은 mark 0x4000 하나뿐", 11, WARN, KR, "end")
d.t(956, 554, "이 예에서는 붙지 않았다", 11, MUTED, KR, "end")
d.path("M 500 566 L 500 588", ACC, 1.6, m="acc")

# ── 레인 2 — POSTROUTING · nat ─────────────────────────────────────────────
ddx.band(d, 588, 760, "POSTROUTING · nat   —   훅 NF_IP_POST_ROUTING · 인터페이스로 나가기 직전")

cell(X0, 630, "KUBE-POSTROUTING", "! --mark 0x4000 검사", "마크가 붙었는지만 본다", w=300)
for i, (title, sub, c) in enumerate((("-j RETURN", "마크 없음 — Pod 가 부른 경우 · src 그대로", MUTED),
                                     ("MASQUERADE --random-fully", "마크 있음 — 노드가 부른 경우 · src → 10.244.1.1:39387", WARN))):
    y = 620 + i * 72
    d.box(520, y, 456, 56, PAPER2, c, 1.1, 6)
    d.t(540, y + 24, ddx.fit(title, 12, 416, title), 12, c, MONO, "start", 600)
    d.t(540, y + 42, ddx.fit(sub, 11, 416, sub), 11, MUTED, KR, "start")
    d.path(f"M 428 664 L 452 664 L 452 {y + 28} L 510 {y + 28}", c, 1.4, m="ar" if i == 0 else "warn")

d.t(36, 788, "체인을 몇 번 갈아타도 헤더는 그대로다 — 실제로 바뀌는 자리는 위 레인의 DNAT 한 번과 "
             "아래 레인의 조건부 MASQUERADE 한 번뿐이다", 12, MUTED, KR, "start")
d.legend(800, [("지나는 체인", INFO), ("바뀌는 자리 · 레인을 갈아타는 자리", ACC),
               ("노드에서 온 요청일 때만", WARN)])
d.save("02-02.nat-table-traverse.svg")
print("ok nat-table-traverse")
