# 사실 출처: go1.25.1 src/net/http/server.go:3433, src/net/http/server.go:1933, src/net/http/server.go:3318, src/net/http/routing_tree.go:26, go doc net/http.ServeMux
# 타입 스펙: type-sequence
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 708

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
            s.t(mx, y + 15, sub, 11, MUTED, _kr(sub), "middle")

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
    ("conn.serve", "server.go:1933"),
    ("ServeMux", "routing_tree.go"),
    ("Handler", "ServeHTTP")
], y0=96, lane_w=150)

d.rails(618)

def sec(y, txt, c):
    # 구간 제목 — 레인 점선이 글자를 관통하지 않게 불투명 밑판을 깐다
    w = sum(11 if "가" <= ch <= "힣" else 6.6 for ch in txt) + 12
    d.box(42, y - 13, w, 18, fill=PAPER, stroke=PAPER, sw=0, r=3)
    d.t(48, y, txt, 11, c, fam=KR, anchor="start", weight=600)

# 1. 연결 수락 & 고루틴 스폰
sec(153, "1. 연결 수락 및 고루틴 생성", INFO)
d.msg("클라이언트", "Server (Listener)", "TCP Connect", 181, MUTED, "ar")
d.msg("Server (Listener)", "conn.serve", "go c.serve(ctx)", 210, ACC, "acc", sub="Accept 후 전용 고루틴 스폰")

# 2. 첫 번째 요청 & 패턴 매칭
sec(247, "2. 첫 번째 요청 디스패치 (패턴 매칭)", OK)
d.msg("클라이언트", "conn.serve", "GET /items/42", 273, MUTED, "ar")
d.msg("conn.serve", "ServeMux", "ServeHTTP(w, req)", 303, MUTED, "ar")
d.msg("ServeMux", "Handler", "ServeHTTP(w, req)", 333, OK, "ok", sub="PathValue(\"id\")=\"42\" 바인딩")
d.msg("Handler", "conn.serve", "WriteHeader(200) · Write()", 383, OK, "ok", dash="4 3")
d.msg("conn.serve", "클라이언트", "HTTP/1.1 200 OK (Keep-Alive)", 413, INFO, "info", dash="4 3")

# 3. 유휴 대기 & Keep-Alive 재사용
sec(453, "3. 유휴 대기 및 동일 연결 재사용", WARN)
d.selfmsg("conn.serve", "bufr.Peek(4) 대기", 473, WARN, sub="Keep-Alive 유휴 대기")
d.msg("클라이언트", "conn.serve", "GET /health", 508, MUTED, "ar", sub="동일 TCP 소켓 재사용")
d.msg("conn.serve", "ServeMux", "ServeHTTP(w, req)", 538, MUTED, "ar")
d.msg("ServeMux", "Handler", "healthHandler.ServeHTTP()", 563, OK, "ok")
d.msg("conn.serve", "클라이언트", "HTTP/1.1 200 OK", 593, INFO, "info", dash="4 3")

# 범례
d.legend(638, [
    ("I/O 메시지", MUTED),
    ("고루틴 스폰 (focal)", ACC),
    ("라우팅·핸들러", OK),
    ("유휴 대기", WARN),
    ("응답 반환", INFO),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-01.server-mux-sequence.svg"))
d.save(out_path)
