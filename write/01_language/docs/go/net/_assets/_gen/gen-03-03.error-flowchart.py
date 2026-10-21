# 사실 출처: go doc net.OpError, DNSError, ErrClosed, os.ErrDeadlineExceeded, mapErr (go1.25.1)
# 타입 스펙: type-flowchart
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 560

d = D(W, H,
      "NET ERROR CLASSIFICATION FLOWCHART",
      "net 패키지 반환 에러의 판별 갈림과 계통",
      "errors.Is 와 errors.As 를 사용한 소켓·타임아웃·컨텍스트·OS 에러 판별 순서",
      "같은 i/o timeout 문자열 뒤에 다른 에러 타입이 숨는 구조를 분기 논리로 정리")

# ── 1. 판별 노드 (좌측 열, x = 48, w = 384, h = 36) ──
# ── 2. 판별 결과 (우측 열, x = 504, w = 408, h = 36) ──
BX, BW, BH = 48, 384, 40
RX, RW, RH = 504, 408, 40

# 판별 순서는 본문 03-03 handleNetError 코드와 같다: ErrClosed → os 데드라인 → ctx 마감 → ctx 취소 → DNS → OpError
steps = [
    (96,  "errors.Is(err, net.ErrClosed)", "닫힌 소켓 연산", "이미 종료된 Conn 에서 I/O 수행", OK),
    (156, "errors.Is(err, os.ErrDeadlineExceeded)", "연결 I/O 데드라인 초과", "SetDeadline 초과 · 드물게 Dial 마감 경합도 여기로", ACC),
    (216, "errors.Is(err, context.DeadlineExceeded)", "연결 수립 마감 초과", "DialContext·DNS 의 ctx 타임아웃 · timeoutError", WARN),
    (276, "errors.Is(err, context.Canceled)", "호출자 컨텍스트 취소", "mapErr 변환 · canceledError 반환", INFO),
    (336, "errors.As(err, &dnsErr)", "도메인 이름 해석 실패", "*net.DNSError · IsNotFound / IsTimeout", INFO),
    (396, "errors.As(err, &opErr)", "소켓 시스템 콜 실패", "*net.OpError · opErr.Err 로 OS 에러 판별", BAD),
]

for i, (y, cond, title, desc, col) in enumerate(steps):
    is_focal = (col == ACC)
    # 좌측 조건 상자
    d.box(BX, y, BW, BH, fill=PAPER2, stroke=ACC if is_focal else RULE, sw=1.2 if is_focal else 0.9)
    d.t(BX + 16, y + 25, cond, 11, ACC if is_focal else INK, fam=MONO, anchor="start", weight=600 if is_focal else 400)

    # Yes 화살표 (수평 직선: 432 -> 504, 길이 72px)
    d.arrow([(BX + BW, y + 20), (RX, y + 20)], col, "ar", 1.4)
    d.chip(BX + BW + 36, y + 9, "Yes", col, 9)

    # 우측 결과 상자
    d.box(RX, y, RW, RH, fill=PAPER2, stroke=col, sw=1.2 if is_focal else 1.0)
    d.t(RX + 16, y + 16, title, 11, col, fam=KR, anchor="start", weight=600)
    d.t(RX + 16, y + 33, desc, 11, MUTED, fam=KR, anchor="start")

    # No 화살표 (수직 직선: y+BH -> next_y, 길이 24px >= 72/4=18px)
    if i < len(steps) - 1:
        next_y = steps[i+1][0]
        d.arrow([(BX + BW // 2, y + BH), (BX + BW // 2, next_y)], MUTED, "ar", 1.0)
        # 상자 사이 20px 에 칩을 넣으면 위아래 상자에 닿으므로 화살표 옆 글자로 둔다
        d.t(BX + BW // 2 + 10, y + BH + 14, "No", 9, SOFT, fam=MONO, anchor="start")

# 6단계 No 분기: 기타 일반 에러
last_y = steps[-1][0]
d.arrow([(BX + BW // 2, last_y + BH), (BX + BW // 2, last_y + BH + 24)], MUTED, "ar", 1.0)
d.box(BX + 72, last_y + BH + 24, 240, 28, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(BX + 192, last_y + BH + 42, "기타 일반 에러 (io.EOF 등)", 11, MUTED, fam=KR, anchor="middle")

# 범례 (y = 516) — 다섯 항목이 폭 960 안에 들도록 라벨을 줄인다(마지막 항목이 잘리던 문제)
d.legend(516, [
    ("정상 닫힘", OK),
    ("소켓 I/O 데드라인 (focal)", ACC),
    ("연결 수립 마감", WARN),
    ("컨텍스트·DNS", INFO),
    ("OS 시스템 콜", BAD)
])

out_name = "03-03.error-flowchart.svg"
out_path = os.path.join(os.path.dirname(__file__), "..", out_name)
d.save(out_path if os.path.exists(os.path.dirname(out_path)) else out_name)
