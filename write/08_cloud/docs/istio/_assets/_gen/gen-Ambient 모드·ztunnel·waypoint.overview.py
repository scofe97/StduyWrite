# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""Ambient 모드 개요 도식 — 사이드카 모델과 Ambient 2계층 데이터 플레인 비교.

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
    "ISTIO · DATA PLANE ARCHITECTURE",
    "사이드카 배포와 Ambient 2계층 데이터 플레인 비교",
    "파드마다 주입되던 프록시를 L4 공유 계층과 L7 독립 프록시로 분리한 아키텍처",
    lead="파드 라이프사이클 결합을 해소하고 L4 전송 보안과 L7 트래픽 관리를 분리합니다"
)


def zone(x, y, w, h, label, c=RULE):
    d.o.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
        f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>'
    )
    lw = len(label) * 11 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 17, label, 12, SOFT, KR, "middle")


# ── 왼쪽 구역: 기존 사이드카 모델 (Sidecar Architecture) ──
Z1_X, Z1_Y, Z1_W, Z1_H = 32, 96, 420, 312
zone(Z1_X, Z1_Y, Z1_W, Z1_H, "기존 사이드카 모델", WARN)

# 파드 1
P1_X, P1_Y, P1_W, P1_H = 56, 136, 170, 200
d.box(P1_X, P1_Y, P1_W, P1_H, PAPER, RULE, 0.9, 6)
d.t(P1_X + P1_W // 2, P1_Y + 24, "애플리케이션 Pod A", 12, INK, KR, "middle", 600)
d.tone(P1_X + 16, P1_Y + 44, 138, 56, INFO, 4, "12", 1.0)
d.t(P1_X + P1_W // 2, P1_Y + 74, "App 컨테이너", 12, INFO, KR, "middle")
d.tone(P1_X + 16, P1_Y + 116, 138, 56, WARN, 4, "12", 1.0)
d.t(P1_X + P1_W // 2, P1_Y + 144, "Envoy 사이드카", 12, WARN, KR, "middle", 600)
d.t(P1_X + P1_W // 2, P1_Y + 160, "L4 + L7 동시 처리", 11, MUTED, KR, "middle")

# 파드 2
P2_X, P2_Y, P2_W, P2_H = 258, 136, 170, 200
d.box(P2_X, P2_Y, P2_W, P2_H, PAPER, RULE, 0.9, 6)
d.t(P2_X + P2_W // 2, P2_Y + 24, "애플리케이션 Pod B", 12, INK, KR, "middle", 600)
d.tone(P2_X + 16, P2_Y + 44, 138, 56, INFO, 4, "12", 1.0)
d.t(P2_X + P2_W // 2, P2_Y + 74, "App 컨테이너", 12, INFO, KR, "middle")
d.tone(P2_X + 16, P2_Y + 116, 138, 56, WARN, 4, "12", 1.0)
d.t(P2_X + P2_W // 2, P2_Y + 144, "Envoy 사이드카", 12, WARN, KR, "middle", 600)
d.t(P2_X + P2_W // 2, P2_Y + 160, "L4 + L7 동시 처리", 11, MUTED, KR, "middle")

# 사이드카 간 mTLS 화살표
d.arrow([(P1_X + 154, P1_Y + 144), (P2_X + 16, P2_Y + 144)], WARN, "warn", 1.4)
d.t((P1_X + P2_X + P1_W) // 2, P1_Y + 134, "mTLS", 11, WARN, MONO, "middle")

# 사이드카 하단 문제점 요약 라벨
d.t(Z1_X + Z1_W // 2, Z1_Y + 276, "파드별 프록시 리소스 할당 오버헤드", 11, MUTED, KR, "middle")
d.t(Z1_X + Z1_W // 2, Z1_Y + 296, "프록시 업그레이드 시 파드 재시작 강제", 11, BAD, KR, "middle")


# ── 오른쪽 구역: Ambient 2계층 데이터 플레인 ──
Z2_X, Z2_Y, Z2_W, Z2_H = 484, 96, 444, 312
zone(Z2_X, Z2_Y, Z2_W, Z2_H, "Ambient 2계층 데이터 플레인", OK)

# 앱 워크로드 (사이드카 없음)
AW_X, AW_Y, AW_W, AW_H = 508, 136, 160, 72
d.box(AW_X, AW_Y, AW_W, AW_H, PAPER, RULE, 0.9, 6)
d.t(AW_X + AW_W // 2, AW_Y + 26, "워크로드 Pod A", 12, INK, KR, "middle", 600)
d.tone(AW_X + 16, AW_Y + 36, 128, 26, INFO, 4, "12", 1.0)
d.t(AW_X + AW_W // 2, AW_Y + 53, "순수 App 컨테이너", 11, INFO, KR, "middle")

BW_X, BW_Y, BW_W, BW_H = 744, 136, 160, 72
d.box(BW_X, BW_Y, BW_W, BW_H, PAPER, RULE, 0.9, 6)
d.t(BW_X + BW_W // 2, BW_Y + 26, "워크로드 Pod B", 12, INK, KR, "middle", 600)
d.tone(BW_X + 16, BW_Y + 36, 128, 26, INFO, 4, "12", 1.0)
d.t(BW_X + BW_W // 2, BW_Y + 53, "순수 App 컨테이너", 11, INFO, KR, "middle")

# L4 계층: ztunnel (Node DaemonSet)
ZT1_X, ZT1_Y, ZT1_W, ZT1_H = 508, 236, 160, 56
d.tone(ZT1_X, ZT1_Y, ZT1_W, ZT1_H, OK, 6, "14", 1.2)
d.t(ZT1_X + ZT1_W // 2, ZT1_Y + 24, "Node 1 ztunnel", 12, OK, KR, "middle", 600)
d.t(ZT1_X + ZT1_W // 2, ZT1_Y + 42, "L4 mTLS · SPIFFE", 11, MUTED, KR, "middle")

ZT2_X, ZT2_Y, ZT2_W, ZT2_H = 744, 236, 160, 56
d.tone(ZT2_X, ZT2_Y, ZT2_W, ZT2_H, OK, 6, "14", 1.2)
d.t(ZT2_X + ZT2_W // 2, ZT2_Y + 24, "Node 2 ztunnel", 12, OK, KR, "middle", 600)
d.t(ZT2_X + ZT2_W // 2, ZT2_Y + 42, "L4 mTLS · SPIFFE", 11, MUTED, KR, "middle")

# CNI 리다이렉션 (수직 화살표)
d.arrow([(AW_X + AW_W // 2, AW_Y + AW_H), (ZT1_X + ZT1_W // 2, ZT1_Y)], MUTED, "ar", 1.2)
d.arrow([(BW_X + BW_W // 2, BW_Y + BW_H), (ZT2_X + ZT2_W // 2, ZT2_Y)], MUTED, "ar", 1.2)

# L7 계층: waypoint 프록시 (필요 시 독립 배포)
WP_X, WP_Y, WP_W, WP_H = 548, 324, 316, 54
d.tone(WP_X, WP_Y, WP_W, WP_H, ACC, 6, "14", 1.2)
d.t(WP_X + WP_W // 2, WP_Y + 24, "Waypoint 프록시 (선택적 L7 Envoy)", 12, ACC, KR, "middle", 600)
d.t(WP_X + WP_W // 2, WP_Y + 42, "HTTP 라우팅 · 헤더 조작 · L7 인가 정책", 11, MUTED, KR, "middle")

# ztunnel 간 HBONE 터널 화살표
d.arrow([(ZT1_X + ZT1_W, ZT1_Y + 28), (ZT2_X, ZT2_Y + 28)], OK, "ok", 1.4)
d.t((ZT1_X + ZT1_W + ZT2_X) // 2, ZT1_Y + 20, "HBONE", 11, OK, MONO, "middle")

# waypoint 경유 연결 수직 직교 화살표
d.arrow([(ZT1_X + ZT1_W // 2, ZT1_Y + ZT1_H), (ZT1_X + ZT1_W // 2, WP_Y)], ACC, "acc", 1.2, "3 3")
d.t(ZT1_X + ZT1_W // 2 - 8, WP_Y - 14, "L7 전달", 11, ACC, KR, "end")

d.arrow([(ZT2_X + ZT2_W // 2, WP_Y), (ZT2_X + ZT2_W // 2, ZT2_Y + ZT2_H)], ACC, "acc", 1.2, "3 3")
d.t(ZT2_X + ZT2_W // 2 + 8, WP_Y - 14, "L7 처리 완료", 11, ACC, KR, "start")

d.save(pathlib.Path(__file__).parent.parent / "Ambient 모드·ztunnel·waypoint.overview.svg")
print("생성 완료: Ambient 모드·ztunnel·waypoint.overview.svg")
