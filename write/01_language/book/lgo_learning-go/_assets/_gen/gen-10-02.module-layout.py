# 10-02.module-layout — 애플리케이션 모듈은 루트 main 을 최소로 두고 로직을 internal 에, 라이브러리 모듈은 루트를 저장소 이름 패키지로 두고 도구는 cmd 에
# 본문 요구(10-02 §5 「모듈 정리, API 이름 바꾸기, init」): 애플리케이션으로만 쓸 모듈은 루트를 main 패키지로 두고 main 의 코드는 최소로,
#           로직은 모두 internal 에 둔다. 라이브러리 모듈은 루트 패키지 이름을 저장소 이름과 맞추고, 딸린 도구는 cmd/ 아래 바이너리마다
#           디렉터리를 두어 package main 으로 쓴다. 모듈 안에서만 나눌 기호는 internal 에 둔다.
# 타입 스펙: type-tree — 두 트리를 좌우로. 모듈 루트에서 아래로 뻗는 디렉터리 트리, 층 간격 96, 노드 폭 208, 직교 연결선.
#           focal 없음(두 모양을 나란히 비교). 트리의 디렉터리 이름 myapp · mylib · mytool 은 설명을 위한 예다.
# 사실 출처: Learning Go 2판 10장 「Organizing Your Module」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 484
NW, NH = 208, 56
TOP, STEP = 164, 112


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, name, sub, c=None):
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW // 2, y + 24, name, 13, c or INK, MONO, "middle", 600)
    d.t(x + NW // 2, y + 44, sub, 11, MUTED, kr(sub), "middle")


def branch(px, py, kids_x, ky):
    mid = py + NH + (ky - py - NH) // 2
    d.line(px, py + NH, px, mid, SOFT, 1.2)
    d.line(min(kids_x + [px]), mid, max(kids_x + [px]), mid, SOFT, 1.2)
    for kx in kids_x:
        d.arrow([(kx, mid), (kx, ky - 4)], SOFT, "soft", 1.2)


d = D(W, H, "TREE · 10-02 §5",
      "모듈 종류에 따라 패키지를 다르게 둡니다",
      "왼쪽은 애플리케이션으로만 쓰는 모듈이다. 루트는 main 패키지로 두고 코드를 최소로 하며 로직은 internal 에 모아 누구도 구현에 기대지 못하게 한다. "
      "오른쪽은 라이브러리 모듈이다. 루트 패키지 이름을 저장소 이름과 맞추고, 딸린 도구는 cmd 아래 바이너리마다 디렉터리를 두며, 모듈 안에서만 나눌 기호는 internal 에 둔다.",
      lead="myapp · mylib · mytool 은 설명을 위한 예입니다.")

d.t(252, 132, "애플리케이션 모듈", 13, MUTED, KR, "middle", 600)
d.t(732, 132, "라이브러리 모듈", 13, MUTED, KR, "middle", 600)
d.line(492, 124, 492, 420, RULE, 0.8, "3 5")

# 애플리케이션
ax = 252 - NW // 2
node(ax, TOP, "myapp/", "package main · 최소 코드", None)
node(ax, TOP + STEP, "internal/", "로직 전부", INFO)
branch(252, TOP, [252], TOP + STEP)

# 라이브러리
lx = 732 - NW // 2
node(lx, TOP, "mylib/", "package mylib · 저장소 이름", OK)
kids = [620, 844]
node(kids[0] - NW // 2, TOP + STEP, "cmd/mytool/", "package main · 도구", WARN)
node(kids[1] - NW // 2, TOP + STEP, "internal/", "모듈 안에서만 공유", INFO)
branch(732, TOP, kids, TOP + STEP)

d.t(252, TOP + STEP + NH + 40, "main 은 internal 을 부르기만 함", 12, MUTED, KR, "middle")
d.t(732, TOP + STEP + NH + 40, "import 이름과 패키지 이름이 같음", 12, MUTED, KR, "middle")

d.legend(428, [("공개 루트 패키지", OK), ("감춘 코드", INFO), ("바이너리", WARN)])
d.save("10-02.module-layout.svg")
print("ok 10-02 module-layout")
