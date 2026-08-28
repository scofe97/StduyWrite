# 00-03-dns-first — 이름을 IP 로 바꾸는 조회가 연결보다 먼저다
# 본문 요구: "이름으로는 아무것도 보낼 수 없다" — IP 헤더에 이름 칸이 없으므로 조회가 선행한다.
#           IP 를 실제로 받아 오는 3 단계가 이 도식의 초점이다.
# 타입 스펙: type-data-flow.md — 이름에서 연결까지 네 단계가 한 줄로 이어진다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER2, KR, MONO

W, H = 1000, 360
X0, BW, BH, STRIDE, BY = 12, 200, 88, 232, 152
STEPS = [("01", "이름을 친다", "example.com", False),
         ("02", "DNS 에 묻는다", "DHCP 가 준 서버", False),
         ("03", "IP 를 받는다", "93.184.216.34", True),
         ("04", "그제야 연결", "TCP 핸드셰이크", False)]

d = D(W, H, "PROCESS · NAME BEFORE CONNECT",
      "이름으로는 아무것도 보낼 수 없다",
      "이름을 IP 로 바꾸는 조회가 실제 연결보다 먼저 일어난다는 것을 네 단계 가로 절차로 보인 도식.",
      lead="IP 헤더에는 이름을 적을 칸이 없습니다. 그래서 연결보다 조회가 먼저입니다.")

for i, (no, title, sub, focal) in enumerate(STEPS):
    x = 60 + i * STRIDE
    if focal:
        d.tone(x, BY, BW, BH, ACC, 6, "12", 1.2)
    else:
        d.box(x, BY, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, BY + 26, no, 8, SOFT, MONO, "start")
    d.t(x + 16, BY + 50, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, BY + 72, ddx.fit(sub, 11, BW - 32, sub), 11, ACC if focal else MUTED,
        MONO if all(ord(c) < 128 or c in '.' for c in sub) else KR, "start")
    if i < 3:
        d.path(f"M {x + BW + 4} {BY + BH // 2} L {x + STRIDE - 8} {BY + BH // 2}", MUTED, 1.4, m="ar")

d.t(X0, 284, "조회가 실패하면 뒤의 모든 것이 시작조차 못 합니다. 연결이 안 될 때 여기부터 보는 이유입니다.", 12, MUTED, KR, "start")
d.legend(300, [("조회 단계", MUTED), ("주소를 실제로 얻는 자리", ACC)])
d.save("00-03-dns-first.svg")
print("ok dns-first")
