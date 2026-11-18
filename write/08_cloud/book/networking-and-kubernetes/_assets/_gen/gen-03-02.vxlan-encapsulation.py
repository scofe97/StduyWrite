# 03-02.vxlan-encapsulation — 누가 씌우고 누가 벗기는가, 그리고 터널을 건너는 패킷의 층
# 본문 요구: 본문이 "VTEP 는 호스트의 브리지에 붙어 있고 컨테이너들이 그 브리지에 연결됩니다"라고 배치를
#           못 박고, "양쪽 호스트의 VTEP 가 캡슐화·역캡슐화를 수행합니다"라고 주체를 지목한다.
#           2026-09-02 사용자 지적 — "VTEP 이 도식에서 잘 안 보인다".
# 타입 스펙: type-architecture.md — 두 호스트의 부품 배치와 그 사이 연결이 요점이다. 세로 사슬이
#           한 호스트 안의 소속(컨테이너 → 브리지 → VTEP)을 보이고, 가로 터널이 두 VTEP 를 잇는다.
# 근거: RFC 7348 §5(헤더 구성 · 목적지 포트 4789 · VNI 24비트),
#       리눅스 v6.12 include/net/vxlan.h vxlan_headroom()(IP + UDP + VXLAN + Ethernet 헤더 = 50),
#       2026-11-18 재현 — MTU 1500 장치 위 vxlan 장치의 mtu 가 1450.
# 이력: 2026-09-02 재제작(단계 사슬 → 배치도). 2026-11-18 — 패킷 한 개가 A 에서 C 로 가는 길로 화살표
#       방향을 맞추고(호스트 2 는 위로), 「겉봉 4겹 + 원본」 칩 대신 아래에 층과 바이트 수를 펼쳤다.
#       본문 §4 의 층 목록과 MTU 계산이 이 띠로 옮겨 왔다.
# 좌표: Layout conventions 타입이라 공식이 없다. 호스트 폭 380 대칭, 세로 stride 90 하나. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 660
HW, HY, HH = 380, 150, 290
LX, RX = 24, 596
LC, RC = LX + HW // 2, RX + HW // 2        # 214 · 786
CT_Y, BR_Y, VT_Y = 196, 286, 376
CT_W, BR_W = 164, 356

d = D(W, H, "VXLAN · WHO WRAPS AND WHO UNWRAPS",
      "VTEP 가 씌우고 반대편 VTEP 가 벗긴다",
      "컨테이너 A 의 프레임이 브리지와 VTEP 를 거쳐 터널을 건너고 반대편 VTEP 와 브리지를 거쳐 컨테이너 C 에 닿는 길. "
      "아래 띠는 터널 구간의 패킷 층이며, 바깥 IP 패킷 1500 바이트 가운데 50 바이트를 헤더가 써서 안쪽 IP 패킷은 1450 이다.",
      lead="컨테이너 A 의 프레임이 컨테이너 C 에 닿는 길입니다 · 모양이 바뀌는 구간은 터널 하나뿐입니다")


