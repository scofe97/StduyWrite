# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: ByteByteGo system-design-101 design-stock-exchange.md·low-latency-stock-exchange.md(커밋 b28380a)와 호가창 그림의 수량(시장가 매수 2700 = 200+400+1100+100 → 100.10 의 1800 주, 나머지 900 은 100.11 의 첫 주문),
#   Linux man-pages sched_setaffinity(2)·mmap(2), Fowler 「The LMAX Architecture」(2011-07-12). 1800 과 900 은 그림의 수량으로 직접 계산한 값이다.
# Layout conventions: 카드 폭 224·높이 148, 가로 stride 240(x=20+240k), 행 y=112·308, 행 간 화살표는 ㄷ자(수직→수평→수직). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 516
d = D(W, H, "BYTEBYTEGO · 09-02",
      "주문 한 건이 지나는 일곱 자리와 값",
      "브로커에서 매칭 엔진까지 같은 시장가 매수 2700 주가 지나는 자리를 값으로 따라갑니다.",
      "호가창 수량은 예시 값이고 1800 과 900 은 계산한 값입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


CW, CH, STRIDE, X0, Y0, Y1 = 224, 148, 240, 20, 112, 308
cards = [
    ("§1", "주문이 지나는 길", "시장가 매수 2700 주", "브로커 → 거래소 → 브로커", "체결이 같은 길로 돌아옴", INFO),
    ("§2", "입구의 검문", "검증 · 속도 제한 · 인증", "위험 점검 → 잔고 확인", "주문 관리자가 이어서", INFO),
    ("§3", "시퀀서", "주문과 체결을 한 줄로", "같은 입력은 같은 체결", "재생해도 결과가 같음", INFO),
    ("§4", "호가창", "가격 레벨마다 FIFO 큐", "100.10 에 1800 주", "2700 − 1800 = 900", INFO),
    ("§5", "자료 구조의 조건", "조회는 상수 시간", "변경은 가능하면 O(1)", "레벨마다 합계를 보관", INFO),
    ("§6", "마이크로초 설계", "한 서버 · 공유 메모리", "단일 스레드 · CPU 고정", "락 없음 · 문맥 전환 없음", ACC),
    ("§7", "경로 밖의 일", "시장 데이터 · 보고", "이벤트 버스 구독", "DB 기록은 뒤에서", INFO),
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
    d.t(cx, y + 28, title, 13, c if c == ACC else INK, _kr(title), "middle", 600)
    d.line(x + 12, y + 44, x + CW - 12, y + 44, RULE, 0.6)
    d.t(cx, y + 76, v1, 13, c if c == ACC else INFO, _kr(v1), "middle", 600)
    d.t(cx, y + 100, v2, 13, INK, _kr(v2), "middle")
    d.t(cx, y + 128, sub, 13, MUTED, _kr(sub), "middle")
    if col < 3 and k < len(cards) - 1 and not (row == 0 and col == 3):
        d.arrow([(x + CW + 2, y + CH / 2), (x + STRIDE - 4, y + CH / 2)], MUTED, "ar", 1.4)

# 첫 행 끝(§4)에서 둘째 행 시작(§5)으로 내려가는 ㄷ자 화살표.
xe = X0 + 3 * STRIDE + CW / 2
xs = X0 + CW / 2
d.arrow([(xe, Y0 + CH + 2), (xe, Y0 + CH + 24), (xs, Y0 + CH + 24), (xs, Y1 - 4)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("09-02.chapter-overview.svg")
