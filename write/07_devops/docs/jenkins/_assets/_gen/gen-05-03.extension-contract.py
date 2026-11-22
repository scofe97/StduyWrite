# 타입 스펙: type-process
# 4절 Extension Point 와 3단 계약 — 정의, 등록, 발견 단계별 주체와 식별자
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 920, 432

d = D(W, H, "JENKINS · EXTENSION POINT",
      "Extension Point 와 3단 계약",
      "인터페이스 선언, 어노테이션 색인, 전역 목록 조회의 3단계 확장 계약과 주체 및 식별자",
      lead="인터페이스 정의 → 어노테이션 색인 등록 → 전역 목록 발견")

# ── 3단계 컬럼 정의 ──────────────────────────────────────────────────────
COL_W = 264
COL_GAP = 28
X0 = 36

STEPS = [
    ("1. 정의", "꽂을 자리 선언", INFO),
    ("2. 등록", "컴파일 시점 색인", ACC),
    ("3. 발견", "전역 목록 조회", OK),
]

HEADER_Y = 104
HEADER_H = 48

for i, (title, sub, col) in enumerate(STEPS):
    x = X0 + i * (COL_W + COL_GAP)
    d.box(x, HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(x + COL_W // 2, HEADER_Y + 20, title, 13, col, KR, "middle", 600)
    d.t(x + COL_W // 2, HEADER_Y + 36, sub, 11, MUTED, KR, "middle")

    if i < len(STEPS) - 1:
        ax1 = x + COL_W + 4
        ax2 = x + COL_W + COL_GAP - 4
        ay = HEADER_Y + HEADER_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.4)

# ── 슬롯 1 (누가) & 슬롯 2 (무엇을 쓰는가) ──────────────────────────────
SLOT1_Y = 168
SLOT1_H = 64

SLOT2_Y = 248
SLOT2_H = 112

DATA = [
    # Step 1: 정의
    {
        "actor": "인터페이스나 추상 클래스",
        "id_primary": "ExtensionPoint",
        "id_primary_col": INFO,
        "id_secondary": "상속",
        "id_sec_mono": False,
    },
    # Step 2: 등록
    {
        "actor": "구현 클래스",
        "id_primary": "@Extension",
        "id_primary_col": ACC,
        "id_secondary": "SezPoz 색인",
        "id_sec_mono": False,
    },
    # Step 3: 발견
    {
        "actor": "코어나 소비자",
        "id_primary": "ExtensionList.lookup(Class)",
        "id_primary_col": OK,
        "id_secondary": "RunListener.all()",
        "id_sec_mono": True,
    },
]

for i, item in enumerate(DATA):
    x = X0 + i * (COL_W + COL_GAP)
    cx = x + COL_W // 2

    # 슬롯 1: 누가
    d.box(x, SLOT1_Y, COL_W, SLOT1_H, PAPER2, RULE, 1.0)
    d.t(x + 16, SLOT1_Y + 20, "누가", 11, SOFT, KR, "start", 600)
    d.t(x + 16, SLOT1_Y + 44, item["actor"], 13, INK, KR, "start", 600)

    # 슬롯 1 → 슬롯 2 연결 화살표
    d.arrow([(cx, SLOT1_Y + SLOT1_H + 2), (cx, SLOT2_Y - 2)], MUTED, "ar", 1.2)

    # 슬롯 2: 무엇을 쓰는가
    d.box(x, SLOT2_Y, COL_W, SLOT2_H, PAPER2, RULE, 1.0)
    d.t(x + 16, SLOT2_Y + 20, "무엇을 쓰는가", 11, SOFT, KR, "start", 600)

    # 1차 식별자 박스
    col = item["id_primary_col"]
    d.box(x + 12, SLOT2_Y + 30, COL_W - 24, 34, PAPER, col, 1.0, r=4)
    fam_primary = MONO if any(c in item["id_primary"] for c in "@.()") or item["id_primary"].isascii() else KR
    font_size = 11 if len(item["id_primary"]) > 20 else 12
    d.t(x + 20, SLOT2_Y + 52, item["id_primary"], font_size, col, fam_primary, "start", 600)

    # 2차 식별자 / 메커니즘
    fam_sec = MONO if item["id_sec_mono"] else KR
    d.t(x + 16, SLOT2_Y + 92, item["id_secondary"], 12, MUTED, fam_sec, "start")

d.legend(380, [("1. 정의", INFO), ("2. 등록", ACC), ("3. 발견", OK)])
d.save(str(pathlib.Path(__file__).resolve().parent.parent / "05-03.extension-contract.svg"))
