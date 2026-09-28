# 14-03.chapter-overview — WithTimeout·WithDeadline 이 요청 시간을 제한하고, 자식 기한은 부모에 묶이며, Err 와 Cause 가 끝난 까닭을 가르고, 긴 계산은 Cause 로 스스로 멈춘다
# 본문 요구(14-03 「학습 목표」 개념도 문단): 첫 줄 시간 제한 context(§1), 둘째 줄 부모·자식 기한(§1), 셋째 줄 Err 와 Cause(§1), 넷째 줄 직접 짠 코드의 취소 확인(§2).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 14장 「Contexts with Deadlines」·「Context Cancellation in Your Own Code」, go1.25.1 로컬 실행(2026-09-28) — nested_timers 2s, own_cancellation 10s 60,618,656회.
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


d = D(W, H, 'ARCHITECTURE · 14-03 OVERVIEW',
      '요청 시간은 context 에 적고 아래 호출이 모두 지킵니다',
      '14-03 의 키워드 개념도. 첫 줄은 요청 시간 제한을 WithTimeout 이나 WithDeadline 으로 context 에 적고, 그 context 를 넘긴 HTTP·데이터베이스 호출이 함께 멈춘다는 것이다. 둘째 줄은 자식에 3초를 줘도 부모 2초에 묶여 2초에 끝난다는 것이다. 셋째 줄은 Err 가 명시적 취소면 context.Canceled, 시간 초과면 context.DeadlineExceeded 를 돌려주고 시간 초과일 때는 Cause 도 같다는 것이다. 넷째 줄은 오래 도는 계산이 매 반복 앞에서 context.Cause 를 확인해 스스로 멈춘다는 것이다.',
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




for i, sec in enumerate(('§1', '§1', '§1', '§2')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, '요청 시간 제한', '성능 한계선')
node(0, 1, '기한이 든 context', '과거 시각이면 이미 취소', INFO)
node(0, 2, 'NewRequestWithContext', 'HTTP · DB 호출도 멈춤', OK)
harrow(0, 0, 'WithTimeout 등')
harrow(0, 1, '아래 호출로')

node(1, 0, 'parent · 2초', 'WithTimeout')
node(1, 1, 'child · 3초', '부모를 감싼 자식', INFO)
node(1, 2, 'child.Done() · 2s', '부모 기한에 묶임', ACC)
harrow(1, 0, '감쌈')
harrow(1, 1, '부모가 끝나면', ACC, 'acc')

node(2, 0, 'ctx.Err()', '끝난 까닭의 종류')
node(2, 1, 'context.Canceled', 'Cause 는 넘긴 원인', INFO)
node(2, 2, 'DeadlineExceeded', 'Cause 도 같은 값', OK)
harrow(2, 0, '명시적 취소면')
harrow(2, 1, '시간 초과면')

node(3, 0, '긴 계산 루프', '라이프니츠 π')
node(3, 1, 'context.Cause(ctx)', '취소됐으면 오류', INFO)
node(3, 2, '부분 결과 반환', '10s · 60,618,656 회', OK)
harrow(3, 0, '매 반복 앞')
harrow(3, 1, '오류면')


d.legend(584, [("context 장치", INFO), ("결과", OK), ("부모에 묶임", ACC)])
d.save('14-03.chapter-overview.svg')
print('ok', '14-03')
