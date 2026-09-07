# 타입 스펙: type-sequence — 접두어 하나가 AS 셋을 건너가며 AS-PATH 가 한 칸씩 길어진다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.4.2 Figure 5.8 · Figure 5.9 의 광고 전파 순서
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 1000, 660
d = Seq(W, H, "SECTION 5.4.2 · ADVERTISING A PREFIX",
        "접두어 하나가 인터넷을 건넙니다",
        "AS3 의 접두어 x 가 AS2 를 거쳐 AS1 까지 전파되는 순서. AS 를 넘을 때는 eBGP 가, AS 안에서는 iBGP 가 나른다.",
        "AS 가 메시지를 보내는 것이 아니라 라우터가 보냅니다")

LX = d.lanes([("3a", "AS3 게이트웨이"), ("2c", "AS2 게이트웨이"),
              ("2a", "AS2 게이트웨이"), ("1c", "AS1 게이트웨이")], y0=110, lane_w=196)
d.rails(486)

d.msg("3a", "2c", "AS3 x", 182, ACC, "acc", sub="eBGP · TCP 179 · AS-PATH 한 칸")
d.selfmsg("2c", "AS2 전체로", 250, INFO, sub="iBGP · 경로 그대로")
d.msg("2c", "2a", "AS3 x", 318, INFO, "info", sub="같은 AS 안이라 경로가 늘지 않습니다")
d.msg("2a", "1c", "AS2 AS3 x", 386, ACC, "acc", sub="eBGP · 자기 ASN 을 앞에 붙입니다")
d.selfmsg("1c", "AS1 전체로", 454, INFO, sub="iBGP")

d.t(30, 528, "AS 를 넘을 때만 AS-PATH 가 길어집니다. iBGP 로 도는 동안에는 경로가 그대로이고,", 11, MUTED, KR, "start")
d.t(30, 548, "그래서 AS-PATH 의 길이는 라우터 홉 수가 아니라 AS 홉 수를 셉니다.", 11, MUTED, KR, "start")
d.t(30, 568, "자기 ASN 이 경로 안에 보이면 그 광고는 버립니다. 이것이 BGP 의 루프 차단 장치입니다.", 11, ACC, KR, "start")

d.legend(592, [("AS 를 넘는 eBGP", ACC), ("AS 안의 iBGP", INFO)])
d.t(960, 640, "KUROSE-ROSS 9E FIG 5.8 · FIG 5.9 · RFC 4271", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.bgp-advertise.svg"
d.save(out)
print("→", out)
