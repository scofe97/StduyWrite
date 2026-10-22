# 타입 스펙: type-data-flow — 여러 경로가 하나로 몰리는 fan-in. 차 키 도난 위협 세 경로가 완화 한 칸에서 모두 막히고 리스크에 닿지 못한다(semantic-patterns 의 Fan-in 변형: 몰린 곳을 막는 쪽이 논지). focal 은 완화.
# 사실 출처: 노트 L49~L51(세 용어), L53(자동차 키 비유: 창문 깨기 · 우편함 낚싯대 · 초인종 공범, 키를 눈에 안 띄는 곳에 두면 세 위협을 한꺼번에 막음)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, KR, MONO

W, H = 984, 520


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "DATA-FLOW · 01-01 §1",
      "완화 하나가 위협 세 경로를 한꺼번에 막습니다",
      "차 키를 훔쳐 차를 몰고 가는 리스크로 가는 길이 셋이다. 창문을 깨고 손을 넣는 길, 우편함에 낚싯대를 넣는 길, 초인종으로 주의를 끈 사이 공범이 들어오는 길이다. "
      "키를 눈에 안 띄는 곳에 두면 세 길이 모두 끊긴다.",
      lead="리스크는 문제 자체, 위협은 거기로 가는 길, 완화는 그 길을 끊는 대응입니다.")

THREATS = [
    ("창문 깨고 손 넣기", "유리를 깨고 키를 집음"),
    ("우편함에 낚싯대", "넣어서 키를 끌어냄"),
    ("초인종 눌러 주의 끌기", "그 사이 공범이 들어옴"),
]
TX, TW, TH = 36, 332, 72
RY0, RSTRIDE = 132, 96

# 열 머리
d.t(TX, 108, "위협 — 리스크로 가는 길", 12, MUTED, KR, "start", 600)
GX, GW = 464, 160
d.t(GX + GW / 2, 108, "완화", 12, MUTED, KR, "middle", 600)
RX, RW = 724, 224
d.t(RX, 108, "리스크", 12, MUTED, KR, "start", 600)

# 완화 칸: 세 길을 모두 가로지르는 focal
GY, GH = 132, 264
d.tone(GX, GY, GW, GH, ACC, 6, "1F", 1.6)
for s, y in (("키를 눈에", 244), ("안 띄는 곳에", 268), ("둔다", 292)):
    fit(s, 13, GW - 16)
    d.t(GX + GW / 2, y, s, 13, ACC, KR, "middle", 600)

# 리스크 칸: 세 길의 도착점
d.tone(RX, RY0, RW, 264, WARN, 6, "14", 1.2)
d.t(RX + RW / 2, RY0 + 124, "차 키 도난", 14, WARN, KR, "middle", 600)
d.t(RX + RW / 2, RY0 + 150, "차를 몰고 감", 12, MUTED, KR, "middle")

for i, (title, sub) in enumerate(THREATS):
    y = RY0 + i * RSTRIDE
    fit(title, 13, TW - 32)
    fit(sub, 12, TW - 32)
    d.tone(TX, y, TW, TH, BAD, 6, "14", 1.1)
    d.t(TX + 16, y + 24, str(i + 1), 11, SOFT, MONO, "start")
    d.t(TX + TW / 2, y + 32, title, 13, BAD, KR, "middle", 600)
    d.t(TX + TW / 2, y + 54, sub, 12, MUTED, KR, "middle")
    cy = y + TH // 2
    # 위협 → 완화: 막히는 화살표
    d.arrow([(TX + TW + 2, cy), (GX - 4, cy)], BAD, "bad", 1.5)
    # 완화 → 리스크: 닿지 못하는 길
    d.line(GX + GW + 4, cy, RX - 4, cy, SOFT, 1.2, "5 5")

d.t((GX + GW + RX) / 2, RY0 + RSTRIDE - 8, "닿지 못함", 12, MUTED, KR, "middle")
d.t(GX + GW / 2, 424, "세 길 모두 여기서 끊김", 12, MUTED, KR, "middle")
d.legend(464, [("리스크", WARN), ("위협", BAD), ("완화", ACC)])
d.save(str(ASSETS / "01-01.risk-threat-mitigation.svg"))
print("ok 01-01 risk-threat-mitigation")
