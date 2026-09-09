# 02-01 §7 — HTTP/2 는 악수를 차례로, HTTP/3 은 하나로 합쳐서 한다.
# 본문이 이 그림의 규격을 적어 두었다: "QUIC 는 TLS 1.3 핸드셰이크를 자기 핸드셰이크 안에 넣습니다.
# 그래서 연결 수립과 암호화 수립이 나란히 이뤄집니다. HTTP/2 때는 이 둘이 차례로 일어났습니다."
# 스트림 셋도 본문의 예 그대로다 — 1 은 HTML 기본 페이지, 2 는 CSS 객체, 3 은 이미지.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 시간 축 + 행마다 막대. 국면이 겹치는지 이어지는지가 논점.
#           축약: 원서가 이 절에 왕복 횟수를 적지 않아 눈금을 두지 않았다. 막대는 구간의 길이가 아니라
#           순서와 겹침만 나른다. 01-04 의 hop-by-hop 이 쓴 것과 같은 무눈금 관례다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 1000, 612
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §7",
      "악수 둘이 하나로 합쳐집니다",
      "HTTP/2 는 TCP 악수 뒤에 TLS 악수를 차례로 하고, HTTP/3 은 QUIC 악수가 TLS 1.3 악수를 품어 나란히 한다.",
      "눈금은 없습니다 — 막대는 순서와 겹침만 나릅니다")

LB, AXL, BARW, GAP = 24, 232, 196, 16

d.t(AXL, 100, "시간", 11, SOFT, MONO, "start")
d.line(AXL, 108, 976, 108, RULE, 0.8)

# ── HTTP/2
d.t(LB, 146, "HTTP/2", 13, INK, KR, "start", 600)
d.t(LB, 166, "TCP 위 · TLS 를 얹어서", 11, MUTED, KR, "start")
for i, (lab, sub, col) in enumerate([("연결 수립", "TCP 3-way 핸드셰이크", INFO),
                                     ("암호화 수립", "TLS 핸드셰이크", INFO),
                                     ("HTTP 요청·응답", "그다음에야 시작합니다", MUTED)]):
    x = AXL + i * (BARW + GAP)
    d.tone(x, 132, BARW, 52, col, 6, "14", 1.2)
    d.t(x + BARW / 2, 154, lab, 12, col, KR, "middle", 600)
    d.t(x + BARW / 2, 172, sub, 11, MUTED, KR)

# ── HTTP/3
d.t(LB, 248, "HTTP/3", 13, INK, KR, "start", 600)
d.t(LB, 268, "QUIC 위 · UDP 를 밑에 깔고", 11, MUTED, KR, "start")
d.tone(AXL, 226, BARW, 60, ACC, 6, "12", 1.4)
d.t(AXL + BARW / 2, 244, "QUIC 핸드셰이크", 12, ACC, KR, "middle", 600)
d.box(AXL + 12, 252, 84, 26, PAPER2, RULE, 0.9)
d.t(AXL + 54, 269, "연결 수립", 11, INK, KR)
d.box(AXL + 100, 252, 84, 26, PAPER2, RULE, 0.9)
d.t(AXL + 142, 269, "암호화 수립", 11, INK, KR)
x2 = AXL + BARW + GAP
d.tone(x2, 226, BARW, 60, MUTED, 6, "14", 1.2)
d.t(x2 + BARW / 2, 250, "HTTP 요청·응답", 12, MUTED, KR, "middle", 600)
d.t(x2 + BARW / 2, 270, "한 국면 일찍 시작합니다", 11, MUTED, KR)

d.path(f"M {AXL + BARW + GAP + BARW + 8} 256 L {AXL + 2 * (BARW + GAP) + 60} 256", SOFT, 1.2, m="soft")
d.t(AXL + 2 * (BARW + GAP) + 68, 252, "TLS 1.3 이 QUIC 안으로 들어간 만큼", 11, SOFT, KR, "start")
d.t(AXL + 2 * (BARW + GAP) + 68, 270, "국면 하나가 통째로 사라집니다", 11, SOFT, KR, "start")

# ── 스트림 다중화
d.line(24, 320, 976, 320, RULE, 0.8)
d.t(24, 346, "하나의 QUIC 연결 안에서 스트림으로 나릅니다", 13, INK, KR, "start", 600)
d.box(24, 360, 952, 96, "none", RULE, 1.0)
for i, (sid, what) in enumerate([("스트림 1", "HTML 기본 페이지"), ("스트림 2", "CSS 객체"), ("스트림 3", "이미지")]):
    bx = 44 + i * 304
    d.box(bx, 380, 288, 56, PAPER2, RULE, 0.9)
    d.t(bx + 144, 404, sid, 12, INFO, MONO, "middle", 600)
    d.t(bx + 144, 424, what, 11, MUTED, KR)
d.t(24, 480, "HTTP/3 이 QUIC API 에 지정하는 것은 연결 ID 와 스트림 ID 둘뿐입니다. "
             "암호화·프레임 분할·다중화는 그 아래에서 처리됩니다.", 11, MUTED, KR, "start")
d.t(24, 502, "그래서 HTTP/3 코드는 QUIC API 까지만 만지고 UDP 소켓 API 는 만지지 않습니다.", 11, ACC, KR, "start")

d.legend(H - 44, [("합쳐진 악수", ACC), ("차례로 하는 악수", INFO), ("데이터가 흐르는 구간", MUTED)])
d.save("02-01.quic-handshake.svg")
print("ok quic-handshake")
