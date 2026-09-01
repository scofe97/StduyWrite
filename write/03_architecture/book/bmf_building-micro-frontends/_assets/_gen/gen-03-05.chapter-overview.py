# 03-05 전체 지도 — Module Federation 을 이루는 세 부분과 각 부분에 붙는 결정.
# 저자는 host 와 remote 둘만 "두 부분"이라 세고 공유 라이브러리는 기능으로 적는다. 셋으로 묶은 것은 노트의 읽기다.
# 타입 스펙: type-tree — 뿌리 하나에서 갈라지는 단일 부모 계층. 되돌아오는 간선이 없어 dependency 가 아니다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
ROOT_W, NW, NH = 260, 220, 52
ROOT_Y, T1_Y, T2_Y = 104, 208, 312
CENTERS = (170, 500, 830)

tier1 = [("호스트", "host"), ("리모트", "remote"), ("공유 라이브러리", "shared")]
tier2 = [("조각을 담는 컨테이너", "조합이 일어나는 자리"),
         ("노출한 객체를 지연 로드", "CDN 또는 앱 서버에서"),
         ("버전이 같으면 한 번만", "다르면 스코프를 나눔")]

LEGEND_Y = T2_Y + NH + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-05",
      "Module Federation 을 이루는 것",
      "뿌리가 플러그인이고 아래로 갈수록 구체적인 결정이다. 색이 붙은 뿌리 하나가 나머지를 규정한다.",
      "위에서 아래로 읽습니다")

# 연결선을 먼저 그린다
BUS_Y = ROOT_Y + NH + 26
d.line(500, ROOT_Y + NH, 500, BUS_Y, MUTED, 1.0)
d.line(CENTERS[0], BUS_Y, CENTERS[2], BUS_Y, MUTED, 1.0)
for cx in CENTERS:
    d.line(cx, BUS_Y, cx, T1_Y, MUTED, 1.0)
    d.line(cx, T1_Y + NH, cx, T2_Y, MUTED, 1.0)

d.o.append(f'<rect x="{500 - ROOT_W/2}" y="{ROOT_Y}" width="{ROOT_W}" height="{NH}" rx="6" '
           f'fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(500, ROOT_Y + 22, "Module Federation", 13.5, ACC, KR, "middle", 600)
d.t(500, ROOT_Y + 39, "2.0 부터 번들러 중립", 9, ACC, MONO)

for cx, (name, en) in zip(CENTERS, tier1):
    d.box(cx - NW / 2, T1_Y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(cx, T1_Y + 22, name, 13, INK, KR, "middle", 600)
    d.t(cx, T1_Y + 39, en, 9, MUTED, MONO)

for cx, (name, sub) in zip(CENTERS, tier2):
    d.box(cx - NW / 2, T2_Y, NW, NH, f"{INK}08", MUTED, 0.8, 6)
    d.t(cx, T2_Y + 22, name, 11.5, INK, KR, "middle", 600)
    d.t(cx, T2_Y + 39, sub, 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("이 편의 뿌리", ACC)])
d.save("03-05.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
