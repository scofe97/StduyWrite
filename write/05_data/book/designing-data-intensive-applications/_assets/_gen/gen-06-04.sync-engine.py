# 06-04 §3 — sync engine과 local-first 아키텍처 (장치 로컬 DB 리더 동작 및 비동기 동기화).
# 사실 출처: 06-04 §3(L60~L73), DDIA 2판 6장 "Sync Engines and Local-First Software"
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 580
LEG = H - 46

d = D(W, H, "06-04 · SYNC ENGINES & LOCAL-FIRST", "sync engine과 local-first 아키텍처",
      "각 기기·탭이 로컬 DB를 리더로 삼아 즉각 응답하고, sync engine을 통해 비동기 복제하는 구조.",
      "로컬 DB 리더 동작 · 16ms 즉각 UI 렌더링 · 오프라인 작업 · local-first")

Y_BOX = 104
H_BOX = 330

# 1. 좌측: 사용자 기기 A (로컬 리더)
X_A = 24
W_DEV = 270
d.box(X_A, Y_BOX, W_DEV, H_BOX, PAPER2, RULE, 0.9)
d.t(X_A + 16, Y_BOX + 24, "사용자 기기 A (Local Leader)", 12, SOFT, KR, "start", 600)

# 기기 A: UI 계층
d.box(X_A + 16, Y_BOX + 42, W_DEV - 32, 60, PAPER, INFO, 1.0)
d.t(X_A + W_DEV / 2, Y_BOX + 64, "사용자 인터페이스 (UI)", 13, INK, KR, "middle", 600)
d.t(X_A + W_DEV / 2, Y_BOX + 84, "16ms 즉각 화면 반영 (네트워크 무대기)", 12, INFO, KR, "middle")

# UI <-> 로컬 DB 화살표 (수직)
d.arrow([(X_A + W_DEV / 2 - 20, Y_BOX + 104), (X_A + W_DEV / 2 - 20, Y_BOX + 132)], OK, "ok", 1.2)
d.arrow([(X_A + W_DEV / 2 + 20, Y_BOX + 132), (X_A + W_DEV / 2 + 20, Y_BOX + 104)], OK, "ok", 1.2)

# 기기 A: 로컬 DB (리더 역할)
d.tone(X_A + 16, Y_BOX + 134, W_DEV - 32, 64, ACC, 6, "22", 1.2)
d.t(X_A + W_DEV / 2, Y_BOX + 158, "로컬 데이터베이스 (Local DB)", 13, INK, KR, "middle", 600)
d.t(X_A + W_DEV / 2, Y_BOX + 178, "리더 역할 · 로컬 데이터에 읽기·쓰기", 12, ACC, KR, "middle")

# 로컬 DB <-> Sync Engine 화살표 (수직)
d.arrow([(X_A + W_DEV / 2 - 20, Y_BOX + 200), (X_A + W_DEV / 2 - 20, Y_BOX + 228)], WARN, "warn", 1.2)
d.arrow([(X_A + W_DEV / 2 + 20, Y_BOX + 228), (X_A + W_DEV / 2 + 20, Y_BOX + 200)], WARN, "warn", 1.2)

# 기기 A: Sync Engine
d.box(X_A + 16, Y_BOX + 230, W_DEV - 32, 64, PAPER, WARN, 1.1)
d.t(X_A + W_DEV / 2, Y_BOX + 254, "동기화 엔진 (Sync Engine)", 13, INK, KR, "middle", 600)
d.t(X_A + W_DEV / 2, Y_BOX + 274, "오프라인 변경을 로컬에 보관", 12, WARN, KR, "middle")


# 2. 중앙: 네트워크 및 동기화 브로커
X_MID = 314
W_MID = 252
d.box(X_MID, Y_BOX, W_MID, H_BOX, PAPER2, RULE, 0.9)
d.t(X_MID + W_MID / 2, Y_BOX + 24, "인터넷 (연결이 극히 불안정)", 12, SOFT, KR, "middle", 600)

# 네트워크 단절/오프라인 안내 배너
d.tone(X_MID + 12, Y_BOX + 42, W_MID - 24, 76, OK, 4, "12", 1.0)
d.t(X_MID + W_MID / 2, Y_BOX + 68, "오프라인 연속 작업", 12, OK, KR, "middle", 600)
d.t(X_MID + W_MID / 2, Y_BOX + 88, "네트워크 단절 중에도 로컬 진행", 12, INK, KR, "middle")
d.t(X_MID + W_MID / 2, Y_BOX + 104, "단절은 극단적 복제 지연과 동일", 11, MUTED, KR, "middle")

# 중앙 브로커/서버 박스
d.box(X_MID + 12, Y_BOX + 134, W_MID - 24, 64, PAPER, RULE, 0.9)
d.t(X_MID + W_MID / 2, Y_BOX + 158, "기기마다 하나의 리전", 12, INK, KR, "middle", 600)
d.t(X_MID + W_MID / 2, Y_BOX + 178, "복제 지연이 시간·날일 수 있음", 12, MUTED, KR, "middle")

