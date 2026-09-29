# 16-04.chapter-overview — Go 가 C 를 부르고 C 가 export 한 Go 를 부르며, 포인터를 품은 값은 Handle 로 건너가고, cgo 호출 비용은 1.26 에서 줄었어도 여전히 크다
# 본문 요구(16-04 「학습 목표」 개념도 문단): 첫 줄 Go→C(§1), 둘째 줄 C→Go(§1), 셋째 줄 cgo.Handle(§2), 넷째 줄 호출 비용(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 16장, go1.27.1 로컬 실행(2026-09-29) — call_c_from_go·call_go_from_c·handle, cgo 호출 비용 1.24~1.27 비교.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 680


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, 'ARCHITECTURE · 16-04 OVERVIEW',
      'cgo 는 C 라이브러리를 잇는 다리입니다',
      '16-04 의 키워드 개념도. 첫 줄은 main.go 의 import "C" 앞 주석에 쓴 C 함수 add 를 C.add(3, 2) 로 불러 5 를 받는다는 것이다. 둘째 줄은 C 의 add 가 _cgo_export.h 로 //export 한 Go 함수 doubler 를 불러 8 을 돌려준다는 것이다. 셋째 줄은 string 필드가 있는 Person 을 cgo.NewHandle 로 정수 손잡이로 바꿔 C 를 건넌 뒤 h.Value 로 되찾는다는 것이다. 넷째 줄은 빈 C 함수 호출이 go1.25.1 에서 약 26ns, Go 1.26 부터 약 18~19ns 로 줄었지만 cgo 는 성능이 아니라 통합을 위한 도구라는 것이다.',
      lead='화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.')


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




for i, sec in enumerate(('§1', '§1', '§2', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'main.go', 'import "C" 앞 주석')
node(0, 1, 'C 함수 add', 'printf · 버퍼링', INFO)
node(0, 2, '5', 'Go 가 받음', OK)
harrow(0, 0, 'C.add(3, 2)')
harrow(0, 1, '반환')

node(1, 0, 'C 의 add', 'example.c')
node(1, 1, 'doubler', '//export 한 Go 함수', INFO)
node(1, 2, '8', 'doubler(3) + 2', OK)
harrow(1, 0, '_cgo_export.h')
harrow(1, 1, '반환')

node(2, 0, 'Person', 'string 필드')
node(2, 1, 'uintptr_t 손잡이', 'C 를 건넘', INFO)
node(2, 2, 'Person', 'Delete 로 정리', OK)
harrow(2, 0, 'cgo.NewHandle')
harrow(2, 1, 'h.Value()')

node(3, 0, '빈 C 함수 호출', 'go1.25.1 · 약 26ns')
node(3, 1, '약 18~19ns', '중앙값 · 약 25~30% 감소', INFO)
node(3, 2, '통합용 도구', '성능용 아님', ACC)
harrow(3, 0, 'Go 1.26 부터')
harrow(3, 1, '그래도', ACC, 'acc')


d.legend(584, [("cgo 장치", INFO), ("결과", OK), ("비용", ACC)])
d.save('16-04.chapter-overview.svg')
print('ok', '16-04')
