# 02-01.framing — 같은 바이트 흐름을 두 약속으로 자르기
# 본문 요구(02-01 §1 「경계가 필요하면 앱이 프레이밍합니다」):
#           구분값은 \n 자리에서, 길이 접두는 길이 칸이 가리키는 만큼 자른다.
#           본문에 \n 이 섞이면 구분값은 메시지 하나를 둘로 쪼갠다.
# 타입 스펙: type-flowchart — 세 줄의 바이트 칸 나열 + 자르는 자리 표시. focal 은 잘못 쪼개지는 셋째 줄.
# 사실 출처: 02-01 Phase 1 문답(질문 1-5, 1-6).
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, MONO, KR

W, H = 960, 452
X0, CW, STEP, CH = 190, 40, 46, 38

d = D(W, H, "FLOWCHART · 02-01 FRAMING", "같은 바이트 흐름을 두 약속으로 자르기",
      "구분값 방식은 줄바꿈이 나온 자리에서 메시지를 자르고, 길이 접두 방식은 앞의 길이 칸이 가리키는 바이트 수만큼 "
      "자른다. 본문 안에 줄바꿈이 들어 있으면 구분값 방식은 메시지 하나를 둘로 잘못 쪼갠다.",
      lead="초록 선은 맞게 자른 자리, 빨간 선은 본문 한가운데를 자른 자리입니다.")


def row(y, label, cells, cuts, cut_c, results):
    d.t(24, y + 24, label, 13, MUTED, KR, "start", 600)
    for i, (txt, c) in enumerate(cells):
        x = X0 + i * STEP
        if c:
            d.tone(x, y, CW, CH, c, 5, "10", 1.1)
            d.t(x + CW / 2, y + 24, txt, 13, c, MONO, "middle", 600)
        else:
            d.box(x, y, CW, CH)
            d.t(x + CW / 2, y + 24, txt, 13, INK, MONO, "middle", 600)
    for k in cuts:
        cx = X0 + k * STEP - 3
        d.line(cx, y - 8, cx, y + CH + 8, cut_c, 2.2)
    d.t(X0 + len(cells) * STEP + 14, y + 24, results, 12, cut_c, MONO, "start", 600)


NL = "\\n"
row(118, "구분값 \\n", [(c, None) for c in "hello"] + [(NL, OK)] + [(c, None) for c in "world"] + [(NL, OK)],
    [6, 12], OK, "hello | world")
row(214, "길이 접두", [("5", OK)] + [(c, None) for c in "hello"] + [("5", OK)] + [(c, None) for c in "world"],
    [6, 12], OK, "hello | world")
row(310, "구분값, 본문에 \\n", [(c, None) for c in "line1"] + [(NL, BAD)] + [(c, None) for c in "line2"] + [(NL, OK)],
    [6], BAD, "line1 | line2")
d.line(X0 + 12 * STEP - 3, 302, X0 + 12 * STEP - 3, 356, OK, 2.2)
d.t(X0 + 6 * STEP - 3, 372, "한 메시지가 둘로", 12, BAD, KR, "middle")

d.legend(404, [("경계 표시 칸", OK), ("본문 속 \\n 이 만든 가짜 경계", BAD)])
d.save("02-01.framing.svg")
print("ok framing")
