# 00-01 개요 — 여섯 개념 군(§1~§6)과 군을 잇는 다섯 축의 핵심 용어 전체 지도.
# 사실 출처: 00-01 도입(L17), §1~§6(L23~L116), §용어 간 관계(L119~L129)
# 타입 스펙: type-nested
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 880
OX, OY, OW = 16, 104, 848        # 바깥 틀
CW, CGAP, CPAD = 264, 16, 12     # 카드 폭·간격·안쪽 여백
CH_HEAD, ROW_STRIDE, CARD_H = 44, 28, 168
ROW_GAP = 16
AX_H = 44

groups = [
    ("§1", "저장·인덱스", "3·4장", ["log", "index", "secondary index", "data warehouse"]),
    ("§2", "데이터 모델·일반", "1·2·3장", ["normalized", "denormalize", "system of record", "derived data"]),
    ("§3", "복제·일관성", "6·7장", ["leader", "quorum", "linearizable", "sharding"]),
    ("§4", "트랜잭션·격리", "8장", ["transaction", "serializable", "2PL", "2PC"]),
    ("§5", "분산·합의", "9·10장", ["consensus", "CAP theorem", "Byzantine", "timeout"]),
    ("§6", "배치·스트림", "11·12·13장", ["batch process", "stream process", "event log", "primary key"]),
]
AXES = "derived data · idempotent·deterministic · log · causality·total order · durable"

row1 = OY + 40
row2 = row1 + CARD_H + ROW_GAP
OH = (row2 + CARD_H + CPAD) - OY
AX_Y = OY + OH + 20
LEG = AX_Y + AX_H + 24
H = LEG + 56

d = D(W, H, "00-01 · GLOSSARY MAP", "여섯 개념 군과 군을 잇는 축 전체 지도",
      "핵심 용어 50선을 여섯 개념 군(§1~§6)으로 묶고, 군을 가로지르는 다섯 축을 아래에 띠로 보인다.",
      "여섯 개념 군과 군을 잇는 축")

d.box(OX, OY, OW, OH, PAPER, RULE, 1.0)
d.t(OX + 16, OY + 26, "핵심 용어 50선", 13, INK, KR, "start", 600)

for i, (sec, name, chap, terms) in enumerate(groups):
    r, c = divmod(i, 3)
    x = OX + CPAD + c * (CW + CGAP)
    y = row1 if r == 0 else row2
    d.box(x, y, CW, CARD_H, PAPER2, RULE, 1.0)
    d.chip(x + 26, y + 24, sec, INFO, 11)
    d.t(x + 50, y + 28, name, 13, INK, KR, "start", 600)
    d.t(x + CW - 16, y + 28, chap, 12, MUTED, KR, "end")
    d.line(x + 12, y + CH_HEAD - 4, x + CW - 12, y + CH_HEAD - 4, RULE, 0.8)
    for j, term in enumerate(terms):
        d.t(x + 16, y + CH_HEAD + 16 + j * ROW_STRIDE, term, 12, INFO, MONO, "start")

d.tone(OX, AX_Y, OW, AX_H, ACC, 6, "1F", 1.4)
d.t(OX + 16, AX_Y + 27, "군을 잇는 축", 13, INK, KR, "start", 600)
d.t(OX + 136, AX_Y + 27, AXES, 12, INK, MONO, "start")

d.legend(LEG, [("개념 군", INFO), ("군을 잇는 축", ACC)])
d.save("00-01.glossary-map.svg")
