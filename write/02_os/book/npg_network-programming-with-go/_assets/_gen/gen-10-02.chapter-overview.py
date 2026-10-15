# 10-02.chapter-overview — Caddy 가 프록시와 정적 파일을 나누고 자동 HTTPS 를 붙입니다
# 본문 요구(10-02 「학습 목표」 개념도 문단): §1 줄은 r.RemoteAddr 대신 X-Forwarded-For 로 원격 클라이언트를 식별하고 trusted_proxies 로 위조를 막는 신뢰 경계,
#           §2 줄은 routes 배열을 순차 평가해 /backend 일치 시 reverse_proxy 로 중계하고 미매칭 시 file_server 로 넘기는 경로 분기,
#           §3 줄은 curl 검증 시 위조 헤더 203.0.113.195 를 폐기하고 실제 소켓 IP 로 덮어써 백엔드 로그에 남기는 신뢰 경계 증명,
#           §4 줄은 host 매처로 도메인을 감지해 ACME 프로토콜로 인증서를 자동 발급받고 포트 443 에 장착하는 자동 HTTPS 다.
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표.
# 사실 출처: 《Network Programming with Go》 Ch.10 Caddy: A Contemporary Web Server (Listing 10-9~10-14),
#           Caddy docs (reverse_proxy, automatic-https), RFC 8555 (ACME).
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


d = D(W, H, "ARCHITECTURE · 10-02 OVERVIEW",
      "Caddy 가 프록시와 정적 파일을 나누고 자동 HTTPS 를 붙입니다",
      "10-02 의 키워드 개념도. §1 줄은 소켓 프록시 주소 대신 X-Forwarded-For 헤더로 원격 클라이언트를 식별하고 trusted_proxies 로 위조를 걸러내는 신뢰 경계다. "
      "§2 줄은 routes 배열을 순차 평가해 /backend 경로 일치 시 reverse_proxy 로 중계하고 미매칭 시 file_server 로 넘기는 경로 분기다. "
      "§3 줄은 실제 curl 시험 시 위조 헤더 203.0.113.195 를 폐기하고 실제 소켓 IP 로 덮어써 백엔드 로그에 남기는 신뢰 경계 증명이다. "
      "§4 줄은 host 매처로 도메인을 감지해 ACME 프로토콜로 인증서를 자동 발급받고 포트 443 에 장착하는 자동 HTTPS 다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 프록시 뒤의 백엔드는 원래 클라이언트를 헤더로 안다
node(0, 0, "r.RemoteAddr", "프록시 직전 홉 주소", INFO)
node(0, 1, "X-Forwarded-For", "원래 클라이언트 IP", OK)
node(0, 2, "trusted_proxies", "미등록 시 위조 덮어씀", ACC)
harrow(0, 0, "소켓 대신 주입")
harrow(0, 1, "신뢰 경계로 검증", ACC, "acc")

# §2 경로별로 프록시와 정적 파일을 가른다
node(1, 0, "routes 순차 평가", "인덱스 순서대로 검사", INFO)
node(1, 1, "reverse_proxy", "localhost:8080 중계", OK)
node(1, 2, "file_server", "기본 폴백 · ./files", OK)
harrow(1, 0, "경로 일치 시 중계", OK, "ok")
harrow(1, 1, "불일치면 다음 route")

# §3 결과를 요청으로 확인한다
node(2, 0, "curl 요청", "GET /backend 시험", INFO)
node(2, 1, "위조 헤더 폐기", "203.0.113.195 무시", ACC)
node(2, 2, "백엔드 로그", "127.0.0.1 피어 기록", OK)
harrow(2, 0, "위조 헤더 전송", ACC, "acc")
harrow(2, 1, "소켓 주소로 덮어씀", OK, "ok")

# §4 자동 HTTPS 는 도메인과 열린 포트를 조건으로 인증서를 받아 온다
node(3, 0, "host 매처", "도메인 지정 · 80/443", INFO)
node(3, 1, "ACME 프로토콜", "기본 CA · Let's Encrypt", INFO)
node(3, 2, "TLS 인증서", "로컬 캐시 · 443 장착 · 308 승격", OK)
harrow(3, 0, "도메인 감지 즉시", INFO, "info")
harrow(3, 1, "HTTP-01 검증 통과", OK, "ok")

d.legend(584, [("Caddy 설정", INFO), ("정상 처리", OK), ("신뢰 경계", ACC)])
d.save("10-02.chapter-overview.svg")
print("ok 10-02 overview")
