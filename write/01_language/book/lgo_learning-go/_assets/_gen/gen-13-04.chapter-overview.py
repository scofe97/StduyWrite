# 13-04.chapter-overview — 타임아웃을 정한 Client, Server 와 ServeMux, Handler 를 감싸는 미들웨어와 ResponseController, 핸들러를 고르는 slog
# 본문 요구(13-04 「학습 목표」 개념도 문단): 첫 줄 Client(§1), 둘째 줄 Server·ServeMux(§2), 셋째 줄 미들웨어와 ResponseController(§3~4), 넷째 줄 slog(§5).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 13장 「net/http」「Structured Logging」, go1.25.1 로컬 실행(2026-09-28).
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


d = D(W, H, 'ARCHITECTURE · 13-04 OVERVIEW',
      '타임아웃은 직접, 미들웨어는 감싸고, 로그는 구조화로',
      '13-04 의 키워드 개념도. 첫 줄은 Timeout 을 정한 http.Client 가 NewRequestWithContext 로 만든 요청을 Do 로 보내고, Body 를 json.Decoder 로 읽는 흐름이다. 둘째 줄은 타임아웃을 정한 http.Server 가 ServeMux 에 요청을 넘기고, ServeMux 가 GET /hello/{name} 같은 패턴에 맞는 Handler 를 부르는 흐름이다. 셋째 줄은 미들웨어가 http.Handler 를 받아 감싼 Handler 를 돌려주고, ResponseController 가 인터페이스를 바꾸지 않고 선택 기능을 더한다는 것이다. 넷째 줄은 slog 가 핸들러로 텍스트나 JSON 을 고르고, LogAttrs 로 할당을 줄인다는 것이다.',
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




for i, sec in enumerate(('§1', '§2', '§3~4', '§5')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'http.Client', 'Timeout 30s', INFO)
node(0, 1, 'client.Do(req)', 'NewRequestWithContext')
node(0, 2, 'res.Body', 'json.Decoder 로 읽음', OK)
harrow(0, 0, 'DefaultClient 대신', ACC, 'acc')
harrow(0, 1, '응답')

node(1, 0, 'http.Server', 'Read · Write · Idle 타임아웃', INFO)
node(1, 1, 'ServeMux', 'GET /hello/{name}')
node(1, 2, 'Handler', 'ServeHTTP(w, r)', OK)
harrow(1, 0, '요청을 넘김')
harrow(1, 1, '패턴에 맞으면')

node(2, 0, '미들웨어', 'func(Handler) Handler', INFO)
node(2, 1, '감싼 Handler', '검사 · 호출 · 정리')
node(2, 2, 'ResponseController', 'ErrNotSupported 로 확인', OK)
harrow(2, 0, '감쌈', ACC, 'acc')
harrow(2, 1, '선택 기능은')

node(3, 0, 'slog.Info', '키 · 값 쌍')
node(3, 1, 'slog.Handler', 'Text · JSON · 레벨', INFO)
node(3, 2, 'LogAttrs', '할당이 적음', OK)
harrow(3, 0, '핸들러를 고름')
harrow(3, 1, '빠른 길')


d.legend(584, [("net/http · slog", INFO), ("결과", OK), ("직접 정할 것", ACC)])
d.save('13-04.chapter-overview.svg')
print('ok', '13-04')
