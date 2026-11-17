# 08-02 §6 — 밀기(StatsD)와 끌기(스크래핑)에서 실제로 오가는 것과 목적지 주소를 쥔 설정의 자리.
#           밀기는 앱 쪽에 목적지 127.0.0.1:8125 가 있고 UDP 데이터그램 "foo:1|c" 가 한 방향으로 간다.
#           끌기는 node exporter 가 :9100/metrics 를 열어 두기만 하고, 대상 주소는 Prometheus 의
#           prometheus.yml targets 에 모여 있어 15s 마다 GET 을 보내 텍스트 메트릭을 받아 간다.
# 1차 자료: StatsD README "port: port to listen for messages on [default: 8125]",
#           예 `echo "foo:1|c" | nc -u -w0 127.0.0.1 8125`.
#           node_exporter README "listens on HTTP port 9100 by default".
# 값: 본문 §8 prometheus.yml(scrape_interval 15s, job prometheus → localhost:9090, job machine → 172.17.0.1:9100),
#     curl localhost:9100/metrics 응답("# TYPE go_goroutines gauge", "go_goroutines 7",
#     Content-Type "text/plain; version=0.0.4 ...").
# 타입 스펙: type-data-flow — 두 길에서 데이터가 무엇을 타고 어느 방향으로 흐르는지. 화살표 위에 실제로
#           오가는 값, 상자 안에 목적지 주소를 쥔 설정. focal 은 끌기에서 주소를 쥔 targets 목록.
# 축약: 앱의 목적지 설정 형식은 클라이언트 라이브러리마다 달라 주소 값만 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 600
LX0, LX1, RX0, RX1 = 24, 304, 600, 896
MX = (LX1 + RX0) / 2

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §6",
      "목적지 주소를 쥔 쪽이 반대다",
      "밀기에서는 앱이 목적지 127.0.0.1:8125 를 알고 StatsD 서버로 UDP 데이터그램 \"foo:1|c\" 를 보내며 응답은 없다. "
      "끌기에서는 node exporter 가 HTTP :9100/metrics 를 열어 두기만 하고, Prometheus 가 prometheus.yml 의 "
      "targets(172.17.0.1:9100)를 보고 15초마다 GET /metrics 를 보내 텍스트 메트릭을 받아 간다. "
      "앱이 늘고 줄 때 밀기는 앱마다 목적지를, 끌기는 수집기의 targets 목록 하나를 고친다.",
      "밀기는 앱이 수집기 주소를 알고, 끌기는 수집기가 앱 주소 목록을 쥔다")

# ── 밀기 · StatsD ────────────────────────────────────────────
PY0, PY1, PW = 124, 236, 180
d.t(LX0, PY0 - 12, "밀기 · StatsD", 13, INFO, KR, "start", 600)
d.arrow([(LX1 + 2, PW), (RX0 - 4, PW)], INFO, "info", 1.6)
d.t(MX, PW - 12, '"foo:1|c"', 13, INFO, MONO, "middle", 600)
d.t(MX, PW + 22, "UDP 데이터그램 · 응답 없음", 12, MUTED, KR)

d.box(LX0, PY0, LX1 - LX0, PY1 - PY0, PAPER2, INFO, 1.1, 8)
d.t(LX0 + 16, PY0 + 24, "앱 프로세스", 13, INK, KR, "start", 600)
d.t(LX0 + 16, PY0 + 46, "계측 코드 · StatsD 클라이언트", 12, MUTED, KR, "start")
d.o.append(f'<rect x="{LX0 + 12}" y="{PY0 + 64}" width="{LX1 - LX0 - 24}" height="32" rx="4" '
           f'fill="{WARN}14" stroke="{WARN}" stroke-width="1.1"/>')
d.t(LX0 + 24, PY0 + 85, "목적지 127.0.0.1:8125", 12, WARN, MONO, "start", 600)

