# 08-02 §8 — Prometheus·Grafana 단일 기계 구성을 한 호스트 안의 실제 자리로 그린다. 호스트에서 도는
#           node exporter(:9100), -p 로 게시한 호스트 포트 :9090 · :3000, 그 뒤의 두 컨테이너, 같은 호스트의
#           브라우저. 컨테이너 안의 localhost 는 컨테이너 자신이라 컨테이너에서 호스트로 갈 때는 Docker 기본
#           브리지 주소 172.17.0.1 을 쓴다 — 긁기(172.17.0.1:9100)와 데이터소스(172.17.0.1:9090)가 그 길이다.
# 원문("Prometheus and Grafana"): `./node_exporter &` · `curl localhost:9100/metrics` ·
#       prometheus.yml(scrape_interval 15s, job prometheus → localhost:9090, job machine → 172.17.0.1:9100) ·
#       `docker run --name prometheus --rm -d -p 9090:9090 -v .../prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus:main` ·
#       `docker run --name grafana --rm -d -p 3000:3000 grafana/grafana:8.0.3`.
# 1차 자료: node_exporter README — "The `node_exporter` listens on HTTP port 9100 by default."
#       Prometheus getting_started — "about itself at localhost:9090", "localhost:9090/targets, or open the
#       Status menu and select Target health".
# 판단(본문 §8 과 같음): 웹 UI 는 -p 9090:9090 으로 게시한 9090, Grafana 데이터소스는 Prometheus 이므로
#       http://172.17.0.1:9090. 9100 을 넣으면 exporter 를 가리킨다. accent 는 데이터소스 길.
# 타입 스펙: type-deployment — 소프트웨어가 어디서 도는가. 호스트 존 안에 호스트 프로세스 · 호스트 포트 ·
#           컨테이너 존을 놓고, 요청이 지나는 포트를 실제 주소로 잇는다.
# 축약: 컨테이너 자체의 브리지 IP 는 본문에 없어 그리지 않았다. 볼륨 원본 경로(/home/mh9/...)는 본문 코드 블록이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 652
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §8",
      "한 호스트, 포트 셋, 두 컨테이너",
      "한 리눅스 호스트에서 node exporter 는 호스트 프로세스로 :9100 을 열고, Prometheus 와 Grafana 컨테이너는 "
      "-p 9090:9090 · -p 3000:3000 으로 호스트 포트에 게시된다. 같은 호스트의 브라우저는 localhost:9090/targets 와 "
      "localhost:3000 을 연다. 컨테이너 안의 localhost 는 컨테이너 자신이라 Prometheus 는 172.17.0.1:9100 을 15초마다 "
      "긁고, Grafana 는 데이터소스 http://172.17.0.1:9090 으로 Prometheus 에 묻는다.",
      "같은 172.17.0.1 뒤에서 포트만 다르다 — Grafana 가 묻는 곳은 :9090 이고 :9100 은 node exporter 다")

HX0, HX1, HY0, HY1 = 24, 896, 104, 512          # 호스트
LX0, LX1 = 48, 256                              # 호스트 프로세스 · 브라우저 열
PX0, PX1 = 304, 408                             # 호스트 포트 열
CX0, CX1, CY0, CY1 = 456, 872, 208, 496         # 컨테이너 존
BX0, BX1 = 480, 856                             # 컨테이너 상자
A, B, C = 176, 284, 440                         # 줄 y: :9100 · :9090 · :3000
B2 = 312                                        # :9090 으로 들어오는 둘째 길(Grafana)

# ── 존(맨 아래) ──────────────────────────────────────────────
d.o.append(f'<rect x="{HX0}" y="{HY0}" width="{HX1 - HX0}" height="{HY1 - HY0}" rx="10" fill="{INFO}08" '
           f'stroke="{INFO}" stroke-width="1.1" stroke-dasharray="5 4"/>')
d.t(HX0 + 16, HY0 + 22, "리눅스 호스트 · 한 기계", 13, INFO, KR, "start", 600)
d.o.append(f'<rect x="{CX0}" y="{CY0}" width="{CX1 - CX0}" height="{CY1 - CY0}" rx="8" fill="{OK}0A" '
           f'stroke="{OK}" stroke-width="1.1" stroke-dasharray="4 4"/>')
d.t(552, CY0 + 22, "Docker 컨테이너", 12, OK, KR, "start", 600)

# ── 길(상자보다 먼저) ────────────────────────────────────────
# 브라우저 → 호스트 포트 → 컨테이너
for y in (B, C):
    d.arrow([(LX1 + 2, y), (PX0 - 4, y)], MUTED, "ar", 1.3)
    d.arrow([(PX1 + 2, y), (BX0 - 4, y)], MUTED, "ar", 1.3)
