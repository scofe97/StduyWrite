# 12-04.chapter-overview — A·B 를 동시에 불러 C 에 넘기는 파이프라인, 값이 흐르면 채널·필드를 나누면 뮤텍스, sync.Map·atomic 대신 map+RWMutex
# 본문 요구(12-04 「학습 목표」 개념도 문단): 첫 줄 세 서비스 파이프라인(§1), 둘째 줄 채널을 쓸 때(§2), 셋째 줄 뮤텍스를 쓸 때와 재진입 없음(§2), 넷째 줄 sync.Map·atomic(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 12장 「Put Your Concurrent Tools Together」「When to Use Mutexes Instead of Channels」「Atomics—You Probably Don’t Need These」, go1.25.1 로컬 실행(2026-09-28).
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


d = D(W, H, 'ARCHITECTURE · 12-04 OVERVIEW',
      '값이 흐르면 채널로, 필드를 나누면 뮤텍스로',
      '12-04 의 키워드 개념도. 첫 줄은 서비스 A 와 B 를 고루틴 둘로 동시에 부르고, 두 결과를 합쳐 서비스 C 에 넘기며, 전체를 50밀리초 안에 끝내는 파이프라인이다. 둘째 줄은 값이 고루틴 여럿을 거치며 변환될 때 채널을 써서 데이터 흐름을 드러내는 경우다. 셋째 줄은 struct 필드를 나눠 읽고 쓰기만 할 때 RWMutex 를 쓰되, Go 의 뮤텍스는 재진입하지 않아 같은 락을 두 번 잡으면 교착이라는 점이다. 넷째 줄은 sync.Map 과 atomic 은 특수한 경우와 전문가용이고, 대개 map 과 RWMutex 로 충분하다는 결론이다.',
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




for i, sec in enumerate(('§1', '§2', '§2', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'A · B 서비스', '고루틴 둘', INFO)
node(0, 1, 'abProcessor.wait', 'select · 2개 모임')
node(0, 2, 'C 서비스', '50ms 안에', OK)
harrow(0, 0, '동시에 호출')
harrow(0, 1, '합쳐서 넘김')

node(1, 0, '값의 변환', '고루틴 여럿을 거침')
node(1, 1, '채널', '흐름이 드러남', INFO)
node(1, 2, '한 번에 한 고루틴', '소유가 분명', OK)
harrow(1, 0, '넘기며 처리')
harrow(1, 1, '접근 주체')

node(2, 0, 'struct 필드 공유', '점수판')
node(2, 1, 'sync.RWMutex', '읽기 여럿 · 쓰기 하나', INFO)
node(2, 2, '재진입 없음', '두 번 잡으면 교착', WARN)
harrow(2, 0, '읽고 쓰기만', ACC, 'acc')
harrow(2, 1, '주의')

node(3, 0, 'sync.Map', 'any 타입 · 특수 경우')
node(3, 1, 'map + RWMutex', '대개 이쪽', OK)
node(3, 2, 'sync/atomic', '전문가용')
harrow(3, 0, '대신')
harrow(3, 1, '더 낮은 수준')


d.legend(584, [("쓰는 도구", INFO), ("얻는 것", OK), ("주의", WARN), ("고르는 기준", ACC)])
d.save('12-04.chapter-overview.svg')
print('ok', '12-04')
