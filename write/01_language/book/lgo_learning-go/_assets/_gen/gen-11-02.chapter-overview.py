# 11-02.chapter-overview — 린터는 vet → staticcheck → revive 순서로 더하고 golangci-lint 가 묶으며, govulncheck 는 의존성을 본다
# 본문 요구(11-02 「학습 목표」 개념도 문단): 윗줄은 원문이 권하는 린터 도입 순서와 각 도구가 더하는 것(§1~§3),
#           가운데 줄은 golangci-lint 와 그 설정·묶인 도구(§3), 아랫줄은 govulncheck 가 취약점 DB 를 소스와 바이너리에 대조하는 두 방식(§4).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, staticcheck → golangci-lint 세로 화살표 하나.
# 사실 출처: Learning Go 2판 11장 「Using Code-Quality Scanners」「Using govulncheck to Scan for Vulnerable Dependencies」,
#           staticcheck 2026.2.1 · revive 1.17.0 · golangci-lint v2.14.0 · govulncheck v1.8.0 로컬 실행(2026-09-28).
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


d = D(W, H, "ARCHITECTURE · 11-02 OVERVIEW",
      "린터는 코드 모양을, govulncheck 는 의존성을 봅니다",
      "11-02 의 키워드 개념도. 윗줄은 go vet 을 필수로 두고 오탐 적은 staticcheck, 설정 파일로 규칙을 켜는 revive 를 차례로 더하는 도입 순서다. "
      "가운데 줄은 모듈 루트의 .golangci.yml 이 켤 린터를 정하고 golangci-lint 가 ineffassign 같은 50개 넘는 도구를 묶어 돌리는 모습이다. "
      "아랫줄은 govulncheck 가 vuln.go.dev 취약점 데이터베이스를 소스 코드와 바이너리에 대조하는 두 방식이다.",
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


for i, sec in enumerate(("§1~3", "§3", "§4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "go vet", "필수 · 기본 탑재", INFO)
node(0, 1, "staticcheck", "150+ 검사 · 오탐 적음", INFO)
node(0, 2, "revive", "golint 계승 · toml 설정", INFO)
harrow(0, 0, "+ 오탐 적은 검사")
harrow(0, 1, "+ 규칙 켜기")

node(1, 0, ".golangci.yml", "모듈 루트에 커밋")
node(1, 1, "golangci-lint", "50+ 도구 묶음", INFO)
node(1, 2, "ineffassign", "읽지 않는 대입")
harrow(1, 0, "켤 린터 합의")
harrow(1, 1, "묶인 도구의 예")
varrow(0, 1, "도 묶어서 실행")

node(2, 0, "vuln.go.dev", "Go 팀 취약점 DB")
node(2, 1, "govulncheck", "표준 라이브러리까지", ACC)
node(2, 2, "호출 경로", "소스는 줄 · 바이너리는 심볼", OK)
harrow(2, 0, "대조")
harrow(2, 1, "짚어 줌")

d.legend(456, [("도구", INFO), ("의존성 검사", ACC), ("알려 주는 것", OK)])
d.save("11-02.chapter-overview.svg")
print("ok 11-02 overview")
