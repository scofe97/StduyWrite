# 사실 출처: 05-05.Interactive Features·Output Styles·Status Line·Settings.md:388-396 · 02-02.Memory.md:234-245 · 원문 chunk-05-05.md:709-733
# 타입 스펙: type-layers
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 500, 500  # Note: W=960, H=500
W = 960
d = D(
    W, H,
    "SETTINGS ARCHITECTURE · LAYER STACK",
    "설정 파일 출처와 우선순위 계층",
    "관리형 정책부터 사용자 전역 설정까지의 오버라이드 우선순위와 배열 병합 방식",
    lead="상위 설정이 하위를 덮어쓰며 권한 배열(allow·deny)은 전 계층이 합집합으로 병합됩니다 (모델 목록 키는 예외)"
)

# 좌측 진행 화살표 (수직: 우선순위 상승 방향)
d.t(44, 114, "최상위 정책", 11, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(44, 396), (44, 126)], SOFT, "soft", 1.2)
d.t(44, 412, "우선순위 ↑", 11, SOFT, fam=KR, anchor="middle")

LX, LW = 88, 848
h_layer = 54
gap = 12
y0 = 104

layers = [
    (
        "L1", "관리형 설정", "managed-settings.json",
        "조직 강제", "정책 잠금 · managed-settings.d/ 알파벳 순 병합",
        PAPER2, RULE, INK, WARN
    ),
    (
        "L2", "CLI 인자", "--settings · --model",
        "임시 옵션", "세션 일회성 인자 반영",
        PAPER2, RULE, INK, INFO
    ),
    (
        "L3", "로컬 설정", ".claude/settings.local.json",
        "git 미커밋", "개인 오버라이드 (Focal)",
        f"{ACC}14", ACC, INK, ACC
    ),
    (
        "L4", "공용 설정", ".claude/settings.json",
        "팀 git 공유", "팀 공용 설정 · 기본 훅 및 권한",
        PAPER2, RULE, INK, SOFT
    ),
    (
        "L5", "사용자 설정", "~/.claude/settings.json",
        "개인 기본값", "개인 전역 기본 환경 · 영구 저장",
        PAPER2, RULE, INK, SOFT
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
    d.chip(LX + 350, y + 20, chip_txt, chip_col, size=11)

    # 2행: 파일 경로/옵션(좌), 핵심 정책(우)
    d.t(LX + 58, y + 43, path_txt, 11, MUTED if not is_focal else INK, fam=MONO, anchor="start")
    d.t(LX + LW - 18, y + 43, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

d.legend(446, [
    ("로컬 오버라이드 (Focal)", ACC),
    ("관리형 강제 정책", WARN),
    ("CLI 세션 인자", INFO),
    ("공용 · 사용자 기본값", SOFT),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05-05.settings-precedence.svg"))
d.save(out)
print(f"saved: {out}")
