# 타입 스펙: type-swimlane — 역할을 가로지르며 넘겨받는 절차. 같은 채널을 세 부류가 시간 구간마다 나눠 갖는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.2 Figure 7.24 —
#   t0~t4 각 구간에서 누가 채널을 쓰는지와 MU-RTS 의 역할은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 624
d = D(W, H, "SECTION 7.3.2 · OFDM AND OFDMA COEXISTENCE",
      "옛 기기와 새 기기가 한 채널을 번갈아 씁니다",
      "AP 는 예약 장치인 MU-RTS 를 확장해 OFDM 만 아는 기기와 OFDMA 를 아는 기기를 같은 채널에 둔다.",
      "구간별 점유는 원문 Figure 7.24 의 것입니다")

LX, LW = 24, 168
CX0, CW = 208, 136
SLOTS = ["t0", "t1", "t2", "t3", "t4"]
LANES = [
    (136, "레거시 802.11g 기기", "OFDM 만 압니다", INFO,
     ["기기 a|채널 전체", "기기 b|채널 전체", "", "기기 b|채널 전체", ""]),
    (248, "WiFi 6 기기", "OFDMA 를 압니다", OK,
     ["", "", "기기 1·2·4·5|RU 를 나눠 씀", "", "기기 1·2·3|RU 를 나눠 씀"]),
    (360, "AP", "누가 언제 쓸지 정합니다", ACC,
     ["", "", "MU-RTS 로|채널 예약", "", "MU-RTS 로|채널 예약"]),
]
LH = 96
for i, s in enumerate(SLOTS):
    d.t(CX0 + i * CW + CW / 2, 116, s, 11, SOFT, MONO, "middle", 600)
for ly, name, sub, c, cells in LANES:
    d.tone(LX, ly, LW, LH, c, 6, "12", 1.2)
    d.t(LX + LW / 2, ly + 38, name, 12, c, KR, "middle", 600)
    d.t(LX + LW / 2, ly + 60, sub, 10, MUTED, KR)
    for i, txt in enumerate(cells):
        x = CX0 + i * CW
        if txt:
            d.tone(x + 4, ly + 12, CW - 8, LH - 24, c, 4, "22", 1.2)
            parts = txt.split("|")
            d.t(x + CW / 2, ly + 44, parts[0], 11, c, KR)
            if len(parts) > 1:
                d.t(x + CW / 2, ly + 64, parts[1], 11, c, KR)
        else:
            d.box(x + 4, ly + 12, CW - 8, LH - 24, PAPER, RULE, 0.7, 4)
d.line(CX0, 128, CX0 + len(SLOTS) * CW, 128, RULE, 0.8)
d.arrow([(CX0, 470), (CX0 + len(SLOTS) * CW, 470)], SOFT, "soft", 1.2)
d.t(CX0 + len(SLOTS) * CW / 2, 490, "시간", 10, SOFT, KR)

PY = 506
d.box(24, PY, 880, 56, PAPER2, RULE, 1.0)
d.t(44, PY + 22, "MU-RTS 는 OFDM 으로 모두에게 나갑니다", 12, INK, KR, "start", 600)
d.t(44, PY + 42,
    "OFDM 만 아는 기기는 보통 CTS 로 답하고, OFDMA 를 아는 기기는 자기에게 배정된 주파수로만 CTS 를 냅니다.",
    11, MUTED, KR, "start")

d.legend(PY + 74, [("레거시 OFDM", INFO), ("OFDMA", OK), ("AP 의 예약", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-03.ofdm-ofdma-coexistence.svg"
d.save(out)
print("→", out)
