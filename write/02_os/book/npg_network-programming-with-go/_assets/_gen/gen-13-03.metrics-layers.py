# 타입 스펙: type-layers
# 사실 출처: NPG Ch.13 Instrumenting Your Code, Go kit metrics/prometheus, Prometheus client_golang promhttp
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 500
d = D(W, H, "LAYERS · METRICS ARCHITECTURE",
      "Go kit 인터페이스 추상화와 Prometheus 계측 계층",
      "비즈니스 코드는 Go kit 인터페이스만 바라보고 하위 어댑터가 Prometheus 형식으로 노출합니다",
      "수집 라이브러리가 바뀌어도 애플리케이션 계측 코드는 수정 없이 유지됩니다")

# 공통 흐름 표시기 (좌측 여백)
d.t(36, 130, "호출 ↓", 11, ACC, KR, "middle", 600)
d.arrow([(36, 142), (36, 330)], c=ACC, m="acc")

d.t(60, 350, "스크랩 ↑", 11, OK, KR, "middle", 600)
d.arrow([(60, 338), (60, 150)], c=OK, m="ok")

x, y0, sw, lh = 90, 105, 820, 58
gap = 14

layers = [
    ("L1", "애플리케이션 계측 코드", "metrics.Counter · metrics.Histogram", "비즈니스 로직에서 인터페이스 메서드만 호출 (플랫폼 독립)", ACC),
    ("L2", "Go kit 어댑터 계층", "kit/metrics/prometheus", "NewCounterFrom · NewHistogramFrom 으로 프로메테우스 타입 매핑", INFO),
    ("L3", "Prometheus 클라이언트 엔진", "client_golang/prometheus", "DefaultRegisterer 등록 및 메모리 내 메트릭 상태 관리", OK),
    ("L4", "HTTP 메트릭 노출 핸들러", "promhttp.Handler()", ":8081/metrics 경로로 텍스트 형식 메트릭 응답 서빙", INFO),
    ("L5", "외부 모니터링 시스템", "Prometheus Server / Grafana", "주기적 HTTP GET Pull 스크랩 및 시계열 데이터베이스(TSDB) 영구 저장", ACC),
]

for idx, (lvl, title, code, desc, col) in enumerate(layers):
    cur_y = y0 + idx * (lh + gap)
    d.tone(x, cur_y, sw, lh, col, op="14", sw=1.1)
    d.t(x + 20, cur_y + 26, lvl, 10, col, MONO, "start", 600)
    d.t(x + 55, cur_y + 26, title, 13, INK, KR, "start", 600)
    d.t(x + 280, cur_y + 26, f"[{code}]", 11, col, MONO, "start")
    d.t(x + 55, cur_y + 46, desc, 11, MUTED, KR, "start")

d.legend(460, [
    ("애플리케이션·수집기 경계", ACC),
    ("추상화 및 노출 어댑터", INFO),
    ("로컬 레지스트리 및 저장소", OK),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "13-03.metrics-layers.svg"))
d.save(out_path)
print("saved:", out_path)
