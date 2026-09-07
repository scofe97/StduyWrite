# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 5G 링크 계층의 다섯 부계층과 그 아래의 물리 계층.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.3 Figure 7.31 · Figure 7.33 (책 507~509쪽) —
#   원문이 세는 다섯 불릿은 RRC · SDAP · PDCP · RLC · MAC 이고 물리 계층은 이 목록에 없다.
#   부계층 이름과 각자의 책임, RU·DU·CU 분해는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 672
d = D(W, H, "SECTION 7.3.3 · 5G RAN LINK LAYER",
      "WiFi 가 한 층으로 하는 일을 5G 는 다섯 부계층으로 나눕니다",
      "원문이 세는 다섯 가운데 첫째가 제어 평면의 RRC 다. 나머지 넷이 사용자 평면을 나눠 맡는다.",
      "다섯 부계층의 구성은 원문 Figure 7.31 과 507~508쪽 불릿의 것입니다")

LX, LW = 24, 592
LY0, LH, STRIDE = 126, 50, 58
LAYERS = [
    ("RRC", "제어 평면. 논리 채널·연결 상태·이동성 일부·채널 품질 보고", ACC),
    ("SDAP", "사용자 평면의 최상위. QoS 흐름 ID 를 붙여 무선 자원에 대응", OK),
    ("PDCP", "IP 헤더 압축. 선택적으로 암호화와 무결성 검사", OK),
    ("RLC", "분할과 재조립. 순서 번호와 CRC 와 ACK/NAK 로 재전송", OK),
    ("MAC", "사용자 프레임과 제어 프레임의 전송 순서를 정함", OK),
]
for i, (name, desc, c) in enumerate(LAYERS):
    y = LY0 + i * STRIDE
    d.tone(LX, y, LW, LH, c, 6, "12", 1.2)
    d.t(LX + 20, y + 22, name, 12, c, KR, "start", 600)
    d.t(LX + 20, y + 40, desc, 10, MUTED, KR, "start")
    d.t(LX + LW - 16, y + 22, f"{i + 1}", 9, SOFT, MONO, "end")

PHY_Y = LY0 + len(LAYERS) * STRIDE + 6
d.box(LX, PHY_Y, LW, LH, PAPER, INFO, 1.2, 6)
d.o[-1] = d.o[-1].replace('stroke-width="1.2"', 'stroke-width="1.2" stroke-dasharray="6 5"')
d.t(LX + 20, PHY_Y + 22, "물리 계층", 12, INFO, KR, "start", 600)
d.t(LX + 20, PHY_Y + 40, "심볼을 자원 블록에 실어 내보냅니다 — 원문은 이것을 링크 부계층으로 세지 않습니다",
    10, MUTED, KR, "start")

RX, RW = 644, 260
d.box(RX, LY0, RW, len(LAYERS) * STRIDE - (STRIDE - LH), PAPER2, RULE, 1.0)
d.t(RX + 20, LY0 + 26, "RRC 가 다른 넷과 다른 점", 12, INK, KR, "start", 600)
d.line(RX + 20, LY0 + 38, RX + RW - 20, LY0 + 38, RULE, 0.8)
for j, ln in enumerate([
    "나머지 넷은 프레임을 실어",
    "나르는 일을 나눠 맡습니다.",
    "",
    "RRC 는 그 넷과 물리 계층의",
    "상태를 설정하는 방식으로",
    "자기 일을 해냅니다.",
    "",
    "기지국과 기기가 RRC 메시지를",
    "주고받으며 그 설정을 맞춥니다.",
]):
    if ln:
        d.t(RX + 20, LY0 + 64 + j * 22, ln, 11, MUTED, KR, "start")
d.arrow([(LX + LW + 6, LY0 + 25), (RX - 6, LY0 + 25)], ACC, "acc", 1.3, "5 5")

PY = PHY_Y + LH + 24
d.box(24, PY, 880, 92, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "5G 부터는 기지국 자체도 셋으로 쪼갭니다", 12, INK, KR, "start", 600)
SPLIT = [("RU", "무선 유닛"), ("DU", "분산 유닛"), ("CU", "중앙 유닛")]
for i, (nm, ko) in enumerate(SPLIT):
    x = 60 + i * 168
    d.tone(x, PY + 40, 144, 38, INFO, 6, "16", 1.2)
    d.t(x + 72, PY + 58, nm, 12, INFO, MONO, "middle", 600)
    d.t(x + 72, PY + 73, ko, 10, MUTED, KR)
    if i < 2:
        d.arrow([(x + 148, PY + 59), (x + 164, PY + 59)], MUTED, "ar", 1.2)
d.t(596, PY + 52, "표준 인터페이스로 이어서 여러 회사가", 11, MUTED, KR, "start")
d.t(596, PY + 72, "부분마다 경쟁 구현을 낼 수 있게 했습니다.", 11, MUTED, KR, "start")

d.legend(PY + 112, [("제어 평면 부계층", ACC), ("사용자 평면 부계층", OK), ("부계층이 아닌 것", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-03.5g-link-layers.svg"
d.save(out)
print("→", out)
