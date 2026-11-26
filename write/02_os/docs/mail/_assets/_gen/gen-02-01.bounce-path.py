# 사실 출처: RFC 5321 §3.7(반송 주소), RFC 3464(DSN 형식), RFC 5322 §3.6.2(From 헤더)
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

LABEL_W, SLOT, NSTEP = 120, 168, 5
W = LABEL_W + NSTEP * SLOT + 28  # 988
Y0, HEAD, LANE = 84, 52, 104
NW, NH = 144, 80
H = Y0 + HEAD + 3 * LANE + 80  # 528

d = D(
    W, H,
    "DATA FLOW · BOUNCE DELIVERY PATH",
    "250 접수 후 다음 홉 실패 시 DSN 반송 경로",
    "게이트웨이가 메일을 250 접수한 뒤 내부 홉에서 550 오류가 발생했을 때 헤더 From이 아닌 봉투 MAIL FROM으로 반송(DSN)을 보내는 흐름",
    "외부 접수 시점의 봉투 발신자와 헤더 작성자가 다를 때 반송 통지가 봉투 주소로 전달되는 원리"
)

def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def cx(j):
    return LABEL_W + j * SLOT + SLOT // 2

def nx(j):
    return cx(j) - NW // 2

def lane_top(k):
    return Y0 + HEAD + k * LANE

def ny(k):
    return lane_top(k) + 12

# 1. 레인 띠와 구분선
d.o.append(f'<rect x="{LABEL_W}" y="{lane_top(0)}" width="{W - LABEL_W - 12}" height="{LANE * 3}" fill="{PAPER2}" opacity="0.6"/>')
for k in range(4):
    d.line(12, lane_top(0) + k * LANE, W - 12, lane_top(0) + k * LANE, RULE, 0.8)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(3), RULE, 0.8)

# 2. 단계 머리 (5단계)
STEPS = [
    ("01", "외부 접수"),
    ("02", "내부 전달"),
    ("03", "최종 거부"),
    ("04", "반송 생성"),
    ("05", "반송 배달")
]
for j, (num, lab) in enumerate(STEPS):
    focal = (j == 3)
    c = ACC if focal else MUTED
    d.o.append(f'<rect x="{cx(j) - 16}" y="{Y0 + 6}" width="32" height="16" rx="8" fill="{c}33" />')
    d.t(cx(j), Y0 + 18, num, 11, c, MONO, "middle", 600)
    d.t(cx(j), Y0 + 38, lab, 13, c, KR, "middle", 600 if focal else 400)

# 3. 레인 라벨 (3개 역할)
LANES = [
    ("발송 도메인", "발신측 인프라"),
    ("수신 게이트웨이", "프런트 MX"),
    ("내부 사서함", "최종 백엔드 MDA")
]
for k, (a, b) in enumerate(LANES):
    y = lane_top(k) + LANE // 2
    d.t(LABEL_W // 2, y - 4, a, 13, INK, KR, "middle", 600)
    d.t(LABEL_W // 2, y + 14, b, 12, MUTED, KR)

# 4. 연결 화살표 (먼저 그려서 노드 배경 아래 배치)
# 화살표 1: Step 0 (게이트웨이) -> Step 1 (게이트웨이) 수평 (동일 레인)
y1 = ny(1) + NH // 2  # 292
d.arrow([(nx(0) + NW + 2, y1), (nx(1) - 6, y1)], MUTED, "ar", 1.4)

# 화살표 2: Step 1 (게이트웨이) -> Step 2 (내부 사서함) top 진입
y2 = ny(2) + NH // 2  # 396
d.path(f"M {nx(1) + NW + 2} {y1} L {cx(2)} {y1} L {cx(2)} {ny(2) - 6}", MUTED, 1.4, m="ar")

# 화살표 3 (Focal): Step 2 (내부 사서함) -> Step 3 (게이트웨이) bottom 진입
d.path(f"M {nx(2) + NW + 2} {y2} L {cx(3)} {y2} L {cx(3)} {ny(1) + NH + 8}", ACC, 1.7, m="acc")
# Focal 라벨 마스크 (Step 3의 빈 레인 영역 중심)
lab = "550 실패 전달"
focal_lbl_y = (y2 + ny(1) + NH) // 2  # (396 + 332) // 2 = 364
d.o.append(f'<rect x="{cx(3) - 52}" y="{focal_lbl_y - 10}" width="104" height="20" rx="4" fill="{PAPER}" stroke="{ACC}" stroke-width="0.8"/>')
d.t(cx(3), focal_lbl_y + 4, lab, 12, ACC, KR, "middle", 600)

# 화살표 4: Step 3 (게이트웨이) -> Step 4 (발송 도메인) bottom 진입
d.path(f"M {nx(3) + NW + 2} {y1} L {cx(4)} {y1} L {cx(4)} {ny(0) + NH + 8}", OK, 1.4, m="ok")

# 5. 노드 렌더링
# (lane, step, title, sub1, sub2, color, focal)
NODES = [
    (1, 0, "250 OK 접수", "봉투: bounce@...", "헤더: alice@...", None, False),
    (1, 1, "내부 릴레이 시도", "사서함 서버 연결", "SMTP DATA 전달", None, False),
    (2, 2, "550 수신 거부", "사서함 부재 (5.1.1)", "영구 배달 실패", BAD, False),
    (1, 3, "DSN 반송 생성", "수신: bounce@...", "헤더 From 무시", ACC, True),
    (0, 4, "반송 메일 도착", "바운스 주소 수신", "실패 집계 처리", OK, False),
]

for k, j, title, s1, s2, c, focal in NODES:
    x, y = nx(j), ny(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, NW, NH, c, 6, "12", 1.2)
    else:
        d.box(x, y, NW, NH, PAPER, RULE, 1.0, 6)

    tc = ACC if focal else (c or INK)
    d.t(cx(j), y + 26, title, 13, tc, kr(title), "middle", 600)
    d.t(cx(j), y + 48, s1, 12, MUTED, kr(s1))
    d.t(cx(j), y + 68, s2, 12, MUTED, kr(s2))

# 6. 범례
d.legend(H - 44, [
    ("반송 생성 (Focal)", ACC),
    ("영구 실패 (550)", BAD),
    ("정상 반송 완료", OK),
    ("중계 흐름", MUTED)
])

out = Path(__file__).parent.parent / "02-01.bounce-path.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
