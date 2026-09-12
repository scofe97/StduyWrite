# 2026-09-12 B(1초) 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "Pod 이 바깥으로 나갈 때 무엇을 거치나"이지 경쟁이 아니다.
# 두 단계 사이의 틈에서 나는 인과는 원인 분석 절의 snat-race 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 노드 경계로 SNAT 위치를 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 812, 392
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-12 B",
      "Pod 이 바깥으로 나가는 길",
      "여러 Pod 이 각자 다른 주소로 바깥 API 를 호출한다. 노드를 빠져나갈 때 "
      "그 주소들은 노드 IP 하나로 바뀌고, 구분을 위해 포트가 하나씩 배정된다.",
      lead="여럿이 하나가 되므로 구분할 무언가가 필요합니다")

NX, NY, NW, NH = 40, 116, 452, 200
d.box(NX, NY, NW, NH, PAPER2, RULE, 1.0, 8)
d.t(NX + 14, NY + 22, "노드 한 대", 12, SOFT, KR, "start", 600)

for i, ip in enumerate(["10.244.1.7", "10.244.1.8", "10.244.1.9"]):
    y = NY + 42 + i * 48
    d.box(NX + 22, y, 164, 40, PAPER2, RULE, 0.9, 5)
    d.t(NX + 104, y + 25, f"Pod · {ip}", 12, INK, MONO, "middle")
    d.arrow([(NX + 186, y + 20), (NX + 236, y + 20)], MUTED, "ar", 1.2)

d.tone(NX + 240, NY + 42, 190, 136, ACC, 6)
d.t(NX + 335, NY + 70, "SNAT", 14, ACC, KR, "middle", 600)
d.t(NX + 335, NY + 94, "주소를 노드 IP 하나로", 12, SOFT, KR, "middle")
d.t(NX + 335, NY + 118, "구분용 포트를 배정", 12, SOFT, KR, "middle")
d.t(NX + 335, NY + 146, "conntrack 에 기록", 12, MUTED, MONO, "middle")

d.arrow([(NX + NW, NY + 110), (NX + NW + 56, NY + 110)], MUTED, "ar", 1.4)
d.t(NX + NW + 28, NY + 94, "나감", 12, MUTED, KR, "middle")

d.box(NX + NW + 60, NY + 62, 200, 96, PAPER2, RULE, 0.9, 6)
d.t(NX + NW + 160, NY + 96, "바깥 API", 13, INK, KR, "middle", 600)
d.t(NX + NW + 160, NY + 118, "상태 페이지 정상", 12, SOFT, KR, "middle")
d.t(NX + NW + 160, NY + 138, "처리 자체는 빠름", 12, SOFT, KR, "middle")

d.t(W // 2, 356, "모든 노드가 같은 일을 하므로 이 구조는 클러스터 전역에 똑같이 있습니다",
    12, MUTED, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-12.snat-topology.svg"))
print("ok")
