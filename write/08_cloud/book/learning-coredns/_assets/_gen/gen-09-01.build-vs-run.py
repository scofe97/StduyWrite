# 09-01 §1 — 무엇이 빌드 때 정해지고 무엇이 실행 때 정해지는가.
# 원문 근거: "Plug-ins are not loaded dynamically, but are instead compiled in at build time."
#            / "regardless of the order that directives are listed in the Corefile, the plug-in
#            chain will be built in the order in plugin.cfg"
# 타입 스펙: type-layers — 위에서 아래로 갈수록 늦게 정해지는 결정의 층이고, 각 층이 무엇을
#           정하는지가 행마다 같은 슬롯으로 반복된다. 순서를 정하는 층 하나가 초점이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 556
d = D(W, H, "LEARNING COREDNS · 09-01 §1",
      "두 시점이 각각 무엇을 정하는가",
      "위 두 층은 빌드 때 굳고 아래 두 층은 실행 때 정해진다. 체인의 순서는 빌드 쪽 층이 "
      "정하므로 Corefile 로는 바꿀 수 없다.",
      "주황이 순서를 정하는 층입니다")

SX, SW, RH = 190, 660, 68
ROWS = [
    ("B1", "소스와 태그", "어느 커밋을 빌드하는가", "git checkout", False),
    ("B2", "plugin.cfg", "무엇이 들어가고 어떤 순서로 서는가", "빌드 때 굳는다", True),
    ("R1", "Corefile", "그중 어느 것을 이 블록에서 켜는가", "실행 때 읽는다", False),
    ("R2", "질의", "켜진 체인을 순서대로 지난다", "요청마다", False),
]

for i, (tag, name, mid, right, focal) in enumerate(ROWS):
    y = 130 + i * RH
    if focal:
        d.tone(SX, y, SW, RH, ACC, 0, "12", 1.4)
    else:
        d.box(SX, y, SW, RH, PAPER2 if i % 2 else PAPER, RULE, 1.0, 0)
    d.t(SX + 18, y + 26, tag, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(SX + 18, y + 48, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(SX + 168, y + 42, mid, 12, MUTED, KR, "start")
    d.t(SX + SW - 18, y + 42, right, 11, ACC if focal else MUTED, KR, "end")

# 왼쪽 시점 구분 — 스택 바깥
d.t(58, 152, "BUILD", 9, SOFT, MONO, "start")
d.t(58, 174, "다시 빌드해야", 11, MUTED, KR, "start")
d.t(58, 192, "바뀐다", 11, MUTED, KR, "start")
d.line(40, 266, 176, 266, RULE, 1.0, "4 4")
d.t(58, 296, "RUN", 9, SOFT, MONO, "start")
d.t(58, 318, "고치고 리로드하면", 11, MUTED, KR, "start")
d.t(58, 336, "바뀐다", 11, MUTED, KR, "start")

d.box(20, 420, 840, 56, PAPER, RULE, 0.8)
d.t(36, 444, "설정으로 바꿀 수 있는 것과 없는 것의 경계가 점선 자리다", 12, INK, KR, "start", 600)
d.t(36, 466, "순서를 고치려면 위쪽 층을 건드려야 하고, 그것은 곧 재빌드와 배포다", 11, MUTED, KR, "start")

d.legend(494, [("순서를 정하는 층", ACC)])
d.save("09-01.build-vs-run.svg")
