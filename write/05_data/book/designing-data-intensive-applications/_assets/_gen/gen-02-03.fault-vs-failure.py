# 02-03 §1 — 같은 사건이 층위에 따라 결함이기도 장애이기도 하다. 본문의 드라이브 예시 하나만 포함 관계로 그린다.
# 옛 도식의 하드웨어·소프트웨어 결함 목록, 사람과 신뢰성, 무비난 포스트모템, 카오스 엔지니어링, Horizon 줄은 뺐다. §3~§6 본문이 맡는다.
# 타입 스펙: type-nested
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 140, 208
LEG = PY + PH + 40
H = LEG + 56

d = D(W, H, "02-03 · FAULT VS FAILURE", "같은 사건, 다른 층위",
      "드라이브 하나가 멈추는 사건은 드라이브가 하나뿐인 시스템에서는 장애이고, 사본이 있는 시스템에서는 결함일 뿐이다.",
      "드라이브가 멈출 때 시스템이 어떻게 되는가")

d.t(224, 120, "드라이브가 하나뿐인 시스템", 14, INK, KR, "middle", 600)
d.box(16, PY, 416, PH, PAPER, BAD, 1.2)
d.t(224, PY + 32, "시스템 전체가 멈춤", 13, BAD, KR, "middle", 600)
d.tone(112, PY + 56, 224, 88, BAD, 6, "14", 1.2)
d.t(224, PY + 92, "드라이브 1", 15, INK, KR, "middle", 600)
d.t(224, PY + 116, "멈춤 → 결함", 13, MUTED, KR)
d.t(224, PY + 184, "결함이 곧 장애", 13, MUTED, KR)

d.t(656, 120, "드라이브가 여러 개인 시스템", 14, INK, KR, "middle", 600)
d.box(448, PY, 416, PH, PAPER, ACC, 1.4)
d.t(656, PY + 32, "시스템은 계속 서비스", 13, OK, KR, "middle", 600)
d.tone(472, PY + 56, 176, 88, BAD, 6, "14", 1.2)
d.t(560, PY + 92, "드라이브 1", 15, INK, KR, "middle", 600)
d.t(560, PY + 116, "멈춤 → 결함", 13, MUTED, KR)
d.tone(664, PY + 56, 176, 88, OK, 6, "14", 1.2)
d.t(752, PY + 92, "드라이브 2", 15, INK, KR, "middle", 600)
d.t(752, PY + 116, "데이터 사본", 13, MUTED, KR)
d.t(656, PY + 184, "결함일 뿐, 사본으로 견딤", 13, MUTED, KR)

d.legend(LEG, [("멈춘 부분", BAD), ("정상 부분", OK), ("핵심 — 층위의 차이", ACC)])
d.save("02-03.fault-vs-failure.svg")
