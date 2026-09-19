# 11-01 §4 — GC 이벤트 해부. 논지는 "타입과 단계별 시간 둘을 본다"인데, 본문이 고친
# 자리가 하나 더 있다 — 단계가 전부 ms 라는 것만으로 건강을 단정할 수 없다는 것.
# 그래서 단계 시간을 막대로 갈라 Evacuate 가 전체의 대부분이라는 사실을 보이되,
# 결론 칸에는 "잘 튜닝됨"이 아니라 "이 한 건으로는 단정 못 함"을 적는다.
# focal 은 Evacuate Collection Set — 이 수집에서 시간을 다 쓴 단계다.
# 타입 스펙: type-bar — 범주별 수치 비교. 네 단계의 ms 를 같은 축에 놓아 비중을 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 800, 540

d = D(W, H, "TROUBLESHOOTING JAVA · 11-01 §4",
      "한 번의 GC 이벤트를 단계로 가르면",
      "listing 11.2 의 Pause Young (Normal) 한 건을 evacuation 네 단계로 가른 막대 그림. "
      "Evacuate Collection Set 4.04ms 가 전체 5.10ms 의 79% 를 차지하고 나머지 셋은 1ms 미만이다. "
      "단계가 모두 ms 단위라는 사실은 그 순간의 관측일 뿐, 한 건으로 튜닝 상태를 판정하지는 못한다. "
      "판정하려면 빈도와 추세와 회수량을 함께 봐야 한다.",
      lead="Normal 은 분류 이름이고 ms 는 단위입니다 — 둘 다 건강 판정이 아닙니다")

# ── 이벤트 머리 — 타입
d.box(44, 104, 712, 40, PAPER2, RULE, 0.9, 6)
d.t(60, 129, "GC(0) Pause Young (Normal) (G1 Evacuation Pause)", 12, INK, MONO, "start")
d.t(740, 129, "타입 — 압박이 아닌 일상 수집", 12, MUTED, KR, "end")

# ── 막대: 단계별 시간
PHASES = [
    ("Pre Evacuate Collection Set", 0.13, "회수 대상 식별", False),
    ("Merge Heap Roots", 0.20, "참조 정렬", False),
    ("Evacuate Collection Set", 4.04, "살아남은 객체 이동", True),
    ("Post Evacuate Collection Set", 0.73, "마무리 정리", False),
]
TOTAL = sum(p[1] for p in PHASES)
BX, BW = 300, 356
Y0, ROW = 176, 52
MAXV = max(p[1] for p in PHASES)

d.t(44, Y0 - 14, "단계", 12, SOFT, KR, "start", 600)
d.t(BX, Y0 - 14, "쓴 시간", 12, SOFT, KR, "start", 600)

for i, (nm, v, sub, focal) in enumerate(PHASES):
    y = Y0 + i * ROW
    c = ACC if focal else INFO
    d.t(44, y + 16, nm, 12, ACC if focal else INK, MONO if not focal else MONO, "start",
        600 if focal else 400)
    d.t(44, y + 34, sub, 12, MUTED, KR, "start")
    bw = max(6, BW * v / MAXV)
    d.tone(BX, y + 4, bw, 26, c, 3, "26" if focal else "1A", 1.4 if focal else 1.0)
    d.t(BX + bw + 12, y + 22, f"{v:.2f}ms", 12, c, MONO, "start", 600 if focal else 400)
    pct = v / TOTAL * 100
    d.t(756, y + 22, f"{pct:.0f}%", 12, MUTED, MONO, "end")

# ── 합계 선
YT = Y0 + len(PHASES) * ROW
d.line(BX, YT - 4, 756, YT - 4, RULE, 1.0)
d.t(BX, YT + 18, f"합계 {TOTAL:.2f}ms — 한 단계가 79% 를 씁니다", 12, MUTED, KR, "start")

# ── 결론 칸 — 본문이 고친 자리
YC = YT + 40
d.box(44, YC, 712, 60, PAPER2, RULE, 0.9, 6)
d.t(60, YC + 25, "이 한 건으로 결론 내지 않습니다", 12, INK, KR, "start", 600)
d.t(60, YC + 46, "짧은 멈춤 하나는 그 순간의 사실입니다. 튜닝 상태는 빈도·추세·회수량을 함께 봐야 판정됩니다.",
    12, MUTED, KR, "start")

d.legend(H - 46, [("이 수집이 시간을 쓴 단계", ACC), ("1ms 미만 단계", INFO)])
d.save(os.path.join(os.path.dirname(__file__), "..", "11-01.fig-gc-event-anatomy.svg"))
print("ok gc-event-anatomy")
