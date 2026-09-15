# 04-01 §5 — 세 스위칭 방식 중 둘째. 원문 4.2.2 의 공유 버스.
# 2026-09-14 재작성: 세 줄을 정적으로 늘어놓고 "한 번에 하나"를 글로만 적던 것을 걷어냈다.
#   한 번에 하나라는 것이 이 방식의 상한인데, 정적 3행에서는 셋이 동시에 건너는 것처럼 보였다.
#   이제 패킷 셋이 t1·t2·t3 에 걸쳐 *차례로* 버스를 건너고, 건너지 못한 것은 입력에 남아 있다.
# 타입 스펙: type-data-flow — 단계마다 무엇이 건너가는가. 버스 위의 자리가 하나뿐인 것이 논지다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import ACC, MUTED, SOFT, INK, OK, WARN, PAPER, KR, MONO
from _cc_04_01_fabric import (frame, packet, lane_y, note, snap_x,
                              SNAP_W, FAB_Y, FAB_H, PW, PH, LEGEND_Y, H)

d = frame("버스를 거쳐 — 한 번에 하나씩만 건넙니다",
          "셋이 동시에 도착해도 버스 자리는 하나입니다. 나머지는 입력에 남습니다.",
          "원문 4.2.2 의 둘째 방식. 입력 포트가 스위치 내부용 라벨을 붙여 버스에 실으면 모든 출력 포트가 받되 "
          "라벨이 맞는 포트만 보관한다. 버스를 건너는 자리가 하나뿐이라 스위칭 속도가 버스 속도에 묶인다.",
          "공유 버스 — 자리 하나")

BUS_Y = FAB_Y + FAB_H - 52

# 슬롯마다 (버스를 건너는 입력, 아직 입력에 남은 것들)
SCENE = [(0, [1, 2]), (1, [2]), (2, [])]

for i, (crossing, waiting) in enumerate(SCENE):
    x = snap_x(i)
    # 버스 — 칸을 가로지르는 한 줄. 이 줄 위에 패킷은 언제나 하나뿐이다.
    d.line(x + 12, BUS_Y + PH + 14, x + SNAP_W - 12, BUS_Y + PH + 14, ACC, 2.2)
    d.t(x + SNAP_W - 12, BUS_Y + PH + 28, "버스", 11, ACC, MONO, "end")

    # 건너는 중인 패킷 하나 — 버스 위 한가운데
    packet(d, x + SNAP_W / 2 - PW / 2, BUS_Y, ACC, f"{crossing + 1}")

    # 아직 자기 입력 줄에 남아 있는 패킷들
    for k in waiting:
        packet(d, x + 14, lane_y(k), WARN, f"{k + 1}")

label = ["1 이 건넘 · 2·3 대기", "2 가 건넘 · 3 대기", "3 이 건넘 · 대기 없음"]
for i in range(3):
    note(d, i, label[i], ACC if i < 2 else OK)

d.tone(16, 356, 848, 52, ACC, 6, "12", 1.4)
d.t(40, 380, "버스 속도 = 스위칭 속도", 13, ACC, KR, "start", 600)
d.t(232, 380, "셋을 보내려면 슬롯 셋 — 라우팅 프로세서는 거치지 않음", 13, INK, KR, "start")
d.t(628, 380, "라벨은 건널 때만 쓰고 뗀다", 13, MUTED, KR, "start")

d.legend(LEGEND_Y, [("버스를 건너는 중", ACC), ("입력에서 대기", WARN)])
d.save("04-01.switching-bus.svg")
print("ok switching-bus")
