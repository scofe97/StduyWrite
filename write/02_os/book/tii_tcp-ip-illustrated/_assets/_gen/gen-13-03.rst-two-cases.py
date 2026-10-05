# 13-03 §5 — 원서 Listing 13-5(닫힌 포트) 와 Listing 13-6(연결 중단) 의 RST 를 나란히.
# 사실 출처: 원서 §13.6.1–13.6.2(PDF 41–45쪽).
#   Listing 13-5: 127.0.0.1.32803 > 127.0.0.1.9999 S 3357881819:3357881819(0) / 9999 > 32803 R 0:0(0) ack 3357881820.
#     들어온 SYN 에 ACK 비트가 없으므로 RST 의 순서 번호는 0, ACK 번호는 ISN + 0 + 1(SYN). Telnet 은 Connection refused.
#   Listing 13-6: 192.168.10.140.2788 > 192.168.10.144.ssh 3-way handshake 뒤 (인증·대량 전송 생략),
#     사용자가 ^C(SIGINT) → 클라이언트가 R 1343:1343(0) ack 132929. 상대는 RST 에 응답하지 않는다.
#     원서는 abortive release 를 만드는 API 로 SO_LINGER(linger 0) 를 들지만, ssh 가 그 옵션을 썼다고는 말하지 않는다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지를 두 판으로 나란히 놓는다.
#           축약: 오른쪽 판의 인증·대량 전송 구간은 원서처럼 생략 표시 한 줄로 줄인다.
#           focal 은 오른쪽 판의 RST 한 줄 — 수립된 연결의 데이터와 상태를 버리는 중단.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 920, 560
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-03 §5",
      "같은 RST, 다른 사건 — 닫힌 포트와 연결 중단",
      "왼쪽은 원서 Listing 13-5 로, 듣는 프로세스가 없는 9999번 포트로 간 SYN 에 RST 가 즉시 돌아온다. 들어온 SYN 에 ACK 비트가 없어 RST 의 순서 번호는 0 이고 "
      "ACK 번호는 ISN 3357881819 에 SYN 의 1 을 더한 3357881820 이다. 오른쪽은 원서 Listing 13-6 으로, 수립된 ssh 연결에서 사용자가 ^C 로 중단하자 "
      "클라이언트가 FIN 대신 RST 를 보내고 상대는 그 RST 에 아무 응답도 하지 않는다.",
      "왼쪽은 수립 전의 거부, 오른쪽은 수립 뒤의 중단입니다")

PW = 424
Y_HEAD, Y_LANE, Y_BOT = 100, 116, 468
LW = 128

def lanes(px, title, left, right):
    lx, rx = px + 80, px + PW - 80
    d.t(px + PW / 2, Y_HEAD, title, 13, INK, KR, "middle", 600)
    for x, (nm, sub) in ((lx, left), (rx, right)):
        d.box(x - LW / 2, Y_LANE, LW, 44, PAPER2, RULE, 1.0, 6)
        d.t(x, Y_LANE + 19, nm, 12, INK, KR, "middle", 600)
        d.t(x, Y_LANE + 36, sub, 11, MUTED, _kr(sub))
        d.line(x, Y_LANE + 50, x, Y_BOT, RULE, 1.0, "3 6")
    return lx, rx

def msg(x1, x2, y, label, c, mk, sub=None, dash=None, sw=1.5):
    dd = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 8 * dd} {y} L {x2 - 10 * dd} {y}", c, sw, m=mk, dash=dash)
    d.t((x1 + x2) / 2, y - 9, label, 12, c, _kr(label), "middle", 600)
    if sub: d.t((x1 + x2) / 2, y + 17, sub, 11, MUTED, _kr(sub))

# 왼쪽 — Listing 13-5
lx, rx = lanes(24, "닫힌 포트 · Listing 13-5", ("Telnet", ":32803"), ("듣는 쪽 없음", ":9999"))
msg(lx, rx, 216, "SYN 3357881819", INFO, "info", sub="ACK 비트 없음")
msg(rx, lx, 280, "RST 0 · ack 3357881820", BAD, "bad", sub="ISN + 1")
d.chip(lx + 4, 352, "Connection refused", BAD, 12)
d.t(px_c := 24 + PW / 2, 404, "connect() 실패", 13, MUTED, KR, "middle", 600)
d.t(px_c, 444, "연결 수립 전", 12, SOFT, KR, "middle")

# 오른쪽 — Listing 13-6
lx2, rx2 = lanes(472, "연결 중단 · Listing 13-6", ("ssh 클라이언트", ":2788"), ("sshd", ":22"))
msg(lx2, rx2, 196, "SYN", INFO, "info")
msg(rx2, lx2, 228, "SYN, ACK", OK, "ok")
msg(lx2, rx2, 260, "ACK", MUTED, "ar")
d.t(472 + PW / 2, 300, "… 인증 · 대량 전송 생략 …", 11, SOFT, KR, "middle")
d.t(lx2 - 12, 344, "^C", 13, WARN, MONO, "end", 700)
msg(lx2, rx2, 344, "RST 1343 · ack 132929", ACC, "acc", sub="tcpdump 상대 번호", sw=1.8)
d.chip(472 + PW / 2, 404, "응답 없음 · 연결 버림", MUTED, 12)
d.t(472 + PW / 2, 444, "수립된 연결의 중단", 12, SOFT, KR, "middle")

d.line(W / 2, 88, W / 2, Y_BOT, RULE, 0.8)
d.legend(H - 56, [("수립 뒤 중단", ACC), ("거부 RST", BAD), ("SYN", INFO), ("^C", WARN)])
d.save("13-03.rst-two-cases.svg")
