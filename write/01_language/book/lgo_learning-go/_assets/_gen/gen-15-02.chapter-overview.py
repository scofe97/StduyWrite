# 15-02.chapter-overview — 사례 목록이 하위 테스트가 되고, 오류는 값으로 확인하며, 병렬 하위 테스트는 부모 함수가 끝난 뒤 돌고, 커버리지 100% 에도 버그가 남는다
# 본문 요구(15-02 「학습 목표」 개념도 문단): 첫 줄 테이블 테스트(§1), 둘째 줄 오류 비교(§1), 셋째 줄 병렬과 루프 변수(§2), 넷째 줄 커버리지(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 15장, go1.27.1 로컬 실행(2026-09-28) — table·parallel, PAUSE/CONT 순서, 커버리지 87.5%→100%, another_mult.
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


d = D(W, H, 'ARCHITECTURE · 15-02 OVERVIEW',
      '사례는 데이터로 적고 커버리지는 빠뜨린 줄만 보여 줍니다',
      '15-02 의 키워드 개념도. 첫 줄은 사례 슬라이스의 원소마다 t.Run 으로 하위 테스트를 만들고 -run 으로 하나만 골라 돌린다는 것이다. 둘째 줄은 오류 메시지 문자열 비교는 문구가 바뀌면 깨지므로 errors.Is·As 로 값과 타입을 확인한다는 것이다. 셋째 줄은 병렬 하위 테스트가 반복문 동안 멈췄다가 부모 함수가 반환한 뒤 돌아, go 지시어가 1.21 이하면 모두 마지막 d 를 본다는 것이다. 넷째 줄은 커버리지를 87.5% 에서 100% 로 채워도 곱셈 버그가 남아 있었다는 것이다.',
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

node(0, 0, '사례 슬라이스', '이름·입력·기대값')
node(0, 1, '하위 테스트', '부모/사례이름', INFO)
node(0, 2, '사례 하나만', '실패만 되풀이', OK)
harrow(0, 0, '원소마다 t.Run')
harrow(0, 1, '-run 으로')

node(1, 0, '오류 비교', 'errMsg 문자열')
node(1, 1, '테스트가 깨짐', '문구 약속 없음', ACC)
node(1, 2, 'errors.Is · As', '값·타입으로 확인', OK)
harrow(1, 0, '문구가 바뀌면', ACC, 'acc')
harrow(1, 1, '대신')

node(2, 0, 't.Parallel()', '하위 테스트 안')
node(2, 1, 'PAUSE', '부모 함수가 끝날 때까지', INFO)
node(2, 2, 'CONT · 마지막 d', '셋 다 50 60', ACC)
harrow(2, 0, '반복문 동안')
harrow(2, 1, 'go 1.21 이하면', ACC, 'acc')

node(3, 0, '-coverprofile', 'c.out')
node(3, 1, '87.5% → 100%', 'default 분기 추가', INFO)
node(3, 2, 'Expected 6, got 5', '곱셈 버그 남음', ACC)
harrow(3, 0, 'go tool cover')
harrow(3, 1, '그래도', ACC, 'acc')


d.legend(584, [("테스트 장치", INFO), ("결과", OK), ("함정", ACC)])
d.save('15-02.chapter-overview.svg')
print('ok', '15-02')
