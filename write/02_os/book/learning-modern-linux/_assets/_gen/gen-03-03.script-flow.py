# 03-03 §7 — gh-user-info.sh 가 실제로 밟는 경로와 저자가 남긴 숙제.
# 원문("End-to-End Example: GitHub User Info Script"): 스크립트는 기본값을 두고
#       `targetuser="${1:-mhausenblas}"`, 의존성을 검사하고 `if ! [ -x "$(command -v jq)" ]` 이면
#       "jq is not installed" 를 stderr 로 내고 `exit 1`, 그다음 curl 로 GitHub API 를 받아 임시 파일에
#       담고, jq 로 .name 과 .created_at 을 뽑고, cut 으로 연도를 잘라 한 줄을 출력한다.
#       실행 결과는 "Michael Hausenblas joined GitHub in 2009".
#       저자가 마지막에 남긴 개선점 넷 — JSON 이 유효하지 않거나 500 이 오는 경우, 네트워크가 없는 경우,
#       curl 이 설치돼 있다고 암묵적으로 가정한 점, -h/--help 로 사용법을 보이는 것.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. accent 는 저자가 유일하게 넣어 둔 검사.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 712
d = D(W, H, "LEARNING MODERN LINUX · 03-03 §7",
      "예제 스크립트가 밟는 길과 밟지 않는 길",
      "저자의 gh-user-info.sh 를 흐름으로 편 것. 왼쪽이 실제 구현된 경로이고, "
      "오른쪽 회색 칸이 저자가 스스로 남겨 둔 네 가지 숙제다.",
      "검사가 하나뿐이라는 것이 이 예제의 교육적 요점입니다")


def oval(x, y, w, h, txt, c=MUTED):
    d.box(x, y, w, h, PAPER2, c, 1.1, r=20)
    d.t(x + w / 2, y + h / 2 + 5, txt, 13, INK)


def step(x, y, w, h, txt, sub=None, c=RULE):
    d.box(x, y, w, h, PAPER2, c, 1.0, r=6)
    d.t(x + w / 2, y + (24 if sub else h / 2 + 5), txt, 13, INK)
    if sub:
        d.t(x + w / 2, y + 44, sub, 12, MUTED, MONO)


def dia(cx, cy, w, h, txt):
    d.o.append(f'<path d="M {cx} {cy - h / 2} L {cx + w / 2} {cy} '
               f'L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z" '
               f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    d.t(cx, cy + 5, txt, 13, ACC)


CX = 268
oval(CX - 140, 100, 280, 40, "./gh-user-info.sh [handle]")

step(CX - 140, 168, 280, 60, "기본값을 채운다", '${1:-mhausenblas}', RULE)
d.arrow([(CX, 140), (CX, 168)], MUTED, "ar", 1.2)

dia(CX, 288, 300, 68, "jq 가 있나")
d.arrow([(CX, 228), (CX, 254)], MUTED, "ar", 1.2)

step(600, 258, 248, 60, "메시지 내고 종료", 'exit 1', BAD)
d.arrow([(CX + 150, 288), (596, 288)], BAD, "bad", 1.4)
d.t(480, 278, "없다", 12, BAD, KR)

step(CX - 140, 372, 280, 60, "curl 로 API 를 받는다", "/tmp 에 담는다", OK)
d.arrow([(CX, 322), (CX, 372)], OK, "ok", 1.2)
d.t(CX + 14, 354, "있다", 12, OK, KR, "start")

step(CX - 140, 460, 280, 60, "jq 로 두 필드를 뽑는다", ".name · .created_at", OK)
d.arrow([(CX, 432), (CX, 460)], OK, "ok", 1.2)

step(CX - 140, 548, 280, 60, "cut 으로 연도를 자른다", "2009-02-07T16:07:32Z", OK)
d.arrow([(CX, 520), (CX, 548)], OK, "ok", 1.2)

d.box(600, 372, 248, 236, PAPER, WARN, 1.0, 6)
d.t(724, 400, "저자가 남긴 숙제 넷", 13, WARN, KR, "middle", 600)
for k, line in enumerate(["JSON 이 깨졌거나 500 이면",
                          "네트워크가 없으면",
                          "curl 이 없으면 wget 으로",
                          "-h 로 사용법 보이기"]):
    d.t(620, 432 + k * 26, line, 12, MUTED, KR, "start")
d.t(620, 552, "어느 것도 지금 코드에는", 12, SOFT, KR, "start")
d.t(620, 572, "들어 있지 않습니다", 12, SOFT, KR, "start")

d.t(20, 640, "출력은 Michael Hausenblas joined GitHub in 2009 한 줄입니다.", 12, SOFT, KR, "start")
d.legend(660, [("검사가 있는 자리", ACC), ("실패 경로", BAD),
               ("정상 경로", OK), ("빠진 검사", WARN)])
d.save("03-03.script-flow.svg")
print("ok 03-03.script-flow")
