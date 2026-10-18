# 타입 스펙: type-flowchart
# 사실 출처: portal/server.go:889,917,956-1024, docs/maintainer/architecture.md §TCP bridge ownership, §Admission
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 1120
d = D(
    W, H,
    "PORTAL-TUNNEL · PUBLIC INGRESS FLOWCHART",
    "공개 인그레스 수락 및 라우팅 흐름",
    "TCP 수락부터 ClientHello 검사, API handoff, 브리지 연결 분기",
    lead="128개 검사 슬롯과 1024개 테넌트 슬롯 안에서 소켓을 이관합니다"
)

def diamond(cx, cy, w, h, fill=PAPER2, stroke=RULE, sw=1.0):
    pts = f"{cx},{cy - h/2} {cx + w/2},{cy} {cx},{cy + h/2} {cx - w/2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

def oval(cx, cy, w, h, fill=PAPER2, stroke=RULE, sw=1.0):
    d.box(cx - w/2, cy - h/2, w, h, fill=fill, stroke=stroke, sw=sw, r=h/2)

def rect_box(cx, cy, w, h, fill=PAPER2, stroke=RULE, sw=1.0, r=6):
    d.box(cx - w/2, cy - h/2, w, h, fill=fill, stroke=stroke, sw=sw, r=r)

# 중심 트렁크 X 와 우측 분기 X
CX = 340
RX = 660

# 1. Start: TCP Accept
oval(CX, 106, 200, 36, fill=PAPER2, stroke=INFO, sw=1.2)
d.t(CX, 111, "TCP accept (:958)", 11, INK, fam=MONO, weight=600)

d.arrow([(CX, 124), (CX, 158)], MUTED, "ar", 1.2)

# 2. Decision 1: Inspection slot available?
diamond(CX, 192, 220, 64, fill=PAPER2, stroke=RULE, sw=1.1)
d.t(CX, 187, "검사 슬롯 여유? (:896)", 11, INK, fam=KR, weight=600)
d.t(CX, 203, "ingressInspecting < 128", 10, MUTED, fam=MONO)

# Branch 1 - NO (우측): Slot full -> Close
d.arrow([(CX + 110, 192), (RX - 85, 192)], BAD, "bad", 1.2)
d.chip((CX + 110 + RX - 85) / 2, 182, "128 초과", BAD, size=9)
rect_box(RX, 192, 170, 34, fill=PAPER2, stroke=BAD, sw=1.0, r=4)
d.t(RX, 196, "소켓 Close (:962)", 10.5, BAD, fam=KR, weight=600)

# Branch 1 - YES (아래): admitIngress
d.arrow([(CX, 224), (CX, 258)], OK, "ok", 1.2)
d.chip(CX, 241, "여유", OK, size=9)

