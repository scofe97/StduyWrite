# 04-02 §1 — 입력 큐잉이 "생기는" 쪽. 슬롯마다 셋이 도착하고 하나만 패브릭을 건너, 잔류 둘이 그대로 얹힌다.
# 슬롯 칸의 도착·통과·잔류 세 줄을 나란히 보면 큐가 2 → 4 → 6 으로 자라는 것이 패킷 수로 드러난다.
# 타입 스펙: type-data-flow — semantic-patterns 의 "Fan-in queue / bottleneck".
#           출발지 여럿 · 보이는 큐 슬롯 · 병목 하나 · 슬롯마다 누적되는 잔량.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import OK, WARN, MUTED, SOFT, ACC
from _cc_04_02_slots import frame, slot, out_arrow, LEGEND_Y

d = frame("패브릭이 회선만큼만 빠르면 줄이 쌓입니다",
          "슬롯마다 셋이 도착하는데 패브릭은 하나만 건넵니다. 남은 둘이 그대로 얹힙니다.",
          "입력 포트 세 곳에 슬롯마다 패킷이 하나씩 도착하는데 스위칭 패브릭이 회선과 같은 속도라 슬롯당 하나만 건넌다. "
          "건너지 못한 둘이 입력 큐에 남아 슬롯마다 두 개씩 누적된다.")

slot(d, 0, crossed=1, left=2)
slot(d, 1, crossed=1, left=4)
slot(d, 2, crossed=1, left=6, focal=True)
out_arrow(d, 2)

d.legend(LEGEND_Y, [("패브릭을 건너 나감", OK), ("입력 큐에 남음", WARN), ("멈추지 않는 누적", ACC)])
d.save("04-02.input-queue-buildup.svg")
