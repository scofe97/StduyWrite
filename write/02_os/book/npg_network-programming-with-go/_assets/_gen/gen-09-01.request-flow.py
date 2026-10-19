# 타입 스펙: type-sequence
# 09-01 요청 한 건의 실제 흐름 (서버·멀티플렉서·미들웨어·핸들러)
# 사실 출처: go1.25.1 net/http/server.go (Accept 3463, go c.serve 3493, readRequest 2031, srv.Handler 2109·3331, findHandler 2859, h.ServeHTTP 2861, finishRequest 2116), NPG 09-02 Listing 9-15
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 1000, 840
d = Seq(W, H, "NPG CH.9 §1 — REQUEST FLOW SEQUENCE",
        "요청 한 건의 실제 흐름",
        "net.Listener 수신부터 보조 기능 미들웨어와 경로 판별 멀티플렉서를 거쳐 비즈니스 로직 핸들러까지 이어집니다",
        "클라이언트 GET /hello 요청이 서버·연결 고루틴·미들웨어·멀티플렉서를 거쳐 핸들러에 도달하고 버퍼 플러시로 반환되는 전 과정")

# 1. 참여자 레인 정의 (x 좌표는 4의 배수)
y0 = 104

LX = {
    "클라이언트": 34,
    "http.Server · net.Listener": 156,
    "c.serve": 280,
    "drainAndClose": 500,
    "ServeMux": 644,
    "/hello 핸들러": 776,
}
d.LX = LX

roles = [
    ("클라이언트", "Client", 60),
    ("http.Server · net.Listener", "소켓 수신 및 서빙", 174),
    ("c.serve", "연결 고루틴", 64),
    ("drainAndClose", "보조 기능", 108),
    ("ServeMux", "경로 판별", 96),
    ("/hello 핸들러", "비즈니스 로직", 112),
]

