# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: 값은 본문 각 절의 도식과 같다. `GET /users/7`·`POST /graphql`(GraphQL over HTTP 초안 §4.4, 요청 JSON 의 query), `Bearer 2YotnFZF…`·`expires_in 3600`(RFC 6749 §5.1 예시 응답, RFC 6750 §2.1 헤더 형식),
#   `HMAC-SHA256`·`83f6b232…`·`b18dc408…`(본문 §3 시연 값을 python hmac 으로 계산 — 키·App ID·nonce 는 만든 예시), `code=SplxlOBe…`·`POST /token`(OIDC Core 1.0 §3.1.2.5·§3.1.3.1 예시), `IdP 세션 쿠키`·`입력 없음`(SAML 2.0 Profiles §4.1.3.4 의 기존 세션 재사용), `argon2id m=19456 t=2 p=1`(OWASP Password Storage Cheat Sheet 최소 설정).
#   추출본 v1.txt 355~410행(SSO)·418~470행(비밀번호)·940~1010행(웹 API 접근)·1560~1580행(API 스타일).
# Layout conventions: 카드 폭 140·높이 212, 가로 stride 156(x=24+156k), 카드 y=112, 화살표는 카드 중앙 y=218. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 03-02",
      "API 의 모양과 접근을 지키는 여섯 장치",
      "스타일이 요청의 모양을 정하고 토큰·서명·SSO·해시가 접근과 비밀번호를 지킵니다.",
      "여섯 절이 값 하나씩을 들고 이어집니다")

CW, CH, STRIDE, X0, Y0 = 140, 212, 156, 24, 112
cards = [
    ("§1", "네 API 스타일", "GET /users/7", "POST /graphql", "같은 조회 네 모양", INFO),
    ("§2", "토큰 접근", "Bearer 2YotnFZF…", "expires_in 3600", "만료되면 401", INFO),
    ("§3", "HMAC 서명", "HMAC-SHA256", "83f6b232…", "변조 시 b18dc408…", ACC),
    ("§4", "SSO 첫 로그인", "code=SplxlOBe…", "POST /token", "코드 앞길 토큰 뒷길", INFO),
    ("§5", "둘째 앱 통과", "IdP 세션 쿠키", "입력 없음", "SAML 도 같은 설계", INFO),
    ("§6", "솔트와 느린 해시", "argon2id", "m=19456 t=2 p=1", "솔트별로 다른 값", INFO),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, MONO, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 12, c, MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("03-02.chapter-overview.svg")
