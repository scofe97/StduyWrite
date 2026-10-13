# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: dig MX gmail.com 실측(2026-10-12, 5 gmail-smtp-in.l.google.com), RFC 5321 §4.5.4.1(재시도 30분 이상), Google Gmail 도움말 imap-smtp 문서(imap.gmail.com:993·pop.gmail.com:995),
#   Gmail 도움말 Send attachments(개인 계정 25 MB), Google Maps JavaScript API Map and tile coordinates(타일 256 px, 시카고 41.85 -87.65 와 project() 식)로 계산한 z=3 의 64 타일·2048 px·타일 (2, 2),
#   Google Routes API computeRoutes(computeAlternativeRoutes·routingPreference). 시카고 좌표는 문서의 예시 값이다.
# Layout conventions: 카드 폭 296·높이 148, 가로 stride 320(x=40+320k), 행 y=112·308, 행 간 화살표는 ㄷ자(수직→수평→수직). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 516
d = D(W, H, "BYTEBYTEGO · 08-02",
      "메일 한 통과 지도 한 장이 지나는 다섯 자리와 값",
      "SMTP 릴레이에서 지도 서비스까지, 같은 메일과 같은 좌표가 지나는 자리를 값으로 따라갑니다.",
      "MX 는 2026-10-12 실측이고 시카고 좌표는 Google 문서의 예시 값입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


CW, CH, STRIDE, X0, Y0, Y1 = 296, 148, 320, 40, 112, 308
cards = [
    ("§1", "MX 조회와 SMTP", "gmail.com → MX 5", "gmail-smtp-in.l.google.com", "실패는 30분 이상 간격 재시도", INFO),
    ("§2", "받는 길", "IMAP 993 · POP3 995", "서버에 둠 대 내려받고 지움", "SMTP 로는 읽지 못함", INFO),
    ("§3", "웹메일 서버 구조", "큐 셋 · 저장소 넷", "첨부 25 MB (개인 계정)", "큐가 수신과 발신을 가름", ACC),
    ("§4", "지도 타일", "4^z 타일 · 256 px", "z=3 → 64 타일 · 2048 px", "시카고 z=3 타일 (2, 2)", INFO),
    ("§5", "지도 서비스 셋", "위치 · 타일 · 길찾기", "주소 → 좌표 → 후보 경로", "시간 예측으로 순위", INFO),
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
d.save("08-02.chapter-overview.svg")
