# 타입 스펙: type-process — 레인 둘(초당 요청 · 저장 용량)이 DAU 에서 갈라지고 칸마다 실제 값이 바뀐다(스펙 §2 공식의 label_col_w 140 · right_pad 28 을 따르고 step_slot_w 는 124 로 넓혔다).
# 사실 출처: 추출본 v2.txt 601~621행·PDF 38쪽 아래~39쪽 예제 가정(MAU 300 M · 일간 50% · 하루 2 글 · 미디어 10% · 1 MB · 5 년)과 결과(DAU 150 M · ≈ 3,500 QPS · 피크 ≈ 7,000 · 30 TB/일 · ≈ 55 PB).
#   계산: 150 M × 2 ÷ 86,400 = 3,472.2 → ≈ 3,500, 피크 = 2 × 3,500 = 7,000, 150 M × 2 × 10% × 1 MB = 30 M MB = 30 TB, 30 TB × 365 × 5 = 54,750 TB ≈ 55 PB.
# Layout conventions: 노드 폭 100 · 높이 64, 레인 stride 80, 칸 stride 124(스펙 112 에서 12 늘려 화살표 구간 24 확보). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

LCW, SLOT, NW, NH = 140, 124, 100, 64
NS = 5
W = LCW + NS * SLOT + 28
HDR_Y, L1_Y, L2_Y = 100, 136, 216
H = 404
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 02-01 §4",
      "가정 여섯 값에서 3,500 QPS 와 55 PB 가 나온다",
      "MAU 300 M 의 절반이 하루 2 글을 올린다. DAU 150 M 에서 초당 요청 ≈ 3,500(피크 ≈ 7,000)과 미디어 30 TB/일 → 5 년 ≈ 55 PB 가 갈라져 나온다.",
      "실제 값이 칸마다 바뀐다")


def nx(j):
    return LCW + j * SLOT + 12


def node(j, y, title, sub, c, focal=False):
    x = nx(j)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    else:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    d.t(x + NW / 2, y + 28, title, 12, INK if not focal else ACC, KR if any("가" <= ch <= "힣" for ch in title) else MONO, "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


for j, lab in enumerate(["가정", "사용자", "변환", "다음 값", "결과"]):
    x = nx(j)
    d.t(x + NW / 2, HDR_Y + 12, f"{j + 1} · {lab}", 12, SOFT, KR, "middle", 600)

d.line(LCW - 8, L1_Y - 12, W - 24, L1_Y - 12, RULE, 0.8)
d.line(LCW - 8, L2_Y - 12, W - 24, L2_Y - 12, RULE, 0.8)
d.t(24, L1_Y + 30, "초당 요청", 13, INK, KR, "start", 600)
d.t(24, L2_Y + 30, "저장 용량", 13, INK, KR, "start", 600)

# 레인 1 — 초당 요청
node(0, L1_Y, "300 M MAU", "× 50 %", INFO)
node(1, L1_Y, "150 M DAU", "하루 사용자", INFO)
node(2, L1_Y, "× 2 ÷ 86,400", "= 3,472 QPS", OK)
node(3, L1_Y, "≈ 3,500", "QPS 반올림", WARN)
node(4, L1_Y, "≈ 7,000", "피크 = 평균 × 2", WARN)
for j in range(4):
    d.arrow([(nx(j) + NW + 2, L1_Y + NH // 2), (nx(j + 1) - 6, L1_Y + NH // 2)], MUTED, "ar", 1.5)

# 레인 2 — 저장 용량 (DAU 에서 갈라짐)
node(2, L2_Y, "30 TB/일", "×2 ×10% ×1MB", OK)
node(3, L2_Y, "54,750 TB", "× 365 × 5", OK)
node(4, L2_Y, "≈ 55 PB", "5 년 보관", ACC, True)
cx = nx(1) + NW // 2
d.arrow([(cx, L1_Y + NH + 2), (cx, L2_Y + NH // 2), (nx(2) - 6, L2_Y + NH // 2)], INFO, "info", 1.5)
for j in (2, 3):
    d.arrow([(nx(j) + NW + 2, L2_Y + NH // 2), (nx(j + 1) - 6, L2_Y + NH // 2)], MUTED, "ar", 1.5)

d.legend(H - 56, [("가정 입력", INFO), ("계산 값", OK), ("반올림 값", WARN), ("짚는 값", ACC)])
d.save("02-01.qps-storage-flow.svg")
