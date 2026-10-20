# 타입 스펙: type-sequence — 순서를 어긴 Tx1 과 Tx2 가 12-24 와 12-25 행을 교차 잠금하여 40P01 교착에 빠지는 왼쪽과, 날짜 오름차순으로 잠가 순차 대기하는 오른쪽의 대비.
# 사실 출처: 자료조사 보고서 research-A-booking.md #13(날짜 순서 불일치 교착과 ORDER BY inventory_date ASC),
#   PostgreSQL 공식 문서 transaction-iso(교착 상태 감지 및 SQLSTATE 40P01 deadlock_detected), 본문 01-01.md 5절 하위 절.
# Layout conventions: 캔버스 1000×640, 두 묶음(x = 12..488 · 512..988), 중앙 구분선 x = 500, 모든 좌표 4의 배수.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, KR, MONO

W = 1000
H = 640
MID_X = 500

d = D(
    W, H,
    "SYSTEM DESIGN COURSE · 01-01 §5",
    "날짜 순서를 어기면 교착, 지키면 줄 서기",
    "순서를 어긴 두 트랜잭션은 상호 행 잠금으로 순환 대기에 빠져 40P01 에러를 내지만, 날짜 오름차순으로 정렬하면 앞선 날짜에서 순차 대기하여 교착이 방지됩니다.",
    "복수 날짜 행을 다룰 때는 ORDER BY inventory_date ASC 로 잠금 순서를 고정합니다."
)

# 중앙 세로 구분선
d.line(MID_X, 96, MID_X, 564, RULE, 1.0, "4 4")

# =========================================================================
# 왼쪽 묶음: 순서 불일치 → 교착 상태 발생 (SQLSTATE 40P01)
# =========================================================================
L_TX1 = 140
L_TX2 = 360

d.box(24, 104, 452, 48, PAPER2, BAD, 1.2)
d.t(250, 123, "순서 미준수: 상호 대기 교착 발생", 13, BAD, KR, "middle", 600)
d.t(250, 140, "Tx1(24일→25일) ↔ Tx2(25일→24일)", 12, MUTED, KR)

# 레인 머리
d.box(L_TX1 - 40, 160, 80, 24, PAPER2, RULE, 1.0)
d.t(L_TX1, 176, "Tx1", 12, INK, KR, "middle", 600)
d.box(L_TX2 - 40, 160, 80, 24, PAPER2, RULE, 1.0)
d.t(L_TX2, 176, "Tx2", 12, INK, KR, "middle", 600)

# 레일
d.line(L_TX1, 184, L_TX1, 516, RULE, 1.0, "3 6")
d.line(L_TX2, 184, L_TX2, 516, RULE, 1.0, "3 6")

# 1. Tx1 12-24 잠금 획득
d.box(L_TX1 - 88, 196, 176, 28, PAPER2, OK, 1.0)
d.t(L_TX1, 214, "1 · 12-24 행 잠금 획득", 12, OK, KR, "middle", 600)

# 2. Tx2 12-25 잠금 획득
d.box(L_TX2 - 88, 236, 176, 28, PAPER2, OK, 1.0)
d.t(L_TX2, 254, "2 · 12-25 행 잠금 획득", 12, OK, KR, "middle", 600)

# 3. Tx1 12-25 잠금 시도 → 대기
d.path(f"M {L_TX1 + 12} 296 L {L_TX2 - 12} 296", WARN, 1.4, m="warn")
d.t(250, 287, "3 · 12-25 잠금 대기 (Tx2 점유)", 12, WARN, KR, "middle", 600)

# 4. Tx2 12-24 잠금 시도 → 대기
d.path(f"M {L_TX2 - 12} 344 L {L_TX1 + 12} 344", WARN, 1.4, m="warn")
d.t(250, 335, "4 · 12-24 잠금 대기 (Tx1 점유)", 12, WARN, KR, "middle", 600)

# 순환 대기 박스 (생명선 점선 차단용 불투명 배경)
d.box(132, 372, 236, 40, fill=PAPER2, stroke="none", r=6)
d.tone(132, 372, 236, 40, BAD, r=6, op="18", sw=1.2)
d.t(250, 389, "순환 대기 발생 (Circular Wait)", 13, BAD, KR, "middle", 600)
d.t(250, 404, "Tx1 ↔ Tx2 상호 잠금 해제 대기", 11, MUTED, KR)

