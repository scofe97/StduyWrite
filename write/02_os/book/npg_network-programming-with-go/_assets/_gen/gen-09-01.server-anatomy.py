# 타입 스펙: type-architecture
# 09-01 Go HTTP 서버 구조와 요청 처리 흐름
# 사실 출처: NPG Ch.9 Listing 9-1 (Server/TimeoutHandler/DefaultHandler), Listing 9-2 (세 가지 테스트 케이스)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 500
d = D(W, H, "NPG CH.9 — SERVER ANATOMY",
      "Go HTTP 서버 구조와 요청 처리 흐름",
      "Listing 9-1 의 서버 구성과 Listing 9-2 의 세 가지 테스트 요청 처리 경로",
      "멀티플렉서 없이 TimeoutHandler 미들웨어가 DefaultHandler 를 직접 감싸는 구조")

# 1. Background Zones
# Zone 1: Client Tier (x=20..296)
d.box(20, 100, 276, 330, fill=PAPER2, stroke=RULE, sw=0.8, r=8)
d.t(32, 122, "CLIENT TIER (Listing 9-2·9-3)", 8, SOFT, MONO, "start", 600)

# Zone 2: HTTP Server (x=360..860)
d.box(360, 100, 500, 330, fill=PAPER2, stroke=RULE, sw=0.8, r=8)
d.t(376, 122, "HTTP SERVER (Listing 9-1: 127.0.0.1:8081)", 8, SOFT, MONO, "start", 600)

# 2. Arrows (Drawn before boxes for z-order)
# (1) Client -> net.Listener in gap x=288..370
d.line(288, 170, 366, 170, c=INFO, sw=1.4)
d.path("M 358 166 L 366 170 L 358 174 Z", c=INFO, sw=1.0)
d.t(328, 158, "요청 전달", 12, INFO, KR, "middle")

# (2) net.Listener -> srv.Serve(l)
d.line(474, 170, 486, 170, c=INFO, sw=1.4)
d.path("M 480 166 L 488 170 L 480 174 Z", c=INFO, sw=1.0)

# (3) srv.Serve(l) -> TimeoutHandler
d.line(594, 170, 606, 170, c=INFO, sw=1.4)
d.path("M 600 166 L 608 170 L 600 174 Z", c=INFO, sw=1.0)

# (4) TimeoutHandler -> DefaultHandler
d.line(726, 170, 738, 170, c=INFO, sw=1.4)
d.path("M 732 166 L 740 170 L 732 174 Z", c=INFO, sw=1.0)

# (5) DefaultHandler -> ResponseWriter (L-bend orthogonal path: down then left)
# Exits bottom center of DefaultHandler (794, 204) -> turns at (794, 290) -> enters right side of ResponseWriter (726, 290)
d.path("M 794 204 V 282 Q 794 290 786 290 H 734", c=OK, sw=1.4)
d.path("M 740 286 L 732 290 L 740 294 Z", c=OK, sw=1.0)
d.t(758, 278, "w.Write()", 10, OK, MONO, "middle", 600)

# (6) ResponseWriter -> Response Output (straight left)
d.line(610, 290, 598, 290, c=OK, sw=1.4)
d.path("M 604 286 L 596 290 L 604 294 Z", c=OK, sw=1.0)

# (7) Response Output -> Client Test Cases in gap x=490..288 (straight left)
d.line(490, 290, 294, 290, c=OK, sw=1.4)
d.path("M 302 286 L 294 290 L 302 294 Z", c=OK, sw=1.0)
d.t(328, 278, "응답 반환", 12, OK, KR, "middle")

# 3. Component Boxes
# Client Tier - Top Client Box
d.box(30, 136, 258, 46, fill=PAPER2, stroke=INFO, sw=1.1)
d.t(159, 156, "http.Client", 11, INK, MONO, "middle", 600)
d.t(159, 172, "client.Do(r)", 10, MUTED, MONO, "middle")

# Client Tier - 3 Test Cases (Listing 9-2)
# Case 1: GET
d.box(30, 194, 258, 66, fill=PAPER2, stroke=OK, sw=1.0)
d.t(38, 214, "Case 1: GET /", 11, INFO, MONO, "start", 600)
d.t(38, 234, '200 OK · "Hello, friend!"', 12, OK, KR, "start")
d.t(38, 250, "기본 본문 반환 검증", 12, MUTED, KR, "start")

# Case 2: POST
d.box(30, 270, 258, 66, fill=PAPER2, stroke=OK, sw=1.0)
d.t(38, 290, 'Case 2: POST / ("<world>")', 11, INFO, MONO, "start", 600)
d.t(38, 310, '200 OK · "Hello, &lt;world&gt;!"', 12, OK, KR, "start")
d.t(38, 326, "HTML 이스케이프 검증", 12, MUTED, KR, "start")

# Case 3: HEAD
d.box(30, 346, 258, 66, fill=PAPER2, stroke=WARN, sw=1.0)
d.t(38, 366, "Case 3: HEAD /", 11, WARN, MONO, "start", 600)
d.t(38, 386, "405 Method Not Allowed", 12, WARN, KR, "start")
d.t(38, 402, "미지원 메서드 빈 본문 검증", 12, MUTED, KR, "start")

# Server Tier - Top Row
d.box(370, 136, 104, 68, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(422, 161, "net.Listener", 11, INK, MONO, "middle", 600)
d.t(422, 183, "8081 포트 수신", 12, MUTED, KR, "middle")

d.box(490, 136, 104, 68, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(542, 161, "srv.Serve(l)", 11, INK, MONO, "middle", 600)
d.t(542, 183, "고루틴 서빙 루프", 12, MUTED, KR, "middle")

d.box(610, 136, 116, 68, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(668, 161, "TimeoutHandler", 11, INK, MONO, "middle", 600)
d.t(668, 183, "미들웨어 (2분)", 12, MUTED, KR, "middle")

# Focal Node: DefaultHandler (ACC Coral tone)
d.tone(742, 136, 104, 68, ACC, op="20", sw=1.4)
d.t(794, 161, "DefaultHandler", 11, ACC, MONO, "middle", 600)
d.t(794, 183, "ServeHTTP", 11, INK, MONO, "middle")

# Server Tier - Bottom Row
d.box(610, 256, 116, 68, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(668, 281, "ResponseWriter", 11, INK, MONO, "middle", 600)
d.t(668, 303, "응답 스트림 작성", 12, MUTED, KR, "middle")

d.box(490, 256, 104, 68, fill=PAPER2, stroke=OK, sw=1.1)
d.t(542, 281, "HTTP Response", 11, OK, MONO, "middle", 600)
d.t(542, 303, "상태·헤더·본문", 12, INK, KR, "middle")

# 4. Legend
d.legend(455, [
    ("핵심 핸들러", ACC),
    ("테스트 요청", INFO),
    ("정상 응답 (200)", OK),
    ("미지원 거부 (405)", WARN),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "09-01.server-anatomy.svg"))
d.save(out)
print(f"saved: {out}")
