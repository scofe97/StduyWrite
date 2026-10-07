# 사실 출처: go1.25.1 src/net/http/client.go:586, src/net/http/transport.go:530, src/net/http/server.go:3433, src/net/http/server.go:2109
# 타입 스펙: type-layers
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520

d = D(W, H,
      "HTTP CLIENT AND SERVER ABSTRACTION LAYERS",
      "클라이언트와 서버의 계층 구조와 책임 분리",
      "Client·Transport 에서 Dialer 로 내려가는 발신 계층과 Server·Listener 에서 Handler 로 올라가는 수신 계층",
      "클라이언트는 연결을 재사용하고 서버는 연결마다 conn.serve 고루틴을 띄워 독립 처리합니다")

COL_W = 424
C1_X = 36
C2_X = 500

# 좌측 컬럼 헤더: HTTP Client
d.box(C1_X, 94, COL_W, 30, fill=PAPER2, stroke=INFO, sw=1.0, r=4)
d.t(C1_X + COL_W // 2, 114, "HTTP 클라이언트 파이프라인 (발신)", 12, INFO, fam=KR, weight=600)

# 우측 컬럼 헤더: HTTP Server
d.box(C2_X, 94, COL_W, 30, fill=PAPER2, stroke=OK, sw=1.0, r=4)
d.t(C2_X + COL_W // 2, 114, "HTTP 서버 파이프라인 (수신)", 12, OK, fam=KR, weight=600)

client_layers = [
    ("C1", "http.Client", "요청 오케스트레이션", "Do() · 리다이렉트 · 쿠키", PAPER2, RULE, INK, False),
    ("C2", "*http.Transport", "RoundTripper 풀링", "RoundTrip() · 연결 풀링", f"{ACC}14", ACC, ACC, True),
    ("C3", "net.Dialer", "전송 계층 연결", "DialContext() · 소켓 생성", PAPER2, RULE, INK, False),
    ("C4", "net.Conn", "소켓 바이트 스트림", "Read() · Write() 스트림", PAPER2, RULE, INK, False),
]

server_layers = [
    ("S1", "http.Handler", "애플리케이션 로직", "ServeHTTP() · 경로 라우팅", PAPER2, RULE, INK, False),
    ("S2", "conn.serve()", "연결당 전용 고루틴", "HTTP 파싱 · 패닉 격리", f"{ACC}14", ACC, ACC, True),
    ("S3", "net.Listener", "네트워크 리스너", "Accept() · 연결 수락", PAPER2, RULE, INK, False),
    ("S4", "net.Conn", "소켓 바이트 스트림", "Read() · Write() 스트림", PAPER2, RULE, INK, False),
]

y0 = 138
h_box = 62
gap = 14

for i, (tag, name, role, note, fill, stroke, text_col, focal) in enumerate(client_layers):
    y = y0 + i * (h_box + gap)
    sw = 1.4 if focal else 1.0
    d.box(C1_X, y, COL_W, h_box, fill=fill, stroke=stroke, sw=sw, r=6)
    d.box(C1_X + 12, y + 18, 30, 22, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(C1_X + 27, y + 33, tag, 10, stroke if focal else SOFT, fam=MONO, weight=600)
    d.t(C1_X + 52, y + 34, name, 13, text_col, fam=MONO, anchor="start", weight=600)
    d.chip(C1_X + 224, y + 30, role, stroke if focal else MUTED, size=10)
    d.t(C1_X + COL_W - 14, y + 34, note, 10, INK if focal else SOFT, fam=KR, anchor="end")
    if i < 3:
        d.arrow([(C1_X + COL_W // 2, y + h_box + 2), (C1_X + COL_W // 2, y + h_box + gap - 2)],
                c=ACC if i == 1 else MUTED, m="acc" if i == 1 else "ar", sw=1.1)

for i, (tag, name, role, note, fill, stroke, text_col, focal) in enumerate(server_layers):
    # 서버는 물리(하단)에서 애플리케이션(상단)으로 올라감
    y = y0 + (3 - i) * (h_box + gap)
    sw = 1.4 if focal else 1.0
    d.box(C2_X, y, COL_W, h_box, fill=fill, stroke=stroke, sw=sw, r=6)
    d.box(C2_X + 12, y + 18, 30, 22, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(C2_X + 27, y + 33, tag, 10, stroke if focal else SOFT, fam=MONO, weight=600)
    d.t(C2_X + 52, y + 34, name, 13, text_col, fam=MONO, anchor="start", weight=600)
    d.chip(C2_X + 224, y + 30, role, stroke if focal else MUTED, size=10)
    d.t(C2_X + COL_W - 14, y + 34, note, 10, INK if focal else SOFT, fam=KR, anchor="end")
    if i < 3:
        prev_y = y0 + (3 - i) * (h_box + gap)
        next_y = y0 + (2 - i) * (h_box + gap)
        d.arrow([(C2_X + COL_W // 2, prev_y - 2), (C2_X + COL_W // 2, next_y + h_box + 2)],
                c=ACC if i == 1 else MUTED, m="acc" if i == 1 else "ar", sw=1.1)

# 하단 연결선: C4 net.Conn <---> S4 net.Conn (TCP 통신)
y_bottom_wire = y0 + 3 * (h_box + gap) + h_box // 2
d.line(C1_X + COL_W, y_bottom_wire, C2_X, y_bottom_wire, RULE, 1.0, "3 3")
d.t((C1_X + COL_W + C2_X) // 2, y_bottom_wire - 6, "TCP 소켓 연결", 10, SOFT, fam=KR, anchor="middle")

# 범례
d.legend(466, [
    ("기본 구성 요소", MUTED),
    ("클라이언트 발신 파이프라인", INFO),
    ("서버 수신 파이프라인", OK),
    ("핵심 처리 계층 (focal)", ACC),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-01.client-server-layers.svg"))
d.save(out_path)
