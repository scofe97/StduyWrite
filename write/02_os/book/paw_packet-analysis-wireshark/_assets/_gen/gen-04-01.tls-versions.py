# 04-01 §1 — 원문의 SSL/TLS 버전 표를 연대 위에 놓는다. 연도는 원문 표의 값 그대로이고,
# 폐기 여부는 원문이 적은 것과 그 뒤 바뀐 것을 색으로 가른다.
# 타입 스펙: type-timeline — 사건이 시간 위에 놓인다. 간격은 실제 연도 차이에 비례해 놓고,
#           라벨은 위아래로 번갈아 두어 겹치지 않게 한다. focal 은 원문 이후 확정된 TLS 1.3.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 432
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §1",
      "SSL/TLS 버전의 연대",
      "원문 표의 연도와 RFC 를 시간축 위에 놓은 것. 원문 시점(2015)에 폐기된 것은 SSL 둘뿐이었고, 그 뒤 TLS 1.0·1.1 도 폐기됐으며 TLS 1.3 은 초안에서 RFC 8446 으로 확정됐다.",
      "왼쪽 네 개가 지금은 모두 폐기됐습니다 — 쓸 수 있는 것은 오른쪽 둘뿐입니다")

Y = 216
X0, X1 = 80, 900
YEARS = [1995, 2018]
def x(yr): return X0 + (X1 - X0) * (yr - YEARS[0]) / (YEARS[1] - YEARS[0])

d.line(X0 - 32, Y, X1 + 48, Y, RULE, 1.0)
for yr in (1995, 2000, 2005, 2010, 2015, 2018):
    d.line(x(yr), Y - 5, x(yr), Y + 5, RULE, 1.0)
    d.t(x(yr), Y + 22, str(yr), 10, SOFT, MONO)

EVENTS = [
    (1995, "SSL 2.0",  "RFC 없음",     "폐기 · RFC 6176", BAD,  True),
    (1996, "SSL 3.0",  "RFC 6101",     "폐기 · RFC 7568", BAD,  False),
    (1999, "TLS 1.0",  "RFC 2246",     "폐기 · RFC 8996", WARN, True),
    (2006, "TLS 1.1",  "RFC 4346",     "폐기 · RFC 8996", WARN, False),
    (2008, "TLS 1.2",  "RFC 5246",     "현행",            OK,   True),
    (2018, "TLS 1.3",  "RFC 8446",     "현행 · 원문은 DRAFT", ACC, False),
]

for yr, name, rfc, note, c, above in EVENTS:
    cx = x(yr)
    focal = (c == ACC)
    d.o.append(f'<circle cx="{cx}" cy="{Y}" r="{6 if focal else 4}" fill="{c}"/>')
    ly = Y - 112 if above else Y + 56
    d.line(cx, Y - 8 if above else Y + 8, cx, ly + (68 if above else -8), c, 1.0, "3 4")
    if focal:
        d.o.append(f'<rect x="{cx - 60}" y="{ly}" width="120" height="68" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(cx - 60, ly, 120, 68, PAPER2, RULE, 1.0, 6)
    d.t(cx, ly + 22, name, 13, c, MONO, "middle", 600)
    d.t(cx, ly + 40, rfc, 11, MUTED, MONO)
    d.t(cx, ly + 58, note, 11, c, KR)

d.legend(H - 64, [("원문 이후 확정", ACC), ("현행", OK), ("원문 이후 폐기", WARN), ("원문 시점에 이미 폐기", BAD)])
d.save("04-01.tls-versions.svg")
