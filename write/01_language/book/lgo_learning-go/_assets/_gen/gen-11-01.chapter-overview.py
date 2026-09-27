# 11-01.chapter-overview — go run 은 임시로 빌드해 지우고, go install 은 GOBIN 에 남기며, goimports 는 그렇게 설치한 도구다
# 본문 요구(11-01 「학습 목표」 개념도 문단): 윗줄은 go run 의 길(§1), 가운데 줄은 모듈 경로와 버전에서 GOBIN 까지의 go install 길(§2),
#           아랫줄은 go install 로 설치한 도구의 예인 goimports(§3). 두 길의 차이는 바이너리가 남느냐다.
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자, 행 안은 가로 화살표, 행 사이는 세로 화살표 하나.
#           관계 라벨은 화살표 위(가로) 또는 오른쪽(세로)에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: Learning Go 2판 11장 「Using go run to Try Out Small Programs」「Adding Third-Party Tools with go install」
#           「Improving Import Formatting with goimports」, go1.25.1 로컬 실행(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 520


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 11-01 OVERVIEW",
      "go run 은 지우고 go install 은 남깁니다",
      "11-01 의 키워드 개념도. 윗줄은 hello.go 를 임시 디렉터리에서 빌드해 실행하고 끝나면 바이너리를 지우는 go run 의 길이다. "
      "가운데 줄은 모듈 경로@버전을 받아 빌드해 GOBIN(기본 ~/go/bin)에 설치하는 go install 의 길이다. "
      "아랫줄의 goimports 는 go install 로 설치한 도구의 예로, go fmt 에 import 정리를 더한다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != SOFT else MUTED, kr(label), "middle", 600)


def varrow(i, j, label):
    x = nx(j) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    d.arrow([(x, y1 + 2), (x, y2 - 4)], SOFT, "soft", 1.3)
    d.t(x + 10, (y1 + y2) / 2 + 4, label, 11, MUTED, kr(label), "start", 600)


for i, sec in enumerate(("§1", "§2", "§3")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "hello.go", "소스 파일 하나")
node(0, 1, "go run", "빌드 + 실행 한 번에", INFO)
node(0, 2, "바이너리 삭제", "디렉터리엔 hello.go 만", WARN)
harrow(0, 0, "임시 디렉터리에 빌드")
harrow(0, 1, "프로그램 종료 후")

node(1, 0, "경로@버전", "@latest 도 가능")
node(1, 1, "go install", "프록시·저장소에서 받아 빌드", INFO)
node(1, 2, "GOBIN", "기본 ~/go/bin · PATH 에 추가", OK)
harrow(1, 0, "@버전 필수", ACC, "acc")
harrow(1, 1, "바이너리 설치")

node(2, 0, "go fmt", "포맷만 고침")
node(2, 1, "goimports", "-l -w .")
node(2, 2, "import 정리", "정렬 · 삭제 · 추측")
harrow(2, 0, "+ import 정리")
harrow(2, 1, "현재 트리 전체")
varrow(1, 1, "로 설치한 도구의 예")

d.legend(456, [("Go 명령", INFO), ("남지 않음", WARN), ("남음", OK), ("빼면 안 되는 것", ACC)])
d.save("11-01.chapter-overview.svg")
print("ok 11-01 overview")
