# 09-01.chapter-overview — 타임아웃으로 서버를 지키고 의존성을 주입해 격리 시험합니다
# 본문 요구(09-01 「학습 목표」 개념도 문단): §1 줄은 서버 수신 루프, §2 줄은 소켓 타임아웃 방어, §3 줄은 TLS 암호화 채널, §4~5 줄은 핸들러 규약과 검증, §6 줄은 의존성 주입.
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자, 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표 하나.
#           관계 라벨은 화살표 위(가로) 또는 오른쪽(세로)에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: 《Network Programming with Go》 Ch.9 Building HTTP Services (Listing 9-1~9-10), go1.25.1 로컬 실행(2026-10-14).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 800


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 09-01 OVERVIEW",
      "타임아웃으로 서버를 지키고 의존성을 주입해 격리 시험합니다",
      "09-01 의 키워드 개념도. 윗줄의 서버 기동과 둘째·셋째 줄의 타임아웃·TLS 설정으로 서버를 보호한다. "
      "넷째 줄의 핸들러 규약과 상태 코드 검증을 거쳐 아랫줄에서 클로저와 구조체로 의존성을 주입한다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4~5", "§6")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1
node(0, 0, "net.Listen", "TCP 리스너 바인딩")
node(0, 1, "http.Server", "Addr · Handler 선언", INFO)
node(0, 2, "srv.Serve(l)", "독립 고루틴 수신 루프", OK)
harrow(0, 0, "Serve 에 넘길 리스너")
harrow(0, 1, "고루틴으로 실행")

# §2
node(1, 0, "ReadHeaderTimeout", "헤더 1분 · 슬로로리스 방어", INFO)
node(1, 1, "IdleTimeout", "Keep-Alive 유휴 5분")
node(1, 2, "http.TimeoutHandler", "엔드포인트별 2분 제한", OK)
harrow(1, 0, "유휴 구간은 따로")
harrow(1, 1, "미들웨어로 개별 제어")

# §3
node(2, 0, "cert.pem · key.pem", "인증서와 개인키")
node(2, 1, "srv.ServeTLS(l)", "TLS 핸드셰이크 완결", INFO)
node(2, 2, "8443 포트", "개발용 HTTPS 서빙", OK)
harrow(2, 0, "인증서 파일 경로")
harrow(2, 1, "암호화 채널 가동")

# §4~5
node(3, 0, "ServeHTTP(w, r)", "Handler 단일 인터페이스")
node(3, 1, "w.WriteHeader(code)", "Write 전에 상태 코드 확정", ACC)
node(3, 2, "httptest.NewRecorder", "w.Result() 로 소켓 없이 검증", OK)
harrow(3, 0, "본문 쓰기 전에", ACC, "acc")
harrow(3, 1, "메모리 버퍼에 기록")

# §6
node(4, 0, "Methods 맵", "map[string]http.Handler", INFO)
node(4, 1, "클로저 팩토리", "dbHandler 의존성 캡처")
node(4, 2, "Handlers 구조체", "공통 자원 필드와 메서드", OK)
harrow(4, 0, "메서드별 핸들러")
harrow(4, 1, "규모 커지면 구조체로")

varrow(3, 0, "인터페이스 직접 구현")

d.legend(736, [("핵심 인터페이스 · 컴포넌트", INFO), ("검증 · 서빙 완료", OK), ("주의할 호출 순서", ACC)])
d.save("09-01.chapter-overview.svg")
print("ok 09-01 overview")
