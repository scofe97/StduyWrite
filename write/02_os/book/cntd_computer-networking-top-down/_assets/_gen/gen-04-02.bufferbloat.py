# 04-02 §3 — 원문 Figure 4.10 의 버퍼블로트. ACK 클록킹 때문에 큐가 줄지 않는다.
# 원문의 값(전송 20 ms · 버스트 25 · 다음 ACK 는 20 ms 뒤)을 쓰되, RTT 는 원문의 200 ms 가 아니라
# 원문 자신의 결론(21번째 전송 중 · 큐 다섯)과 맞는 400 ms 로 그렸다. 본문에 이 어긋남을 정오로 적어 두었다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 시간 축 + 행마다 막대 하나, 국면별 zone 묶음.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 592
LX, TX0, TX1 = 20, 230, 950
ROW_H, BAR_H, Y0 = 40, 22, 172
TMAX = 480

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §3",
      "큐가 줄지 않습니다",
      "가정용 라우터의 출력 링크. 하나가 나갈 때마다 ACK 가 하나를 불러들여 큐 길이가 그대로 유지된다.",
      "손실은 한 건도 없는데 지연만 일정하게 남습니다")

def xp(t): return TX0 + t / TMAX * (TX1 - TX0)

for g in range(0, TMAX + 1, 80):
    x = xp(g)
    d.line(x, 142, x, Y0 + 5 * ROW_H, RULE, 0.8)
    d.t(x, 134, f"{g} ms", 12, MUTED, MONO)
d.line(TX0, 142, TX1, 142, RULE, 1.0)

ROWS = [
    ("패킷 1~20 전송", 0, 400, MUTED, False, "20 ms 씩 스무 개"),
    ("첫 ACK 도착", 400, 420, OK, True, "이때 21번째를 전송 중"),
    ("ACK 가 부른 새 패킷", 400, 480, ACC, True, "나간 만큼 들어옵니다"),
]
for i, (name, s, e, c, focal, note) in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.t(LX + 8, y + 30, name, 12, INK, KR, "start", 600)
    x0, x1 = xp(s), xp(e)
    if focal: d.tone(x0, y + 12, max(x1 - x0, 12), BAR_H, c, 4)
    else: d.box(x0, y + 12, x1 - x0, BAR_H, PAPER, c, 1.0, 4)
    nx = x1 + 12 if x1 + 12 + len(note) * 11 < 980 else x0 - 12
    d.t(nx, y + 28, note, 12, c if focal else SOFT, KR, "start" if nx > x0 else "end")

QY = Y0 + 3 * ROW_H + 12
d.t(LX + 8, QY + 26, "큐 길이", 12, INK, KR, "start", 600)
for i, (t, q) in enumerate([(0, 25), (80, 21), (160, 17), (240, 13), (320, 9), (400, 5), (480, 5)]):
    c = ACC if t >= 400 else MUTED
    d.o.append(f'<circle cx="{xp(t):.1f}" cy="{QY + 26 - q * 1.6:.1f}" r="4" fill="{c}"/>')
    d.t(xp(t), QY + 26 - q * 1.6 - 12, str(q), 12, c, MONO)
d.t(xp(440), QY + 26 - 5 * 1.6 + 22, "여기서부터 줄지 않습니다", 12, ACC, KR)

d.t(20, 414, "정상 상태 큐 = 윈도 − 대역폭·지연 곱. 여기서는 25 − 20 = 5 이고, 그 다섯이 만드는 지연이 사라지지 않습니다.",
     11, MUTED, KR, "start")
d.t(20, 436, "파이프는 꽉 차 있고 손실도 없습니다. 그런데 게이머는 100 ms 를 늘 더 기다립니다 — 이것이 버퍼블로트입니다.",
     11, MUTED, KR, "start")
d.t(20, 466, "원문은 RTT 를 200 ms 라 적는데, 그러면 t=200 에 11번째를 전송 중이고 큐가 15 여야 합니다.",
     11, SOFT, KR, "start")
d.t(20, 488, "원문 자신의 결론인 '21번째·큐 다섯'과 맞는 값은 400 ms 라, 이 그림은 400 ms 로 그렸습니다.",
     11, SOFT, KR, "start")

d.legend(H - 48, [("ACK 가 불러들인 패킷", ACC), ("첫 ACK", OK), ("전송 구간", MUTED)])
d.save("04-02.bufferbloat.svg")
