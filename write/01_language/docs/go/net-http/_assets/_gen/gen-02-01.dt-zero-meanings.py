# 본문 요구: ### 함정·관찰: 필드마다 다른 0. 같은 0·같은 -1 이 필드마다 다른 뜻이라는 것, 그중 MaxIdleConns 의 -1 이 0 과 정반대라는 것.
# 타입 스펙: type-heatmap
# 사실 출처: go1.25.1 src/net/http/transport.go:1125, 1040-1045, 1053, 1568, 1631, 1134, 1169, 2531-2538, 실측 보고서 시험 3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, KR, MONO

W, H = 960, 520

d = D(W, H,
      "HTTP TRANSPORT ZERO AND NEGATIVE MEANINGS",
      "0 과 음수(-1)의 필드별 동작 의미 비교",
      "MaxIdleConns, MaxIdleConnsPerHost, MaxConnsPerHost, IdleConnTimeout, ExpectContinueTimeout의 DefaultTransport 값, 0, -1 설정 시 동작 차이",
      "같은 0과 -1이라도 필드마다 의미가 다르며 MaxIdleConns의 -1은 0과 정반대로 빈 연결을 풀에 남기지 않습니다")

# 열 레이아웃
# X 시작: 좌측 라벨 컬럼(216px), Col 1(224px), Col 2(224px), Col 3(224px)
C_LABEL_X = 24
C_LABEL_W = 216
COL_W = 224
C0_X = 252
C1_X = 488
C2_X = 724

