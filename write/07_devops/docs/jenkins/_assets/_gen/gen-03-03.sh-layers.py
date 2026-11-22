# 사실 출처: 03-03.sh step 이 실패를 삼키는 이유.md:38-51
# 타입 스펙: type-layers
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, WARN, BAD, INFO, KR, MONO

W, H = 960, 500

d = D(
    W, H,
    "JENKINS · SH STEP EXECUTION LAYERS",
    "sh step 실행 계층과 종료 코드 전파",
    "OS 명령부터 Groovy 파이프라인까지의 4계층과 기본 -xe 가 꺼졌을 때 실패가 묻히는 경로",
    lead="기본 -xe 는 중간 실패 시 즉시 중단하나 꺼지는 경로에서는 마지막 명령의 0 만 전달됩니다"
)

# 좌측 진행 화살표 (종료 코드 전파 방향: 하단 OS 명령 → 상단 Groovy 파이프라인)
d.t(44, 116, "종료 코드 ↑", 11, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(44, 396), (44, 128)], SOFT, "soft", 1.2)
d.t(44, 416, "명령 실행", 11, SOFT, fam=KR, anchor="middle")

LX, LW = 88, 848

# ── L4: Groovy 파이프라인 ──────────────────────────────────────────────
y_l4 = 96
h_l4 = 56
d.box(LX, y_l4, LW, h_l4, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
# 태그
d.box(LX + 12, y_l4 + 14, 32, 28, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(LX + 28, y_l4 + 32, "L4", 11, SOFT, fam=MONO, anchor="middle", weight=600)
# 계층명 및 설명
d.t(LX + 56, y_l4 + 24, "Groovy 파이프라인", 14, INK, fam=KR, anchor="start", weight=600)
d.t(LX + 56, y_l4 + 43, "Jenkins 고유 규칙 · 파이프라인 엔진", 11, MUTED, fam=KR, anchor="start")
d.chip(LX + 340, y_l4 + 20, "stage 통과 여부 판정", INFO, size=11)
d.t(LX + LW - 18, y_l4 + 34, "0 읽고 초록불(통과) vs 비0 시 stage 실패", 11, MUTED, fam=KR, anchor="end")

# ── L3: step 래퍼 ──────────────────────────────────────────────────────
y_l3 = 164
h_l3 = 56
d.box(LX, y_l3, LW, h_l3, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
# 태그
d.box(LX + 12, y_l3 + 14, 32, 28, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(LX + 28, y_l3 + 32, "L3", 11, SOFT, fam=MONO, anchor="middle", weight=600)
# 계층명 및 설명
d.t(LX + 56, y_l3 + 24, "step 래퍼", 14, INK, fam=KR, anchor="start", weight=600)
d.t(LX + 56, y_l3 + 43, "문자열 가공과 종료 코드 판정 층", 11, MUTED, fam=KR, anchor="start")
d.chip(LX + 340, y_l3 + 20, "셸의 종료 코드 수신", INFO, size=11)
d.t(LX + LW - 18, y_l3 + 34, "스크립트를 실행한 셸의 종료 코드를 읽음", 11, MUTED, fam=KR, anchor="end")

# ── L2: 셸 프로세스 (Focal Layer) ──────────────────────────────────────
y_l2 = 232
h_l2 = 120
d.tone(LX, y_l2, LW, h_l2, ACC, r=6, op="10", sw=1.4)
# 태그
d.box(LX + 12, y_l2 + 14, 32, 28, fill=PAPER, stroke=ACC, sw=0.8, r=4)
d.t(LX + 28, y_l2 + 32, "L2", 11, ACC, fam=MONO, anchor="middle", weight=600)
# 좌측 영역: 계층명 및 기본 -xe 경로
d.t(LX + 56, y_l2 + 32, "셸 프로세스", 14, INK, fam=KR, anchor="start", weight=600)

d.box(LX + 12, y_l2 + 50, 284, 58, fill=PAPER, stroke=ACC, sw=1.0, r=4)
d.t(LX + 24, y_l2 + 70, "기본 -xe: 비0 시 즉시 중단", 11, INK, fam=KR, anchor="start", weight=600)
d.chip(LX + 246, y_l2 + 66, "비0 전파", BAD, size=11)
d.t(LX + 24, y_l2 + 94, "stage 실패 판정으로 직결", 11, MUTED, fam=KR, anchor="start")

# 우측 영역: 꺼지는 경로 4가지 및 실패 소멸
d.box(400, y_l2 + 12, 524, 96, fill=PAPER, stroke=WARN, sw=1.0, r=4)
d.t(416, y_l2 + 32, "기본 -xe 가 꺼지는 경우 (실패가 묻힘):", 11, WARN, fam=KR, anchor="start", weight=600)
d.chip(474, y_l2 + 62, "shebang (#!...)", WARN, size=11)
d.chip(600, y_l2 + 62, "set +e 선언", WARN, size=11)
d.chip(700, y_l2 + 62, "|| true", WARN, size=11)
d.chip(828, y_l2 + 62, "파이프 앞쪽 (a | b)", WARN, size=11)
d.t(416, y_l2 + 92, "중간 비0 실패 무시 → 마지막 명령(0)만 전달되어 실패 삼킴", 11, WARN, fam=KR, anchor="start")

# ── L1: OS 명령 ────────────────────────────────────────────────────────
y_l1 = 364
h_l1 = 56
d.box(LX, y_l1, LW, h_l1, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
# 태그
d.box(LX + 12, y_l1 + 14, 32, 28, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(LX + 28, y_l1 + 32, "L1", 11, SOFT, fam=MONO, anchor="middle", weight=600)
# 계층명 및 설명
d.t(LX + 56, y_l1 + 24, "OS 명령", 14, INK, fam=KR, anchor="start", weight=600)
d.t(LX + 56, y_l1 + 43, "에이전트 머신에서 실행되는 명령", 11, MUTED, fam=KR, anchor="start")
d.chip(LX + 340, y_l1 + 20, "명령 실행", INFO, size=11)
d.t(LX + LW - 18, y_l1 + 34, "curl · tar 등 개별 명령 비0 종료 코드 발생", 11, MUTED, fam=KR, anchor="end")

# ── 범례 ────────────────────────────────────────────────────────────────
LEG_Y = 444
d.legend(LEG_Y, [
    ("셸 프로세스 (기본 -xe)", ACC),
    ("비0 실패 전파", BAD),
    ("실패 삼킴 (0 반환)", WARN),
    ("파이프라인 계층", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "03-03.sh-layers.svg")
d.save(out_path)
print(f"saved: {out_path}")
