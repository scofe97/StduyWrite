# 타입 스펙: type-data-flow — LB IPAM 풀에서 배정된 외부 IP 와 NodePort·ClusterIP 프런트엔드가 같은 서비스 맵과 백엔드로 모이는 흐름. 배정된 배치 타입 대신 흐름 문법의 이 타입으로 바꿨다
# 사실 출처: 추출본 cil6.txt 줄 888-920·964-991(풀·192.168.9.1·10.96.72.137·31478), 1045-1048(광고는 별도) / docs.cilium.io v1.20 kubeproxy-free(Selective Service Type Exposure), lb-ipam
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "CILIUM UP AND RUNNING · 06-01 §6", "한 서비스의 세 프런트엔드와 외부 IP",
      "풀이 IP 를 붙이고 세 주소가 같은 맵과 백엔드로 모입니다",
      "httpd 서비스 · LoadBalancer · 80:31478/TCP")

CX, CW = 12, 188
FX, FW = 268, 216
MX, MW = 552, 148
BX, BW = 768, 140
BH = 60
Y = [120, 204, 288]
for x, w, t in [(CX, CW, "CLIENT"), (FX, FW, "FRONTEND"), (MX, MW, "SERVICE MAP"), (BX, BW, "BACKEND")]:
    d.t(x + w / 2, 104, t, 8, SOFT, MONO, "middle")

clients = [("클러스터 안 Pod", "ClusterIP 로 호출"), ("외부 클라이언트", "노드 IP 로 호출"), ("외부 클라이언트", "LB IP 로 호출")]
fronts = [("10.96.72.137:80", "ClusterIP", INFO), ("노드 IP:31478", "NodePort", INFO), ("192.168.9.1:80", "LoadBalancer", WARN)]
for y, (cn, cs), (fa, ft, fc) in zip(Y, clients, fronts):
    d.box(CX, y, CW, BH, PAPER2, RULE, 0.9)
    d.t(CX + CW / 2, y + 26, cn, 12, INK, KR, "middle", 600)
    d.t(CX + CW / 2, y + 46, cs, 11, MUTED, KR)
    d.box(FX, y, FW, BH, PAPER2, fc, 1.0)
    d.t(FX + FW / 2, y + 26, fa, 12, INK, MONO, "middle", 600)
    d.t(FX + FW / 2, y + 46, ft, 11, fc, MONO)
    cy = y + BH / 2
    d.arrow([(CX + CW, cy), (FX, cy)], MUTED, "ar", 1.5)
    d.arrow([(FX + FW, cy), (MX, 204 + BH / 2)] if False else [(FX + FW, cy), (FX + FW + 34, cy), (FX + FW + 34, 234), (MX, 234)], MUTED, "ar", 1.4)

d.tone(MX, 188, MW, 92, ACC, r=6, op="14", sw=1.4)
d.t(MX + MW / 2, 222, "eBPF 맵", 13, ACC, KR, "middle", 600)
d.t(MX + MW / 2, 244, "조회 · 백엔드 선택", 11, MUTED, KR)
d.box(BX, 204, BW, BH, PAPER2, OK, 1.0)
d.t(BX + BW / 2, 230, "httpd Pod", 12, OK, MONO, "middle", 600)
d.t(BX + BW / 2, 250, "Ready 백엔드", 11, MUTED, KR)
d.arrow([(MX + MW, 234), (BX, 234)], OK, "ok", 1.5)

PY = 400
d.box(FX, PY, FW, BH, PAPER2, WARN, 1.0)
d.t(FX + FW / 2, PY + 26, "lb-pool", 12, INK, MONO, "middle", 600)
d.t(FX + FW / 2, PY + 46, "192.168.9.0/24 · \"No\"", 11, WARN, MONO)
d.arrow([(FX + FW / 2, PY), (FX + FW / 2, Y[2] + BH)], WARN, "warn", 1.5)
d.t(FX + FW / 2 + 10, (PY + Y[2] + BH) / 2 + 4, "IP 배정", 11, WARN, KR, "start")

d.box(CX, PY, CW, BH, PAPER2, SOFT, 1.0)
d.t(CX + CW / 2, PY + 26, "BGP · L2 Announcements", 11, INK, MONO, "middle", 600)
d.t(CX + CW / 2, PY + 46, "LB IP 광고", 11, MUTED, KR)
d.arrow([(CX + CW / 2, PY), (CX + CW / 2, Y[2] + BH)], SOFT, "soft", 1.4, "4 4")

d.legend(PY + BH + 28, [("LB IPAM 배정", WARN), ("프런트엔드", INFO), ("eBPF 맵", ACC), ("백엔드", OK)])
d.save("06-01.lb-ipam-flow.svg")
