# 05-02.closure-capture — makeMult 가 돌려준 클로저는 호출마다 따로 base 를 붙잡는다
# 본문 요구(05-02 §5 「함수에서 함수 돌려주기」): makeMult(2) 와 makeMult(3) 이 돌려준 함수가 각자 자기 base 를 쥐고 있어서,
#           같은 i 로 불러도 twoBase 는 0 2 4, threeBase 는 0 3 6 을 낸다. 호출 하나가 만든 환경 안에 클로저가 들어 있는
#           포함 관계가 논지다.
# 타입 스펙: type-nested — 좌우 두 열, 각 열의 바깥 상자는 makeMult 호출 한 번이 만든 환경(base), 안쪽 상자는 그 환경을
#           붙잡은 채 반환된 클로저. 아래 칩이 변수 이름과 호출 결과. stride: 열 폭 448, 열 간격 40, 겹 여백 24.
#           focal 은 없고(두 열이 대등), 붙잡은 변수 base 칩만 accent 로 강조하지 않고 info 로 둔다.
# 사실 출처: Learning Go 2판 5장 「Returning Functions from Functions」, go1.25.1 실행(2026-09-27) — 0 0 · 2 3 · 4 6.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER2, KR, MONO

W, H = 984, 508
COLW, GAP = 448, 40
XS = (24, 24 + COLW + GAP)


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "NESTED · 05-02 §5",
      "클로저는 자기 환경을 붙잡고 반환된다",
      "makeMult(2) 와 makeMult(3) 을 한 번씩 부른 결과를 좌우로 나란히 그린 그림. 호출마다 base 가 담긴 환경이 따로 생기고, "
      "반환된 클로저는 그 환경을 붙잡은 채 twoBase·threeBase 변수에 담긴다. 그래서 같은 i 로 불러도 두 함수는 각자의 base 를 곱한다.",
      lead="바깥 상자가 호출 한 번의 환경, 안쪽 상자가 그 환경을 붙잡은 채 반환된 함수입니다.")

cols = [("makeMult(2)", "base = 2", "twoBase", "0 · 2 · 4"), ("makeMult(3)", "base = 3", "threeBase", "0 · 3 · 6")]
for k, x in enumerate(XS):
    call, base, var, out = cols[k]
    d.o.append(f'<rect x="{x}" y="104" width="{COLW}" height="232" rx="8" fill="#161B22" stroke="rgba(191,192,192,0.30)" stroke-width="0.9"/>')
    d.t(x + 16, 130, call + " 호출이 만든 환경", 14, INK, KR, "start", 600)
    d.tone(x + COLW - 140, 114, 116, 28, INFO, 4, "18", 1.0)
    d.t(x + COLW - 82, 133, base, 13, INFO, MONO, "middle", 600)
    d.o.append(f'<rect x="{x + 24}" y="160" width="{COLW - 48}" height="152" rx="8" fill="#0D1117" stroke="{OK}" stroke-width="1.2"/>')
    d.t(x + 40, 188, "반환된 클로저", 13, OK, KR, "start", 600)
    d.t(x + 40, 224, "func(factor int) int {", 13, INK, MONO, "start")
    d.t(x + 64, 252, "return base * factor", 13, INFO, MONO, "start", 600)
    d.t(x + 40, 280, "}", 13, INK, MONO, "start")
    d.t(x + 40, 300, "base 는 인자가 아니라 붙잡은 변수", 12, MUTED, KR, "start")
    cx = x + COLW // 2
    d.arrow([(cx, 336), (cx, 372)], SOFT, "soft", 1.2)
    d.tone(cx - 140, 376, 280, 36, OK, 4, "14", 1.0)
    d.t(cx, 399, var + " := " + call, 13, OK, MONO, "middle", 600)
    d.t(cx, 440, var + "(0), (1), (2) → " + out, 13, INK, MONO, "middle")

d.legend(460, [("붙잡힌 변수", INFO), ("클로저와 그것을 담은 변수", OK)])
d.save("05-02.closure-capture.svg")
print("ok 05-02 closure-capture")
