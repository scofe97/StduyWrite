# 11-03 §4 — GC 병렬성. 본문이 원서를 두 군데 뒤집은 자리다. 원서는 "8개 중 2개면
# 과소 할당이니 ParallelGCThreads 를 늘려라" 라고 하지만 (1) G1 은 상한 안에서
# 적응적으로 고르므로 2개는 그만큼이면 충분했다는 뜻일 수 있고 (2) 8코어에서 =6 을
# 주면 상한을 되레 낮춘다. 그래서 이 도식은 "과소 vs 과다" 두 진단 상자를 그리지 않는다 —
# 관측 한 줄에서 결론으로 곧장 가는 길을 막고, 그 사이에 함께 봐야 할 것들을 세운다.
# focal 은 "단서일 뿐" 이라는 판정 — 본문의 논지 그 자체.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 관측에서 결론까지의 게이트.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, INFO, BAD, PAPER2, RULE, KR, MONO

W, H = 800, 512

d = D(W, H, "TROUBLESHOOTING JAVA · 11-03 §4",
      "워커 수는 단서이지 결론이 아닙니다",
      "GC 병렬성 판단 흐름도. 로그의 Using N workers of M for evacuation 한 줄은 관측일 뿐이다. "
      "G1 은 힙 상태와 처리할 region 양에 따라 상한 안에서 필요한 만큼만 적응적으로 고르므로, "
      "8개 중 2개를 썼다는 것은 그만큼이면 충분했다는 뜻일 수 있다. 과소 할당을 단정하려면 "
      "멈춤 시간의 추세와 빈도와 코어 수를 함께 놓아야 한다. 8코어에서 ParallelGCThreads=6 은 "
      "상한을 8에서 6으로 낮추므로 늘리려던 의도와 반대로 작동한다.",
      lead="G1 은 상한 안에서 적응적으로 고릅니다 — 적게 썼다고 모자란 것이 아닙니다")

# ── 관측 한 줄
d.box(44, 108, 712, 44, PAPER2, RULE, 0.9, 6)
d.t(64, 128, "관측", 11, SOFT, MONO, "start")
d.t(64, 144, "[gc,task] GC(0) Using 6 workers of 8 for evacuation", 12, INK, MONO, "start")
d.t(736, 136, "gc*=info 로 켜면 나옵니다", 12, MUTED, KR, "end")

# ── 막는 게이트 (focal)
GY = 180
d.arrow([(400, 152), (400, GY - 4)], MUTED, "ar", 1.3)
d.tone(200, GY, 400, 52, ACC, 6)
d.t(400, GY + 22, "이 한 줄로는 결론이 안 납니다", 13, ACC, KR, "middle", 600)
d.t(400, GY + 42, "G1 은 필요한 만큼만 씁니다", 12, ACC, KR)

# ── 함께 봐야 할 것 셋
CY = 268
ITEMS = [
    ("멈춤 시간 추세", "늘고 있는가"),
    ("GC 빈도", "잦아지고 있는가"),
    ("코어 수", "16 워커도 16코어면 정상"),
]
CW = 224
GAP = 20
SX = (800 - (len(ITEMS) * CW + (len(ITEMS) - 1) * GAP)) / 2
d.arrow([(400, GY + 52), (400, CY - 4)], ACC, "acc", 1.3)
d.t(412, CY - 14, "함께 놓고 봅니다", 12, SOFT, KR, "start")
for i, (nm, sub) in enumerate(ITEMS):
    x = SX + i * (CW + GAP)
    d.box(x, CY, CW, 56, PAPER2, RULE, 0.9, 6)
    d.t(x + CW / 2, CY + 24, nm, 13, INFO, KR, "middle", 600)
    d.t(x + CW / 2, CY + 44, sub, 12, MUTED, KR)

# ── 두 플래그
FY = 356
d.box(44, FY, 712, 60, PAPER2, RULE, 0.9, 6)
d.line(400, FY + 10, 400, FY + 50, RULE, 0.9)
d.t(64, FY + 26, "-XX:ParallelGCThreads", 12, INK, MONO, "start")
d.t(64, FY + 46, "STW 단계 워커 상한 — 기본은 코어 수", 12, MUTED, KR, "start")
d.t(420, FY + 26, "-XX:ConcGCThreads", 12, INK, MONO, "start")
d.t(420, FY + 46, "동시(백그라운드) 단계 워커 수", 12, MUTED, KR, "start")

# ── 원서 처방이 반대로 작동하는 자리
WY = 428
d.tone(44, WY, 712, 40, BAD, 6)
d.t(64, WY + 25, "8코어에서 ParallelGCThreads=6 은 상한을 8에서 6으로 낮춥니다 — 늘리려던 의도와 반대입니다",
    12, BAD, KR, "start")

d.legend(H - 40, [("결론으로 곧장 가지 못하게 막는 자리", ACC), ("원서 처방이 뒤집히는 자리", BAD)])
d.save(os.path.join(os.path.dirname(__file__), "..", "11-03.fig-parallelism-tuning.svg"))
print("ok parallelism-tuning")
