# 14-03 §2 — DSACK·Eifel·F-RTO 가 같은 타이머 오탐 하나를 언제 알아채는지 한 축 위에 놓는다.
# 사실 출처(ch14.txt §14.7.1–14.7.4, RFC 3522·5682·4015):
#   Eifel: 재전송 때 TSval 저장, 그 번호를 덮는 첫 정상 ACK 의 TSecr 가 더 작으면 원본에 대한 ACK → 오탐.
#          손실 복구 전에 도착한 패킷이 만든 ACK 에 기대므로 DSACK 만 쓰는 방법보다 일찍 알 수 있다.
#   F-RTO: 타임아웃 재전송 뒤 첫 ACK 가 오면 새 데이터를 보내고, 두 번째 ACK 까지 본다. 둘 다 창을 전진시키면 오탐.
#   DSACK: 중복 세그먼트가 수신자에 도착한 뒤에야 보낼 수 있고, 그 DSACK 이 송신자에 돌아와야 쓸 수 있다.
#   Eifel 응답(§14.7.4): Eifel·F-RTO 처럼 일찍 잡으면 SPUR_TO, DSACK 처럼 늦게 잡으면 LATE_SPUR_TO.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 축 + 행마다 막대, 막대 길이 = 판정까지 걸리는 구간.
#           축약: 가로 축은 실제 시간이 아니라 '송신자가 증거를 받는 순서' 네 칸이다. 칸 사이 간격은 경로마다 다르다.
#           focal 은 가장 짧은 Eifel 막대 — DSACK 보다 이를 수 있다는 원서 문장의 그림.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 920, 456
LX, ROW_H, BAR_H = 20, 72, 28
COLS = [260, 440, 620, 800]   # 증거 순서 네 칸, stride 180

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-03 §2",
      "세 탐지법이 타이머 오탐을 아는 시점",
      "같은 타이머 오탐 한 번을 두고 송신자가 증거를 받는 순서를 가로로 놓았다. Eifel 은 원본에 대한 첫 ACK 의 TSecr 만으로 판정하고, "
      "F-RTO 는 첫 ACK 뒤 새 데이터를 보낸 다음 두 번째 ACK 까지 본다. DSACK 은 재전송본이 수신자에 닿은 뒤 그 보고가 돌아와야 한다. "
      "앞의 둘은 Eifel 응답의 SPUR_TO, DSACK 은 LATE_SPUR_TO 에 해당한다. 칸 사이의 실제 시간 간격은 경로마다 다르다.",
      "가로 축은 시간이 아니라 송신자가 증거를 받는 순서입니다")

HEAD = [("RTO 만료 · 재전송", "TSval T2 저장"), ("첫 ACK 도착", "원본에 대한 ACK"),
        ("두 번째 ACK 도착", "타임아웃 뒤"), ("DSACK 도착", "재전송본 수신 뒤")]
Y0 = 168
for x, (a, b) in zip(COLS, HEAD):
    d.t(x, 116, a, 12, INK, KR, "middle", 600)
    d.t(x, 134, b, 11, MUTED, KR)

ROWS = [("Eifel 탐지", "SPUR_TO"), ("F-RTO", "SPUR_TO"), ("DSACK", "LATE_SPUR_TO")]
for i, (name, grp) in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.box(LX - 8, y, W - 40 - (LX - 8), ROW_H - 8, PAPER2, RULE, 0.8, 6)
    d.t(LX + 4, y + 26, name, 13, INK, KR, "start", 600)
    d.t(LX + 4, y + 46, grp, 11, SOFT, MONO, "start")
for x in COLS:
    d.line(x, 144, x, Y0 + 3 * ROW_H - 8, RULE, 0.8, "3 5")

def bar(i, c0, c1, c, label, focal=False, lc=None):
    y = Y0 + i * ROW_H + 10
    x, w = COLS[c0], COLS[c1] - COLS[c0]
    tx = (COLS[lc] + COLS[c1]) / 2 if lc is not None else x + w / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.tone(x, y, w, BAR_H, c, 4, "14", 1.0)
    d.t(tx, y + 19, label, 12, c, MONO if all(ord(ch) < 128 for ch in label) else KR, "middle", 600)

bar(0, 0, 1, ACC, "TSecr T1 < T2", focal=True)
bar(1, 0, 2, INFO, "두 번째 ACK 도 창 전진", lc=1)
yb = Y0 + ROW_H + 10
d.line(COLS[1], yb - 4, COLS[1], yb + BAR_H + 4, INFO, 1.6)
d.t(COLS[1], yb + BAR_H + 18, "새 데이터 송신", 11, MUTED, KR)
bar(2, 0, 3, WARN, "중복 범위 보고", lc=2)

d.legend(H - 56, [("가장 이른 판정", ACC), ("ACK 진행으로 판정", INFO), ("수신자 보고로 판정", WARN)])
d.save("14-03.detection-timing.svg")
