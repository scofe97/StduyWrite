# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: IETF datatracker draft-ietf-httpapi-idempotency-key-header-07 (2025-10-15, 2026-04-18 만료, §2.2 예시 키 8e03978e-40d5-43e8-bc93-6894a57f9324),
#   Stripe 문서 Idempotent requests(API v1 은 24시간 이상 지난 키를 정리할 수 있다), 추출본 v1.txt 3283~3324행(주문 $200 · 컷오프 23:59:55 와 00:00:30),
#   PCI SSC 블로그 2024-06-11(PCI DSS v4.0.1), PCI DSS Tokenization Guidelines 2011 Table 1(PAN 5994 0059 0172 3383 → 599400x18523mw4cw3383).
#   10.00 USD 는 추출본 v1.txt 3408행의 $10 예시, ORD 번호와 01-01·01-02 날짜는 문서용 예시.
# Layout conventions: 카드 폭 296·높이 148, 가로 stride 320(x=40+320k), 행 y=112·308, 행 간 화살표는 ㄷ자(수직→수평→수직). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 516
d = D(W, H, "BYTEBYTEGO · 07-02",
      "결제 한 건의 정확성을 지키는 다섯 절과 값",
      "중복 요청 막기에서 장부 맞추기와 카드 번호 숨기기까지, 같은 10.00 USD 가 지나는 자리를 값으로 따라갑니다.",
      "금액·번호는 문서용 예시이고 키·버전은 공식 자료의 값입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


CW, CH, STRIDE, X0, Y0, Y1 = 296, 148, 320, 40, 112, 308
cards = [
    ("§1", "재시도가 만드는 중복", "응답 유실 → 재시도", "10.00 USD × 2 = 20.00", "키 없이는 서버가 구분 못 함", INFO),
    ("§2", "멱등 키", "같은 키 → 저장된 응답 200", "PSP 청구는 1건", "키 보관 24시간 이상 (Stripe v1)", ACC),
    ("§3", "대사", "주문 = PSP 파일 = 원장", "200.00 = 200.00 = 200.00", "세 장부의 같은 행을 비교", INFO),
    ("§4", "불일치 처리", "23:59:55 대 00:00:30", "임시 불일치 → 다음 파일에서 해소", "끝내 없으면 조사", INFO),
    ("§5", "결제 보안", "PAN → 토큰", "PCI DSS v4.0.1", "3D Secure 는 도전 인증을 요구할 수 있음", INFO),
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
    d.t(x + 12, y + 28, tag, 13, SOFT, MONO, "start")
    d.t(cx, y + 28, title, 13, c if c == ACC else INK, _kr(title), "middle", 600)
    d.line(x + 12, y + 44, x + CW - 12, y + 44, RULE, 0.6)
    d.t(cx, y + 76, v1, 13, c if c == ACC else INFO, _kr(v1), "middle", 600)
    d.t(cx, y + 100, v2, 13, INK, _kr(v2), "middle")
    d.t(cx, y + 128, sub, 13, MUTED, _kr(sub), "middle")
    if col < 2 and k < len(cards) - 1:
        d.arrow([(x + CW + 2, y + CH / 2), (x + STRIDE - 4, y + CH / 2)], MUTED, "ar", 1.4)

# 첫 행 끝(§3)에서 둘째 행 시작(§4)으로 내려가는 ㄷ자 화살표.
xe = X0 + 2 * STRIDE + CW / 2
xs = X0 + CW / 2
d.arrow([(xe, Y0 + CH + 2), (xe, Y0 + CH + 24), (xs, Y0 + CH + 24), (xs, Y1 - 4)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("07-02.chapter-overview.svg")
