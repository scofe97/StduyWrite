# 14-03.nested-deadline — 자식 context 에 3초를 줘도 부모 2초가 끝나면 자식도 끝난다
# 본문 요구(14-03 §1 「자식 context 의 기한은 부모 기한을 넘지 못합니다」): parent 는 2초 WithTimeout, child 는 parent 를 감싼 3초 WithTimeout 이다.
#           child.Done() 을 기다리면 2s 가 찍힌다. 자식에 건 시간 제한은 부모의 시간 제한에 묶인다.
# 타입 스펙: type-gantt — 가로 시간축 0~3초, 막대 둘(parent · child). child 막대는 2초까지 실선, 2~3초는 점선으로 "쓰지 못한 기한".
#           초당 240px, 축 시작 x 216. focal 은 2초 지점의 끝남 표시 하나.
# 사실 출처: Learning Go 2판 14장 「Contexts with Deadlines」 nested_timers, go1.25.1 실행(2026-09-28) — 2s.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 420
AX, PX_PER_S, AY = 216, 240, 180
BH = 40


def xs(sec):
    return AX + int(sec * PX_PER_S)


d = D(W, H, "GANTT · 14-03 §1",
      "자식에 3초를 줘도 부모의 2초에 끝납니다",
      "parent 는 2초 WithTimeout, child 는 parent 를 감싼 3초 WithTimeout 이다. 두 막대는 각자 받은 기한이다. "
      "2초에 parent 가 끝나면 child 도 함께 끝나므로 child 의 2~3초 구간은 쓰이지 못한다. child.Done() 을 기다린 시간은 2s 로 찍힌다.",
      lead="막대 길이는 각자 받은 기한, 점선 구간은 부모 때문에 쓰지 못한 기한입니다.")

for s in range(4):
    x = xs(s)
    d.line(x, AY - 12, x, AY + 2 * (BH + 24) + 8, RULE, 0.8, "2 4")
    d.t(x, AY - 20, f"{s}s", 12, MUTED, MONO, "middle")

rows = [("parent", "WithTimeout(ctx, 2s)", 2, INFO), ("child", "WithTimeout(parent, 3s)", 3, None)]
for i, (name, sub, dur, c) in enumerate(rows):
    y = AY + i * (BH + 24)
    d.t(36, y + 18, name, 14, INK, MONO, "start", 600)
    d.t(36, y + 34, sub, 11, MUTED, MONO, "start")
    if c:
        d.tone(xs(0), y, xs(dur) - xs(0), BH, c, 4, "18", 1.1)
    else:
        d.tone(xs(0), y, xs(2) - xs(0), BH, INFO, 4, "18", 1.1)
        d.o.append(f'<rect x="{xs(2)}" y="{y}" width="{xs(3) - xs(2)}" height="{BH}" rx="4" fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 4"/>')
        d.t((xs(2) + xs(3)) // 2, y + 25, "쓰지 못한 기한", 11, MUTED, KR, "middle")

ex = xs(2)
d.line(ex, AY - 4, ex, AY + 2 * (BH + 24) - 16, ACC, 1.6)
d.tone(ex - 96, AY + 2 * (BH + 24) + 4, 192, 32, ACC, 4, "22", 1.4)
d.t(ex, AY + 2 * (BH + 24) + 25, "<-child.Done() · 2s", 12, ACC, MONO, "middle", 600)

d.legend(364, [("살아 있는 기한", INFO), ("부모에 묶여 끝남", ACC)])
d.save("14-03.nested-deadline.svg")
print("ok 14-03 nested-deadline")
