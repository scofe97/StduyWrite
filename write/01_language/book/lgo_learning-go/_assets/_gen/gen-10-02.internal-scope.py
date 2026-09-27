# 10-02.internal-scope — foo/internal 을 import 할 수 있는 범위는 foo 를 뿌리로 하는 트리 전체다
# 본문 요구(10-02 §4 「internal 로 감추고 순환 의존을 피합니다」의 원문 정오): go doc cmd/go 는 internal 을 "부모 디렉터리를
#           뿌리로 하는 트리 안의 코드"만 import 할 수 있다고 정의한다. foo·sibling 뿐 아니라 sibling/deep 도 되고, 루트와 bar 는 안 된다.
# 타입 스펙: type-tree — 모듈 루트에서 아래로 뻗는 디렉터리 트리. 층 간격 96, 노드 폭 176, 직교 연결선.
#           foo 를 뿌리로 하는 하위 트리를 점선 영역으로 감싸 허용 범위를 보인다. focal 은 internal 노드 하나.
# 사실 출처: Learning Go 2판 10장 「Using the internal Package」, go1.25.1 go build(2026-09-27) — foo/sibling/deep 허용,
#           bar 는 use of internal package ... not allowed. sibling/deep 은 노트가 더한 디렉터리다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 600
NW, NH = 176, 52


def node(x, y, title, sub, c):
    d.tone(x, y, NW, NH, c, 6, "22" if c == ACC else "14", 1.4 if c == ACC else 1.0)
    d.t(x + NW // 2, y + 23, title, 13, c if c != SOFT else MUTED, MONO, "middle", 600)
    d.t(x + NW // 2, y + 42, sub, 11, MUTED, KR, "middle")


def link(x1, y1, x2, y2):
    my = (y1 + y2) // 2
    d.path(f"M {x1} {y1} L {x1} {my} L {x2} {my} L {x2} {y2}", SOFT, 1.2)


d = D(W, H, "TREE · 10-02 §4",
      "internal 패키지를 import 할 수 있는 범위",
      "foo/internal 은 부모인 foo 를 뿌리로 하는 트리 안의 코드만 import 할 수 있다. foo 자신, 형제 sibling, 그 아래 sibling/deep 까지 허용되고, "
      "트리 밖인 모듈 루트와 bar 는 use of internal package not allowed 로 막힌다. 원문은 직계 부모와 형제만이라고 적었지만 규칙은 더 넓다.",
      lead="점선 안이 foo 를 뿌리로 하는 트리입니다. sibling/deep 은 노트가 더해 확인한 디렉터리입니다.")

root = (404, 112)
node(*root, "모듈 루트", "example.go · 거부", BAD)
L1 = 224
foo = (224, L1)
bar = (680, L1)
node(*bar, "bar", "bar.go · 거부", BAD)
L2 = 336
internal = (48, L2)
sibling = (400, L2)
L3 = 448
deep = (400, L3)
d.o.append(f'<rect x="32" y="{L1 - 16}" width="560" height="{L3 + NH + 16 - (L1 - 16)}" rx="10" fill="none" stroke="{OK}" stroke-width="1.2" stroke-dasharray="6 5"/>')
d.t(44, L3 + NH + 4, "foo 를 뿌리로 하는 트리 · import 허용", 12, OK, KR, "start", 600)
node(*foo, "foo", "foo.go · 허용", OK)
node(*internal, "foo/internal", "Doubler", ACC)
node(*sibling, "foo/sibling", "sibling.go · 허용", OK)
node(*deep, "foo/sibling/deep", "deep.go · 허용", OK)
link(root[0] + NW // 2, root[1] + NH, foo[0] + NW // 2, foo[1])
link(root[0] + NW // 2, root[1] + NH, bar[0] + NW // 2, bar[1])
link(foo[0] + NW // 2, foo[1] + NH, internal[0] + NW // 2, internal[1])
link(foo[0] + NW // 2, foo[1] + NH, sibling[0] + NW // 2, sibling[1])
link(sibling[0] + NW // 2, sibling[1] + NH, deep[0] + NW // 2, deep[1])

d.legend(548, [("import 허용", OK), ("import 거부", BAD), ("internal 패키지", ACC)])
d.save("10-02.internal-scope.svg")
print("ok 10-02 internal-scope")
