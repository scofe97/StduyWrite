# 14-01 §4 — 피드백 루프와 시스템 사고: 신용 점수와 채용 평가가 만드는 자기강화 하향 나선과 시스템 사고의 결과 예측.
# 사실 출처: 14-01 본문 §4(L64~L73), 원서 Ch.14 "Feedback Loops" (PDF p.5 신용 점수·채용 예, p.6 systems thinking)
# 10-31 검증(cc-ddia-dverify14): 되먹임을 원서대로 빈곤→점수 하락(4→2)으로, 단편 시각 상자 색을 범례(SOFT)에 맞춤, 원서에 없는 '알고리즘 위험 분류'·'부분 최적화'·'악순환 차단' 제거
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, WARN, BAD, OK, KR, MONO

W = 840
BANNER_Y = 96
BANNER_H = 42
Y_PANEL = 154
H_PANEL = 236
LEG = 412
H = LEG + 52

d = D(W, H, "14-01 · §4 FEEDBACK LOOP", "신용 점수 하향 나선과 시스템 사고",
      "예측 분석이 개인의 행동과 삶을 제약하고 다시 악화된 입력으로 되먹임되는 자기강화 하향 나선과 시스템 사고.",
      "통제 밖 불운 · 신용 점수 하락 · 구직 어려움 · 실직과 빈곤 · 점수 추가 하락 · 시스템 사고")

# 상단 공통 전제 배너 (중립 박스 적용으로 범례 색상 불일치 방지)
d.box(24, BANNER_Y, W - 48, BANNER_H, PAPER2, RULE, 1.0)
d.t(W / 2, BANNER_Y + 17, "자기강화 피드백 루프: 예측이 바꾼 행동이 다시 예측의 입력", 13, INK, KR, "middle", 600)
d.t(W / 2, BANNER_Y + 33, "수학적 엄밀함의 위장 뒤 독성 가정 · 사람까지 포함한 전체 시스템", 12, MUTED, KR, "middle")

# 좌측 패널: 자기강화 하향 나선 (BAD)
PW_LEFT = 430
d.tone(24, Y_PANEL, PW_LEFT, H_PANEL, BAD, 6, "10", 1.2)
d.chip(24 + PW_LEFT / 2, Y_PANEL + 16, "자기강화 하향 나선 (신용 점수 → 채용 예시)", BAD, 11, pad=6)

# 4개 노드 배치 (NW=160, GAP=60, 상단 2개, 하단 2개)
NW = 160
NH = 50
X_N1 = 44
X_N2 = X_N1 + NW + 60  # 264
Y_N_TOP = 194
Y_N_BOT = 286

# 노드 1: 통제 밖의 불운
d.box(X_N1, Y_N_TOP, NW, NH, PAPER, WARN, 0.8, r=4)
d.t(X_N1 + NW / 2, Y_N_TOP + 20, "1. 통제 밖의 불운", 12, WARN, KR, "middle", 600)
d.t(X_N1 + NW / 2, Y_N_TOP + 38, "재정 곤란 · 청구서 연체", 11, MUTED, KR, "middle")

# 노드 2: 신용 점수 하락
d.box(X_N2, Y_N_TOP, NW, NH, PAPER, WARN, 0.8, r=4)
d.t(X_N2 + NW / 2, Y_N_TOP + 20, "2. 신용 점수 하락", 12, WARN, KR, "middle", 600)
d.t(X_N2 + NW / 2, Y_N_TOP + 38, "연체가 점수에 반영", 11, MUTED, KR, "middle")

# 노드 3: 고용 평가 탈락
d.box(X_N2, Y_N_BOT, NW, NH, PAPER, BAD, 0.8, r=4)
d.t(X_N2 + NW / 2, Y_N_BOT + 20, "3. 구직 어려움", 12, BAD, KR, "middle", 600)
d.t(X_N2 + NW / 2, Y_N_BOT + 38, "고용주의 신용 점수 평가", 11, MUTED, KR, "middle")

# 노드 4: 실직과 빈곤 심화
d.box(X_N1, Y_N_BOT, NW, NH, PAPER, BAD, 0.8, r=4)
d.t(X_N1 + NW / 2, Y_N_BOT + 20, "4. 실직과 빈곤", 12, BAD, KR, "middle", 600)
d.t(X_N1 + NW / 2, Y_N_BOT + 38, "실직이 빈곤으로", 11, MUTED, KR, "middle")

# 연결 화살표: 1 → 2 (간격 60px 내부 중앙 배치)
d.arrow([(X_N1 + NW, Y_N_TOP + NH / 2), (X_N2, Y_N_TOP + NH / 2)], c=WARN, m="warn", sw=1.4)
d.t((X_N1 + NW + X_N2) / 2, Y_N_TOP + NH / 2 - 8, "연체", 11, SOFT, KR, "middle")

