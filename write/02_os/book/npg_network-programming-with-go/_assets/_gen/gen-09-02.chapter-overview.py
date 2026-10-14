# 09-02.chapter-overview — 미들웨어는 핸들러를 감싸고, ServeMux 는 경로를 나누며, HTTP/2 서버 푸시는 브라우저가 걷어냈다
# 본문 요구(09-02 「학습 목표」 개념도 문단): §1~2 줄은 func(http.Handler) http.Handler 시그니처와 http.TimeoutHandler 의 시간 한도 감시,
#           §3 줄은 http.StripPrefix 와 RestrictPrefix, http.FileServer 의 정적 파일 경로 검증 파이프라인,
#           §4 줄은 http.ServeMux 의 최장 일치 패턴과 301 리다이렉트, drainAndClose 본문 회수,
#           §5 줄은 http.Pusher 서버 푸시의 브라우저 퇴출과 103 Early Hints 대안.
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표.
# 사실 출처: 《Network Programming with Go》 Ch.9 Building HTTP Services (Listing 9-11~9-20),
#           net/http, TimeoutHandler, RestrictPrefix, StripPrefix, FileServer, ServeMux, Pusher, Chrome 106, Firefox 132, RFC 8297.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 680


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 09-02 OVERVIEW",
      "미들웨어는 감싸고 ServeMux 는 나누며 서버 푸시는 걷어냈습니다",
      "09-02 의 키워드 개념도. "
      "§1~2 줄은 func(http.Handler) http.Handler 시그니처로 핸들러를 감싸고 http.TimeoutHandler 가 지정 시간을 감시해 초과 시 ErrHandlerTimeout 으로 후속 쓰기를 차단하는 미들웨어 흐름이다. "
      "§3 줄은 http.StripPrefix 로 경로 앞부분을 자르고 RestrictPrefix 로 점 접두사 숨김 파일을 404 차단해 http.FileServer 로 넘기는 파이프라인이다. "
      "§4 줄은 http.ServeMux 가 가장 긴 일치 패턴으로 라우팅하고 슬래시 누락 요청을 301 리다이렉트하며 drainAndClose 로 요청 본문을 회수하는 흐름이다. "
      "§5 줄은 http.Pusher 로 자원을 선제 전송하던 서버 푸시가 캐시 불일치와 대역폭 경합으로 퇴출되고 103 Early Hints 로 대체된 과정이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


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


for i, sec in enumerate(("§1~2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1~2: 미들웨어 시그니처와 TimeoutHandler
node(0, 0, "미들웨어", "func(http.Handler) Handler", INFO)
node(0, 1, "http.TimeoutHandler", "지정 시간 초과 감시", INFO)
node(0, 2, "ErrHandlerTimeout", "503 반환 · 후속 쓰기 차단", WARN)
harrow(0, 0, "시간 한도 부여")
harrow(0, 1, "초과 후 쓰기 시")

# §3: 경로 접두사 검사와 파일 은닉
node(1, 0, "http.StripPrefix", "'/static/' 접두사 절삭", INFO)
node(1, 1, "RestrictPrefix", "'.' 숨김 파일 404 차단", INFO)
node(1, 2, "http.FileServer", "200 OK 정적 파일 제공", OK)
harrow(1, 0, "접두사 제거 후")
harrow(1, 1, "검사 통과 시")

# §4: ServeMux 패턴 매칭과 본문 정리
node(2, 0, "drainAndClose", "미처리 요청 본문 회수", OK)
node(2, 1, "http.ServeMux", "최장 일치 패턴 라우팅", INFO)
node(2, 2, "301 Moved", "URL 정규화 유도", WARN)
harrow(2, 0, "멀티플렉서를 감쌈")
harrow(2, 1, "슬래시 누락 요청 시")

# §5: HTTP/2 서버 푸시와 브라우저 퇴출
node(3, 0, "http.Pusher", "PUSH_PROMISE 선제 전송", INFO)
node(3, 1, "브라우저 퇴출", "Chrome 106 비활성 · FF 132 제거", BAD)
node(3, 2, "103 Early Hints", "Link 프리로드 헤더 통보", OK)
harrow(3, 0, "캐시 중복 · 경합")
harrow(3, 1, "현대 표준 대안")

d.legend(584, [("핵심 API · 미들웨어", INFO), ("정상 응답 · 대안", OK), ("시간 초과 · 정규화", WARN), ("생태계 퇴출", BAD)])
d.save("09-02.chapter-overview.svg")
print("ok 09-02 overview")
