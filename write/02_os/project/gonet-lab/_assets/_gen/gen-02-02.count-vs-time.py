# 02-02.count-vs-time — 같은 순서 뒤바뀜을 개수 기준과 시간 기준(RACK)이 어떻게 판정하나
# 본문 요구(02-02 §2 「개수로 기다리기」, §3 「시간으로 기다리기 - RACK」):
#           N 이 10ms 늦고 N+1~N+3 이 먼저 도착하면, 개수 기준(문턱 3)은 3 번째 도착에서 N 을 잃었다고 판정해 불필요한 재전송을 하고,
#           RACK 은 N 을 보낸 뒤 RTT + 재정렬 창이 지나야 판정한다. 창이 좁으면 역시 틀리고, DSACK 으로 창이 넓어지면 N 을 기다린다.
# 타입 스펙: type-flowchart — 공통 시간축 위 네 줄. focal 은 창이 넓어져 기다리는 마지막 줄.
# 사실 출처: RFC 8985 §3.3.1·§3.3.2, Linux net/ipv4/tcp_recovery.c tcp_rack_reo_wnd, 02-01 Phase 3 실험 5.
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, RULE, MONO, KR

W, H = 960, 470
T0, PX = 230, 52          # 0ms 의 x, 1ms 당 px (0~12ms → 230~854)
ROWS = [128, 204, 280, 356]
RH = 40


def x(ms):
    return T0 + ms * PX


d = D(W, H, "FLOWCHART · 02-02 COUNT VS TIME", "같은 뒤바뀜, 두 가지 판정",
      "세그먼트 N 이 10ms 늦고 뒤에 보낸 N+1, N+2, N+3 이 먼저 도착한다. 개수 기준은 뒤 세그먼트 셋이 도착한 3ms 에 N 을 "
      "잃었다고 판정해 불필요하게 재전송한다. 시간 기준인 RACK 은 N 을 보낸 뒤 RTT 와 재정렬 창이 지나야 판정하므로, "
      "창이 좁으면 역시 틀리고 DSACK 으로 창이 넓어지면 N 이 도착할 때까지 기다린다.",
      lead="일반적인 예입니다. 가로축은 N 을 보낸 뒤 흐른 시간입니다.")

labels = ["도착 순서", "개수 기준 (문턱 3)", "RACK · 창 좁음", "RACK · DSACK 뒤 창 넓음"]
for y, lab in zip(ROWS, labels):
    d.t(24, y + 25, lab, 12, MUTED, KR, "start", 600)
    d.line(T0, y + RH / 2, x(12), y + RH / 2, RULE, 0.8, "3 6")

# 도착 줄
y = ROWS[0]
for ms, name in ((1, "N+1"), (2, "N+2"), (3, "N+3")):
    d.box(x(ms) - 22, y + 4, 44, 32)
    d.t(x(ms), y + 25, name, 12, INK, MONO, "middle", 600)
d.tone(x(10) - 22, y + 4, 44, 32, ACC, 5, "14", 1.4)
d.t(x(10), y + 25, "N", 13, ACC, MONO, "middle", 600)

# 개수 기준: 3ms 에 판정
y = ROWS[1]
d.line(x(3), ROWS[0] + 36, x(3), y + 4, BAD, 1.2, "4 4")
d.tone(x(3) - 58, y + 4, 116, 32, BAD, 5, "10", 1.1)
d.t(x(3), y + 25, "N 재전송", 12, BAD, KR, "middle", 600)
d.t(x(3) + 70, y + 25, "불필요", 12, BAD, KR, "start")

# RACK 창 좁음: 0~5ms 창, 5ms 에 판정
y = ROWS[2]
d.tone(x(0), y + 12, 5 * PX, 16, INK, 4, "10", 0.8)
d.t(x(2.5), y + 8, "RTT + 창", 11, MUTED, KR, "middle")
d.tone(x(5) + 8, y + 4, 100, 32, BAD, 5, "10", 1.1)
d.t(x(5) + 58, y + 25, "N 재전송", 12, BAD, KR, "middle", 600)
d.t(x(5) + 120, y + 25, "불필요", 12, BAD, KR, "start")

# RACK 창 넓음: 0~11ms 창, 10ms 에 N 도착
y = ROWS[3]
d.tone(x(0), y + 12, 11 * PX, 16, OK, 4, "14", 1.4)
d.t(x(5.5), y + 8, "RTT + 넓어진 창", 11, OK, KR, "middle")
d.line(x(10), ROWS[0] + 36, x(10), y + 4, ACC, 1.2, "4 4")
d.t(x(10) - 8, y + 50, "N 도착 · 재전송 없음", 12, OK, KR, "end", 600)

# 시간축
ya = 420
d.line(T0, ya, x(12), ya, SOFT, 1.0)
for ms in range(0, 13, 2):
    d.line(x(ms), ya - 4, x(ms), ya + 4, SOFT, 1.0)
    d.t(x(ms), ya + 18, f"{ms}ms", 11, MUTED, MONO, "middle")

d.save("02-02.count-vs-time.svg")
print("ok count-vs-time")
