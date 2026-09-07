# 타입 스펙: type-data-flow — 데이터그램이 NAT 를 지나며 어느 필드가 다시 쓰이는지.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.3.3 Figure 4.25 의 값 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, KR, MONO

W, H = 940, 500
d = D(W, H, "NAT · REWRITE AND RESTORE",
      "나갈 때 출발지를, 들어올 때 목적지를",
      "NAT 라우터가 나가는 데이터그램의 출발지와 들어오는 데이터그램의 목적지를 다시 쓰는 왕복. 가운데 변환 표 한 줄이 두 방향을 이어 준다.",
      "값은 원문 Figure 4.25 그대로입니다")

PW, PH = 290, 52
LX, RX = 24, 626

d.t(169, 104, "집 안", 11, SOFT, KR, "middle", 600)
d.t(470, 104, "NAT 라우터 · 138.76.29.7", 11, SOFT, KR, "middle", 600)
d.t(771, 104, "인터넷 · 128.119.40.186", 11, SOFT, KR, "middle", 600)


def packet(x, y, title, fields, hot=False):
    c = ACC if hot else MUTED
    d.box(x, y, PW, PH, PAPER2, f"{c}66", 1.4 if hot else 0.9, 6)
    d.t(x + 14, y + 21, title, 11, ACC if hot else INK, KR, "start", 600)
    d.t(x + 14, y + 40, fields, 10, MUTED, MONO, "start")


# 나가는 길
packet(LX, 126, "집 안 호스트가 만든 데이터그램",
       "src 10.0.0.1:3345    dst 128.119.40.186:80")
packet(RX, 126, "NAT 이 출발지를 바꿔 적었습니다",
       "src 138.76.29.7:5001  dst 128.119.40.186:80", hot=True)
d.arrow([(LX + PW + 4, 152), (RX - 6, 152)], MUTED, "ar", 1.5)
d.t(388, 142, "나가는 길", 11, MUTED, KR, "end")
d.chip(470, 152, "NAT", MUTED, 11)

# 들어오는 길
packet(RX, 344, "웹 서버가 그대로 되돌려 보냅니다",
       "src 128.119.40.186:80  dst 138.76.29.7:5001")
packet(LX, 344, "NAT 이 목적지를 되돌렸습니다",
       "src 128.119.40.186:80  dst 10.0.0.1:3345", hot=True)
d.arrow([(RX - 6, 370), (LX + PW + 4, 370)], MUTED, "ar", 1.5)
d.t(552, 360, "들어오는 길", 11, MUTED, KR, "end")
d.chip(470, 370, "NAT", MUTED, 11)

# 변환 표
d.box(330, 210, 280, 108, PAPER2, f"{ACC}55", 1.4, 7)
d.t(470, 236, "NAT 변환 표", 12, ACC, KR, "middle", 600)
d.line(470, 250, 470, 310, RULE, 0.8)
d.t(400, 266, "LAN 쪽", 11, MUTED, KR, "middle")
d.t(540, 266, "WAN 쪽", 11, MUTED, KR, "middle")
d.t(400, 288, "10.0.0.1 : 3345", 11, INK, MONO, "middle", 600)
d.t(540, 288, "138.76.29.7 : 5001", 11, ACC, MONO, "middle", 600)
d.t(470, 308, "이 한 줄이 왕복을 이어 줍니다", 11, MUTED, KR, "middle")

# 표가 두 방향의 값을 공급한다
d.path("M 614 288 L 700 288 L 700 186", ACC, 1.2, m="acc", dash="5 4")
d.path("M 326 288 L 250 288 L 250 338", ACC, 1.2, m="acc", dash="5 4")

d.t(24, 418, "웹 서버는 자기가 상대한 것이 집 안의 어느 기기였는지 끝내 알지 못합니다. "
              "새 출발지 포트 5001 이 그 사실을 감춥니다.", 11, MUTED, KR, "start")

d.legend(440, [("NAT 이 다시 쓴 필드", ACC), ("그대로 지나는 필드", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "04-03.nat-translation.svg"
d.save(out)
print("→", out)