# focal: PostgreSQL 교착 감지기 동작 및 40P01 에러 (생명선 점선 차단용 불투명 배경)
d.box(52, 440, 396, 68, fill=PAPER2, stroke="none", r=6)
d.tone(52, 440, 396, 68, ACC, r=6, op="18", sw=1.4)
d.t(250, 461, "PostgreSQL 교착 감지기 동작", 13, ACC, KR, "middle", 600)
d.t(250, 480, "SQLSTATE 40P01 (deadlock_detected)", 12, ACC, MONO, "middle", 600)
d.t(250, 497, "Tx2 강제 중단 및 롤백 (교착 해소)", 12, ACC, KR)

# =========================================================================
# 오른쪽 묶음: 날짜 오름차순 고정 → 순차 대기 줄 서기
# =========================================================================
R_TX1 = 640
R_TX2 = 860

d.box(524, 104, 452, 48, PAPER2, OK, 1.2)
d.t(750, 123, "날짜 오름차순 고정: 순환 대기 예방", 13, OK, KR, "middle", 600)
d.t(750, 140, "ORDER BY inventory_date ASC", 12, MUTED, MONO)

# 레인 머리
d.box(R_TX1 - 40, 160, 80, 24, PAPER2, RULE, 1.0)
d.t(R_TX1, 176, "Tx1", 12, INK, KR, "middle", 600)
d.box(R_TX2 - 40, 160, 80, 24, PAPER2, RULE, 1.0)
d.t(R_TX2, 176, "Tx2", 12, INK, KR, "middle", 600)

# 레일
d.line(R_TX1, 184, R_TX1, 516, RULE, 1.0, "3 6")
d.line(R_TX2, 184, R_TX2, 516, RULE, 1.0, "3 6")

# 1. Tx1 12-24 선점 획득
d.box(R_TX1 - 88, 196, 176, 28, PAPER2, OK, 1.0)
d.t(R_TX1, 214, "1 · 12-24 행 선점 획득", 12, OK, KR, "middle", 600)

# 2. Tx2 12-24 잠금 시도 및 줄 서기 (대기 막대)
d.path(f"M {R_TX2 - 12} 252 L {R_TX1 + 12} 252", WARN, 1.4, m="warn")
d.t(750, 243, "2 · 12-24 잠금 시도 (대기)", 12, WARN, KR, "middle", 600)

# Tx2 대기 막대 (생명선 점선 차단용 불투명 배경)
d.box(R_TX2 - 8, 264, 16, 120, fill=PAPER2, stroke="none", r=3)
d.tone(R_TX2 - 8, 264, 16, 120, WARN, r=3, op="22", sw=1.2)
d.t(R_TX2 + 18, 316, "12-24 순차 대기", 12, WARN, KR, "start", 600)
d.t(R_TX2 + 18, 334, "(줄 서기 완료)", 11, MUTED, KR, "start")

# 3. Tx1 12-25 잠금 획득 (충돌 없음)
d.box(R_TX1 - 88, 316, 176, 28, PAPER2, OK, 1.0)
d.t(R_TX1, 334, "3 · 12-25 행 잠금 획득", 12, OK, KR, "middle", 600)

# 4. Tx1 커밋 및 잠금 해제
d.box(R_TX1 - 88, 376, 176, 36, PAPER2, OK, 1.0)
d.t(R_TX1, 393, "4 · Tx1 커밋 및 잠금 해제", 12, OK, KR, "middle", 600)
d.t(R_TX1, 406, "12-24 · 12-25 갱신 완료", 11, MUTED, KR)

# 5. Tx2 대기 해제 및 순차 진행
d.path(f"M {R_TX1 + 12} 448 L {R_TX2 - 12} 448", OK, 1.4, m="ok", dash="4 4")
d.t(750, 439, "5 · 대기 해제 · 12-24 잠금 획득", 12, OK, KR, "middle", 600)

# 순차 진행 박스 (생명선 점선 차단용 불투명 배경)
d.box(684, 468, 296, 48, fill=PAPER2, stroke="none", r=6)
d.tone(684, 468, 296, 48, OK, r=6, op="18", sw=1.2)
d.t(832, 487, "순환 대기 없음 (교착 방지)", 13, OK, KR, "middle", 600)
d.t(832, 503, "12-25 순차 진행 후 정상 완료", 12, MUTED, KR)

# 범례
d.legend(588, [
    ("정상 잠금 획득 및 진행", OK),
    ("단방향 대기 (줄 서기)", WARN),
    ("순환 대기 교착 (Deadlock)", BAD),
    ("교착 감지 40P01 (focal)", ACC),
])

out_path = Path(__file__).parent.parent / "01-01.lock-order-deadlock.svg"
d.save(str(out_path))
