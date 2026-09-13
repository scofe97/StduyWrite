# 타입 스펙: type-nested — 인터넷 안에 AS 가 있고 AS 안에 라우터가 있다. 경계마다 다른 프로토콜이 산다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.3 도입 (규모·관리 자율성) + §5.4.2 게이트웨이/내부 라우터
# 짝: gen-05-02.flat-routing-problems.py 가 같은 라우터 배치에서 경계가 없을 때 무너지는 두 자리를 그린다.
#     아래 두 칸은 그 그림의 두 칸과 줄 단위로 대응한다 — 한쪽 줄을 바꾸면 다른 쪽도 바꾼다.
# 주의: 원문 Figure 5.8 은 AS 에 구체적 ASN 값을 주지 않는다. 앞서 넣었던 65001~65003 은 책에도 RFC 1930 에도
#       없는 값(RFC 6996 사설 대역)이라 걷어냈다. 도식 서명이 FIG 5.8 이므로 그림 밖 수치를 실으면 안 된다.
#       AS 마다 내부 프로토콜 이름을 적지 않는 것도 같은 이유다 — 원문 그림은 그것을 정하지 않는다.
# 해결 칸의 "너무 커지면 둘로 쪼갭니다" 는 원문 §5.4.5 (노트 6절) 의 서술이다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 640
d = D(W, H, "SECTION 5.3 · AUTONOMOUS SYSTEMS",
      "AS 경계를 그으면 두 문제가 풀립니다",
      "위 그림과 같은 라우터를 자율 시스템으로 묶은 뒤의 구조. 같은 AS 안은 그 AS 가 고른 라우팅 프로토콜이, AS 사이는 BGP 가 맡는다. 아래 두 칸이 규모와 관리 자율성 문제가 풀리는 방식이다.",
      "위 그림과 같은 라우터를 자율 시스템으로 묶었습니다. 아래 두 칸은 위 그림의 두 칸에 한 줄씩 대응합니다.")

d.box(20, 116, 960, 300, f"{INK}04", RULE, 1.0, 12)
d.t(36, 144, "인터넷 — AS 사이는 모두가 BGP 하나로 맞춥니다", 12, INK, KR, "start", 600)

AS = [(48, 164, 280, "AS1"), (360, 164, 280, "AS2"), (672, 164, 280, "AS3")]
for x, y, w, name in AS:
    d.box(x, y, w, 232, f"{INK}07", f"{MUTED}88", 1.2, 10)
    d.t(x + 16, y + 26, name, 13, INK, MONO, "start", 600)
    d.t(x + w - 16, y + 26, "고유 ASN", 12, SOFT, KR, "end")   # 한글 섞인 라벨은 MONO 가 자간을 벌린다
    d.t(x + w / 2, y + 52, "안의 알고리즘은 이 AS 가 고릅니다", 12, MUTED, KR)


# 라우터 — 게이트웨이는 경계에, 내부는 안쪽에
def router(x, y, name, gw):
    c = ACC if gw else MUTED
    d.box(x, y, 76, 44, PAPER2, c, 1.4 if gw else 1.0, 6)
    d.t(x + 38, y + 19, name, 12, INK, MONO, "middle", 600)
    d.t(x + 38, y + 36, "게이트웨이" if gw else "내부", 12, c, KR)


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
d.t(344, 410, "eBGP", 12, INFO, MONO)
d.t(656, 410, "eBGP", 12, INFO, MONO)

# 풀린 두 자리 — flat-routing-problems 의 두 칸과 같은 자리, 같은 줄 순서
CARDS = [
    (20, "규모", "계산은 경계 안쪽에서만 합니다",
     ["밖의 목적지는 BGP 가 나르는 접두어로만 압니다",
      "내부 라우팅 정보는 자기 AS 안에서만 오갑니다",
      "AS 가 너무 커지면 둘로 쪼갭니다"]),
    (516, "관리 자율성", "경계 안쪽은 그 AS 의 몫입니다",
     ["AS 안은 한 관리 주체가 자기 뜻대로 운영합니다",
      "안에서 쓸 알고리즘은 그 AS 가 고릅니다",
      "밖에 알리는 것은 내부 구조가 아니라 접두어입니다"]),
]
for x, head, sub, lines in CARDS:
    d.tone(x, 440, 464, 128, OK, r=8, op="10", sw=1.2)
    d.t(x + 20, 468, head, 14, OK, KR, "start", 600)
    d.t(x + 20 + (28 if len(head) == 2 else 80) + 16, 468, sub, 12, MUTED, KR, "start")
    for i, ln in enumerate(lines):
        y = 496 + 24 * i
        d.box(x + 20, y - 8, 4, 4, OK, OK, 0, 1)
        d.t(x + 32, y, ln, 13, INK, KR, "start")

d.legend(592, [("게이트웨이 라우터", ACC), ("AS 를 넘는 연결", INFO), ("내부 라우터", MUTED), ("풀린 자리", OK)])
d.t(960, 614, "KUROSE-ROSS 9E FIG 5.8 · RFC 1930", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.as-nesting.svg"
d.save(out)
print("→", out)
