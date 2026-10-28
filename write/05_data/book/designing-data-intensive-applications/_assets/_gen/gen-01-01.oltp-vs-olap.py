# 01-01 §3 — OLTP 와 OLAP 은 같은 데이터에 던지는 질문의 모양이 다르다.
# 옛 도식은 본문 8행 비교표를 다시 적고 웨어하우스·레이크 흐름까지 한 장에 넣었다. 표는 본문이 이미 갖고 있어서,
#   여기서는 표가 못 보이는 것 하나만 그린다 — 키로 한 건을 집는 접근과 전 레코드를 훑어 집계하는 접근.
#   ETL·웨어하우스·레이크 흐름은 §4 이후 본문이 말로 맡는다.
# 타입 스펙: type-heatmap
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 880
PX, PW, PGAP, PY = 16, 416, 16, 104
HEAD_H = 44
COLS, ROWS = 5, 8
CELL_W, CELL_H, CSTR, RSTR = 36, 20, 44, 28
GX, GY = 24, 172 - PY            # 격자 좌상단(패널 안)
CHIP_Y, CHIP_STR, CHIP_H = 408 - PY, 36, 28
PH = (CHIP_Y + 2 * CHIP_STR + CHIP_H + 16)
LEG = PY + PH + 16
H = LEG + 56

panels = [
    ("운영 · OLTP", "point query", INFO, {3}, "레코드 1건", "",
     ["키로 한 건 조회", "작은 쿼리 다수", "현재 시점 최신 상태"]),
    ("분석 · OLAP", "집계 쿼리", ACC, set(range(ROWS)), "집계 통계", "count · sum · average",
     ["대량 레코드 집계", "복잡한 쿼리 소수", "시간에 걸친 이벤트 이력"]),
]

d = D(W, H, "01-01 · OLTP VS OLAP", "운영과 분석은 질문의 모양이 다르다",
      "운영 시스템은 키로 레코드 한 건을 찾아 읽고 쓰고, 분석 시스템은 대량 레코드를 훑어 집계 통계를 낸다. 오른쪽 분석의 대량 집계가 두 접근을 가르는 지점이다.",
      "같은 레코드 격자에 던지는 두 질문")

for i, (name, sub, c, hit, res, res2, chips) in enumerate(panels):
    x = PX + i * (PW + PGAP)
    d.box(x, PY, PW, PH, PAPER2, RULE, 1.0)
    d.t(x + 16, PY + 28, name, 14, INK, KR, "start", 600)
    d.t(x + PW - 16, PY + 28, sub, 12, MUTED, MONO if sub.isascii() else KR, "end")
    d.line(x + 12, PY + HEAD_H, x + PW - 12, PY + HEAD_H, RULE, 0.8)
    for r in range(ROWS):
        for k in range(COLS):
            cx, cy = x + GX + k * CSTR, PY + GY + r * RSTR
            if r in hit:
                d.tone(cx, cy, CELL_W, CELL_H, c, 3, "33", 1.0)
            else:
                d.box(cx, cy, CELL_W, CELL_H, PAPER, RULE, 0.8, 3)
    gx1 = x + GX + COLS * CSTR - (CSTR - CELL_W)
    mid = PY + GY + (ROWS * RSTR - (RSTR - CELL_H)) / 2
    ay = (PY + GY + 3 * RSTR + CELL_H / 2) if len(hit) == 1 else mid
    d.arrow([(gx1 + 8, ay), (gx1 + 36, ay)], c, "acc" if c == ACC else "info", 1.6)
    rx = gx1 + 44
    rh = 44 if res2 else 28
    d.tone(rx, ay - rh / 2, 116, rh, c, 6, "14", 1.2)
    if res2:
        d.t(rx + 58, ay - 3, res, 13, INK, KR, "middle", 600)
        d.t(rx + 58, ay + 14, "count·sum·avg", 11, MUTED, MONO)
    else:
        d.t(rx + 58, ay + 5, res, 13, INK, KR, "middle", 600)
    for j, txt in enumerate(chips):
        cy = PY + CHIP_Y + j * CHIP_STR
        d.box(x + 24, cy, PW - 48, CHIP_H, PAPER, RULE, 0.9)
        d.t(x + 40, cy + 19, txt, 13, INK, KR, "start")

d.legend(LEG, [("운영 · 한 건 조회", INFO), ("분석 · 전체 훑기", ACC)])
d.save("01-01.oltp-vs-olap.svg")
