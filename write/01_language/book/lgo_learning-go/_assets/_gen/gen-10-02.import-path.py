# 10-02.import-path — import 경로는 모듈 경로 + 패키지 디렉터리이고, 코드에서 부르는 이름은 그 디렉터리 파일의 package 절이 정한다
# 본문 요구(10-02 §1 「패키지를 만들고 가져옵니다」·「패키지 이름은 패키지 절이 정합니다」): import 경로
#           "github.com/learning-go-book-2e/package_example/do-format" 는 모듈 경로와 모듈 안의 경로 /do-format 로 되어 있고,
#           그 디렉터리의 formatter.go 는 package format 이라 main 은 format.Number 로 부른다.
# 타입 스펙: type-architecture — 왼→오른 노드 넷(import 경로 · 디렉터리 · package 절 · 부르는 코드), 직교 화살표만.
#           노드 폭 176, stride 248, 위에 import 경로 문자열을 두 구간(모듈 경로 · 패키지 경로)으로 나눈 띠. focal 은 package 절 노드.
# 사실 출처: Learning Go 2판 10장 「Creating and Accessing a Package」·「Naming Packages」 package_example, 실행 결과 The number is 4.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 420
NX0, NW, NS, NY, NH = 36, 176, 248, 244, 88


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 10-02 §1",
      "import 경로는 디렉터리를, 부르는 이름은 package 절을 따릅니다",
      "main.go 가 import 한 경로는 go.mod 의 모듈 경로 github.com/learning-go-book-2e/package_example 에 모듈 안의 디렉터리 /do-format 을 붙인 것이다. "
      "그 디렉터리의 formatter.go 첫 줄이 package format 이므로 main 은 do-format 이 아니라 format.Number 로 부른다.",
      lead="디렉터리 이름 do-format 은 Go 식별자가 될 수 없어서 package 절이 format 으로 바꿨습니다.")

# import 경로 띠: 모듈 경로 | 패키지 경로
BX, BY, BW1, BW2, BH = 36, 128, 640, 272, 44
d.box(BX, BY, BW1, BH, r=4)
d.t(BX + 16, BY + 28, "github.com/learning-go-book-2e/package_example", 13, INK, MONO, "start", 600)
d.tone(BX + BW1, BY, BW2, BH, INFO, 4, "14", 1.0)
d.t(BX + BW1 + 16, BY + 28, "/do-format", 13, INFO, MONO, "start", 600)
d.t(BX + BW1 // 2, BY + BH + 20, "모듈 경로 · go.mod 의 module 줄", 12, MUTED, KR, "middle")
d.t(BX + BW1 + BW2 // 2, BY + BH + 20, "모듈 안의 패키지 경로", 12, MUTED, KR, "middle")

nodes = [("import 경로", ".../do-format", None),
         ("디렉터리", "formatter.go", INFO),
         ("package 절", "package format", ACC),
         ("부르는 코드", "format.Number(num)", OK)]
labels = ["가리킴", "첫 줄", "이 이름으로"]
for k, (title, sub, c) in enumerate(nodes):
    x = NX0 + k * NS
    if c:
        d.tone(x, NY, NW, NH, c, 6, "14" if c != ACC else "18", 1.1 if c != ACC else 1.4)
    else:
        d.box(x, NY, NW, NH)
    d.t(x + NW // 2, NY + 34, title, 14, c or INK, KR, "middle", 600)
    d.t(x + NW // 2, NY + 58, sub, 11, MUTED, MONO, "middle")
    if k < 3:
        y = NY + NH // 2
        d.arrow([(x + NW + 2, y), (x + NS - 4, y)], SOFT, "soft", 1.3)
        d.t(x + NW + (NS - NW) // 2, y - 10, labels[k], 11, MUTED, KR, "middle", 600)

d.legend(364, [("디렉터리", INFO), ("이름을 정하는 곳", ACC), ("코드에서 쓰는 모양", OK)])
d.save("10-02.import-path.svg")
print("ok 10-02 import-path")
