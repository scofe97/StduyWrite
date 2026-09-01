# 03-05 §2 — 호스트가 런타임에 리모트를 가져와 뷰를 조합한다 (원문 Figure 3-19).
# 타입 스펙: type-architecture — 신뢰 경계(브라우저 / 정적 호스팅)로 묶은 구성요소와 그 사이 연결.
#           accent 는 조합이 일어나는 단일 지점 하나와 그리로 들어오는 첫 연결뿐.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 1000
Z_Y, Z_H = 110, 254
Z1_X, Z1_W = 40, 420
Z2_X, Z2_W = 560, 400
LEGEND_Y = Z_Y + Z_H + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-05 §2",
      "호스트가 리모트를 런타임에 가져온다",
      "왼쪽은 브라우저에서 도는 호스트이고 오른쪽은 별도로 배포된 정적 산출물이다. 조각은 빌드 시점이 아니라 런타임에 합쳐진다.",
      "화살표는 호스트가 리모트를 지연 로드하는 방향입니다")

# 존을 먼저 그린다
for x, w, label in ((Z1_X, Z1_W, "BROWSER"), (Z2_X, Z2_W, "STATIC HOSTING · CDN / APP SERVER")):
    d.o.append(f'<rect x="{x}" y="{Z_Y}" width="{w}" height="{Z_H}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    tw = len(label) * 5.6 + 14
    d.o.append(f'<rect x="{x + 14}" y="{Z_Y - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(x + 20, Z_Y + 4, label, 8, SOFT, MONO, "start")

# 브라우저 쪽
HX, HY, HW, HH = 80, 160, 340, 64
d.tone(HX, HY, HW, HH, ACC, 6, "14", 1.4)
d.t(HX + 18, HY + 27, "호스트", 13, ACC, KR, "start", 600)
d.t(HX + 18, HY + 46, "조각을 담는 컨테이너 · 조합이 여기서 일어난다", 9.5, ACC, KR, "start")

VX, VY, VW, VH = 80, 276, 340, 64
d.box(VX, VY, VW, VH, PAPER2, RULE, 1.0, 6)
d.t(VX + 18, VY + 27, "조합된 뷰", 12.5, INK, KR, "start", 600)
d.t(VX + 18, VY + 46, "사용자가 보는 하나의 화면", 9.5, MUTED, KR, "start")
d.arrow([(250, HY + HH), (250, VY)], MUTED, "ar", 1.4)

# 정적 호스팅 쪽
remotes = [
    ("리모트 A", "노출 객체 · 조각", 150),
    ("리모트 B", "노출 객체 · 조각", 214),
    ("공유 라이브러리", "디자인 시스템 등", 278),
]
for name, sub, y in remotes:
    d.box(600, y, 320, 52, PAPER2, RULE, 1.0, 6)
    d.t(618, y + 22, name, 12, INK, KR, "start", 600)
    d.t(618, y + 39, sub, 9, MUTED, MONO, "start")

# 연결 — 호스트 오른쪽 변 부착점을 16px 씩 벌린다
d.arrow([(HX + HW, 176), (600, 176)], ACC, "acc", 1.5)
d.t(510, 166, "lazy import", 9, ACC, MONO)
d.arrow([(HX + HW, 192), (510, 192), (510, 240), (600, 240)], MUTED, "ar", 1.4)
d.arrow([(HX + HW, 208), (486, 208), (486, 304), (600, 304)], MUTED, "ar", 1.4)

d.legend(LEGEND_Y, [("조합이 일어나는 단일 지점", ACC), ("런타임 로드", MUTED)])
d.save("03-05.host-remote.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
