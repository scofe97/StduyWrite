# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·대표 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: §1 Prometheus 노출 형식 문서의 예 줄(http_requests_total{method="post",code="200"} 1027 1395066363000, prometheus/docs 605cf81 docs/instrumenting/exposition_formats.md L130)과 데이터 모델 문서(밀리초 정밀도 타임스탬프),
#   §2 InfluxDB v1 OSS 하드웨어 산정 표의 마지막 행(8+ 코어 · 32+ GB · 쓰기 초당 250,000 초과, docs.influxdata.com/influxdb/v1/guides/hardware_sizing/),
#   §3 Prometheus v3.15.0 docs/configuration/configuration.md L57(scrape_interval 기본 1m)·L61(scrape_timeout 기본 10s)·L347(metrics_path 기본 /metrics),
#   §4 Prometheus v3.15.0 docs/storage.md L14(2시간 블록)·L95(보존 기본 15d)와 Thanos v0.42.4 docs/components/compact.md L166-L167(40시간·10일),
#   §5 Prometheus v3.15.0 docs/configuration/alerting_rules.md L35-L39(for 절·pending 상태)·L76-L78(InstanceDown 규칙의 for: 5m)와 Grafana Mimir 3.2.2 query-frontend 문서 L37(분할 간격 기본 24시간).
# Layout conventions: 카드 폭 168·높이 212, 가로 stride 184(x=20+184k), 카드 y=112, 화살표는 카드 중앙 y=218. 5 카드. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 08-03",
      "메트릭 한 점이 지나는 다섯 자리",
      "노출된 값 하나가 수집·저장·질의·경보를 지나며 값 하나씩을 들고 이어집니다.",
      "절마다 대표 값 하나씩을 달았습니다")

CW, CH, STRIDE, X0, Y0 = 168, 212, 184, 20, 112
cards = [
    ("§1", "시계열 한 점", "1027", "@ 1395066363000 ms", "이름 + 라벨이 시계열", INFO),
    ("§2", "시계열 DB", "250,000 초과/초", "8+ 코어 · 32+ GB", "쓰기가 몰리는 쪽", ACC),
    ("§3", "당기기와 밀기", "1m · 10s", "HTTP /metrics", "수집 간격 · 제한 시간", INFO),
    ("§4", "저장 · 보존", "2시간 블록", "15d · 40h · 10d", "보존 · 다운샘플링", INFO),
    ("§5", "질의 · 경보", "for: 5m", "분할 24시간", "pending → firing", INFO),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, MONO, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 13, c, KR if any("가" <= ch <= "힣" for ch in v1) else MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 13, INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 13, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("08-03.chapter-overview.svg")
