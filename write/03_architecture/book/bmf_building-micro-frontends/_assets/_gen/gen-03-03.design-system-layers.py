# 03-03 §3 — 디자인 시스템의 네 겹 (원문 Figure 3-7). 아래가 저수준 값, 위로 갈수록 구체.
# 저자가 "중앙화하기에 완벽한 단계"라고 못 박은 층 하나에만 accent 를 준다.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 층 넷은 스펙의 4~6 범위 안이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 472
LX, LW, LH = 80, 860, 68
d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-03 §3",
      "디자인 시스템의 네 겹",
      "아래가 저수준 값이고 위로 갈수록 구체적이다. 색이 붙은 층이 저자가 중앙화하기에 완벽한 단계라고 적은 자리다.",
      "왼쪽 화살표 방향으로 갈수록 구체적입니다")

layers = [  # 위에서 아래로
    ("04", "마이크로 프론트엔드", "UI 라이브러리를 호스팅 · 독립성 유지", False),
    ("03", "UI 컴포넌트 라이브러리", "도메인 로직 일부 포함 · 공유는 신중히", False),
    ("02", "기본 컴포넌트", "레이블 · 버튼 · 로직 없음", True),
    ("01", "디자인 토큰", "JSON · YAML · 보통 배포하지 않음", False),
]
for i, (idx, name, note, focal) in enumerate(layers):
    y = 120 + i * LH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        fill = PAPER2 if i % 2 == 0 else f"{INK}08"
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" fill="{fill}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(LX + 20, y + LH / 2 + 4, idx, 9, ACC if focal else SOFT, MONO, "start")
    d.t(LX + 72, y + LH / 2 + 5, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 20, y + LH / 2 + 4, note, 10, MUTED, MONO, "end")

# 방향 지시자 — 스택 바깥 왼쪽 여백
d.arrow([(48, 380), (48, 128)], SOFT, "soft", 1.1)
d.o.append(f'<text x="34" y="256" transform="rotate(-90 34 256)" text-anchor="middle" '
           f'font-family="{MONO}" font-size="9" fill="{SOFT}" letter-spacing="0.14em">SPECIFICITY</text>')

d.legend(432, [("중앙화하기에 완벽한 단계", ACC)])
d.save("03-03.design-system-layers.svg")
print("h 필요:", 432 + 40, " 실제:", H)
