# 타입 스펙: type-dp-security-matrix — 격자 문법으로 "어느 행과 어느 열이 어긋나는가"를 본다.
#   축약: 역할×대상 권한 격자가 아니라 비트 격자다. 행·열 두 축의 교차가 답을 낸다는 구조는 같다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.2.1 Figure 6.5 의 비트값 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, OK, KR, MONO

W, H = 940, 444
d = D(W, H, "SECTION 6.2.1 · TWO-DIMENSIONAL EVEN PARITY",
      "행과 열이 동시에 어긋나면 자리가 나옵니다",
      "짝수 패리티를 행과 열 양쪽에 걸면, 한 비트가 뒤집혔을 때 어긋나는 행과 열의 교차점이 곧 그 비트의 자리다.",
      "원문 Figure 6.5 의 비트값 그대로입니다")

CLEAN = [[1, 0, 1, 0, 1], [1, 1, 1, 1, 0], [0, 1, 1, 1, 0]]
ROWP = [1, 0, 1]
COLP = [0, 0, 1, 0, 1]
CORNER = 0
CW, PW, RH = 36, 64, 32
GY = 148


def panel(px, title, flip):
    d.t(px + 152, 116, title, 12, INK, KR, "middle", 600)
    for j in range(5):
        d.t(px + 60 + j * CW + CW / 2, GY - 8, str(j + 1), 10, SOFT, MONO)
    d.t(px + 240 + PW / 2, GY - 8, "행 패리티", 10, SOFT, KR)

    for i in range(3):
        y = GY + i * RH
        d.t(px + 52, y + 21, str(i + 1), 10, SOFT, MONO, "end")
        for j in range(5):
            v = CLEAN[i][j]
            hot = flip and i == 1 and j == 1
            if hot:
                v = 0
            x = px + 60 + j * CW
            bad = flip and (i == 1 or j == 1)
            d.box(x, y, CW, RH, PAPER2 if not bad else PAPER, f"{BAD}55" if bad else RULE, 1.1 if bad else 0.8, 3)
            if hot:
                d.tone(x + 3, y + 3, CW - 6, RH - 6, ACC, 3, "22", 1.5)
            d.t(x + CW / 2, y + 21, str(v), 12, ACC if hot else INK, MONO, "middle", 600 if hot else 400)
        x = px + 240
        bad = flip and i == 1
        d.box(x, y, PW, RH, PAPER, f"{BAD}55" if bad else RULE, 1.1 if bad else 0.8, 3)
        d.t(x + PW / 2, y + 21, str(ROWP[i]), 12, BAD if bad else MUTED, MONO, "middle", 600 if bad else 400)

    y = GY + 3 * RH + 8
    d.t(px + 52, y + 21, "열 패리티", 10, SOFT, KR, "end")
    for j in range(5):
        x = px + 60 + j * CW
        bad = flip and j == 1
        d.box(x, y, CW, RH, PAPER, f"{BAD}55" if bad else RULE, 1.1 if bad else 0.8, 3)
        d.t(x + CW / 2, y + 21, str(COLP[j]), 12, BAD if bad else MUTED, MONO, "middle", 600 if bad else 400)
    d.box(px + 240, y, PW, RH, PAPER, RULE, 0.8, 3)
    d.t(px + 240 + PW / 2, y + 21, str(CORNER), 12, MUTED, MONO)
    return y + RH


bot = panel(64, "오류가 없을 때 — 모든 행과 열이 짝수", False)
panel(524, "(2,2) 의 1 이 0 으로 뒤집혔을 때", True)

d.t(64, bot + 30, "다섯 열과 세 행이 모두 1의 개수가 짝수입니다.", 11, MUTED, KR, "start")
d.t(524, bot + 30, "행 2 와 열 2 가 함께 어긋납니다. 교차점이 뒤집힌 비트입니다.", 11, MUTED, KR, "start")
d.t(524, bot + 48, "패리티 비트 자체가 뒤집혀도 같은 방식으로 잡힙니다.", 11, MUTED, KR, "start")

d.line(24, 344, W - 48, 344, RULE, 0.8)
d.t(24, 366, "데이터를 i 행 j 열로 나누면 패리티는 i + j + 1 비트입니다. 여기서는 3 행 5 열이라 9 비트입니다.",
     11, MUTED, KR, "start")
d.t(24, 384, "한 비트 오류는 검출하고 정정합니다. 두 비트 오류는 어떤 조합이든 검출하지만 정정하지는 못합니다.",
     11, MUTED, KR, "start")

d.legend(404, [("패리티가 어긋난 행과 열", BAD), ("교차점 — 뒤집힌 비트", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-01.two-dim-parity.svg"
d.save(out)
print("→", out)
