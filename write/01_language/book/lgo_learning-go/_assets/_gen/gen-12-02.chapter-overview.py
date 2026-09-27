# 12-02.chapter-overview — select 는 준비된 case 를 무작위로 고르고, 동시성은 API 에서 감추며, 루프 변수는 반복마다 새로 생기고, 고루틴은 context 로 끝낸다
# 본문 요구(12-02 「학습 목표」 개념도 문단): 첫 줄 select 와 for-select(§1), 둘째 줄 API 에서 채널·뮤텍스 감추기(§2), 셋째 줄 Go 1.22 루프 변수(§3), 넷째 줄 고루틴 누수와 context 취소(§4).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 12장 「select」「Keep Your APIs Concurrency-Free」「Goroutines, for Loops, and Varying Variables」「Always Clean Up Your Goroutines」「Use the Context to Terminate Goroutines」, go1.25.1 로컬 실행(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 648


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, 'ARCHITECTURE · 12-02 OVERVIEW',
      'select 로 고르고, 고루틴은 끝나는 길을 둡니다',
      '12-02 의 키워드 개념도. 첫 줄은 여러 채널 가운데 준비된 case 를 select 가 무작위로 골라 기아와 교착을 피하고, for 로 감싸 for-select 루프가 되는 흐름이다. 둘째 줄은 채널과 뮤텍스를 내보내지 않고 클로저가 비즈니스 로직을 감싸 동시성을 API 밖에 두는 원칙이다. 셋째 줄은 Go 1.22 부터 루프 변수가 반복마다 새로 생기고, 그 밖의 바뀌는 변수는 매개변수로 복사해 넘긴다는 것이다. 넷째 줄은 끝나지 않는 고루틴이 누수가 되고, ctx.Done() 을 select 에 넣은 뒤 cancel 하면 끝난다는 흐름이다.',
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

node(0, 0, '여러 채널', '읽기 · 쓰기 case')
node(0, 1, 'select', '기아 · 교착 방지', INFO)
node(0, 2, 'for-select', '빠져나갈 길 필수')
harrow(0, 0, '준비된 것 무작위', ACC, 'acc')
harrow(0, 1, 'for 로 감쌈')

node(1, 0, '채널 · 뮤텍스', '구현 세부')
node(1, 1, '동시성 없는 API', '내보내지 않음', OK)
node(1, 2, '비즈니스 로직', '고루틴을 모름')
harrow(1, 0, 'API 에서 감춤')
harrow(1, 1, '클로저가 감쌈')

node(2, 0, '루프 변수 캡처', 'go func() { v }')
node(2, 1, '반복마다 새 v', 'go 지시어 1.22 이상', OK)
node(2, 2, '그 밖의 변수', '매개변수로 복사')
harrow(2, 0, 'Go 1.22 부터')
harrow(2, 1, '여전히 조심')

node(3, 0, '끝나지 않는 고루틴', '채널 쓰기에서 멈춤', WARN)
node(3, 1, 'ctx.Done()', 'select 의 case 로', INFO)
node(3, 2, 'cancel()', 'Done 채널을 닫음', OK)
harrow(3, 0, '누수를 막으려면')
harrow(3, 1, '고루틴 종료')


d.legend(584, [("Go 구성 요소", INFO), ("지켜진 상태", OK), ("누수 위험", WARN), ("선택 규칙", ACC)])
d.save('12-02.chapter-overview.svg')
print('ok', '12-02')
