# 타입 스펙: type-sequence — 두 트랜잭션 Tx1 과 Tx2 가 2026-12-26 재고 행의 109 를 동시에 읽고 통과한 뒤 순차 갱신하여 111 로 상한 110 을 초과하는 경쟁 조건.
# 사실 출처: 강의 요약 §3.9(read committed 경쟁 조건과 한도 초과), 자료조사 보고서 research-A-booking.md #6(PostgreSQL 최신 행 버전 재평가),
#   본문 01-01.md 4절(100실 정원, 110% 오버부킹 상한 110, 현재 109에서 동시 진입 시 111 초과).
# Layout conventions: 캔버스 960×580, 레인 셋(Tx1 · 재고 행 · Tx2), x = 180 · 480 · 780, 모든 좌표 4의 배수.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W = 960
H = 580
Y0 = 104
LANE_W = 200
ROW_W = 220
TX1_X = 180
ROW_X = 480
TX2_X = 780
RAIL_BOT = 504

d = D(
    W, H,
    "SYSTEM DESIGN COURSE · 01-01 §4",
    "두 트랜잭션이 109 를 함께 읽고 둘 다 통과한다",
    "read committed 격리 수준에서 두 트랜잭션이 잔여 재고 109 를 동시에 확인하고 각각 1 씩 더해 커밋하여 상한 110 을 초과한 111 이 되는 경쟁 조건",
    "가용성 검증과 갱신 사이 시간차로 두 트랜잭션 모두 통과해 정원을 초과합니다."
)

# 1. 참여자 레인 머리
d.box(TX1_X - LANE_W // 2, Y0, LANE_W, 44, PAPER2, RULE, 1.0)
d.t(TX1_X, Y0 + 19, "Tx1 (사용자 A)", 13, INK, KR, "middle", 600)
d.t(TX1_X, Y0 + 36, "트랜잭션 1", 12, MUTED, KR)

d.box(ROW_X - ROW_W // 2, Y0, ROW_W, 44, PAPER2, INFO, 1.2)
d.t(ROW_X, Y0 + 19, "재고 행 (2026-12-26)", 13, INK, KR, "middle", 600)
d.t(ROW_X, Y0 + 36, "정원 100 · 상한 110", 12, INFO, KR)

d.box(TX2_X - LANE_W // 2, Y0, LANE_W, 44, PAPER2, RULE, 1.0)
d.t(TX2_X, Y0 + 19, "Tx2 (사용자 B)", 13, INK, KR, "middle", 600)
d.t(TX2_X, Y0 + 36, "트랜잭션 2", 12, MUTED, KR)

# 2. 생명선 레일
d.line(TX1_X, Y0 + 44, TX1_X, RAIL_BOT, RULE, 1.0, "3 6")
d.line(ROW_X, Y0 + 44, ROW_X, RAIL_BOT, RULE, 1.0, "3 6")
d.line(TX2_X, Y0 + 44, TX2_X, RAIL_BOT, RULE, 1.0, "3 6")

# 3. 초기 재고 상태
d.box(ROW_X - 104, 164, 208, 36, PAPER2, RULE, 1.0)
d.t(ROW_X, 179, "초기 total_reserved: 109", 13, INK, KR, "middle", 600)
d.t(ROW_X, 193, "잔여 1실 (상한까지 여유 1실)", 12, MUTED, KR, "middle")

# 4. Tx1 잔여 재고 조회 및 통과
d.path(f"M {TX1_X + 12} 216 L {ROW_X - 108} 216", MUTED, 1.4, m="ar")
d.t((TX1_X + ROW_X - 104) // 2, 206, "1 · SELECT 잔여 재고", 13, MUTED, KR, "middle", 600)

d.path(f"M {ROW_X - 108} 244 L {TX1_X + 12} 244", MUTED, 1.4, m="ar", dash="4 4")
d.t((TX1_X + ROW_X - 104) // 2, 234, "2 · 109 반환 (잔여 1실)", 13, MUTED, KR, "middle", 600)

d.box(TX1_X - 84, 256, 168, 26, PAPER2, OK, 1.0)
d.t(TX1_X, 273, "109 + 1 ≤ 110 (통과)", 13, OK, KR, "middle", 600)

# 5. Tx2 동시 조회 및 통과
d.path(f"M {TX2_X - 12} 288 L {ROW_X + 108} 288", MUTED, 1.4, m="ar")
d.t((TX2_X + ROW_X + 104) // 2, 278, "1 · SELECT 잔여 재고", 13, MUTED, KR, "middle", 600)

d.path(f"M {ROW_X + 108} 316 L {TX2_X - 12} 316", MUTED, 1.4, m="ar", dash="4 4")
d.t((TX2_X + ROW_X + 104) // 2, 306, "2 · 109 반환 (잔여 1실)", 13, MUTED, KR, "middle", 600)

d.box(TX2_X - 84, 328, 168, 26, PAPER2, OK, 1.0)
d.t(TX2_X, 345, "109 + 1 ≤ 110 (통과)", 13, OK, KR, "middle", 600)

# 6. Tx1 갱신 및 커밋
d.path(f"M {TX1_X + 12} 364 L {ROW_X - 108} 364", OK, 1.4, m="ok")
d.t((TX1_X + ROW_X - 104) // 2, 354, "3 · UPDATE (+1) 및 커밋", 13, OK, KR, "middle", 600)

d.box(ROW_X - 104, 376, 208, 40, PAPER2, OK, 1.0)
d.t(ROW_X, 393, "total_reserved: 109 → 110", 13, OK, KR, "middle", 600)
d.t(ROW_X, 408, "Tx1 커밋 완료 (상한선 도달)", 12, MUTED, KR, "middle")

# 7. Tx2 갱신 및 상한 초과 (focal)
d.path(f"M {TX2_X - 12} 432 L {ROW_X + 108} 432", BAD, 1.4, m="bad")
d.t((TX2_X + ROW_X + 104) // 2, 422, "4 · 최신 행 재평가 UPDATE", 13, BAD, KR, "middle", 600)

# focal: 상한 초과 박스
d.tone(ROW_X - 108, 448, 216, 44, ACC, r=6, op="18", sw=1.4)
d.t(ROW_X, 467, "total_reserved: 110 → 111", 13, ACC, KR, "middle", 600)
d.t(ROW_X, 483, "상한 110 초과 (초과 예약 발생)", 12, ACC, KR, "middle")

# 8. 범례
d.legend(528, [
    ("가용 재고 확인 (정상 통과)", OK),
    ("최신 행 재평가 갱신", BAD),
    ("상한 초과 발생 (focal)", ACC),
])

out_path = Path(__file__).parent.parent / "01-01.last-room-race.svg"
d.save(str(out_path))
