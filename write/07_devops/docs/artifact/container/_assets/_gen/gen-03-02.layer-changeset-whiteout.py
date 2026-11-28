# 타입 스펙: type-layers
# 03-02 layer 변경분 tar 와 whiteout 가림 구조 (lab-0303/leak:v1 실측값)
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 528

d = D(
    W,
    H,
    "DEVOPS · CONTAINER · 03-02",
    "layer 변경분 tar 와 whiteout 가림 구조",
    "아래에서 위로 쌓이는 세 layer 의 실제 tar 엔트리와 컨테이너 /opt 에서 보이거나 가려지는 결과",
    lead="alpine:3.20(layer 0) 위에 예제 layer 세 장이 쌓인 결과 — 이름·크기는 lab-0303/leak:v1 실측값",
)

# 좌측 적용 순서 축 + 레이어 라벨 열 + 파일 3열
DIR_X = 36
LBL_X, LBL_W = 76, 156
COL_X0, COL_W, COL_GAP = 248, 216, 16
COLS = [COL_X0 + i * (COL_W + COL_GAP) for i in range(3)]
COL_CX = [x + COL_W // 2 for x in COLS]

ROW_H, ROW_GAP = 68, 28
# 위에서 아래 좌표(합쳐진 뷰가 맨 위, layer 1 이 맨 아래)
YS = [100 + i * (ROW_H + ROW_GAP) for i in range(4)]
Y_TOP, Y_L3, Y_L2, Y_L1 = YS

# 좌측 적용 순서 표시 (선 + 짧은 위쪽 화살표로 형제 길이 균형 유지)
MID_Y = (Y_TOP + Y_L1 + ROW_H) // 2
d.t(DIR_X, MID_Y - 8, "적용", 13, SOFT, KR, "middle", 600)
d.t(DIR_X, MID_Y + 10, "순서", 13, SOFT, KR, "middle", 600)
d.line(DIR_X + 24, Y_L1 + ROW_H - 8, DIR_X + 24, MID_Y + 24, SOFT, 1.4)
d.arrow([(DIR_X + 24, MID_Y + 24), (DIR_X + 24, MID_Y - 24)], SOFT, "soft", 1.4)
d.line(DIR_X + 24, MID_Y - 24, DIR_X + 24, Y_TOP + 8, SOFT, 1.4)

# 열 간 전달 화살표 (아래 → 위, 노드보다 먼저 그린다)
for i, cx in enumerate(COL_CX):
    for lower_y, upper_y, col, mk, dash in [
        # layer 1 -> layer 2
        (Y_L1, Y_L2, MUTED if i != 1 else INFO, "ar" if i != 1 else "info", "4 4" if i != 1 else None),
        # layer 2 -> layer 3
        (Y_L2, Y_L3, MUTED if i != 1 else ACC, "ar" if i != 1 else "acc", "4 4" if i != 1 else None),
        # layer 3 -> 컨테이너 /opt
        (Y_L3, Y_TOP, OK if i == 0 else BAD, "ok" if i == 0 else "bad", None),
    ]:
        d.arrow([(cx, lower_y), (cx, upper_y + ROW_H + 2)], col, mk, 1.4, dash)

# 각 행의 외곽 밴드와 좌측 레이어 헤더
ROWS_META = [
    (Y_TOP, "컨테이너 /opt", "합쳐진 뷰", True),
    (Y_L3, "layer 3", "0 B · rm -f", False),
    (Y_L2, "layer 2", "4.2 MB · >> 1B", False),
    (Y_L1, "layer 1", "4.2 MB · dd", False),
]
for ry, title, sub, is_kr_sub in ROWS_META:
    d.box(LBL_X, ry, (COLS[-1] + COL_W) - LBL_X, ROW_H, PAPER, RULE, 0.9, 6)
    d.box(LBL_X + 8, ry + 8, LBL_W - 16, ROW_H - 16, PAPER2, RULE, 0.9, 4)
    d.t(LBL_X + LBL_W // 2, ry + 30, title, 13, INK, KR, "middle", 600)
    d.t(LBL_X + LBL_W // 2, ry + 48, sub, 13 if is_kr_sub else 12, MUTED, KR if is_kr_sub else MONO, "middle")


def cell(col_idx, ry, main, sub, tone=None, is_mono=True):
    x = COLS[col_idx] + 8
    y = ry + 8
    w = COL_W - 16
    h = ROW_H - 16
    if tone:
        sw = 1.6 if tone == ACC else 1.2
        d.tone(x, y, w, h, tone, 4, "14", sw)
        d.t(x + w // 2, y + 22, main, 13 if not is_mono else 12, INK, MONO if is_mono else KR, "middle", 600)
        d.t(x + w // 2, y + 40, sub, 13, tone, KR, "middle")
    else:
        d.box(x, y, w, h, PAPER2, RULE, 0.8, 4)
        d.t(x + w // 2, y + 31, main, 12, SOFT, MONO, "middle")


# Row 3 (bottom): layer 1
cell(0, Y_L1, "opt/app.conf", "10 B 생성", INFO)
cell(1, Y_L1, "opt/big.bin", "4,194,304 B 생성", INFO)
cell(2, Y_L1, "opt/token.txt", "21 B 생성", INFO)

# Row 2: layer 2
cell(0, Y_L2, "-", "", None)
cell(1, Y_L2, "opt/big.bin", "4,194,305 B 전체 복사", ACC)
cell(2, Y_L2, "-", "", None)

# Row 1: layer 3
cell(0, Y_L3, "-", "", None)
cell(1, Y_L3, "opt/.wh.big.bin", "0 B 삭제 표시", BAD)
cell(2, Y_L3, "opt/.wh.token.txt", "0 B 삭제 표시", BAD)

# Row 0 (top): 합쳐진 컨테이너 /opt
cell(0, Y_TOP, "/opt/app.conf", "보임 · 10 B", OK)
cell(1, Y_TOP, "/opt/big.bin", "가려짐 · 8.4 MB 잔류", BAD)
cell(2, Y_TOP, "/opt/token.txt", "가려짐 · layer 1 잔류", BAD)

LEG_Y = Y_L1 + ROW_H + 24
d.legend(
    LEG_Y,
    [
        ("만든 파일", INFO),
        ("고친 파일 전체 복사", ACC),
        ("whiteout · 가려짐", BAD),
        ("컨테이너에 보임", OK),
    ],
)

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "03-02.layer-changeset-whiteout.svg")
d.save(out_path)
print("ok gen-03-02.layer-changeset-whiteout")
