# 05-03 실습 편 전체 지도 — 세 묶음이 05-01·05-02 의 어느 절을 실습으로 옮기는지. 타입 스펙: type-flowchart.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, PAPER2, RULE, KR, MONO
W, H = 880, 500
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-03",
      "실습 편 — 세 묶음이 옮기는 것",
      "묶음 A 는 05-01 의 네 걸음을, 묶음 B 는 05-01 의 어긋남·확인·릴레이를, 묶음 C 는 05-02 의 이름과 요청을 컨테이너에서 다시 잡는다. 한 세션에 한 묶음이다.",
      "위 줄이 노트의 절, 아래 줄이 그 절을 옮긴 묶음입니다")
CW, CH, GAP, X0 = 256, 92, 32, 24
notes = [("05-01 §1~§4", "네 걸음 · 두 걸음", "SARR · DORA · rapid commit"),
         ("05-01 §5~§7", "예약 아님 · 두 확인 · 릴레이", "NAK · ICMP·ARP · giaddr"),
         ("05-02 §1~§4", "이름과 요청", "DNS · http.time · 재조립 · CONNECT")]
bund = [("묶음 A", "주소를 받는 네 걸음", "A1~A5", False),
        ("묶음 B", "어긋나는 경우들", "B1~B5", True),
        ("묶음 C", "이름과 요청", "C1~C8", False)]
Y1, Y2 = 112, 292
for i, ((sec, t, sub), (b, bt, rng, focal)) in enumerate(zip(notes, bund)):
    x = X0 + i * (CW + GAP)
    d.box(x, Y1, CW, CH, PAPER2, RULE, 1, 8)
    d.t(x + CW / 2, Y1 + 26, sec, 12, MUTED, MONO)
    d.t(x + CW / 2, Y1 + 52, t, 15, INK, KR, "middle", 600)
    d.t(x + CW / 2, Y1 + 76, sub, 12, MUTED, KR)
    col = ACC if focal else INK
    d.box(x, Y2, CW, CH, PAPER2, ACC if focal else RULE, 1.4 if focal else 1, 8)
    d.t(x + CW / 2, Y2 + 26, rng, 12, MUTED, MONO)
    d.t(x + CW / 2, Y2 + 52, b + " · " + bt, 15, col, KR, "middle", 600)
    d.t(x + CW / 2, Y2 + 76, "한 세션", 12, MUTED, KR)
    d.arrow([(x + CW / 2, Y1 + CH + 4), (x + CW / 2, Y2 - 4)], MUTED, "ar", 1.4)
    if i < 2:
        d.arrow([(x + CW + 4, Y2 + CH / 2), (x + CW + GAP - 4, Y2 + CH / 2)], MUTED, "ar", 1.4)
d.t(X0, Y2 + CH + 36, "잘못 알던 인과 둘 — B2 (REQUEST 뒤 바로 써도 된다) · C4 (느린 요청은 SYN·ACK 간격)", 12, MUTED, KR, "start")
d.legend(H - 44, [("잘못 알던 인과가 몰린 묶음", ACC)])
d.save("05-03.chapter-overview.svg")
