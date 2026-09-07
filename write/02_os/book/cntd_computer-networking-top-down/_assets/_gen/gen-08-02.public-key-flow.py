# 타입 스펙: type-swimlane — 앨리스·밥·트루디 세 역할을 가로지르며 무엇이 공개이고 무엇이 비밀인지 갈린다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.2.2 Figure 8.6 (책 568~569쪽) —
#   K_B+ · K_B- 기호와 K_B-(K_B+(m)) = m, 그리고 "누구나 밥에게 보낼 수 있다"는 우려는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 592
d = D(W, H, "SECTION 8.2.2 · PUBLIC KEY CRYPTOGRAPHY",
      "미리 만나지 않아도 비밀을 보낼 수 있습니다",
      "밥의 공개키는 온 세상이 가져다 쓴다. 그런데도 열 수 있는 사람은 개인키를 쥔 밥뿐이다.",
      "기호와 흐름은 원문 Figure 8.6 의 것입니다")

CX0, CW = 264, 232
STAGES = ["1 · 공개키를 가져옴", "2 · 공개키로 잠금", "3 · 개인키로 엶"]
LANES = [
    (140, "앨리스", INFO, ["밥의 공개키 K_B+ 를 받아 옵니다", "K_B+(m) 을 계산해 보냅니다", ""]),
    (240, "밥", OK, ["K_B+ 를 온 세상에 내놓습니다", "", "K_B-(K_B+(m)) = m 을 계산합니다"]),
    (340, "트루디", BAD, ["K_B+ 를 똑같이 가질 수 있습니다", "암호문을 볼 수 있습니다", "K_B- 가 없어 열지 못합니다"]),
]
LH = 88
for i, s in enumerate(STAGES):
    d.t(CX0 + i * CW + CW / 2, 122, s, 11, SOFT, KR, "middle", 600)
d.line(CX0, 132, CX0 + 3 * CW, 132, RULE, 0.8)
for ly, name, c, cells in LANES:
    d.tone(24, ly, 216, LH, c, 6, "12", 1.2)
    d.t(132, ly + LH / 2 + 5, name, 13, c, KR, "middle", 600)
    for i, txt in enumerate(cells):
        x = CX0 + i * CW
        if txt:
            d.tone(x + 6, ly + 12, CW - 12, LH - 24, c, 4, "20", 1.2)
            words = txt.split()
            mid = (len(words) + 1) // 2
            d.t(x + CW / 2, ly + 40, " ".join(words[:mid]), 11, c, KR)
            if words[mid:]:
                d.t(x + CW / 2, ly + 60, " ".join(words[mid:]), 11, c, KR)
        else:
            d.box(x + 6, ly + 12, CW - 12, LH - 24, PAPER, RULE, 0.7, 4)

PY = 456
d.tone(24, PY, 952, 60, ACC, 8, "16", 1.4)
d.t(44, PY + 26, "순서를 뒤집어도 같은 결과가 나옵니다", 12, ACC, KR, "start", 600)
d.t(44, PY + 48, "K_B-(K_B+(m)) = K_B+(K_B-(m)) = m  —  이 대칭이 뒤에서 디지털 서명이 됩니다",
    11, MUTED, MONO, "start")

d.legend(536, [("앨리스", INFO), ("밥", OK), ("트루디", BAD), ("뒤집기", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-02.public-key-flow.svg"
d.save(out); print("→", out.name)
