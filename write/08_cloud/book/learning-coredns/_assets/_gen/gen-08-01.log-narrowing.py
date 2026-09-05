# 08-01 §3 — log 를 좁히는 축 셋. 앞의 둘은 줄 수를, 마지막은 줄 길이를 줄인다.
# 원문 근거: "NAMES is a list of domains for which queries are logged; queries for domain names
#            that don't end in one of the listed domains are not logged." / "You can even specify
#            that only queries that generated certain 'classes' of responses be logged."
#            / "the log plug-in provides a remarkable amount of control over the format"
# 타입 스펙: type-nested — 바깥에서 안으로 갈수록 남는 것이 줄어드는 포함 관계다.
#           세 손잡이가 순서대로 좁히는 동심 구조라 중첩으로만 그 순서가 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 606
d = D(W, H, "LEARNING COREDNS · 08-01 §3",
      "세 손잡이가 각각 다른 축을 좁힌다",
      "바깥이 아무것도 걸지 않은 상태이고 안으로 갈수록 남는 로그가 줄어든다. "
      "앞의 두 손잡이는 줄 수를 줄이고 가장 안쪽 손잡이는 줄 길이를 줄인다.",
      "주황이 줄 수가 아니라 줄 길이를 줄이는 자리입니다")

# 중첩 간격은 58px — 부제 글자(상단 +48)가 다음 상자 테두리를 걸터앉지 않게 한다.
BOXES = [
    (40, 96, 760, 350, "모든 질의", "log — 손잡이 없음 · 받는 질의마다 한 줄", False),
    (100, 154, 640, 264, "NAMES 로 거른 질의", "log foo.example bar.example", False),
    (160, 212, 520, 176, "class 로 거른 응답", "class denial error", False),
    (220, 270, 400, 96, "형식으로 줄인 한 줄", '"Query: {name} {class} {type}"', True),
]

for x, y, w, h, title, sub, focal in BOXES:
    if focal:
        d.tone(x, y, w, h, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER if y == 96 else PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 48, sub, 11, ACC if focal else MUTED, MONO, "start")

d.t(238, 342, "여기서 남는 것이 최종 로그다", 11, ACC, KR, "start")

# 오른쪽 축 — 무엇이 줄어드는가. 바깥 상자(40..800) 밖에 둔다.
d.t(824, 170, "줄 수", 11, MUTED, KR)
d.arrow([(824, 186), (824, 256)], MUTED, "ar", 1.3)
d.t(824, 288, "줄 길이", 11, ACC, KR)
d.arrow([(824, 304), (824, 360)], ACC, "acc", 1.3)

d.box(20, 462, 840, 62, PAPER, RULE, 0.8)
d.t(36, 486, "셋은 서로 다른 질문에 답한다", 12, INK, KR, "start", 600)
d.t(36, 508, "NAMES 는 어느 도메인을 · class 는 어떤 결과를 · 형식 문자열은 한 줄에 무엇을 적을지를 고른다",
     11, MUTED, KR, "start")

d.legend(544, [("줄 길이를 줄이는 손잡이", ACC), ("줄 수를 줄이는 손잡이", MUTED)])
d.save("08-01.log-narrowing.svg")
