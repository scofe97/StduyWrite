# 타입 스펙: type-process — 레인 둘(저장 용량 · CDN 전송)이 일간 사용자 5,000,000 에서 갈라지고 칸마다 실제 값이 바뀐다(스펙 §2 공식의 label_col_w 140 · right_pad 28 을 따르고 step_slot_w 는 124 로 넓혔다).
# 사실 출처: 가정은 추출본 v2.txt 3931~3935행(DAU 5 M · 하루 5 편 · 10% 업로드 · 300 MB)·3939~3942행(전송 단가 $0.02/GB · 하루 $150,000)이고 결과 150 TB 도 3935행.
#   계산: 5,000,000 × 10% = 500,000 · 500,000 × 300 MB = 150,000,000 MB = 150 TB · 5,000,000 × 5 = 25,000,000 · 25,000,000 × 0.3 GB = 7,500,000 GB · 7,500,000 × $0.02 = $150,000.
#   계단식: AWS Price List(AmazonCloudFront 20261003000426, 2026-10-01 시행) 미국 구간 $0.085·$0.080·$0.060·$0.040·$0.030·$0.025·$0.020(5 PB 초과)로 월 225,000,000 GB 를 합산하면 $4,540,724.48 → 30 일 환산 ≈ $151,357.
# Layout conventions: 노드 폭 100 · 높이 64, 레인 stride 80, 칸 stride 124(스펙 112 에서 12 늘려 화살표 구간 24 확보). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, SOFT, INFO, RULE, KR, MONO

LCW, SLOT, NW, NH = 140, 124, 100, 64
NS = 5
W = LCW + NS * SLOT + 28
HDR_Y, L1_Y, L2_Y = 100, 136, 216
H = 404
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-01 §1",
      "사용자 5,000,000 명에서 150 TB 와 $150,000 이 갈라져 나온다",
      "하루 업로드 500,000 건 × 300 MB 는 150 TB 이고, 하루 시청 25,000,000 회 × 0.3 GB 는 7,500,000 GB 이며 GB 당 $0.02 면 $150,000, 구간 요금표로 합산하면 ≈ $151,357 이다.",
      "실제 값이 칸마다 바뀐다 · 설계 가정")


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


def nx(j):
    return LCW + j * SLOT + 12


def node(j, y, title, sub, c, focal=False):
    x = nx(j)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    else:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    d.t(x + NW / 2, y + 28, title, 12, INK if not focal else ACC, fam(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, fam(sub))


for j, lab in enumerate(["가정", "건수", "용량", "결과", "구간 요금"]):
    d.t(nx(j) + NW / 2, HDR_Y + 12, f"{j + 1} · {lab}", 12, SOFT, KR, "middle", 600)

d.line(LCW - 8, L1_Y - 12, W - 24, L1_Y - 12, RULE, 0.8)
d.line(LCW - 8, L2_Y - 12, W - 24, L2_Y - 12, RULE, 0.8)
d.t(24, L1_Y + 30, "저장 용량", 13, INK, KR, "start", 600)
d.t(24, L2_Y + 30, "CDN 전송", 13, INK, KR, "start", 600)

# 레인 1 — 저장 용량
node(0, L1_Y, "5,000,000", "DAU", INFO)
node(1, L1_Y, "500,000 건", "× 10 % 업로드", OK)
node(2, L1_Y, "150,000,000", "MB · × 300 MB", OK)
node(3, L1_Y, "150 TB", "÷ 1,000,000", WARN)
for j in range(3):
    d.arrow([(nx(j) + NW + 2, L1_Y + NH // 2), (nx(j + 1) - 6, L1_Y + NH // 2)], MUTED, "ar", 1.5)

# 레인 2 — CDN 전송 (DAU 에서 갈라짐)
node(1, L2_Y, "25,000,000 회", "× 5 편 시청", OK)
node(2, L2_Y, "7,500,000", "GB · × 0.3 GB", OK)
node(3, L2_Y, "$150,000", "× $0.02 /GB", ACC, True)
node(4, L2_Y, "$151,357", "구간 요금표 합산", WARN)
cx = nx(0) + NW // 2
d.arrow([(cx, L1_Y + NH + 2), (cx, L2_Y + NH // 2), (nx(1) - 6, L2_Y + NH // 2)], INFO, "info", 1.5)
for j in (1, 2, 3):
    d.arrow([(nx(j) + NW + 2, L2_Y + NH // 2), (nx(j + 1) - 6, L2_Y + NH // 2)], MUTED, "ar", 1.5)

d.legend(H - 56, [("사용자 수", INFO), ("중간 값", OK), ("결과", WARN), ("본문이 짚는 값", ACC)])
d.save("14-01.cost-calc.svg")
