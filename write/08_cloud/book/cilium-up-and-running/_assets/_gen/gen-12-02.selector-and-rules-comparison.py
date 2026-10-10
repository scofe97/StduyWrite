# 타입 스펙: type-dp-security-matrix — 단일 규칙 내 두 문장(AND) 대 두 규칙 분리(OR)의 YAML 구조·판정 조건·보안 결과 비교 행렬. 배정된 comparison 이 스펙 목록에 없어 비교 행렬 스펙의 이 타입으로 선언했다.
# 사실 출처: Cilium Up and Running 12장 cil12.txt 줄 592-608(webserver-8080-from-endpoints.yaml), 620-642(문장 대 규칙 문법 차이 및 보안 영향), 633-642(그림 12-3)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 420
LP, LBL_W, GAP, COL_W = 12, 196, 12, 340
HDR_Y, HDR_H = 96, 44
ROW_Y0, ROW_H, STRIDE = 152, 48, 56
cols = ["단일 규칙 내 두 문장 (AND)", "분리된 두 규칙 (OR)"]
rows = [
    ("YAML 문법 형태", "단일 항목에 두 문장 정의", "대시로 분리된 두 항목 정의", False),
    ("판정 평가 논리", "모든 문장 일치 필요 (AND)", "어느 한 규칙만 일치해도 허용 (OR)", False),
    ("라벨 있는 Pod (test)", "TCP 8080 포트만 허용", "모든 포트 허용 (민감 포트 노출)", True),
    ("라벨 없는 Pod · 외부", "모든 접근 차단 (안전)", "TCP 8080 허용 (외부 무단 접근)", True),
]

d = D(W, H, "CILIUM UP AND RUNNING · 12-02 §1", "단일 규칙 안의 두 문장과 두 규칙의 차이",
      "대시 하나 차이로 AND 결합이 OR 결합으로 바뀌어 보안 구멍이 열린다",
      "대시 하나 차이로 AND 결합이 OR 결합으로 바뀌어 보안 구멍이 열린다")

def cx(j): return LP + LBL_W + GAP + j * (COL_W + GAP)

d.box(LP, HDR_Y, LBL_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LP + LBL_W / 2, HDR_Y + 27, "비교 항목", 13, INK, KR, "middle", 600)
for j, c in enumerate(cols):
    d.box(cx(j), HDR_Y, COL_W, HDR_H, PAPER2, RULE, 0.9, 6)
    d.t(cx(j) + COL_W / 2, HDR_Y + 27, c, 13, INK, KR, "middle", 600)

for i, (lab, a, b, focal) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, LBL_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(LP + 12, y + 29, lab, 12, INK, KR, "start", 600)

    # col 0 (case A)
    d.box(cx(0), y, COL_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(cx(0) + COL_W / 2, y + 29, a, 12, OK if focal else INK, KR, "middle")

    # col 1 (case B)
    if focal:
        d.tone(cx(1), y, COL_W, ROW_H, ACC, r=4, op="14", sw=1.3)
        d.t(cx(1) + COL_W / 2, y + 29, b, 12, ACC, KR, "middle", 600)
    else:
        d.box(cx(1), y, COL_W, ROW_H, PAPER2, RULE, 0.9, 4)
        d.t(cx(1) + COL_W / 2, y + 29, b, 12, INK, KR, "middle")

d.save("12-02.selector-and-rules-comparison.svg")
