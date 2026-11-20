# HAProxy 능동 검사와 Nginx 오픈소스 수동 판정의 동작 경로 및 상태 전이 비교.
# 타입 스펙: type-architecture
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(W, H, "02_OS / REVERSE-PROXY · 01-03",
      "능동 헬스체크와 수동 실패 감지의 상태 판정 경로",
      "HAProxy 의 주기적 프로브와 카운터 기반 상태 전이, 그리고 Nginx 오픈소스의 실제 트래픽 기반 수동 판정과 탐침 복구 메커니즘",
      lead="HAProxy 백그라운드 프로브(inter·fall·rise)와 Nginx 오픈소스 트래픽 관측(max_fails·fail_timeout)의 동작 차이")

# 2개 대구획 (좌: HAProxy 능동 검사, 우: Nginx 수동 판정)
zones = [
    {"name": "HAProxy 능동 검사 (Active Health Check)", "sub": "트래픽과 무관한 백그라운드 타이머 프로브", "x": 28, "w": 436},
    {"name": "Nginx 오픈소스 수동 판정 (Passive Detection)", "sub": "실제 클라이언트 트래픽 처리 중 실패 집계", "x": 496, "w": 436}
]

for z in zones:
    d.box(z["x"], 100, z["w"], 46, PAPER2, RULE, 1.0, 6)
    d.t(z["x"] + z["w"] / 2, 120, z["name"], 13, INK, KR, "middle", 600)
    d.t(z["x"] + z["w"] / 2, 136, z["sub"], 11, MUTED, KR, "middle")

# -------------------------------------------------------------
# 좌측: HAProxy 능동 검사 파이프라인
# -------------------------------------------------------------
# 1-1. 백그라운드 주기적 프로브
d.box(28, 160, 436, 84, PAPER2, RULE, 0.9, 6)
d.t(42, 180, "1. 백그라운드 주기적 프로브 전송", 12, INK, KR, "start", 600)
d.t(42, 198, "check inter 2000ms | option httpchk GET /healthz HTTP/1.1", 11, MUTED, MONO, "start")
d.box(40, 206, 412, 28, PAPER2, INFO, 1.0, 4)
d.t(50, 224, "L4 TCP 연결 또는 L7 HTTP 2xx/3xx 응답을 주기적으로 독립 검증", 11, INFO, KR, "start")

# 1-2. 연속 성공/실패 카운터와 상태 전이
d.box(28, 256, 436, 96, PAPER2, RULE, 0.9, 6)
d.t(42, 276, "2. 카운터 누적에 따른 UP / DOWN 전이", 12, INK, KR, "start", 600)
d.t(42, 294, "fall 3 (연속 3회 실패 시 DOWN) | rise 2 (연속 2회 성공 시 UP)", 11, MUTED, MONO, "start")
d.box(40, 302, 198, 40, PAPER2, BAD, 1.0, 4)
d.t(50, 318, "장애 발생: 3회 실패 시", 11, BAD, KR, "start", 600)
d.t(50, 334, "UP → DOWN (풀에서 제외)", 11, BAD, MONO, "start")

d.box(254, 302, 198, 40, PAPER2, OK, 1.0, 4)
d.t(264, 318, "정상 복구: 2회 성공 시", 11, OK, KR, "start", 600)
d.t(264, 334, "DOWN → UP (풀에 재투입)", 11, OK, MONO, "start")

# 1-3. 클라이언트 요청 흐름 및 영향
d.box(28, 364, 436, 84, PAPER2, RULE, 0.9, 6)
d.t(42, 384, "3. 클라이언트 트래픽 격리 및 사용자 영향", 12, INK, KR, "start", 600)
d.t(42, 402, "기본값에서 DOWN 판정까지 약 4~6초 (그 사이 요청 실패 위험)", 11, WARN, KR, "start")
d.t(42, 420, "복구 시 실제 트래픽 노출 없이 백그라운드 프로브로 사전 검증 완료", 11, OK, KR, "start", 600)

# -------------------------------------------------------------
# 우측: Nginx 오픈소스 수동 판정 파이프라인
# -------------------------------------------------------------
# 2-1. 실제 요청 중 실패 감지
d.box(496, 160, 436, 84, PAPER2, RULE, 0.9, 6)
d.t(510, 180, "1. 실제 클라이언트 요청 처리 중 실패 감지", 12, INK, KR, "start", 600)
d.t(510, 198, "proxy_next_upstream error timeout invalid_header http_500 ...", 11, MUTED, MONO, "start")
d.box(508, 206, 412, 28, PAPER2, BAD, 1.0, 4)
d.t(518, 224, "사전 프로브 없음: 실제 사용자 요청이 직접 실패를 겪어야 감지 시작", 11, BAD, KR, "start")

# 2-2. max_fails 와 fail_timeout 격리
d.box(496, 256, 436, 96, PAPER2, RULE, 0.9, 6)
d.t(510, 276, "2. 윈도우 내 실패 집계 및 일시 격리", 12, INK, KR, "start", 600)
d.t(510, 294, "server backend:8080 max_fails=1 fail_timeout=10s;", 11, MUTED, MONO, "start")
d.box(508, 302, 198, 40, PAPER2, WARN, 1.0, 4)
d.t(518, 318, "fail_timeout(10초) 동안", 11, WARN, KR, "start")
d.t(518, 334, "max_fails(1회) 도달 시 비가용", 11, WARN, MONO, "start", 600)

d.box(722, 302, 198, 40, PAPER2, ACC, 1.0, 4)
d.t(732, 318, "proxy_next_upstream:", 11, ACC, MONO, "start", 600)
d.t(732, 334, "실패 요청은 다음 서버로 우회", 11, INK, KR, "start")

# 2-3. 격리 만료 후 실 트래픽 탐침 복구
d.box(496, 364, 436, 84, PAPER2, RULE, 0.9, 6)
d.t(510, 384, "3. fail_timeout 경과 후 점진적 탐침 복구", 12, INK, KR, "start", 600)
d.t(510, 402, "10초 후 들어오는 실제 클라이언트 요청 1개를 시험 삼아 전송 (Live Probe)", 11, WARN, KR, "start")
d.t(510, 420, "성공 시 정상 가용 복귀 / 재실패 시 다시 10초 동안 비가용 격리", 11, MUTED, KR, "start")

# 연결 화살표 (두 구획 분리선)
d.line(480, 100, 480, 448, RULE, 0.8, "4 4")

# 하단 범례
d.legend(H - 44, [
    ("정상 경로 / 사전 검증 성공", OK),
    ("능동 프로브 / 상태 전이 규약", INFO),
    ("수동 판정 / 실패 집계 및 일시 격리", WARN)
])

out_path = os.path.join(os.path.dirname(__file__), "..", "01-03.chapter-overview.svg")
d.save(out_path)
print("ok generated 01-03.chapter-overview.svg")
