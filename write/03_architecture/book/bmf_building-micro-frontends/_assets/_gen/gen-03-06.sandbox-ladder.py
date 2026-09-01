# 03-06 §1 — sandbox 를 여는 단계. 저자가 보인 두 코드 조각과 그 설명만 옮긴다.
# 세 번째 칸은 두 값을 함께 준 경우로, 저자의 두 번째 예제가 그대로 그 상태다.
# 타입 스펙: type-process — 단계마다 같은 의미 슬롯(무엇을 여나 · 그때의 마크업)이 반복되고 화살표가 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 lanes 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1200
CW, CH, GAP, X0, Y = 356, 136, 32, 40, 112
LEGEND_Y = Y + CH + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-06 §1",
      "sandbox 는 닫힌 데서 시작해 하나씩 연다",
      "왼쪽이 가장 권한이 적은 구현이고 오른쪽으로 갈수록 제한이 풀린다. 색이 붙은 첫 칸이 저자가 기본으로 든 상태다.",
      "오른쪽으로 갈수록 iframe 안에서 할 수 있는 일이 늘어납니다")

steps = [
    ("01", "sandbox 단독", "스크립트도 폼 제출도 막힌다", "sandbox", True),
    ("02", "스크립트를 연다", "자바스크립트 파일 실행을 허용", 'sandbox="allow-scripts"', False),
    ("03", "폼까지 연다", "폼 제출도 함께 허용", 'sandbox="allow-scripts allow-forms"', False),
]

def x_of(i): return X0 + i * (CW + GAP)

for i in range(2):
    d.arrow([(x_of(i) + CW, Y + CH / 2), (x_of(i + 1) - 2, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, name, sub, mark, focal) in enumerate(steps):
    x = x_of(i)
    if focal:
        d.tone(x, Y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, Y + 28, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, Y + 56, name, 14.5, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, Y + 80, sub, 11, MUTED, KR, "start")
    d.t(x + 18, Y + 112, mark, 9.5, ACC if focal else INK, MONO, "start")

d.legend(LEGEND_Y, [("저자가 가장 권한이 적다고 든 구현", ACC)])
d.save("03-06.sandbox-ladder.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
