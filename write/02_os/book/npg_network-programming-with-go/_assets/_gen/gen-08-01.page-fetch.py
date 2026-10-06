# 타입 스펙: type-tree — 루트 HTML 요청에서 브라우저가 파싱한 4개 자원 요청으로 갈라지는 트리 구조.
# 사실 출처: NPG Ch.8 From Request to Rendered Page (p.7)
# 실제 값: woodbeck.net 상의 /, main.min.css, code.css, avatar.jpeg, favicon.ico 요청 결과
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, MONO, KR

W, H = 840, 400
d = D(W, H, "NPG CHAPTER 8 · FROM REQUEST TO RENDERED PAGE",
      "단일 HTML 요청에서 부속 자원으로 뻗는 트리와 지속 연결",
      "HTML 수신 후 브라우저가 CSS·이미지 등 4개 부속 자원을 요청하며, HTTP/1.1 은 동일한 TCP 연결을 재사용한다.",
      "한 페이지 요청의 실제 값: 상태 코드(200·304·404)와 전송 바이트, 소요 시간")

# 1. 단일 TCP 연결 외곽 상자
TX, TY, TW, TH = 24, 98, 792, 224
d.box(TX, TY, TW, TH, PAPER2, RULE, 1.0, 8)
d.t(TX + 16, TY + 22, "같은 TCP 연결 · HTTP/1.1", 11, INFO, KR, "start", 600)

# 2. 트리 연결선 (노드보다 먼저 그림)
# 루트 중심: x=420, y=190
# 버스 Y: y=210
# 각 자식 중심: 132, 324, 516, 708
d.line(420, 190, 420, 210, MUTED, 1.2)
d.line(132, 210, 708, 210, MUTED, 1.2)
for cx in [132, 324, 516, 708]:
    d.path(f"M {cx} 210 L {cx} 230", MUTED, 1.2, m="ar")

# 3. 루트 노드 (HTML 요청) - ACC
RX, RY, RW, RH = 310, 126, 220, 64
d.tone(RX, RY, RW, RH, ACC, 6, "18", 1.4)
d.t(RX + RW / 2, RY + 22, "GET / (HTML)", 12, ACC, KR, "middle", 600)
d.t(RX + RW / 2, RY + 40, "woodbeck.net · 200 OK", 11, OK, MONO, "middle")
d.t(RX + RW / 2, RY + 55, "1.83KB · 49 ms", 11, INK, MONO, "middle")

# 4. 자식 노드 4개 (부속 자원 요청)
CW, CH, CY = 172, 64, 232
kids = [
    (46, 132, "GET main.min.css", "CSS · 200 OK", "1.30KB · 20 ms", OK),
    (238, 324, "GET code.css", "CSS · 200 OK", "0.99KB · 20 ms", OK),
    (430, 516, "GET avatar.jpeg", "JPEG · 304 Not Modified", "0 bytes · 0 ms (캐시)", WARN),
    (622, 708, "GET favicon.ico", "IMG · 404 Not Found", "0 bytes · 0 ms (미발견)", BAD),
]

for x, cx, req, status, stat, col in kids:
    d.tone(x, CY, CW, CH, col, 6, "14", 1.1)
    d.t(cx, CY + 20, req, 11, INK, MONO, "middle", 600)
    d.t(cx, CY + 38, status, 11, col, MONO, "middle")
    d.t(cx, CY + 54, stat, 11, col, KR, "middle")

# 5. 범례
d.legend(350, [("루트 (HTML)", ACC), ("200 OK", OK), ("304 캐시", WARN), ("404 없음", BAD), ("지속 연결", INFO)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "08-01.page-fetch.svg"))
d.save(out)
print(f"saved: {out}")
