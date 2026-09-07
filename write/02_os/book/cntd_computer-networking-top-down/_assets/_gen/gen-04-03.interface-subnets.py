# 타입 스펙: type-nested — 담기는 관계. 서브넷이 인터페이스를 담는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.3.2 Figure 4.20 의 주소 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, KR, MONO

W, H = 940, 570
d = D(W, H, "FIGURE 4.20 · SIX SUBNETS",
      "라우터 한 대가 세 섬에 있습니다",
      "원문 Figure 4.20 의 여섯 서브넷을 담는 상자로 그린 그림. R1 의 인터페이스 셋이 서로 다른 세 서브넷에 각각 들어가 있어, 주소가 장비가 아니라 인터페이스에 결부된다는 것을 보인다.",
      "인터페이스를 장비에서 떼어 내면 남는 고립망 하나가 곧 서브넷입니다")

BW, BH = 280, 160
COLS = [40, 340, 640]
ROWS = [112, 288]


def subnet(x, y, title, sub, items):
    d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, title, 13, INK, MONO, "start", 600)
    d.t(x + 16, y + 45, sub, 11, MUTED, KR, "start")
    d.line(x + 14, y + 58, x + BW - 14, y + 58, RULE, 0.8)
    iy = y + 68
    for addr, owner, mark in items:
        c = {"r1": ACC, "bad": BAD, "": MUTED}[mark]
        d.box(x + 16, iy, BW - 32, 26, PAPER, f"{c}66", 1.3 if mark else 0.9, 5)
        d.t(x + 28, iy + 18, addr, 12, c if mark else INK, MONO, "start", 600)
        d.t(x + BW - 28, iy + 18, owner, 11, c, KR, "end")
        iy += 30


subnet(COLS[0], ROWS[0], "223.1.1.0/24", "R1 과 호스트 둘", [
    ("223.1.1.1", "호스트", ""), ("223.1.1.4", "호스트", ""), ("223.1.1.3", "R1", "r1")])
subnet(COLS[1], ROWS[0], "223.1.9.0/24", "R1 과 R2 를 잇는 링크", [
    ("223.1.9.2", "R1", "r1"), ("223.1.9.1", "R2", "")])
subnet(COLS[2], ROWS[0], "223.1.7.0/24", "R3 과 R1 을 잇는 링크", [
    ("223.1.7.1", "R3", ""), ("223.1.7.0", "R1 · 호스트 자리가 0", "bad")])
subnet(COLS[0], ROWS[1], "223.1.2.0/24", "R2 와 호스트 둘", [
    ("223.1.2.1", "호스트", ""), ("223.1.2.2", "호스트", ""), ("223.1.2.6", "R2", "")])
subnet(COLS[1], ROWS[1], "223.1.8.0/24", "R2 와 R3 을 잇는 링크", [
    ("223.1.8.1", "R2", ""), ("223.1.8.0", "R3 · 호스트 자리가 0", "bad")])
subnet(COLS[2], ROWS[1], "223.1.3.0/24", "R3 과 호스트 둘", [
    ("223.1.3.1", "호스트", ""), ("223.1.3.2", "호스트", ""), ("223.1.3.27", "R3", "")])

d.t(40, 478, "R1 은 세 상자에 있습니다. 223.1.1.3, 223.1.9.2, 그리고 붉게 표시한 223.1.7.0 입니다. 겹친 장비가 아니라 서로 다른 인터페이스입니다.",
     11, MUTED, KR, "start")

d.legend(500, [("R1 의 인터페이스", ACC), ("RFC 1812 가 금지하는 주소", BAD), ("그 밖의 인터페이스", MUTED)])
d.t(900, 522, "KUROSE-ROSS 9E FIG 4.20", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-03.interface-subnets.svg"
d.save(out)
print("→", out)
