# 08-02 §8 — Prometheus·Grafana 단일 기계 구성을 어디서 무엇이 도는지로 그린다.
# 원문("Prometheus and Grafana"): "We'll use the node exporter to expose a range of system metrics, from
#       CPU to memory and network. We'll then use Prometheus to scrape the node exporter. Scraping means
#       that Prometheus calls an HTTP endpoint that the node exporter offers via the URL path /metrics,
#       returning the metrics in OpenMetrics format."
#       구성은 `./node_exporter &` · `curl localhost:9100/metrics` ·
#       prometheus.yml(scrape_interval 15s, targets ['localhost:9090'] 와 ['172.17.0.1:9100']) ·
#       `docker run --name prometheus --rm -d -p 9090:9090 -v .../prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus:main` ·
#       `docker run --name grafana --rm -d -p 3000:3000 grafana/grafana:8.0.3` 이고,
#       이어 "open localhost:9000 in your browser, then click Targets in the Status dropdown menu" 와
#       "Add Prometheus as a datasource in Grafana, using 172.17.0.1:9100 as the URL" 이 나온다.
# 1차 자료: node_exporter README — "The `node_exporter` listens on HTTP port 9100 by default."
#       Prometheus getting_started.md — "about itself at [localhost:9090](http://localhost:9090)".
# 판단: 웹 UI 는 -p 9090:9090 으로 게시한 9090 에 뜨고, Grafana 데이터소스는 Prometheus 이므로 9090 이다.
#       9100 은 node exporter 의 포트다. accent 는 데이터소스 화살표 하나에 건다.
# 타입 스펙: type-deployment — 소프트웨어가 어디서 도는가. 구역(브라우저 · 리눅스 호스트 · Docker 브리지)
#           안에 노드를 놓고 아티팩트와 포트를 붙인다. 축약: 볼륨 마운트 경로는 본문 코드 블록이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 516
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §8",
      "무엇이 어느 기계의 어느 포트에서 도는가",
      "단일 기계 구성을 배치로 그린 것. 화살표 옆이 실제로 넣는 주소이고, 컨테이너에서 호스트로 갈 때는 "
      "Docker 기본 브리지 주소를 쓴다.",
      "Grafana 데이터소스는 :9090 이고 :9100 은 node exporter 입니다")

Z = [("브라우저", 24, 116, 212, 330, MUTED),
     ("리눅스 호스트", 256, 116, 300, 330, INFO),
     ("Docker 브리지 · 172.17.0.1", 584, 116, 272, 330, OK)]
for name, x, y, w, h, col in Z:
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{col}0A" '
               f'stroke="{col}" stroke-width="1.1" stroke-dasharray="4 4"/>')
    d.t(x + 14, y + 22, name, 11, col, KR, "start", 600)

def node(x, y, w, h, tag, title, chip, port, col, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, col, 1.2, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="{len(tag) * 7 + 12}" height="16" rx="2" '
               f'fill="{PAPER}" stroke="{col}" stroke-width="0.9"/>')
    d.t(x + 18, y + 24, tag, 9, col, MONO, "start", 600)
    d.t(x + 14, y + 50, title, 13.5, INK, KR, "start", 600)
    d.o.append(f'<rect x="{x + 12}" y="{y + 60}" width="{w - 24}" height="24" rx="4" '
               f'fill="{INK}0D" stroke="{MUTED}" stroke-width="0.9"/>')
    d.t(x + 22, y + 76, chip, 11, MUTED, MONO, "start")
    d.t(x + w - 22, y + 76, port, 10, col, MONO, "end", 600)

node(36, 160, 188, 100, "USER", "웹 브라우저", "Prometheus UI", ":9090", MUTED)
node(36, 300, 188, 100, "USER", "웹 브라우저", "Grafana UI", ":3000", MUTED)
node(268, 220, 216, 108, "HOST", "node exporter", "./node_exporter &", ":9100", INFO)
node(600, 160, 240, 108, "CONTAINER", "Prometheus", "prom/prometheus:main", ":9090", OK)
node(600, 320, 240, 108, "CONTAINER", "Grafana", "grafana/grafana:8.0.3", ":3000", OK)

d.path(f"M 600 214 L 570 214 L 570 274 L 488 274", OK, 1.3, m="ok")
d.t(548, 250, "15s", 9.5, OK, MONO, "end")
d.t(548, 264, "/metrics", 9.5, OK, MONO, "end")
d.path(f"M 720 318 L 720 274", ACC, 1.5, m="acc")
d.t(730, 288, "datasource", 9.5, ACC, MONO, "start", 600)
d.t(730, 304, "172.17.0.1:9090", 9.5, ACC, MONO, "start", 600)

d.path(f"M 224 205 L 596 205", MUTED, 1.3, m="ar")
d.t(420, 196, "localhost:9090", 10, MUTED, MONO, "middle")
d.path(f"M 224 372 L 596 372", MUTED, 1.3, m="ar")
d.t(420, 363, "localhost:3000", 10, MUTED, MONO, "middle")

d.legend(H - 44, [("Grafana 가 묻는 주소", ACC), ("호스트에서 도는 것", INFO),
                  ("컨테이너에서 도는 것", OK), ("사람이 여는 화면", MUTED)])
d.save("08-02.prom-grafana.svg")
print("ok 08-02.prom-grafana")
