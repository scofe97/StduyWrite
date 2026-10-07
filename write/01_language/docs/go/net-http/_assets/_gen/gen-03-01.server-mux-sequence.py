# 사실 출처: go1.25.1 src/net/http/server.go:3433, src/net/http/server.go:1930, src/net/http/server.go:3318, src/net/http/routing_tree.go:21, go doc net/http.ServeMux
# 타입 스펙: type-sequence
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 680

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub), "middle")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        fam = _kr(txt)
        w = len(str(txt)) * (10.0 if fam == KR else 6.5) + 16
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 10, c, fam)

d = SeqKR(W, H,
          "HTTP SERVER DISPATCH AND SERVEMUX ROUTING",
          "Server 연결 수락과 ServeMux 라우팅 시퀀스",
          "Server.Serve 의 Accept 루프부터 conn.serve 고루틴 스폰, 패턴 매칭, Keep-Alive 재사용 흐름",
          "Server 는 연결마다 고루틴을 띄우고 conn.serve 는 동일 TCP 소켓으로 후속 요청을 이어 처리합니다")

lanes = d.lanes([
    ("클라이언트", "HTTP Client"),
    ("Server (Listener)", "server.go:Serve"),
    ("conn.serve", "server.go:1930"),
    ("ServeMux", "routing_tree.go"),
    ("Handler", "ServeHTTP")
], y0=96, lane_w=150)

d.rails(590)

# 1. 연결 수락 & 고루틴 스폰
d.t(48, 155, "1. 연결 수락 및 고루틴 생성", 10, INFO, fam=KR, anchor="start", weight=600)
d.msg("클라이언트", "Server (Listener)", "TCP Connect", 175, MUTED, "ar")
d.msg("Server (Listener)", "conn.serve", "go c.serve(ctx)", 205, ACC, "acc", sub="Accept 후 전용 고루틴 스폰")

# 2. 첫 번째 요청 & 패턴 매칭
d.t(48, 245, "2. 첫 번째 요청 디스패치 (패턴 매칭)", 10, OK, fam=KR, anchor="start", weight=600)
d.msg("클라이언트", "conn.serve", "GET /items/42", 265, MUTED, "ar")
d.msg("conn.serve", "ServeMux", "ServeHTTP(w, req)", 295, MUTED, "ar")
d.msg("ServeMux", "Handler", "ServeHTTP(w, req)", 325, OK, "ok", sub="PathValue(\"id\")=\"42\" 바인딩")
d.msg("Handler", "conn.serve", "WriteHeader(200) · Write()", 355, OK, "ok", dash="4 3")
d.msg("conn.serve", "클라이언트", "HTTP/1.1 200 OK (Keep-Alive)", 385, INFO, "info", dash="4 3")

# 3. 유휴 대기 & Keep-Alive 재사용
d.t(48, 425, "3. 유휴 대기 및 동일 연결 재사용", 10, WARN, fam=KR, anchor="start", weight=600)
d.selfmsg("conn.serve", "bufr.Peek(4) 대기", 445, WARN, sub="Keep-Alive 유휴 대기")
d.msg("클라이언트", "conn.serve", "GET /health", 480, MUTED, "ar", sub="동일 TCP 소켓 재사용")
d.msg("conn.serve", "ServeMux", "ServeHTTP(w, req)", 510, MUTED, "ar")
d.msg("ServeMux", "Handler", "healthHandler.ServeHTTP()", 535, OK, "ok")
d.msg("conn.serve", "클라이언트", "HTTP/1.1 200 OK", 565, INFO, "info", dash="4 3")

# 범례
d.legend(610, [
    ("네트워크 I/O 메시지", MUTED),
    ("고루틴 스폰 (focal)", ACC),
    ("라우팅 및 핸들러 처리", OK),
    ("Keep-Alive 유휴 대기", WARN),
    ("응답 반환", INFO),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-01.server-mux-sequence.svg"))
d.save(out_path)
