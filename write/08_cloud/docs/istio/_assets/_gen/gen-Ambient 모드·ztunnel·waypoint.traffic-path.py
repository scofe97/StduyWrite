# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""Ambient 모드 트래픽 경로 도식 — L4 기본 경로와 L7 waypoint 경유 경로 비교.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
스킨은 writing-method Diagram Design 스타일 계약의 다크 토큰을 쓴다.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 440

d = D(
    W, H,
    "TRAFFIC PATH · HBONE OVERLAY",
    "Ambient 모드의 두 가지 트래픽 경로 — L4 전송과 L7 waypoint 경유",
    "L4 보안 오버레이만 거치는 기본 경로와 L7 정책 집행을 위해 waypoint 를 경유하는 경로",
    lead="정책 요구사항에 따라 불필요한 L7 프록시 홉 없이 필요한 계층만 선택적으로 거칩니다"
)


def zone(x, y, w, h, label, c=RULE):
    d.o.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
        f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>'
    )
    lw = len(label) * 11 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 17, label, 12, SOFT, KR, "middle")


# ── 상단 구역: 경로 1 — L4 전용 통신 (기본 경로) ──
Z1_X, Z1_Y, Z1_W, Z1_H = 32, 96, 896, 140
zone(Z1_X, Z1_Y, Z1_W, Z1_H, "경로 1: L4 전용 통신 (mTLS · L4 인가 · 텔레메트리)", OK)

