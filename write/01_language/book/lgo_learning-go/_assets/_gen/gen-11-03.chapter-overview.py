# 11-03.chapter-overview — 지원 파일은 //go:embed 로 바이너리에, 숨김 파일은 dir/* · all: 로, 코드는 //go:generate 로 만들어 커밋한다
# 본문 요구(11-03 「학습 목표」 개념도 문단): 윗줄은 지원 파일이 //go:embed 를 거쳐 패키지 수준 변수에 담기고 단일 바이너리가 되는 길(§1),
#           가운데 줄은 숨김 파일을 넣는 두 패턴(§2), 아랫줄은 //go:generate 주석이 도구를 불러 만든 코드를 커밋하는 길(§3~§4).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표만.
# 사실 출처: Learning Go 2판 11장 「Embedding Content into Your Program」「Embedding Hidden Files」「Using go generate」
#           「Working with go generate and Makefiles」, go1.25.1 로컬 실행(2026-09-28).
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


d = D(W, H, "ARCHITECTURE · 11-03 OVERVIEW",
      "파일은 embed 로, 코드는 generate 로 빌드 앞에 준비합니다",
      "11-03 의 키워드 개념도. 윗줄은 지원 파일이 //go:embed 주석을 거쳐 string, []byte, embed.FS 타입의 패키지 수준 변수에 담기고 컴파일 때 단일 바이너리에 들어가는 길이다. 가운데 줄은 기본으로 빠지는 숨김 파일을 dir/* 는 맨 위 디렉터리만, all:dir 는 모든 하위 디렉터리까지 넣는다는 것이다. 아랫줄은 //go:generate 주석을 go generate 가 읽어 protoc 나 stringer 를 실행하고, 만든 소스 코드를 커밋하는 길이다.",
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




for i, sec in enumerate(("§1", "§2", "§3~4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "지원 파일", "txt · 템플릿 · 바이너리")
node(0, 1, "패키지 수준 변수", "string · []byte · embed.FS", INFO)
node(0, 2, "단일 바이너리", "파일 없이 배포", OK)
harrow(0, 0, "//go:embed", ACC, "acc")
harrow(0, 1, "컴파일 때 포함")

node(1, 0, "숨김 파일", ". 이나 _ 로 시작")
node(1, 1, "dir/*", "맨 위 숨김만")
node(1, 2, "all:dir", "모든 하위 숨김까지")
harrow(1, 0, "기본 제외 · 넣으려면")
harrow(1, 1, "하위까지 넓히면")

node(2, 0, "//go:generate", "주석에 적은 명령")
node(2, 1, "protoc · stringer", "go generate 가 실행", INFO)
node(2, 2, "생성 코드", ".pb.go · _string.go · 커밋", OK)
harrow(2, 0, "go generate ./...", ACC, "acc")
harrow(2, 1, "소스 코드 생성")

d.legend(456, [("변수·도구", INFO), ("매직 주석", ACC), ("남는 산출물", OK)])
d.save("11-03.chapter-overview.svg")
print("ok 11-03 overview")
