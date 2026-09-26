# 02-01.chapter-overview — Go 의 사전 선언 타입을 다섯 갈래로 나누고, 갈래마다 제로 값과 리터럴 기본 타입을 단다
# 본문 요구(02-01 「학습 목표」 지도 문단): "사전 선언 타입은 불리언·정수·부동소수점·복소수·문자열 다섯 갈래이고,
#           갈래마다 선언만 했을 때의 제로 값과 리터럴이 기본으로 갖는 타입이 다르다" — 한 뿌리에서 갈라지는 계층이다.
# 타입 스펙: type-tree — root 1 · 1단 5개 · 2단 5개(leaf). 스펙 관례: 노드 폭 120–180(여기 176), 높이 40–52(여기 52),
#           연결선은 꺾은선(부모 수직 → 가로 버스 → 자식 수직), coral 은 leaf 하나(정수의 "기본 int").
#           stride 는 가로 192(노드 176 + 간격 16), 세로 단 간격 104. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 2장 「The Zero Value」「Literals」「Booleans」「Numeric Types」「A Taste of Strings and Runes」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 984, 492
NW, NH, STRIDE = 176, 52, 192
X0 = (W - (5 * STRIDE - 16)) // 2          # 32
ROOT_Y, L1_Y, L2_Y = 108, 212, 316


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def cx(j):
    return X0 + j * STRIDE + NW // 2


d = D(W, H, "TREE · 02-01 OVERVIEW",
      "사전 선언 타입 다섯 갈래와 제로 값",
      "Go 에 미리 선언된 타입을 불리언·정수·부동소수점·복소수·문자열 다섯 갈래로 나눈 트리. "
      "1단은 갈래와 그 안의 타입 이름, 2단은 값을 주지 않고 선언했을 때의 제로 값과 리터럴의 기본 타입이다. "
      "정수 갈래의 기본 타입 int 가 이 편에서 가장 자주 쓰는 선택이다.",
      lead="1단은 타입 이름, 2단은 제로 값과 리터럴이 기본으로 갖는 타입입니다.")

cats = [("불리언", "bool"), ("정수", "int · int64 · uint8 …"), ("부동소수점", "float32 · float64"),
        ("복소수", "complex64 · complex128"), ("문자열", "string")]
leaves = [("false", "값은 true · false"), ("0", "기본 int"), ("0", "기본 float64"),
          ("0 + 0i", "기본 complex128"), ('""', "불변 · 기본 string")]
tones = (INFO, ACC, INFO, INFO, OK)

# 연결선 먼저 — 루트 → 버스 → 1단, 1단 → 2단
rx = W // 2
d.line(rx, ROOT_Y + 40, rx, 176, SOFT, 1.0)
d.line(cx(0), 176, cx(4), 176, SOFT, 1.0)
for j in range(5):
    d.line(cx(j), 176, cx(j), L1_Y, SOFT, 1.0)
    d.line(cx(j), L1_Y + NH, cx(j), L2_Y, SOFT, 1.0)

d.box(rx - 120, ROOT_Y, 240, 40)
d.t(rx, ROOT_Y + 26, "사전 선언 타입", 14, INK, KR, "middle", 600)

for j in range(5):
    x = cx(j) - NW // 2
    d.box(x, L1_Y, NW, NH)
    d.t(cx(j), L1_Y + 22, cats[j][0], 14, INK, KR, "middle", 600)
    d.t(cx(j), L1_Y + 42, cats[j][1], 12, MUTED, MONO, "middle")
    c = tones[j]
    d.tone(x, L2_Y, NW, NH, c, 6, "14" if c == ACC else "10", 1.4 if c == ACC else 1.0)
    d.t(cx(j), L2_Y + 22, leaves[j][0], 14, c, MONO, "middle", 600)
    d.t(cx(j), L2_Y + 42, leaves[j][1], 12, MUTED, kr(leaves[j][1]), "middle")


d.legend(424, [("수 · 참거짓의 제로 값", INFO), ("빈 문자열", OK), ("기본으로 쓸 정수 타입", ACC)])
d.save("02-01.chapter-overview.svg")
print("ok 02-01 overview")
