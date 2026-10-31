# 08-01 §2 — 다중 쓰기 실행 중 장애 발생 시 원자성 보장(abort 시 선행 쓰기 롤백)과 원자성 부재(부분 완료 오염)의 데이터 흐름 비교.
# 사실 출처: 08-01 §2(L33~L42), 원서 Ch.8 Atomicity(PDF p.4, "risks making the same change twice") 및 Figure 8-3(PDF p.10, emails 삽입 OK 뒤 mailboxes 갱신 "Error or timeout")
# 검증(10-31 cc-ddia-dverify08): 실패 칸을 Fig 8-3 의 "Error or timeout" 으로, 본문 라벨의 "(focal)" 제거, 한글 칩을 KR 로, 구역 칩이 제목 글자를 덮던 자리 수정
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY1 = 104
H_ROW = 180
PY2 = 304
LEG = 504
H = LEG + 56

d = D(W, H, "08-01 · §2 ATOMICITY & ABORT", "다중 쓰기 장애 시 원자성 보장과 롤백 흐름",
      "다중 쓰기 실행 중 오류 발생 시 선행 쓰기를 전면 폐기하는 원자성(abortability)과 부분 완료 오염의 비교.",
      "1차 쓰기 성공 · 2차 쓰기 오류 · 선행 쓰기 전면 롤백 · 깨끗한 초기 상태 보존")

SW = 188
SH = 124
GAP = 20
X0 = 36

# --- 1구역 (상단): 원자성 보장 (Atomicity / abortability) ---
d.box(24, PY1, W - 48, H_ROW, PAPER2, RULE, 1.0)
def band_chip(y, txt, c):
    w = len(txt) * 11 + 14
    d.chip(40 + w / 2, y, txt, c, 11)
    return 40 + w + 12

tx = band_chip(PY1 + 20, "원자성 보장 (트랜잭션)", OK)
d.t(tx, PY1 + 24, "오류 발생 시 선행 쓰기 전면 폐기 및 초기 상태 보존", 12, INK, KR, "start", 600)

top_steps = [
    (0, "1. 메일 삽입 성공", "emails 테이블", "INSERT into emails", "정상 반영 완료", INFO, False),
    (1, "2. 카운터 갱신 실패", "mailboxes 테이블", "UPDATE mailboxes", "오류 · 타임아웃", WARN, False),
    (2, "3. 트랜잭션 Abort", "선행 쓰기 폐기", "ROLLBACK / UNDO", "1차 emails 삽입 취소", ACC, True),
    (3, "4. 초기 상태 보존", "재시도 안전성 확보", "초기 상태 무결성 복원", "오염 없는 안전한 재시도", OK, False),
]

for col, head, sub, code_txt, desc, col_c, is_focal in top_steps:
    sx = X0 + col * (SW + GAP)
    sy = PY1 + 42
    if is_focal:
        d.box(sx, sy, SW, SH, PAPER, ACC, 1.4)
    else:
        d.box(sx, sy, SW, SH, PAPER, RULE, 0.9)
    
    d.chip(sx + 24, sy + 18, f"0{col+1}", col_c, 11)
    d.t(sx + 44, sy + 20, head, 12, INK, KR, "start", 600)
    d.t(sx + 12, sy + 38, sub, 11, SOFT, KR, "start")
    d.line(sx + 10, sy + 48, sx + SW - 10, sy + 48, RULE, 0.7)
    
    d.box(sx + 8, sy + 56, SW - 16, 28, PAPER2, RULE, 0.6)
    d.t(sx + SW / 2, sy + 74, code_txt, 11, col_c if is_focal else INK, KR if any('가' <= ch <= '힣' for ch in code_txt) else MONO, "middle", 600)
    d.t(sx + SW / 2, sy + 106, desc, 11, MUTED, KR, "middle")
    
    if col < 3:
        ax1 = sx + SW
        ax2 = sx + SW + GAP
        ay = sy + SH / 2
        d.arrow([(ax1 + 4, ay), (ax2 - 6, ay)], MUTED, "ar", 1.2)


# --- 2구역 (하단): 원자성 부재 (Partial failure) ---
d.box(24, PY2, W - 48, H_ROW, PAPER2, RULE, 1.0)
tx = band_chip(PY2 + 20, "원자성 부재 (비트랜잭션)", BAD)
d.t(tx, PY2 + 24, "부분 완료 상태 방치로 인한 데이터 불일치 및 재시도 위험", 12, INK, KR, "start", 600)

bot_steps = [
    (0, "1. 메일 삽입 성공", "emails 테이블", "INSERT into emails", "정상 반영 완료", INFO, False),
    (1, "2. 카운터 갱신 실패", "mailboxes 테이블", "UPDATE mailboxes", "오류 · 타임아웃", WARN, False),
    (2, "3. 롤백 메커니즘 부재", "중단 기능 없음", "선행 쓰기 잔존", "1차 쓰기 그대로 방치", BAD, False),
    (3, "4. 부분 완료 오염", "불일치 상태 잔존", "메일 있음 · 카운터 0", "재시도 시 중복 삽입 위험", BAD, False),
]

for col, head, sub, code_txt, desc, col_c, is_focal in bot_steps:
    sx = X0 + col * (SW + GAP)
    sy = PY2 + 42
    d.box(sx, sy, SW, SH, PAPER, BAD if col >= 2 else RULE, 1.2 if col >= 2 else 0.9)
    
    d.chip(sx + 24, sy + 18, f"0{col+1}", col_c, 11)
    d.t(sx + 44, sy + 20, head, 12, INK, KR, "start", 600)
    d.t(sx + 12, sy + 38, sub, 11, SOFT, KR, "start")
    d.line(sx + 10, sy + 48, sx + SW - 10, sy + 48, RULE, 0.7)
    
    d.box(sx + 8, sy + 56, SW - 16, 28, PAPER2, RULE, 0.6)
    d.t(sx + SW / 2, sy + 74, code_txt, 11, col_c if col >= 2 else INK, KR if any('가' <= ch <= '힣' for ch in code_txt) else MONO, "middle", 600)
    d.t(sx + SW / 2, sy + 106, desc, 11, MUTED, KR, "middle")
    
    if col < 3:
        ax1 = sx + SW
        ax2 = sx + SW + GAP
        ay = sy + SH / 2
        d.arrow([(ax1 + 4, ay), (ax2 - 6, ay)], MUTED, "ar", 1.2)


d.legend(LEG, [
    ("롤백 (focal)", ACC),
    ("정상 쓰기", OK),
    ("진행 단계", INFO),
    ("장애 경고", WARN),
    ("오염 위험", BAD),
])

d.save("08-01.atomicity-abort.svg")
