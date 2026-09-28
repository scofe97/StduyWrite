# 14-02.chapter-overview — WithCancel 의 취소 함수는 defer 로 꼭 부르고, 취소는 Done 채널이 닫히는 것으로 전해지며, WithCancelCause 의 첫 원인이 Cause 에 남는다
# 본문 요구(14-02 「학습 목표」 개념도 문단): 첫 줄 WithCancel 과 취소 함수(§1), 둘째 줄 Done 채널로 전해지는 취소(§1), 셋째 줄 WithCancelCause 와 Cause(§2).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 14장 「Cancellation」, go1.25.1 로컬 실행(2026-09-28) — cancel_http·cancel_error_http, Cause first · Err context canceled.
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


d = D(W, H, 'ARCHITECTURE · 14-02 OVERVIEW',
      '취소는 닫히는 채널로 전해지고 이유는 Cause 에 남습니다',
      '14-02 의 키워드 개념도. 첫 줄은 WithCancel 이 돌려준 취소 함수를 defer 로 걸고, 부르지 않으면 메모리와 고루틴이 샌다는 것이다. 둘째 줄은 실패한 고루틴이 취소 함수를 부르면 Done 채널이 닫혀 select 가 깨어나고 다른 고루틴의 HTTP 요청도 함께 끝난다는 흐름이다. 셋째 줄은 WithCancelCause 의 취소 함수에 넘긴 첫 오류를 context.Cause 가 돌려주고 두 번째 오류는 덮지 않으며, Err 는 context canceled 라는 것이다.',
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




for i, sec in enumerate(('§1', '§1', '§2')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'WithCancel(parent)', 'ctx · cancel')
node(0, 1, 'defer cancel()', '여러 번 불러도 됨', INFO)
node(0, 2, '안 부르면 누수', '메모리 · 고루틴', ACC)
harrow(0, 0, '곧바로')
harrow(0, 1, '잊으면', ACC, 'acc')

node(1, 0, 'cancelFunc()', '실패한 고루틴이 부름')
node(1, 1, 'ctx.Done() 닫힘', 'chan struct{}', INFO)
node(1, 2, '다른 고루틴 · HTTP 요청', '함께 끝남', OK)
harrow(1, 0, '취소')
harrow(1, 1, 'select 가 깨어남')

node(2, 0, 'WithCancelCause', 'cancel(err)')
node(2, 1, 'context.Cause(ctx)', '첫 원인만 남음', INFO)
node(2, 2, 'ctx.Err()', 'context canceled', OK)
harrow(2, 0, '첫 원인')
harrow(2, 1, '까닭의 종류는')


d.legend(456, [("context 장치", INFO), ("결과", OK), ("함정", ACC)])
d.save('14-02.chapter-overview.svg')
print('ok', '14-02')
