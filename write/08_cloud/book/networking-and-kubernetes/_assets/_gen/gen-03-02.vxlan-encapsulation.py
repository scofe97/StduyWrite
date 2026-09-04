# 03-02.vxlan-encapsulation — 누가 씌우고 누가 벗기는가
# 본문 요구: 본문이 "VTEP 는 호스트의 브리지 인터페이스에 붙어 있고 컨테이너들이 그 브리지에
#           연결됩니다"라고 배치를 못 박고, "양쪽 호스트의 VTEP 가 캡슐화·역캡슐화를 수행합니다"
#           라고 주체를 지목한다. 옛 판은 단계 사슬이라 그 배치와 주체가 머리글로만 있었다.
#           2026-09-02 사용자 지적 — "VTEP 이 도식에서 잘 안 보인다".
# 타입 스펙: type-architecture.md — 두 호스트의 부품 배치와 그 사이 연결이 요점이다. 세로 사슬이
#           한 호스트 안의 소속(컨테이너 → 브리지 → VTEP)을 보이고, 가로 터널이 두 VTEP 를 잇는다.
#           패킷 모양은 칩으로 간선에 얹어 "어느 구간에서 모양이 바뀌는가"를 같은 그림에 담는다.
# 좌표: Layout conventions 타입이라 공식이 없다. 호스트 폭 396 대칭, 세로 stride 90 하나. 전부 4의 배수.
# 이력: 2026-09-02 재제작. 옛 판은 단계 사슬(원문자 머리글 ①~④)이었고 원문자는 이 저장소 금지 표기다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 600
HW, HY, HH = 396, 150, 290
LX, RX = 24, 580
LC, RC = LX + HW // 2, RX + HW // 2        # 222 · 778
CT_Y, BR_Y, VT_Y = 196, 286, 376
CT_W, BR_W = 164, 356

d = D(W, H, "VXLAN · WHO WRAPS AND WHO UNWRAPS",
      "VTEP 가 씌우고 반대편 VTEP 가 벗긴다",
      "두 호스트의 부품 배치와 그 사이 터널. 컨테이너는 브리지에 매달리고 브리지는 VTEP 에 붙으며, "
      "겉봉이 붙는 구간은 두 VTEP 사이뿐이다. 물리망은 그 겉봉만 읽는다.",
      lead="컨테이너 → 브리지 → VTEP 순으로 매달립니다 · 모양이 바뀌는 구간은 터널 하나뿐입니다")


def host(x, label, sub):
    d.o.append(f'<rect x="{x}" y="{HY}" width="{HW}" height="{HH}" rx="10" '
               f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    d.t(x + 16, HY - 14, label, 12, INFO, KR, "start", 600)
    d.t(x + HW - 16, HY - 14, sub, 11, SOFT, MONO, "end")


def box(cx, cy, w, h, t, sub, c=None, focal=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6)
        tc = c or INK
    d.t(cx, cy - 4, ddx.fit(t, 12, w - 16, t), 12, tc,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 15, ddx.fit(sub, 11, w - 14, sub), 11, MUTED, KR)


for x, lab, sub, c1, c2 in ((LX, "호스트 1", "192.168.1.20", "컨테이너 A", "컨테이너 B"),
                            (RX, "호스트 2", "192.168.1.23", "컨테이너 C", "컨테이너 D")):
    c = x + HW // 2
    host(x, lab, sub)
    box(x + 102, CT_Y, CT_W, 48, c1, "자기 netns", OK)
    box(x + 294, CT_Y, CT_W, 48, c2, "자기 netns", OK)
    box(c, BR_Y, BR_W, 48, "브리지", "컨테이너들이 여기 매달린다", INFO)
    box(c, VT_Y, BR_W, 52, "VTEP", "겉봉을 씌우고 벗긴다", focal=True)
    for cx in (x + 102, x + 294):
        d.path(f"M {cx} {CT_Y+24} L {cx} {BR_Y-24-6}", MUTED, 1.4, m="ar")
    d.path(f"M {c} {BR_Y+24} L {c} {VT_Y-26-6}", MUTED, 1.4, m="ar")
    d.t(c, BR_Y - 34, "원본 프레임 그대로", 11, MUTED, KR)

# 터널 — 모양이 바뀌는 유일한 구간
d.path(f"M {LC+BR_W//2+8} {VT_Y} L {RC-BR_W//2-10} {VT_Y}", ACC, 1.8, m="acc")
d.path(f"M {RC-BR_W//2-8} {VT_Y+16} L {LC+BR_W//2+10} {VT_Y+16}", ACC, 1.4, m="acc", dash="5 5")
# 칩은 두 VTEP 상자 사이 빈 통로에만 둔다 — 상자 폭(…400 / 600…) 밖으로 176px 을 잡는다
ddx.focal_tag(d, 500, VT_Y - 52, "겉봉 4겹 + 원본", 176)
d.t(500, VT_Y + 40, "물리망은 겉봉만 읽는다", 11, MUTED, KR)

d.t(24, 484, "겉봉이 붙어 있는 구간은 두 VTEP 사이뿐입니다. 컨테이너도 브리지도 원본 프레임만 보므로 "
             "오버레이가 있다는 사실조차 모릅니다.", 12, MUTED, KR, "start")
d.t(24, 508, "겉봉은 약 50바이트라 안쪽에 쓸 수 있는 MTU 가 그만큼 줄어듭니다. 이 값을 안 맞추면 "
             "큰 패킷만 조용히 사라집니다.", 12, WARN, KR, "start")
d.legend(532, [("겉봉을 다루는 주체", ACC), ("컨테이너 · 자기 netns", OK),
               ("호스트 경계와 브리지", INFO), ("MTU 주의", WARN)])
d.save("03-02.vxlan-encapsulation.svg")
print("ok vxlan-encapsulation")
