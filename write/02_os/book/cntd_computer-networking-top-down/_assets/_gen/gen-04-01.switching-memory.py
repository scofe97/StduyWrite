# 04-01 §5 — 세 스위칭 방식 중 첫째. 원문 4.2.2 의 메모리 경유 방식.
# 2026-09-14 재작성: 네 단계를 정적 칸에 적고 장단점을 2단 격자로 붙이던 것을 걷어냈다.
#   패킷이 메모리를 *두 번* 건드린다는 것이 이 방식의 논지인데, 그 두 번이 글에만 있고
#   그림에는 없었다. 이제 같은 패킷이 t1 입력 → t2 메모리 → t3 출력으로 자리를 옮기고,
#   t2 에 쓰기·읽기 두 화살표가 같은 버스를 지나는 것이 보인다.
# 타입 스펙: type-data-flow — 단계마다 무엇이 건너가는가. 건너가는 것은 패킷 하나다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import ACC, MUTED, SOFT, INK, OK, WARN, INFO, KR, MONO
from _cc_04_01_fabric import (frame, packet, lane_y, note, snap_x,
                              SNAP_W, FAB_Y, FAB_H, PW, PH, IN_X, IN_W,
                              OUT_X, LEGEND_Y, H)

d = frame("메모리를 거쳐 — 같은 패킷을 두 번 옮깁니다",
          "패킷 하나가 메모리에 한 번 쓰이고 한 번 읽힙니다. 그 두 걸음이 같은 버스를 지납니다.",
          "원문 4.2.2 의 첫 방식. 초기 라우터는 그냥 컴퓨터였고 입출력 포트가 운영체제의 I/O 장치처럼 동작했다. "
          "패킷마다 메모리 쓰기 한 번과 읽기 한 번이 들고, 둘이 같은 공유 버스를 지나므로 처리량이 B/2 아래로 접힌다.",
          "공유 버스 · 프로세서 메모리")

MEM_W, MEM_H = 108, 46
mem_y = FAB_Y + (FAB_H - MEM_H) / 2


def memory(i, filled):
    """스냅샷 i 의 메모리 상자. filled 면 패킷이 그 안에 있다."""
    x = snap_x(i) + (SNAP_W - MEM_W) / 2
    d.tone(x, mem_y, MEM_W, MEM_H, INFO if filled else MUTED, 5, "14" if filled else "0A", 1.2)
    d.t(x + MEM_W / 2, mem_y + 18, "메모리", 13, INFO if filled else SOFT, KR)
    if filled:
        packet(d, x + (MEM_W - PW) / 2, mem_y + 24, INFO)
    return x


# t1 — 패킷이 입력 2 에 도착해 있다. 메모리는 비었다.
memory(0, False)
packet(d, snap_x(0) + 14, lane_y(1), WARN)
_ax = snap_x(0) + 14 + PW + 6
_ay = lane_y(1) + PH / 2
_bx = snap_x(0) + (SNAP_W - MEM_W) / 2 - 6
d.path(f"M {_ax} {_ay} L {(_ax + _bx) / 2} {_ay} L {(_ax + _bx) / 2} {mem_y + MEM_H / 2} "
       f"L {_bx} {mem_y + MEM_H / 2}", WARN, 1.3, m="warn")
note(d, 0, "도착 · 버스 대기", WARN)

# t2 — 같은 패킷이 메모리 안에 있다. 쓰기 한 번이 끝났고 읽기가 남았다.
mx = memory(1, True)
d.t(snap_x(1) + SNAP_W / 2, mem_y - 14, "쓰기 ①", 11, WARN, MONO)
d.t(snap_x(1) + SNAP_W / 2, mem_y + MEM_H + 20, "읽기 ②", 11, OK, MONO)
note(d, 1, "같은 버스 · 한 번에 하나", ACC)

# t3 — 패킷이 출력 2 로 나갔다. 메모리는 다시 비었다.
mx = memory(2, False)
_cx = mx + MEM_W + 6
_dx = snap_x(2) + SNAP_W - 40
d.path(f"M {_cx} {mem_y + MEM_H / 2} L {(_cx + _dx) / 2} {mem_y + MEM_H / 2} "
       f"L {(_cx + _dx) / 2} {lane_y(1) + PH / 2} L {_dx} {lane_y(1) + PH / 2}", OK, 1.3, m="ok")
packet(d, snap_x(2) + SNAP_W - 36, lane_y(1), OK)
note(d, 2, "출력 2 로 나감", OK)

d.tone(16, 356, 848, 52, ACC, 6, "12", 1.4)
d.t(40, 380, "메모리가 초당 B 패킷", 13, ACC, KR, "start", 600)
d.t(196, 380, "쓰기 + 읽기 두 번 → 처리량 B / 2", 13, INK, KR, "start")
d.t(470, 380, "목적지가 달라도 버스는 하나", 13, MUTED, KR, "start")

d.legend(LEGEND_Y, [("도착 · 대기", WARN), ("메모리 안", INFO), ("나감", OK)])
d.save("04-01.switching-memory.svg")
print("ok switching-memory")