# 3. Step 1: admitIngress
rect_box(CX, 280, 240, 42, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(CX, 274, "admitIngress (:889)", 11, INK, fam=MONO, weight=600)
d.t(CX, 292, "inspecting++ · 고루틴", 10, MUTED, fam=KR)

d.arrow([(CX, 301), (CX, 336)], MUTED, "ar", 1.2)

# 4. Step 2: l4.InspectClientHello
rect_box(CX, 358, 240, 42, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(CX, 352, "l4.InspectClientHello (:968)", 11, INK, fam=MONO, weight=600)
d.t(CX, 370, "버퍼 캡처 · 2초 제한", 10, MUTED, fam=KR)

d.arrow([(CX, 379), (CX, 414)], MUTED, "ar", 1.2)

# 5. Decision 2: Parse success in 2s?
diamond(CX, 448, 220, 64, fill=PAPER2, stroke=RULE, sw=1.1)
d.t(CX, 443, "2초 내 파싱 완료? (:968)", 11, INK, fam=KR, weight=600)
d.t(CX, 459, "ClientHello 검증", 10, MUTED, fam=KR)

# Branch 2 - NO (우측): Timeout / non-TLS -> Close
d.arrow([(CX + 110, 448), (RX - 85, 448)], BAD, "bad", 1.2)
d.chip((CX + 110 + RX - 85) / 2, 438, "타임아웃·비TLS", BAD, size=9)
rect_box(RX, 448, 170, 34, fill=PAPER2, stroke=BAD, sw=1.0, r=4)
d.t(RX, 452, "소켓 Close (:971)", 10.5, BAD, fam=KR, weight=600)

# Branch 2 - YES (아래): Normalize & extract helloSpan
d.arrow([(CX, 480), (CX, 514)], OK, "ok", 1.2)
d.chip(CX, 497, "성공", OK, size=9)

# 6. Step 3: ServerName 정규화 & helloSpan 추출
rect_box(CX, 536, 240, 42, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(CX, 530, "ServerName 정규화 (:979)", 11, INK, fam=MONO, weight=600)
d.t(CX, 548, "helloSpan 추출", 10, MUTED, fam=KR)

d.arrow([(CX, 557), (CX, 592)], MUTED, "ar", 1.2)

# 7. Decision 3: Root / Cache / Empty SNI?
diamond(CX, 626, 230, 64, fill=PAPER2, stroke=RULE, sw=1.1)
d.t(CX, 621, "Root / 캐시 / 공백? (:984)", 11, INK, fam=KR, weight=600)
d.t(CX, 637, "serverName 검사", 10, MUTED, fam=KR)

# Branch 3 - YES (우측): API handoff
d.arrow([(CX + 115, 626), (RX - 95, 626)], INFO, "info", 1.2)
d.chip((CX + 115 + RX - 95) / 2, 616, "Root·캐시", INFO, size=9)
rect_box(RX, 626, 190, 42, fill=PAPER2, stroke=INFO, sw=1.1, r=4)
d.t(RX, 620, "API 서버 handoff (:986)", 11, INFO, fam=KR, weight=600)
d.t(RX, 637, "로컬 TCP 홉 없이 전달", 10, MUTED, fam=KR)

# Branch 3 - NO (아래): Tenant promotion
d.arrow([(CX, 658), (CX, 692)], OK, "ok", 1.2)
d.chip(CX, 675, "테넌트 호스트", OK, size=9)

# 8. Decision 4: Tenant slot available?
diamond(CX, 726, 220, 64, fill=PAPER2, stroke=RULE, sw=1.1)
d.t(CX, 721, "테넌트 슬롯 여유? (:920)", 11, INK, fam=KR, weight=600)
d.t(CX, 737, "ingressTenants < 1024", 10, MUTED, fam=MONO)

# Branch 4 - NO (우측): Tenant budget exhausted -> Close
d.arrow([(CX + 110, 726), (RX - 85, 726)], BAD, "bad", 1.2)
d.chip((CX + 110 + RX - 85) / 2, 716, "1024 초과", BAD, size=9)
rect_box(RX, 726, 170, 34, fill=PAPER2, stroke=BAD, sw=1.0, r=4)
d.t(RX, 730, "슬롯 초과 Close (:996)", 10.5, BAD, fam=KR, weight=600)

# Branch 4 - YES (아래): promoteIngress
d.arrow([(CX, 758), (CX, 792)], OK, "ok", 1.2)
d.chip(CX, 775, "여유", OK, size=9)

# 9. Step 4: promoteIngress
rect_box(CX, 814, 240, 42, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(CX, 808, "promoteIngress (:917)", 11, INK, fam=MONO, weight=600)
d.t(CX, 826, "inspecting-- · tenants++", 10, MUTED, fam=MONO)

d.arrow([(CX, 835), (CX, 870)], MUTED, "ar", 1.2)

# 10. Decision 5: registry.Lookup success?
diamond(CX, 904, 220, 64, fill=PAPER2, stroke=RULE, sw=1.1)
d.t(CX, 899, "registry.Lookup 성공? (:1000)", 11, INK, fam=KR, weight=600)
d.t(CX, 915, "임대 레코드 검색", 10, MUTED, fam=KR)

# Branch 5 - NO (우측): Unknown hostname -> Close
d.arrow([(CX + 110, 904), (RX - 85, 904)], BAD, "bad", 1.2)
d.chip((CX + 110 + RX - 85) / 2, 894, "미등록", BAD, size=9)
rect_box(RX, 904, 170, 34, fill=PAPER2, stroke=BAD, sw=1.0, r=4)
d.t(RX, 908, "미등록 Close (:1006)", 10.5, BAD, fam=KR, weight=600)

# Branch 5 - YES (아래): bridgeLeaseConn (Happy path focal)
d.arrow([(CX, 936), (CX, 970)], ACC, "acc", 1.4)
d.chip(CX, 953, "일치", ACC, size=9)

# 11. Final Action: bridgeLeaseConn
rect_box(CX, 1002, 380, 52, fill=PAPER2, stroke=ACC, sw=1.4, r=8)
d.t(CX, 995, "bridgeLeaseConn (:1009, :1026)", 12, ACC, fam=MONO, weight=600)
d.t(CX, 1015, "Issue(:1034) → bridge(:1049)", 10, MUTED, fam=MONO)

# Legend at bottom
d.legend(1060, [
    ("정상 흐름", OK),
    ("종착 (브리지)", ACC),
    ("제어 평면 이관", INFO),
    ("거절 / 소켓 종료", BAD),
])

out_svg = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-02-ingress-flow.svg"))
d.save(out_svg)
print(f"saved: {out_svg}")
