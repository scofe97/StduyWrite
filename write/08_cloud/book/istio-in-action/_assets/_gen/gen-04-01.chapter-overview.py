# 04-01 학습 목표 뒤 개요 그림 — 클러스터 밖 요청 한 건이 서비스에 닿기까지의 줄기.
# 본문 요구(04-01 「학습 목표」): 클라이언트 -> 인그레스 게이트웨이(Envoy) -> Gateway(받아들이는가: 포트·프로토콜·호스트·TLS 모드)
#           -> VirtualService(어디로 보내는가: 호스트·경로 -> 목적지) -> 서비스. TLS 종료 갈래(§4)와 TCP·SNI 패스스루 갈래(§5) 포함.
# 값 근거: 04-01 §1~§6 및 ch04.txt (80·443·31400, Envoy 8080, blackhole:80, SIMPLE·MUTUAL·PASSTHROUGH, Host·:authority·SNI).
# 타입 스펙: type-architecture — 존으로 경계(클러스터 밖 · 인그레스 게이트웨이 · 클러스터 안)를 묶고 직교 화살표로 요청 흐름과 갈래를 잇는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, WARN, KR, MONO

W, H = 984, 608


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 04-01 OVERVIEW",
      "밖의 요청이 인그레스 게이트웨이를 거쳐 서비스에 닿기까지",
      "클러스터 밖 요청이 가상 IP·가상 호스팅을 거쳐 인그레스 게이트웨이(Envoy)에 닿는다. "
      "Gateway가 포트·프로토콜·TLS 모드로 무엇을 받아들일지 정하고, VirtualService가 호스트·경로·SNI로 목적지 서비스를 고른다.",
      lead="칩은 다루는 절, 색은 문제(파랑)·대응(초록)·핵심 분리(코랄)·갈래(노랑)·흐름 밖 판단(회색)이며 왼쪽에서 오른쪽으로 읽습니다.")


def node(x, y, w, h, title, sub, c, sec, sub2=None, op="14"):
    d.tone(x, y, w, h, c, 6, op, 1.2 if c == ACC else 1.1)
    cw = len(sec) * 6.8 + 14
    d.chip(x + cw / 2 + 8, y + 14, sec, c if c != MUTED else MUTED, 11)
    d.t(x + w / 2, y + 40, title, 14, c if c != MUTED else INK, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 76, sub2, 13, MUTED, kr(sub2), "middle")


# 구역 경계 (z-order: zone -> arrows -> nodes; eyebrow 는 존 내부 상단에 16px 여유로 배치)
zones = [
    (16, 104, 184, 344, "OUTSIDE CLUSTER"),
    (272, 104, 444, 424, "INGRESS GATEWAY · ENVOY 8080"),
    (780, 104, 188, 344, "INSIDE MESH"),
]
for zx, zy, zw, zh, zlab in zones:
    d.o.append(f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(zx + 14, zy + 20, zlab, 8, SOFT, MONO, "start")

# 구역 1: 클러스터 밖 (문제)
node(28, 160, 160, 92, "클라이언트", "도메인 → 가상 IP", INFO, "§1", "단일 IP 장애 회피")
node(28, 300, 160, 92, "가상 호스팅 단서", "Host · :authority", INFO, "§1", "TLS · SNI")

# 구역 2: 인그레스 게이트웨이 (핵심 분리 + 갈래)
node(288, 148, 192, 92, "Gateway · 문 열기", "L4·L5 포트·프로토콜", ACC, "§2·§4", "받아들이는 규칙", op="1e")
node(512, 148, 192, 92, "VirtualService", "L7 호스트·경로 → 목적지", OK, "§2·§5", "없으면 blackhole 404")

node(288, 296, 192, 92, "TLS 종료·리다이렉트", "SIMPLE · MUTUAL", OK, "§4", "게이트웨이 인증서 종료")
node(288, 424, 192, 88, "TCP·SNI 패스스루", "포트 · sniHosts", WARN, "§5", "미종료 통과")
node(512, 424, 192, 88, "운영 판단 넷", "쪼개기·주입·로그", MUTED, "§6", "설정 크기 축소")

# 구역 3: 클러스터 안
node(792, 148, 164, 92, "사이드카 서비스", "webapp", OK, "§2·§4", "Auto mTLS 구간")
node(792, 328, 164, 92, "TCP·TLS 백엔드", "tcp-echo-service", WARN, "§5", "simple-tls-service")

# 화살표 (직교 경로, 라벨은 구역 사이 통로에 배치)
# 클라이언트 -> Gateway
d.arrow([(188, 194), (286, 194)], INFO, "info", 1.4)
d.t(236, 184, "진입", 13, MUTED, KR, "middle", 600)

# 가상 호스팅 단서 -> Gateway 아래로 진입
d.arrow([(188, 346), (236, 346), (236, 212), (286, 212)], INFO, "info", 1.3, "4 3")
d.t(236, 366, "단서 판별", 13, MUTED, KR, "middle")

# Gateway -> VirtualService (핵심 handoff)
d.arrow([(480, 194), (510, 194)], ACC, "acc", 1.5)
d.t(496, 182, "허용", 13, ACC, KR, "middle", 600)

# Gateway -> TLS 종료 (하단)
d.arrow([(384, 240), (384, 294)], OK, "ok", 1.3)
d.t(394, 272, "HTTPS 종료", 13, MUTED, KR, "start")

# TLS 종료 -> VirtualService
d.arrow([(480, 342), (496, 342), (496, 224), (510, 224)], OK, "ok", 1.3)
d.t(504, 290, "복호화 뒤", 13, MUTED, KR, "start")

# Gateway -> TCP/SNI 패스스루 (왼쪽 통로)
d.arrow([(288, 234), (278, 234), (278, 468), (286, 468)], WARN, "warn", 1.3)
d.t(264, 468, "비-HTTP", 13, MUTED, KR, "end")

# VirtualService -> 사이드카 서비스
d.arrow([(704, 194), (790, 194)], OK, "ok", 1.5)
d.t(746, 182, "라우트", 13, OK, KR, "middle", 600)

# TCP/SNI 패스스루 -> TCP/TLS 백엔드
d.arrow([(480, 468), (496, 468), (496, 374), (790, 374)], WARN, "warn", 1.4)
d.t(638, 364, "SNI · 포트 매칭 전달", 13, WARN, KR, "middle")

d.legend(H - 44, [
    ("진입 문제", INFO),
    ("문 열기(핵심)", ACC),
    ("길 내기 · TLS 대응", OK),
    ("비-HTTP 갈래", WARN),
    ("흐름 밖 판단", MUTED),
])
d.save("04-01.chapter-overview.svg")
print("ok 04-01 chapter-overview")
