# 원서 §13.7.4 — 수립 전 상태, 완료 뒤 수락 대기, 애플리케이션 수락의 경계.
# 타입 스펙: type-flowchart — 위에서 아래로 이어지는 동작 다섯 단계.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 920, 568
CW, CH, GAP, X, Y0 = 608, 60, 28, 156, 108
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-04 §2",
      "SYN부터 accept까지, 서버의 두 대기 단계",
      "SYN을 받은 뒤 SYN_RCVD 상태를 거쳐 마지막 ACK로 연결을 성립시킨다. "
      "완료된 연결은 애플리케이션이 accept를 호출할 때까지 다른 큐에서 기다린다.",
      "connect 성공과 accept 호출은 서로 다른 시점입니다")
steps = [
    ("SYN 수신", "새 연결 요청"),
    ("SYN_RCVD 큐", "수립 전 · 마지막 ACK 대기"),
    ("세 번째 ACK", "3-way handshake 완료"),
    ("accept 대기 큐", "완료 후 · 애플리케이션 수락 대기"),
    ("accept()", "애플리케이션에 연결 전달"),
]
for i, (title, sub) in enumerate(steps):
    y = Y0 + i * (CH + GAP)
    if i < len(steps)-1:
        d.arrow([(W/2, y+CH+4), (W/2, y+CH+GAP-8)], MUTED, "ar", 1.6)
    if i == 3:
        d.tone(X, y, CW, CH, ACC, 6, "12", 1.4)
    else:
        d.box(X, y, CW, CH, PAPER2, RULE, 1, 6)
    d.t(X+24, y+26, title, 15, ACC if i == 3 else INK, KR, "start", 600)
    d.t(X+24, y+48, sub, 12, MUTED, KR, "start")
d.save("13-04.server-queues.svg")
