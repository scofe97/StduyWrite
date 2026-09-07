# 타입 스펙: type-loop — 마지막 단계가 첫 단계를 먹이고 가운데 표에 상태가 쌓이는 순환.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.3 Self-Learning 세 단계와
#   Figure 6.23 의 표 값, 그리고 aging time 60 분 예 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 528
d = D(W, H, "SECTION 6.4.3 · SELF-LEARNING",
      "표는 스스로 채워지고 스스로 비워집니다",
      "관리자도 설정 프로토콜도 없이 표가 만들어진다. 프레임의 출발지 주소가 표를 먹이고, 그 표가 다음 프레임의 판정을 먹인다.",
      "표의 값과 시각은 원문 Figure 6.23 그대로입니다")

STEPS = [
    (40, 116, "1 · 표는 비어서 시작합니다", ["관리자가 아무것도 넣지 않습니다"], INFO),
    (40, 300, "3 · 오래된 항목을 지웁니다", ["그 주소가 출발지인 프레임이", "aging time 동안 없으면 삭제합니다"], BAD),
    (700, 116, "2 · 받은 프레임에서 배웁니다", ["출발지 MAC · 들어온 인터페이스", "· 현재 시각을 적습니다"], OK),
    (700, 300, "그리고 다시 판정에 씁니다", ["채워진 표가 필터링과", "포워딩의 근거가 됩니다"], ACC),
]
for x, y, title, lines, c in STEPS:
    d.box(x, y, 260, 92, PAPER2, f"{c}55", 1.2, 6)
    d.t(x + 16, y + 26, title, 11, c, KR, "start", 600)
    for j, line in enumerate(lines):
        d.t(x + 16, y + 50 + j * 18, line, 11, MUTED, KR, "start")

TX, TY, TW, TH = 348, 176, 304, 156
d.box(TX, TY, TW, TH, PAPER, f"{ACC}55", 1.4, 7)
d.t(TX + TW / 2, TY + 26, "스위치 표", 12, ACC, KR, "middle", 600)
d.line(TX + 16, TY + 38, TX + TW - 16, TY + 38, RULE, 0.8)
d.t(TX + 16, TY + 58, "주소", 10, SOFT, KR, "start")
d.t(TX + 200, TY + 58, "인터페이스", 10, SOFT, KR, "middle")
d.t(TX + TW - 16, TY + 58, "시각", 10, SOFT, KR, "end")
for i, (mac, itf, t, c) in enumerate([("01-12-23-34-45-56", "2", "9:39", ACC),
                                      ("62-FE-F7-11-89-A3", "1", "9:32", MUTED),
                                      ("7C-BA-B2-B4-91-10", "3", "9:36", MUTED)]):
    y = TY + 82 + i * 22
    d.t(TX + 16, y, mac, 11, c, MONO, "start", 600 if c is ACC else 400)
    d.t(TX + 200, y, itf, 11, c, MONO, "middle")
    d.t(TX + TW - 16, y, t, 11, c, MONO, "end")
d.t(TX + TW / 2, TY + TH - 8, "9:39 에 새 항목이 하나 늘었습니다", 10, ACC, KR)

d.path("M 300 162 L 324 162 L 324 176", INFO, 1.2, m="info")
d.path("M 700 162 L 676 162 L 676 176", OK, 1.2, m="ok")
d.path("M 300 346 L 324 346 L 324 332", BAD, 1.2, m="bad")
d.path("M 676 332 L 676 346 L 696 346", ACC, 1.2, m="acc")

d.line(24, 420, W - 48, 420, RULE, 0.8)
d.t(24, 442, "aging time 이 60 분이고 9:32 부터 10:32 까지 62-FE-F7-11-89-A3 이 출발지인 프레임이 없으면 10:32 에 그 줄이 사라집니다.",
     11, MUTED, KR, "start")
d.t(24, 460, "그래서 PC 를 다른 어댑터를 가진 PC 로 바꿔도 옛 주소가 저절로 정리됩니다. 스위치가 플러그 앤 플레이인 이유입니다.",
     11, MUTED, KR, "start")

d.legend(478, [("표에 쌓이는 상태", ACC), ("빈 표에서 시작", INFO), ("배워서 적음", OK), ("때가 되면 지움", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-04.self-learning.svg"
d.save(out)
print("→", out)
