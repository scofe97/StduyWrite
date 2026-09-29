# 16-01.chapter-overview — 변수에서 타입과 종류를 얻고, 필드와 태그를 읽고, 포인터로 값을 바꾸고, 새 값을 만들며, 인터페이스 속 nil 을 가린다
# 본문 요구(16-01 「학습 목표」 개념도 문단): 첫 줄 TypeOf·Kind(§2), 둘째 줄 StructField(§2), 셋째 줄 값 바꾸기(§2), 넷째 줄 New·MakeSlice(§3), 다섯째 줄 IsValid·IsNil(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 16장, go1.27.1 로컬 실행(2026-09-29) — struct_tag·reflect_string_slice·no_value, 패닉 메시지.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 808


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, 'ARCHITECTURE · 16-01 OVERVIEW',
      '리플렉션은 타입 확인을 실행 중으로 미룹니다',
      '16-01 의 키워드 개념도. 첫 줄은 변수에 TypeOf 를 불러 reflect.Type 을 얻고, Kind 가 무엇으로 이뤄졌는지 알려 주며 종류에 맞지 않는 메서드는 패닉을 낸다는 것이다. 둘째 줄은 구조체의 NumField·Field 로 StructField 를 얻어 이름·타입·태그를 읽는다는 것이다. 셋째 줄은 포인터를 ValueOf 에 넘기고 Elem 으로 가서 SetInt 로 원래 변수를 바꾼다는 것이다. 넷째 줄은 reflect.Type 에서 New·MakeSlice 로 새 값을 만들고 Interface 와 타입 단언으로 되돌린다는 것이다. 다섯째 줄은 nil 인 *int 를 담은 인터페이스가 == nil 로는 false 이지만 IsValid·IsNil 로는 값이 nil 임을 안다는 것이다.',
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




for i, sec in enumerate(('§2', '§2', '§2', '§3', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'var x int', '변수')
node(0, 1, 'reflect.Type', 'Name · int', INFO)
node(0, 2, 'reflect.Int', '종류가 메서드를 정함', ACC)
harrow(0, 0, 'TypeOf')
harrow(0, 1, 'Kind()', ACC, 'acc')

node(1, 0, 'struct Foo', '태그 붙은 필드')
node(1, 1, 'StructField', 'Name · Type · Tag', INFO)
node(1, 2, '"value"', 'myTag 값', OK)
harrow(1, 0, 'Field(i)')
harrow(1, 1, 'Tag.Get')

node(2, 0, '&i', '포인터를 넘김')
node(2, 1, '설정 가능한 값', 'CanSet true', INFO)
node(2, 2, 'i == 20', '원래 변수가 바뀜', OK)
harrow(2, 0, 'Elem()')
harrow(2, 1, 'SetInt(20)')

node(3, 0, 'reflect.Type', 'TypeFor[T] · Go 1.22')
node(3, 1, '새 reflect.Value', '포인터 · slice', INFO)
node(3, 2, '[]string{"hello"}', '타입 단언', OK)
harrow(3, 0, 'New 등')
harrow(3, 1, 'Interface()')

node(4, 0, 'any 에 담긴 *int', 'nil 포인터')
node(4, 1, 'false', '타입이 담겨 있음', ACC)
node(4, 2, 'true', '값은 nil', OK)
harrow(4, 0, '== nil', ACC, 'acc')
harrow(4, 1, 'IsValid · IsNil')


d.legend(712, [("리플렉션 값", INFO), ("결과", OK), ("주의", ACC)])
d.save('16-01.chapter-overview.svg')
print('ok', '16-01')
