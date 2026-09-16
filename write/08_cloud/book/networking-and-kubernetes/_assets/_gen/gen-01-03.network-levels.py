# 01-03.network-levels — 번호 붙은 흐름 + 점선 경계
# 본문: "(4)에서 L2 와 L3 가 갈린다", "바깥으로 가는 프레임은 예외 없이 게이트웨이로 모인다"
#        점선 테두리를 넘는 순간 판단 근거가 MAC 에서 IP 로 바뀐다
# 타입 스펙: type-flowchart.md 관례 + type-nested.md 의 경계 링
#           경계는 점선 한 겹, coral 은 경계를 넘는 그 한 걸음에만.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "INSIDE THE SUBNET · L2 -> L3",
      "내부망을 빠져나가는 순서 — 번호를 따라가면 프레임 한 장의 일생이다",
      "(1) 가른다 → (2) 묻는다 → (3) 넘긴다 → (4) 나간다 → (5) 고른다. 점선을 넘는 순간 판단 근거가 MAC 에서 IP 로 바뀐다.",
      lead="(1) 가른다 → (2) 묻는다 → (3) 넘긴다 → (4) 나간다 → (5) 고른다")

BW, BH = 168, 92
ROW1, ROW2 = 272, 424
ME, SW, GW, RT = 148, 360, 572, 826
RING = (40, 172, 664, 328)

def cell(cx, cy, title, sub, tag, c=None):
    x, y = cx - BW // 2, cy - BH // 2
    d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 22, ddx.fit(title, 13, BW - 20, title), 13, c or INK, KR, "middle", 600)
    d.t(cx, cy - 1, ddx.fit(sub, 12, BW - 20, sub), 12, MUTED, KR)
    d.t(cx, cy + 24, ddx.fit(tag, 11, BW - 16, tag), 11, SOFT, KR)

ddx.band(d, 104, 548, "바깥행 프레임은 모두 게이트웨이로")

# ── 점선 경계 — 브로드캐스트가 닿는 범위 ──────────────────
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
# 링 라벨 마스크는 테두리와 겹친다 — 경계 안쪽 위(첫 줄 칸 위 빈 띠)에 쓴다
d.t(rx + 16, ry + 28, "내부망 — 브로드캐스트가 닿는 범위 (L2)", 12, INFO, KR, "start", 600)

cell(ME, ROW1, "내 PC",     "(1) 안인가 밖인가",  "L2 · 갈림 지점")
cell(SW, ROW1, "스위치",    "(3) MAC 보고 한 대", "L2 · IP 미확인")
cell(GW, ROW1, "게이트웨이", "(4) 바깥행 집결",   "L2 · L3 접점")
cell(SW, ROW2, "이웃 PC",   "(2) 브로드캐스트 수신", "남의 것은 폐기")
cell(RT, ROW1, "바깥 라우터", "(5) IP 로 다음 망", "겉봉 재작성", INFO)
cell(RT, ROW2, "목적 망",    "마지막 홉",         "L3 에서 L2 로", OK)

H2 = BW // 2
d.path(f"M {ME+H2+8} {ROW1} L {SW-H2-10} {ROW1}", MUTED, 1.5, m="ar")
d.path(f"M {SW+H2+8} {ROW1} L {GW-H2-10} {ROW1}", MUTED, 1.5, m="ar")
d.t((SW + GW) // 2, ROW1 - 14, "밖일 때", 11, MUTED, KR)
d.path(f"M {SW} {ROW1+BH//2+6} L {SW} {ROW2-BH//2-10}", MUTED, 1.4, m="ar", dash="6 5")
d.t(SW + 14, (ROW1 + ROW2) // 2 + 4, "조건: MAC 을 모를 때", 11, MUTED, KR, "start")
d.path(f"M {RT} {ROW1+BH//2+6} L {RT} {ROW2-BH//2-10}", MUTED, 1.4, m="ar")
d.t(RT + 14, (ROW1 + ROW2) // 2 + 4, "다음 망", 11, MUTED, KR, "start")

# ── 경계를 넘는 그 한 걸음 (focal) ────────────────────────
d.path(f"M {GW+H2+8} {ROW1} L {RT-H2-10} {ROW1}", ACC, 1.8, m="acc")
# 화살표 가운데에 두면 점선 경계(x=704)를 가로지른다 — 경계 바깥, 바깥 라우터 칸 위에 붙인다
d.t(rx + rw + 8, ROW1 - 72, "근거 전환", 12, ACC, KR, "start", 600)
d.t(rx + rw + 8, ROW1 - 56, "MAC → IP", 11, ACC, MONO, "start")

# 하단 해설((1) 에서 갈리고 (5) 부터 겉봉 재작성)은 도식 뒤 본문 표와 두 문단이 말한다 — 뺐다
d.legend(568, [("경계 안 · L2", INFO), ("도착", OK), ("근거가 바뀌는 걸음", ACC)])
d.save("01-03.network-levels.svg")
print("ok network-levels")