def host(x, label, sub):
    d.o.append(f'<rect x="{x}" y="{HY}" width="{HW}" height="{HH}" rx="10" '
               f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    d.t(x + 16, HY - 14, label, 12, INFO, KR, "start", 600)
    d.t(x + HW - 16, HY - 14, sub, 11, SOFT, MONO, "end")


def box(cx, cy, w, h, t, sub, c=None, focal=False, dim=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    elif dim:
        d.box(x, y, w, h, PAPER, RULE, 0.9, 6)
        tc = SOFT
    else:
        d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6)
        tc = c or INK
    d.t(cx, cy - 4, ddx.fit(t, 12, w - 16, t), 12, tc,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 15, ddx.fit(sub, 11, w - 14, sub), 11, SOFT if dim else MUTED, KR)


# 호스트 1 — 보내는 쪽. 프레임이 아래로 내려간다
host(LX, "호스트 1", "192.168.1.20")
box(LX + 102, CT_Y, CT_W, 48, "컨테이너 A", "보내는 쪽", OK)
box(LX + 294, CT_Y, CT_W, 48, "컨테이너 B", "같은 브리지", dim=True)
box(LC, BR_Y, BR_W, 48, "브리지", "원본 프레임 그대로 넘김", INFO)
box(LC, VT_Y, BR_W, 52, "VTEP", "바깥 헤더를 씌움", focal=True)
d.path(f"M {LX+102} {CT_Y+24} L {LX+102} {BR_Y-24-6}", MUTED, 1.4, m="ar")
d.path(f"M {LC} {BR_Y+24} L {LC} {VT_Y-26-6}", MUTED, 1.4, m="ar")

# 호스트 2 — 받는 쪽. 프레임이 위로 올라간다
host(RX, "호스트 2", "192.168.1.23")
box(RX + 102, CT_Y, CT_W, 48, "컨테이너 C", "받는 쪽", OK)
box(RX + 294, CT_Y, CT_W, 48, "컨테이너 D", "같은 브리지", dim=True)
box(RC, BR_Y, BR_W, 48, "브리지", "원본 프레임 그대로 넘김", INFO)
box(RC, VT_Y, BR_W, 52, "VTEP", "바깥 헤더를 벗김", focal=True)
d.path(f"M {RC} {VT_Y-26} L {RC} {BR_Y+24+6}", MUTED, 1.4, m="ar")
d.path(f"M {RX+102} {BR_Y-24} L {RX+102} {CT_Y+24+6}", MUTED, 1.4, m="ar")

# 터널 — 모양이 바뀌는 유일한 구간
d.path(f"M {LC+BR_W//2+8} {VT_Y} L {RC-BR_W//2-10} {VT_Y}", ACC, 1.8, m="acc")
d.t(500, VT_Y - 12, "UDP 4789", 12, ACC, MONO, "middle", 600)
d.t(500, VT_Y + 22, "물리망은 바깥 헤더만 읽음", 11, MUTED, KR)

# 터널을 건너는 패킷 — 바깥에서 안쪽으로
SY, SH = 496, 60
d.t(24, SY - 16, "터널을 건너는 패킷 — 왼쪽이 바깥", 12, SOFT, KR, "start", 600)
CELLS = [(128, "바깥 Ethernet", "14 · 다음 홉 MAC", ACC),
         (172, "바깥 IP", "20 · VTEP 주소", ACC),
         (152, "UDP", "8 · 목적지 4789", ACC),
         (152, "VXLAN", "8 · VNI 24비트", ACC),
         (140, "안쪽 Ethernet", "14 · 컨테이너 MAC", OK),
         (168, "안쪽 IP 패킷", "1450 까지", OK)]
x = 24
XS = []
for w, t, sub, c in CELLS:
    d.o.append(f'<rect x="{x}" y="{SY}" width="{w}" height="{SH}" rx="6" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
    d.t(x + w // 2, SY + 25, ddx.fit(t, 12, w - 14, t), 12, c,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(x + w // 2, SY + 45, ddx.fit(sub, 11, w - 12, sub), 11, MUTED, KR)
    XS.append((x, w))
    x += w + 8
# 바깥 IP 부터 안쪽 Ethernet 까지 네 칸이 MTU 를 깎는다
bx0, bx1 = XS[1][0], XS[4][0] + XS[4][1]
d.path(f"M {bx0} {SY+SH+8} L {bx0} {SY+SH+16} L {bx1} {SY+SH+16} L {bx1} {SY+SH+8}", MUTED, 1.2)
d.t((bx0 + bx1) // 2, SY + SH + 34, "20 + 8 + 8 + 14 = 50 바이트 · 1500 에서 빼면 1450", 12, MUTED, KR)

d.legend(H - 48, [("VTEP 와 바깥 헤더", ACC), ("컨테이너와 원본 프레임", OK),
                  ("호스트 경계와 브리지", INFO)])
d.save("03-02.vxlan-encapsulation.svg")
print("ok vxlan-encapsulation")
