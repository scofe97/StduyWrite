# 14-01.chapter-overview — context 는 빈 출발점에서 감싸 첫 매개변수로 넘기고, HTTP 요청에 붙여 나르며, 내보내지 않은 키로 값을 담고, 추적 GUID 는 context 에 남긴다
# 본문 요구(14-01 「학습 목표」 개념도 문단): 첫 줄 Background 와 첫 매개변수(§1), 둘째 줄 req.Context·WithContext(§1), 셋째 줄 키와 ContextWith·FromContext(§2), 넷째 줄 GUID 추적(§2).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 14장 「What Is the Context?」·「Values」, go1.25.1 로컬 실행(2026-09-28) — context_user 401·200, context_guid 두 서비스 로그에 같은 GUID.
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


d = D(W, H, 'ARCHITECTURE · 14-01 OVERVIEW',
      'context 는 매개변수이고 값은 아래로만 흐릅니다',
      '14-01 의 키워드 개념도. 첫 줄은 context.Background 로 만든 빈 출발점을 감싸 함수의 첫 매개변수 ctx 로 넘기는 흐름이다. 둘째 줄은 HTTP 요청에 붙은 context 를 미들웨어가 꺼내 값을 담고 WithContext 로 새 요청에 붙여 다음 핸들러로 넘기는 흐름이다. 셋째 줄은 내보내지 않은 키 타입으로 값을 담는 ContextWithUser 와 꺼내는 UserFromContext 이고, 꺼낸 값은 명시적 인자로 넘긴다. 넷째 줄은 X-GUID 헤더의 GUID 를 context 에 담아 업무 로직을 모르게 지나 로그와 다음 서비스에 전한다는 것이다.',
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




for i, sec in enumerate(('§1', '§1', '§2', '§2')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'context.Background()', '빈 출발점 · TODO 는 임시')
node(0, 1, 'ctx context.Context', '첫 매개변수', INFO)
node(0, 2, 'logic(ctx, info)', '명시적으로 넘김', OK)
harrow(0, 0, '감싸서')
harrow(0, 1, '넘김')

node(1, 0, 'req.Context()', '요청에 붙은 context')
node(1, 1, 'req.WithContext(ctx)', '값을 담은 새 요청', INFO)
node(1, 2, 'h.ServeHTTP(rw, req)', 'Handler 시그니처 그대로', OK)
harrow(1, 0, '값을 담아')
harrow(1, 1, '다음 핸들러')

node(2, 0, 'type userKey int', '내보내지 않은 키')
node(2, 1, 'ContextWithUser', 'WithValue 로 자식 context', INFO)
node(2, 2, 'UserFromContext', '꺼내 명시적 인자로', OK)
harrow(2, 0, 'WithValue')
harrow(2, 1, '핸들러에서')

node(3, 0, 'X-GUID 헤더', '없으면 새 UUID')
node(3, 1, 'context 의 GUID', '업무 로직은 모름', INFO)
node(3, 2, '로그 · 다음 서비스', '같은 GUID', OK)
harrow(3, 0, '미들웨어')
harrow(3, 1, 'Logger · Request')


d.legend(584, [("context", INFO), ("쓰는 쪽", OK)])
d.save('14-01.chapter-overview.svg')
print('ok', '14-01')
