# 타입 스펙: type-architecture
# 사실 출처: NPG Ch.13 Instrumenting a Basic HTTP Server (Listing 13-24~13-27)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, WARN, KR, MONO

W, H = 980, 520
d = D(W, H, "ARCHITECTURE · DUAL-PORT SERVER",
      "비즈니스 웹 서버와 메트릭 서버의 포트 격리 아키텍처",
      "앱 서버(:8082)는 핸들러와 ConnState로 계측하고 메트릭 서버(:8081)는 스크랩 전용으로 격리합니다",
      "클라이언트 트래픽과 모니터링 내부 트래픽이 서로 간섭하지 않도록 분리합니다")

# Zone 1: Web App Server (:8082)
z1_x, z1_y, z1_w, z1_h = 35, 105, 400, 335
d.box(z1_x, z1_y, z1_w, z1_h, fill="#161B22", stroke=RULE, sw=1.0)
d.t(z1_x + 16, z1_y + 24, "ZONE 1 · 앱 서버 (:8082)", 13, INFO, KR, "start", 600)

# Inside Zone 1: ConnState Hook
d.tone(z1_x + 18, z1_y + 40, 364, 72, INFO, op="12", sw=1.0)
d.t(z1_x + 30, z1_y + 63, "연결 상태 훅: connStateMetrics", 12, INK, KR, "start", 600)
d.t(z1_x + 30, z1_y + 81, "ConnState (StateNew · StateClosed)", 11, MUTED, KR, "start")
d.t(z1_x + 30, z1_y + 98, "새 연결 +1, 소켓 닫힘 -1 반영", 11, SOFT, KR, "start")

# Inside Zone 1: helloHandler
d.tone(z1_x + 18, z1_y + 124, 364, 98, ACC, op="14", sw=1.0)
d.t(z1_x + 30, z1_y + 146, "비즈니스 핸들러: helloHandler", 12, INK, KR, "start", 600)
d.t(z1_x + 30, z1_y + 166, "① 진입: Requests.Add(1)", 11, ACC, KR, "start")
d.t(z1_x + 30, z1_y + 184, "② 종료: RequestDuration.Observe(s)", 11, OK, KR, "start")
d.t(z1_x + 30, z1_y + 203, "③ 오류: WriteErrors.Add(1)", 11, WARN, KR, "start")

# Client Request Flow into Zone 1
d.box(z1_x + 18, z1_y + 234, 364, 48, fill="#0D1117", stroke=RULE, sw=0.8)
d.t(z1_x + 30, z1_y + 254, "클라이언트 HTTP GET / 요청 수신", 11, INK, KR, "start")
d.t(z1_x + 30, z1_y + 271, "TCP 악수 및 HTTP 요청 본문 처리", 11, MUTED, KR, "start")


# Zone 2: Metrics Server (:8081)
z2_x, z2_y, z2_w, z2_h = 545, 105, 400, 335
d.box(z2_x, z2_y, z2_w, z2_h, fill="#161B22", stroke=RULE, sw=1.0)
d.t(z2_x + 16, z2_y + 24, "ZONE 2 · 메트릭 서버 (:8081)", 13, OK, KR, "start", 600)

# Inside Zone 2: promhttp.Handler()
d.tone(z2_x + 18, z2_y + 40, 364, 72, OK, op="14", sw=1.0)
d.t(z2_x + 30, z2_y + 63, "노출 엔드포인트: /metrics", 12, INK, KR, "start", 600)
d.t(z2_x + 30, z2_y + 81, "promhttp.Handler() 바인딩", 11, OK, MONO, "start")
d.t(z2_x + 30, z2_y + 98, "DefaultGatherer 텍스트 직렬화", 11, MUTED, KR, "start")

# Inside Zone 2: Prometheus Scraper
d.tone(z2_x + 18, z2_y + 124, 364, 72, INFO, op="12", sw=1.0)
d.t(z2_x + 30, z2_y + 146, "Prometheus 서버 스크랩 수집", 12, INK, KR, "start", 600)
d.t(z2_x + 30, z2_y + 166, "④ 주기적 GET /metrics Pull", 11, INFO, KR, "start")
d.t(z2_x + 30, z2_y + 183, "내부 관리망으로만 접근 허용", 11, SOFT, KR, "start")

# Inside Zone 2: Isolated Network Note
d.box(z2_x + 18, z2_y + 208, 364, 68, fill="#0D1117", stroke=RULE, sw=0.8)
d.t(z2_x + 30, z2_y + 228, "포트 분리 이유 (보안 및 격리)", 11, WARN, KR, "start", 600)
d.t(z2_x + 30, z2_y + 247, "런타임 민감 정보 외부 노출 차단", 11, MUTED, KR, "start")
d.t(z2_x + 30, z2_y + 264, "요청 폭주 시에도 모니터링 보장", 11, MUTED, KR, "start")


# Arrows between zones / shared memory
d.arrow([(z1_x + z1_w, z1_y + 76), (z2_x, z1_y + 76)], c=OK, m="ok", sw=1.5)
d.t(490, z1_y + 68, "상태 공유", 11, OK, KR, "middle", 600)

d.arrow([(z1_x + z1_w, z1_y + 172), (z2_x, z1_y + 172)], c=ACC, m="acc", sw=1.5)
d.t(490, z1_y + 164, "카운터 갱신", 11, ACC, KR, "middle", 600)

# Legend (y=460 leaves 60px margin to H=520, fits all 4 colors)
d.legend(460, [
    ("비즈니스 (:8082)", ACC),
    ("연결 감시", INFO),
    ("관리 격리 (:8081)", OK),
    ("보안·오류 고려", WARN),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "13-03.dual-port-server-architecture.svg"))
d.save(out_path)
print("saved:", out_path)
