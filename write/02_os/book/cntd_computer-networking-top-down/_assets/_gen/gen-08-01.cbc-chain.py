# 타입 스펙: type-data-flow — 값이 상자를 지나며 변형되고, 앞 단계의 출력이 다음 단계의 입력으로 되돌아 흐른다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.2.1 Cipher-Block Chaining (책 566~567쪽) —
#   평문 010010010, IV c(0)=001, 그리고 c(1)=100 · c(2)=000 · c(3)=101 은 원문 예제의 값이며
#   표 8.1 의 사상으로 이 기계에서 재현해 확인했다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 600
d = D(W, H, "SECTION 8.2.1 · CIPHER BLOCK CHAINING",
      "앞 블록의 결과가 다음 블록의 무작위가 됩니다",
      "블록마다 무작위를 보내면 대역폭이 두 배가 된다. 그래서 무작위는 맨 앞 한 번만 보내고 그다음은 직전 암호문을 쓴다.",
      "평문과 IV 와 세 암호문 블록은 원문 예제의 값입니다")

BAD_Y, OK_Y = 152, 320
d.t(24, BAD_Y - 18, "독립 암호화 — 같은 평문이 같은 암호문이 됩니다", 12, BAD, KR, "start", 600)
X0, CW, GAP = 172, 132, 56
for i, (m, c) in enumerate((("010", "101"), ("010", "101"), ("010", "101"))):
    x = X0 + i * (CW + GAP)
    d.box(x, BAD_Y, CW, 48, PAPER2, RULE, 0.9)
    d.t(x + CW / 2, BAD_Y + 30, m, 12, MUTED, MONO)
    d.arrow([(x + CW / 2, BAD_Y + 52), (x + CW / 2, BAD_Y + 78)], MUTED, "ar", 1.2)
    d.tone(x, BAD_Y + 82, CW, 48, BAD, 6, "18", 1.2)
    d.t(x + CW / 2, BAD_Y + 112, c, 12, BAD, MONO)
d.t(24, BAD_Y + 30, "평문", 11, SOFT, KR, "start")
d.t(24, BAD_Y + 112, "암호문", 11, SOFT, KR, "start")
d.t(X0 + 3 * (CW + GAP) + 8, BAD_Y + 112, "반복이 그대로 보입니다", 11, BAD, KR, "start")

d.line(24, 272, 976, 272, RULE, 0.8)
d.t(24, OK_Y - 18, "CBC — 직전 암호문을 섞어 넣습니다", 12, OK, KR, "start", 600)
IVX = 24
d.tone(IVX, OK_Y, 116, 48, ACC, 6, "20", 1.4)
d.t(IVX + 58, OK_Y + 22, "IV = c(0)", 11, ACC, MONO)
d.t(IVX + 58, OK_Y + 40, "001", 12, ACC, MONO, "middle", 600)
d.t(IVX + 58, OK_Y + 70, "평문으로 보냅니다", 11, SOFT, KR)

CHAIN = [("m(1)=010", "011", "c(1)=100"), ("m(2)=010", "110", "c(2)=000"), ("m(3)=010", "010", "c(3)=101")]
CX0, CCW, CGAP = 196, 220, 32
for i, (m, xor, c) in enumerate(CHAIN):
    x = CX0 + i * (CCW + CGAP)
    d.box(x, OK_Y, CCW, 104, PAPER2, RULE, 1.0, 7)
    d.t(x + CCW / 2, OK_Y + 26, m, 12, INK, MONO, "middle", 600)
    d.t(x + CCW / 2, OK_Y + 50, f"⊕ 앞 값 → {xor}", 11, MUTED, MONO)
    d.t(x + CCW / 2, OK_Y + 74, "K_S 통과", 11, INFO, KR)
    d.tone(x + 28, OK_Y + 120, CCW - 56, 44, OK, 6, "18", 1.3)
    d.t(x + CCW / 2, OK_Y + 148, c, 12, OK, MONO, "middle", 600)
    d.arrow([(x + CCW / 2, OK_Y + 106), (x + CCW / 2, OK_Y + 116)], MUTED, "ar", 1.2)
    if i == 0:
        d.arrow([(IVX + 118, OK_Y + 24), (x - 6, OK_Y + 24)], ACC, "acc", 1.4)
    if i < 2:
        nx = CX0 + (i + 1) * (CCW + CGAP)
        d.path(f"M {x + CCW / 2 + 34} {OK_Y + 142} L {x + CCW + 16} {OK_Y + 142} "
               f"L {x + CCW + 16} {OK_Y + 24} L {nx - 6} {OK_Y + 24}", OK, 1.4, m="ok")

NY = OK_Y + 196
d.t(24, NY, "받는 쪽은 c(i) 를 복호해 m(i) ⊕ c(i−1) 을 얻고, 이미 아는 c(i−1) 을 다시 걷어 평문을 복원합니다.",
    11, MUTED, KR, "start")
d.t(24, NY + 22, "IV 가 평문으로 나가도 열쇠 K_S 를 모르면 복호할 수 없고, 추가로 나가는 것은 이 한 블록뿐입니다.",
    11, MUTED, KR, "start")

d.legend(NY + 44, [("반복이 드러남", BAD), ("연쇄 뒤 암호문", OK), ("한 번만 보내는 IV", ACC), ("열쇠로 하는 일", INFO)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-01.cbc-chain.svg"
d.save(out); print("→", out.name)
