# 15-02 §2 — 같은 순간인데 응답이 다른 이유
# 본문이 "요청을 받아 주는 주체가 있느냐"로 이유를 댄다. 그러니 두 경로를 나란히 두되
# 중간에 서 있는 것이 무엇인지가 보여야 한다. kube-proxy 모드 갈림도 함께 적는다.
# 타입 스펙: type-architecture.md — 클라이언트 · 프록시(또는 커널) · 파드 구성도 두 벌. 파드가 없을 때 무엇이 응답하는지가 경로마다 다르다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 900, 636
d = D(W, H, "KUBERNETES IN ACTION · 15-02",
      "받아 주는 주체가 있느냐가 응답을 가른다",
      "가용 파드가 0 인 같은 순간인데 경로마다 다른 답이 온다. Ingress 프록시는 자기가 살아 있으니 "
      "'보낼 곳이 없다'를 상태 코드로 만들어 돌려줄 수 있다.")

lead = "Recreate 의 가용 0 구간에 요청이 들어왔을 때"
d.t(12, 74, lead, 12, MUTED, KR, "start")

def my_node(d, cx, cy, title, sub, w, h, c, dim=False):
    fill = PAPER if dim else PAPER2
    stroke = RULE if dim else c
    sw = 0.9 if dim else 1.2
    tc = SOFT if dim else INK
    d.box(cx - w // 2, cy - h // 2, w, h, fill, stroke, sw, 6)
    d.t(cx, cy - 6, title, 13, tc, KR, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, KR, "middle")

def my_tag(d, cx, cy, txt, c, w=180):
    d.box(cx - w // 2, cy - 14, w, 28, fill=PAPER, stroke=c, sw=1.1, r=4)
    d.t(cx, cy + 5, txt, 12, c, KR, "middle", 600)

def path_row(y0, label, mid, mid_sub, mid_c, ans, ans_sub, ans_c, why):
    d.box(24, y0, W - 48, 200, PAPER2, RULE, 0.9, 8)
    d.t(36, y0 + 26, label, 13, INK, KR, "start", 600)
    cy = y0 + 94
    my_node(d, 114, cy, "클라이언트", "GET /", 140, 64, INFO)
    my_node(d, 316, cy, mid, mid_sub, 180, 64, mid_c)
    d.path(f"M 184 {cy} L 226 {cy}", MUTED, 1.4, m="ar")
    my_node(d, 520, cy, "파드", "하나도 없음", 144, 64, mid_c, dim=True)
    d.path(f"M 406 {cy} L 448 {cy}", BAD, 1.4, m="bad", dash="5 5")
    
    rx = 730
    my_tag(d, rx, cy - 10, ans, ans_c, 196)
    d.t(rx, cy + 22, ans_sub, 12, MUTED, KR, "middle")
    d.t(316, y0 + 172, why, 12, SOFT, KR, "middle")

path_row(96, "Ingress 프록시를 거칠 때", "L7 프록시", "자기는 살아 있음", ACC,
         "503 Service Unavailable", "상태 코드를 만들어 돌려줌", ACC,
         "보낼 곳 없음을 상태 코드로 알림")
path_row(312, "ClusterIP 로 직접 갈 때", "노드 커널", "EndpointSlice 비어 있음", INFO,
         "연결 거부", "iptables · nftables 모드", BAD,
         "readiness 를 잃은 주소는 명단에서 빠짐")

d.t(24, 530, "빈 ClusterIP 의 반응은 kube-proxy 모드에 따라 갈림", 12, MUTED, KR, "start")
d.t(24, 552, "iptables·nftables: 거부 규칙을 심어 연결 거부 · IPVS: 그런 경로가 없어 빈 virtual server 로 남아 타임아웃일 수 있음", 12, MUTED, KR, "start")
d.t(24, 574, "모드는 kube-system 의 kube-proxy ConfigMap, mode 필드에서 확인", 12, MUTED, KR, "start")

def my_legend(d, y, items):
    d.line(12, y, d.w - 48, y, RULE, 0.8)
    d.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
    x = 100
    for lab, c in items:
        d.o.append(f'<rect x="{x}" y="{y+10}" width="14" height="14" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        d.t(x + 22, y + 22, lab, 12, MUTED, KR, "start")
        x += 44 + len(lab) * 14

my_legend(d, 594, [("클라이언트", INFO), ("답을 만들어 주는 주체", ACC), ("끊기는 자리", BAD)])
d.save("15-02-recreate-downtime-clients.svg")
print("ok")
