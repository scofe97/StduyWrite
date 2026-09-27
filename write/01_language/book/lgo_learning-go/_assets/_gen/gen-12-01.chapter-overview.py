# 12-01.chapter-overview — 독립 단계가 있을 때 동시성을 쓰고, 고루틴은 런타임이 스레드에 태우며, 값은 채널로 넘기고 쓰는 쪽이 닫는다
# 본문 요구(12-01 「학습 목표」 개념도 문단): 첫 줄은 데이터 흐름에 독립 단계가 있을 때 동시성, 하드웨어가 허락할 때 병렬(§1), 둘째 줄은 go 로 띄운 고루틴을 스케줄러가 OS 스레드에 태움(§2),
#           셋째 줄은 채널을 만들어 주고받다 쓰는 쪽이 닫으면 읽는 쪽 루프가 끝남(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 12장 「When to Use Concurrency」「Goroutines」「Channels」, go1.25.1 로컬 실행(2026-09-28).
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


d = D(W, H, 'ARCHITECTURE · 12-01 OVERVIEW',
      '고루틴은 런타임이 나눠 태우고 값은 채널로 넘깁니다',
      '12-01 의 키워드 개념도. 첫 줄은 데이터 흐름에 서로 기다리지 않는 단계가 있을 때 동시성을 쓰고, 하드웨어와 알고리즘이 허락할 때만 병렬로 돈다는 것이다. 둘째 줄은 go 키워드로 띄운 고루틴을 Go 런타임 스케줄러가 적은 수의 OS 스레드에 나눠 태우는 모습이다. 셋째 줄은 make 로 만든 채널에 <- 로 값을 주고받고, 쓰는 쪽이 close 하면 읽는 쪽 for-range 가 끝나는 흐름이다.',
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




for i, sec in enumerate(('§1', '§2', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, '데이터 흐름', '받기 · 변환 · 내기')
node(0, 1, '동시성', '문제를 나누는 구조', INFO)
node(0, 2, '병렬 실행', '하드웨어가 허락할 때')
harrow(0, 0, '독립 단계가 있으면')
harrow(0, 1, '같은 뜻이 아님')

node(1, 0, 'go f()', '반환 값은 버려짐')
node(1, 1, '고루틴', '작은 스택 · 빠른 전환', INFO)
node(1, 2, 'OS 스레드', '런타임이 만든 몇 개')
harrow(1, 0, '런타임 스케줄러')
harrow(1, 1, '나눠 태움')

node(2, 0, 'make(chan T)', '제로 값은 nil')
node(2, 1, '채널', '버퍼 없음 · 있음', INFO)
node(2, 2, 'for-range 끝', 'comma ok 로 확인', OK)
harrow(2, 0, '<- 로 쓰기·읽기')
harrow(2, 1, '쓰는 쪽이 close', ACC, 'acc')


d.legend(456, [("핵심 개념", INFO), ("책임 규칙", ACC), ("끝나는 조건", OK)])
d.save('12-01.chapter-overview.svg')
print('ok', '12-01')
