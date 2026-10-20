# 타입 스펙: type-process — 같은 재고 객체 3행을 4단계(초기·1박·2박·3박)에 걸쳐 반복 배치해 total_reserved 값 갱신과 상한 110 도달을 보인다.
# 사실 출처: 본문 01-01.md §2(호텔 42·방 타입 7·12-24 체크인 3박 1실 n=1, total_inventory 100, 10% 오버부킹 상한 110, 12-24 92→93, 12-25 108→109, 12-26 109→110 도달),
#   요약 §3.8, 조사 보고서 #3.
# Layout conventions: 캔버스 960×512, 4열 x = 36·264·492·720, 열 폭 208, 행 y = 192·248·304. 모든 좌표 4의 배수.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, ACC, OK, MUTED, INK, RULE, PAPER2, KR, MONO

W, H = 960, 512
d = D(
    W, H,
    "SYSTEM DESIGN COURSE · 01-01 §2",
    "3박 예약이 날짜별 재고 행을 하나씩 검사하고 갱신한다",
    "호텔 42 · 방 타입 7 · 3박 1실 예약 시 연속된 3개 날짜 행의 total_reserved 를 순차 검사하여 110 상한 통과 후 갱신합니다.",
    "12-24(92→93) → 12-25(108→109) → 12-26(109→110 상한 도달) → 3박 예약 확정"
)

# 예약 요청 조건 바
d.box(32, 104, 896, 36, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(480, 126, "요청: 호텔 42 · 디럭스 7 · 2026-12-24 체크인 3박 1실 (n=1)  |  정원 100 · 상한 110", 13, INK, KR, "middle", 600)

COL_XS = (32, 264, 496, 728)
CW = 212

# 열별 메타데이터 (헤더 제목, 헤더 색, 12-24 상태, 12-25 상태, 12-26 상태, 판정 텍스트, 판정 색)
COLS = [
    (
        "초기 재고 (대기)", MUTED,
        ("2026-12-24", "reserved: 92 (여유 18)", MUTED, False),
        ("2026-12-25", "reserved: 108 (여유 2)", MUTED, False),
        ("2026-12-26", "reserved: 109 (여유 1)", MUTED, False),
        "검사 대기 (3박)", MUTED,
    ),
    (
        "1단계: 12-24 검사", OK,
        ("2026-12-24", "92 → 93 갱신", OK, True),
        ("2026-12-25", "reserved: 108 (대기)", MUTED, False),
        ("2026-12-26", "reserved: 109 (대기)", MUTED, False),
        "92 + 1 ≤ 110 (통과)", OK,
    ),
    (
        "2단계: 12-25 검사", OK,
        ("2026-12-24", "reserved: 93 (완료)", MUTED, False),
        ("2026-12-25", "108 → 109 갱신", OK, True),
        ("2026-12-26", "reserved: 109 (대기)", MUTED, False),
        "108 + 1 ≤ 110 (통과)", OK,
    ),
    (
        "3단계: 12-26 검사 (focal)", ACC,
        ("2026-12-24", "reserved: 93 (완료)", MUTED, False),
        ("2026-12-25", "reserved: 109 (완료)", MUTED, False),
        ("2026-12-26", "109 → 110 도달", ACC, True),
        "109 + 1 = 110 (상한 도달)", ACC,
    ),
]

ROW_YS = (192, 248, 304)

for i, (col_title, col_c, r1, r2, r3, eval_txt, eval_c) in enumerate(COLS):
    x = COL_XS[i]

    # 열 헤더
    d.box(x, 152, CW, 32, fill=PAPER2, stroke=col_c, sw=1.2 if col_c == ACC else 1.0)
    d.t(x + CW // 2, 172, col_title, 13, col_c, KR, "middle", 600)

    # 3개 날짜 행
    for y, (d_str, val_str, c, is_active) in zip(ROW_YS, (r1, r2, r3)):
        if is_active:
            d.tone(x, y, CW, 48, c, r=6, op="18" if c == ACC else "14", sw=1.4 if c == ACC else 1.2)
            d.t(x + 12, y + 20, d_str, 13, c, MONO, "start", 600)
            d.t(x + 12, y + 38, val_str, 13, c, KR, "start", 600)
        else:
            d.box(x, y, CW, 48, fill=PAPER2, stroke=RULE, sw=1.0)
            d.t(x + 12, y + 20, d_str, 13, INK, MONO, "start", 600)
            d.t(x + 12, y + 38, val_str, 13, MUTED, KR, "start")

    # 검사 판정 알약
    d.box(x, 360, CW, 32, fill=PAPER2, stroke=eval_c, sw=1.2 if eval_c == ACC else 1.0)
    d.t(x + CW // 2, 381, eval_txt, 13, eval_c, KR, "middle", 600)

# 헤더 간 수평 연결 화살표
for i in range(3):
    x_from = COL_XS[i] + CW + 2
    x_to = COL_XS[i + 1] - 6
    d.arrow([(x_from, 168), (x_to, 168)], MUTED, "ar", 1.4)

# 최종 결과 바
d.box(32, 404, 896, 40, fill=PAPER2, stroke=OK, sw=1.2)
d.t(480, 428, "검증 완료: 3개 날짜 행 모두 통과 · reservations CONFIRMED 커밋", 13, OK, KR, "middle", 600)

# 범례
d.legend(464, [
    ("대기 / 이전 완료", MUTED),
    ("검사 통과 갱신", OK),
    ("오버부킹 상한 110 도달 (focal)", ACC),
])

out_path = Path(__file__).parent.parent / "01-01.inventory-rows.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
