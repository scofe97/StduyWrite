# 03-08 §2 — 응답을 빠르게 만들려고 캐시를 놓을 수 있는 자리. 저자가 든 것만 층으로 세운다.
# 저자는 이 넷을 층으로 세지 않는다. 층으로 묶은 것은 노트의 읽기이며 각 층의 문구는 원문 서술을 옮긴 것이다.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 층 넷은 스펙의 4~6 범위 안이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1100
LX, LW, LH = 80, 940, 68
TOP = 120
layers = [   # 위(사용자에 가까움)에서 아래(오리진)로
    ("04", "CDN", "클라이언트와 콘텐츠 사이 지연을 줄인다", False),
    ("03", "조각 DOM 인메모리 캐시", "매번 조합하지 않고 통째로 꺼내 쓴다", True),
    ("02", "마이크로서비스 응답 캐시", "Redis 로 짧게 저장해 조합 처리량을 올린다", False),
    ("01", "매번 조합하는 오리진", "캐시가 없으면 요청마다 여기까지 내려간다", False),
]
LEGEND_Y = TOP + len(layers) * LH + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-08 §2",
      "캐시를 놓을 수 있는 네 자리",
      "위로 갈수록 사용자에 가깝고 오리진이 지는 부담이 준다. 색이 붙은 층이 저자가 조합 자체를 건너뛰는 수단으로 든 자리다.",
      "왼쪽 화살표 방향으로 갈수록 사용자에 가깝습니다")

for i, (idx, name, note, focal) in enumerate(layers):
    y = TOP + i * LH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        fill = PAPER2 if i % 2 == 0 else f"{INK}08"
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" fill="{fill}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(LX + 20, y + LH / 2 + 4, idx, 9, ACC if focal else SOFT, MONO, "start")
    d.t(LX + 72, y + LH / 2 + 5, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 20, y + LH / 2 + 4, note, 10.5, MUTED, KR, "end")

d.arrow([(56, TOP + len(layers) * LH - 12), (56, TOP + 12)], SOFT, "soft", 1.1)
mid = TOP + len(layers) * LH / 2
d.o.append(f'<text x="40" y="{mid}" transform="rotate(-90 40 {mid})" text-anchor="middle" '
           f'font-family="{MONO}" font-size="9" fill="{SOFT}" letter-spacing="0.14em">TOWARD USER</text>')

d.legend(LEGEND_Y, [("조합 자체를 건너뛰는 자리", ACC)])
d.save("03-08.cache-layers.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
