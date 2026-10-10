# 타입 스펙: type-sequence — 정상 누적 ACK 와 악의적 수신자의 ACK 분할 공격 시 혼잡 창 팽창 비교.
# 사실 출처: ch16.txt 3093~3110행 — Savage et al. (1999) TCP Daytona, 패킷 도착 기반 cwnd 증가 취약점, ABC(RFC 3465) 방어.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 620
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-05 §4",
      "정상 누적 ACK 와 ACK 분할 공격 시 혼잡 창 변화 비교",
      "전통적 TCP 는 ACK 패킷의 도착 건수를 기준으로 cwnd 를 늘립니다. 비정상 수신자가 1500바이트 세그먼트 하나를 500바이트짜리 3개 ACK 로 쪼개어 보내면, 송신자는 패킷 3개가 온 것으로 오인하여 혼잡 창을 3배 빠르게 팽창시킵니다.",
      "세그먼트당 ACK 1개면 1 SMSS 증가하지만, 3개로 분할하면 3 SMSS 더 늘어 4 SMSS 로 폭증합니다")

# 두 패널 배치 (좌: 정상 누적 ACK, 우: ACK 분할 공격)
PW, PH = 428, 440
Y0 = 110
X_LEFT, X_RIGHT = 24, 468

# 패널 배경 상자
d.box(X_LEFT, Y0, PW, PH, PAPER2, RULE, 1.0, 8)
d.box(X_RIGHT, Y0, PW, PH, PAPER2, RULE, 1.0, 8)

# 패널 제목
d.t(X_LEFT + PW // 2, Y0 + 26, "정상 수신자 — 누적 ACK (1회 증가)", 14, OK, KR, "middle", 600)
d.t(X_RIGHT + PW // 2, Y0 + 26, "공격 수신자 — ACK 분할 (3회 급팽창)", 14, ACC, KR, "middle", 600)

# 레인 좌표
# 좌측 패널: 송신자 (x=100), 수신자 (x=370)
# 우측 패널: 송신자 (x=550), 수신자 (x=820)
LS_S, LS_R = X_LEFT + 80, X_LEFT + PW - 80
RS_S, RS_R = X_RIGHT + 80, X_RIGHT + PW - 80

# 레인 헤더
for x, name, sub in [(LS_S, "송신자", "cwnd = 1 SMSS"), (LS_R, "수신자", "정상 TCP"),
                     (RS_S, "송신자", "cwnd = 1 SMSS"), (RS_R, "공격 수신자", "TCP Daytona")]:
    d.box(x - 55, Y0 + 44, 110, 38, PAPER, RULE, 0.9, 4)
    d.t(x, Y0 + 60, name, 12, INK, KR, "middle", 600)
    d.t(x, Y0 + 74, sub, 11, MUTED, MONO if "cwnd" in sub or "Daytona" in sub else KR)
    d.line(x, Y0 + 82, x, Y0 + PH - 16, RULE, 0.8, "3 4")

# [좌측 패널] 정상 전송 흐름
# 1. 송신자가 1500B 전송
y_l1 = Y0 + 130
d.path(f"M {LS_S + 10} {y_l1} L {LS_R - 12} {y_l1}", MUTED, 1.4, m="ar")
d.t((LS_S + LS_R) / 2, y_l1 - 8, "데이터 1500B · seq 1:1500", 11, MUTED, MONO, "middle")

# 2. 수신자가 1개 ACK 회신
y_l2 = Y0 + 200
d.path(f"M {LS_R - 10} {y_l2} L {LS_S + 12} {y_l2}", OK, 1.4, m="ok", dash="4 3")
d.t((LS_S + LS_R) / 2, y_l2 - 8, "누적 ACK · ack 1501", 11, OK, MONO, "middle")
d.t((LS_S + LS_R) / 2, y_l2 + 16, "1500바이트 전체 확인", 11, MUTED, KR, "middle")

# 3. 송신자 cwnd 갱신
y_l3 = Y0 + 280
d.chip(LS_S, y_l3, "cwnd: 1 → 2 SMSS", OK, 11)
d.t(LS_S + 14, y_l3 + 26, "정상 느린 시작 (+1 SMSS)", 11, OK, KR, "start")

d.box(X_LEFT + 24, Y0 + PH - 64, PW - 48, 44, PAPER, OK, 0.8, 4)
d.t(X_LEFT + PW // 2, Y0 + PH - 44, "정상 동작: 왕복 1회당 1 SMSS 증가", 11, OK, KR, "middle", 600)
d.t(X_LEFT + PW // 2, Y0 + PH - 28, "도착한 ACK 패킷 수 = 1", 11, MUTED, KR, "middle")


# [우측 패널] ACK 분할 공격 흐름
# 1. 동일한 1500B 전송
y_r1 = Y0 + 130
d.path(f"M {RS_S + 10} {y_r1} L {RS_R - 12} {y_r1}", MUTED, 1.4, m="ar")
d.t((RS_S + RS_R) / 2, y_r1 - 8, "데이터 1500B · seq 1:1500", 11, MUTED, MONO, "middle")

# 2. 공격자가 3개로 분할된 마이크로 ACK 송신 (화살촉 가림 방지를 위해 cwnd 칩을 송신자 레일 왼쪽에 배치)
y_r2 = Y0 + 185
d.path(f"M {RS_R - 10} {y_r2} L {RS_S + 8} {y_r2}", ACC, 1.4, m="acc", dash="4 3")
d.t((RS_S + RS_R) / 2, y_r2 - 8, "분할 ACK 1 · ack 501", 11, ACC, MONO, "middle")
d.chip(RS_S - 40, y_r2, "cwnd += 1", WARN, 11)

y_r3 = Y0 + 235
d.path(f"M {RS_R - 10} {y_r3} L {RS_S + 8} {y_r3}", ACC, 1.4, m="acc", dash="4 3")
d.t((RS_S + RS_R) / 2, y_r3 - 8, "분할 ACK 2 · ack 1001", 11, ACC, MONO, "middle")
d.chip(RS_S - 40, y_r3, "cwnd += 1", WARN, 11)

y_r4 = Y0 + 285
d.path(f"M {RS_R - 10} {y_r4} L {RS_S + 8} {y_r4}", ACC, 1.4, m="acc", dash="4 3")
d.t((RS_S + RS_R) / 2, y_r4 - 8, "분할 ACK 3 · ack 1501", 11, ACC, MONO, "middle")
d.chip(RS_S - 40, y_r4, "cwnd += 1", WARN, 11)

# 3. 송신자 cwnd 최종 상태
y_r5 = Y0 + 338
d.chip(RS_S, y_r5, "cwnd: 1 → 4 SMSS", BAD, 11)
d.t(RS_S + 20, y_r5 + 24, "패킷 3개로 오인해 +3 폭증", 11, BAD, KR, "middle")

# 우측 하단 방어 요약 상자
d.box(X_RIGHT + 24, Y0 + PH - 64, PW - 48, 44, PAPER, INFO, 0.8, 4)
d.t(X_RIGHT + PW // 2, Y0 + PH - 44, "방어책: ABC (RFC 3465 바이트 계수)", 11, INFO, KR, "middle", 600)
d.t(X_RIGHT + PW // 2, Y0 + PH - 28, "확인된 바이트 합산(1500B)으로 1 SMSS 만 증가", 11, MUTED, KR, "middle")

d.legend(H - 48, [
    ("정상 누적 ACK", OK),
    ("분할된 마이크로 ACK", ACC),
    ("비정상 cwnd 폭증", BAD),
    ("바이트 계수 방어 (ABC)", INFO),
])

d.save("16-05.ack-division-attack.svg")
