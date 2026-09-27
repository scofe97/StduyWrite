# 11-04.chapter-overview — go build 는 빌드 정보를 바이너리에 남기고, GOOS·GOARCH 와 파일 이름·빌드 태그가 대상과 파일을 고르며, golang.org/dl 로 옛 Go 를 시험한다
# 본문 요구(11-04 「학습 목표」 개념도 문단): 윗줄은 빌드 정보를 go version -m 과 govulncheck 가 읽는 길(§1),
#           가운데 두 줄은 GOOS·GOARCH 가 대상 플랫폼을 정하고 파일 이름 접미사와 //go:build 가 파일을 고르는 길(§2~§3),
#           아랫줄은 golang.org/dl 로 다른 Go 버전을 설치해 시험하는 길(§4).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 교차 컴파일 → 빌드 태그 세로 화살표 하나.
# 사실 출처: Learning Go 2판 11장 「Reading the Build Info Inside a Go Binary」「Building Go Binaries for Other Platforms」
#           「Using Build Tags」「Testing Versions of Go」, go1.25.1 로컬 실행(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 648


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 11-04 OVERVIEW",
      "빌드 정보는 바이너리에 남고, 대상은 환경 변수와 파일 선택이 정합니다",
      "11-04 의 키워드 개념도. 윗줄은 go build 가 모든 바이너리에 모듈 버전, 빌드 설정, vcs 리비전을 기록하고 go version -m 과 govulncheck -mode binary 가 그것을 읽는 길이다. 둘째 줄은 GOOS 와 GOARCH 로 대상 플랫폼을 정해 교차 컴파일하는 길이고, 셋째 줄은 파일 이름 접미사와 //go:build 태그가 그 대상에 들어갈 파일을 고르는 길이다. 아랫줄은 golang.org/dl 로 go1.19.2 를 ~/sdk 에 받아 시험하고 지우는 길이다.",
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




for i, sec in enumerate(("§1", "§2", "§3", "§4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "go build", "모든 바이너리에", INFO)
node(0, 1, "빌드 정보", "모듈 버전 · 설정 · vcs 리비전", OK)
node(0, 2, "go version -m", "govulncheck -mode binary")
harrow(0, 0, "자동으로 기록")
harrow(0, 1, "읽어서 점검")

node(1, 0, "GOOS · GOARCH", "기본은 지금 컴퓨터")
node(1, 1, "교차 컴파일", "linux/amd64 · windows/arm64", INFO)
node(1, 2, "대상용 바이너리", "ELF · PE32+ · file 로 확인", OK)
harrow(1, 0, "대상 플랫폼 지정")
harrow(1, 1, "기계어로 빌드")
varrow(1, 1, "플랫폼마다 다른 코드")

node(2, 0, "파일 이름 접미사", "_windows_arm64.go")
node(2, 1, "//go:build", "&& · || · ! · -tags", ACC)
node(2, 2, "빌드에 들 파일", "대상·태그에 맞는 것만")
harrow(2, 0, "+ 세밀한 조건")
harrow(2, 1, "파일 선택")

node(3, 0, "golang.org/dl", "go1.19.2@latest")
node(3, 1, "go1.19.2", "~/sdk/go1.19.2", INFO)
node(3, 2, "옛 버전 시험", "끝나면 sdk · go/bin 삭제")
harrow(3, 0, "download")
harrow(3, 1, "go1.19.2 build")

d.legend(584, [("Go 명령·환경", INFO), ("바이너리에 남는 것", OK), ("매직 주석", ACC)])
d.save("11-04.chapter-overview.svg")
print("ok 11-04 overview")
