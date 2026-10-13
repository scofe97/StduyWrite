# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: 추출본 v1.txt 3767~3850행(결제 열 단계·플래시 세일 디자인 원칙), §4 의 재고 100 개와 요청 100,000 건은 설계 가정 예시, §1 의 PE-1001 과 §7 의 재고 10 개·수량 4 도 문서용 예시.
# Layout conventions: 카드 폭 224·높이 148, 가로 stride 244(x=12+244k), 행 y=112·308, 행 간 화살표는 ㄷ자(수직→수평→수직). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 516
d = D(W, H, "BYTEBYTEGO · 07-03",
      "결제 세 절과 플래시 세일 네 절을 값으로 따라간다",
      "구매 버튼 뒤의 기록 순서에서 재고 차감까지 같은 카드 자리에 대표 값을 놓았습니다.",
      "금액·재고·요청 수는 문서용 예시이고 §4 의 값은 설계 가정입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


CW, CH, STRIDE, X0, Y0, Y1 = 224, 148, 244, 12, 112, 308
cards = [
    ("§1", "결제 열 단계", "이벤트 → 주문 둘", "30.00 = 20.00 + 10.00", "PSP 는 실행기만 부름", INFO),
    ("§2", "갱신 순서", "PSP → 지갑 → 원장", "멈춘 지점별 남는 값", "원장만 비면 대사로 발견", INFO),
    ("§3", "정산 파일", "밤마다 도착", "당일 거래 전체", "대사로 이어짐", INFO),
    ("§4", "부하 모양", "재고 100 · 요청 100,000", "99.9% 거절", "대부분이 실패할 요청", INFO),
    ("§5", "앞단 줄이기", "CDN · IP 당 제한", "화면 요소·JS 줄이기", "원본에 닿기 전에 걸러냄", INFO),
    ("§6", "큐와 격리", "큐 → 서비스 → DB", "전용 인스턴스", "임계 경로 줄이기", INFO),
    ("§7", "재고 차감", "10 → 6 → 2 → 거절", "과판매 0", "주문됐다 품절 방지", ACC),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    row, col = divmod(k, 4)
    x = X0 + col * STRIDE
    y = Y0 if row == 0 else Y1
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, y, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, y + 28, tag, 13, SOFT, MONO, "start")
    d.t(cx + 12, y + 28, title, 13, c if c == ACC else INK, _kr(title), "middle", 600)
    d.line(x + 12, y + 44, x + CW - 12, y + 44, RULE, 0.6)
    d.t(cx, y + 76, v1, 13, c if c == ACC else INFO, _kr(v1), "middle", 600)
    d.t(cx, y + 100, v2, 13, INK, _kr(v2), "middle")
    d.t(cx, y + 128, sub, 13, MUTED, _kr(sub), "middle")
    if col < 3 and k < len(cards) - 1:
        d.arrow([(x + CW + 2, y + CH / 2), (x + STRIDE - 4, y + CH / 2)], MUTED, "ar", 1.4)

# 첫 행 끝(§4)에서 둘째 행 시작(§5)으로 내려가는 ㄷ자 화살표.
xe = X0 + 3 * STRIDE + CW / 2
xs = X0 + CW / 2
d.arrow([(xe, Y0 + CH + 2), (xe, Y0 + CH + 24), (xs, Y0 + CH + 24), (xs, Y1 - 4)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("07-03.chapter-overview.svg")
