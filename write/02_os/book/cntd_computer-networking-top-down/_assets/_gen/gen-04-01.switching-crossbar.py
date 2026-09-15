# 04-01 §5 — 세 스위칭 방식 중 셋째. 원문 4.2.2 의 크로스바.
# N 입력과 N 출력을 잇는 2N 개의 버스가 있고, 교차점을 패브릭 컨트롤러가 열고 닫는다.
# 논블로킹 조건도 원문 그대로다 — 같은 출력 포트로 가는 다른 패킷이 없는 한 막히지 않는다.
#
# 2026-09-14 재작성: type-dp-security-matrix 로 선언하고 교차점 상태를 3x3 격자에 적던 것을 걷어냈다.
#   타입 이름이 스펙에 있어 게이트는 통과했지만, 격자는 *조합의 가부*를 보이는 문법이라
#   "둘은 나란히 건너고 셋째는 기다린다"는 이 방식의 논지가 셀 안 글자로만 남았다.
#   이제 패킷 셋이 교차점 위를 실제로 지나고, 겹치는 하나만 제자리에 남는다.
# 타입 스펙: type-data-flow — 단계마다 무엇이 건너가는가. 동시에 둘이 건너는 것이 논지다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import ACC, MUTED, SOFT, INK, OK, WARN, INFO, KR, MONO
from _cc_04_01_fabric import (frame, packet, lane_y, note, snap_x,
                              SNAP_W, FAB_Y, FAB_H, PW, PH, LEGEND_Y, H)

d = frame("크로스바 — 줄이 겹치지 않으면 나란히 건넙니다",
          "입력 1 과 2 는 출력이 달라 동시에 건넙니다. 입력 3 은 출력 1 이 빌 때까지 기다립니다.",
          "원문 4.2.2 의 셋째 방식. N 입력과 N 출력을 잇는 2N 개의 버스가 놓이고, 가로와 세로가 만나는 교차점을 "
          "패브릭 컨트롤러가 열고 닫는다. 쓰는 줄이 겹치지 않으면 여러 쌍이 동시에 건너므로 버스 방식의 상한을 넘는다.",
          "교차점 — 열고 닫는 스위치")

# 입력 i 가 노리는 출력. 1 과 3 이 같은 출력 1 을 노려 겹친다.
DEST = {0: 0, 1: 1, 2: 0}
GRID_X0, GRID_STEP = 46, 42


def cross_points(i, lit):
    """스냅샷 i 의 교차점 격자. lit 에 든 (입력, 출력) 만 켜진다."""
    x0 = snap_x(i) + GRID_X0
    y0 = FAB_Y + 30
    for r in range(3):
        for c in range(3):
            on = (r, c) in lit
            cx = x0 + c * GRID_STEP
            cy = y0 + r * GRID_STEP
            d.tone(cx, cy, 12, 12, ACC if on else MUTED, 2, "FF" if on else "14", 1.0)
    return x0, y0


# t1 — 1→출력1 과 2→출력2 가 동시에 건넌다. 3 은 출력 1 이 겹쳐 입력에 남는다.
cross_points(0, {(0, 0), (1, 1)})
packet(d, snap_x(0) + 150, lane_y(0), OK, "1")
packet(d, snap_x(0) + 150, lane_y(1), OK, "2")
packet(d, snap_x(0) + 14, lane_y(2), WARN, "3")
note(d, 0, "1·2 동시 통과 · 3 대기", OK)

# t2 — 1 과 2 가 나갔다. 이제 출력 1 이 비어 3 이 건넌다.
cross_points(1, {(2, 0)})
packet(d, snap_x(1) + 150, lane_y(2), OK, "3")
note(d, 1, "출력 1 이 비어 3 통과", OK)

# t3 — 모두 나갔고 교차점은 다 닫혔다.
cross_points(2, set())
note(d, 2, "모두 나감 · 교차점 닫힘", MUTED)

d.tone(16, 356, 848, 52, ACC, 6, "12", 1.4)
d.t(40, 380, "논블로킹", 13, ACC, KR, "start", 600)
d.t(124, 380, "같은 출력으로 몰릴 때만 막힘 — 두 슬롯이면 셋이 다 건넌다", 13, INK, KR, "start")
d.t(560, 380, "입출력 8 개 → 줄 16 · 교차점 64", 13, MUTED, KR, "start")

d.legend(LEGEND_Y, [("건너는 중 · 교차점 열림", OK), ("출력 겹침으로 대기", WARN)])
d.save("04-01.switching-crossbar.svg")
print("ok switching-crossbar")
