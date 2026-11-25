# 타입 스펙: type-process
# 6절 업그레이드 시 Values 유지와 초기화 — 플래그별 동작 경로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 500

d = D(W, H, "HELM · UPGRADE VALUES FLAGS",
      "업그레이드 플래그별 Values 유지·초기화 경로",
      "새 차트 기본값과 이전 릴리스 사용자 값의 병합 및 폐기 동작 비교",
      lead="플래그에 따라 이전 사용자 값 또는 새 차트 기본값이 통째 폐기됨 · 안전한 선택 비교")

# 열(Column) 좌표
COL1_X, COL1_W = 24, 180    # 플래그
COL2_X, COL2_W = 216, 216   # 새 차트 기본값 (demo-chart-v2)
COL3_X, COL3_W = 444, 216   # 이전 사용자 값 (리비전 2)
COL4_X, COL4_W = 672, 264   # 최종 결과

# 헤더 라벨 행
HEAD_Y = 96
d.t(COL1_X + COL1_W // 2, HEAD_Y, "업그레이드 조건 (플래그)", 12, SOFT, KR, "middle", 600)
d.t(COL2_X + COL2_W // 2, HEAD_Y, "새 차트 기본값 (v2)", 12, SOFT, KR, "middle", 600)
d.t(COL3_X + COL3_W // 2, HEAD_Y, "이전 사용자 값 (rev 2)", 12, SOFT, KR, "middle", 600)
d.t(COL4_X + COL4_W // 2, HEAD_Y, "최종 렌더 결과", 12, SOFT, KR, "middle", 600)

ROWS = [
    {
        "flag_title": "플래그 없음",
        "flag_sub": "--set timeoutSeconds=60",
        "flag_c": WARN,
        "new_chart": ("timeoutSeconds: 30", "replicas: 1 · INFO"),
        "new_status": ("적용", INFO),
        "old_val": ("replicas: 4", "logLevel: WARN"),
        "old_status": ("폐기", BAD),
        "res_lines": ("timeoutSeconds: 60", "replicas: 1 · INFO"),
        "res_status": ("사용자 값 유실", BAD),
        "focal": False,
    },
    {
        "flag_title": "--reuse-values",
        "flag_sub": "이전 값 강제 재사용",
        "flag_c": WARN,
        "new_chart": ("newFeature: true", "timeoutSeconds: 30"),
        "new_status": ("폐기", BAD),
        "old_val": ("replicas: 4", "logLevel: WARN"),
        "old_status": ("보존", OK),
        "res_lines": ("replicas: 4 · WARN", "newFeature: false"),
        "res_status": ("새 기본값 누락", WARN),
        "focal": False,
    },
    {
        "flag_title": "--reset-values",
        "flag_sub": "기본값 위에 명령행",
        "flag_c": WARN,
        "new_chart": ("newFeature: true", "replicas: 1 · INFO"),
        "new_status": ("적용", OK),
        "old_val": ("replicas: 4", "logLevel: WARN"),
        "old_status": ("폐기", BAD),
        "res_lines": ("newFeature: true", "replicas: 1 · INFO"),
        "res_status": ("사용자 값 초기화", WARN),
        "focal": False,
    },
    {
        "flag_title": "--reset-then-reuse",
        "flag_sub": "기본값·지난 값·명령행",
        "flag_c": ACC,
        "new_chart": ("newFeature: true", "timeoutSeconds: 30"),
        "new_status": ("보존", OK),
        "old_val": ("replicas: 4", "logLevel: WARN"),
        "old_status": ("보존", OK),
        "res_lines": ("replicas: 4 · WARN", "newFeature: true"),
        "res_status": ("둘 다 안전 보존", OK),
        "focal": True,
    },
]

ROW_Y0 = 112
ROW_H = 70
ROW_GAP = 12

for i, r in enumerate(ROWS):
    y = ROW_Y0 + i * (ROW_H + ROW_GAP)
    focal = r["focal"]

    # 1열: 플래그 박스
    border_col = ACC if focal else RULE
    d.box(COL1_X, y, COL1_W, ROW_H, PAPER2, border_col, 1.2 if focal else 0.9)
    d.t(COL1_X + 12, y + 26, r["flag_title"], 12, r["flag_c"], MONO if "--" in r["flag_title"] else KR, "start", 600)
    d.t(COL1_X + 12, y + 46, r["flag_sub"], 11, MUTED, MONO if "--" in r["flag_sub"] else KR, "start")

    # 2열: 새 차트 기본값
    d.box(COL2_X, y, COL2_W, ROW_H, PAPER, RULE, 0.9)
    is_new_bad = r["new_status"][1] == BAD
    col_new = BAD if is_new_bad else INK
    d.t(COL2_X + 10, y + 26, r["new_chart"][0], 11, col_new, MONO, "start")
    d.t(COL2_X + 10, y + 46, r["new_chart"][1], 11, col_new, MONO, "start")
    
    # 2열 칩 (상자 내부 완전 중첩)
    cw2 = 48
    cx2 = COL2_X + COL2_W - cw2 // 2 - 8
    d.o.append(f'<rect x="{cx2 - cw2 // 2}" y="{y + 8}" width="{cw2}" height="20" rx="4" fill="{PAPER}" stroke="{r["new_status"][1]}" stroke-width="0.8"/>')
    d.t(cx2, y + 22, r["new_status"][0], 11, r["new_status"][1], KR, "middle")

    if is_new_bad:
        d.line(COL2_X + 8, y + 22, COL2_X + COL2_W - 64, y + 22, BAD, 1.2)
        d.line(COL2_X + 8, y + 42, COL2_X + COL2_W - 64, y + 42, BAD, 1.2)

    # 3열: 이전 사용자 값
    d.box(COL3_X, y, COL3_W, ROW_H, PAPER, RULE, 0.9)
    is_old_bad = r["old_status"][1] == BAD
    col_old = BAD if is_old_bad else INK
    d.t(COL3_X + 10, y + 26, r["old_val"][0], 11, col_old, MONO, "start")
    d.t(COL3_X + 10, y + 46, r["old_val"][1], 11, col_old, MONO, "start")
    
    # 3열 칩 (상자 내부 완전 중첩)
    cw3 = 48
    cx3 = COL3_X + COL3_W - cw3 // 2 - 8
    d.o.append(f'<rect x="{cx3 - cw3 // 2}" y="{y + 8}" width="{cw3}" height="20" rx="4" fill="{PAPER}" stroke="{r["old_status"][1]}" stroke-width="0.8"/>')
    d.t(cx3, y + 22, r["old_status"][0], 11, r["old_status"][1], KR, "middle")

    if is_old_bad:
        d.line(COL3_X + 8, y + 22, COL3_X + COL3_W - 64, y + 22, BAD, 1.2)
        d.line(COL3_X + 8, y + 42, COL3_X + COL3_W - 64, y + 42, BAD, 1.2)

    # 4열: 최종 렌더 결과
    res_border = ACC if focal else RULE
    d.box(COL4_X, y, COL4_W, ROW_H, PAPER2, res_border, 1.2 if focal else 0.9)
    d.t(COL4_X + 10, y + 26, r["res_lines"][0], 11, INK, MONO, "start", 600 if focal else 400)
    d.t(COL4_X + 10, y + 46, r["res_lines"][1], 11, MUTED if not focal else INK, MONO, "start")
    
    # 4열 칩: 너비 92px, 상자 우측 8px 여백 -> 상자(COL4_X..COL4_X+COL4_W) 내부에 완전히 들어감
    cw4 = 92
    cx4 = COL4_X + COL4_W - cw4 // 2 - 8
    d.o.append(f'<rect x="{cx4 - cw4 // 2}" y="{y + 8}" width="{cw4}" height="20" rx="4" fill="{PAPER}" stroke="{r["res_status"][1]}" stroke-width="0.8"/>')
    d.t(cx4, y + 22, r["res_status"][0], 11, r["res_status"][1], KR, "middle")

    # 수평 화살표 (3열 -> 4열)
    arr_c = ACC if focal else MUTED
    d.arrow([(COL3_X + COL3_W + 2, y + ROW_H // 2), (COL4_X - 2, y + ROW_H // 2)], arr_c, "acc" if focal else "ar", 1.2)

# 범례
LEG_Y = 454
d.legend(LEG_Y, [
    ("값 유지 및 반영", OK),
    ("기본값 합성 (권장)", ACC),
    ("새 기본값 적용", INFO),
    ("값 누락 및 불일치", WARN),
    ("값 통째 폐기", BAD),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm values와 렌더 검증.upgrade-values-flags.svg")
d.save(out_path)
print("ok gen-Helm values와 렌더 검증.upgrade-values-flags")
