# 타입 스펙: type-architecture — 노드별 Hubble 서버(에이전트 안) → Hubble Relay → CLI·UI, 에이전트에서 곁으로 나가는 Exporter 파일과 Metrics. 컴포넌트와 포트가 달린 구성도.
# 사실 출처: Cilium Up and Running 15장 cil15.txt 줄 29-40(에이전트 안 Hubble·Relay 는 Deployment), 156-166(port-forward 4245), 429-443(Exporter 파일·10MB·백업 5), 798-808(UI 8081), 912(지표 9965) / docs.cilium.io v1.20 values.yaml(relay listenPort 4245·servicePort 80, listenAddress :4244)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 524
d = D(W, H, "CILIUM UP AND RUNNING · 15-01", "Hubble 구성도",
      "노드의 Hubble 서버가 흐름을 만들고 Relay 가 모으며 파일과 지표로도 나간다",
      "노드의 Hubble 서버가 흐름을 만들고 Relay 가 모으며 파일과 지표로도 나간다")

# 노드 두 칸
for i, nm in enumerate(["노드 1 · cilium-agent", "노드 2 · cilium-agent"]):
    y = 100 + i * 126
    d.box(24, y, 290, 110, PAPER2, RULE, 0.9, r=6)
    d.t(36, y + 22, nm, 11, SOFT, MONO, "start", 600)
    d.tone(40, y + 36, 258, 62, ACC, r=4, op="14", sw=1.0)
    d.t(169, y + 58, "Hubble 서버", 12, ACC, KR, "middle", 600)
    d.chip(169, y + 82, "gRPC :4244", ACC, size=10)

# Relay
d.tone(388, 126, 210, 190, INFO, r=6, op="18", sw=1.4)
d.t(493, 156, "Hubble Relay", 12, INFO, MONO, "middle", 600)
d.t(493, 182, "Deployment", 11, MUTED, MONO)
d.chip(493, 222, "컨테이너 :4245", INFO, size=11)
d.chip(493, 252, "Service :80", INFO, size=10)
d.t(493, 292, "노드 전체 흐름", 11, INK, KR)

# 클라이언트
d.box(684, 100, 212, 236, PAPER2, RULE, 0.9, r=6)
d.box(698, 118, 184, 98, PAPER, WARN, 0.9, r=4)
d.t(790, 142, "Hubble CLI", 12, WARN, MONO, "middle", 600)
d.chip(790, 170, "hubble observe", WARN, size=10)
d.chip(790, 198, "127.0.0.1:4245", WARN, size=10)
d.box(698, 230, 184, 90, PAPER, OK, 0.9, r=4)
d.t(790, 254, "Hubble UI", 12, OK, MONO, "middle", 600)
d.chip(790, 282, "port-forward", OK, size=10)
d.chip(790, 306, "localhost:8081", OK, size=10)

# 노드 → Relay → 클라이언트
d.arrow([(298, 156), (388, 156)], INFO, "info", sw=1.3)
d.arrow([(298, 282), (343, 282), (343, 196), (388, 196)], INFO, "info", sw=1.3)
d.arrow([(598, 168), (698, 168)], WARN, "warn", sw=1.3)
d.arrow([(598, 276), (698, 276)], OK, "ok", sw=1.3)

# 곁으로 나가는 두 길
d.tone(24, 372, 430, 80, OK, r=6, op="10", sw=1.0)
d.t(40, 396, "Exporter", 12, OK, MONO, "start", 600)
d.t(40, 420, "노드의 JSON 파일", 11, INK, KR, "start")
d.chip(330, 424, "/var/run/cilium/hubble/events.log", OK, size=10)
d.tone(466, 372, 430, 80, WARN, r=6, op="10", sw=1.0)
d.t(482, 396, "Metrics", 12, WARN, MONO, "start", 600)
d.t(482, 420, "Prometheus 가 긁어 감", 11, INK, KR, "start")
d.chip(790, 424, "에이전트 :9965", WARN, size=11)
d.arrow([(120, 336), (120, 372)], OK, "ok", sw=1.3)
d.arrow([(240, 336), (240, 354), (560, 354), (560, 372)], WARN, "warn", sw=1.3)

d.legend(480, [("에이전트 안 서버", ACC), ("모으는 Relay", INFO), ("CLI", WARN), ("UI·파일", OK)])
d.save("15-01.chapter-overview.svg")
