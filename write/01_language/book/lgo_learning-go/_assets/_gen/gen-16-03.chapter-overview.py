# 16-03.chapter-overview — 필드 순서가 구조체 크기를 바꾸고, 바이트를 unsafe.Pointer 로 구조체로 보며, 리플렉션 오프셋으로 막힌 필드에 닿고, checkptr 이 일부 오용만 잡는다
# 본문 요구(16-03 「학습 목표」 개념도 문단): 첫 줄 패딩(§1), 둘째 줄 바이트→구조체(§2), 셋째 줄 내보내지 않은 필드(§3), 넷째 줄 checkptr(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 16장, go1.27.1 로컬 실행(2026-09-29) — sizeof_offsetof·unsafe_data·unexported_field_access, checkptr 실험.
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


d = D(W, H, 'ARCHITECTURE · 16-03 OVERVIEW',
      'unsafe 는 메모리 배치를 스스로 책임지게 합니다',
      '16-03 의 키워드 개념도. 첫 줄은 BoolIntBool 이 24바이트이고 bool 을 모은 BoolBoolInt 는 16바이트이며, 구조체 크기는 가장 큰 정렬값의 배수라 bool 셋은 3바이트라는 것이다. 둘째 줄은 16바이트 배열을 unsafe.Pointer 로 Data 로 보고 리틀 엔디언이면 Value 만 뒤집는다는 것이다. 셋째 줄은 리플렉션의 FieldByName 이 준 오프셋 8 을 unsafe.Add 로 더해 *bool 로 바꾸면 막힌 필드가 바뀐다는 것이다. 넷째 줄은 24바이트 객체를 *[8]uint64 로 보는 변환을 -d=checkptr 이 잡지만 바이트 배열이나 스택 객체 변환은 못 잡는다는 것이다.',
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




for i, sec in enumerate(('§1', '§2', '§3', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'BoolIntBool', '24 바이트')
node(0, 1, 'BoolBoolInt', '16 바이트', INFO)
node(0, 2, 'bool 셋', '3 바이트', OK)
harrow(0, 0, '순서 바꾸기')
harrow(0, 1, '정렬값 배수')

node(1, 0, '[16]byte', '네트워크 바이트')
node(1, 1, 'Data', 'Value · Label · Active', INFO)
node(1, 2, 'ReverseBytes32', 'Value 만 뒤집기', ACC)
harrow(1, 0, '포인터 변환')
harrow(1, 1, '리틀 엔디언이면', ACC, 'acc')

node(2, 0, 'FieldByName("b")', '리플렉션')
node(2, 1, 'unsafe.Add', '포인터 + 8', INFO)
node(2, 2, 'b = true', '막힌 필드 바뀜', ACC)
harrow(2, 0, 'Offset 8')
harrow(2, 1, '*bool 로', ACC, 'acc')

node(3, 0, '*[8]uint64 변환', '24바이트 객체')
node(3, 1, 'fatal error', 'straddles allocations', OK)
node(3, 2, '못 잡음', '바이트 배열 · 스택', ACC)
harrow(3, 0, '-d=checkptr')
harrow(3, 1, '예외도 있음', ACC, 'acc')


d.legend(584, [("unsafe 장치", INFO), ("결과", OK), ("책임·한계", ACC)])
d.save('16-03.chapter-overview.svg')
print('ok', '16-03')
