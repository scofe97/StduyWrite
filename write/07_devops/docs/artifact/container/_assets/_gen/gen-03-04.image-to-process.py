# 타입 스펙: type-data-flow
# 03-04.image-to-process — OCI 이미지가 변환·압축 해제를 거쳐 번들과 runc 를 지나 컨테이너 프로세스가 되는 흐름
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 456

d = D(
    W,
    H,
    "DEVOPS · CONTAINER · 03-04",
    "이미지에서 컨테이너 프로세스까지",
    "OCI 이미지의 config 와 layer 가 변환·해제를 거쳐 번들이 되고 runc create 와 start 로 프로세스가 되는 흐름",
    lead="image-spec 산출물 → conversion · unpack → OCI 번들(config.json + rootfs) → runc create · start",
)

# 5단계 열 + 3개 레인 (모든 좌표 4의 배수)
LANE_X, LANE_W = 16, 92
COL_X0, SLOT, CARD_W, CARD_H = 124, 168, 128, 60
STEP_Y = 92
LANE_Y0, LANE_STRIDE = 152, 80

STEPS = [
    ("01", "이미지", False),
    ("02", "변환·해제", False),
    ("03", "OCI 번들", True),
    ("04", "create", False),
    ("05", "프로세스", False),
]

LANES = [
    ("설정 JSON", "config", INFO),
    ("파일시스템", "rootfs", INFO),
    ("런타임", "runc", OK),
]


def col_x(c):
    return COL_X0 + SLOT * c


def col_cx(c):
    return col_x(c) + CARD_W // 2


def lane_y(r):
    return LANE_Y0 + LANE_STRIDE * r + 8


# 단계 머리 칩
for idx, (num, label, is_focal) in enumerate(STEPS):
    cx = col_cx(idx)
    c = ACC if is_focal else MUTED
    fill = f"{ACC}22" if is_focal else PAPER2
    stroke = ACC if is_focal else RULE
    d.box(cx - 52, STEP_Y, 104, 28, fill, stroke, 1.2 if is_focal else 0.9, 14)
    d.t(cx, STEP_Y + 18, f"{num} · {label}", 13, c if is_focal else INK, KR, "middle", 600)

# 좌측 레인 머리
for r, (nm, sub, c) in enumerate(LANES):
    y = LANE_Y0 + LANE_STRIDE * r
    d.box(LANE_X, y, LANE_W, 76, PAPER2, RULE, 0.9, 6)
    d.t(LANE_X + LANE_W // 2, y + 32, nm, 13, INK, KR, "middle", 600)
    d.t(LANE_X + LANE_W // 2, y + 52, sub, 12, MUTED, MONO, "middle")

# OCI 번들 경계 (focal) — 위쪽 라벨 공간 확보
bx = col_x(2) - 8
by = lane_y(0) - 24
bw = CARD_W + 16
bh = LANE_STRIDE + CARD_H + 32
d.o.append(
    f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" '
    f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 4"/>'
)
d.t(bx + bw // 2, by + 16, "OCI 번들", 13, ACC, KR, "middle", 600)

# ── 화살표 (노드보다 먼저 그린다) ──
y0 = lane_y(0) + CARD_H // 2
y1 = lane_y(1) + CARD_H // 2
y2 = lane_y(2) + CARD_H // 2

# 설정 줄: Col 0 -> Col 1 -> Col 2
d.arrow([(col_x(0) + CARD_W, y0), (col_x(1) - 2, y0)], INFO, "info", 1.4)
d.arrow([(col_x(1) + CARD_W, y0), (col_x(2) - 2, y0)], INFO, "info", 1.4)

# 파일시스템 줄: Col 0 -> Col 1 -> Col 2
d.arrow([(col_x(0) + CARD_W, y1), (col_x(1) - 2, y1)], INFO, "info", 1.4)
d.arrow([(col_x(1) + CARD_W, y1), (col_x(2) - 2, y1)], INFO, "info", 1.4)

# 번들 경계 오른쪽 -> runc create (직각 꺾임)
bundle_mid_y = (y0 + y1) // 2
d.arrow([(bx + bw, bundle_mid_y), (col_cx(3), bundle_mid_y), (col_cx(3), lane_y(2) - 2)], ACC, "acc", 1.6)
d.t(col_cx(3) + 10, bundle_mid_y + 16, "번들 경로", 13, ACC, KR, "start", 600)

# runc create -> 컨테이너 프로세스 (gap=40px, start 라벨을 화살표 위에 배치)
d.arrow([(col_x(3) + CARD_W, y2), (col_x(4) - 2, y2)], OK, "ok", 1.5)
d.t((col_x(3) + CARD_W + col_x(4)) // 2, y2 - 12, "start", 10.5, OK, MONO, "middle", 600)

# ── 노드 카드 ──
NODES = [
    (0, 0, "image config", "Cmd·Env·User", INFO, True),
    (0, 1, "conversion", "필드 변환", INFO, True),
    (0, 2, "config.json", "process·mounts", ACC, True),
    (1, 0, "manifest·layers", "tar.gz 변경분", INFO, True),
    (1, 1, "unpack·.wh.", "레이어 해제", INFO, True),
    (1, 2, "rootfs/", "root.path 대상", ACC, True),
    (2, 3, "runc create", "status: created", MUTED, True),
    (2, 4, "컨테이너 프로세스", "status: running", OK, False),
]

for r, c, title, sub, tone, title_mono in NODES:
    x = col_x(c)
    y = lane_y(r)
    if tone == MUTED:
        d.box(x, y, CARD_W, CARD_H, PAPER2, MUTED, 1.2, 6)
        tc = INK
    else:
        d.tone(x, y, CARD_W, CARD_H, tone, 6, "14", 1.4 if tone == ACC else 1.2)
        tc = tone
    d.t(x + CARD_W // 2, y + 24, title, 12.5 if title_mono else 13, tc, MONO if title_mono else KR, "middle", 600)
    sub_is_kr = any("가" <= ch <= "힣" for ch in sub)
    d.t(x + CARD_W // 2, y + 44, sub, 13 if sub_is_kr else 11.5, INK if tone == ACC else MUTED, KR if sub_is_kr else MONO, "middle")

LEG_Y = 408
d.legend(
    LEG_Y,
    [
        ("이미지·변환", INFO),
        ("OCI 번들", ACC),
        ("runc 구성", MUTED),
        ("실행 중", OK),
    ],
)

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "03-04.image-to-process.svg")
d.save(out_path)
print("ok gen-03-04.image-to-process")
