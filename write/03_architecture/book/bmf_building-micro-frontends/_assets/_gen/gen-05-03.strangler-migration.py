# 05-03 §2 — F1.com 이 모놀리스에서 조각으로 옮겨 간 경로. 저자가 적은 단계와 방아쇠만 옮긴다.
# 한 번에 다시 쓰지 않고 도메인을 하나씩 빼내는 스트랭글러 무화과 패턴이다.
# 타입 스펙: type-state — 유한한 상태와 그 사이 전이. accent 는 독자가 알아채야 할 상태 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1380
SW, SH, SY = 300, 76, 180
XS = (70, 540, 1010)
MY = SY + SH / 2
BACK_Y = SY + SH + 84
LEGEND_Y = BACK_Y + 52
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-03 §2",
      "F1.com 은 한 번에 다시 쓰지 않았다",
      "도메인 경계를 먼저 찾고 1 단계 URL 라우팅을 엣지에 걸어, 옮긴 페이지부터 새 애플리케이션이 받게 했다. 색이 붙은 가운데 상태가 마이그레이션 내내 유지된 자리다.",
      "화살표 위 글이 그 전이를 일으키는 방아쇠입니다")

d.o.append(f'<circle cx="16" cy="{MY}" r="6" fill="{INK}"/>')
d.arrow([(24, MY), (XS[0] - 2, MY)], MUTED, "ar", 1.4)

d.arrow([(XS[0] + SW, MY), (XS[1] - 2, MY)], MUTED, "ar", 1.4)
d.t((XS[0] + SW + XS[1]) / 2, MY - 26, "도메인 경계를 찾는다", 9.5, MUTED, KR)
d.t((XS[0] + SW + XS[1]) / 2, MY - 10, "엣지에 1 단계 라우팅", 9.5, MUTED, KR)
d.arrow([(XS[1] + SW, MY), (XS[2] - 2, MY)], MUTED, "ar", 1.4)
d.t((XS[1] + SW + XS[2]) / 2, MY - 18, "남은 페이지도 옮긴다", 9.5, MUTED, KR)
d.path(f"M {XS[1] + SW / 2} {SY + SH} V {BACK_Y} H {XS[1] + SW / 2 - 120} V {SY + SH + 2}",
       ACC, 1.5, m="acc")
d.t(XS[1] + SW / 2 - 60, BACK_Y + 20, "도메인을 하나씩 빼낸다 · 나머지는 모놀리스가 계속 받는다", 10.5, ACC, KR)

states = [
    ("AEM 모놀리스", "한 서버가 모든 HTML 을 만든다", False),
    ("모놀리스와 조각의 공존", "옮긴 경로만 새 애플리케이션이 받는다", True),
    ("조각 아키텍처", "공유 컴포넌트와 전용 컴포넌트가 섞인다", False),
]
for x, (name, sub, focal) in zip(XS, states):
    if focal:
        d.tone(x, SY, SW, SH, ACC, 8, "14", 1.4)
        d.t(x + SW / 2, SY + 32, name, 14, ACC, KR, "middle", 600)
        d.t(x + SW / 2, SY + 54, sub, 9.5, ACC, KR)
    else:
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 8)
        d.t(x + SW / 2, SY + 32, name, 14, INK, KR, "middle", 600)
        d.t(x + SW / 2, SY + 54, sub, 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("마이그레이션 내내 유지된 상태", ACC)])
d.save("05-03.strangler-migration.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", XS[2] + SW)
