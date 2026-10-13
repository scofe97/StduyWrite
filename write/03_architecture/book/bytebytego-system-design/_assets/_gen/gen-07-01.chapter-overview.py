# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: 추출본 v1.txt 2950~3025행(정보 흐름과 자금 흐름, 은행 A·B 100 대 500 순액 400), 2175~2230행(100 USD → 88 EUR),
#   EU 규정 2015/751 제3조 0,2 %·제4조 0,3 %, Stripe 문서 authorization validity window(CIT 7일),
#   BIS Bulletin No 87(2024-05-30, USD 100 → KRW 120,000), Swift 보도자료 2025-11-25(MT 병행 2025-11-22 종료),
#   BIS Triennial Survey 2025 확정치(2026-06) Table 1(하루 9,510,240백만 달러, 2025-04).
# Layout conventions: 카드 폭 296·높이 148, 가로 stride 320(x=40+320k), 행 y=112·308, 행 간 화살표는 ㄷ자(수직→수평→수직). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 516
d = D(W, H, "BYTEBYTEGO · 07-01",
      "결제 한 건이 지나는 다섯 자리와 값",
      "카드 승인에서 외환과 장부까지 메시지와 돈이 따로 움직이는 길을 값으로 따라갑니다.",
      "값은 문서용 예시이며 상한·날짜는 규정과 공식 발표를 따릅니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


CW, CH, STRIDE, X0, Y0, Y1 = 296, 148, 320, 40, 112, 308
cards = [
    ("§1", "카드 결제의 참여자", "발급사 · 매입사 · 네트워크", "카드 소지자 · 가맹점 · PSP", "인터체인지 상한 0.2% · 0.3%", INFO),
    ("§2", "승인과 정산", "승인 100.00 EUR → 보류", "청구 → 청산 기록 → 정산", "승인 유효 7일 (비대면 고객 개시)", INFO),
    ("§3", "국경 간 송금", "메시지는 SWIFT, 돈은 대리 은행", "USD 100 → KRW 120,000", "MT 병행 종료 2025-11-22", INFO),
    ("§4", "외환", "100 USD → 88 EUR", "소매 → 도매 → 최상위", "하루 9.5조 달러 (2025-04)", INFO),
    ("§5", "지갑과 장부", "100 대 500 → 순액 400", "잔액은 저장하거나 계산", "준비금 이동은 정산 은행에서", ACC),
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
    d.t(cx, y + 28, title, 13, c if c == ACC else INK, _kr(title), "middle", 600)
    d.line(x + 12, y + 44, x + CW - 12, y + 44, RULE, 0.6)
    d.t(cx, y + 76, v1, 12, c if c == ACC else INFO, _kr(v1), "middle", 600)
    d.t(cx, y + 100, v2, 12, INK, _kr(v2), "middle")
    d.t(cx, y + 128, sub, 12, MUTED, _kr(sub), "middle")
    if col < 2 and k < len(cards) - 1:
        d.arrow([(x + CW + 2, y + CH / 2), (x + STRIDE - 4, y + CH / 2)], MUTED, "ar", 1.4)

# 첫 행 끝(§3)에서 둘째 행 시작(§4)으로 내려가는 ㄷ자 화살표.
xe = X0 + 2 * STRIDE + CW / 2
xs = X0 + CW / 2
d.arrow([(xe, Y0 + CH + 2), (xe, Y0 + CH + 24), (xs, Y0 + CH + 24), (xs, Y1 - 4)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("07-01.chapter-overview.svg")
