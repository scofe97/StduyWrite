# 타입 스펙: type-sequence
# 사실 출처: NPG Ch.10 Listing 10-1 (Posting configuration), Listing 10-2 (Adding test server in real time), p.4-8
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 520
d = Seq(W, H, "NPG CH.10 — ADMIN API CONFIG RELOAD SEQUENCE",
        "관리 API 를 통한 실시간 무중단 설정 변경 시퀀스",
        "재시작 없이 포트 2019 로 새 JSON 을 전송하여 소켓 리스너를 교체합니다",
        "atomic 교체 검증, 새 포트 바인드, 기존 연결 보존과 즉각 서빙")

# 1. 참여자 레인 정의
y0 = 104
lane_w = 170

LX = {
    "관리자 (curl)": 110,
    "관리 API (:2019)": 350,
    "Caddy 런타임 코어": 600,
    "웹 클라이언트": 845,
}
d.LX = LX

roles = [
    ("관리자 (curl)", "Admin / CI·CD"),
    ("관리 API (:2019)", "localhost:2019"),
    ("Caddy 런타임 코어", "Server Engine"),
    ("웹 클라이언트", "Browser / Client"),
]

for name, sub in roles:
    x = LX[name]
    d.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
    d.t(x, y0 + 19, name, 12, INK, KR, "middle", 600)
    d.t(x, y0 + 35, sub, 10, MUTED, MONO, "middle")

d.lane_top = y0 + 44

# 2. 레일
y_bot = 460
for x in LX.values():
    d.line(x, d.lane_top + 6, x, y_bot, RULE, 1.0, "3 6")

# 3. 활성화 바
d.box(LX["관리자 (curl)"] - 4, 165, 8, 160, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["관리 API (:2019)"] - 4, 165, 8, 160, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["Caddy 런타임 코어"] - 4, 210, 8, 235, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["웹 클라이언트"] - 4, 370, 8, 65, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 4. 메시지 시퀀스
# 4-1: curl -> 관리 API: POST /load
d.msg("관리자 (curl)", "관리 API (:2019)", "POST /load (JSON)", 175, c=INFO, mk="info", sub="apps.http.servers.hello")

# 4-2: 관리 API -> Caddy 런타임: 새 설정 로드 및 프로비저닝
d.msg("관리 API (:2019)", "Caddy 런타임 코어", "새 설정 로드 및 검증", 225, c=ACC, mk="acc", sub="Provisioner & Validator 실행")

# 4-3: Caddy 런타임 자체 동작: net.Listen 소켓 바인드
d.path(f"M {LX['Caddy 런타임 코어']+4} 260 L {LX['Caddy 런타임 코어']+42} 260 L {LX['Caddy 런타임 코어']+42} 280 L {LX['Caddy 런타임 코어']+8} 280", ACC, 1.4, m="acc")
d.t(LX["Caddy 런타임 코어"] + 50, 266, "새 리스너 소켓 바인드", 11, ACC, KR, "start", 600)
d.t(LX["Caddy 런타임 코어"] + 50, 282, "net.Listen tcp :2020", 11, MUTED, MONO, "start")

# 4-4: 관리 API -> curl: 200 OK
d.msg("관리 API (:2019)", "관리자 (curl)", "200 OK 응답", 320, c=OK, mk="ok", dash="4 3", sub="무중단 교체 완료")

# 4-5: 웹 클라이언트 -> Caddy 런타임: GET localhost:2020
d.msg("웹 클라이언트", "Caddy 런타임 코어", "GET / (포트 2020)", 380, c=WARN, mk="warn", sub="새 hello 서버 요청")

# 4-6: Caddy 런타임 -> 웹 클라이언트: 200 OK
d.msg("Caddy 런타임 코어", "웹 클라이언트", "200 OK (Hello, world!)", 430, c=OK, mk="ok", dash="4 3", sub="static_response 본문 반환")

# 범례
d.legend(480, [
    ("관리 API (포트 2019)", INFO),
    ("설정 교체 (내부)", ACC),
    ("정상 응답 (200)", OK),
    ("서비스 트래픽", WARN),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "10-01.admin-api-sequence.svg"))
d.save(out)
print(f"saved: {out}")
