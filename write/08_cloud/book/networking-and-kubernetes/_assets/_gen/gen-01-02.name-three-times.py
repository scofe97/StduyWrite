# 01-02 §5 — 같은 이름이 세 번 실린다. DNS 질의 · SNI · Host 헤더. 이유가 각각 다르다.
# 노트의 읽기: 2026-09-08 복습 세션에서 학습자가 직접 요청한 도식. 논지는 닭과 달걀이다 — Host 헤더는 암호문
#       안에 있어 서버가 읽으려면 복호화해야 하는데, 복호화하려면 어느 사이트의 인증서를 쓸지 먼저 정해야 한다.
#       그래서 핸드셰이크 맨 앞(ClientHello)에 이름을 평문으로 한 번 더 싣는다.
#   RFC 6066 §3 — "TLS does not provide a mechanism for a client to tell a server the name of the server it is
#       contacting.  It may be desirable for clients to provide this information to facilitate secure connections
#       to servers that host multiple 'virtual' servers at a single underlying network address."
#   본문 §5: "1단계의 네 메시지가 전부 평문입니다" · "HTTP 요청 본문은 마지막 화살표에 가서야 나갑니다".
# 타입 스펙: type-swimlane — 주체 셋(브라우저·DNS·서버)이 레인이고, 레인을 건너는 인계선이 핵심 간선이다.
#       가장 큰 결합을 만드는 인계(ClientHello 의 SNI)에만 강조색. 같은 절의 tls-handshake 는 sequence 라
#       타입이 겹치지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 616
LANES = [("브라우저", 104), ("DNS 리졸버", 200), ("서버", 296)]
LH = 96
d = D(W, H, "NETWORKING AND KUBERNETES · 01-02 §5",
      "같은 이름이 세 번 실립니다",
      "DNS 질의, TLS ClientHello 의 SNI, HTTP Host 헤더에 같은 이름이 실린다. 이유가 각각 다르고, "
      "Host 는 암호문 안에 있어 인증서를 고르려면 SNI 가 앞에 평문으로 한 번 더 필요하다.",
      "이유가 셋 다 다릅니다 — 주소를 찾으려고, 인증서를 고르려고, 가상 호스트를 고르려고")

for i, (name, y) in enumerate(LANES):
    if i % 2 == 0: d.box(24, y, W - 48, LH, "rgba(245,245,245,0.02)", "none", 0, 0)
    d.line(24, y, W - 24, y, RULE, 0.8)
    d.t(36, y + 20, name, 12, SOFT, MONO, "start")
d.line(24, LANES[-1][1] + LH, W - 24, LANES[-1][1] + LH, RULE, 0.8)

BW, BH, PITCH, BX0 = 136, 56, 148, 104
def cx(step): return BX0 + step * PITCH + BW / 2
def cy(lane): return LANES[lane][1] + LH / 2 + 8
STEPS = [  # (열, 레인, 제목, 부제, 색)
    (0, 0, "이름을 주소로 묻는다", "DNS 질의 · 평문", INFO),
    (1, 1, "주소를 돌려준다", "A 레코드 · 평문", INFO),
    (2, 0, "ClientHello", "SNI = 이름 · 평문", ACC),
    (3, 2, "인증서를 고른다", "SNI 의 이름으로", INFO),
    (4, 0, "GET / Host: 이름", "암호문 안", OK),
    (5, 2, "가상 호스트를 고른다", "Host 의 이름으로", OK),
]
for col, lane, title, sub, c in STEPS:
    x, y = cx(col) - BW / 2, cy(lane) - BH / 2
    d.tone(x, y, BW, BH, c, 6, "16" if c is ACC else "12", 1.4 if c is ACC else 1.0)
    d.t(x + BW / 2, y + 24, title, 12, c if c is ACC else INK, _kr := (KR if any("가" <= ch <= "힣" for ch in title) else MONO), "middle", 600)
    d.t(x + BW / 2, y + 42, sub, 12, MUTED, KR)

def hand(a, b, c, mk, dash=None):
    (ca, la), (cb, lb) = a, b
    x1, y1, x2, y2 = cx(ca) + BW / 2, cy(la), cx(cb) - BW / 2, cy(lb)
    mx = (x1 + x2) / 2
    d.arrow([(x1, y1), (mx, y1), (mx, y2), (x2 - 2, y2)], c, mk, 1.4, dash)
hand((0, 0), (1, 1), INFO, "info")
hand((1, 1), (2, 0), INFO, "info")
hand((2, 0), (3, 2), ACC, "acc")
hand((3, 2), (4, 0), INFO, "info", "4 4")
hand((4, 0), (5, 2), OK, "ok", "4 4")

# 닭과 달걀
CY = 428
d.tone(24, CY, W - 48, 72, ACC, 8, "0A", 1.0)
d.t(44, CY + 28, "Host 헤더는 암호문 안에 있습니다. 읽으려면 복호화해야 하고, 복호화하려면 어느 사이트의 인증서를 쓸지 먼저 정해야 합니다.",
    12, INK, KR, "start")
d.t(44, CY + 52, "그래서 핸드셰이크 맨 앞의 ClientHello 에 이름을 평문으로 한 번 더 싣습니다. 그것이 SNI 입니다.",
    12, INK, KR, "start")
d.t(24, 528, "같은 이름이 세 번 나오는데 이유가 다릅니다. DNS 는 주소를 찾으려고, SNI 는 인증서를 고르려고, Host 는 가상 호스트를 고르려고 싣습니다.",
    12, MUTED, KR, "start")

d.legend(H - 44, [("평문으로 건넌다", INFO), ("암호문 안에서 건넌다", OK), ("이름을 평문으로 한 번 더", ACC)])
d.save("01-02.name-three-times.svg")
print("ok 01-02.name-three-times")
