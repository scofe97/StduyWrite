# 09-02.chapter-overview — %w 로 감싸 원래 오류를 품고, 여럿은 Join 으로 묶으며, Is·As 가 트리를 뒤지고, defer 가 한 곳에서 감싼다
# 본문 요구(09-02 「학습 목표」 개념도 문단): 첫 줄 %w 감싸기와 Unwrap(§1), 둘째 줄 errors.Join 과 Unwrap() []error(§2), 셋째 줄 errors.Is·As(§3), 넷째 줄 defer 감싸기(§4).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 9장 「Wrapping Errors」·「Wrapping Multiple Errors」·「Is and As」·「Wrapping Errors with defer」, go1.25.1 로컬 실행(2026-09-27).
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


d = D(W, H, 'ARCHITECTURE · 09-02 OVERVIEW',
      '오류를 감싸면 트리가 되고, Is·As 가 그 안을 찾습니다',
      '09-02 의 키워드 개념도. 첫 줄은 fmt.Errorf 의 %w 가 원래 오류를 품은 새 오류를 만들고 errors.Unwrap 이 그것을 꺼내지만, 보통은 Is·As 로 찾는다는 것이다. 둘째 줄은 여러 오류를 errors.Join 으로 묶으면 Unwrap() []error 를 구현하는 오류가 되어 errors.Unwrap 이 nil 을 돌려준다는 것이다. 셋째 줄은 errors.Is 가 트리를 내려가며 == 나 Is 메서드로 값을 찾고, errors.As 가 타입이 맞는 오류를 변수에 꺼낸다는 것이다. 넷째 줄은 이름 붙은 반환 값 err 를 defer 클로저가 한 번에 감싼다는 것이다.',
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




for i, sec in enumerate(('§1', '§2', '§3', '§4')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'fmt.Errorf("…: %w", err)', '원래 오류를 품음')
node(0, 1, 'errors.Unwrap', '감싼 오류 하나를 꺼냄', INFO)
node(0, 2, 'errors.Is · As', '보통은 이쪽으로 찾음', OK)
harrow(0, 0, '꺼내기')
harrow(0, 1, '직접 대신')

node(1, 0, 'err1 · err2 · err3', '검증 오류 여럿')
node(1, 1, 'errors.Join', 'Unwrap() []error', INFO)
node(1, 2, 'errors.Unwrap → nil', '직접 부르지 않는 이유', ACC)
harrow(1, 0, '묶기')
harrow(1, 1, 'Unwrap 하면', ACC, 'acc')

node(2, 0, 'os.ErrNotExist', '찾는 값')
node(2, 1, '트리의 모든 오류', '== 또는 Is 메서드', INFO)
node(2, 2, 'errors.As(&pe)', '타입이 맞으면 꺼냄', OK)
harrow(2, 0, 'errors.Is')
harrow(2, 1, '타입은')

node(3, 0, 'return "", err', '감싸지 않고 반환')
node(3, 1, 'defer 클로저', 'err = fmt.Errorf(…%w)', INFO)
node(3, 2, 'in DoSomeThings: …', '한 곳에서 감쌈', OK)
harrow(3, 0, '함수가 끝날 때')
harrow(3, 1, '호출자가 받음')


d.legend(584, [("errors 함수", INFO), ("쓸 형태", OK), ("함정", ACC)])
d.save('09-02.chapter-overview.svg')
print('ok', '09-02')
