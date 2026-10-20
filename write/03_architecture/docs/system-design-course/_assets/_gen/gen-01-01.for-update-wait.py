# 타입 스펙: type-sequence — Tx1 이 SELECT FOR UPDATE 로 배타 잠금을 획득하면 Tx2 가 대기하고, Tx1 커밋 후 110 을 확인한 Tx2 가 매진으로 거절되어 롤백하는 흐름.
# 사실 출처: 강의 요약 §3.9(FOR UPDATE 와 serializable 비교), 자료조사 보고서 research-A-booking.md #11·#12(PostgreSQL 행 잠금 대기 및 최신 행 버전 평가),
#   본문 01-01.md 5절(배타적 행 잠금 획득, 대기 후 110 확인, 매진 안내 및 안전한 롤백).
# Layout conventions: 캔버스 960×600, 레인 셋(Tx1 · 재고 행 · Tx2), x = 180 · 480 · 780, 대기 막대 폭 16, 모든 좌표 4의 배수.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W = 960
H = 600
Y0 = 104
LANE_W = 200
ROW_W = 220
TX1_X = 180
ROW_X = 480
TX2_X = 780
RAIL_BOT = 528

d = D(
    W, H,
    "SYSTEM DESIGN COURSE · 01-01 §5",
    "FOR UPDATE 로 두 번째 트랜잭션이 기다린 뒤 110 을 보고 거절된다",
    "Tx1 이 SELECT FOR UPDATE 로 배타 잠금을 획득해 Tx2 가 대기하고, Tx1 이 110 으로 커밋한 뒤 110 을 읽은 Tx2 가 상한 초과로 거절되어 롤백하는 흐름",
    "같은 재고 행 갱신을 한 줄로 세워 상한 초과 방지"
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

# 4. Tx1 SELECT FOR UPDATE 및 배타 잠금 획득
d.path(f"M {TX1_X + 12} 216 L {ROW_X - 108} 216", OK, 1.4, m="ok")
d.t((TX1_X + ROW_X - 104) // 2, 206, "1 · SELECT FOR UPDATE", 13, OK, KR, "middle", 600)

d.box(ROW_X - 104, 236, 208, 36, PAPER2, OK, 1.0)
d.t(ROW_X, 251, "배타 잠금 획득 (X-Lock)", 12, OK, KR, "middle", 600)
d.t(ROW_X, 265, "행 잠금 완료 · 109 반환", 12, MUTED, KR, "middle")

d.path(f"M {ROW_X - 108} 244 L {TX1_X + 12} 244", OK, 1.4, m="ok", dash="4 4")

# 5. Tx2 SELECT FOR UPDATE 시도 및 대기 (막대)
d.path(f"M {TX2_X - 12} 292 L {ROW_X + 108} 292", WARN, 1.4, m="warn")
d.t((TX2_X + ROW_X + 104) // 2, 282, "2 · SELECT FOR UPDATE 시도", 13, WARN, KR, "middle", 600)

d.box(ROW_X - 104, 308, 208, 36, PAPER2, WARN, 1.0)
d.t(ROW_X, 323, "잠금 충돌 · 대기 큐 등록", 12, WARN, KR, "middle", 600)
d.t(ROW_X, 337, "Tx1 커밋 완료 시점까지 보류", 12, MUTED, KR, "middle")

# Tx2 대기 막대 (Lock Wait) — 폭 16 슬림 막대 + 우측 라벨
d.tone(TX2_X - 8, 304, 16, 120, WARN, r=3, op="22", sw=1.2)
d.t(TX2_X + 18, 356, "잠금 대기", 13, WARN, KR, "start", 600)
d.t(TX2_X + 18, 374, "Lock Wait", 12, WARN, MONO, "start")

# 6. Tx1 갱신 및 커밋
d.path(f"M {TX1_X + 12} 372 L {ROW_X - 108} 372", OK, 1.4, m="ok")
d.t((TX1_X + ROW_X - 104) // 2, 362, "3 · UPDATE (+1) 및 커밋", 13, OK, KR, "middle", 600)

d.box(ROW_X - 104, 380, 208, 40, PAPER2, OK, 1.0)
d.t(ROW_X, 397, "total_reserved: 109 → 110", 13, OK, KR, "middle", 600)
d.t(ROW_X, 412, "Tx1 커밋 완료 · 행 잠금 해제", 12, MUTED, KR, "middle")

# 7. 대기 해제 및 Tx2 최신 값 110 반환
d.path(f"M {ROW_X + 108} 448 L {TX2_X - 12} 448", WARN, 1.4, m="warn", dash="4 4")
d.t((TX2_X - 12 + ROW_X + 108) // 2, 438, "4 · 대기 해제 · 최신 110 반환", 13, WARN, KR, "middle", 600)

# 8. Tx2 상한 초과 감지 및 거절 (focal)
d.tone(TX2_X - 104, 468, 208, 48, ACC, r=6, op="18", sw=1.4)
d.t(TX2_X, 487, "110 + 1 = 111 > 110 (매진)", 13, ACC, KR, "middle", 600)
d.t(TX2_X, 505, "예약 거절 및 롤백 (초과 방지)", 12, ACC, KR, "middle")

# 9. 범례
d.legend(548, [
    ("배타 잠금 획득 및 커밋", OK),
    ("행 잠금 대기 (Lock Wait)", WARN),
    ("매진 감지 및 예약 거절 (focal)", ACC),
])

out_path = Path(__file__).parent.parent / "01-01.for-update-wait.svg"
d.save(str(out_path))
