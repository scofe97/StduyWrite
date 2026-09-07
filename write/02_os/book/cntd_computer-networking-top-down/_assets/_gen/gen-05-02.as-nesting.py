# 타입 스펙: type-nested — 인터넷 안에 AS 가 있고 AS 안에 라우터가 있다. 경계마다 다른 프로토콜이 산다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.3 도입 (규모·관리 자율성) + §5.4.2 게이트웨이/내부 라우터
# 주의: 원문 Figure 5.8 은 AS 에 구체적 ASN 값을 주지 않는다. 앞서 넣었던 65001~65003 은 책에도 RFC 1930 에도
#       없는 값(RFC 6996 사설 대역)이라 걷어냈다. 도식 서명이 FIG 5.8 이므로 그림 밖 수치를 실으면 안 된다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 1000, 620
d = D(W, H, "SECTION 5.3 · AUTONOMOUS SYSTEMS",
      "경계를 그으니 문제가 둘 다 풀립니다",
      "라우터를 자율 시스템으로 묶은 뒤의 구조. 같은 AS 안은 하나의 라우팅 프로토콜이 지배하고, AS 를 넘는 순간 다른 프로토콜이 맡는다.",
      "규모 문제와 관리 자율성 문제가 같은 경계 하나로 해결됩니다")

d.box(20, 116, 960, 300, f"{INK}04", RULE, 1.0, 12)
d.t(36, 140, "인터넷 — AS 사이는 BGP 하나뿐입니다", 12, INK, KR, "start", 600)

AS = [(48, 164, 280, "AS1", "고유 ASN"), (360, 164, 280, "AS2", "고유 ASN"),
      (672, 164, 280, "AS3", "고유 ASN")]
for x, y, w, name, asn in AS:
    d.box(x, y, w, 232, f"{INK}07", f"{MUTED}88", 1.2, 10)
    d.t(x + 16, y + 26, name, 13, INK, MONO, "start", 600)
    d.t(x + w - 16, y + 26, asn, 11, SOFT, KR, "end")   # 한글 섞인 라벨은 MONO 가 자간을 벌린다
    d.t(x + w / 2, y + 50, "안에서는 OSPF", 11, ACC, KR)

# 라우터 — 게이트웨이는 경계에, 내부는 안쪽에
def router(x, y, name, gw):
    c = ACC if gw else MUTED
    d.box(x, y, 76, 44, PAPER2, c, 1.4 if gw else 1.0, 6)
    d.t(x + 38, y + 20, name, 11, INK, MONO, "middle", 600)
    d.t(x + 38, y + 36, "게이트웨이" if gw else "내부", 11, c, KR)


router(72, 248, "1a", False); router(168, 248, "1b", False)
router(72, 316, "1d", False); router(240, 316, "1c", True)
router(384, 248, "2b", False); router(480, 248, "2d", False)
router(384, 316, "2a", True); router(552, 316, "2c", True)
router(696, 248, "3b", False); router(792, 248, "3c", False)
router(696, 316, "3a", True); router(864, 316, "3d", False)

# Figure 5.8 에서 접두어 x 는 3d 에 붙어 있다. 3d 는 게이트웨이가 아니다
d.path("M 902 360 L 902 370", ACC, 1.2)
d.chip(902, 382, "접두어 x", ACC, 11, 6)

# eBGP — AS 를 넘는 연결
for p in ("M 320 338 L 380 338", "M 632 338 L 692 338"):
    d.path(p, INFO, 1.8, m="info")
d.t(350, 372, "eBGP", 11, INFO, KR)
d.t(662, 372, "eBGP", 11, INFO, KR)

d.t(500, 446, "같은 AS 안의 라우터는 같은 라우팅 알고리즘을 돌리고 서로의 정보를 갖습니다.", 11, MUTED, KR)
d.t(500, 466, "AS 를 넘는 순간 필요한 것은 최단 경로가 아니라 합의된 하나의 프로토콜입니다.", 11, MUTED, KR)

d.t(30, 508, "라우터를 무리로 묶는 이유는 둘입니다. 수억 개 라우터의 도달 정보를 저장하고 전파하는 비용이 감당되지 않고,", 11, MUTED, KR, "start")
d.t(30, 528, "ISP 마다 자기 망을 자기 뜻대로 운영하고 내부를 숨기고 싶어 합니다. 경계 하나가 둘을 함께 해결합니다.", 11, MUTED, KR, "start")

d.legend(552, [("게이트웨이 라우터", ACC), ("AS 를 넘는 연결", INFO), ("내부 라우터", MUTED)])
d.t(960, 600, "KUROSE-ROSS 9E FIG 5.8 · RFC 1930", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.as-nesting.svg"
d.save(out)
print("→", out)
