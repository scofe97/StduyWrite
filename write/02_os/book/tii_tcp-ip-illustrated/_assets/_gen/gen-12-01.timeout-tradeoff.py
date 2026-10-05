# 12-01 §5 — 재전송 타임아웃을 어디에 둘 것인가. 원서 12.1.4 에는 그림이 없어 본문 문장을 시간축 위에 옮긴다.
# 원문 12.1.4: 송신자가 기다릴 시간은 대략 넷의 합이다 — 패킷을 보내는 시간, 수신자가 처리하고 ACK 를 보내는 시간,
#   ACK 가 돌아오는 시간, 송신자가 ACK 를 처리하는 시간. 어느 것도 확실히 알 수 없고 부하에 따라 바뀐다.
#   참 RTT 는 표본 평균에 가깝다고 보지만, 타이머를 평균과 똑같이 잡으면 실제 RTT 가운데 상당수가 그보다 길어
#   원치 않는 재전송이 생긴다. 타임아웃은 평균보다 커야 한다. 너무 크게 잡으면 망이 놀아 처리량이 떨어진다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 시간축 + 행마다 막대, 막대 길이 = 구간.
#           축약: 가로축에 눈금 수치가 없다. 원문에 값이 없으므로 길이는 순서·앞뒤만 보이는 모식이고 분포 곡선은 그리지 않는다.
#           둘째·셋째 행은 같은 늦은 왕복에서 타이머 위치 하나만 다르다. 넷째 행은 손실 장면이다.
#           focal 은 평균보다 큰 타이머 하나 — 절 제목의 결론.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 920, 504
LX = 20
TX0, TX1 = 216, 872
PIECE = 80                     # 네 조각 하나의 폭
X_MEAN = TX0 + 4 * PIECE       # 평균 RTT = 네 조각의 합
X_LATE = TX0 + 5 * PIECE       # 이번 왕복이 평균보다 길게 끝나는 자리
X_T_OK = X_LATE + 32           # 평균보다 큰 타이머
X_T_BIG = 856                  # 너무 큰 타이머
ROW_H, BAR_H = 72, 24
Y_AX, Y0 = 116, 132

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01 §5",
      "재전송 타이머는 평균보다 크되 너무 크지 않게",
      "맨 윗줄은 송신자가 기다릴 시간 네 조각이 이어져 한 번의 왕복이 되는 모습이고, 그 끝을 평균 RTT 로 삼는다. "
      "둘째·셋째 줄은 이번 왕복이 평균보다 길게 끝난 같은 장면에서 타이머 위치만 다르다. 타이머가 평균이면 ACK 보다 먼저 만료돼 "
      "필요 없는 재전송이 나가고, 평균보다 크면 ACK 가 먼저 와 재전송이 없다. 넷째 줄은 패킷이 사라진 장면으로, 타이머가 너무 크면 "
      "다시 보내기 전까지 망이 논다. 길이는 측정값이 아니라 순서만 보이는 모식이다.",
      "타이머가 평균이면 헛되이 다시 보내고, 너무 크면 손실 뒤 망이 오래 놉니다")

# 시간축 — 수치 없이 기준점만
d.t(TX0, Y_AX, "보냄", 12, SOFT, KR, "start")
d.t(X_MEAN, Y_AX, "평균 RTT", 12, SOFT, KR, "middle", 600)
d.t(TX1, Y_AX, "시간", 12, SOFT, KR, "end")

ROWS = [("평균적인 왕복", "기다릴 시간 네 조각"),
        ("타이머 = 평균", "이번 왕복이 더 김"),
        ("타이머 > 평균", "같은 늦은 왕복"),
        ("타이머가 너무 큼", "패킷이 사라짐")]
for i, (lab, sub) in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.box(LX - 8, y, W - 40 - (LX - 8), ROW_H - 8, PAPER2, RULE, 0.8, 6)
    d.t(LX + 4, y + 26, lab, 13, INK, KR, "start", 600)
    d.t(LX + 4, y + 46, sub, 12, MUTED, KR, "start")

# 평균 RTT 기준선 — 평균과 견주는 앞의 세 줄에만
d.line(X_MEAN, Y_AX + 8, X_MEAN, Y0 + 3 * ROW_H - 8, RULE, 0.8, "2 4")

def bar(i, x0, x1, c, label, dash=False, row2=False):
    y = Y0 + i * ROW_H + (38 if row2 else 10)
    h = 20 if row2 else BAR_H
    if dash:
        d.o.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h}" rx="4" fill="none" stroke="{c}" stroke-width="1.1" stroke-dasharray="5 4"/>')
    else:
        d.tone(x0, y, x1 - x0, h, c, 4, "14", 1.0)
    if label:
        d.t((x0 + x1) / 2, y + h / 2 + 5, label, 12, c, KR, "middle", 600)

def timer(i, x, c, sw=2.0):
    y = Y0 + i * ROW_H
    d.line(x, y + 4, x, y + ROW_H - 12, c, sw)

# 0행 — 네 조각의 합이 한 번의 왕복
for k, lab in enumerate(["송신", "수신 처리", "ACK 귀환", "ACK 처리"]):
    bar(0, TX0 + k * PIECE, TX0 + (k + 1) * PIECE, INFO, lab)
d.t(X_MEAN + 12, Y0 + 26, "넷의 합 · 어느 것도 확실히 모름", 12, MUTED, KR, "start")

# 1행 — 타이머 = 평균, 이번 왕복이 더 김
bar(1, TX0, X_LATE, INFO, "이번 왕복 · 끝에서 ACK 도착")
timer(1, X_MEAN, WARN)
bar(1, X_MEAN, X_MEAN + 2 * PIECE, WARN, "필요 없는 재전송", row2=True)

# 2행 — 타이머 > 평균, 같은 늦은 왕복 (focal)
bar(2, TX0, X_LATE, INFO, "이번 왕복 · 끝에서 ACK 도착")
timer(2, X_T_OK, ACC, 2.4)
d.t(X_T_OK + 12, Y0 + 2 * ROW_H + 27, "ACK 먼저 · 재전송 없음", 12, ACC, KR, "start", 600)

# 3행 — 패킷 손실, 타이머가 너무 큼
bar(3, TX0, TX0 + PIECE, INFO, "송신")
d.t(TX0 + PIECE + 12, Y0 + 3 * ROW_H + 28, "✕", 15, BAD, KR, "start", 700)
bar(3, TX0 + PIECE + 40, X_T_BIG, BAD, "재전송 전까지 노는 구간", dash=True)
timer(3, X_T_BIG, BAD)
d.t(TX0 + PIECE + 40, Y0 + 3 * ROW_H + 54, "타이머가 클수록 길어짐", 12, BAD, KR, "start")

d.legend(H - 56, [("평균보다 큰 타이머", ACC), ("왕복 구간", INFO), ("평균 타이머 · 필요 없는 재전송", WARN), ("너무 큰 타이머 · 노는 구간", BAD)])
d.save("12-01.timeout-tradeoff.svg")
