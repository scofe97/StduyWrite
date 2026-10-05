# 원서 §13.8 — 서버가 SYN 수신 시 상태를 쌓지 않고 마지막 ACK에서 복원하는 경계.
# 타입 스펙: type-flowchart — 위에서 아래로 이어지는 동작 네 단계.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, PAPER2, RULE, KR

W, H = 920, 492
CW, CH, GAP, X, Y0 = 608, 60, 32, 156, 104
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-04 §3",
      "SYN cookie는 마지막 ACK까지 상태 할당을 미룬다",
      "서버는 SYN에 응답하면서 연결별 상태 대신 복원 가능한 ISN을 보낸다. "
      "마지막 ACK가 돌아오면 cookie를 검증하고 연결 상태를 만든다.",
      "수립 전 상태를 순서 번호에 담아 SYN flood 압박을 줄입니다")
steps = [
    ("SYN 수신", "아직 연결별 상태 없음"),
    ("cookie ISN으로 SYN + ACK", "시간 · MSS · 4-tuple 해시 인코딩"),
    ("마지막 ACK 수신", "서버 ISN + 1을 돌려받음"),
    ("cookie 검증 · 상태 할당", "유효한 요청을 ESTABLISHED로 전환"),
]
for i, (title, sub) in enumerate(steps):
    y = Y0 + i * (CH + GAP)
    if i < len(steps)-1:
        d.arrow([(W/2, y+CH+4), (W/2, y+CH+GAP-8)], MUTED, "ar", 1.6)
    if i == 1:
        d.tone(X, y, CW, CH, ACC, 6, "12", 1.4)
    else:
        d.box(X, y, CW, CH, PAPER2, RULE, 1, 6)
    d.t(X+24, y+26, title, 15, ACC if i == 1 else INK, KR, "start", 600)
    d.t(X+24, y+48, sub, 12, MUTED, KR, "start")
d.save("13-04.syn-cookie.svg")
