"""되감기 옵션 6가지(행) × 되돌아가는 것(코드·대화, 열) 조합 매트릭스.

# 타입 스펙: type-dp-security-matrix
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

# type-dp-security-matrix §2 Layout formulas
LEFT_PAD = 16
RIGHT_PAD = 48
COMP_W = 280
GAP_CR = 14
ROLE_W = 266
ROLE_GAP = 16

HEADER_Y = 100
HEADER_H = 38
ROW_H = 42
STRIDE = 48

cols = [
    "코드 (파일 변경)",
    "대화 (메시지 내역)",
]

rows = [
    {
        "name": "Restore code and conversation",
        "focal": True,
        "note": "변경이 있을 때만",
        "cells": [
            ("되감기 (시점 복원)", ACC),
            ("되감기 (시점 복원)", ACC),
        ],
    },
    {
        "name": "Restore conversation",
        "focal": False,
        "cells": [
            ("두고 (코드 유지)", MUTED),
            ("되감기 (시점 복원)", OK),
        ],
    },
    {
        "name": "Restore code",
        "focal": False,
        "note": "변경이 있을 때만",
        "cells": [
            ("되감기 (시점 복원)", OK),
            ("두고 (대화 유지)", MUTED),
        ],
    },
    {
        "name": "Summarize from here",
        "focal": False,
        "cells": [
            ("두고 (코드 유지)", MUTED),
            ("시점 이후 압축", WARN),
        ],
    },
    {
        "name": "Summarize up to here",
        "focal": False,
        "cells": [
            ("두고 (코드 유지)", MUTED),
            ("시점 이전 압축", WARN),
        ],
    },
    {
        "name": "Never mind",
        "focal": False,
        "cells": [
            ("두고 (코드 유지)", MUTED),
            ("두고 (대화 유지)", MUTED),
        ],
    },
]

W = LEFT_PAD + COMP_W + GAP_CR + len(cols) * ROLE_W + (len(cols) - 1) * ROLE_GAP + RIGHT_PAD
H = HEADER_Y + HEADER_H + 16 + len(rows) * STRIDE + 50

d = D(
    W, H,
    "CHECKPOINT REWIND · OPTIONS MATRIX",
    "여섯 가지 되감기 옵션별 코드와 대화 복원 매트릭스",
    "되감기 메뉴 선택지에 따른 작업 파일 상태와 대화 컨텍스트 변경 범위 조합",
    lead="여섯 선택지 중에서 작업 목적에 맞는 하나를 고릅니다"
)

# 열 머리 (헤더)
d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(LEFT_PAD + 16, HEADER_Y + 24, "되감기 옵션 (CLI 메뉴)", 12, INK, KR, "start", 600)

for j, col_title in enumerate(cols):
    col_x = LEFT_PAD + COMP_W + GAP_CR + j * (ROLE_W + ROLE_GAP)
    d.box(col_x, HEADER_Y, ROLE_W, HEADER_H, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(col_x + ROLE_W / 2, HEADER_Y + 24, col_title, 12.5, INK, KR, "middle", 600)

# 데이터 행
y_start = HEADER_Y + HEADER_H + 16
for i, r in enumerate(rows):
    row_y = y_start + i * STRIDE

    # 행 머리 (좌측 열)
    if r["focal"]:
        d.tone(LEFT_PAD, row_y, COMP_W, ROW_H, ACC, r=6, op="14", sw=1.4)
        d.t(LEFT_PAD + 14, row_y + (18 if r.get("note") else 26), r["name"], 12, ACC, MONO, "start", 600)
    else:
        d.box(LEFT_PAD, row_y, COMP_W, ROW_H, fill=PAPER2, stroke=RULE, sw=0.9)
        d.t(LEFT_PAD + 14, row_y + (18 if r.get("note") else 26), r["name"], 12, INK, MONO, "start", 600)
    if r.get("note"):
        d.t(LEFT_PAD + 14, row_y + 34, r["note"], 11, MUTED, KR, "start")

    # 셀 값들
    for j, (val, color) in enumerate(r["cells"]):
        cell_x = LEFT_PAD + COMP_W + GAP_CR + j * (ROLE_W + ROLE_GAP)
        if r["focal"]:
            d.tone(cell_x, row_y, ROLE_W, ROW_H, ACC, r=6, op="14", sw=1.4)
            d.t(cell_x + ROLE_W / 2, row_y + 26, val, 12.5, ACC, KR, "middle", 600)
        else:
            stroke_c = color if color != MUTED else RULE
            d.box(cell_x, row_y, ROLE_W, ROW_H, fill=PAPER2, stroke=stroke_c, sw=1.0 if color != MUTED else 0.8)
            d.t(cell_x + ROLE_W / 2, row_y + 26, val, 12.5, color, KR, "middle", 600 if color != MUTED else 400)

# 범례
legend_y = y_start + len(rows) * STRIDE + 8
d.legend(legend_y, [
    ("코드·대화 동시 복원 (Focal)", ACC),
    ("단독 되감기 복원", OK),
    ("대화 요약 압축", WARN),
    ("두고 (현재 상태 유지)", MUTED),
])

out_path = _HERE.parent / "05-01.rewind-options.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
