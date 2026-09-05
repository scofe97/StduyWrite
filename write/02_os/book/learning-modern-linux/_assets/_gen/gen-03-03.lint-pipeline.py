# 03-03 §6 — 스크립트를 저장소에 넣기까지 거치는 손과 도구.
# 원문("Linting and Testing Scripts"): "While you're developing, you want to check and lint your scripts,
#       making sure that you're using commands and instructions correctly ... with the program ShellCheck;
#       you can download and install it locally, or you can also use the online version via shellcheck.net.
#       Also, consider formatting your script with shfmt. It automatically fixes issues that can be
#       reported later by shellcheck."
#       "And further, before you check your script into a repo, consider using bats to test it. bats,
#       short for Bash Automated Testing System, allows you to define test files as a bash script with
#       special syntax for test cases. Each test case is simply a bash function with a description, and
#       you would typically invoke these scripts as part of a CI pipeline—for example, as a GitHub action."
# 타입 스펙: type-swimlane — 역할을 가로지르며 넘겨받는 절차. 레인은 사람 · 로컬 도구 · 저장소와 CI.
#           accent 는 저자가 저장소에 넣기 전에 하라고 못 박은 한 칸.
#           축약: 가로 슬롯을 넷으로 줄였다. 여섯이면 슬롯 폭이 100px 아래로 내려가 한글이 뭉갠다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 580
LANE_X, LANE_W = 16, 168
TRACK_X = LANE_X + LANE_W + 12
LANE_H, LANE_GAP, LANE_Y0 = 104, 12, 132
SLOT_W, SLOT_GAP, SLOT_H = 156, 12, 76

lanes = [
    ("사람", "손으로 하는 일", INFO),
    ("로컬 도구", "치기 전에 붙이는 것", MUTED),
    ("저장소와 CI", "넣은 뒤 도는 것", OK),
]
steps = [
    (0, 0, "스크립트를 쓴다", ["좋은 관례를 적용하며"], False),
    (1, 1, "shellcheck · shfmt", ["검사하고", "포맷을 자동으로 고친다"], False),
    (1, 2, "bats", ["저장소에 넣기 전에", "테스트한다"], True),
    (2, 3, "저장소와 CI", ["GitHub action 으로", "다시 돈다"], False),
]

d = D(W, H, "LEARNING MODERN LINUX · 03-03 §6",
      "저장소에 넣기 전에 거치는 손과 도구",
      "스크립트가 사람의 손에서 저장소와 CI 로 넘어가기까지의 절차를 역할 레인으로 가른 것. "
      "저자가 순서를 못 박은 자리는 테스트를 저장소에 넣기 전에 두라는 대목이다.",
      "shfmt 가 고친 것은 나중에 shellcheck 가 보고할 일을 미리 없앱니다")


def slot_x(i):
    return TRACK_X + i * (SLOT_W + SLOT_GAP)


for li, (name, sub, c) in enumerate(lanes):
    y = LANE_Y0 + li * (LANE_H + LANE_GAP)
    d.box(LANE_X, y, LANE_W, LANE_H, PAPER2, c, 1.0, 6)
    d.t(LANE_X + 16, y + 44, name, 14, c, KR, "start", 600)
    d.t(LANE_X + 16, y + 66, sub, 12, MUTED, KR, "start")
    if li < len(lanes) - 1:
        d.line(TRACK_X - 4, y + LANE_H + LANE_GAP / 2, W - 20,
               y + LANE_H + LANE_GAP / 2, RULE, 0.8)

for li, si, title, subs, focal in steps:
    y = LANE_Y0 + li * (LANE_H + LANE_GAP) + 14
    x = slot_x(si)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SLOT_W}" height="{SLOT_H}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SLOT_W, SLOT_H, PAPER, RULE, 1.0, 6)
    d.t(x + SLOT_W / 2, y + 26, title, 13, ACC if focal else INK,
        MONO if all(ord(ch) < 128 or ch == "·" or ch == " " for ch in title) else KR,
        "middle", 600)
    for k, part in enumerate(subs):
        d.t(x + SLOT_W / 2, y + 48 + k * 18, part, 12, MUTED, KR)

for a, b in zip(steps, steps[1:]):
    ya = LANE_Y0 + a[0] * (LANE_H + LANE_GAP) + 52
    yb = LANE_Y0 + b[0] * (LANE_H + LANE_GAP) + 52
    xa = slot_x(a[1]) + SLOT_W
    xb = slot_x(b[1])
    c = ACC if b[4] else MUTED
    mk = "acc" if b[4] else "ar"
    if a[0] == b[0]:
        d.path(f"M {xa + 4} {ya} L {xb - 8} {yb}", c, 1.4, m=mk)
    else:
        mid = xa + 6
        d.path(f"M {xa + 4} {ya} L {mid} {ya} L {mid} {yb} L {xb - 8} {yb}", c, 1.4, m=mk)

d.t(20, 496, "bats 는 Bash Automated Testing System 의 줄임말이고, 테스트 파일을 특별한 문법의 "
             "bash 스크립트로 정의합니다.", 12, MUTED, KR, "start")
d.t(20, 518, "테스트 케이스 하나가 설명이 붙은 bash 함수 하나입니다.", 12, SOFT, KR, "start")

d.legend(536, [("사람의 손", INFO), ("로컬 도구", MUTED),
               ("저장소 전에 두라는 자리", ACC), ("저장소와 CI", OK)])
d.save("03-03.lint-pipeline.svg")
print("ok 03-03.lint-pipeline")
