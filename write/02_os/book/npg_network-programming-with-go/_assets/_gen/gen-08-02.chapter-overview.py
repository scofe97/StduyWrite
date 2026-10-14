# 08-02.chapter-overview — Go HTTP 클라이언트는 응답 본문을 닫아야 연결을 재사용하고 context 로 요청을 끊는다
# 본문 요구(08-02 「학습 목표」 개념도 문단): §1 줄 http.Head 와 Date 시각 오차 측정, §2 줄 resp.Body 소진과 TCP 연결 재사용,
#           §3 줄 DefaultClient 무한 대기 방지와 NewRequestWithContext, §4 줄 req.Close = true 와 DisableKeepAlives,
#           §5 줄 json.NewEncoder 와 multipart.Writer POST 전송.
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자, 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표 하나.
#           관계 라벨은 화살표 위(가로) 또는 오른쪽(세로)에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: 《Network Programming with Go》 Ch.8 Writing HTTP Clients (Listing 8-2~8-11),
#           http.Head, resp.Body, io.Discard, http.NewRequestWithContext, req.Close, multipart.Writer.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 768


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 08-02 OVERVIEW",
      "본문을 끝까지 읽고 닫아야 재사용하고 context 로 끊습니다",
      "08-02 의 키워드 개념도. "
      "§1 줄은 http.Head 로 본문 없이 헤더만 받아 본문을 먼저 닫은 뒤 Date 로 로컬 시각 오차를 측정하는 기본 클라이언트 흐름이다. "
      "§2 줄은 응답 본문 resp.Body 가 소켓에 남지 않도록 io.Discard 로 EOF 까지 소진하고 닫아 TCP 연결을 재사용하는 규약이다. "
      "§3 줄은 타임아웃 없는 DefaultClient 의 영구 블로킹을 NewRequestWithContext 와 5초 데드라인으로 방어하는 취소 제어다. "
      "§4 줄은 req.Close = true 로 Connection: close 헤더를 보내고 Transport.DisableKeepAlives 로 전역 풀링을 끄는 세션 정리다. "
      "§5 줄은 json.NewEncoder 로 버퍼에 직렬화하고 multipart.Writer 로 파트를 조립해 FormDataContentType 을 등록하는 POST 전송이다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 기본 클라이언트로 요청하고 응답을 읽는다
node(0, 0, "http.Head", "본문 없는 HEAD 요청", INFO)
node(0, 1, "resp.Body.Close()", "nil 아니므로 먼저 닫음", OK)
node(0, 2, "Date 헤더", "time.RFC1123 오차 측정")
harrow(0, 0, "응답 직후")
harrow(0, 1, "닫은 뒤 헤더 읽기")

# §2 응답 본문을 끝까지 읽고 닫아야 연결이 재사용된다
node(1, 0, "resp.Body", "소켓 버퍼의 응답 스트림", INFO)
node(1, 1, "io.Discard", "io.Copy 로 EOF 까지 소진", ACC)
node(1, 2, "TCP 연결 재사용", "유휴 풀 회수 · 세션 유지", OK)
harrow(1, 0, "EOF 까지 배출")
harrow(1, 1, "소진 후 Close")

# §3 타임아웃과 취소로 요청이 영원히 막히지 않게 한다
node(2, 0, "DefaultClient", "기본 타임아웃 0s 무한 대기", WARN)
node(2, 1, "NewRequestWithContext", "context 로 요청 수명 제어", INFO)
node(2, 2, "DeadlineExceeded", "errors.Is 판별 · 즉시 탈출", OK)
harrow(2, 0, "context 주입")
harrow(2, 1, "5초 만료 시")

# §4 지속 연결을 끄는 것은 요청 하나 또는 클라이언트 전체에서 정한다
node(3, 0, "req.Close = true", "응답 후 이 연결만 닫음", INFO)
node(3, 1, "Connection: close", "서버에 세션 정리 통보", WARN)
node(3, 2, "DisableKeepAlives", "클라이언트 전역 풀링 해제", WARN)
harrow(3, 0, "헤더 전송")
harrow(3, 1, "전역 설정은")

# §5 JSON 과 multipart 폼으로 데이터를 보낸다
node(4, 0, "json.NewEncoder", "버퍼에 JSON 직렬화", INFO)
node(4, 1, "multipart.Writer", "boundary 및 파트 조립", INFO)
node(4, 2, "FormDataContentType", "Content-Type 에 boundary 등록", OK)
harrow(4, 0, "파일을 함께 보낼 때는")
harrow(4, 1, "요청 헤더 설정")

varrow(0, 0, "본문 있는 응답이면")

d.legend(712, [("핵심 API · 요청", INFO), ("정상 완료 · 재사용", OK), ("무한 대기 · 세션 종료", WARN), ("본문 배출", ACC)])
d.save("08-02.chapter-overview.svg")
print("ok 08-02 overview")
