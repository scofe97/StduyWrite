# 01-02 §2 — 카운터에서 알림까지의 용어 위계(원서 그림 1.4), 층마다 만드는 주체와 예.
# 타입 스펙: type-layers — 아래 층의 값을 골라 가공한 것이 위 층이 되는 네 층 스택이다.
#           축약: 그림 1.4 는 아래에서 위로 쌓으므로 카운터를 맨 아래에 둔다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 928, 496
BX, BW, BH, Y0, STRIDE = 136, 720, 56, 112, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-02 §2 · FIG 1.4",
       "카운터에서 알림까지",
       "원서 그림 1.4. 앱과 커널의 카운터를 성능 도구·에이전트가 읽어 통계를 내고, 모니터링 UI 가 그중 고른 통계를 메트릭으로 기록하며, 이벤트 처리가 메트릭으로 알림을 만든다. 원서는 업계의 쓰임이 엄격하지 않다고 덧붙인다.",
       "용어를 익히는 길잡이일 뿐, 알림은 어느 층에서든 생길 수 있습니다")

LAYERS = [   # 위 → 아래
    ("알림", "alert", "이벤트 처리", "Prometheus", None),
    ("메트릭", "metric", "성능 모니터링 UI", "Grafana", ACC),
    ("통계", "statistics", "성능 도구 · 에이전트", "vmstat · collectd", None),
    ("카운터", "counter", "애플리케이션 · 커널", "/proc", None),
]
for i, (name, en, who, ex, c) in enumerate(LAYERS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 6)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(BX + 20, y + 34, name, 15, c if c else INK, KR, "start", 600)
    d.t(BX + 96, y + 34, en, 12, SOFT, MONO, "start")
    d.t(BX + 340, y + 34, who, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 34, ex, 13, c if c else INK, MONO, "end", 600)

d.t(BX + 340, Y0 - 12, "만드는 주체", 12, SOFT, KR, "start")
d.t(BX + BW - 20, Y0 - 12, "예", 12, SOFT, KR, "end")
YB = Y0 + 3 * STRIDE + BH
d.t(64, YB + 4, "카운터", 12, SOFT, KR, "middle")
d.arrow([(64, YB - 12), (64, Y0 + 12)], SOFT, "soft", 1.2, "4 6")
d.t(64, Y0 - 4, "고르고 가공", 12, SOFT, KR, "middle")

d.legend(YB + 40, [("모니터링 대상으로 고른 통계", ACC), ("나머지 층", MUTED)])
d.save("01-02.instrumentation-terminology.svg")
