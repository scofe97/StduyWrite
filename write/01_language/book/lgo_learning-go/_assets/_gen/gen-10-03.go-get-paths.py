# 10-03.go-get-paths — go get ./... 은 소스를 훑어 직접·간접 두 묶음을 적고, 모듈 경로를 넘긴 go get 은 모두 indirect 로 적어 tidy 로 바로잡는다
# 본문 요구(10-03 §1 「money 예제로 go get 을 봅니다」·「모듈 경로를 넘기면 모두 indirect 로 적힙니다」): go get ./... 은 import 를 훑어
#           직접 의존성과 // indirect 묶음을 나눠 적고 go.sum 을 만든다. go.mod 를 되돌린 뒤 모듈 경로를 넘겨 go get 하면 소스를 확인하지 않아
#           모든 줄에 // indirect 가 붙는다. go mod tidy 가 소스를 훑어 앞의 두 묶음 모양으로 되돌린다.
# 타입 스펙: type-process — lanes(go get ./... · go get 모듈 경로) × steps(시작 · 명령 · go.mod 결과). 칸 사이는 수평 화살표,
#           아래 줄 끝에서 위 줄 끝으로 go mod tidy 세로 화살표 하나. 노드 폭 240, stride 320, 줄 간격 152.
# 사실 출처: Learning Go 2판 10장 「Working with Modules」, go1.25.1 로컬 실행(2026-09-27) — tidy 뒤 두 묶음으로 돌아옴.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 476
X0, NW, NS, NH = 60, 240, 320, 72
YS = [152, 304]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(i, j, title, sub, c=None):
    x, y = X0 + j * NS, YS[i]
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW // 2, y + 30, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW // 2, y + 52, sub, 11, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    y = YS[i] + NH // 2
    x1, x2 = X0 + j * NS + NW, X0 + (j + 1) * NS
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) // 2, y - 10, label, 11, MUTED, kr(label), "middle", 600)


d = D(W, H, "PROCESS · 10-03 §1",
      "go get 은 두 가지로 쓰고 tidy 가 표시를 맞춥니다",
      "위 줄은 소스의 import 를 훑는 go get ./... 이다. 직접 쓰는 모듈과 의존성의 의존성을 두 require 묶음으로 나눠 적고 go.sum 에 해시를 남긴다. "
      "아래 줄은 go.mod 를 되돌린 뒤 모듈 경로를 넘긴 go get 이다. 소스를 확인하지 않아 모든 줄에 // indirect 가 붙고, go mod tidy 가 소스를 훑어 위 줄의 모양으로 되돌린다.",
      lead="모듈 경로를 넘기는 쪽은 개별 모듈의 버전을 바꿀 때 씁니다.")

d.t(X0 - 24, YS[0] - 16, "소스를 훑음", 12, MUTED, KR, "start", 600)
d.t(X0 - 24, YS[1] - 16, "모듈 경로를 넘김", 12, MUTED, KR, "start", 600)

node(0, 0, "main.go 의 import", "formatter · decimal", None)
node(0, 1, "go get ./...", "import 를 모두 더함", INFO)
node(0, 2, "require 두 묶음", "직접 · // indirect · go.sum", OK)
harrow(0, 0, "빌드 오류 뒤")
harrow(0, 1, "적음")

node(1, 0, "go.mod 되돌림", "go.sum 지움", None)
node(1, 1, "go get formatter", "go get decimal", INFO)
node(1, 2, "모든 줄 // indirect", "소스를 확인하지 않음", WARN)
harrow(1, 0, "모듈 경로로")
harrow(1, 1, "적음")

cx = X0 + 2 * NS + NW // 2
d.arrow([(cx, YS[1] - 2), (cx, YS[0] + NH + 4)], OK, "ok", 1.3)
d.t(cx + 12, (YS[0] + NH + YS[1]) // 2 + 4, "go mod tidy", 12, OK, MONO, "start", 600)

d.legend(420, [("go 명령", INFO), ("소스와 맞는 go.mod", OK), ("고칠 표시", WARN)])
d.save("10-03.go-get-paths.svg")
print("ok 10-03 go-get-paths")
