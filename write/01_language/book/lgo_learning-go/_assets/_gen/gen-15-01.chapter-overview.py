# 15-01.chapter-overview — 테스트 함수가 실패를 알리고, TestMain 이 패키지 테스트를 감싸고, 결과가 캐시되고, _test 패키지가 공개 API 를 시험하며, go-cmp 가 비교한다
# 본문 요구(15-01 「학습 목표」 개념도 문단): 첫 줄 Error·Fatal(§1), 둘째 줄 TestMain(§2), 셋째 줄 결과 캐시(§3), 넷째 줄 _test 패키지(§3), 다섯째 줄 go-cmp(§4).
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 15장, go1.27.1 로컬 실행(2026-09-28) — testmain·adder·pubadder·cmp, os.Exit 없는 TestMain, 결과 캐시 실험.
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


d = D(W, H, 'ARCHITECTURE · 15-01 OVERVIEW',
      '테스트도 같은 패키지의 Go 코드이고 go test 가 돌립니다',
      '15-01 의 키워드 개념도. 첫 줄은 테스트 함수가 어긋남을 t.Error 로 알리고 이어서 검사하거나, 뒤 검사가 막히면 t.Fatal 로 그 테스트만 멈춘다는 것이다. 둘째 줄은 TestMain 이 패키지에 한 번 불려 m.Run 으로 테스트 함수를 돌리고, 반환하면 Go 1.15 부터 그 결과로 종료 코드가 정해진다는 것이다. 셋째 줄은 패키지 인자를 주어 돌릴 때(go test . 포함) 통과한 결과가 캐시되고 코드나 testdata 가 바뀌면 다시 돈다는 것이다. 넷째 줄은 패키지 이름에 _test 를 붙이면 내보낸 것만 써서 공개 API 를 시험한다는 것이다. 다섯째 줄은 cmp.Diff 가 어긋난 필드를 보여 주고 IgnoreFields 로 시각 필드를 뺀다는 것이다.',
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




for i, sec in enumerate(('§1', '§2', '§3', '§3', '§4')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'Test_addNumbers', 't *testing.T')
node(0, 1, 't.Error', '이어서 검사', INFO)
node(0, 2, 't.Fatal', '그 테스트만 멈춤', ACC)
harrow(0, 0, '실패하면')
harrow(0, 1, '뒤 검사가 막히면', ACC, 'acc')

node(1, 0, 'TestMain(m)', '패키지에 한 번')
node(1, 1, '테스트 함수들', 'Cleanup 은 거꾸로', INFO)
node(1, 2, '종료 코드', 'Go 1.15+ 자동 os.Exit', OK)
harrow(1, 0, 'm.Run()')
harrow(1, 1, '반환하면')

node(2, 0, 'go test ./...', '패키지 인자를 주면')
node(2, 1, '(cached)', '코드·testdata 그대로', INFO)
node(2, 2, '다시 실행', '-count=1 은 늘', OK)
harrow(2, 0, '통과한 결과')
harrow(2, 1, '파일이 바뀌면')

node(3, 0, 'pubadder_test', '패키지 이름')
node(3, 1, 'pubadder.AddNumbers', '내보낸 것만', INFO)
node(3, 2, '블랙박스 시험', '공개 API 계약', OK)
harrow(3, 0, 'import 해서')
harrow(3, 1, '결과')

node(4, 0, 'cmp.Diff(want, got)', 'go-cmp')
node(4, 1, '- / + 줄', '어긋난 필드', INFO)
node(4, 2, 'IgnoreFields', '그 필드만 뺌', ACC)
harrow(4, 0, '다르면')
harrow(4, 1, '시각 필드는', ACC, 'acc')


d.legend(712, [("테스트 장치", INFO), ("결과", OK), ("주의", ACC)])
d.save('15-01.chapter-overview.svg')
print('ok', '15-01')
