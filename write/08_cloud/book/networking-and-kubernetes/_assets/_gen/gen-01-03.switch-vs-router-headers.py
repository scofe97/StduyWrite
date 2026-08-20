# 01-03.switch-vs-router-headers — 중첩 헤더 + 장비별 깊이 대조
# 본문: "프레임은 세 겹, 장비마다 여는 깊이가 다르다"
#        왼쪽이 프레임 한 장의 생김새, 오른쪽 두 행이 그 프레임을 받은 장비가 하는 일의 순서
# 타입 스펙: type-nested.md — 겹은 일정한 inset(가로 28 · 세로 44)으로 3 겹,
#           라벨은 좌상단 paper 마스크 위. coral 은 한 겹에만 → 둘 다 열지 않는 데이터 겹.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 580
d = D(W, H, "ONE FRAME · THREE LAYERS",
      "프레임은 세 겹이고 장비마다 여는 깊이가 다르다",
      "왼쪽이 프레임 한 장의 생김새, 오른쪽 두 행이 그 프레임을 받은 장비가 각각 하는 일의 순서다",
      lead="왼쪽이 프레임 한 장의 생김새 · 오른쪽 두 행이 장비가 하는 일의 순서")

RINGS = [(48, 192, 384, 248, "겉봉 · Ethernet — 목적지 MAC", INFO),
         (76, 236, 328, 160, "속 · IP 헤더 — 8.8.8.8",       WARN),
         (104, 280, 272, 72,  "데이터 · TCP · HTTP",          ACC)]
RX, BW, BH, GAP = 476, 144, 76, 32
CXS = [RX + BW // 2 + i * (BW + GAP) for i in range(3)]        # 548 724 900

ddx.band(d, 104, 520, "겉봉을 여는 깊이가 그 장비가 할 수 있는 일을 정한다")
d.t(48, 168, "프레임 한 장의 생김새 — 겉봉 안에 속, 속 안에 데이터", 12, SOFT, KR, "start", 600)

for x, y, w, h, lab, c in RINGS:
    focal = (c == ACC)
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{c}{"12" if focal else "08"}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    ddx.ring_label(d, x, y, lab, 11, c)
d.t(240, 328, "둘 다 열지 않는다", 12, ACC, KR, "middle", 600)

def row(cy, header, c, steps):
    d.t(RX, cy - BH // 2 - 14, header, 12, c, KR, "start", 600)
    for cx, (t, s) in zip(CXS, steps):
        x = cx - BW // 2
        d.box(x, cy - BH // 2, BW, BH, PAPER2, c, 1.1, 6)
        d.t(cx, cy - 6, ddx.fit(t, 12, BW - 18, t), 12, c, KR, "middle", 600)
        d.t(cx, cy + 15, ddx.fit(s, 11, BW - 18, s), 11, MUTED, KR)
    for a, b in zip(CXS, CXS[1:]):
        d.path(f"M {a+BW//2+6} {cy} L {b-BW//2-10} {cy}", MUTED, 1.4, m="ar")

row(248, "스위치 · L2 — 겉봉만 연다", INFO,
    [("겉봉을 읽는다", "목적지 MAC"), ("MAC 표 조회", "나갈 포트 하나"), ("그대로 전달", "겉봉을 안 고침")])
row(396, "라우터 · L3 — 속의 IP 까지 연다", WARN,
    [("속을 읽는다", "목적지 IP"), ("라우팅 표 조회", "다음 홉"), ("겉봉 교체", "속 IP 는 그대로")])

d.t(36, 488, "스위치가 겉봉을 고치지 않는 것과 라우터가 겉봉을 갈아 끼우는 것이 "
             "같은 프레임에서 갈린다 — 여는 깊이가 하나 다를 뿐이다", 12, MUTED, KR, "start")
d.legend(536, [("겉봉 · 스위치", INFO), ("속 · 라우터", WARN), ("아무도 안 여는 겹", ACC)])
d.save("01-03.switch-vs-router-headers.svg")
print("ok switch-vs-router")