for name, sub, w in roles:
    x = LX[name]
    d.box(x - w // 2, y0, w, 44, PAPER2, RULE, 1.0)
    is_server = (name == "http.Server · net.Listener")
    fn_size = 10.0 if is_server else (11 if name == "클라이언트" else 12)
    d.t(x, y0 + 19, name, fn_size, INK, KR if not name.startswith("c.") and not name.startswith("http.") and not name.startswith("drain") and not name.startswith("Serve") else MONO, "middle", 600)
    d.t(x, y0 + 35, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")

d.lane_top = y0 + 44

# 2. 레일
y_bot = 772
for x in LX.values():
    d.line(x, d.lane_top + 6, x, y_bot, RULE, 1.0, "3 6")

# 3. 활성화 바
d.box(LX["클라이언트"] - 4, 172, 8, 592, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["http.Server · net.Listener"] - 4, 172, 8, 56, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["c.serve"] - 4, 220, 8, 544, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["drainAndClose"] - 4, 324, 8, 356, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["ServeMux"] - 4, 380, 8, 228, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["/hello 핸들러"] - 4, 480, 8, 76, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 활성화 막대 간격에 안전하게 안착하는 호출 메시지 도우미
def call_msg(a, b, label, y, c=INFO, mk="info", sub=None, size=9.5, weight=600):
    x1, x2 = d.LX[a], d.LX[b]
    dir_sign = 1 if x2 > x1 else -1
    d.path(f"M {x1+8*dir_sign} {y} L {x2-10*dir_sign} {y}", c, 1.5, m=mk)
    mx = (x1 + x2) / 2
    d.t(mx, y - 8, label, size, c, MONO, "middle", weight)
    if sub:
        d.t(mx, y + 17, sub, 11, MUTED, KR, "middle")

# 4. 메시지 시퀀스

# 1. 클라이언트 -> Server: TCP 연결 (l.Accept)
d.msg("클라이언트", "http.Server · net.Listener", "TCP 연결", 180, c=INFO, mk="info", sub="l.Accept()")

# 2. Server -> c.serve: go c.serve(ctx)
d.msg("http.Server · net.Listener", "c.serve", "go c.serve(ctx)", 228, c=INFO, mk="info", sub="연결 고루틴 분기")

# 3. c.serve 자기 호출: c.readRequest
x_c = LX["c.serve"]
d.path(f"M {x_c+4} 268 L {x_c+28} 268 L {x_c+28} 288 L {x_c+8} 288", INFO, 1.4, m="info")
d.t(x_c + 36, 274, "c.readRequest()", 11, INFO, MONO, "start", 600)
d.t(x_c + 36, 290, "*http.Request 생성", 11, MUTED, KR, "start")

# 4. c.serve -> drainAndClose: srv.Handler.ServeHTTP(w, r) [FOCAL ACC Coral]
call_msg("c.serve", "drainAndClose", "srv.Handler.ServeHTTP(w, r)", 332, c=ACC, mk="acc", sub="서버 Handler 진입점", size=10)

# 5. drainAndClose -> ServeMux: next.ServeHTTP(w, r)
call_msg("drainAndClose", "ServeMux", "next.ServeHTTP(w, r)", 388, c=INFO, mk="info", sub="전처리 없이 전달", size=10)

# 6. ServeMux 자기 호출: findHandler
x_mux = LX["ServeMux"]
d.path(f"M {x_mux+4} 428 L {x_mux+28} 428 L {x_mux+28} 448 L {x_mux+8} 448", INFO, 1.4, m="info")
d.t(x_mux + 36, 434, "findHandler()", 11, INFO, MONO, "start", 600)
d.t(x_mux + 36, 450, "패턴 /hello 일치", 11, MUTED, KR, "start")

# 7. ServeMux -> /hello 핸들러: h.ServeHTTP(w, r)
call_msg("ServeMux", "/hello 핸들러", "h.ServeHTTP(w, r)", 488, c=INFO, mk="info", sub="핸들러 함수 실행", size=10)

# 8. /hello 핸들러 자기 호출: fmt.Fprint
x_h = LX["/hello 핸들러"]
d.path(f"M {x_h+4} 524 L {x_h+24} 524 L {x_h+24} 544 L {x_h+8} 544", OK, 1.4, m="ok")
d.t(x_h + 30, 530, 'fmt.Fprint(w, "Hello friend.")', 10, OK, MONO, "start", 600)
d.t(x_h + 30, 546, "200 OK · 본문 버퍼 기록", 11, MUTED, KR, "start")

# 9. 반환 역방향 사슬
# 9-1: /hello 핸들러 -> ServeMux
d.msg("/hello 핸들러", "ServeMux", "반환", 576, c=MUTED, mk="ar", dash="4 3")

# 9-2: ServeMux -> drainAndClose
d.msg("ServeMux", "drainAndClose", "반환", 608, c=MUTED, mk="ar", dash="4 3")

# 9-3: drainAndClose 후처리: io.Copy(io.Discard, r.Body) + r.Body.Close()
x_d = LX["drainAndClose"]
d.path(f"M {x_d-4} 636 L {x_d-24} 636 L {x_d-24} 656 L {x_d-8} 656", WARN, 1.4, m="warn")
d.t(x_d - 32, 638, "io.Copy(io.Discard, r.Body)", 10, WARN, MONO, "end", 600)
d.t(x_d - 32, 652, "r.Body.Close()", 10, WARN, MONO, "end", 600)
d.t(x_d - 32, 666, "남은 본문 비우고 닫기", 11, MUTED, KR, "end")

# 9-4: drainAndClose -> c.serve
d.msg("drainAndClose", "c.serve", "반환", 692, c=MUTED, mk="ar", dash="4 3")

# 10. c.serve 마무리 및 클라이언트 응답 전송
# 10-1: c.serve 자기 호출: w.finishRequest()
d.path(f"M {x_c+4} 718 L {x_c+28} 718 L {x_c+28} 738 L {x_c+8} 738", OK, 1.4, m="ok")
d.t(x_c + 36, 724, "w.finishRequest()", 11, OK, MONO, "start", 600)
d.t(x_c + 36, 740, "버퍼 플러시", 11, MUTED, KR, "start")

# 10-2: c.serve -> 클라이언트: 200 OK 응답
d.msg("c.serve", "클라이언트", '200 OK · "Hello friend."', 764, c=OK, mk="ok", dash="4 3", sub="응답 전송 · 연결 재사용 대기")

# 범례
d.legend(800, [
    ("동기 요청", INFO),
    ("단일 진입점 (Handler)", ACC),
    ("정상 응답 / 버퍼 기록", OK),
    ("후처리 (본문 정리)", WARN),
    ("역방향 반환", MUTED),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "09-01.request-flow.svg"))
d.save(out)
print(f"saved: {out}")
