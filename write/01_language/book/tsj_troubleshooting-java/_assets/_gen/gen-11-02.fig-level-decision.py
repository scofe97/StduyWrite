# 11-02 §3 — 로그 레벨 선택. 본문이 원서를 뒤집은 자리다. 원서는 "운영은 error·warning
# 만" 이라 적었지만 JDK 25 실측에서 그 설정은 GC 이벤트가 0줄이다. 정상 GC 이벤트가
# info 레벨에 찍히기 때문이다(JEP 271). 그래서 이 도식은 옛 조언을 재현하지 않는다 —
# 판단을 "무엇을 조사하나"로 시작해 운영은 info 로, 깊은 조사는 staging 의 debug·trace 로
# 보내고, error·warning 갈래는 "0줄" 이라는 결과와 함께 막다른 길로 그린다.
# focal 은 운영 = info — 본문이 실제로 권하는 단 하나의 답이다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, INFO, BAD, PAPER2, RULE, KR, MONO

W, H = 800, 516

d = D(W, H, "TROUBLESHOOTING JAVA · 11-02 §3",
      "어느 레벨을 켤까",
      "GC 로그 레벨 선택 흐름도. 운영 환경에서는 info 를 켜고 로테이션을 건다 — "
      "info 는 이벤트당 한 줄 수준이라 오버헤드가 작고 이것이 실무 표준이다. "
      "더 깊은 조사가 필요하면 운영을 verbose 로 채우지 말고 staging 에서 재현하며 debug·trace 로 판다. "
      "원서가 권한 error·warning 은 HotSpot 이 정상 GC 이벤트를 info 이상에서만 찍으므로 "
      "GC 로그를 줄이는 것이 아니라 0줄로 만든다. JDK 25 실측이다.",
      lead="원서의 error·warning 권고는 로그를 줄이지 않고 없애 버립니다")

CX = 232          # 판단 열 중심
RX = 560          # 결과 열 중심
BW, BH = 300, 56

# ── 시작
d.box(CX - BW / 2, 104, BW, 40, PAPER2, RULE, 0.9, 6)
d.t(CX, 129, "GC 로그로 무엇을 하려는가", 13, INK, KR, "middle", 600)

# ── 갈래 1: 상시 관측 (운영) → info  [focal]
Y1 = 176
d.arrow([(CX, 144), (CX, Y1 - 4)], MUTED, "ar", 1.3)
d.box(CX - BW / 2, Y1, BW, BH, PAPER2, RULE, 0.9, 6)
d.t(CX, Y1 + 24, "운영에서 상시 관측", 13, INK, KR, "middle", 600)
d.t(CX, Y1 + 44, "장애가 났을 때 볼 로그가 있어야 함", 12, MUTED, KR)

d.tone(RX - BW / 2, Y1, BW, BH, ACC, 6)
d.t(RX, Y1 + 24, "gc*=info + 로테이션", 13, ACC, MONO, "middle", 600)
d.t(RX, Y1 + 44, "이벤트당 한 줄 — 실무 표준", 12, ACC, KR)
d.arrow([(CX + BW / 2, Y1 + 28), (RX - BW / 2 - 4, Y1 + 28)], ACC, "acc", 1.4)

# ── 갈래 2: 깊은 조사 → staging 에서 debug·trace
Y2 = 268
d.arrow([(CX, Y1 + BH), (CX, Y2 - 4)], MUTED, "ar", 1.3)
d.t(CX + 12, Y2 - 14, "단서가 부족하면", 12, SOFT, KR, "start")
d.box(CX - BW / 2, Y2, BW, BH, PAPER2, RULE, 0.9, 6)
d.t(CX, Y2 + 24, "더 깊이 파야 함", 13, INK, KR, "middle", 600)
d.t(CX, Y2 + 44, "운영을 verbose 로 채우지 않음", 12, MUTED, KR)

d.tone(RX - BW / 2, Y2, BW, BH, INFO, 6)
d.t(RX, Y2 + 24, "staging 에서 debug · trace", 13, INFO, KR, "middle", 600)
d.t(RX, Y2 + 44, "재현해 놓고 판다", 12, MUTED, KR)
d.arrow([(CX + BW / 2, Y2 + 28), (RX - BW / 2 - 4, Y2 + 28)], INFO, "info", 1.3)

# ── 막다른 길: error · warning
Y3 = 360
# 이 갈래는 순서상 다음 단계가 아니라 *기각된 선택지*다 — 점선으로 갈라 낸다
d.line(CX, Y2 + BH, CX, Y3 - 4, RULE, 0.9, "4 5")
d.t(CX + 12, Y3 - 12, "택하지 않습니다", 12, SOFT, KR, "start")
d.box(CX - BW / 2, Y3, BW, BH, PAPER2, RULE, 0.9, 6)
d.t(CX, Y3 + 24, "원서 권고 — error · warning", 13, MUTED, KR, "middle", 600)
d.t(CX, Y3 + 44, "성능이 걱정돼 줄이려는 선택", 12, SOFT, KR)

d.tone(RX - BW / 2, Y3, BW, BH, BAD, 6)
d.t(RX, Y3 + 24, "GC 이벤트 0줄", 13, BAD, KR, "middle", 600)
d.t(RX, Y3 + 44, "정상 이벤트는 info 에 찍힘 (JEP 271)", 12, BAD, KR)
d.arrow([(CX + BW / 2, Y3 + 28), (RX - BW / 2 - 4, Y3 + 28)], BAD, "bad", 1.3)

# ── 실측 근거 한 줄
d.t(44, 448, "JDK 25 실측 — gc=error 0줄 · gc=warning 0줄 · gc=info 7줄", 12, MUTED, MONO, "start")

d.legend(H - 44, [("운영에서 실제로 켤 것", ACC), ("로그가 비어 버리는 선택", BAD)])
d.save(os.path.join(os.path.dirname(__file__), "..", "11-02.fig-level-decision.svg"))
print("ok level-decision")
