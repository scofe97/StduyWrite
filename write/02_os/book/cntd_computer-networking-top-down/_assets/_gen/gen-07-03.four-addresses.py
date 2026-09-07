# 타입 스펙: type-data-flow — 단계마다 누가 무엇을 하는지. 프레임이 AP 를 지나며 형식과 주소가 바뀐다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.2 Figure 7.26 · Figure 7.27 —
#   주소 1·2·3 의 정의와 R1·H1 예시는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 580
d = D(W, H, "SECTION 7.3.2 · 802.11 ADDRESS FIELDS",
      "주소가 셋이어야 라우터의 MAC 주소가 살아 건너갑니다",
      "AP 는 3 계층을 모르는 링크 계층 장치다. 그래서 프레임 자체가 라우터 인터페이스의 주소를 들고 다녀야 한다.",
      "주소 정의와 예시는 원문 Figure 7.27 의 것입니다")

NODES = [(100, "라우터 인터페이스 R1", "IP 를 압니다"),
         (470, "AP", "링크 계층만 압니다"),
         (840, "무선 기기 H1", "IP 를 압니다")]
for x, name, sub in NODES:
    d.tone(x - 84, 100, 168, 54, INFO, 6, "12", 1.2)
    d.t(x, 122, name, 11, INFO, KR, "middle", 600)
    d.t(x, 142, sub, 10, MUTED, KR)

FW, FH = 264, 104
ROWS = [
    (176, "R1 에서 H1 로", ACC,
     [(285, "이더넷 프레임", [("출발지", "R1 의 MAC"), ("목적지", "H1 의 MAC")]),
      (655, "802.11 프레임", [("주소 1", "H1 의 MAC"), ("주소 2", "AP 의 MAC"), ("주소 3", "R1 의 MAC")])],
     [(184, 386, 1)]),
    (312, "H1 에서 R1 로", OK,
     [(285, "이더넷 프레임", [("출발지", "H1 의 MAC"), ("목적지", "R1 의 MAC")]),
      (655, "802.11 프레임", [("주소 1", "AP 의 MAC"), ("주소 2", "H1 의 MAC"), ("주소 3", "R1 의 MAC")])],
     [(756, 554, -1)]),
]
for ry, label, c, cards, _ in ROWS:
    d.t(24, ry + FH / 2, label, 11, c, KR, "start", 600)
    for cx, title, fields in cards:
        d.box(cx - FW / 2, ry, FW, FH, PAPER2, RULE, 1.0)
        d.t(cx, ry + 24, title, 11, c, KR, "middle", 600)
        d.line(cx - FW / 2 + 16, ry + 34, cx + FW / 2 - 16, ry + 34, RULE, 0.8)
        for j, (k, v) in enumerate(fields):
            y = ry + 56 + j * 20
            d.t(cx - FW / 2 + 20, y, k, 10, SOFT, KR, "start")
            d.t(cx + FW / 2 - 20, y, v, 11, INK if k == "주소 3" else MUTED, MONO, "end",
                600 if k == "주소 3" else 400)

d.arrow([(285, 168), (655, 168)], ACC, "acc", 1.4)
d.t(470, 160, "AP 가 802.11 로 바꿉니다", 10, ACC, KR)
d.arrow([(655, 304), (285, 304)], OK, "ok", 1.4)
d.t(470, 296, "AP 가 이더넷으로 바꿉니다", 10, OK, KR)

PY = 440
d.box(24, PY, 880, 80, PAPER2, RULE, 1.0)
d.t(44, PY + 24, "주소 3 이 하는 일", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "내려갈 때 — H1 은 주소 3 을 보고 이 데이터그램을 서브넷에 넣은 라우터 인터페이스를 압니다.",
    "올라갈 때 — AP 는 주소 3 을 보고 이더넷 프레임의 목적지 MAC 을 채웁니다. 네 번째 주소는 애드혹용입니다.",
]):
    d.t(44, PY + 48 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(536, [("R1 에서 H1 로", ACC), ("H1 에서 R1 로", OK), ("장치", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-03.four-addresses.svg"
d.save(out)
print("→", out)
