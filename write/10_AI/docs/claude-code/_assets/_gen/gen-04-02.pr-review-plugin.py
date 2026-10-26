"""PR 리뷰 플러그인의 훅·MCP·서브에이전트 연계 실행 워크플로."""
# 타입 스펙: type-swimlane
# 사실 출처: 04-02.Plugins.md:509-516 · 원문 07-plugins/README.md:1289-1306
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 500
d = D(
    W, H,
    "PR REVIEW WORKFLOW · SWIMLANE",
    "PR 리뷰 플러그인 컴포넌트 연계 워크플로",
    "사용자 명령 입력부터 훅 검증, MCP 데이터 수집, 서브에이전트 병렬 분석, 종합 보고서 출력까지의 실행 레인",
    lead="훅과 MCP, 복수 서브에이전트가 역할별 레인에서 순차 및 병렬로 연계되어 동작합니다",
)

LABEL_W = 152
LANE_W = 792
Y0 = 104

LANES = [
    ("사용자 · 세션", "User · Session", 64),
    ("수명주기 훅", "Hooks · pre-review", 64),
    ("MCP 도구 서버", "GitHub MCP", 64),
    ("서브에이전트", "일부 · 병렬 실행", 108),
]

# 1. 레인 배경 및 구분선
curr_y = Y0
for k, (name, role, lh) in enumerate(LANES):
    if k % 2 == 0:
        d.o.append(f'<rect x="{LABEL_W}" y="{curr_y}" width="{LANE_W}" height="{lh}" fill="rgba(245,245,243,0.02)"/>')
    d.line(16, curr_y, 16 + LABEL_W + LANE_W - 8, curr_y, RULE, 0.8)

    # 레인 라벨
    cy = curr_y + lh // 2
    d.t(24, cy - 6, name, 12.5, INK, KR, "start", 600)
    d.t(24, cy + 14, role, 11, MUTED, MONO if any(c.isascii() and c.isalpha() for c in role) else KR, "start")
    curr_y += lh

# 바닥 경계선 및 세로 구분선
d.line(16, curr_y, 16 + LABEL_W + LANE_W - 8, curr_y, RULE, 0.8)
d.line(LABEL_W, Y0, LABEL_W, curr_y, RULE, 1.0)

# 2. 연계 화살표 (노드보다 먼저 그린다)
# Step 0 (세션) → Step 1 (훅)
d.arrow([(304, 136), (388, 136), (388, 180)], MUTED, "ar", 1.4)
d.t(396, 154, "트리거", 11, MUTED, KR, "start")

# Step 1 (훅) → Step 2 (MCP)
d.arrow([(456, 200), (540, 200), (540, 244)], MUTED, "ar", 1.4)
d.t(548, 218, "검증 완료", 11, MUTED, KR, "start")

# Step 2 (MCP) → Step 3 (서브에이전트 병렬 분기)
d.line(608, 264, 624, 264, ACC, 1.4)
d.arrow([(624, 264), (624, 328), (632, 328)], ACC, "acc", 1.4)
d.arrow([(624, 264), (624, 376), (632, 376)], ACC, "acc", 1.4)
d.t(616, 320, "diff 주입", 11, ACC, KR, "end")

# Step 3 (서브에이전트) → Step 4 (세션 종합 보고서)
d.line(784, 328, 856, 328, OK, 1.4)
d.line(784, 376, 856, 376, OK, 1.4)
d.arrow([(856, 376), (856, 156)], OK, "ok", 1.4)
d.t(864, 264, "결과 종합", 11, OK, KR, "start")

# 3. 단계별 노드 박스
# Step 0: 사용자 명령 입력
d.box(168, 116, 136, 40, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(236, 132, "/pr-review:start", 11.5, INK, MONO, "middle", 600)
d.t(236, 147, "검토 명령 호출", 11, MUTED, KR, "middle")

# Step 1: 훅 스크립트 실행
d.box(320, 180, 136, 40, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.t(388, 196, "pre-review.js", 11.5, INFO, MONO, "middle", 600)
d.t(388, 211, "Git 작업 트리 점검", 11, MUTED, KR, "middle")

# Step 2: GitHub MCP PR 데이터 수집
d.box(472, 244, 136, 40, fill=PAPER2, stroke=OK, sw=1.0, r=6)
d.t(540, 260, "GitHub MCP", 12, OK, MONO, "middle", 600)
d.t(540, 275, "PR diff · 커밋 수집", 11, MUTED, KR, "middle")

# Step 3A: 보안 분석 서브에이전트 (Focal!)
d.tone(632, 308, 152, 40, ACC, r=6, op="14", sw=1.4)
d.t(708, 324, "security-reviewer", 11.5, ACC, MONO, "middle", 600)
d.t(708, 339, "보안 취약점 분석", 11, INK, KR, "middle")

# Step 3B: 테스트 점검 서브에이전트 (Focal!)
d.tone(632, 356, 152, 40, ACC, r=6, op="14", sw=1.4)
d.t(708, 372, "test-checker", 11.5, ACC, MONO, "middle", 600)
d.t(708, 387, "테스트 커버리지 검증", 11, INK, KR, "middle")

# Step 4: 종합 요약 보고서 출력
d.box(784, 116, 144, 40, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(856, 132, "종합 보고서 출력", 12, OK, KR, "middle", 600)
d.t(856, 147, "분석 요약 · 권고안", 11, MUTED, KR, "middle")

# 4. 범례
d.legend(428, [
    ("병렬 서브에이전트 (Focal)", ACC),
    ("사전 검증 훅", INFO),
    ("MCP 및 최종 출력", OK),
    ("실행 제어", MUTED),
])

d.save("04-02.pr-review-plugin.svg")
