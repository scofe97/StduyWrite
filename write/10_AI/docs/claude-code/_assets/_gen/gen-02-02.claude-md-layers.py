# 사실 출처: 02-02.Memory.md:57-92 · 원문 README.md:237-252
# 타입 스펙: type-layers
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 960, 512
d = D(
    W, H,
    "MEMORY ARCHITECTURE · CONTEXT CONCATENATION",
    "CLAUDE.md 메모리 계층과 @path 임포트 확장",
    "관리자 정책부터 하위 모듈까지 프롬프트 컨텍스트에 순서대로 이어 붙는 계층 구조",
    lead="상위 설정이 하위 설정을 덮어쓰지 않고 순서대로 컨텍스트에 이어 붙습니다"
)

# 좌측 진행 화살표 (수직)
d.t(44, 116, "누적 순서 ↓", 11, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(44, 128), (44, 404)], SOFT, "soft", 1.2)
d.t(44, 420, "컨텍스트 후반", 11, SOFT, fam=KR, anchor="middle")

LX, LW = 88, 848
h_layer = 54
gap = 12
y0 = 104

layers = [
    (
        "L1", "관리자 정책", "/Library/.../CLAUDE.md",
        "조직 정책", "사내 표준 및 보안 지침",
        PAPER2, RULE, INK, SOFT
    ),
    (
        "L2", "사용자 메모리", "~/.claude/CLAUDE.md",
        "개인 선호", "개인 코딩 선호 및 응답 양식",
        PAPER2, RULE, INK, INFO
    ),
    (
        "L3", "프로젝트 메모리", "./CLAUDE.md",
        "@path 재귀 확장", "팀 표준 아키텍처 및 빌드 규칙",
        f"{ACC}14", ACC, INK, ACC
    ),
    (
        "L4", "로컬 프로젝트 메모리", "./CLAUDE.local.md",
        "로컬 전용", "개인 디버그 설정 (.gitignore)",
        PAPER2, RULE, INK, SOFT
    ),
    (
        "L5", "하위 디렉터리 메모리", "./sub-module/CLAUDE.md",
        "지연 로드", "하위 파일 접근 시 동적 적재",
        PAPER2, RULE, INK, INFO
    ),
]

for i, (tag, name, path_txt, chip_txt, note, fill, stroke, text_col, chip_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 좌측 태그 (L1 ~ L5)
    d.box(LX + 14, y + 13, 30, 28, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 29, y + 31, tag, 11, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 1행: 계층 이름, 상태 칩
    d.t(LX + 58, y + 24, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.chip(LX + 340, y + 20, chip_txt, chip_col, size=11)

    # 2행: 파일 경로(좌), 핵심 정책(우)
    d.t(LX + 58, y + 43, path_txt, 11, MUTED if not is_focal else INK, fam=MONO, anchor="start")
    d.t(LX + LW - 18, y + 43, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

d.legend(456, [
    ("기본 적재 계층", MUTED),
    ("프로젝트 메모리 및 임포트 (Focal)", ACC),
    ("동적 지연 로드 계층", INFO),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-02.claude-md-layers.svg"))
d.save(out)
print(f"saved: {out}")
