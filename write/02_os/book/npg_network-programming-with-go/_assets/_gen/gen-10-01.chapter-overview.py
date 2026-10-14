# 10-01.chapter-overview — Caddy 는 에지에서 TLS 와 인증서를 자동 관리하고, 관리 API 로 설정을 무중단 교체하며, 어댑터로 TOML 을 JSON 으로 바꾸고, 미들웨어 모듈로 요청을 가로챈다
# 본문 요구(10-01 「학습 목표」 개념도 문단): §1~2 줄은 에지 프록시와 xcaddy 정적 빌드(§1~2),
#           §3 줄은 관리 API 와 원자적 리로드(§3), §4 줄은 설정 어댑터와 JSON 변환(§4), §5 줄은 미들웨어 모듈 생명주기와 요청 가로채기(§5).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자, 행 안은 가로 화살표.
#           관계 라벨은 화살표 위에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: 《Network Programming with Go》 Ch.10 Caddy: A Contemporary Web Server (Listing 10-1~10-8),
#           Let's Encrypt, ACME, localhost:2019/load, caddyconfig.Adapter, caddyhttp.MiddlewareHandler.
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


d = D(W, H, "ARCHITECTURE · 10-01 OVERVIEW",
      "Caddy 는 설정을 API 로 실시간 바꾸고 어댑터와 모듈로 넓힙니다",
      "10-01 의 키워드 개념도. §1~2 줄은 ACME 프로토콜로 인증서를 자동 갱신하고 에지 리버스 프록시로 TLS 를 종단하며 xcaddy 로 커스텀 모듈을 정적 빌드하는 흐름이다. "
      "§3 줄은 2019 포트의 관리 API 로 새 JSON 설정을 전송해 사전 검증하고 새 리스너를 열어 원자적으로 리로드하는 제어 평면이다. "
      "§4 줄은 caddy.toml 설정 문서를 caddyconfig.Adapter 로 파싱해 Caddy 표준 JSON 으로 변환하는 어댑터 파이프라인이다. "
      "§5 줄은 caddy.ModuleInfo 로 모듈을 등록하고 Provisioner 와 Validator 생명주기를 거쳐 MiddlewareHandler 로 HTTP 요청을 가로채는 데이터 평면이다.",
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

# §1~2: 에지 프록시와 정적 빌드
node(0, 0, "ACME 프로토콜", "Let's Encrypt · 60일 갱신", INFO)
node(0, 1, "에지 리버스 프록시", "TLS 종단 · 토폴로지 은닉", OK)
node(0, 2, "xcaddy 정적 빌드", "커스텀 모듈 단일 바이너리", INFO)
harrow(0, 0, "인증서 자동 관리로")
harrow(0, 1, "확장 모듈 포함 시")

# §3: 관리 API 와 원자적 리로드
node(1, 0, "관리 API", "localhost:2019", INFO)
node(1, 1, "POST /load", "JSON 설정 사전 검증", INFO)
node(1, 2, "원자적 리로드", "새 소켓 바인드 · in-flight 보존", ACC)
harrow(1, 0, "새 설정 게시")
harrow(1, 1, "사전 검증 통과 시")

# §4: 설정 어댑터와 JSON 변환
node(2, 0, "caddy.toml", "인간 친화적 설정 문서", INFO)
node(2, 1, "caddyconfig.Adapter", "Adapt(body, opts) 변환", INFO)
node(2, 2, "Caddy 표준 JSON", "코어 엔진에 주입", OK)
harrow(2, 0, "바이트 스트림 전달")
harrow(2, 1, "Go 맵 거쳐 직렬화")

# §5: 미들웨어 모듈 생명주기와 요청 가로채기
node(3, 0, "caddy.ModuleInfo", "http.handlers 고유 ID", INFO)
node(3, 1, "Provisioner · Validator", "로거 주입 · 기본값 보정", INFO)
node(3, 2, "MiddlewareHandler", "ServeHTTP · 404 차단", OK)
harrow(3, 0, "생명주기 단계 진입")
harrow(3, 1, "검증 후 체인 결합")

d.legend(584, [("Caddy 아키텍처 · 설정", INFO), ("정상 완료 · 서빙", OK), ("원자적 무중단 교체", ACC)])
d.save("10-01.chapter-overview.svg")
print("ok 10-01 overview")
