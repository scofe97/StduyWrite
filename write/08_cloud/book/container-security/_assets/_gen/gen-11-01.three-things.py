# 타입 스펙: type-architecture — 구성 요소 하나가 갖춰야 할 세 가지(개인키·자기 인증서·CA 인증서)가 경계 밖으로 나가는지 들어오는지로 갈린다: 개인키는 못 나가고, 인증서는 나가고, 상대의 인증서는 들어와 CA 인증서로 검증된다. focal 은 세 가지를 한꺼번에 가진 구성 요소 영역.
# 사실 출처: 노트 L204~L208(세 가지와 취급: 개인키 시크릿·인증서 자유 배포·CA 인증서로 검증), L220(키스토어=개인키+자기 인증서, 트러스트스토어=CA), L224~L229(keystore.p12·truststore.p12), L235(나를 증명 · 남을 검증)
# Layout conventions: 영역 둘(구성 요소 x=48, 통신 상대 x=648), 행 stride 88(y=148·236·324, 상자 높이 68). 오른쪽은 인증서·CA 행이 맞교환돼 두 가로 화살표가 행을 벗어나지 않는다. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


W, H = 960, 500
d = D(W, H, "ARCHITECTURE · 11-01 §6",
      "구성 요소마다 개인키 · 인증서 · CA 인증서 셋이 필요합니다",
      "개인키는 구성 요소 밖으로 나가지 않는 시크릿이고, 자기 인증서는 상대에게 건네며, 신뢰하는 CA 인증서는 상대에게서 받은 인증서를 검증하는 데 쓴다. Spring 에서는 앞의 둘이 keystore.p12, 마지막이 truststore.p12 에 든다.",
      lead="나가는 것 · 못 나가는 것 · 들어와서 검증되는 것으로 역할이 갈립니다")

ROWS = [148, 236, 324]
IH = 68
LZX, LZW = 48, 432          # 구성 요소 영역
RZX, RZW = 648, 264         # 통신 상대 영역
LIX, LIW = 200, 264         # 왼쪽 상자
RIX, RIW = 664, 232         # 오른쪽 상자


def item(x, w, y, c, title, sub):
    fit(title, 14, w - 24); fit(sub, 12, w - 24)
    d.tone(x, y, w, IH, c, 6, "14", 1.2)
    d.t(x + w / 2, y + 28, title, 14, c, KR, "middle", 600)
    d.t(x + w / 2, y + 52, sub, 12, MUTED, kr(sub), "middle")


# 영역 (뒤에 깐다) — 왼쪽은 focal
d.tone(LZX, 100, LZW, 316, ACC, 8, "0C", 1.4)
d.t(LZX + 16, 124, "구성 요소", 13, ACC, KR, "start", 600)
d.box(RZX, 100, RZW, 316, "rgba(245,245,245,0.02)", RULE, 1.0, 8)
d.t(RZX + 16, 124, "통신 상대", 13, MUTED, KR, "start", 600)

# 화살표 (상자보다 먼저)
# 행 1: 개인키는 경계를 못 넘는다 — 양쪽 모두 짧은 선에서 막힌다
d.line(LZX + LZW, ROWS[0] + IH / 2, 508, ROWS[0] + IH / 2, BAD, 1.6)
d.t(516, ROWS[0] + IH / 2 + 5, "✗", 14, BAD, KR, "middle", 600)
d.line(RZX, ROWS[0] + IH / 2, 620, ROWS[0] + IH / 2, BAD, 1.6)
d.t(612, ROWS[0] + IH / 2 + 5, "✗", 14, BAD, KR, "middle", 600)
# 행 2: 내 인증서가 상대로 건너간다
y2 = ROWS[1] + IH / 2
d.arrow([(LIX + LIW + 2, y2), (RIX - 2, y2)], OK, "ok", 1.6)
d.t((LIX + LIW + RIX) / 2, y2 - 12, "배포", 12, OK, KR, "middle", 600)
# 행 3: 상대의 인증서가 들어와 내 CA 인증서로 간다
y3 = ROWS[2] + IH / 2
d.arrow([(RIX - 2, y3), (LIX + LIW + 2, y3)], INFO, "info", 1.6)
d.t((LIX + LIW + RIX) / 2, y3 - 12, "검증", 12, INFO, KR, "middle", 600)
d.chip(564, ROWS[0] + IH / 2 - 24, "공유 금지", BAD, 12, 7)

# 왼쪽 상자 + 스토어 표지
item(LIX, LIW, ROWS[0], BAD, "개인키", "시크릿 · 밖으로 안 나감")
item(LIX, LIW, ROWS[1], OK, "자기 인증서", "자유롭게 배포")
item(LIX, LIW, ROWS[2], INFO, "신뢰하는 CA 인증서", "하나 이상 · 받은 인증서 검증")

BX, BWD = 64, 120
for y0, y1, name, sub in [(ROWS[0], ROWS[1] + IH, "keystore.p12", "나를 증명"), (ROWS[2], ROWS[2] + IH, "truststore.p12", "남을 검증")]:
    fit(name, 12, BWD - 8)
    d.box(BX, y0, BWD, y1 - y0, PAPER2, RULE, 1.0)
    cy = (y0 + y1) / 2
    d.t(BX + BWD / 2, cy - 2, name, 12, INK, MONO, "middle", 600)
    d.t(BX + BWD / 2, cy + 18, sub, 12, MUTED, KR, "middle")

# 오른쪽 상자: 같은 셋을 가진 다른 구성 요소 (인증서·CA 행이 맞교환)
item(RIX, RIW, ROWS[0], BAD, "개인키", "시크릿 · 밖으로 안 나감")
item(RIX, RIW, ROWS[1], INFO, "신뢰하는 CA 인증서", "받은 인증서 검증")
item(RIX, RIW, ROWS[2], OK, "자기 인증서", "자유롭게 배포")

d.legend(440, [("개인키 · 비공개", BAD), ("인증서 · 배포", OK), ("CA 인증서 · 검증 기준", INFO), ("세 가지를 갖춘 구성 요소", ACC)])
d.save(str(ASSETS / "11-01.three-things.svg"))
print("ok 11-01 three-things")
