# 클라이언트에서 CDN, 사내 프록시(Nginx/HAProxy), 백엔드로 이어지는 헤더 누적과 신뢰 경계.
# 타입 스펙: type-architecture
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER2, RULE, KR, MONO

W, H = 960, 500
d = D(W, H, "02_OS / REVERSE-PROXY · 01-01",
      "프록시 체인의 헤더 전달과 신뢰 경계",
      "클라이언트가 보낸 위조 헤더와 프록시가 덧붙인 헤더를 구분하고 신뢰 경계로 실제 클라이언트 IP 를 판별한다.",
      lead="위조 가능 구간(외부)과 신뢰 검증 구간(사내 프록시), 그리고 안전하게 전달받는 백엔드 애플리케이션")

# 4개 열(zone) 배치
cols = [
    {"name": "클라이언트 (외부)", "ip": "IP: 203.0.113.195", "x": 32, "w": 184},
    {"name": "외부 프록시 / CDN", "ip": "IP: 192.0.2.1", "x": 248, "w": 204},
    {"name": "사내 프록시 (Nginx/HAProxy)", "ip": "IP: 10.0.0.0/8", "x": 484, "w": 252},
    {"name": "백엔드 애플리케이션", "ip": "app1.example.com:8080", "x": 768, "w": 160}
]

# 상단 호스트 박스들
for c in cols:
    d.box(c["x"], 104, c["w"], 54, PAPER2, RULE, 1.0, 6)
    d.t(c["x"] + c["w"] / 2, 126, c["name"], 13, INK, KR, "middle", 600)
    d.t(c["x"] + c["w"] / 2, 146, c["ip"], 11, MUTED, MONO, "middle")

# 상단 연결 화살표 (요청 전달 홉)
for i in range(3):
    x1 = cols[i]["x"] + cols[i]["w"]
    x2 = cols[i + 1]["x"]
    d.arrow([(x1 + 4, 131), (x2 - 4, 131)], MUTED, "ar", 1.2)

# 신뢰 경계 박스 (사내 프록시부터 백엔드까지)
d.box(472, 176, 464, 252, PAPER2, OK, 1.2, 8)
d.t(488, 198, "[ 신뢰 경계 (Trust Boundary) ]", 12, OK, MONO, "start", 600)
d.t(488, 216, "set_real_ip_from 192.0.2.0/24 — 앞단 CDN 을 신뢰로 등록", 11, MUTED, KR, "start")

# 1열: 클라이언트 행동 (외부 위조)
d.box(32, 176, 184, 114, PAPER2, RULE, 0.9, 6)
d.t(44, 198, "임의 조작 가능 헤더", 12, BAD, KR, "start", 600)
d.box(42, 210, 164, 68, PAPER2, BAD, 1.0, 4)
d.t(50, 232, "X-Forwarded-For:", 11, MUTED, MONO, "start")
d.t(50, 252, "198.51.100.1 (스푸핑)", 11, BAD, MONO, "start", 600)

# 2열: 외부 CDN 동작
d.box(248, 176, 204, 114, PAPER2, RULE, 0.9, 6)
d.t(260, 198, "직전 홉 IP 덧붙임", 12, INK, KR, "start", 600)
d.box(258, 210, 184, 68, PAPER2, RULE, 0.9, 4)
d.t(266, 232, "X-Forwarded-For 누적:", 11, MUTED, MONO, "start")
d.t(266, 252, "198.51.100.1,", 11, MUTED, MONO, "start")
d.t(266, 268, "203.0.113.195", 11, INK, MONO, "start", 600)

# 3열: 사내 프록시 내부 검증 (§1, §2, §3)
d.box(478, 230, 240, 186, PAPER2, RULE, 1.0, 6)
d.t(496, 252, "Nginx / HAProxy 헤더 제어", 12, ACC, KR, "start", 600)
d.t(496, 272, "§1 상속 단절 주의 (proxy_set_header)", 11, INK, KR, "start")
d.t(496, 290, "§2 덮어쓰기 (http-request set-header)", 11, INK, KR, "start")
d.t(496, 310, "§3 real_ip_recursive on 역탐색", 11, OK, KR, "start", 600)

# 역탐색 시각화 박스
d.box(488, 320, 220, 84, PAPER2, OK, 1.0, 4)
d.t(502, 340, "연결 주소 192.0.2.1 = 신뢰 CDN", 11, MUTED, KR, "start")
d.t(502, 360, "헤더 우측부터: 203.0.113.195", 11, MUTED, KR, "start")
d.t(502, 382, "→ 첫 비신뢰 주소, 실제 IP 확정", 11, OK, KR, "start", 600)

# 4열: 백엔드 수신 결과
d.box(768, 230, 154, 186, PAPER2, RULE, 1.0, 6)
d.t(780, 252, "백엔드 확정 정보", 12, OK, KR, "start", 600)
d.t(780, 278, "Remote IP:", 11, MUTED, MONO, "start")
d.t(780, 298, "203.0.113.195", 11, OK, MONO, "start", 600)
d.t(780, 328, "Proto:", 11, MUTED, MONO, "start")
d.t(780, 348, "HTTPS (ssl_fc)", 11, OK, MONO, "start", 600)
d.t(780, 378, "Host: 원래 호스트", 11, INK, KR, "start")

# 하단 연결 화살표 흐름
d.arrow([(216, 233), (248, 233)], MUTED, "ar", 1.2)
d.arrow([(452, 233), (484, 233)], MUTED, "ar", 1.2)
d.arrow([(712, 323), (764, 323)], OK, "ok", 1.4)

# 범례
d.legend(H - 44, [
    ("외부 위조 / 스푸핑 위험", BAD),
    ("신뢰 경계 / 확정된 실제 클라이언트 IP", OK),
    ("프록시 설정 및 헤더 조작 규약", ACC)
])

out_path = os.path.join(os.path.dirname(__file__), "..", "01-01.chapter-overview.svg")
d.save(out_path)
print("ok generated 01-01.chapter-overview.svg")