# 헤더 행
HDR_Y = 104
HDR_H = 36
d.box(C_LABEL_X, HDR_Y, C_LABEL_W, HDR_H, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(C_LABEL_X + 16, HDR_Y + 22, "제어 필드 (net/http)", 12, INK, fam=KR, anchor="start", weight=600)

headers = [
    (C0_X, "DefaultTransport", "리터럴 또는 기본 상수"),
    (C1_X, "0", "zero-value 기본 동작"),
    (C2_X, "-1", "음수 입력 시 분기 동작"),
]

for cx, title, sub in headers:
    d.box(cx, HDR_Y, COL_W, HDR_H, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
    d.t(cx + COL_W // 2, HDR_Y + 16, title, 12, INK, fam=MONO if title in ("0", "-1") else KR, anchor="middle", weight=600)
    d.t(cx + COL_W // 2, HDR_Y + 30, sub, 11, SOFT, fam=KR, anchor="middle")

# 데이터 행 5개
rows = [
    {
        "field": "MaxIdleConns",
        "doc": "전체 호스트 유휴 (1125)",
        "c0": ("100", "전체 호스트 유휴 상한", "neutral"),
        "c1": ("무제한", "풀 크기 제한 없음", "ok"),
        "c2": ("풀 없음", "0 과 정반대 · 풀에 남지 않음", "focal"),
    },
    {
        "field": "MaxIdleConnsPerHost",
        "doc": "호스트당 유휴 (1040)",
        "c0": ("없음 → 2", "const 기본값 대체", "warn"),
        "c1": ("2", "기본값 2 로 대체", "warn"),
        "c2": ("풀에 안 넣음", "응답 뒤 연결을 닫음 (1053)", "bad"),
    },
    {
        "field": "MaxConnsPerHost",
        "doc": "호스트당 총 연결 (1568)",
        "c0": ("없음 → 무제한", "리터럴 생략 시 0", "ok"),
        "c1": ("무제한", "다이얼 개수 미집계", "ok"),
        "c2": ("무제한", "<= 0 조건으로 동일", "ok"),
    },
    {
        "field": "IdleConnTimeout",
        "doc": "유휴 연결 대기 (1134)",
        "c0": ("90s", "90초 유휴 후 폐기", "neutral"),
        "c1": ("타이머 없음", "유휴 연결 유지", "ok"),
        "c2": ("타이머 없음", "> 0 조건 미충족", "ok"),
    },
    {
        "field": "ExpectContinueTimeout",
        "doc": "100 응답 대기 (2531)",
        "c0": ("1s", "1초 대기 후 전송", "neutral"),
        "c1": ("바로 본문", "대기 없이 즉시 전송", "ok"),
        "c2": ("바로 본문", "대기 없이 즉시 전송", "ok"),
    },
]

ROW_Y0 = 148
ROW_H = 54
ROW_GAP = 8

for r_idx, r in enumerate(rows):
    ry = ROW_Y0 + r_idx * (ROW_H + ROW_GAP)
    
    # 좌측 필드명 셀
    d.box(C_LABEL_X, ry, C_LABEL_W, ROW_H, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
    d.t(C_LABEL_X + 14, ry + 22, r["field"], 12, INK, fam=MONO, anchor="start", weight=600)
    d.t(C_LABEL_X + 14, ry + 40, r["doc"], 11, SOFT, fam=KR, anchor="start")
    
    # 3개 열 셀
    cols_data = [
        (C0_X, r["c0"], "DefaultTransport"),
        (C1_X, r["c1"], "0"),
        (C2_X, r["c2"], "-1"),
    ]
    
    for cx, (val, desc, cat), col_name in cols_data:
        data_attrs = f'data-row="{r["field"]}" data-col="{col_name}" data-value="{val}"'
        
        if cat == "neutral":
            d.box(cx, ry, COL_W, ROW_H, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
            d.t(cx + COL_W // 2, ry + 22, val, 13, INK, fam=MONO if any(c.isdigit() for c in val) else KR, anchor="middle", weight=600)
            d.t(cx + COL_W // 2, ry + 40, desc, 11, SOFT, fam=KR, anchor="middle")
        elif cat == "ok":
            d.o.append(f'<rect {data_attrs} x="{cx}" y="{ry}" width="{COL_W}" height="{ROW_H}" rx="4" fill="{OK}16" stroke="{OK}" stroke-width="0.9"/>')
            d.t(cx + COL_W // 2, ry + 22, val, 13, OK, fam=KR, anchor="middle", weight=600)
            d.t(cx + COL_W // 2, ry + 40, desc, 11, OK, fam=KR, anchor="middle", op="0.85")
        elif cat == "warn":
            d.o.append(f'<rect {data_attrs} x="{cx}" y="{ry}" width="{COL_W}" height="{ROW_H}" rx="4" fill="{WARN}16" stroke="{WARN}" stroke-width="0.9"/>')
            d.t(cx + COL_W // 2, ry + 22, val, 13, WARN, fam=KR, anchor="middle", weight=600)
            d.t(cx + COL_W // 2, ry + 40, desc, 11, WARN, fam=KR, anchor="middle", op="0.85")
        elif cat == "bad":
            d.o.append(f'<rect {data_attrs} x="{cx}" y="{ry}" width="{COL_W}" height="{ROW_H}" rx="4" fill="{BAD}18" stroke="{BAD}" stroke-width="1.0"/>')
            d.t(cx + COL_W // 2, ry + 22, val, 13, BAD, fam=KR, anchor="middle", weight=600)
            d.t(cx + COL_W // 2, ry + 40, desc, 11, BAD, fam=KR, anchor="middle", op="0.85")
        elif cat == "focal":
            d.o.append(f'<rect {data_attrs} data-focal="true" x="{cx}" y="{ry}" width="{COL_W}" height="{ROW_H}" rx="4" fill="{ACC}22" stroke="{ACC}" stroke-width="1.5"/>')
            d.t(cx + COL_W // 2, ry + 22, f"{val} (focal)", 13, ACC, fam=KR, anchor="middle", weight=600)
            d.t(cx + COL_W // 2, ry + 40, desc, 11, ACC, fam=KR, anchor="middle")

# 범례
LEGEND_Y = 466
d.legend(LEGEND_Y, [
    ("제한 없음 (무제한 · 대기 없음)", OK),
    ("기본값 대체 (2)", WARN),
    ("풀에 안 넣음 (끔)", BAD),
    ("풀 없음 (0과 정반대 · focal)", ACC),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01.dt-zero-meanings.svg"))
d.save(out_path)
