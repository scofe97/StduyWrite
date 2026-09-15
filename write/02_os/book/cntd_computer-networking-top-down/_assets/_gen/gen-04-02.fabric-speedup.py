# 04-02 §2 — 입력 큐잉이 "안 생기는" 쪽. 패브릭이 회선의 N 배면 한 슬롯 안에 N 개를 다 건넌다.
# §1 과 같은 골격·stride 를 쓴다(_cc_04_02_slots). 달라지는 것은 슬롯당 통과 개수뿐이고, 그 차이가 이 편의 논점이다.
# 타입 스펙: type-data-flow — semantic-patterns 의 "Fan-in queue / bottleneck". 같은 격자에서 병목이 풀린 쪽.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import OK, WARN, MUTED, SOFT, ACC
from _cc_04_02_slots import frame, slot, out_arrow, LEGEND_Y

d = frame("패브릭이 회선의 N 배면 그 슬롯 안에 다 건넙니다",
          "§1 과 같은 격자입니다. 달라진 것은 슬롯 하나에 세 번 건넌다는 것뿐입니다.",
          "입력 포트 세 곳에 슬롯마다 패킷이 하나씩 도착하고 스위칭 패브릭이 회선 속도의 세 배로 돈다. "
          "슬롯 하나 안에 세 번 전송이 들어가므로 다음 묶음이 도착하기 전에 이번 묶음이 모두 건너가고 입력 큐가 빈다.")

slot(d, 0, crossed=3, left=0)
slot(d, 1, crossed=3, left=0)
slot(d, 2, crossed=3, left=0, focal=True)
out_arrow(d, 2)

d.legend(LEGEND_Y, [("패브릭을 건너 나감", OK), ("다음 묶음 전에 비워짐", ACC)])
d.save("04-02.fabric-speedup.svg")
