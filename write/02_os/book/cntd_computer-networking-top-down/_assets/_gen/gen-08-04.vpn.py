# 타입 스펙: type-deployment — 무엇이 어디에 놓이고 어느 구간에서 암호화되는가.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.7.1 Figure 8.27 (책 599쪽) —
#   본사·지사·출장 영업 사원 구성과 "공용 인터넷을 지날 때만 암호화" 는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO

W, H = 1000, 588
d = D(W, H, "SECTION 8.7.1 · VIRTUAL PRIVATE NETWORK",
      "사설망을 사지 않고 공용 인터넷 위에 만듭니다",
      "같은 기관 안에서는 평범한 IPv4 로 오간다. 공용 인터넷을 지나는 구간에서만 IPsec 으로 바꾼다.",
      "구성과 암호화 구간은 원문 Figure 8.27 의 것입니다")

SITES = [(24, 148, 264, 132, "본사", "게이트웨이 라우터", INFO),
         (368, 148, 264, 132, "공용 인터넷", "평범한 라우터들", MUTED),
         (712, 148, 264, 132, "지사", "게이트웨이 라우터", INFO)]
for x, y, w, h, name, sub, c in SITES:
    d.tone(x, y, w, h, c, 8, "12", 1.2)
    d.t(x + w / 2, y + 42, name, 13, c, KR, "middle", 600)
    d.t(x + w / 2, y + 66, sub, 11, MUTED, KR)
    if name != "공용 인터넷":
        d.t(x + w / 2, y + 100, "안에서는 평범한 IPv4", 11, OK, KR)
    else:
        d.t(x + w / 2, y + 100, "IPsec 인 줄 모르고 전달합니다", 11, SOFT, KR)

d.tone(368, 320, 264, 96, ACC, 8, "18", 1.4)
d.t(500, 352, "출장 영업 사원", 12, ACC, KR, "middle", 600)
d.t(500, 376, "호텔에서 접속합니다", 11, MUTED, KR)
d.t(500, 398, "노트북 OS 가 복호합니다", 11, MUTED, KR)

for a, b, lab in ((288, 364, "IPsec"), (636, 708, "IPsec")):
    d.arrow([(a + 4, 214), (b - 4, 214)], ACC, "acc", 1.6)
    d.t((a + b) / 2, 200, lab, 11, ACC, MONO, "middle", 600)
d.path("M 300 240 L 336 240 L 336 340 L 364 340", ACC, 1.5, m="acc")
d.t(316, 300, "IPsec", 11, ACC, MONO, "middle", 600)

PY = 448
d.box(24, PY, 952, 76, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "게이트웨이가 하는 일", 12, INK, KR, "start", 600)
d.t(44, PY + 56, "평범한 IPv4 데이터그램을 IPsec 데이터그램으로 바꿔 인터넷에 내보냅니다. 바깥 헤더는 진짜 IPv4 라 중간 라우터는 평범한 데이터그램으로 처리합니다.",
    11, MUTED, KR, "start")

d.legend(544, [("기관 내부", INFO), ("암호화 없이", OK), ("암호화 구간", ACC), ("공용 구간", MUTED)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-04.vpn.svg"
d.save(out); print("→", out.name)
