"""스킬 로딩의 3단계 계층과 토큰 비용 구조.

# 타입 스펙: type-pyramid
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 460
APEX_X, APEX_Y = 340, 116
BASE_Y = 368
HW_TOP, HALF = 140, 248
BANDS = 3
BAND_H = (BASE_Y - APEX_Y) / BANDS

d = D(
    W, H,
    "PROGRESSIVE DISCLOSURE",
    "스킬 로딩 3단계와 토큰 비용",
    "Level 1 메타데이터, Level 2 본문 지시문, Level 3 부속 리소스의 로딩 시점과 토큰 비용 구조",
    lead="상시 상주하는 메타데이터부터 필요 시 실행되는 부속 리소스까지의 계층입니다"
)

def hw(y):
    return HW_TOP + (HALF - HW_TOP) * (y - APEX_Y) / (BASE_Y - APEX_Y)

# 좌측 축: 상시 상주 vs 온디맨드
d.t(48, APEX_Y + 12, "상시 상주 ↑", 12, SOFT, KR, "middle")
d.line(48, APEX_Y + 28, 48, BASE_Y - 28, RULE, 0.8)
d.t(48, BASE_Y - 12, "온디맨드 ↓", 12, SOFT, KR, "middle")

LAYERS = [
    (
        "Level 1: 메타데이터",
        "YAML 프론트매터 (name · description)",
        "세션 시작 시 상시 로드",
        "~100 토큰 / 스킬",
        ACC
    ),
    (
        "Level 2: 본문 지시문",
        "SKILL.md 본문 (워크플로 지침)",
        "스킬 발동 시 로드",
        "5,000 토큰 미만 권장",
        MUTED
    ),
    (
        "Level 3: 부속 리소스",
        "스크립트 · 템플릿 · 예제 파일",
        "필요 시 온디맨드 참조",
        "미접근 시 0토큰 · 스크립트는 출력만",
        MUTED
    ),
]

for i, (name, content, timing, cost, c) in enumerate(LAYERS):
    yt = APEX_Y + i * BAND_H
    yb = APEX_Y + (i + 1) * BAND_H
    pts = f"{APEX_X - hw(yt)},{yt} {APEX_X + hw(yt)},{yt} {APEX_X + hw(yb)},{yb} {APEX_X - hw(yb)},{yb}"
    fill = f"{ACC}14" if c is ACC else PAPER2
    stroke = c if c is ACC else RULE
    sw = 1.4 if c is ACC else 1.0
    d.o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    
    cy = (yt + yb) / 2
    is_acc = (c is ACC)
    d.t(APEX_X, cy - 8, name, 13, ACC if is_acc else INK, KR, "middle", 600)
    d.t(APEX_X, cy + 12, content, 12, ACC if is_acc else SOFT, KR, "middle")
    
    # 우측 인출선 및 설명 카드
    right_x = APEX_X + hw(cy)
    d.line(right_x + 8, cy, 616, cy, stroke, 0.8)
    
    # 우측 상태 정보
    d.box(624, cy - 24, 252, 48, PAPER2, stroke, sw, r=4)
    d.t(640, cy - 6, timing, 12, INK, KR, "start", 600)
    d.t(640, cy + 12, cost, 12, ACC if is_acc else MUTED, MONO, "start")

d.legend(420, [("상시 컨텍스트 상주 (focal)", ACC), ("조건부 및 온디맨드 로드", MUTED)])
d.save("03-01.skill-loading-levels.svg")
