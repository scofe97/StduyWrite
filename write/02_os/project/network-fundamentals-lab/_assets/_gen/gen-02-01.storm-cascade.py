# 02-01 §2 — 브로드캐스트 한 발이 통신 전체를 죽이는 경로.
# 타입 스펙: type-flowchart — 한 사건에서 출발해 증폭 고리를 거쳐 두 갈래 결과로
#           갈라진다. 직선 단계가 아니라 분기가 있어 process 가 아닌 flowchart.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, WARN, KR, MONO

W, H = 880, 400
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 02-01 §2",
      "브로드캐스트 한 발이 통신 전체를 죽이는 경로",
      "루프가 있으면 브로드캐스트가 복제되어 돌아오고, 이더넷에 TTL 이 없어 끊기지 않는다. 증폭은 두 갈래 피해로 갈라진다.",
      "증폭만으로 끝나지 않고 FDB 가 오염되어 유니캐스트까지 길을 잃는다")

d.box(24, 104, 240, 64, PAPER2, RULE, 1.0, 8)
d.t(44, 130, "브로드캐스트 1발", 14, INK, KR, "start", 600)
d.t(44, 152, "ARP who-has", 12, MUTED, MONO, "start")

d.tone(316, 104, 240, 64, WARN, 8, "12", 1.3)
d.t(336, 130, "두 링크로 복제", 14, WARN, KR, "start", 600)
d.t(336, 152, "서로에게 돌아온다", 12, MUTED, KR, "start")

d.tone(608, 104, 248, 64, BAD, 8, "12", 1.3)
d.t(628, 130, "끊을 방법이 없다", 14, BAD, KR, "start", 600)
d.t(628, 152, "이더넷에 TTL 이 없다", 12, MUTED, KR, "start")

d.arrow([(264, 136), (312, 136)], MUTED, "ar", 1.4)
d.arrow([(556, 136), (604, 136)], MUTED, "ar", 1.4)

# 증폭 고리 — 박스 위로 되돌아온다 (아래 분기와 겹치지 않게)
d.path("M 732 104 V 90 H 436 V 100", BAD, 1.4, m="bad", dash="4 5")
d.chip(584, 90, "무한 증폭", BAD)

# 두 갈래 결과
d.box(24, 236, 400, 92, PAPER2, RULE, 1.0, 8)
d.t(44, 264, "겉으로 보이는 것", 13, SOFT, KR, "start", 600)
d.t(44, 290, "트래픽과 CPU 폭증", 14, INK, KR, "start", 600)
d.t(44, 312, "저장소 기록 기준 2초에 약 1만 패킷", 12, MUTED, KR, "start")

d.tone(456, 236, 400, 92, BAD, 8, "12", 1.3)
d.t(476, 264, "실제로 통신을 죽이는 것", 13, BAD, KR, "start", 600)
d.t(476, 290, "FDB 오염", 14, BAD, KR, "start", 600)
d.t(476, 312, "소스 MAC 이 엉뚱한 포트에서 재학습", 12, MUTED, KR, "start")

# 아래 분기 — 오른쪽 박스 밑에서 내려와 좌우 두 결과로 갈린다
d.path("M 732 168 V 202 H 224 V 232", MUTED, 1.4, m="ar")
d.path("M 656 202 V 232", BAD, 1.4, m="bad")

d.t(24, 368, "그래서 증상이 '느려진다' 가 아니라 '다 죽는다' 다 — 유니캐스트까지 길을 잃는다", 12, ACC, KR, "start", 600)
d.save("02-01.storm-cascade.svg")
