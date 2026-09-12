# 2026-09-08 E 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "이 장비에 무엇이 같이 돌고 있나"이지 STW 안의 시간 배분이 아니다.
# 멈춤을 구간으로 가르는 일은 원인 분석 절의 stw-anatomy 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 장비 경계로 공유 자원을 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, WARN, PAPER2, RULE, KR, MONO

W, H = 804, 412
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-08 E",
      "한 장비를 나눠 쓰는 둘",
      "지연에 민감한 자바 서비스와 대량 쓰기를 하는 배치 작업이 같은 장비에 있다. "
      "멈춤은 배치가 디스크에 쓰고 있을 때 몰린다.",
      lead="둘이 공유하는 것이 무엇인지가 이 문항의 자리입니다")

MX, MY, MW, MH = 40, 120, 724, 176
d.box(MX, MY, MW, MH, PAPER2, RULE, 1.0, 8)
d.t(MX + 14, MY + 22, "장비 한 대", 12, SOFT, KR, "start", 600)

d.tone(MX + 26, MY + 42, 316, 112, ACC, 6)
d.t(MX + 184, MY + 70, "자바 서비스", 14, ACC, KR, "middle", 600)
d.t(MX + 184, MY + 94, "힙 8GB · G1 컬렉터", 12, SOFT, MONO, "middle")
d.t(MX + 184, MY + 118, "STW 가 4.17 초로 찍힘", 12, WARN, KR, "middle")
d.t(MX + 184, MY + 140, "수집량은 적음", 12, MUTED, KR, "middle")

d.box(MX + 382, MY + 42, 316, 112, PAPER2, RULE, 0.9, 6)
d.t(MX + 540, MY + 70, "배치 작업", 14, INK, KR, "middle", 600)
d.t(MX + 540, MY + 94, "디스크에 150MB/s 쓰기", 12, SOFT, MONO, "middle")
d.t(MX + 540, MY + 118, "이때만 멈춤이 몰림", 12, WARN, KR, "middle")

d.t(MX + 362, MY + 100, "?", 16, MUTED, MONO, "middle", 600)

d.t(W // 2, 336, "힙을 키우고 GC 파라미터를 바꿔도 달라지지 않았습니다", 13, MUTED, KR, "middle")
d.t(W // 2, 362, "메모리 지표는 조용하고 Full GC 가 몰아치는 패턴도 아닙니다", 12, SOFT, KR, "middle")
d.t(W // 2, 388, "그 4 초 동안 JVM 이 무엇을 하고 있었는지가 출력에 없습니다", 12, WARN, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-08.gc-io-topology.svg"))
print("ok")
