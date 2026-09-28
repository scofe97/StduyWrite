# 10-04.major-version — 메이저 버전을 올리는 두 저장 방식: 하위 디렉터리 vN, 또는 옛 코드를 vN-1 브랜치로
# 본문 요구(10-04 §2 「메이저 버전을 올리는 두 방법」): 하위 디렉터리 방식은 모듈 안에 v2 디렉터리를 만들어 코드를 복사하고,
#           브랜치 방식은 옛 코드나 새 코드를 브랜치에 둔다(버전 2 를 만들며 버전 1 코드를 둔 브랜치 이름은 v1). 어느 쪽이든 새 코드의
#           go.mod 모듈 경로와 모든 import 는 /v2 로 끝나고, 새 코드가 있는 곳에 v2.0.0 태그를 단다.
# 타입 스펙: type-tree — 판 둘을 좌우로. 판마다 저장소 뿌리에서 아래로 뻗는 트리, 노드 폭 200·높이 56, 층 간격 104, 직교 연결선.
#           focal 은 두 판의 v2 코드 노드(같은 색). 모듈 경로 example.com/mod 는 설명을 위한 예다.
# 사실 출처: Learning Go 2판 10장 「Versioning Your Module」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 508
PW, PX = [448, 448], [36, 500]
PY, PH = 132, 300
NW, NH = 200, 56


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, name, sub, c=None):
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW // 2, y + 24, name, 13, c or INK, kr(name), "middle", 600)
    d.t(x + NW // 2, y + 44, sub, 11, MUTED, kr(sub), "middle")


def fork(px, py, kids, ky):
    mid = py + NH + (ky - py - NH) // 2
    d.line(px, py + NH, px, mid, SOFT, 1.2)
    d.line(min(kids), mid, max(kids), mid, SOFT, 1.2)
    for kx in kids:
        d.arrow([(kx, mid), (kx, ky - 4)], SOFT, "soft", 1.2)


d = D(W, H, "TREE · 10-04 §2",
      "v2 코드는 하위 디렉터리나 브랜치에 둡니다",
      "하위 호환을 깨는 v2 를 낼 때의 두 저장 방식. 왼쪽 하위 디렉터리 방식은 메인 브랜치의 모듈 안에 v2 디렉터리를 만들어 코드를 복사한다. "
      "오른쪽 브랜치 방식은 새 코드를 메인 브랜치에 두고 옛 코드를 v1 브랜치로 옮긴다. 두 방식 모두 새 코드의 go.mod 모듈 경로와 import 가 /v2 로 끝나고, 새 코드가 있는 곳에 v2.0.0 태그를 단다.",
      lead="example.com/mod 는 설명을 위한 예입니다. 원문은 새 코드를 브랜치에 두는 반대 배치도 허용합니다.")

titles = ["하위 디렉터리 방식", "브랜치 방식"]
for k in range(2):
    d.box(PX[k], PY, PW[k], PH, r=8)
    d.t(PX[k] + 16, PY + 24, titles[k], 13, INK, KR, "start", 600)

# 하위 디렉터리
cx0 = PX[0] + PW[0] // 2
node(cx0 - NW // 2, PY + 48, "메인 브랜치", "module example.com/mod", None)
kids = [PX[0] + 120, PX[0] + PW[0] - 120]
node(kids[0] - NW // 2, PY + 48 + 120, "기존 코드", "v1 · 그대로 둠", None)
node(kids[1] - NW // 2, PY + 48 + 120, "v2/ 디렉터리", "module example.com/mod/v2", OK)
fork(cx0, PY + 48, kids, PY + 48 + 120)
d.t(cx0, PY + PH - 20, "메인 브랜치에 v2.0.0 태그", 12, MUTED, KR, "middle")

# 브랜치
cx1 = PX[1] + PW[1] // 2
node(cx1 - NW // 2, PY + 48, "저장소", "브랜치 둘", None)
kids = [PX[1] + 120, PX[1] + PW[1] - 120]
node(kids[0] - NW // 2, PY + 48 + 120, "v1 브랜치", "옛 코드", WARN)
node(kids[1] - NW // 2, PY + 48 + 120, "메인 브랜치", "module example.com/mod/v2", OK)
fork(cx1, PY + 48, kids, PY + 48 + 120)
d.t(cx1, PY + PH - 20, "새 코드가 있는 브랜치에 v2.0.0 태그", 12, MUTED, KR, "middle")

d.legend(452, [("v2 코드 · 경로가 /v2", OK), ("옛 코드 브랜치", WARN)])
d.save("10-04.major-version.svg")
print("ok 10-04 major-version")
