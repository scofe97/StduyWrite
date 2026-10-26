"""백그라운드 작업 실행부터 대화 병행 및 완료 통지 수신 시간 관계."""
# 타입 스펙: type-gantt
# 사실 출처: 05-03.Background Tasks.md:60-108 · 원문 09-advanced-features/README.md:582-656
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 960, 460
LABEL_W = 190
X_START = 210
X_END = 920
TIMELINE_W = X_END - X_START  # 710px
TOTAL_MIN = 10.0

def x_at(minute):
    return X_START + (minute / TOTAL_MIN) * TIMELINE_W

d = D(
    W, H,
    "BACKGROUND TASKS · TIMELINE RELATION",
    "백그라운드 작업 실행과 대화 병행 시간 관계",
    "테스트와 린트 작업이 비동기로 실행되는 동안 대화 세션이 차단 없이 이어지고 완료 통지가 끼어드는 흐름",
    lead="오래 걸리는 명령을 백그라운드로 전환하여 대화 흐름을 유지하고 완료 시 알림을 수신합니다 (ID·수치는 예)",
)

# 1. 시간 눈금 헤더
Y_AXIS = 100
d.line(X_START, Y_AXIS + 16, X_END, Y_AXIS + 16, RULE, 0.8)
for m in [0, 2, 4, 6, 8, 10]:
    xm = x_at(m)
    d.line(xm, Y_AXIS + 12, xm, Y_AXIS + 16, RULE, 0.8)
d.t(X_START, Y_AXIS + 6, "시작", 11, SOFT, KR, "start")
d.t(X_END, Y_AXIS + 6, "경과 시간", 11, SOFT, KR, "end")

# 2. 페이즈 영역 배경 (subtle zone rect)
# Phase 1: 포그라운드 대화 세션
P1_Y = 126
P1_H = 152
d.box(16, P1_Y, W - 32, P1_H, fill=f"{INK}04", stroke=RULE, sw=0.6, r=6)
d.t(28, P1_Y + 18, "SESSION", 8, SOFT, MONO, "start", 600)
d.t(96, P1_Y + 18, "포그라운드 대화", 11, MUTED, KR, "start", 600)

# Phase 2: 비동기 백그라운드 프로세스
P2_Y = 286
P2_H = 88
d.box(16, P2_Y, W - 32, P2_H, fill=f"{INK}04", stroke=RULE, sw=0.6, r=6)
d.t(28, P2_Y + 18, "BACKGROUND", 8, SOFT, MONO, "start", 600)
d.t(112, P2_Y + 18, "비동기 작업", 11, MUTED, KR, "start", 600)

# 세로 그리드 가이드라인 (Phase 내부)
for m in [2, 4, 6, 8]:
    xm = x_at(m)
    d.line(xm, P1_Y + 24, xm, P1_Y + P1_H - 8, RULE, 0.5, "2 4")
    d.line(xm, P2_Y + 24, xm, P2_Y + P2_H - 8, RULE, 0.5, "2 4")

# 3. 작업 행 정의 (label, sub, start_m, end_m, focal, color, bar_text)
tasks = [
    # Phase 1: 대화 세션 행
    ("백그라운드 요청", "Ctrl+B · 자연어", 0.0, 0.8, False, MUTED, "요청 전달", 146),
    ("인증 모듈 리팩터링", "테스트와 병행", 1.0, 4.4, False, INFO, "리팩터링", 178),
    ("API 규격 작성", "린트와 병행", 4.8, 7.8, False, INFO, "API 엔드포인트 구현", 210),
    ("결과 확인", "/tasks 열람", 8.0, 9.8, False, MUTED, "실패 3건 확인", 242),
    # Phase 2: 백그라운드 프로세스 행
    ("테스트 스위트", "bg-1234 (예)", 0.8, 8.0, True, ACC, "bg-1234 테스트 (예: 245 통과 · 3 실패)", 304),
    ("린트", "bg-5002 (예)", 1.5, 6.2, False, MUTED, "bg-5002 린트 실행 (예)", 336),
]

for name, sub, m_start, m_end, focal, col, bar_text, ry in tasks:
    # 좌측 컬럼 라벨
    d.t(28, ry + 12, name, 11, INK, KR, "start", 600)
    d.t(28, ry + 25, sub, 11, SOFT, MONO if not any("가" <= c <= "힣" for c in sub) else KR, "start")

    # 타임라인 막대
    bx = x_at(m_start)
    bw = x_at(m_end) - bx
    bh = 22
    by = ry + 4

    if focal:
        d.o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4" fill="{ACC}18" stroke="{ACC}" stroke-width="1.2"/>')
        d.t(bx + 10, by + 15, bar_text, 11, ACC, KR, "start", 600)
    else:
        d.o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4" fill="{PAPER2}" stroke="{col}" stroke-width="0.9"/>')
        d.t(bx + 10, by + 15, bar_text, 11, INK, KR, "start")

# 4. 완료 통지 마일스톤 (8:00 시점)
mx = x_at(8.0)
d.line(mx, P1_Y + 12, mx, P2_Y + P2_H - 6, OK, 1.2, "3 3")
# 마일스톤 칩
d.chip(mx, P1_Y + 14, "완료 알림 수신", OK, 11, 6)

# 5. 범례
d.legend(406, [
    ("테스트 실행 (Focal)", ACC),
    ("대화 세션 작업", INFO),
    ("보조 백그라운드 작업", MUTED),
    ("완료 통지 시점", OK),
])

d.save("05-03.background-task.svg")
print("Saved 05-03.background-task.svg")