# 양방향 동기화 스트림 화살표 (기기 A <-> 중앙 릴레이)
d.arrow([(X_A + W_DEV - 16, Y_BOX + 262), (X_MID + 12, Y_BOX + 262)], WARN, "warn", 1.3, dash="4 3")
d.arrow([(X_MID + 12, Y_BOX + 278), (X_A + W_DEV - 16, Y_BOX + 278)], WARN, "warn", 1.3, dash="4 3")

# 양방향 동기화 스트림 화살표 (중앙 릴레이 <-> 기기 B)
d.arrow([(X_MID + W_MID - 12, Y_BOX + 262), (X_B_POS := 586, Y_BOX + 262)], WARN, "warn", 1.3, dash="4 3")
d.arrow([(X_B_POS, Y_BOX + 278), (X_MID + W_MID - 12, Y_BOX + 278)], WARN, "warn", 1.3, dash="4 3")

d.t(X_MID + W_MID / 2, Y_BOX + 248, "갱신을 비동기로 복제", 12, ACC, KR, "middle", 600)
d.t(X_MID + W_MID / 2, Y_BOX + 296, "다음 온라인 때 동기화", 11, SOFT, KR, "middle")


# 3. 우측: 사용자 기기 B (협업 피어 리더)
X_B = 586
d.box(X_B, Y_BOX, W_DEV, H_BOX, PAPER2, RULE, 0.9)
d.t(X_B + 16, Y_BOX + 24, "사용자 기기 B (Local Leader)", 12, SOFT, KR, "start", 600)

# 기기 B: UI 계층
d.box(X_B + 16, Y_BOX + 42, W_DEV - 32, 60, PAPER, INFO, 1.0)
d.t(X_B + W_DEV / 2, Y_BOX + 64, "사용자 인터페이스 (UI)", 13, INK, KR, "middle", 600)
d.t(X_B + W_DEV / 2, Y_BOX + 84, "반응형 상태 갱신 · 협업자 편집 표시", 12, INFO, KR, "middle")

# UI <-> 로컬 DB 화살표 (수직)
d.arrow([(X_B + W_DEV / 2 - 20, Y_BOX + 104), (X_B + W_DEV / 2 - 20, Y_BOX + 132)], OK, "ok", 1.2)
d.arrow([(X_B + W_DEV / 2 + 20, Y_BOX + 132), (X_B + W_DEV / 2 + 20, Y_BOX + 104)], OK, "ok", 1.2)

# 기기 B: 로컬 DB (리더 역할)
d.tone(X_B + 16, Y_BOX + 134, W_DEV - 32, 64, ACC, 6, "22", 1.2)
d.t(X_B + W_DEV / 2, Y_BOX + 158, "로컬 데이터베이스 (Local DB)", 13, INK, KR, "middle", 600)
d.t(X_B + W_DEV / 2, Y_BOX + 178, "리더 역할 · 다른 기기의 갱신 반영", 12, ACC, KR, "middle")

# 로컬 DB <-> Sync Engine 화살표 (수직)
d.arrow([(X_B + W_DEV / 2 - 20, Y_BOX + 200), (X_B + W_DEV / 2 - 20, Y_BOX + 228)], WARN, "warn", 1.2)
d.arrow([(X_B + W_DEV / 2 + 20, Y_BOX + 228), (X_B + W_DEV / 2 + 20, Y_BOX + 200)], WARN, "warn", 1.2)

# 기기 B: Sync Engine
d.box(X_B + 16, Y_BOX + 230, W_DEV - 32, 64, PAPER, WARN, 1.1)
d.t(X_B + W_DEV / 2, Y_BOX + 254, "동기화 엔진 (Sync Engine)", 13, INK, KR, "middle", 600)
d.t(X_B + W_DEV / 2, Y_BOX + 274, "협업자 편집을 낮은 지연으로 수신", 12, WARN, KR, "middle")


# 4. 하단 장단점/한계 카드
Y_BOT = 450
H_BOT = 48

d.box(24, Y_BOT, 404, H_BOT, PAPER2, OK, 1.1)
d.t(40, Y_BOT + 29, "핵심 장점", 12, OK, KR, "start", 600)
d.t(104, Y_BOT + 29, "16ms 즉시 UI 반응 · 오프라인 지속 · 단순 모델", 12, INK, KR, "start")

d.box(452, Y_BOT, 404, H_BOT, PAPER2, WARN, 1.1)
d.t(468, Y_BOT + 29, "적용 한계", 12, WARN, KR, "start", 600)
d.t(532, Y_BOT + 29, "필요 데이터를 미리 로컬에 · 전체 상품 카탈로그는 무리", 12, INK, KR, "start")


# 범례
d.legend(LEG, [("UI 반응성", INFO), ("로컬 DB (리더)", ACC), ("sync engine 동기화", WARN), ("오프라인·local-first", OK)])
d.save("06-04.sync-engine.svg")
