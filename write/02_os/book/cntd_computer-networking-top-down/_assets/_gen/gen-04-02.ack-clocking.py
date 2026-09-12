# 04-02 §3 버퍼블로트 — 원문 Figure 4.10 의 ACK 클록킹. 큐에서 하나가 나가면 한 RTT 뒤 ACK 가 하나를 불러들여 큐 길이가 그대로다.
# 정거장 여덟은 원문 시나리오의 순서(전송 20 ms · ACK · 새 세그먼트 · 큐 입장)를 편 것이고, 허브의 다섯은 원문 자신의 결론값이다.
# 줄에서 기다리는 100 ms 는 5 × 20 ms 로, 본문의 정오 노트가 검산한 값이다.
# 타입 스펙: type-loop — 마지막 단계가 첫 단계를 먹이고 허브에 상태(큐 길이)가 쌓인다. 정거장 5~8 · 허브 하나.
#           반경 방향 스포크는 스펙이 허용한 예외지만 이 그림은 축 위(위·왼쪽) 정거장 둘에서만 내려 사선을 만들지 않는다.
import sys, math; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 700
CXY = (500, 352)
R = 212
SW, SH = 136, 52
HW, HH = 184, 84
N = 8
ST = [("큐에서 하나 나감", "링크로", "−1"),
      ("링크 위 20 ms", "병목 속도"),
      ("서버 도착", "세그먼트"),
      ("ACK 발송", "서버가"),
      ("ACK 도착", "한 RTT 뒤"),
      ("하나 더 보냄", "ACK 가 TCP 를 깨움"),
      ("큐 입장", "가정용 라우터", "+1"),
      ("줄에서 기다림", "5 × 20 = 100 ms")]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §3",
      "하나가 나가면 하나가 들어옵니다",
      "원문 Figure 4.10 의 ACK 클록킹. 큐에서 세그먼트가 나가 ACK 가 돌아오면 TCP 가 하나를 더 보내 그 자리를 채우므로 큐 길이는 줄지 않는다.",
      "나간 세그먼트의 ACK 는 한 RTT 뒤에 오고, 허브의 다섯은 그대로입니다")

def center(k):
    th = math.radians(-90 + k * 360 / N)
    return CXY[0] + R * math.cos(th), CXY[1] + R * math.sin(th), th

def hits(cx, cy):
    """정거장 상자와 원의 교점 (스펙 §2.2)"""
    pts = []
    x0, x1, y0, y1 = cx - SW / 2, cx + SW / 2, cy - SH / 2, cy + SH / 2
    for xe in (x0, x1):
        dx = xe - CXY[0]
        if abs(dx) <= R:
            dy = math.sqrt(R * R - dx * dx)
            for y in (CXY[1] - dy, CXY[1] + dy):
                if y0 - 0.01 <= y <= y1 + 0.01: pts.append((xe, y))
    for ye in (y0, y1):
        dy = ye - CXY[1]
        if abs(dy) <= R:
            dx = math.sqrt(R * R - dy * dy)
            for x in (CXY[0] - dx, CXY[0] + dx):
                if x0 - 0.01 <= x <= x1 + 0.01: pts.append((x, ye))
    return pts

def exit_entry(k):
    cx, cy, th = center(k)
    best_exit, best_entry = None, None
    for (x, y) in hits(cx, cy):
        ph = math.atan2(y - CXY[1], x - CXY[0])
        dd = (ph - th + math.pi) % (2 * math.pi) - math.pi
        if dd > 0 and (best_exit is None or dd < best_exit[0]): best_exit = (dd, x, y, ph)
        if dd < 0 and (best_entry is None or dd > best_entry[0]): best_entry = (dd, x, y, ph)
    return best_exit, best_entry

# 링 화살표 (상자보다 먼저 그려 z-order 를 맞춘다)
for k in range(N):
    ex, _ = exit_entry(k)
    _, en = exit_entry((k + 1) % N)
    ph_end = en[3] - 1.2 / R
    x2, y2 = CXY[0] + R * math.cos(ph_end), CXY[1] + R * math.sin(ph_end)
    d.path(f"M {ex[1]:.3f} {ex[2]:.3f} A {R} {R} 0 0 1 {x2:.3f} {y2:.3f}", MUTED, 1.2, m="ar")

# 허브
d.tone(CXY[0] - HW / 2, CXY[1] - HH / 2, HW, HH, ACC, 8, "14", 1.4)
d.t(CXY[0], CXY[1] - 8, "출력 큐 길이 5", 14, ACC, KR, "middle", 600)
d.t(CXY[0], CXY[1] + 14, "줄지 않습니다", 12, SOFT, KR)
d.t(CXY[0], CXY[1] + 32, "queue = 25 − 20", 11, SOFT, MONO)

# 쓰기 스포크 — 위(−1)·왼쪽(+1) 정거장에서 허브로, 축 위라 사선이 아니다
GAP = 6
cx0, cy0, _ = center(0)
d.path(f"M {cx0:.3f} {cy0 + SH / 2 + 2:.3f} L {cx0:.3f} {CXY[1] - HH / 2 - GAP:.3f}", ACC, 1.1, m="acc", dash="4 3")
d.t(cx0 + 10, (cy0 + SH / 2 + CXY[1] - HH / 2) / 2 + 4, ST[0][2], 12, ACC, MONO, "start", 600)
cx6, cy6, _ = center(6)
d.path(f"M {cx6 + SW / 2 + 2:.3f} {cy6:.3f} L {CXY[0] - HW / 2 - GAP:.3f} {cy6:.3f}", ACC, 1.1, m="acc", dash="4 3")
d.t((cx6 + SW / 2 + CXY[0] - HW / 2) / 2, cy6 - 10, ST[6][2], 12, ACC, MONO, "middle", 600)

# 정거장
for k, st in enumerate(ST):
    cx, cy, _ = center(k)
    cx, cy = round(cx / 4) * 4, round(cy / 4) * 4
    d.box(cx - SW / 2, cy - SH / 2, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(cx, cy - 4, st[0], 13, INK, KR, "middle", 600)
    d.t(cx, cy + 15, st[1], 12, SOFT, KR)

d.t(24, 616, "ACK 가 하나 오면 TCP 가 세그먼트를 하나 내보내고 그것이 곧장 가정용 라우터의 큐에 들어갑니다. 나간 만큼 들어오니 길이가 줄지 않습니다.", 13, MUTED, KR, "start")
d.t(24, 638, "파이프는 꽉 차 있고 손실은 한 건도 없습니다. 그런데 게이머는 큐의 다섯만큼 100 ms 를 늘 더 기다립니다 — 버퍼블로트입니다.", 13, SOFT, KR, "start")

d.legend(H - 44, [("허브 — 줄지 않는 큐와 그것을 바꾸는 두 사건", ACC), ("한 바퀴 = RTT + 줄에서 기다린 시간", MUTED)])
d.save("04-02.ack-clocking.svg")
