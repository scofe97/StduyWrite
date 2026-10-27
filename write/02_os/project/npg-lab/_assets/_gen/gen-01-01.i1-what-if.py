# 01-01-i1-what-if — I1 네 가지 개선 후보의 사고 실험 결과 판정 행렬
# 본문 요구(01-01 I1 사고 실험): 개선 후보 넷과 세 지표 영향(프록시 자원·백엔드 창구·단건 조회)의 판정 행렬을 보여 단독 조치의 한계를 드러낸다.
# 타입 스펙: type-dp-security-matrix — 행 넷(개선 후보) × 열 셋(영향 지표) 사고 실험 판정 행렬. focal 은 검색 상한 8 + 2s 기한의 백엔드 창구 32 칸.
# 사실 출처: ch08-slow-search-starves-lookup.md:31-34 (진단 과정 7~10행)
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, BAD, KR, MONO

W = 960
H = 484

# 열 치수 (4의 배수)
LP = 24
LBL_W = 240
GAP = 16
COL_W = 208

# 행 치수 (4의 배수)
HY = 108
HH = 40
Y0 = 164
RH = 52
STRIDE = 64
LEG_Y = 428


def col_x(c):
    return LP + LBL_W + GAP + c * (COL_W + GAP)


def col_cx(c):
    return col_x(c) + COL_W // 2


def row_y(r):
    return Y0 + r * STRIDE


d = D(
    W,
    H,
    "MATRIX · CH08 I1 WHAT-IF",
    "개선 후보 네 가지의 사고 실험 판정 행렬",
    "프록시 타임아웃·연결 상한·격벽·검색 상한 조치가 프록시 자원·백엔드 창구·단건 조회 지연에 미치는 영향 대조",
    lead="프록시 상한은 프록시 자원만 · 백엔드가 취소를 무시하면 창구 32 그대로"
)

# 1. 헤더 행
d.box(LP, HY, LBL_W, HH, PAPER2, RULE, 0.9, 6)
d.t(LP + LBL_W // 2, HY + 25, "개선 조치 후보", 13, INK, KR, "middle", 600)

col_headers = [
    ("프록시 자원", KR),
    ("백엔드 창구 32", KR),
    ("get p99", MONO),
]

for c, (ch_title, ch_fam) in enumerate(col_headers):
    d.box(col_x(c), HY, COL_W, HH, PAPER2, RULE, 0.9, 6)
    d.t(col_cx(c), HY + 25, ch_title, 13, INK, ch_fam, "middle", 600)

# 2. 데이터 행
# 각 셀: (표시 텍스트, 상태색, focal 여부, 폰트)
rows = [
    (
        "ResponseHeaderTimeout 2s",
        MONO,
        [
            ("2s 에 회수 ✓", OK, False, KR),
            ("8s 묶임 ✗", BAD, False, KR),
            ("그대로 ✗", BAD, False, KR),
        ]
    ),
    (
        "MaxConnsPerHost 32",
        MONO,
        [
            ("대기 시 메모리 상승 △", WARN, False, KR),
            ("백엔드 보호 · 헛일 감소 ✓", OK, False, KR),
            ("그대로 ✗", BAD, False, KR),
        ]
    ),
    (
        "격벽 (경로별 상한)",
        KR,
        [
            ("—", MUTED, False, MONO),
            ("—", MUTED, False, MONO),
            ("단건 조회 보호 ✓", OK, False, KR),
        ]
    ),
    (
        "검색 상한 8 + 2s 기한",
        KR,
        [
            ("2s 에 칸 비움 ✓", OK, False, KR),
            ("8 × (8/2) = 32 묶임 ✗", ACC, True, KR),
            ("—", MUTED, False, MONO),
        ]
    ),
]

for r, (r_label, r_fam, cells) in enumerate(rows):
    y = row_y(r)
    # 행 라벨 셀
    d.box(LP, y, LBL_W, RH, PAPER2, RULE, 0.9, 6)
    d.t(LP + 16, y + 32, r_label, 12 if r_fam == MONO else 13, INK, r_fam, "start", 600)

    # 데이터 셀들
    for c, (val, color, is_focal, val_fam) in enumerate(cells):
        bx = col_x(c)
        bcx = col_cx(c)
        if is_focal:
            d.tone(bx, y, COL_W, RH, ACC, 6, "18", 1.6)
            d.t(bcx, y + 32, val, 13, ACC, val_fam, "middle", 600)
        elif color == MUTED:
            d.box(bx, y, COL_W, RH, PAPER2, RULE, 0.9, 6)
            d.t(bcx, y + 32, val, 13, MUTED, val_fam, "middle", 400)
        else:
            d.tone(bx, y, COL_W, RH, color, 6, "12", 1.0)
            d.t(bcx, y + 32, val, 13, color, val_fam, "middle", 600)

# 3. 범례
d.legend(
    LEG_Y,
    [
        ("나아짐 (✓)", OK),
        ("일부 완화 (△)", WARN),
        ("그대로 (✗)", BAD),
        ("핵심 병목", ACC),
    ]
)

d.save("01-01-i1-what-if.svg")
