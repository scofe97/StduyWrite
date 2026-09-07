# 03-02 §2 — 원문 3.4.2 의 대륙 횡단 예. RTT 30 ms · R 1 Gbps · L 8,000 비트.
# 시간 값은 원문 그대로이고 파이썬으로 검산해 다섯 값이 모두 일치함을 확인했다.
# 가로 축이 30.008 ms 인데 전송 구간은 0.008 ms 라, 실제 비율로 그리면 막대가 0.2px 로 보이지 않는다.
# 그래서 전송 구간만 눈에 보이게 최소 폭을 준다 — 축약을 여기 적어 둔다. 비율의 요점은 아래 수치가 말한다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 시간 축 + 행마다 막대 하나, 국면별 zone 묶음.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 552
LX, TX0, TX1 = 20, 250, 950
ROW_H, BAR_H, Y0 = 40, 24, 168
TMAX = 30.008
MINW = 10          # 전송 구간의 최소 표시 폭

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-02 §2",
      "30밀리초 중 0.008밀리초만 보냅니다",
      "원문의 대륙 횡단 예. 링크는 1 Gbps 인데 정지 후 대기 때문에 유효 처리량이 267 kbps 로 떨어진다.",
      "가로 한 칸이 5 밀리초입니다 — 전송 구간은 실제로는 이보다 훨씬 얇습니다")

def xp(t): return TX0 + t / TMAX * (TX1 - TX0)

for g in range(0, 31, 5):
    x = xp(g)
    d.line(x, 138, x, Y0 + 3 * ROW_H, RULE, 0.8)
    d.t(x, 130, f"{g} ms", 11, MUTED, MONO)
d.line(TX0, 138, TX1, 138, RULE, 1.0)

ROWS = [
    ("보내는 중", 0, 0.008, ACC, True,  "0 → 0.008 ms"),
    ("전파 · 수신", 0.008, 15.008, INFO, False, "패킷이 대륙을 건넘"),
    ("ACK 가 돌아옴", 15.008, 30.008, MUTED, False, "다음 패킷은 그때까지 못 감"),
]
for i, (name, s, e, c, focal, note) in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.t(LX + 8, y + 30, name, 11, INK, KR, "start", 600)
    x0, x1 = xp(s), xp(e)
    w = max(x1 - x0, MINW)
    if focal: d.tone(x0, y + 12, w, BAR_H, c, 4)
    else: d.box(x0, y + 12, w, BAR_H, PAPER, c, 1.0, 4)
    d.t(x0 + max(w / 2, 40) + (30 if focal else 0), y + 28, note, 11, c if focal else SOFT,
        KR if any("가" <= ch <= "힣" for ch in note) else MONO)

BOT = Y0 + 3 * ROW_H
d.box(TX0 - 230, BOT + 22, 700, 96, PAPER2, RULE, 0.9, 6)
d.t(TX0 - 210, BOT + 50, "U = (L/R) / (RTT + L/R) = 0.008 / 30.008 = 0.00027", 12, ACC, MONO, "start", 600)
d.t(TX0 - 210, BOT + 74, "유효 처리량 = 8,000 비트 / 30.008 ms = 267 kbps", 12, INK, MONO, "start")
d.t(TX0 - 210, BOT + 98, "1 Gbps 링크를 깔아 놓고 267 kbps 를 씁니다", 11, SOFT, KR, "start")

d.t(20, 448, "해법은 창을 여는 것입니다. 셋을 미리 보내면 이용률이 세 배가 되고, 창이 대역폭·지연 곱만큼 크면 링크를 다 씁니다.",
     11, MUTED, KR, "start")
d.t(20, 470, "여기서는 30 ms 왕복의 1 Gbps 링크라 3.75 메가바이트가 공중에 떠 있어야 링크가 놀지 않습니다.",
     11, MUTED, KR, "start")

d.legend(H - 44, [("실제로 보내는 구간", ACC), ("기다리는 구간", INFO), ("놀고 있는 구간", MUTED)])
d.save("03-02.stop-and-wait-utilization.svg")