# 연결 화살표: 2 → 3
d.arrow([(X_N2 + NW / 2, Y_N_TOP + NH), (X_N2 + NW / 2, Y_N_BOT)], c=BAD, m="bad", sw=1.4)
d.t(X_N2 + NW / 2 + 36, (Y_N_TOP + NH + Y_N_BOT) / 2 + 4, "채용 평가", 11, SOFT, KR, "middle")

# 연결 화살표: 3 → 4 (하단 우회 경로로 텍스트 간섭 완전 차단)
Y_ROUTE = Y_N_BOT + NH + 16
d.path(f"M {X_N2 + NW / 2} {Y_N_BOT + NH} L {X_N2 + NW / 2} {Y_ROUTE} L {X_N1 + NW / 2} {Y_ROUTE} L {X_N1 + NW / 2} {Y_N_BOT + NH + 6}", c=BAD, sw=1.4, m="bad")
d.t((X_N1 + NW + X_N2) / 2, Y_ROUTE - 6, "실직", 11, SOFT, KR, "middle")

# 되먹임 화살표: 4 → 2 (원서 p.5: 빈곤이 점수를 더 낮춘다. 1 은 루프 밖 시작점)
X_RET = X_N1 + NW + 30
Y_IN2 = Y_N_TOP + NH - 10
d.path(f"M {X_N1 + NW} {Y_N_BOT + NH / 2} L {X_RET} {Y_N_BOT + NH / 2} L {X_RET} {Y_IN2} L {X_N2 - 6} {Y_IN2}", c=BAD, sw=1.6, m="bad", dash="4 3")
d.t(X_RET - 8, (Y_N_TOP + NH + Y_N_BOT) / 2 + 4, "점수 추가 하락", 11, BAD, KR, "end")

# 우측 패널: 시스템 사고 관점 대비
PX_RIGHT = 474
PW_RIGHT = 342
d.box(PX_RIGHT, Y_PANEL, PW_RIGHT, H_PANEL, PAPER2, RULE, 1.0)
d.chip(PX_RIGHT + PW_RIGHT / 2, Y_PANEL + 16, "시스템 사고 관점 대비", SOFT, 11, pad=6)

# 우측 상단 박스: 좁은 전산 시각
d.box(PX_RIGHT + 14, Y_PANEL + 38, PW_RIGHT - 28, 66, PAPER, SOFT, 0.8, r=4)
d.chip(PX_RIGHT + PW_RIGHT / 2, Y_PANEL + 50, "전산화된 부분만", SOFT, 11, pad=4)
d.t(PX_RIGHT + 28, Y_PANEL + 72, "상호작용하는 사람은 시야 밖", 11, MUTED, KR, "start")
d.t(PX_RIGHT + 28, Y_PANEL + 90, "예측이 바꾼 사람 행동 누락", 11, MUTED, KR, "start")

# 우측 상단 → 하단 관점 전환 화살표 (20px 연결선으로 short 경고 방지)
d.arrow([(PX_RIGHT + PW_RIGHT / 2, Y_PANEL + 104), (PX_RIGHT + PW_RIGHT / 2, Y_PANEL + 124)], c=OK, m="ok", sw=1.2)
d.t(PX_RIGHT + PW_RIGHT / 2 + 36, Y_PANEL + 116, "관점 전환", 11, OK, KR, "middle")

# 우측 하단 박스: 확장된 전체 시스템 사고
d.tone(PX_RIGHT + 14, Y_PANEL + 124, PW_RIGHT - 28, 92, OK, 4, "12", 1.2)
d.chip(PX_RIGHT + PW_RIGHT / 2, Y_PANEL + 140, "시스템 사고 (systems thinking)", OK, 11, pad=4)
d.t(PX_RIGHT + 28, Y_PANEL + 162, "상호작용하는 사람까지 전체 시스템", 11, INK, KR, "start")
d.t(PX_RIGHT + 28, Y_PANEL + 180, "기존 격차를 강화·증폭하는지 점검", 11, INK, KR, "start")
d.t(PX_RIGHT + 28, Y_PANEL + 198, "많은 결과 사전 예측 (항상은 아님)", 11, OK, KR, "start")

# 범례
d.legend(LEG, [
    ("불운·점수 하락", WARN),
    ("구직·빈곤 악순환 (focal)", BAD),
    ("전산화된 부분만", SOFT),
    ("전체 시스템 사고", OK)
])

d.save("14-01.feedback-loop.svg")
