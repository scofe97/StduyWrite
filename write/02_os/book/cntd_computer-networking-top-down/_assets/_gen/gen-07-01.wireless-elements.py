# 타입 스펙: type-architecture — 시스템의 구성요소와 연결. 무선망을 이루는 넷과 그 사이 링크.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.1 Figure 7.1 —
#   구성요소 넷의 이름과 셀룰러·WiFi 용어 대조는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 940, 540
d = D(W, H, "SECTION 7.1 · ELEMENTS OF A WIRELESS NETWORK",
      "무선망을 이루는 넷, 그리고 WiFi 에 없는 하나",
      "무선 기기와 기지국과 코어망과 바깥 인터넷이 한 줄로 이어진다. 셀룰러에는 코어망이 있고 WiFi 에는 없다.",
      "구성요소 이름과 용어 대조는 원문 §7.1 Figure 7.1 의 것입니다")

BOXES = [
    (24, "무선 기기", "스마트폰 · 노트북 · 센서", "다섯 계층을 모두 구현", INFO),
    (260, "기지국", "유선망에는 없는 부품", "연결된 기기의 중계를 맡음", INFO),
    (496, "무선 코어망", "서버 · 저장소 · 라우터", "신원 · 이동성 · 데이터 전달", ACC),
    (732, "바깥 인터넷", "게이트웨이 너머", "지금까지 여섯 장이 다룬 곳", MUTED),
]
BY, BH, BW = 116, 96, 172
for x, title, sub1, sub2, c in BOXES:
    d.tone(x, BY, BW, BH, c, 8, "14", 1.2)
    d.t(x + BW / 2, BY + 30, title, 13, INK, KR, "middle", 600)
    d.t(x + BW / 2, BY + 54, sub1, 11, c, KR)
    d.t(x + BW / 2, BY + 74, sub2, 11, MUTED, KR)

LINKS = [(196, 260, "무선 채널"), (432, 496, "백홀"), (668, 732, "게이트웨이")]
for x1, x2, label in LINKS:
    d.arrow([(x1 + 6, BY + BH / 2), (x2 - 6, BY + BH / 2)], MUTED, "ar", 1.4)
    d.t((x1 + x2) / 2, BY + BH / 2 - 14, label, 10, SOFT, KR)

TY = 244
d.t(24, TY, "같은 자리를 두 기술이 다르게 부릅니다", 12, INK, KR, "start", 600)
d.box(24, TY + 14, 880, 104, PAPER2, RULE, 1.0)
COLS = [188, 396, 604, 806]
for label, x in zip(["무선 기기", "기지국", "코어망", ""], COLS):
    if label:
        d.t(x, TY + 40, label, 11, SOFT, KR)
d.line(24, TY + 50, 904, TY + 50, RULE, 0.8)
ROWS = [
    ("5G 셀룰러", ["user equipment (UE)", "gNB", "5G Core", "3GPP 표기"], INFO),
    ("WiFi", ["device", "access point (AP)", "없음", "기업 유선망을 그대로"], ACC),
]
for i, (name, cells, c) in enumerate(ROWS):
    y = TY + 76 + i * 26
    d.t(32, y, name, 11, c, KR, "start", 600)
    for cell, x in zip(cells, COLS):
        is_none = cell == "없음"
        d.t(x, y, cell, 11, ACC if is_none else MUTED,
            KR if any("가" <= ch <= "힣" for ch in cell) else MONO,
            "middle", 600 if is_none else 400)

MY = 386
MODES = [
    (24, "인프라 모드", INK,
     ["주소 배정 · 신원 · 라우팅을 망이 줍니다.",
      "이 장은 WiFi 를 인프라 모드로 가정합니다."]),
    (496, "애드혹 모드", INK,
     ["그런 인프라가 없어 기기끼리 스스로 합니다.",
      "블루투스가 순수 애드혹의 예입니다."]),
]
for x, title, c, lines in MODES:
    d.box(x, MY, 408, 74, PAPER2, RULE, 1.0)
    d.t(x + 20, MY + 26, title, 12, c, KR, "start", 600)
    for j, ln in enumerate(lines):
        d.t(x + 20, MY + 48 + j * 18, ln, 11, MUTED, KR, "start")

d.legend(482, [("셀룰러에만 있는 자리", ACC), ("두 기술이 공유하는 자리", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-01.wireless-elements.svg"
d.save(out)
print("→", out)
