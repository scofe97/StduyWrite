# 01-02.tcp-window — 윈도우 크기는 확인 응답마다 새로 실려 오는 여유분이다
# 본문 요구(01-02 §2 "흐름 제어 — 창이 줄었다 늘었다"): "한 줄로 적으면 이 값이 움직인다는 점이
#           드러나지 않는다. 확인 응답마다 새로 실려 오면서 줄었다 늘었다 하는 것이 흐름 제어의
#           실제 모습"이다. 그래서 값을 표로 적지 않고 ACK 마다 오른쪽 게이지를 다시 그린다 —
#           4000 → 2000 → 0 → 3000 이 줄었다 늘었다 하는 그 움직임이다.
#           본문이 "보내는 쪽이 멈추는 자리가 win=0"이고 "기다리는 대상은 망이 아니라 받는 쪽
#           애플리케이션"이라고 못 박으므로, win=0 다음 줄에 송신 정지 칸을 세우고 그 옆에
#           "망은 한가한데 데이터가 흐르지 않는다"를 적었다.
# 타입 스펙: type-sequence.md — 주체 둘 사이의 시간순 메시지. 세로가 시간이다.
#           오른쪽 게이지 열은 시퀀스 밖의 보조 축이라 레인을 892 에서 끊고 그 오른쪽을 비웠다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 740   # 캔버스 상한 준수
LANE_W, SEQ_RIGHT = 168, 800      # 오른쪽 228px 은 수신 버퍼 게이지가 쓴다
LX, RX = 24 + LANE_W / 2, SEQ_RIGHT - LANE_W / 2
MID = (LX + RX) / 2
Y0, STRIDE = 200, 54
GX, GW, GMAX = 856, 104, 4000     # 게이지 만점은 첫 광고값 4000

d = D(W, H, "SEQUENCE · 01-02 TCP WINDOW",
      "윈도우 크기 — 확인 응답마다 새로 실려 오는 여유분",
      "TCP 흐름 제어. 수신 측이 확인 응답마다 알리는 윈도우 크기가 줄었다 늘었다 한다. "
      "0이 되면 송신이 멈추고, 수신 애플리케이션이 버퍼를 읽어 가야 창이 다시 열린다.",
      lead="보내는 쪽이 멈추는 자리가 win=0 입니다 — 기다리는 대상은 망이 아니라 받는 쪽 앱입니다.")

for cx, name, sub in ((LX, "보내는 쪽", "sender"), (RX, "받는 쪽", "receiver")):
    d.box(cx - LANE_W / 2, 104, LANE_W, 44, PAPER2, RULE, 1.0)
    d.t(cx, 124, name, 12, INK, KR, "middle", 600)
    d.t(cx, 141, sub, 11, MUTED, MONO)
for cx in (LX, RX):
    d.line(cx, 154, cx, 670, RULE, 1.0, "3 6")

d.t(GX + GW / 2, 182, "수신 버퍼 여유", 11, SOFT, MONO)

# 세로는 슬롯 번호가 곧 시간이다. 6번 슬롯만 메시지가 아니라 송신이 멈춘 구간이라
# 아래에서 슬롯 순서대로 한 번에 그린다 — 시간 축 위의 칸이므로 순서를 건너뛰면 안 된다.
# (방향, 라벨, 부제, 색, 마커, 굵기, 광고된 win) — win 이 None 이면 게이지를 그리지 않는다
MSGS = {
    0: (1, "DATA 1000B", None, OK, "ok", 1.5, None),
    1: (0, "ACK  win=4000", "여유 넉넉 — 계속 보내도 된다", INFO, "info", 1.3, 4000),
    2: (1, "DATA 2000B", None, OK, "ok", 1.5, None),
    3: (0, "ACK  win=2000", "처리에 밀리기 시작 — 창이 줄었다", WARN, "warn", 1.3, 2000),
    4: (1, "DATA 2000B", None, OK, "ok", 1.5, None),
    5: (0, "ACK  win=0", "버퍼가 찼다 — 송신이 멈춘다", BAD, "bad", 1.3, 0),
    7: (0, "Window Update  win=3000", "앱이 읽어 갔다 — 창이 다시 열린다", ACC, "acc", 1.3, 3000),
    8: (1, "DATA 2000B", None, OK, "ok", 1.5, None),
}
STOP_SLOT = 6

for slot in range(9):
    y = Y0 + STRIDE * slot
    if slot == STOP_SLOT:
        d.tone(LX - 70, y - 14, 140, 28, BAD, 6, "1A", 1.3)
        d.t(LX, y + 5, "송신 정지", 11, BAD, KR, "middle", 600)
        d.t(LX + 120, y + 5, "망은 한가한데 데이터가 흐르지 않는다", 11, MUTED, KR, "start")
        continue
    fwd, label, sub, c, mk, sw, win = MSGS[slot]
    if fwd:
        d.path(f"M {LX+10} {y} L {RX-12} {y}", c, sw, m=mk)
    else:
        d.path(f"M {RX-10} {y} L {LX+12} {y}", c, sw, m=mk, dash="4 4")
    d.t(MID, y - 9, label, 11, c, MONO, "middle", 600)
    if sub:
        d.t(MID, y + 15, sub, 11, MUTED)
    if win is None:
        continue
    gy = y - 10
    d.box(GX, gy, GW, 20, PAPER2, RULE, 0.8, 4)
    if win:                       # win=0 은 채울 것이 없다 — 빈 트랙이 곧 그 뜻이다
        d.tone(GX, gy, GW * win / GMAX, 20, c, 4, "44", 1.1)
    d.t(GX + GW + 8, gy + 14, str(win), 11, c, MONO, "start", 600)

d.legend(696, [("데이터 전송", OK), ("창이 줄었다", WARN),
               ("창이 닫혔다 win=0", BAD), ("앱이 읽어 창이 열림", ACC)])
d.save("01-02.tcp-window.svg")
print("ok tcp-window")