# Pod A
P1_X, P1_Y, P1_W, P1_H = 64, 136, 140, 68
d.box(P1_X, P1_Y, P1_W, P1_H, PAPER, INFO, 1.0, 6)
d.t(P1_X + P1_W // 2, P1_Y + 28, "클라이언트 Pod A", 12, INK, KR, "middle", 600)
d.t(P1_X + P1_W // 2, P1_Y + 50, "App (평문 TCP)", 11, MUTED, KR, "middle")

# Node 1 ztunnel
ZT1_X, ZT1_Y, ZT1_W, ZT1_H = 264, 136, 150, 68
d.tone(ZT1_X, ZT1_Y, ZT1_W, ZT1_H, OK, 6, "14", 1.2)
d.t(ZT1_X + ZT1_W // 2, ZT1_Y + 28, "Node 1 ztunnel", 12, OK, KR, "middle", 600)
d.t(ZT1_X + ZT1_W // 2, ZT1_Y + 50, "HBONE 캡슐화", 11, MUTED, KR, "middle")

# Node 2 ztunnel
ZT2_X, ZT2_Y, ZT2_W, ZT2_H = 554, 136, 150, 68
d.tone(ZT2_X, ZT2_Y, ZT2_W, ZT2_H, OK, 6, "14", 1.2)
d.t(ZT2_X + ZT2_W // 2, ZT2_Y + 28, "Node 2 ztunnel", 12, OK, KR, "middle", 600)
d.t(ZT2_X + ZT2_W // 2, ZT2_Y + 50, "mTLS 종단 · L4 인가", 11, MUTED, KR, "middle")

# Pod B
P2_X, P2_Y, P2_W, P2_H = 764, 136, 140, 68
d.box(P2_X, P2_Y, P2_W, P2_H, PAPER, INFO, 1.0, 6)
d.t(P2_X + P2_W // 2, P2_Y + 28, "목적지 Pod B", 12, INK, KR, "middle", 600)
d.t(P2_X + P2_W // 2, P2_Y + 50, "App (평문 전달)", 11, MUTED, KR, "middle")

# 화살표 1: Pod A -> Node 1 ztunnel
d.arrow([(P1_X + P1_W, P1_Y + 34), (ZT1_X, ZT1_Y + 34)], INFO, "info", 1.2)

# 화살표 2: ztunnel -> ztunnel (HBONE 터널)
d.arrow([(ZT1_X + ZT1_W, ZT1_Y + 34), (ZT2_X, ZT2_Y + 34)], OK, "ok", 1.5)
d.t((ZT1_X + ZT1_W + ZT2_X) // 2, ZT1_Y + 24, "HBONE 터널 (TCP:15008)", 11, OK, MONO, "middle")

# 화살표 3: Node 2 ztunnel -> Pod B
d.arrow([(ZT2_X + ZT2_W, ZT2_Y + 34), (P2_X, P2_Y + 34)], INFO, "info", 1.2)


# ── 하단 구역: 경로 2 — L7 정책 적용 통신 (waypoint 경유) ──
Z2_X, Z2_Y, Z2_W, Z2_H = 32, 256, 896, 156
zone(Z2_X, Z2_Y, Z2_W, Z2_H, "경로 2: L7 정책 적용 통신 (HTTP 라우팅 · 헤더 조작 · L7 인가)", ACC)

# Pod A
Q1_X, Q1_Y, Q1_W, Q1_H = 64, 304, 130, 68
d.box(Q1_X, Q1_Y, Q1_W, Q1_H, PAPER, INFO, 1.0, 6)
d.t(Q1_X + Q1_W // 2, Q1_Y + 28, "클라이언트 Pod A", 12, INK, KR, "middle", 600)
d.t(Q1_X + Q1_W // 2, Q1_Y + 50, "HTTP 요청 생성", 11, MUTED, KR, "middle")

# Node 1 ztunnel
ZQ1_X, ZQ1_Y, ZQ1_W, ZQ1_H = 244, 304, 130, 68
d.tone(ZQ1_X, ZQ1_Y, ZQ1_W, ZQ1_H, OK, 6, "14", 1.2)
d.t(ZQ1_X + ZQ1_W // 2, ZQ1_Y + 28, "Node 1 ztunnel", 12, OK, KR, "middle", 600)
d.t(ZQ1_X + ZQ1_W // 2, ZQ1_Y + 50, "Waypoint 로 전달", 11, MUTED, KR, "middle")

# Waypoint Proxy
WP_X, WP_Y, WP_W, WP_H = 434, 300, 160, 76
d.tone(WP_X, WP_Y, WP_W, WP_H, ACC, 6, "14", 1.4)
d.t(WP_X + WP_W // 2, WP_Y + 26, "Waypoint 프록시", 12, ACC, KR, "middle", 600)
d.t(WP_X + WP_W // 2, WP_Y + 46, "HTTPRoute · L7 인가", 11, INK, KR, "middle")
d.t(WP_X + WP_W // 2, WP_Y + 62, "Envoy L7 독립 배포", 11, MUTED, KR, "middle")

# Node 2 ztunnel
ZQ2_X, ZQ2_Y, ZQ2_W, ZQ2_H = 654, 304, 130, 68
d.tone(ZQ2_X, ZQ2_Y, ZQ2_W, ZQ2_H, OK, 6, "14", 1.2)
d.t(ZQ2_X + ZQ2_W // 2, ZQ2_Y + 28, "Node 2 ztunnel", 12, OK, KR, "middle", 600)
d.t(ZQ2_X + ZQ2_W // 2, ZQ2_Y + 50, "목적지 파드로 전달", 11, MUTED, KR, "middle")

# Pod B
Q2_X, Q2_Y, Q2_W, Q2_H = 834, 304, 74, 68
d.box(Q2_X, Q2_Y, Q2_W, Q2_H, PAPER, INFO, 1.0, 6)
d.t(Q2_X + Q2_W // 2, Q2_Y + 28, "Pod B", 12, INK, KR, "middle", 600)
d.t(Q2_X + Q2_W // 2, Q2_Y + 50, "App", 11, MUTED, KR, "middle")

# 화살표들
d.arrow([(Q1_X + Q1_W, Q1_Y + 34), (ZQ1_X, ZQ1_Y + 34)], INFO, "info", 1.2)
d.arrow([(ZQ1_X + ZQ1_W, ZQ1_Y + 34), (WP_X, WP_Y + 38)], ACC, "acc", 1.4)
d.t((ZQ1_X + ZQ1_W + WP_X) // 2, ZQ1_Y + 24, "HBONE", 11, ACC, MONO, "middle")

d.arrow([(WP_X + WP_W, WP_Y + 38), (ZQ2_X, ZQ2_Y + 34)], ACC, "acc", 1.4)
d.t((WP_X + WP_W + ZQ2_X) // 2, ZQ2_Y + 24, "HBONE", 11, ACC, MONO, "middle")

d.arrow([(ZQ2_X + ZQ2_W, ZQ2_Y + 34), (Q2_X, Q2_Y + 34)], INFO, "info", 1.2)

d.save(pathlib.Path(__file__).parent.parent / "Ambient 모드·ztunnel·waypoint.traffic-path.svg")
print("생성 완료: Ambient 모드·ztunnel·waypoint.traffic-path.svg")
