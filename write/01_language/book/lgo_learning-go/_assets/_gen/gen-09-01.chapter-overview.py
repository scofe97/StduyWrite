# 09-01.chapter-overview — Go 오류는 마지막 반환 값으로 돌려주고, 문자열·센티널·사용자 정의 타입으로 뜻을 담으며, 성공이면 nil 을 직접 돌려준다
# 본문 요구(09-01 「학습 목표」 개념도 문단): 첫 줄 반환 값과 nil 비교(§1), 둘째 줄 문자열 오류와 센티널(§2·§3), 셋째 줄 사용자 정의 오류 타입과 nil 함정(§4).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 9장 「How to Handle Errors: The Basics」·「Sentinel Errors」·「Errors Are Values」, go1.25.1 로컬 실행(2026-09-27).
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


d = D(W, H, 'ARCHITECTURE · 09-01 OVERVIEW',
      'Go 오류는 반환 값이고, 뜻은 값과 타입에 담습니다',
      '09-01 의 키워드 개념도. 첫 줄은 함수가 마지막 반환 값으로 error 를 돌려주고 호출자가 if 로 nil 과 비교해, 오류가 없으면 들여쓰지 않은 황금 경로로 이어가는 흐름이다. 둘째 줄은 errors.New 로 만든 오류에 이름을 붙여 패키지 수준 센티널로 공개하면 호출자가 == 로 확인한다는 것이다. 셋째 줄은 정보를 담은 사용자 정의 오류 타입도 반환 타입은 error 로 두고, 성공이면 그 타입의 변수가 아니라 nil 을 직접 돌려준다는 것이다.',
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




for i, sec in enumerate(('§1', '§2·§3', '§4')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'calcRemainderAndMod', '(int, int, error)')
node(0, 1, 'err != nil ?', 'if 로 nil 과 비교', INFO)
node(0, 2, '황금 경로', '들여쓰지 않은 본문', OK)
harrow(0, 0, '돌려줌')
harrow(0, 1, 'nil 이면')

node(1, 0, 'errors.New(...)', '문자열 오류')
node(1, 1, 'var ErrFormat', '패키지 수준 센티널', INFO)
node(1, 2, 'err == zip.ErrFormat', '문서가 밝힌 경우', OK)
harrow(1, 0, '이름 붙여 공개')
harrow(1, 1, '호출자는')

node(2, 0, 'StatusErr{Status}', '정보를 담은 오류 타입')
node(2, 1, '반환 타입 error', '호출자가 타입에 안 묶임', INFO)
node(2, 2, 'return nil', 'StatusErr 변수 반환 금지', OK)
harrow(2, 0, '돌려줄 때')
harrow(2, 1, '성공이면', ACC, 'acc')


d.legend(456, [("error 인터페이스", INFO), ("쓸 형태", OK), ("함정 피하기", ACC)])
d.save('09-01.chapter-overview.svg')
print('ok', '09-01')
