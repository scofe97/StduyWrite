# 11-01 §3 — 힙 구조. 논지는 "옷장 비유는 Serial·Parallel 의 배치이고, G1 은 다르다"이다.
# 그래서 연속된 Eden/Survivor/Old 블록을 그리면 본문이 고친 자리를 도식이 되살린다.
# G1 은 균등 크기 region 집합이고 세대는 region 에 붙는 이름표이므로, 같은 크기 칸을
# 늘어놓고 그 칸에 역할 이름표를 칠하는 그림으로 그린다. focal 은 humongous —
# Eden 을 거치지 않고 곧바로 할당되는 예외라 본문이 따로 짚은 자리다.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 여기서는 위 칸에 물리 배치(균등 region),
#           아래 칸에 그 region 이 받는 역할 이름표를 쌓아 "배치 ≠ 세대"를 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 800, 528

d = D(W, H, "TROUBLESHOOTING JAVA · 11-01 §3",
      "G1 의 힙은 구역이 아니라 region 입니다",
      "G1 힙 구조 도식. 힙은 균등 크기 region 집합이고 Eden·Survivor·Old 는 "
      "고정된 연속 구역이 아니라 region 에 붙는 역할 이름표다. 역할은 수집마다 바뀔 수 있다. "
      "humongous 객체는 region 절반을 넘어 Eden 을 거치지 않고 곧바로 humongous region 에 할당된다. "
      "리스팅이 세대를 region 개수로 세는 이유가 이 구조다.",
      lead="세대는 자리가 아니라 이름표입니다 — 그래서 로그가 개수로 셉니다")

# ── 층 1: 물리 배치 — 균등 크기 region 스무 칸
LX, LW = 44, 712
Y1 = 108
d.t(LX, Y1 - 12, "물리 배치 — 균등 크기 region", 12, SOFT, KR, "start", 600)
d.box(LX, Y1, LW, 60, PAPER2, RULE, 0.9, 6)

N = 20
CW = 32
GAP = 4
SX = LX + (LW - (N * CW + (N - 1) * GAP)) / 2
# 역할 배정 — 이름표는 흩어져 붙는다 (연속이 아니라는 것이 논지)
ROLE = ["eden", "old", "eden", "free", "surv", "eden", "eden", "old",
        "free", "eden", "hum", "eden", "surv", "free", "eden", "old",
        "eden", "free", "eden", "eden"]
COL = {"eden": OK, "surv": INFO, "old": WARN, "free": SOFT, "hum": ACC}

for i, r in enumerate(ROLE):
    x = SX + i * (CW + GAP)
    c = COL[r]
    if r == "hum":
        d.tone(x, Y1 + 14, CW, 32, ACC, 3, "26", 1.4)
    elif r == "free":
        d.box(x, Y1 + 14, CW, 32, PAPER2, RULE, 0.9, 3)
    else:
        d.tone(x, Y1 + 14, CW, 32, c, 3, "22", 1.0)

# focal 지시선 — humongous region 하나를 아래에서 짚는다
HX = SX + ROLE.index("hum") * (CW + GAP) + CW / 2
d.arrow([(HX, Y1 + 88), (HX, Y1 + 52)], ACC, "acc", 1.4)
d.t(HX, Y1 + 106, "humongous — Eden 을 건너뜁니다", 12, ACC, KR)
d.t(LX + 8, Y1 + 76, "region size 1024K — 칸 크기는 모두 같습니다", 12, MUTED, KR, "start")

# ── 층 2: 역할 이름표 — 같은 칸이 받는 이름
Y2 = 272
d.t(LX, Y2 - 12, "역할 이름표 — 수집마다 바뀔 수 있음", 12, SOFT, KR, "start", 600)
d.box(LX, Y2, LW, 92, PAPER2, RULE, 0.9, 6)

LABELS = [
    ("Eden", OK, "새 객체", "Eden regions: 47->0(109)"),
    ("Survivor", INFO, "살아남음", "Survivor regions: 0->6(6)"),
    ("Old", WARN, "승격됨", "Old regions: 2->2"),
    ("Humongous", ACC, "region 절반 초과", "Humongous regions: 0->0"),
]
CELLW = (LW - 40) / 4
for i, (nm, c, sub, log) in enumerate(LABELS):
    cx = LX + 20 + CELLW * i + CELLW / 2
    d.tone(cx - CELLW / 2 + 6, Y2 + 14, CELLW - 12, 28, c, 4, "1E", 1.2)
    d.t(cx, Y2 + 33, nm, 13, c, KR, "middle", 600)
    d.t(cx, Y2 + 58, sub, 12, MUTED, KR)
    d.t(cx, Y2 + 78, log, 9, SOFT, MONO)

# ── 층 3: 비유가 어긋나는 자리
Y3 = 392
d.t(LX, Y3 - 12, "옷장 비유가 어긋나는 자리", 12, SOFT, KR, "start", 600)
d.box(LX, Y3, LW, 64, PAPER2, RULE, 0.9, 6)
d.line(LX + LW / 2, Y3 + 10, LX + LW / 2, Y3 + 54, RULE, 0.9)
d.t(LX + 24, Y3 + 26, "Serial · Parallel", 12, SOFT, KR, "start", 600)
d.t(LX + 24, Y3 + 47, "연속 구역 · Survivor 는 from/to 두 semispace", 12, MUTED, KR, "start")
d.t(LX + LW / 2 + 24, Y3 + 26, "G1 — 이 장의 모든 리스팅", 12, INK, KR, "start", 600)
d.t(LX + LW / 2 + 24, Y3 + 47, "semispace 없음 · Survivor 는 young 수집에 포함", 12, MUTED, KR, "start")

d.legend(H - 52, [("Eden 을 거치지 않는 유일한 예외", ACC), ("region 이 받는 역할", INFO)])
d.save(os.path.join(os.path.dirname(__file__), "..", "11-01.fig-heap-structure.svg"))
print("ok heap-structure")
