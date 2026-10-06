# 타입 스펙: type-sequence
# 09-02 HTTP/2 서버 푸시 프레임 교환 시퀀스와 브라우저 지원 현황
# 사실 출처: NPG Ch.9 Listing 9-17 (index.html, style.css, hiking.svg), Listing 9-19 (http.Pusher Push)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 640
d = Seq(W, H, "NPG CH.9 — HTTP/2 SERVER PUSH SEQUENCE",
        "HTTP/2 서버 푸시 프레임 교환과 브라우저 지원 현황",
        "서버가 클라이언트의 후속 요청 전에 자원을 미리 밀어 넣는 절차입니다",
        "PUSH_PROMISE 약속, 병렬 스트림 자원 전송, 현대 브라우저 제거 현황")

# 1. 참여자 레인 수동 배치 (우측 상태 카드 공간 확보)
y0 = 104
lane_w = 200
bx = 160  # 웹 브라우저 중심 x
sx = 490  # Go 서버 중심 x

d.LX = {"웹 브라우저": bx, "Go HTTP/2 서버": sx}

# 레인 상자
d.box(bx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(bx, y0 + 19, "웹 브라우저", 12, INK, KR, "middle", 600)
d.t(bx, y0 + 35, "Client / Chrome·Firefox", 10, MUTED, MONO, "middle")

d.box(sx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(sx, y0 + 19, "Go HTTP/2 서버", 12, INK, KR, "middle", 600)
d.t(sx, y0 + 35, "Server / http.Pusher", 10, MUTED, MONO, "middle")

d.lane_top = y0 + 44

# 2. 레일
y_bot = 550
d.line(bx, d.lane_top + 6, bx, y_bot, RULE, 1.0, "3 6")
d.line(sx, d.lane_top + 6, sx, y_bot, RULE, 1.0, "3 6")

# 3. 활성화 바 (Activation Bar)
d.box(bx - 4, 168, 8, 358, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(sx - 4, 168, 8, 358, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 4. 시퀀스 메시지
# 4-1: 브라우저 -> 서버: GET /
d.msg("웹 브라우저", "Go HTTP/2 서버", "GET / (Stream 1)", 168, c=INFO, mk="info", sub="HEADERS frame (HTML 요청)")

# 4-2: 서버 내부 동작: Pusher 확인
# selfmsg: x+10 to x+46
d.path(f"M {sx+4} 208 L {sx+42} 208 L {sx+42} 224 L {sx+8} 224", MUTED, 1.4, m="ar")
d.t(sx + 50, 212, "w.(http.Pusher) 확인", 11, MUTED, KR, "start", 600)
d.t(sx + 50, 228, "푸시 대상 목록 준비", 11, SOFT, KR, "start")

# 4-3: 서버 -> 브라우저: PUSH_PROMISE (/static/style.css)
d.msg("Go HTTP/2 서버", "웹 브라우저", "PUSH_PROMISE (Stream 1 → 2)", 270, c=WARN, mk="warn", dash="4 3", sub="약속 경로: /static/style.css")

# 4-4: 서버 -> 브라우저: PUSH_PROMISE (/static/hiking.svg)
d.msg("Go HTTP/2 서버", "웹 브라우저", "PUSH_PROMISE (Stream 1 → 4)", 330, c=WARN, mk="warn", dash="4 3", sub="약속 경로: /static/hiking.svg")

# 4-5: 서버 -> 브라우저: style.css 전송
d.msg("Go HTTP/2 서버", "웹 브라우저", "HEADERS + DATA (Stream 2)", 390, c=MUTED, mk="ar", sub="/static/style.css 전송")

# 4-6: 서버 -> 브라우저: hiking.svg 전송
d.msg("Go HTTP/2 서버", "웹 브라우저", "HEADERS + DATA (Stream 4)", 450, c=MUTED, mk="ar", sub="/static/hiking.svg 전송")

# 4-7: 서버 -> 브라우저: index.html 응답 완료
d.msg("Go HTTP/2 서버", "웹 브라우저", "200 OK (Stream 1)", 510, c=OK, mk="ok", sub="index.html 응답 본문 전송")

# 5. 브라우저 생태계 퇴출 현황 카드 (우측 독립 영역, x=670~930)
cx, cy, cw, ch = 672, 170, 258, 204
d.tone(cx, cy, cw, ch, BAD, op="14", sw=1.2)
d.t(cx + cw / 2, cy + 26, "브라우저 생태계 현황", 12, BAD, KR, "middle", 600)

d.chip(cx + cw / 2, cy + 58, "Chrome 106 기본 비활성", BAD, 11)
d.chip(cx + cw / 2, cy + 92, "Firefox 132 완전 제거", BAD, 11)

d.t(cx + cw / 2, cy + 130, "중복 전송 · 캐시 비효율", 11, MUTED, KR, "middle")
d.t(cx + cw / 2, cy + 152, "대안: 103 Early Hints", 11, INFO, KR, "middle", 600)
d.t(cx + cw / 2, cy + 174, "대안: <link rel=preload>", 11, INFO, KR, "middle", 600)

# 6. 범례
d.legend(574, [
    ("클라이언트 요청", INFO),
    ("서버 푸시 약속", WARN),
    ("데이터 스트림 / 응답", OK),
    ("브라우저 제거 상태", BAD),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "09-02.server-push.svg")
d.save(out_path)
print("saved:", out_path)
