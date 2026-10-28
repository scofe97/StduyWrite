# 02-05 §4 — 2장이 다룬 비기능 요구사항 넷과 유지보수성의 세 원칙, 공통 해법. 본문 종합 목록과 §1~§3 제목만 쓴다.
# 옛 도식의 원칙별 세부 항목 아홉 줄, 본질/우발 복잡도, 추상화 예시, 비가역성 줄은 뺐다. §1~§3 본문이 맡는다.
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 496
H = LEG + 56

d = D(W, H, "02-05 · SUMMARY", "2장의 비기능 요구사항 넷",
      "2장은 성능·확장성·신뢰성·유지보수성을 다뤘다. 유지보수성은 운영성·단순성·발전성으로 나뉘고, 공통 해법은 잘 이해된 빌딩 블록이다.",
      "2장 전체 지도")

d.box(340, 112, 200, 48, PAPER2, INFO, 1.2)
d.t(440, 142, "비기능 요구사항", 15, INK, KR, "middle", 600)

d.line(440, 160, 440, 188, MUTED, 1.4)
d.line(116, 188, 764, 188, MUTED, 1.4)
KIDS = [(16, "성능", "02-01 · 02-02"), (232, "확장성", "02-04"), (448, "신뢰성", "02-03"), (664, "유지보수성", "02-05")]
for x, a, b in KIDS:
    d.box(x, 216, 200, 64, PAPER2, INFO, 1.2)
    d.t(x + 100, 244, a, 15, INK, KR, "middle", 600)
    d.t(x + 100, 266, b, 12, MUTED, MONO)
    d.arrow([(x + 100, 188), (x + 100, 212)], MUTED, "ar", 1.4)

d.line(672, 280, 672, 426, MUTED, 1.4)
for y, lab in [(312, "운영성"), (360, "단순성"), (408, "발전성")]:
    d.box(688, y, 176, 36, PAPER, RULE, 1.0)
    d.t(776, y + 24, lab, 14, INK, KR)
    d.arrow([(672, y + 18), (684, y + 18)], MUTED, "ar", 1.4)

d.tone(16, 312, 600, 132, ACC, 6, "12", 1.4)
d.t(316, 364, "공통 해법", 14, MUTED, KR, "middle")
d.t(316, 394, "잘 이해된 빌딩 블록", 18, ACC, KR, "middle", 600)
d.t(316, 424, "트랜잭션 · 인덱스 · 로그", 13, MUTED, KR)

d.legend(LEG, [("핵심 — 공통 해법", ACC), ("비기능 요구사항", INFO)])
d.save("02-05.maintainability.svg")
