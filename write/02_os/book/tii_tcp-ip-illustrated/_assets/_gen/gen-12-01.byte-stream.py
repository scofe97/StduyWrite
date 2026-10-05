# 12-01 §6 — 원문 12.2.1 의 예: 한쪽이 10·20·50 바이트로 세 번 쓰면 다른 쪽은 20 바이트씩 네 번 읽을 수도 있다.
#   TCP 는 레코드 표시나 메시지 경계를 넣지 않으므로 받는 쪽은 개별 write 크기를 알 수 없다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 축 + 행마다 막대 하나, 국면별 zone 묶음.
#           축약: 가로 축이 시간이 아니라 스트림 안의 바이트 위치(0–80)다. 행 × 축 × 막대 하나의 문법은 그대로 쓰고
#           "막대 길이 = 구간" 을 바이트 구간으로 읽는다. 가운데 TCP 행 하나가 경계 없는 80 바이트이고 focal.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 572
LX, TX0, TX1 = 20, 216, 872
ROW_H, BAR_H = 40, 24
TOTAL = 80
PITCH = (TX1 - TX0) / TOTAL          # 1 바이트 = 8.2px

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01 §6",
      "write 경계는 선을 건너지 못한다",
      "송신 애플리케이션이 10·20·50 바이트로 세 번 쓴 데이터는 TCP 안에서 경계 없는 80 바이트 줄 하나가 되고, "
      "수신 애플리케이션은 그것을 20 바이트씩 네 번 읽는다. 가로 축은 시간이 아니라 스트림 안의 바이트 위치다.",
      "가운데 줄에는 칸막이가 없습니다 — 경계를 다시 세우는 일은 애플리케이션 몫입니다")

Y_AX = 112
for b in range(0, TOTAL + 1, 10):
    x = TX0 + b * PITCH
    d.t(x, Y_AX, str(b), 11, SOFT, MONO)
    d.line(x, Y_AX + 8, x, 120 + 9 * ROW_H, RULE, 0.6, "2 4")
d.t(TX0 - 12, Y_AX, "바이트", 11, SOFT, KR, "end")

ZONES = [("송신 앱 · write 세 번", 0, 3), ("TCP · 바이트 스트림", 3, 1), ("수신 앱 · read 네 번", 4, 4)]
ROWS = [  # (라벨, 시작, 끝, 색)
    ("write 1", 0, 10, INFO), ("write 2", 10, 30, INFO), ("write 3", 30, 80, INFO),
    ("한 줄의 80 바이트", 0, 80, ACC),
    ("read 1", 0, 20, OK), ("read 2", 20, 40, OK), ("read 3", 40, 60, OK), ("read 4", 60, 80, OK),
]
Y0 = 132
GAP = 16          # zone 사이 띄움
def row_y(i):
    z = 0 if i < 3 else (1 if i < 4 else 2)
    return Y0 + i * ROW_H + z * GAP

for name, start, n in ZONES:
    y0 = row_y(start) - 4
    d.box(LX - 8, y0, W - 40 - (LX - 8), n * ROW_H + 0, PAPER2, RULE, 0.8, 6)
for name, start, n in ZONES:
    d.t(LX + 4, row_y(start) + 12, name, 12, SOFT, KR, "start", 600)

for i, (lab, s, e, c) in enumerate(ROWS):
    y = row_y(i)
    x, w = TX0 + s * PITCH, (e - s) * PITCH
    if c is ACC:
        d.o.append(f'<rect x="{x}" y="{y + 8}" width="{w}" height="{BAR_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        d.t(x + w / 2, y + 25, "경계 없음", 12, ACC, KR, "middle", 600)
        d.t(LX + 4, y + 30, lab, 12, ACC, KR, "start", 600)
    else:
        d.tone(x, y + 8, w, BAR_H, c, 4, "14", 1.0)
        d.t(x + w / 2, y + 25, f"{e - s}B", 11, c, MONO, "middle", 600)
        d.t(LX + 4 + 40, y + 30, lab, 12, INK, MONO, "start", 600)

d.legend(H - 56, [("TCP 안 · 칸막이 없는 줄", ACC), ("보낸 쪽의 write 단위", INFO), ("받는 쪽의 read 단위", OK)])
d.save("12-01.byte-stream.svg")
