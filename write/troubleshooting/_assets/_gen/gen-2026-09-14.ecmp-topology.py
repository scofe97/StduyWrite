# 2026-09-14 A(몇몇 사용자) 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "사용자 패킷이 무엇을 지나 서버 셋 중 하나에 닿나"와 "지난주 바뀐 자리가 어디인가"다.
# 알림이 엉뚱한 서버로 가는 인과는 원인 분석 절의 ptb-misdelivery 가 맡는다.
# 그래서 이 장에는 화살표도 번호도 없다. 선은 연결만 보이고 방향은 사건 도식에서 붙인다.
# 타입 스펙: type-architecture — 구성요소와 연결. 데이터센터 경계 상자로 ECMP 가 갈라 주는 범위를 보인다.
#           deployment 를 검토했으나 버전·아티팩트가 논지가 아니고 서버 셋을 따로 그려야 해 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 432
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-14 A",
      "주소 하나를 서버 셋이 나눠 받습니다",
      "IPv6 를 IPv4 터널로 실어 오는 사용자가 인터넷과 경로 중간 라우터를 지나 데이터센터에 닿는다. "
      "서버 셋은 같은 서비스 주소를 내부 BGP 로 광고하고, 경로 비용이 같아진 뒤로 데이터센터 라우터가 "
      "TCP 흐름마다 네 값을 해시해 서버 하나를 고른다.",
      lead="지난주 경로 비용을 같게 맞춘 뒤로 데이터센터 라우터가 흐름마다 서버를 고릅니다")

CY = 232                 # 주 경로의 세로 중심
BH = 72                  # 경로 위 상자 높이
BY = CY - BH // 2        # 196

# 데이터센터 경계 — 먼저 그려 상자와 선이 위에 앉게 한다
ZX, ZY, ZW, ZH = 528, 104, 376, 252
d.o.append(f'<rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="rgba(245,245,245,0.02)" '
           f'stroke="rgba(245,245,245,0.20)" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(ZX + 16, ZY + 22, "데이터센터", 12, SOFT, KR, "start", 600)

# 연결선 — 방향 없음
for x1, x2 in ((144, 184), (304, 344), (504, 544), (704, 736)):
    d.line(x1, CY, x2, CY, MUTED, 1.2)
SX, SW, SH = 768, 120, 56
S_CY = [152, 232, 312]
d.line(736, S_CY[0], 736, S_CY[-1], MUTED, 1.2)
for cy in S_CY:
    d.line(736, cy, SX, cy, MUTED, 1.2)

def node(x, w, title, sub, sub_c=SOFT, sub_f=KR, size=14):
    d.box(x, BY, w, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + w // 2, BY + 30, title, size, INK, KR, "middle", 600)
    d.t(x + w // 2, BY + 52, sub, 12, sub_c, sub_f, "middle")

node(24, 120, "사용자", "터널 뒤")
node(184, 120, "인터넷", "IPv4", sub_f=MONO)
node(344, 160, "경로 중간 라우터", "다음 링크 MTU 작음", sub_c=WARN, size=13)

# 지난주 바뀐 자리 — focal 한 곳
d.tone(544, BY, 160, BH, ACC, 6)
d.t(624, BY + 30, "데이터센터 라우터", 13, INK, KR, "middle", 600)
d.t(624, BY + 52, "ECMP", 12, ACC, MONO, "middle", 600)
d.t(624, 296, "경로 비용 셋 다 같음", 12, SOFT, KR, "middle")
d.t(624, 316, "TCP · 네 값 해시", 12, MUTED, KR, "middle")

for i, cy in enumerate(S_CY):
    y = cy - SH // 2
    d.box(SX, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(SX + SW // 2, y + 24, f"서버 {i + 1}", 13, INK, KR, "middle", 600)
    d.t(SX + SW // 2, y + 44, "같은 서비스 주소", 12, SOFT, KR, "middle")

# 좁은 구간 — 터널이 경로 중간 라우터에서 사용자까지 이어진다
TY = 300
d.line(84, TY, 424, TY, WARN, 1.6)
d.line(84, TY - 8, 84, TY + 8, WARN, 1.6)
d.line(424, TY - 8, 424, TY + 8, WARN, 1.6)
d.t(254, TY + 24, "IPv6 over IPv4 터널 · MTU 작음", 12, WARN, KR, "middle")

d.legend(376, [("지난주 바꾼 자리", ACC), ("MTU 작은 구간", WARN)])

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-14.ecmp-topology.svg"))
print("ok")
