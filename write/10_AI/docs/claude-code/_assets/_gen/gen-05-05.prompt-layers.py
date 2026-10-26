# 사실 출처: 05-05.Interactive Features·Output Styles·Status Line·Settings.md:175-185 · 원문 chunk-05-05.md:340-348
# 타입 스펙: type-layers
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 960, 500
d = D(
    W, H,
    "PROMPT COMPOSITION · LAYER STACK",
    "시스템 프롬프트와 런타임 지침 계층 구조",
    "Output Style과 CLAUDE.md 및 런타임 프롬프트가 놓이는 영역과 역할 구분",
    lead="출력 스타일은 시스템 프롬프트에 역할·어조를 덧입히며 CLAUDE.md는 사용자 메시지로 주입됩니다"
)

LX, LW = 88, 848
h_layer = 54
gap = 12
y0 = 104

layers = [
    (
        "L1", "기본 시스템 프롬프트", "Claude Code 내장",
        "기본 지침", "기본 역할 정의",
        PAPER2, RULE, INK, SOFT
    ),
    (
        "L2", "출력 스타일", "outputStyle / /output-style",
        "어조 지침", "역할·어조를 덧입힘 · 코딩 지침은 keep-coding-instructions 로 유지·제외",
        f"{ACC}14", ACC, INK, ACC
    ),
    (
        "L3", "추가 시스템 지침", "--append-system-prompt",
        "지침 덧붙임", "기존 프롬프트 유지 및 말미 추가",
        PAPER2, RULE, INK, INFO
    ),
    (
        "L4", "프로젝트 메모리", "./CLAUDE.md",
        "메시지 주입", "시스템 직후 첫 사용자 메시지 주입",
        PAPER2, RULE, INK, OK
    ),
    (
        "L5", "런타임 입력", "프롬프트 · /skills",
        "동적 로드", "명시적 호출 시 스킬 지침 로드",
        PAPER2, RULE, INK, SOFT
    ),
]

# 좌측 영역 구분 (층 번호·주입 순서 대신 놓이는 영역만 표기)
def bracket(y_top, y_bot, lines):
    d.line(74, y_top, 74, y_bot, SOFT, 1.2)
    cy = (y_top + y_bot) / 2 - 8 * (len(lines) - 1)
    for k, ln in enumerate(lines):
        d.t(36, cy + 4 + 16 * k, ln, 11, SOFT, fam=KR, anchor="middle", weight=600)

bracket(y0, y0 + 2 * (h_layer + gap) + h_layer, ["시스템", "프롬프트", "영역"])
bracket(y0 + 3 * (h_layer + gap), y0 + 3 * (h_layer + gap) + h_layer, ["사용자", "메시지"])

for i, (tag, name, path_txt, chip_txt, note, fill, stroke, text_col, chip_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 1행: 계층 이름, 상태 칩
    d.t(LX + 18, y + 24, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.chip(LX + 350, y + 20, chip_txt, chip_col, size=11)

    # 2행: 파일 경로/명령(좌), 핵심 정책(우)
    d.t(LX + 18, y + 43, path_txt, 11, MUTED if not is_focal else INK, fam=KR if any("가" <= c <= "힣" for c in path_txt) else MONO, anchor="start")
    d.t(LX + LW - 18, y + 43, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

d.legend(446, [
    ("출력 스타일 계층 (Focal)", ACC),
    ("추가 시스템 지침 계층", INFO),
    ("메모리 사용자 주입 계층", OK),
    ("기본 및 런타임 지침", SOFT),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05-05.prompt-layers.svg"))
d.save(out)
print(f"saved: {out}")
