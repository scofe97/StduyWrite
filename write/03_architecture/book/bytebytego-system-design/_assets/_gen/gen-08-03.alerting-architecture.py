# 타입 스펙: type-architecture — 메트릭 소스에서 수집기·Kafka·소비자를 거쳐 시계열 DB 에 쌓이는 쓰기 경로와, 시계열 DB 앞의 질의 서비스를 경보 시스템과 시각화가 함께 쓰는 읽기·경보 경로. 노드 아래 작은 글씨는 그 자리를 현재 채우는 실제 구성 요소다.
# 사실 출처: ByteByteGo 그림 해설 모음의 메트릭 모니터링 구성도(추출본 v1.txt 3228~3270행, PDF 쪽 130 그림: Metrics Source → Collector → Kafka → Consumers → Time series DB, Query Service 와 Cache, Alert System → Email·Text Message·PagerDuty·HTTPS Endpoints, Visualization System),
#   Grafana Mimir 3.2.2 docs about-grafana-mimir-architecture/_index.md L20-L24(3.0 부터 ingest storage 가 preferred, Kafka 로 읽기·쓰기를 분리)·about-ingest-storage-architecture/index.md L12·L33-L36(distributor 가 Kafka 로 쓰고 ingester 가 파티션을 소비, 수집기 Prometheus 는 remote write 로 distributor 에 보낸다: _index.md L28 의 remote write 와 L34 의 distributor 처리),
#   query-frontend/index.md L37·L43-L46(24시간 분할·결과 캐시), Alertmanager v0.34.1 docs/alertmanager.md L7-L10(중복 제거·그룹·라우팅, email·PagerDuty 등 수신자)·docs/configuration.md `<email_config>` L1055·`<pagerduty_config>` L1468·`<sns_config>` L1785(phone_number L1810 은 SMS)·`<webhook_config>` L1939.
#   원 그림의 PageDuty 는 PagerDuty 의 오기라서 바른 표기를 썼다. 캐시는 원 그림의 별도 상자를 질의 서비스 노드에 합쳤다.
# Layout conventions: 노드 폭 148·높이 68, 가로 stride 196(x=24+196k), 행 y=116·268·420, 노드 사이 화살표 폭 44. 채널 묶음 상자 x=216 폭 332. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


W, H = 1000, 560
d = D(W, H, "BYTEBYTEGO · 08-03 §5",
      "경보와 시각화는 같은 질의 서비스를 지나 시계열 DB 를 읽는다",
      "쓰기는 수집기에서 Kafka 를 거쳐 쌓이고 읽기와 경보는 질의 서비스 한 곳으로 모입니다.",
      "노드 아래 글씨는 그 자리를 채우는 실제 구성 요소(Grafana Mimir 3.x · Alertmanager)입니다")

NW, NH, STR, X0 = 148, 68, 196, 24


def node(x, y, name, sub, c=None, focal=False, w=NW):
    if focal:
        d.tone(x, y, w, NH, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, w, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 30, name, 13, ACC if focal else INK, _kr(name), "middle", 600)
    d.t(x + w / 2, y + 52, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub), "middle")


# 쓰기 경로
d.t(24, 104, "쓰기 경로", 13, SOFT, KR, "start")
row1 = [("메트릭 소스", "웹 서버 · DB · 큐"), ("수집기", "Prometheus"), ("Kafka", "distributor → Kafka"),
        ("소비자", "Mimir ingester"), ("시계열 DB", "TSDB 블록")]
for k, (a, b) in enumerate(row1):
    x = X0 + k * STR
    node(x, 116, a, b)
    if k < len(row1) - 1:
        d.arrow([(x + NW + 2, 150), (x + STR - 4, 150)], MUTED, "ar", 1.5)

# 읽기 · 경보 경로
d.t(24, 256, "읽기 · 경보 경로", 13, SOFT, KR, "start")
XQ, XA = X0 + 4 * STR, X0 + 3 * STR
node(XQ, 268, "질의 서비스 · 캐시", "query-frontend", focal=True)
node(XA, 268, "경보 시스템", "rule · Alertmanager")
d.box(216, 268, 332, NH, PAPER2, RULE, 1.0, 6)
d.t(216 + 166, 298, "알림 채널", 13, INK, KR, "middle", 600)
d.t(216 + 166, 320, "Email · SMS · PagerDuty · webhook", 12, MUTED, MONO, "middle")
node(XQ, 420, "시각화", "Grafana")

# 화살표
d.arrow([(XQ + NW / 2, 266), (XQ + NW / 2, 186)], INFO, "info", 1.5)
d.t(XQ + NW / 2 + 12, 232, "질의", 13, INFO, KR, "start")
d.arrow([(XA + NW + 2, 302), (XQ - 4, 302)], INFO, "info", 1.5)
d.arrow([(XQ + NW / 2, 418), (XQ + NW / 2, 340)], INFO, "info", 1.5)
d.t(XQ + NW / 2 + 12, 384, "질의", 13, INFO, KR, "start")
d.arrow([(XA - 2, 302), (552, 302)], WARN, "warn", 1.5)
d.t(582, 292, "전송", 13, WARN, KR, "middle")

d.legend(H - 44, [("쓰기 경로", MUTED), ("질의", INFO), ("경보 전송", WARN), ("이 절의 초점", ACC)])
d.save("08-03.alerting-architecture.svg")
