# 03-01 §3 — Corefile 문법의 중첩 깊이와 그 바닥.
# 원문 근거: "Corefiles consist of one or more entries, which themselves comprise labels and
#            definitions" / 여는 중괄호는 라벨 줄 끝에, 닫는 중괄호는 홀로 한 줄에 / 중괄호 안 텍스트를
#            블록이라 부른다 / "Definitions are made up of directives and optional arguments" /
#            인자가 여러 줄이면 중괄호로 감싼다 / "subdirectives can appear within a directive, as long
#            as they begin the line" / "The subdirectives can't begin a new curly-brace-delimited block".
# 타입 스펙: type-nested — 포함으로 계층을 보이고, 가장 안쪽이 더 못 들어가는 바닥이라는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING COREDNS · 03-01 §3",
      "Corefile 문법이 품는 네 겹과 그 바닥",
      "엔트리 안에 블록이 있고, 블록 안에 지시어가 있고, 지시어의 인자가 길면 다시 중괄호로 감싼다. "
      "그 안에 서브지시어까지는 들어가지만 거기서 끝이다.",
      "바깥 두 겹만 중괄호가 그리고, 안쪽 둘은 문법이 품는 관계입니다")

rings = [
    (40, 96, 800, 340, "엔트리", "라벨 + 정의", MUTED),
    (72, 132, 736, 268, "블록", "여는 중괄호는 라벨 줄 끝, 닫는 중괄호는 홀로 한 줄", MUTED),
    (104, 168, 672, 196, "지시어와 인자", "줄마다 지시어 하나로 시작한다", MUTED),
    (136, 204, 608, 124, "서브지시어", "", ACC),
]
for x, y, w, h, label, band, color in rings:
    if color is ACC:
        d.tone(x, y, w, h, ACC, 8, "0A", 1.4)
    else:
        d.box(x, y, w, h, PAPER, RULE, 1.0, 8)
    d.o.append(f'<rect x="{x + 14}" y="{y - 8}" width="{len(label) * 13 + 20}" height="16" fill="{PAPER}"/>')
    d.t(x + 20, y + 4, label, 13, ACC if color is ACC else SOFT, KR, "start", 600)
    if band:
        d.t(x + w - 20, y + 26, band, 12, MUTED, KR, "end")

d.t(440, 250, "새 중괄호 블록을 열 수 없다", 15, ACC, KR, "middle", 600)
d.t(440, 276, "저자가 \"작은 자비\"라 부르는 지점", 12, MUTED)
d.t(440, 302, "여기가 Corefile 문법의 바닥이다", 12, MUTED)

d.t(20, 468, "라벨이 여러 줄에 걸치면 마지막 줄을 뺀 각 줄의 끝 라벨은 쉼표로 닫는다", 13, MUTED, KR, "start")
d.t(20, 490, "주석은 # 로 시작해 줄 끝까지 가고, 정의는 관례상 탭으로 들여쓰지만 강제는 아니다", 13, MUTED, KR, "start")

d.legend(510, [("더 들어갈 수 없는 층", ACC)])
d.save("03-01.corefile-nesting.svg")
