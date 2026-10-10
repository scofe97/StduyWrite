# 타입 스펙: type-layers — VXLAN 터널과 WireGuard 암호화가 중첩된 패킷의 헤더 겹. 바깥에서 안쪽 순으로 6개 층, focal 은 WireGuard 로 암호화된 페이로드 층.
# 사실 출처: Cilium Up and Running 14장 cil14.txt 줄 169-188(Figure 14-4 터널 캡슐화와 암호화 계층), 277-285(UDP 51871·cilium_wg0) / docs.cilium.io v1.20 security/network/encryption-wireguard/
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
LX, LW, LH, Y0 = 88, 800, 56, 108
d = D(W, H, "CILIUM UP AND RUNNING · 14-01", "VXLAN 터널과 WireGuard 암호화 중첩 패킷",
      "터널 캡슐화 패킷 전체를 WireGuard 가 다시 감싸 노드 사이를 건넌다", "터널 캡슐화 패킷 전체를 WireGuard 가 다시 감싸 노드 사이를 건넌다")

layers = [
    ("14B", "바깥 이더넷", "노드 간 물리·가상 브리지 프레임", False),
    ("20B", "바깥 IPv4", "노드 A IP > 노드 B IP", False),
    ("8B", "바깥 UDP", "51871 > 51871 (cilium_wg0)", False),
    ("16B", "WireGuard 헤더", "수신 인덱스 · 카운터", False),
    ("암호화", "WireGuard 페이로드", "바깥 IP·UDP·VXLAN + 안쪽 이더넷·IP·TCP·데이터", True),
    ("16B", "WireGuard 푸터", "Poly1305 인증 태그 (MAC 무결성 검증)", False),
]

for i, (tag, name, sub, focal) in enumerate(layers):
    y = Y0 + i * LH
    if focal:
        d.tone(LX, y, LW, LH, ACC, r=0, op="14", sw=1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 0.8, r=0)
    cy = y + LH / 2
    d.t(LX + 16, cy + 4, tag, 12, ACC if focal else SOFT, KR if any('가' <= c <= '힣' for c in tag) else MONO, "start")
    d.t(LX + 88, cy + 6, name, 15, ACC if focal else INK, KR, "start", 600)
    sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
    d.t(LX + LW - 16, cy + 5, sub, 12, MUTED, sfam, "end")

# 왼쪽 여백: 바깥 → 안쪽 방향 표시
d.t(44, Y0 + 20, "바깥", 12, MUTED, KR)
d.arrow([(44, Y0 + 36), (44, Y0 + 6 * LH - 36)], MUTED, "ar", 1.4)
d.t(44, Y0 + 6 * LH - 16, "안쪽", 12, MUTED, KR)

LEG_Y = Y0 + 6 * LH + 24
d.legend(LEG_Y, [("노드 간 전송 헤더", SOFT), ("WireGuard 암호화 구간", ACC)])
d.save("14-01.chapter-overview.svg")
