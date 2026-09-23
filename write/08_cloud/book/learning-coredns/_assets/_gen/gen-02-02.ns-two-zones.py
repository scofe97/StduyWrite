# 02-02 §5 — 같은 NS 세트가 부모 존과 자신의 존에 함께 살고, 두 사본이 하는 일이 다르다.
# 원문 근거: "NS records ... usually appear in two zones: the zone they're attached to and its parent zone",
#            부모 쪽은 위임(질의마다 참조로 돌려줌), 자신 쪽은 권한 응답에 실려 재귀 서버가 결국 배워 쓰고,
#            주 서버가 NOTIFY 를, 소프트웨어가 동적 업데이트를 어디로 보낼지 정하는 데 쓴다.
# 2026-09-23 신설: 적대적 검증이 "두 존에 사는 NS 에 도식이 없다"고 지적했다.
# 타입 스펙: type-architecture — 두 존을 나란히 두고, 같은 레코드 사본이 각 존에서 맡는 역할을 잇는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 02-02 §5",
      "같은 NS 가 두 존에 산다",
      "foo.example 의 NS 세트는 부모인 example 존과 자신의 foo.example 존에 한 벌씩 있다. "
      "부모 쪽 사본은 위임을 걸고 참조로 돌아가며, 자신 쪽 사본은 권한 응답에 실려 재귀 서버가 결국 배워 쓰고 "
      "NOTIFY 와 동적 업데이트 목적지를 정한다.",
      "두 사본이 다르면 재귀 서버는 결국 오른쪽을 씁니다")

ZW, ZH, ZY = 360, 272, 108
LX, RX = 24, 496

def zone(x, color, head, role1, role2, role3):
    d.tone(x, ZY, ZW, ZH, color, 8, "0C", 1.3)
    d.t(x + 18, ZY + 26, head, 13, color, MONO, "start", 600)
    # NS 세트 — 두 존에 똑같이 적힌 세 줄
    bx, by = x + 24, ZY + 48
    d.box(bx, by, ZW - 48, 96, PAPER2, RULE, 1.0, 6)
    # SVG 는 연속 공백을 접으므로 NAME 칸과 NS 칸을 따로 찍어 들여쓰기를 보인다
    d.t(bx + 14, by + 26, "foo.example.", 12, INK, MONO, "start")
    for i, t in enumerate(["ns1.foo.example.", "ns2.foo.example.", "ns1.isp.net."]):
        d.t(bx + 124, by + 26 + i * 24, "NS", 12, SOFT, MONO, "start")
        d.t(bx + 152, by + 26 + i * 24, t, 12, INK, MONO, "start")
    d.t(x + ZW / 2, ZY + 178, role1, 14, color, KR, "middle", 600)
    d.t(x + ZW / 2, ZY + 206, role2, 12, MUTED)
    d.t(x + ZW / 2, ZY + 230, role3, 12, MUTED)

zone(LX, INFO, "example 존 · 부모", "위임을 거는 사본", "example 권한 서버가 질의마다", "참조로 돌려줌")
zone(RX, ACC, "foo.example 존 · 자신", "권한 응답에 실리는 사본", "재귀 서버가 결국 배워 쓰는 목록",
     "NOTIFY · 동적 업데이트 목적지")

# 두 사본을 잇는 점선 — 같은 레코드
y = ZY + 96
d.path(f"M {LX + ZW - 24} {y} L {RX + 24} {y}", SOFT, 1.2, dash="4 4")
d.chip((LX + ZW + RX) / 2, y - 22, "같은 NS 세트", MUTED)

d.legend(412, [("부모 쪽 사본", INFO), ("자신 쪽 사본", ACC)])
d.save("02-02.ns-two-zones.svg")
