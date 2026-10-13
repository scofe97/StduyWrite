# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: 추출본 v1.txt 2448~2505행(URL 입력 뒤 순서·example.com), RFC 3986 §3(scheme·authority·path), 직접 dig·openssl 측정(2026-10-12T16:28Z·16:33Z, 본문 §2·§3 에 명령 수록), RFC 9114 §3.1(ALPN h3·Alt-Svc), RFC 9111 §5.1(Age).
#   §6 의 www.shop.example·203.0.113.17·Age: 60 은 문서용 예시 값(RFC 2606 의 .example, RFC 5737 의 203.0.113.0/24).
# Layout conventions: 카드 폭 296·높이 148, 가로 stride 320(x=40+320k), 행 y=112·308, 행 간 화살표는 ㄷ자(수직→수평→수직). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 516
d = D(W, H, "BYTEBYTEGO · 03-01",
      "URL 한 줄이 지나는 여섯 단계와 값",
      "주소창의 URL 이 이름 조회, 연결, 암호화 합의, 요청, 그리기를 차례로 열고 CDN 이 그 길을 줄인다.",
      "§1~§5 는 example.com 의 값을, §6·§7 은 문서용 이름을 따라갑니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


CW, CH, STRIDE, X0, Y0, Y1 = 296, 148, 320, 40, 112, 308
cards = [
    ("§1", "주소 분해", "https://example.com", "/product/electric/phone", "scheme · authority · path", INFO),
    ("§2", "DNS 조회", "example.com A ?", "A 104.20.23.154 · TTL 300", "루트 → .com → 권한 서버", INFO),
    ("§3", "TCP · TLS 1.3", "SYN → ClientHello", "첫 요청은 2 RTT 뒤", "TLS_AES_256_GCM_SHA384", INFO),
    ("§4", "HTTP 요청", "GET /product/electric/phone", "ALPN h2 · Alt-Svc h3", "버전마다 막힘 범위가 좁아짐", INFO),
    ("§5", "화면 그리기", "HTML → DOM → 스타일", "레이아웃 → 페인트 → 합성", "script 가 파싱을 멈춤", INFO),
    ("§6 · §7", "CDN", "CNAME → 엣지 203.0.113.17", "미스 → 지역 캐시 → 원본", "Age: 60 은 적중", ACC),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    row, col = divmod(k, 3)
    x = X0 + col * STRIDE
    y = Y0 if row == 0 else Y1
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, y, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, y + 28, tag, 12, SOFT, MONO, "start")
    d.t(cx, y + 28, title, 14, c if c == ACC else INK, _kr(title), "middle", 600)
    d.line(x + 12, y + 44, x + CW - 12, y + 44, RULE, 0.6)
    d.t(cx, y + 76, v1, 13, c if c == ACC else INFO, _kr(v1), "middle", 600)
    d.t(cx, y + 100, v2, 13, INK, _kr(v2), "middle")
    d.t(cx, y + 128, sub, 13, MUTED, _kr(sub), "middle")
    if col < 2:
        d.arrow([(x + CW + 2, y + CH / 2), (x + STRIDE - 4, y + CH / 2)], MUTED, "ar", 1.4)

# 첫 행 끝(§3)에서 둘째 행 시작(§4)으로 내려가는 ㄷ자 화살표.
xe = X0 + 2 * STRIDE + CW / 2
xs = X0 + CW / 2
d.arrow([(xe, Y0 + CH + 2), (xe, Y0 + CH + 24), (xs, Y0 + CH + 24), (xs, Y1 - 4)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("단계별 대표 값", INFO)])
d.save("03-01.chapter-overview.svg")
