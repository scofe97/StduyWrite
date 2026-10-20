# 타입 스펙: type-pyramid — 방문자 깔때기(point down)와 상향식 실적 역산 띠를 대조하고 17 TPS 채택을 결론 칸에 둔다.
# 사실 출처: 본문 01-01.md §1(방문 1,700만·검색 170만·예약 17만 약 2 TPS 대 연 11억 room night·5.5억 예약·150만 약 17 TPS, 9배 격차, 설계 채택 17 TPS, 읽기 1,000 QPS),
#   요약 §3.5, 조사 보고서 #17, #18.
# Layout conventions: 캔버스 960×548, 깔때기 중심 CX=240, 상향식 띠 x=512..912, 결론 상자 y=392..480. 모든 좌표 4의 배수.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, SOFT, RULE, PAPER2, KR, MONO

W, H = 960, 548
d = D(
    W, H,
    "SYSTEM DESIGN COURSE · 01-01 §1",
    "방문자 깔때기와 실적 역산의 두 계산 경로",
    "방문자 전환 깔때기(약 2 TPS)와 연간 숙박 실적 역산(약 17 TPS)의 9배 격차를 대조하고 안전한 17 TPS 를 쓰기 설계 기준으로 채택합니다.",
    "하향식 깔때기(약 2 TPS) vs 상향식 실적 역산(약 17 TPS) → 17 TPS 채택 · 읽기 1,000 QPS"
)

# 1. 좌측 하향식 방문자 깔때기 (point down)
CX = 240
layers = [
    # (top_w, bot_w, y0, y1, title, sub, side_text)
    (384, 288, 116, 180, "전체 방문자: 하루 1,700만 명", "월 5억 ÷ 30일 · 초당 약 200명 진입", "100%"),
    (288, 208, 188, 252, "객실 검색: 하루 170만 명", "방문자의 10% · 탐색 및 날짜 조회", "전환율 10%"),
    (208, 144, 260, 324, "예약 결제: 하루 17만 건", "170,000 ÷ 86,400 ≈ 2/s", "전환율 1%"),
]

for top_w, bot_w, y0, y1, title, sub, side_text in layers:
    x_t1, x_t2 = CX - top_w // 2, CX + top_w // 2
    x_b1, x_b2 = CX - bot_w // 2, CX + bot_w // 2
    pts = f"{x_t1},{y0} {x_t2},{y0} {x_b2},{y1} {x_b1},{y1}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(CX, (y0 + y1) // 2 - 8, title, 14, INK, KR, "middle", 600)
    sz = 12 if "≈" in sub else 13
    d.t(CX, (y0 + y1) // 2 + 12, sub, sz, MUTED, MONO if "s" in sub or "÷" in sub else KR, "middle")
    d.t(x_t2 + 16, (y0 + y1) // 2 + 4, side_text, 13, SOFT, KR if "전환율" in side_text else MONO, "start")

# 하향식 결과 칩
d.box(140, 336, 200, 36, fill=PAPER2, stroke=INFO, sw=1.0)
d.t(240, 359, "하향식 결과: 약 2 TPS", 13, INFO, KR, "middle", 600)

# 2. 우측 상향식 실적 역산 띠
steps = [
    (116, "연간 11억 room night", "부킹 홀딩스 그룹 연간 실적 (공시치)"),
    (188, "연간 5.5억 건 예약", "평균 숙박 기간 2박 가정 (11억 ÷ 2)"),
    (260, "하루 150만 건 예약", "연간 5.5억 건 ÷ 365일 (약 17.36 TPS)"),
]

for y, title, sub in steps:
    d.box(512, y, 400, 56, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(712, y + 24, title, 14, INK, KR, "middle", 600)
    d.t(712, y + 44, sub, 13, MUTED, KR, "middle")

d.arrow([(712, 172), (712, 184)], MUTED, "ar", 1.4)
d.arrow([(712, 244), (712, 256)], MUTED, "ar", 1.4)

# 상향식 결과 칩
d.box(612, 336, 200, 36, fill=PAPER2, stroke=OK, sw=1.0)
d.t(712, 359, "상향식 결과: 약 17 TPS", 13, OK, KR, "middle", 600)

# 3. 중앙 비교 브리지
d.line(344, 354, 420, 354, RULE, 1.0)
d.chip(476, 354, "약 9배 격차", c=WARN, size=13)
d.line(532, 354, 608, 354, RULE, 1.0)

# 4. 결론 상자 (focal ACC)
d.tone(48, 388, 864, 88, ACC, r=6, op="14", sw=1.4)
d.t(480, 408, "설계 기준 채택 · 읽기-쓰기 용량 분리", 14, ACC, KR, "middle", 600)
d.line(480, 418, 480, 468, RULE, 0.8)

# 좌측 쓰기 기준
d.t(264, 434, "쓰기 기준: 17 TPS 채택 (focal)", 14, INK, KR, "middle", 600)
d.t(264, 456, "실적 기반 상향식 수치 적용 · 피크 트래픽 대비", 13, MUTED, KR, "middle")

# 우측 읽기 기준
d.t(696, 434, "읽기 기준: 약 1,000 QPS", 14, INK, KR, "middle", 600)
d.t(696, 456, "초당 200명 방문 × 방문당 백엔드 5회 조회", 13, MUTED, KR, "middle")

# 5. 범례
d.legend(496, [
    ("하향식 깔때기 (경험치)", INFO),
    ("상향식 실적 역산 (공시치)", OK),
    ("격차 비교", WARN),
    ("설계 채택 기준 (focal)", ACC),
])

out_path = Path(__file__).parent.parent / "01-01.traffic-funnel.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
