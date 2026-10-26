"""슬래시 명령의 수명주기와 파이프라인 처리 흐름."""
# 타입 스펙: type-process
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 976, 480
d = D(
    W, H,
    "COMMAND LIFECYCLE · PIPELINE ARCHITECTURE",
    "슬래시 명령의 수명주기와 단계별 처리 파이프라인",
    "입력 검증부터 파일 탐색, 인자 대입, 동적 셸 치환, 모델 전송까지의 페이로드 변화",
    lead="입력 문자열이 템플릿 로드, 변수 치환($), 인라인 셸 실행(!)을 거쳐 최종 프롬프트로 조립됩니다",
)

LABEL_W = 136
SLOT_W = 168
NODE_W = 140
NODE_H = 64
LANE_H = 88
HEADER_Y = 96
LANE0_Y = 128

# 1. 레인 배경 및 구분선
for k in range(3):
    y = LANE0_Y + k * LANE_H
    if k % 2 == 0:
        d.o.append(f'<rect x="{LABEL_W}" y="{y}" width="{W - LABEL_W - 12}" height="{LANE_H}" fill="rgba(245,245,243,0.02)"/>')
    d.line(16, y, W - 12, y, RULE, 0.8)

d.line(16, LANE0_Y + 3 * LANE_H, W - 12, LANE0_Y + 3 * LANE_H, RULE, 0.8)
d.line(LABEL_W, LANE0_Y, LABEL_W, LANE0_Y + 3 * LANE_H, RULE, 1.0)

# 레인 이름
lanes = [
    ("실행기", "런타임 제어"),
    ("페이로드", "데이터 상태"),
    ("검증·제어", "조건 분기"),
]
for k, (title, sub) in enumerate(lanes):
    cy = LANE0_Y + k * LANE_H + LANE_H // 2
    d.t(24, cy - 6, title, 13, INK, KR, "start", 600)
    d.t(24, cy + 14, sub, 11.5, MUTED, KR, "start")

# 2. 단계 머리 (Step Header)
steps = [
    ("1 · 입력", False, False),
    ("2 · 파일 특정", False, False),
    ("3 · 인자 대입", False, False),
    ("4 · 셸 치환", True, False),
    ("5 · 전송", False, True),
]

for j, (st_name, is_focal, is_ok) in enumerate(steps):
    cx = LABEL_W + 16 + j * SLOT_W + NODE_W // 2
    c = ACC if is_focal else (OK if is_ok else INK)
    d.t(cx, HEADER_Y + 18, st_name, 12, c, KR, "middle", 600)

# 3. 페이로드 흐름 화살표 (노드보다 먼저 그린다)
for j in range(4):
    x_from = LABEL_W + 16 + j * SLOT_W + NODE_W
    x_to = LABEL_W + 16 + (j + 1) * SLOT_W
    y_mid = LANE0_Y + 1 * LANE_H + (LANE_H - NODE_H) // 2 + NODE_H // 2
    if j == 2:
        d.arrow([(x_from, y_mid), (x_to, y_mid)], ACC, "acc", 1.4)
    elif j == 3:
        d.arrow([(x_from, y_mid), (x_to, y_mid)], OK, "ok", 1.4)
    else:
        d.arrow([(x_from, y_mid), (x_to, y_mid)], MUTED, "ar", 1.4)

# 4. 그리드 노드 (3행 x 5열)
nodes_data = {
    # (lane, step): (title, sub, color, is_focal, is_mono_sub)
    (0, 0): ("명령 입력", "접두어 /", INK, False, False),
    (1, 0): ("/optimize", "명령 텍스트", INFO, False, False),
    (2, 0): ("오타 검증", "퍼지 차단", INK, False, False),

    (0, 1): ("스킬 탐색", ".claude/skills/", INK, False, True),
    (1, 1): ("SKILL.md", "템플릿 로드", INFO, False, False),
    (2, 1): ("프론트매터", "YAML 파싱", INK, False, False),

    (0, 3): ("셸 실행", "!`command`", ACC, True, True),
    (1, 3): ("stdout 치환", "본문 삽입", ACC, True, False),
    (2, 3): ("훅 통과 후 실행", "UserPromptSubmit", ACC, True, True),

    (0, 2): ("변수 치환", "$ARGUMENTS", INK, False, True),
    (1, 2): ("인자 결합", "인자 값 주입", INFO, False, False),
    (2, 2): ("인자 바인딩", "$0·$1 매핑", INK, False, True),

    (0, 4): ("모델 전달", "컨텍스트 전송", INK, False, False),
    (1, 4): ("최종 프롬프트", "조립 완료", OK, False, False),
    (2, 4): ("컨텍스트 제어", "context: fork", INK, False, True),
}

for (k, j), (title, sub, c, is_focal, is_mono_sub) in nodes_data.items():
    nx = LABEL_W + 16 + j * SLOT_W
    ny = LANE0_Y + k * LANE_H + (LANE_H - NODE_H) // 2
    ncx = nx + NODE_W // 2

    if is_focal:
        d.tone(nx, ny, NODE_W, NODE_H, ACC, 6, "14", 1.4)
    elif c == OK:
        d.tone(nx, ny, NODE_W, NODE_H, OK, 6, "14", 1.2)
    else:
        d.box(nx, ny, NODE_W, NODE_H, PAPER2, RULE, 1.0)

    # 텍스트
    fam_title = MONO if "/" in title or "SKILL" in title else KR
    fam_sub = MONO if is_mono_sub or "/" in sub or "$" in sub else KR
    d.t(ncx, ny + 26, title, 12.5, c, fam_title, "middle", 600)
    d.t(ncx, ny + 47, sub, 11.5, MUTED, fam_sub, "middle")

# 5. 범례
d.legend(432, [("인라인 셸 치환 (동적 실행)", ACC), ("치환 완료 최종 프롬프트", OK), ("단계별 처리 및 데이터", INFO)])

d.save("02-01.command-lifecycle.svg")
