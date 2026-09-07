# 타입 스펙: type-process — 단계마다 같은 슬롯(들어오는 것·하는 일·나가는 것)이 반복된다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.2.2 Figure 7.11 —
#   단계 이름과 수신기 피드백 화살표의 뜻은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 568
d = D(W, H, "SECTION 7.2.2 · CODING AND MODULATION",
      "링크 계층이 준 비트가 파형이 되어 돌아오기까지",
      "송신기는 비트를 늘리고 섞은 뒤 파형으로 바꾼다. 수신기는 그 반대 순서를 밟고, 채널 상태를 되돌려 준다.",
      "단계 이름과 피드백의 뜻은 원문 Figure 7.11 의 것입니다")

COLS = [(24, 168, "부호화", INFO), (216, 168, "변조", INFO), (408, 168, "무선 채널", ACC),
        (600, 168, "복조", OK), (792, 112, "복호", OK)]
HEAD_Y, HEAD_H = 108, 38
SLOTS = ["들어오는 것", "하는 일", "나가는 것"]
SY, SH, SSTRIDE = 158, 56, 64
CELLS = [
    ["링크 계층 비트", "중복 비트를 더하고 순서를 섞습니다", "늘어난 비트열"],
    ["부호화된 비트", "비트를 묶어 심볼로, 심볼을 파형으로", "전자기 파형"],
    ["전자기 파형", "감쇠 · 반사 · 잡음을 더합니다", "일그러진 파형"],
    ["받은 파형", "진폭 · 주파수 · 위상을 재서 심볼을 봅니다", "부호화된 비트"],
    ["부호화 비트", "섞인 순서를 풀고 오류를 메웁니다", "원래 비트"],
]
d.t(24, 96, "각 칸의 세 줄은 위에서부터 들어오는 것 · 하는 일 · 나가는 것입니다", 11, SOFT, KR, "start")
for (x, w, name, c), cells in zip(COLS, CELLS):
    d.tone(x, HEAD_Y, w, HEAD_H, c, 6, "18", 1.2)
    d.t(x + w / 2, HEAD_Y + 25, name, 12, c, KR, "middle", 600)
    for i, txt in enumerate(cells):
        y = SY + i * SSTRIDE
        d.box(x, y, w, SH, PAPER2, RULE, 0.9)
        words = txt.split()
        line1, line2 = txt, ""
        if len(txt) > 13:
            half = len(words) // 2 or 1
            line1, line2 = " ".join(words[:half]), " ".join(words[half:])
        if line2:
            d.t(x + w / 2, y + 24, line1, 10, MUTED, KR)
            d.t(x + w / 2, y + 40, line2, 10, MUTED, KR)
        else:
            d.t(x + w / 2, y + 32, line1, 11, MUTED, KR)

for i in range(len(COLS) - 1):
    x1 = COLS[i][0] + COLS[i][1]
    d.arrow([(x1 + 4, HEAD_Y + HEAD_H / 2), (COLS[i + 1][0] - 4, HEAD_Y + HEAD_H / 2)], MUTED, "ar", 1.3)

FB_Y = SY + 3 * SSTRIDE + 12
d.arrow([(COLS[3][0] + 84, FB_Y), (COLS[3][0] + 84, FB_Y + 26),
         (COLS[1][0] + 84, FB_Y + 26), (COLS[1][0] + 84, FB_Y)], ACC, "acc", 1.4, "5 5")
d.t((COLS[1][0] + COLS[3][0]) / 2 + 84, FB_Y + 46,
    "수신기가 채널 상태를 되돌려 주면 송신기가 변조 방식을 바꿉니다", 11, ACC, KR, "middle", 600)

NY = FB_Y + 64
d.box(24, NY, 880, 62, PAPER2, RULE, 1.0)
d.t(44, NY + 24, "물리 계층이 더하는 비트는 6장에서 배운 CRC 와 별개입니다", 12, INK, KR, "start", 600)
d.t(44, NY + 46, "링크 계층 프레임 안의 CRC 비트도 물리 계층에서는 그냥 비트라서, 다시 보호 대상이 됩니다.",
    11, MUTED, KR, "start")

d.legend(NY + 82, [("송신기 쪽", INFO), ("채널", ACC), ("수신기 쪽", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-02.bits-to-waveform.svg"
d.save(out)
print("→", out)
