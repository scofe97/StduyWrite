# 타입 스펙: type-dp-security-matrix
# 2절 input 승인 대기와 실행기 점유 해제 — 파이프라인 구성 방식과 국면별 실행기 점유 격자 비교
# 본문 사실 출처: 03-02.병렬·승인·재시도와 실행기 점유.md 57~86행
#   59행: 사람의 수동 승인을 기다리는 단계는 에이전트를 배정받기 전에 멈추도록 input 지시어를 쓰고 파이프라인 최상위를 agent none 으로 두어야 실행기를 붙잡지 않습니다.
#   61행: 운영 환경 배포 전에는 승인권자의 확인을 받는 수동 승인 게이트가 자주 쓰입니다... 파이프라인 최상위에 agent any 가 있거나 단계 안에서 에이전트를 잡은 뒤 input 스텝을 호출하면, 에이전트 실행기를 쥔 채 대기합니다.
#   63행: 에이전트가 묶이면 아무런 연산을 하지 않으면서도 정규 실행기 슬롯을 독점합니다. 큐에 들어온 다른 프로젝트의 빌드들이 빈 슬롯을 얻지 못해 지연됩니다.
#   65행: 해결책은 두 가지를 함께 쓰는 것입니다. 첫째, 단계에 input 지시어를 쓰면 그 단계는 옵션을 적용한 뒤 단계의 에이전트에 들어가기 전에 멈춥니다. 둘째, 최상위를 agent none 으로 두면 실행기가 불필요하게 배정되지 않습니다. 그러면 승인 대기 중에는 에이전트 실행기 없이 컨트롤러의 경량 작업(Flyweight Task)만 남아 웹 요청을 기다립니다.
#   84행: 실제 배포는 승인 뒤 다음 단계에서 agent { label ... } 로 에이전트를 새로 배정받아 수행합니다.
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

LP = 16
CW = 260
GAP = 16
RW = 196
RG = 16
RP = 24
NCOL = 3
W = LP + CW + GAP + NCOL * RW + (NCOL - 1) * RG + RP  # 936

HY = 96
HH = 48
RH = 44
RS = 52
ROW0 = HY + HH + 20  # 164
NROW = 2
ROWS_BOTTOM = ROW0 + (NROW - 1) * RS + RH  # 260
LEG = ROWS_BOTTOM + 24  # 284
H = LEG + 48  # 332

d = D(
    W,
    H,
    "JENKINS · INPUT & EXECUTOR HOLD",
    "input 승인 대기와 실행기 점유 해제",
    "파이프라인 최상위 agent 선언과 input 배치 방식에 따른 국면별 실행기 점유 비교. 최상위 agent any 는 승인 대기 중에도 정규 실행기 슬롯을 독점하여 큐 지연을 일으키지만, 최상위 agent none 과 input 지시어는 실행기 없이 Flyweight Task 로 대기합니다.",
    lead="최상위 agent any 는 승인 대기 중 슬롯 독점(상단) vs agent none 은 실행기 없이 경량 대기(하단)",
)


def colx(j):
    return LP + CW + GAP + j * (RW + RG)


# ── 헤더 행 ─────────────────────────────────────────────────────────────
d.box(LP, HY, CW, HH, PAPER2, RULE, 0.9, 6)
d.t(LP + CW // 2, HY + 20, "파이프라인 구성", 13, MUTED, KR, "middle", 600)
d.t(LP + CW // 2, HY + 36, "agent 선언 위치", 13, SOFT, KR, "middle")

COLS = [
    ("1. 빌드 단계", "컴파일 및 테스트"),
    ("2. 승인 대기 단계", "수동 승인 게이트"),
    ("3. 배포 단계", "운영 환경 배포"),
]
for j, (name, sub) in enumerate(COLS):
    cx = colx(j)
    d.box(cx, HY, RW, HH, PAPER2, RULE, 0.9, 6)
    d.t(cx + RW // 2, HY + 20, name, 13, INK, KR, "middle", 600)
    d.t(cx + RW // 2, HY + 36, sub, 13, MUTED, KR, "middle")

# ── 데이터 행 ───────────────────────────────────────────────────────────
ROWS = [
    ("최상위 agent any", "단계 내 input 스텝 호출"),
    ("최상위 agent none", "단계 input 지시어 적용"),
]

# 셀 데이터: (주 라벨, 부 라벨, 색상, focal 여부, kr_mono)
CELLS = [
    # Row 0: agent any
    [
        ("실행기 점유", "정규 슬롯 점유", INFO, False),
        ("실행기 점유 (독점)", "유휴 상태 슬롯 독점", BAD, False),
        ("실행기 점유", "배포 작업 수행", INFO, False),
    ],
    # Row 1: agent none
    [
        ("실행기 배정", "agent { label ... }", INFO, False),
        ("실행기 해제 (미점유)", "Flyweight Task 대기", ACC, True),
        ("실행기 배정", "agent { label ... }", INFO, False),
    ],
]

for r, (row_name, row_sub) in enumerate(ROWS):
    y = ROW0 + r * RS
    focal_row = r == 1
    d.box(LP, y, CW, RH, PAPER2, RULE, 0.9, 4)
    d.t(LP + 14, y + 18, row_name, 13, ACC if focal_row else INK, MONO, "start", 600)
    d.t(LP + 14, y + 34, row_sub, 13, MUTED, KR, "start")

    for j, (val, sub, c, focal) in enumerate(CELLS[r]):
        cx = colx(j)
        if focal:
            d.tone(cx, y, RW, RH, ACC, 4, "1F", 1.4)
            d.t(cx + RW // 2, y + 18, val, 13, ACC, KR, "middle", 600)
            d.t(cx + RW // 2, y + 34, sub, 13, ACC, MONO, "middle")
        else:
            d.tone(cx, y, RW, RH, c, 4, "14", 1.0)
            d.t(cx + RW // 2, y + 18, val, 13, c if c == BAD else INK, KR, "middle", 600)
            fam = MONO if "{" in sub else KR
            d.t(cx + RW // 2, y + 34, sub, 13, c if c == BAD else MUTED, fam, "middle")

# ── 범례 ────────────────────────────────────────────────────────────────
d.legend(
    LEG,
    [
        ("정규 실행기 점유 (작업 수행)", INFO),
        ("실행기 슬롯 독점 (자원 누수)", BAD),
        ("실행기 해제 (Flyweight Task)", ACC),
    ],
)

out_path = pathlib.Path(__file__).resolve().parent.parent / "03-02.input-executor-hold.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
