# 타입 스펙: type-process — 국면이 왼쪽에서 오른쪽으로 흐르고 각 국면이 같은 의미 슬롯을 갖는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.7.5 (책 604~605쪽) —
#   국면 1 의 두 교환과 국면 2 의 내용, 나눈 이유가 계산 비용이라는 것은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 560
d = D(W, H, "SECTION 8.7.5 · IKE TWO PHASES",
      "국면을 둘로 나눈 이유는 계산 비용입니다",
      "국면 2 는 공개키 암호를 쓰지 않는다. 그래서 한 번 세운 통로 위에서 많은 SA 를 싸게 만든다.",
      "두 국면의 내용은 원문 §8.7.5 의 것입니다")

BW, BH, BY = 296, 232, 148
XS = [24, 352, 680]
STEPS = [
    ("국면 1 · 첫 교환", "디피-헬먼으로 양방향 IKE SA",
     "IKE SA 용 암호화·인증 열쇠\n국면 2 에서 쓸 마스터 비밀",
     "RSA 공개키·개인키를 쓰지 않습니다.\n어느 쪽도 신원을 드러내지 않습니다.", INFO),
    ("국면 1 · 둘째 교환", "서명으로 서로 신원을 드러냄",
     "IPsec SA 가 쓸 암호화·인증\n알고리즘 협상",
     "이미 안전한 통로로 가므로\n엿듣는 자에게는 안 드러납니다.", INFO),
    ("국면 2", "방향마다 IPsec SA 하나씩",
     "두 SA 의 암호화·인증\n세션 열쇠 확립",
     "공개키 암호를 전혀 쓰지 않습니다.\n그래서 SA 를 많이 싸게 만듭니다.", ACC),
]
for x, (name, what, out_, note, c) in zip(XS, STEPS):
    if c is ACC:
        d.tone(x, BY, BW, BH, c, 7, "18", 1.4)
    else:
        d.box(x, BY, BW, BH, PAPER2, RULE, 1.0, 7)
    d.t(x + BW / 2, BY + 30, name, 12, c, KR, "middle", 600)
    d.line(x + 16, BY + 44, x + BW - 16, BY + 44, RULE, 0.8)
    d.t(x + BW / 2, BY + 68, what, 11, INK, KR)
    d.t(x + BW / 2, BY + 96, "세워지는 것", 10, SOFT, KR)
    for i, ln in enumerate(out_.split("\n")):
        d.t(x + BW / 2, BY + 118 + i * 18, ln, 11, OK, KR)
    for i, ln in enumerate(note.split("\n")):
        d.t(x + BW / 2, BY + 176 + i * 18, ln, 11, MUTED, KR)
for a, b in zip(XS, XS[1:]):
    d.arrow([(a + BW + 2, BY + BH / 2), (b - 4, BY + BH / 2)], MUTED, "ar", 1.3)

PY = 408
d.box(24, PY, 952, 76, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "IKE SA 와 IPsec SA 는 다른 것입니다", 12, INK, KR, "start", 600)
d.t(44, PY + 56, "국면 1 이 만드는 양방향 IKE SA 는 두 라우터 사이에 인증되고 암호화된 통로를 줄 뿐이고, 데이터그램을 나르는 것은 국면 2 가 만드는 단방향 IPsec SA 입니다.",
    11, MUTED, KR, "start")

d.legend(504, [("공개키를 쓰는 국면", INFO), ("공개키를 안 쓰는 국면", ACC), ("세워지는 것", OK)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-04.ike-phases.svg"
d.save(out); print("→", out.name)
