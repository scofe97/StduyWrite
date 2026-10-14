# 08-01.chapter-overview — HTTP 는 URL 로 자원을 가리키고 메서드로 요청하며 상태 코드로 답합니다
# 본문 요구(08-01 「학습 목표」 개념도 문단): §1 줄은 프로토콜과 호스트로 대상 서버를 가리키고 fragment 는 브라우저에 남기는 경계입니다.
#           §2 줄은 안전한 메서드와 멱등 메서드를 가르고 비멱등 POST 재시도에는 멱등성 키를 두는 약속입니다.
#           §3 줄은 상태 코드 범주별 대응 전략이며, §2 의 멱등성에 따라 5xx 서버 장애 시 지수 백오프 재시도를 판단하는 흐름입니다.
#           §4 줄은 루트 HTML 수신 후 부속 자원을 요청할 때 지속 연결이 TCP 소켓을 재사용해 핸드셰이크 왕복을 줄이는 원리입니다.
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표 하나.
# 사실 출처: 《Network Programming with Go》 Ch.8 Writing HTTP Clients (Understanding the Basics of HTTP ~ From Request to Rendered Page, Listing 8-1, Table 8-1),
#           RFC 9110 (HTTP Semantics), RFC 3986 (URI Generic Syntax), Go net/http.
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


d = D(W, H, "ARCHITECTURE · 08-01 OVERVIEW",
      "HTTP 는 URL 로 자원을 가리키고 메서드로 요청하며 상태 코드로 답합니다",
      "08-01 의 키워드 개념도. "
      "§1 줄은 scheme://host 로 대상 서버를 지정하고 자원 경로를 전달하되 #fragment 는 요청 줄에서 제외해 브라우저에만 남기는 구조다. "
      "§2 줄은 서버 상태를 바꾸지 않는 안전한 메서드와 여러 번 수행해도 결과가 같은 멱등 메서드를 구분하고 비멱등 POST 재시도에는 Idempotency-Key 를 두는 규약이다. "
      "§3 줄은 세 자리 상태 코드에 따라 304 캐시 재사용과 4xx 수정을 분기하고 5xx 서버 장애 시 멱등성을 검증해 지수 백오프로 재시도하는 흐름이다. "
      "§4 줄은 루트 HTML 수신 후 부속 자원을 연쇄 요청할 때 HTTP/1.1 지속 연결(Keep-Alive)이 단일 TCP 소켓을 재사용해 핸드셰이크 왕복을 줄이는 원리다.",
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


def varrow(i, j, label):
    x = nx(j) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    d.arrow([(x, y1 + 2), (x, y2 - 4)], SOFT, "soft", 1.3)
    d.t(x + 10, (y1 + y2) / 2 + 4, label, 11, MUTED, kr(label), "start", 600)


for i, sec in enumerate(("§1", "§2", "§3", "§4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 URL 은 다섯 부분으로 자원을 가리킨다
node(0, 0, "scheme://host", "필수 프로토콜 · 호스트", INFO)
node(0, 1, "path?query", "자원 경로 · 질의 매개변수")
node(0, 2, "#fragment", "브라우저 소비 · 서버 미전송", WARN)
harrow(0, 0, "자원 경로 지정")
harrow(0, 1, "요청 줄에서 제외")

# §2 요청은 메서드·URL·헤더·본문이고 메서드마다 약속이 다르다
node(1, 0, "안전한 메서드", "GET · HEAD · 서버 상태 불변", INFO)
node(1, 1, "멱등 메서드", "PUT · DELETE · 동일 효과", OK)
node(1, 2, "Idempotency-Key", "중복 결제 방지 · 서버 저장", ACC)
harrow(1, 0, "안전하면 멱등도")
harrow(1, 1, "비멱등 POST 보완", ACC, "acc")

# §3 응답은 상태 코드 범주로 클라이언트가 할 일을 알려 준다
node(2, 0, "상태 코드별 분기", "304 캐시 · 4xx 수정 · 5xx 대기", INFO)
node(2, 1, "멱등성 확인", "GET · PUT 또는 키 검증")
node(2, 2, "지수 백오프 재시도", "무작위 지터 · 점진적 대기", OK)
harrow(2, 0, "5xx 일시 장애 시")
harrow(2, 1, "멱등 요청일 때")

# §4 한 페이지는 HTML 하나에서 시작해 여러 요청이 된다
node(3, 0, "루트 HTML (GET /)", "기본 인덱스 문서 수신", INFO)
node(3, 1, "부속 자원 요청", "CSS · JPEG(304) · ICO(404)")
node(3, 2, "지속 연결 (Keep-Alive)", "단일 TCP 소켓 · RTT 절감", OK)
harrow(3, 0, "태그 파싱 후")
harrow(3, 1, "동일 소켓 재사용")

# §2 멱등성 규약이 §3 의 재시도 판단 기준이 됨
varrow(1, 1, "재시도 판단 기준")

d.legend(584, [("프로토콜 규약", INFO), ("안전한 동작 · 비용 절감", OK), ("서버 미전송", WARN), ("재시도 보증 장치", ACC)])
d.save("08-01.chapter-overview.svg")
print("ok 08-01 overview")
