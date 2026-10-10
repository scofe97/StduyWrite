# 타입 스펙: type-gantt — 지연 ACK 타이머 동작과 편승·만료 조건별 구간 비교.
# 사실 출처: ch15.txt 193~242행, RFC 9293 §3.8.6.3, Linux include/net/tcp.h — TCP_DELACK_MIN 40ms, TCP_DELACK_MAX 200ms, 편승 15ms, quickack 0ms.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 920, 500
LX = 24
TX0, TX1 = 250, 680
ROW_H, BAR_H = 76, 26
Y_AX, Y0 = 120, 142

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-01 §2",
      "지연 ACK 의 타이머 구간과 송신 시점",
      "세그먼트를 받은 수신자는 즉시 ACK 를 보내지 않고 타이머를 켠 뒤 응답 데이터가 생기기를 기다린다. "
      "데이터가 생기면 그 세그먼트에 ACK 를 실어 보내고, 데이터가 없으면 타이머 만료 시 순수 ACK 를 전송한다. "
      "두 번째 전체 크기 세그먼트가 도착하거나 quickack 모드일 때는 지연 없이 즉시 전송한다.",
      "보낼 데이터에 ACK 를 얹으면 대화형 패킷이 넷에서 셋으로 줄어듭니다")

MS_SCALE = (TX1 - TX0) / 200.0  # 200ms = TX1 - TX0
def ms_x(ms): return TX0 + ms * MS_SCALE

TICKS = [(0, "0ms"), (40, "40ms"), (100, "100ms"), (200, "200ms")]
for ms, lab in TICKS:
    x = ms_x(ms)
    d.line(x, Y_AX + 6, x, Y0 + 4 * ROW_H - 12, RULE, 0.7, "2 4")
    d.t(x, Y_AX, lab, 11, SOFT, MONO, "middle")

ROWS = [
    ("즉시 ACK (quickack)", "지연 없이 즉시 응답"),
    ("지연 ACK (데이터 편승)", "응답 데이터에 ACK 결합"),
    ("지연 ACK (타이머 만료)", "데이터 없어 순수 ACK 전송"),
    ("두 번째 MSS 도착", "누적 ACK 규정 충족"),
]

for i, (lab, sub) in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.box(LX, y, TX0 - LX - 16, ROW_H - 12, PAPER2, RULE, 0.8, 6)
    d.t(LX + 12, y + 26, lab, 13, INK, KR, "start", 600)
    d.t(LX + 12, y + 46, sub, 11, MUTED, KR, "start")

def bar(row, ms_start, ms_end, c, label, is_event=False):
    y = Y0 + row * ROW_H + 12
    x0, x1 = ms_x(ms_start), ms_x(ms_end)
    if is_event:
        d.line(x0, y - 3, x0, y + BAR_H + 3, c, 2.4)
        d.t(x0 + 10, y + BAR_H / 2 + 4, label, 11, c, KR, "start", 600)
    else:
        w = max(x1 - x0 - 2, 6)
        d.tone(x0 + 1, y, w, BAR_H, c, 4, "16", 1.0)
        if label:
            if w >= 70:
                d.t((x0 + x1) / 2, y + BAR_H / 2 + 4, label, 11, c, KR, "middle", 600)
            else:
                d.t((x0 + x1) / 2, y - 4, label, 11, c, KR, "middle", 600)

# 1. 즉시 ACK
bar(0, 0, 0, INFO, "도착 즉시 순수 ACK 전송 (지연 0ms)", is_event=True)

# 2. 지연 ACK 데이터 편승 (지연 도중 응답 데이터 발생 예시)
bar(1, 0, 30, WARN, "대기")
bar(1, 30, 30, OK, "응답 데이터 발생 · ACK 편승 송신 (예시 시점)", is_event=True)

# 3. 지연 ACK 타이머 만료 (Linux TCP_DELACK_MIN 40ms ~ TCP_DELACK_MAX 200ms)
bar(2, 0, 40, WARN, "최소 40ms")
bar(2, 40, 200, SOFT, "대기 구간 (상한 200ms)")
bar(2, 200, 200, BAD, "타이머 만료 · 순수 ACK 전송 (200ms)", is_event=True)

# 4. 두 번째 MSS 세그먼트 도착 (지연 도중 두 번째 전체 크기 도착 예시)
bar(3, 0, 50, WARN, "대기")
bar(3, 50, 50, OK, "2번째 전체 MSS 도착 · 즉시 ACK (예시 시점)", is_event=True)

d.legend(H - 46, [
    ("지연 타이머 대기 구간", WARN),
    ("편승 및 조건 충족 즉시 전송", OK),
    ("타이머 만료 단독 전송", BAD),
    ("즉시 ACK 모드 전송", INFO)
])

d.save("15-01.delayed-ack-timing.svg")
