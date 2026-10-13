# 타입 스펙: type-process — 레인 셋(몫 · 나머지 · 문자)이 나눗셈 회차마다 이어지고 칸마다 실제 값이 바뀐다(스펙 §2 공식의 label_col_w 140 · right_pad 28 을 따르고 step_slot_w 는 124 로 넓혔다).
# 사실 출처: 추출본 v2.txt 2223~2231행·PDF 127쪽 base62 변환 풀이(11157 = 2×62² + 55×62 + 59 → [2, T, X]),
#   계산: 11157 = 62×179 + 59, 179 = 62×2 + 55, 2 = 62×0 + 2. 대응은 0-9→0~9, a-z→10~35, A-Z→36~61(55 → T, 59 → X).
# Layout conventions: 노드 폭 100 · 높이 64, 레인 stride 80, 칸 stride 124. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, RULE, SOFT, INFO, KR, MONO

LCW, SLOT, NW, NH = 140, 124, 100, 64
NS = 5
W = LCW + NS * SLOT + 28
HDR_Y, L1_Y, L2_Y, L3_Y = 100, 136, 216, 296
H = 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 08-01 §5",
      "11157 을 62 로 세 번 나눈 나머지가 2TX 가 된다",
      "몫이 0 이 될 때까지 62 로 나누고, 나머지를 문자로 바꿔 마지막 나머지부터 읽는다.",
      "실제 값이 회차마다 바뀐다")


def nx(j):
    return LCW + j * SLOT + 12


def node(j, y, title, sub, c, focal=False):
    x = nx(j)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    else:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    d.t(x + NW / 2, y + 28, title, 14, INK if not focal else ACC, MONO, "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


for j, lab in enumerate(["입력", "1회째", "2회째", "3회째", "읽기"]):
    d.t(nx(j) + NW / 2, HDR_Y + 12, lab, 12, SOFT, KR, "middle", 600)

for y, lab in ((L1_Y, "몫"), (L2_Y, "나머지"), (L3_Y, "문자")):
    d.line(LCW - 8, y - 12, W - 24, y - 12, RULE, 0.8)
    d.t(24, y + 30, lab, 13, INK, KR, "start", 600)

# 레인 1 — 몫
for j, (q, sub) in enumerate([("11157", "입력"), ("179", "11157 ÷ 62"), ("2", "179 ÷ 62"), ("0", "2 ÷ 62")]):
    node(j, L1_Y, q, sub, INFO)
for j in range(3):
    d.arrow([(nx(j) + NW + 2, L1_Y + NH // 2), (nx(j + 1) - 6, L1_Y + NH // 2)], MUTED, "ar", 1.5)

# 레인 2 — 나머지, 레인 3 — 문자 (회차마다 몫 노드 아래로 내려온다)
for j, (r, ch) in zip((1, 2, 3), (("59", "X"), ("55", "T"), ("2", "2"))):
    node(j, L2_Y, r, "나머지", OK)
    node(j, L3_Y, ch, f"{r} → {ch}", WARN)
    cx = nx(j) + NW // 2
    d.arrow([(cx, L1_Y + NH + 2), (cx, L2_Y - 6)], INFO, "info", 1.5)
    d.arrow([(cx, L2_Y + NH + 2), (cx, L3_Y - 6)], OK, "ok", 1.5)

node(4, L3_Y, "2TX", "3회째부터 읽기", ACC, True)
d.arrow([(nx(3) + NW + 2, L3_Y + NH // 2), (nx(4) - 6, L3_Y + NH // 2)], MUTED, "ar", 1.5)

d.legend(H - 56, [("몫", INFO), ("나머지", OK), ("문자", WARN), ("결과", ACC)])
d.save("08-01.base62-division.svg")
