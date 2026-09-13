# 타입 스펙: type-architecture — AS 셋(영역 셋)과 라우터 위로 광고가 번호 순서대로 건너간다. AS-PATH 는 경계를 넘을 때만 길어진다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.4.2 Figure 5.8 · Figure 5.9 의 광고 전파 순서
# 2026-09-13: type-sequence 에서 바꿨다. 시퀀스는 게이트웨이 넷의 시간 순서만 보여 망 모양과
#             "AS 안 모든 라우터에게 퍼진다"는 iBGP 의 범위가 안 보였다(사용자 지적).
# 라우터 배치는 원문 Figure 5.8 의 상대 위치를 따른다. iBGP 는 물리 링크가 아니라 TCP 연결이라 점선으로 그린다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, ACC, INFO, KR, MONO

W, H = 1000, 548
d = D(W, H, "SECTION 5.4.2 · ADVERTISING A PREFIX",
      "접두어 x 가 AS 셋을 건너는 길",
      "AS3 의 접두어 x 가 AS2 를 거쳐 AS1 의 모든 라우터에게 알려지는 네 단계. 1·3단계는 eBGP 로 경계를 넘으며 보낸 쪽 ASN 이 붙고, 2·4단계는 iBGP 로 AS 안에 퍼지며 경로가 그대로다.",
      "광고는 AS 가 아니라 라우터가 보냅니다. 번호 순서대로 따라가면 AS-PATH 가 어디서 길어지는지 보입니다.")

Y0, BH = 108, 320
AS = [(24, "AS1", "받은 경로", "AS2 AS3 x", ACC),
      (356, "AS2", "받은 경로", "AS3 x", INFO),
      (688, "AS3", "접두어 x 의 주인", "x", MUTED)]
for x, name, lab, val, c in AS:
    d.box(x, Y0, 288, BH, f"{INK}07", f"{MUTED}88", 1.2, 10)
    d.t(x + 16, Y0 + 28, name, 13, INK, MONO, "start", 600)
    focal = c == ACC
    d.tone(x + 16, 156, 256, 32, c, r=6, op="12" if focal else "0C", sw=1.4 if focal else 1.0)
    d.t(x + 28, 177, lab, 12, MUTED, KR, "start")
    d.t(x + 260, 177, val, 14, c if c != MUTED else INK, MONO, "end", 600)


def router(x, y, name, gw):
    c = INFO if gw else MUTED
    d.box(x, y, 76, 44, PAPER2, c, 1.4 if gw else 1.0, 6)
    d.t(x + 38, y + 19, name, 12, INK, MONO, "middle", 600)
    d.t(x + 38, y + 36, "게이트웨이" if gw else "내부", 12, c, KR)


def badge(cx, cy, n, c):
    d.box(cx - 10, cy - 10, 20, 20, PAPER, c, 1.2, 4)
    d.t(cx, cy + 5, str(n), 12, c, MONO, "middle", 600)


# iBGP 를 먼저 그려 라우터 상자가 선 끝을 덮게 한다
IB = dict(c=MUTED, sw=1.2, dash="4 3")
# 2단계 — 2c 가 AS2 안의 다른 라우터 전부에게
d.path("M 540 350 L 460 350", m="ar", **IB)
d.path("M 582 324 L 582 300 L 418 300", **IB)
d.path("M 514 300 L 514 280", m="ar", **IB)
d.path("M 418 300 L 418 280", m="ar", **IB)
# 4단계 — 1c 가 AS1 안의 다른 라우터 전부에게
d.path("M 208 350 L 128 350", m="ar", **IB)
d.path("M 250 324 L 250 300 L 86 300", **IB)
d.path("M 182 300 L 182 280", m="ar", **IB)
d.path("M 86 300 L 86 280", m="ar", **IB)

# eBGP — 경계를 넘는 두 단계, 오른쪽에서 왼쪽으로
d.path("M 708 350 L 624 350", INFO, 1.8, m="info")   # 1단계 3a → 2c
d.path("M 376 350 L 292 350", ACC, 1.8, m="acc")     # 3단계 2a → 1c, 여기서 AS2 가 붙는다

for x, y, name, gw in ((48, 232, "1a", False), (144, 232, "1b", False), (48, 328, "1d", False), (212, 328, "1c", True),
                       (380, 232, "2b", False), (476, 232, "2d", False), (380, 328, "2a", True), (544, 328, "2c", True),
                       (712, 232, "3b", False), (808, 232, "3c", False), (712, 328, "3a", True), (876, 328, "3d", False)):
    router(x, y, name, gw)

d.path("M 914 372 L 914 388", MUTED, 1.2)
d.chip(914, 400, "접두어 x", MUTED, 11, 6)

badge(666, 328, 1, INFO)
badge(606, 300, 2, MUTED)
badge(334, 328, 3, ACC)
badge(274, 300, 4, MUTED)

d.t(24, 456, "경계를 넘는 1·3단계(eBGP)에서만 보낸 쪽이 자기 ASN 을 경로 앞에 붙입니다.", 13, INK, KR, "start")
d.t(24, 480, "AS 안에 퍼지는 2·4단계(iBGP)에서는 경로가 그대로라, AS-PATH 의 길이는 라우터 홉이 아니라 AS 홉을 셉니다.", 13, MUTED, KR, "start")

d.legend(500, [("eBGP · 경계를 넘는 광고", INFO), ("iBGP · 물리 링크가 아닌 TCP 연결", MUTED), ("경로가 길어진 자리", ACC)])
d.t(960, 540, "KUROSE-ROSS 9E FIG 5.8 · FIG 5.9 · RFC 4271", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.bgp-advertise.svg"
d.save(out)
print("→", out)
