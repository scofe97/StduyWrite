"""MCP 서버 설정의 로컬·프로젝트·사용자·관리형 스코프와 계층별 우선순위.

# 타입 스펙: type-layers
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, WARN, KR, MONO

W, H = 920, 452
d = D(
    W, H,
    "MCP CONFIGURATION SCOPES",
    "MCP 서버 설정 스코프와 계층별 우선순위",
    "동일 이름 서버 정의 충돌 시 로컬 스코프가 최우선 적용되는 3단계 설정 계층과 사다리 밖 관리형 스코프",
    lead="동일 이름의 서버가 여러 스코프에 중복 정의되면 로컬 스코프가 가장 높은 우선순위를 가집니다"
)

# 좌측 진행 화살표 (수직)
d.t(44, 116, "우선순위 ↓", 11, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(44, 128), (44, 268)], SOFT, "soft", 1.2)
d.t(44, 284, "낮음", 11, SOFT, fam=KR, anchor="middle")

LX, LW = 88, 808
h_layer = 54
gap = 12
y0 = 104

layers = [
    (
        "L1", "로컬 스코프 (local)", "~/.claude.json (프로젝트)",
        "1순위 최우선", "개인 전용 · 충돌 시 최우선 승리",
        f"{ACC}14", ACC, INK, ACC
    ),
    (
        "L2", "프로젝트 스코프 (project)", "./.mcp.json",
        "2순위 팀 공유", "팀 공유 (Git) · 첫 실행 시 승인",
        PAPER2, RULE, INK, INFO
    ),
    (
        "L3", "사용자 스코프 (user)", "~/.claude.json",
        "3순위 전역 기본", "모든 프로젝트 공통 개인 도구",
        PAPER2, RULE, INK, INFO
    ),
    (
        "L4", "관리형 스코프 (managed)", "managed-mcp.json (시스템 전역)",
        "사다리 밖 · 배타적 통제", "IT 중앙 정책 · 허용/차단 필터링",
        PAPER2, WARN, INK, WARN
    ),
]

for i, (tag, name, path_txt, chip_txt, note, fill, stroke, text_col, chip_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    if tag == "L4":
        y += 16
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{h_layer}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.2" stroke-dasharray="5 4"/>')
    else:
        d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 좌측 태그 (L1 ~ L4)
    d.box(LX + 14, y + 13, 30, 28, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 29, y + 31, tag, 11, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 1행: 계층 이름, 상태 칩
    d.t(LX + 58, y + 24, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.chip(LX + 300, y + 20, chip_txt, chip_col, size=12)

    # 2행: 파일 경로(좌), 핵심 정책(우)
    d.t(LX + 58, y + 43, path_txt, 11, INK if is_focal else MUTED, fam=MONO, anchor="start")
    d.t(LX + LW - 18, y + 43, note, 12, INK if is_focal else MUTED, fam=KR, anchor="end")

d.legend(392, [
    ("동일 이름 충돌 시 최우선 적용 (Focal)", ACC),
    ("팀 공유 및 전역 도구", INFO),
    ("IT 중앙 통제 정책", WARN)
])

d.save("03-03.mcp-scopes.svg")