d.box(RX0, PY0, RX1 - RX0, PY1 - PY0, PAPER2, INFO, 1.1, 8)
d.t(RX0 + 16, PY0 + 24, "StatsD 서버", 13, INK, KR, "start", 600)
d.t(RX0 + 16, PY0 + 52, "UDP :8125", 13, INFO, MONO, "start", 600)
d.t(RX0 + 100, PY0 + 52, "에서 받음", 12, MUTED, KR, "start")
d.t(RX0 + 16, PY0 + 76, "카운터 foo 에 1", 12, MUTED, KR, "start")

d.t(LX0, PY1 + 26, '$ echo "foo:1|c" | nc -u -w0 127.0.0.1 8125', 12, SOFT, MONO, "start")
d.t(LX0 + 340, PY1 + 26, "README 의 예", 12, SOFT, KR, "start")
d.line(LX0, PY1 + 48, RX1, PY1 + 48, RULE, 0.8)

# ── 끌기 · 스크래핑 ──────────────────────────────────────────
QY0, QY1 = 324, 484
REQ, RES = 372, 440
d.t(LX0, QY0 - 12, "끌기 · 스크래핑", 13, OK, KR, "start", 600)
d.arrow([(RX0 - 2, REQ), (LX1 + 4, REQ)], OK, "ok", 1.6)
d.t(MX, REQ - 12, "GET /metrics", 13, OK, MONO, "middle", 600)
d.t(MX, REQ + 22, "15초마다 · scrape_interval", 12, MUTED, KR)
d.arrow([(LX1 + 2, RES), (RX0 - 4, RES)], OK, "ok", 1.3, "5 4")
d.t(MX, RES - 12, "200 · text/plain; version=0.0.4", 12, OK, MONO, "middle")
d.t(MX, RES + 22, "응답 본문 = 텍스트 메트릭", 12, MUTED, KR)

d.box(LX0, QY0, LX1 - LX0, QY1 - QY0, PAPER2, OK, 1.1, 8)
d.t(LX0 + 16, QY0 + 24, "node exporter", 13, INK, MONO, "start", 600)
d.t(LX0 + 16, QY0 + 48, "HTTP :9100/metrics", 13, OK, MONO, "start", 600)
d.box(LX0 + 12, QY0 + 64, LX1 - LX0 - 24, 52, PAPER, RULE, 0.9, 4)
d.t(LX0 + 24, QY0 + 84, "# TYPE go_goroutines gauge", 12, SOFT, MONO, "start")
d.t(LX0 + 24, QY0 + 104, "go_goroutines 7", 12, INK, MONO, "start")
d.t(LX0 + 16, QY0 + 142, "목적지 설정 없음 · 노출만", 12, SOFT, KR, "start")

d.box(RX0, QY0, RX1 - RX0, QY1 - QY0, PAPER2, OK, 1.1, 8)
d.t(RX0 + 16, QY0 + 24, "Prometheus", 13, INK, MONO, "start", 600)
d.tone(RX0 + 12, QY0 + 36, RX1 - RX0 - 24, 112, ACC, 4, "14", 1.4)
d.t(RX0 + 24, QY0 + 56, "prometheus.yml", 12, SOFT, MONO, "start")
d.t(RX0 + 24, QY0 + 80, "scrape_interval: 15s", 12, INK, MONO, "start")
d.t(RX0 + 24, QY0 + 104, "prometheus → localhost:9090", 12, MUTED, MONO, "start")
d.t(RX0 + 24, QY0 + 128, "machine → 172.17.0.1:9100", 12, ACC, MONO, "start", 600)

d.t(LX0, QY1 + 30, "앱이 늘고 줄 때 고칠 곳 — 밀기: 앱마다의 목적지 · 끌기: targets 목록 하나", 13, INK, KR, "start")
d.t(LX0, QY1 + 56, "주소·포트·간격·응답 줄은 본문 §8 과 StatsD·node_exporter README 값 그대로", 11, SOFT, KR, "start")
LEG = QY1 + 72
d.legend(LEG, [("밀기 흐름", INFO), ("끌기 흐름", OK), ("앱이 쥔 목적지", WARN), ("수집기가 쥔 targets", ACC)])
assert LEG + 40 <= H, (LEG, H)
d.save("08-02.push-pull.svg")
print("ok 08-02.push-pull")
