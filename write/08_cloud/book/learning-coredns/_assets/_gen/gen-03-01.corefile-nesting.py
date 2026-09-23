# 03-01 §3 — Corefile 문법의 중첩 깊이와 그 바닥.
# 원문 근거: "Corefiles consist of one or more entries, which themselves comprise labels and
#            definitions" / 여는 중괄호는 라벨 줄 끝에, 닫는 중괄호는 홀로 한 줄에 / 중괄호 안 텍스트를
#            블록이라 부른다 / "Definitions are made up of directives and optional arguments" /
#            인자가 여러 줄이면 중괄호로 감싼다 / "subdirectives can appear within a directive, as long
#            as they begin the line" / "The subdirectives can't begin a new curly-brace-delimited block".
# 2026-09-23 개정: 부제가 본문(중괄호가 그리는 깊이는 블록과 여러 줄 인자 둘)과 어긋나 고쳤다.
#   테두리 위 라벨 knockout 이 shape-overlap 을 내서 라벨을 상자 안으로 옮기고, 바닥의 문장 라벨을 걷었다.
# 타입 스펙: type-nested — 포함으로 계층을 보이고, 가장 안쪽이 더 못 들어가는 바닥이라는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 880, 500
d = D(W, H, "LEARNING COREDNS · 03-01 §3",
      "Corefile 문법이 품는 네 겹과 그 바닥",
      "엔트리 안에 블록이 있고, 블록 안에 지시어가 있고, 지시어의 인자가 길면 다시 중괄호로 감싼다. "
      "그 안에 서브지시어까지는 들어가지만 거기서 끝이다. 중괄호가 실제로 그리는 것은 블록과 여러 줄 인자 두 겹이다.",
      "점선 테두리가 중괄호로 그어지는 겹입니다")

# stride — 바깥에서 안으로 좌우 32px, 위 48px(라벨 자리), 아래 24px 씩 줄인다
rings = [
    (40, 96, 800, 344, "엔트리", "라벨 + 정의", False),
    (72, 144, 736, 272, "블록", "{ 는 라벨 줄 끝 · } 는 홀로 한 줄", True),
    (104, 192, 672, 200, "지시어와 인자", "줄마다 지시어 하나 · 여러 줄 인자는 { }", True),
    (136, 240, 608, 128, "서브지시어", "", False),
]
for i, (x, y, w, h, label, band, brace) in enumerate(rings):
    last = i == len(rings) - 1
    if last:
        d.tone(x, y, w, h, ACC, 8, "0A", 1.4)
    else:
        dash = ' stroke-dasharray="6 4"' if brace else ""
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{PAPER}" '
                   f'stroke="{SOFT if brace else RULE}" stroke-width="1.1"{dash}/>')
    d.t(x + 18, y + 26, label, 13, ACC if last else INK, KR, "start", 600)
    if band:
        d.t(x + w - 18, y + 26, band, 12, MUTED, KR, "end")

d.t(440, 304, "새 { } 블록 열기 불가", 15, ACC, KR, "middle", 600)
d.t(440, 332, "저자의 \"작은 자비\" · Corefile 문법의 바닥", 12, MUTED)

d.legend(456, [("더 들어갈 수 없는 층", ACC), ("중괄호로 그어지는 겹 · 점선", SOFT)])
d.save("03-01.corefile-nesting.svg")
