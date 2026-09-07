# 타입 스펙: type-swimlane — 역할을 가로지르며 넘겨받는 절차. 핸드오버가 RAN 에서 시작해 코어에서 끝난다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.5.3 Figure 7.45 —
#   세 국면의 구분과 각 국면에서 오가는 메시지는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 648
d = D(W, H, "SECTION 7.5.3 · 5G HANDOVER",
      "RAN 에서 시작해 코어에서 끝납니다",
      "핸드오버는 판단과 전환과 갱신 세 국면으로 나뉜다. 데이터가 끊기지 않도록 옛 기지국이 잠시 중계까지 맡는다.",
      "국면 구분과 메시지는 원문 Figure 7.45 의 것입니다")

LX, LW = 24, 168
CX0, CW = 208, 232
STAGES = ["1 · 판단", "2 · 기지국 전환", "3 · 코어 갱신"]
LANES = [
    (148, "무선 기기", INFO, ["들리는 기지국의 품질을 재서 보고", "재설정 완료를 타깃에 알림", ""]),
    (244, "소스 기지국", ACC, ["핸드오버 요청을 타깃에 보냄", "기기 상태를 넘기고 데이터그램 중계", "종료 표시를 받고 타깃에 알림"]),
    (340, "타깃 기지국", OK, ["받아들일지 정해 응답", "새 RAN 연결을 세우고 버퍼링", "SMF 에 자기가 새 기지국임을 알림"]),
    (436, "코어 (AMF · SMF · UPF)", MUTED, ["", "", "UPF 의 터널 끝을 타깃으로 옮김"]),
]
LH = 84
for i, s in enumerate(STAGES):
    d.t(CX0 + i * CW + CW / 2, 130, s, 11, SOFT, KR, "middle", 600)
d.line(CX0, 140, CX0 + len(STAGES) * CW, 140, RULE, 0.8)
for ly, name, c, cells in LANES:
    d.tone(LX, ly, LW, LH, c, 6, "12", 1.2)
    d.t(LX + LW / 2, ly + 50, name, 11, c, KR, "middle", 600)
    for i, txt in enumerate(cells):
        x = CX0 + i * CW
        if txt:
            d.tone(x + 6, ly + 14, CW - 12, LH - 28, c, 4, "22", 1.2)
            words = txt.split()
            mid = (len(words) + 1) // 2
            d.t(x + CW / 2, ly + 42, " ".join(words[:mid]), 10, c, KR)
            if words[mid:]:
                d.t(x + CW / 2, ly + 60, " ".join(words[mid:]), 10, c, KR)
        else:
            d.box(x + 6, ly + 14, CW - 12, LH - 28, PAPER, RULE, 0.7, 4)
d.arrow([(CX0, 542), (CX0 + len(STAGES) * CW, 542)], SOFT, "soft", 1.2)
d.t(CX0 + len(STAGES) * CW / 2, 562, "시간", 10, SOFT, KR)

d.legend(582, [("기기", INFO), ("옛 기지국", ACC), ("새 기지국", OK), ("코어", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-05.5g-handover.svg"
d.save(out)
print("→", out)