# Prometheus → 172.17.0.1:9100 → node exporter (긁기)
d.arrow([(520, 246), (520, A), (PX1 + 4, A)], OK, "ok", 1.5)
d.arrow([(PX0 - 2, A), (LX1 + 4, A)], OK, "ok", 1.5)
d.t(466, A - 10, "15s /metrics", 12, OK, MONO, "middle", 600)
# Grafana → 172.17.0.1:9090 → Prometheus (데이터소스, focal)
d.arrow([(BX0 - 2, 404), (356, 404), (356, 332)], ACC, "acc", 1.8)          # 포트 :9090 아래로 들어감
d.arrow([(PX1 + 2, B2), (BX0 - 4, B2)], ACC, "acc", 1.2, "4 3")             # 게시된 포트 → Prometheus

# ── 호스트 프로세스와 브라우저 ───────────────────────────────
d.box(LX0, 144, LX1 - LX0, 64, PAPER2, INFO, 1.2, 6)
d.t(LX0 + 14, 168, "./node_exporter &", 13, INK, MONO, "start", 600)
d.t(LX0 + 14, 192, "호스트 프로세스", 12, INFO, KR, "start")

d.box(LX0, 236, LX1 - LX0, 236, PAPER2, MUTED, 1.0, 6)
d.t(LX0 + 14, 256, "웹 브라우저", 13, INK, KR, "start", 600)
for y, url, sub, sy in ((B, "localhost:9090/targets", "Prometheus UI · Target health", B + 36),
                        (C, "localhost:3000", "Grafana UI", C - 24)):
    d.box(LX0 + 12, y - 16, LX1 - LX0 - 24, 32, PAPER, MUTED, 0.9, 4)
    d.t(LX0 + 22, y + 5, url, 12, INK, MONO, "start")
    d.t(LX0 + 14, sy, sub, 12, MUTED, KR, "start")

# ── 호스트 포트 ──────────────────────────────────────────────
d.t((PX0 + PX1) / 2, 140, "호스트 포트", 12, INK, KR, "middle", 600)
for y0, y1, port, sub, c in ((156, 196, ":9100", "exporter", INFO), (264, 328, ":9090", "-p 게시", OK),
                             (420, 460, ":3000", "-p 게시", OK)):
    d.box(PX0, y0, PX1 - PX0, y1 - y0, PAPER2, c, 1.3, 6)
    cy = (y0 + y1) / 2
    d.t((PX0 + PX1) / 2, cy - 1, port, 14, c, MONO, "middle", 600)
    d.t((PX0 + PX1) / 2, cy + 15, sub, 11, MUTED, MONO if sub.isascii() else KR)

# ── 컨테이너 ─────────────────────────────────────────────────
d.box(BX0, 248, BX1 - BX0, 120, PAPER2, OK, 1.2, 6)
d.t(BX0 + 16, 270, "Prometheus", 13, INK, MONO, "start", 600)
d.t(BX1 - 14, 270, "prom/prometheus:main", 12, MUTED, MONO, "end")
d.t(BX0 + 16, 294, "-p 9090:9090", 12, MUTED, MONO, "start")
d.t(BX0 + 16, 316, "-v → /etc/prometheus/prometheus.yml", 12, MUTED, MONO, "start")
d.t(BX0 + 16, 340, "machine → 172.17.0.1:9100", 12, OK, MONO, "start", 600)
d.t(BX0 + 16, 360, "prometheus → localhost:9090", 12, MUTED, MONO, "start")
d.t(BX1 - 14, 360, "자기 자신", 12, SOFT, KR, "end")

d.box(BX0, 392, BX1 - BX0, 88, PAPER2, OK, 1.2, 6)
d.t(BX0 + 16, 414, "Grafana", 13, INK, MONO, "start", 600)
d.t(BX1 - 14, 414, "grafana/grafana:8.0.3", 12, MUTED, MONO, "end")
d.t(BX0 + 16, 438, "-p 3000:3000", 12, MUTED, MONO, "start")
d.t(BX0 + 16, 464, "datasource http://172.17.0.1:9090", 12, ACC, MONO, "start", 600)

# ── 아래 줄 ──────────────────────────────────────────────────
NY = HY1 + 32
d.t(HX0, NY, "컨테이너 안 localhost = 컨테이너 자신 · 호스트 = 172.17.0.1", 13, INK, KR, "start")
d.t(HX0, NY + 26, "✕ datasource :9100 → node exporter 를 가리킴", 12, BAD, KR, "start")
d.t(HX0, NY + 50, "포트 · 이미지 · 주소 · 간격은 본문 §8 의 설정과 명령 그대로 · 컨테이너 자체의 IP 는 본문에 없어 생략",
    11, SOFT, KR, "start")
LEG = NY + 66
d.legend(LEG, [("데이터소스 길", ACC), ("호스트에서 도는 것", INFO), ("컨테이너 · 긁기", OK), ("사람이 여는 화면", MUTED)])
assert LEG + 40 <= H, (LEG, H)
d.save("08-02.prom-grafana.svg")
print("ok 08-02.prom-grafana")
