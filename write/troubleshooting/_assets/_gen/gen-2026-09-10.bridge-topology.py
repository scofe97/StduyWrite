# 2026-09-10 A 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "이 호스트가 어느 링크에 붙어 있고 누가 같은 링크에 있나"이지 인과가 아니다.
# 드롭의 성격 구분은 원인 분석 절의 drop-kinds 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 경계 상자로 호스트 범위를 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, WARN, PAPER2, RULE, KR, MONO

W, H = 812, 424
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-10 A",
      "브리지가 붙어 있는 링크",
      "컨테이너 몇 개가 br0 브리지에 물려 있고, 그 브리지는 사무실 링크에 붙어 있다. "
      "같은 링크에는 우리 장비만 있는 것이 아니다.",
      lead="브리지는 같은 링크의 브로드캐스트를 전부 받습니다")

HX, HY, HW, HH = 40, 112, 420, 252
d.box(HX, HY, HW, HH, PAPER2, RULE, 1.0, 8)
d.t(HX + 14, HY + 22, "리눅스 호스트 한 대", 12, SOFT, KR, "start", 600)

for i, name in enumerate(["컨테이너 A", "컨테이너 B", "컨테이너 C"]):
    x = HX + 24 + i * 126
    d.box(x, HY + 44, 112, 54, PAPER2, RULE, 0.9, 6)
    d.t(x + 56, HY + 68, name, 12, INK, KR, "middle", 600)
    d.t(x + 56, HY + 86, "veth", 11, SOFT, MONO)
    d.arrow([(x + 56, HY + 98), (x + 56, HY + 132)], MUTED, "ar", 1.2)

d.tone(HX + 24, HY + 136, 364, 56, ACC, 6)
d.t(HX + 40, HY + 160, "br0 브리지", 13, ACC, KR, "start", 600)
d.t(HX + 40, HY + 180, "Receive drop 이 초당 1건씩 증가", 12, WARN, KR, "start")

d.t(HX + 24, HY + 222, "앱은 멀쩡합니다. 요청은 다 성공하고 지연도 평소와 같습니다.",
    12, SOFT, KR, "start")

d.arrow([(HX + HW, HY + 164), (HX + HW + 64, HY + 164)], MUTED, "ar", 1.4)
d.t(HX + HW + 32, HY + 150, "링크", 12, MUTED, KR, "middle")

LX = HX + HW + 68
d.box(LX, HY + 44, 264, 148, PAPER2, RULE, 1.0, 8)
d.t(LX + 14, HY + 66, "같은 이더넷 링크", 12, SOFT, KR, "start", 600)
d.box(LX + 20, HY + 84, 224, 44, PAPER2, RULE, 0.9, 6)
d.t(LX + 132, HY + 104, "우리 장비들", 12, INK, KR, "middle", 600)
d.t(LX + 132, HY + 120, "정상 트래픽", 11, SOFT, MONO)
d.box(LX + 20, HY + 136, 224, 44, PAPER2, RULE, 0.9, 6)
d.t(LX + 132, HY + 156, "그 밖의 장비", 12, INK, KR, "middle", 600)
d.t(LX + 132, HY + 172, "무엇이 있는지 아직 모릅니다", 11, WARN, KR)

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-10.bridge-topology.svg"))
print("ok")
