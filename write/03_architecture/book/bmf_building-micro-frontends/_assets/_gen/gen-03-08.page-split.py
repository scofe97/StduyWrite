# 03-08 §4 — 페이지 또는 페이지 그룹 단위로 나누는 서버 사이드 구조 (원문 Figure 3-22).
# 각 페이지를 한 팀이 끝까지 소유하고, 푸터처럼 공통인 부분만 런타임에 얹는다.
# 타입 스펙: type-architecture — 논리 경계(페이지 그룹)로 묶은 구성요소와 그 사이 연결.
#           accent 는 모든 페이지가 공유하는 표준 템플릿 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1200
TX, TY, TW, TH = 300, 108, 600, 76
ZY, ZH = 232, 172
ZXS = (40, 420, 800)
ZW = 360
LEGEND_Y = ZY + ZH + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-08 §4",
      "페이지 그룹마다 한 팀이 끝까지 소유한다",
      "가운데 위가 모든 페이지가 함께 쓰는 템플릿이고 아래 세 칸이 각 팀의 소유 범위다. 캐시도 인프라도 칸마다 따로 정한다.",
      "화살표는 각 페이지 그룹이 같은 템플릿 안에 실린다는 뜻입니다")

d.tone(TX, TY, TW, TH, ACC, 8, "12", 1.4)
d.t(TX + TW / 2, TY + 32, "표준 템플릿", 15, ACC, KR, "middle", 600)
d.t(TX + TW / 2, TY + 56, "푸터처럼 공통인 부분은 런타임에 얹는다", 11, MUTED, KR)

groups = [
    ("랜딩 페이지 그룹", "team A", ["독립 개발 · 독립 배포", "정적에 가까워 길게 캐시"]),
    ("카탈로그 뷰", "team B", ["한 뷰에 조각이 여럿", "그룹 단위로 따로 캐시"]),
    ("체크아웃 그룹", "team C", ["하부 인프라를 따로 설정", "개인화가 많아 짧게 캐시"]),
]
for x, (name, en, lines) in zip(ZXS, groups):
    d.o.append(f'<rect x="{x}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    lab = f"OWNED BY {en.upper()}"
    tw = len(lab) * 5.6 + 14
    d.o.append(f'<rect x="{x + 14}" y="{ZY - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(x + 20, ZY + 4, lab, 8, SOFT, MONO, "start")
    d.box(x + 24, ZY + 26, ZW - 48, ZH - 52, PAPER2, RULE, 1.0, 6)
    d.t(x + 44, ZY + 54, name, 13.5, INK, KR, "start", 600)
    for i, ln in enumerate(lines):
        d.t(x + 44, ZY + 82 + i * 22, "· " + ln, 10.5, MUTED, KR, "start")

for x, ax in zip(ZXS, (TX + 60, TX + TW / 2, TX + TW - 60)):
    cx = x + ZW / 2
    my = (TY + TH + ZY) / 2
    if abs(cx - ax) < 2:
        d.arrow([(ax, TY + TH), (cx, ZY)], MUTED, "ar", 1.4)
    else:
        d.arrow([(ax, TY + TH), (ax, my), (cx, my), (cx, ZY)], MUTED, "ar", 1.4)

d.legend(LEGEND_Y, [("모든 페이지가 함께 쓰는 것", ACC), ("팀이 끝까지 소유하는 범위", MUTED)])
d.save("03-08.page-split.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
