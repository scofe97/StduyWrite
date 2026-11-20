# 클라이언트 요청 크기·시간 제약과 업스트림 응답 기한의 상태 코드 분기.
# 타입 스펙: type-architecture
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(W, H, "02_OS / REVERSE-PROXY · 01-02",
      "업스트림 기한과 요청 제한의 상태 코드 결정 경로",
      "클라이언트 전송 제한과 업스트림 통신 기한이 413, 408, 502, 504 상태 코드로 분기되는 경로",
      lead="클라이언트 유입 단계(크기·시간)와 업스트림 단계(연결·응답)별 프록시의 타임아웃 판정 및 상태 코드 매핑")

# 3개 대구획 (클라이언트 전송, 프록시 제어, 업스트림 및 상태 코드)
zones = [
    {"name": "클라이언트 요청 유입", "sub": "요청 크기 및 전송 간격 감시", "x": 28, "w": 272},
    {"name": "리버스 프록시 제어 (Nginx / HAProxy)", "sub": "버퍼링·업스트림 파이프라인", "x": 324, "w": 312},
    {"name": "업스트림 백엔드 및 상태 코드", "sub": "연결 상태 및 응답 기한 판정", "x": 660, "w": 272}
]

for z in zones:
    d.box(z["x"], 100, z["w"], 46, PAPER2, RULE, 1.0, 6)
    d.t(z["x"] + z["w"] / 2, 120, z["name"], 13, INK, KR, "middle", 600)
    d.t(z["x"] + z["w"] / 2, 136, z["sub"], 11, MUTED, KR, "middle")

# 1열: 클라이언트 전송 단계 검증 박스들
# 1-1. 본문 크기 초과 -> 413
d.box(28, 160, 272, 84, PAPER2, RULE, 0.9, 6)
d.t(40, 180, "요청 본문 크기 검증", 12, INK, KR, "start", 600)
d.t(40, 198, "Nginx: client_max_body_size (1MB)", 11, MUTED, MONO, "start")
d.box(40, 206, 248, 28, PAPER2, WARN, 1.0, 4)
d.t(50, 224, "한도 초과: 413 Content Too Large", 11, WARN, MONO, "start", 600)

# 1-2. 메모리 버퍼링 (디스크 임시 파일)
d.box(28, 256, 272, 84, PAPER2, RULE, 0.9, 6)
d.t(40, 276, "메모리 버퍼링 및 임시 파일", 12, INK, KR, "start", 600)
d.t(40, 294, "client_body_buffer_size (8k/16k)", 11, MUTED, MONO, "start")
d.box(40, 302, 248, 28, PAPER2, RULE, 1.0, 4)
d.t(50, 320, "버퍼 초과: 디스크 임시 파일 기록", 11, MUTED, KR, "start")

# 1-3. 전송 시간 지연 -> 408
d.box(28, 352, 272, 94, PAPER2, RULE, 0.9, 6)
d.t(40, 372, "클라이언트 무활동 전송 지연", 12, INK, KR, "start", 600)
d.t(40, 390, "client_header / body_timeout (60s)", 11, MUTED, MONO, "start")
d.t(40, 406, "HAProxy: timeout http-request (cR)", 11, MUTED, MONO, "start")
d.box(40, 412, 248, 26, PAPER2, WARN, 1.0, 4)
d.t(50, 429, "무활동 초과: 408 Request Timeout", 11, WARN, MONO, "start", 600)

# 2열: 프록시 코어 및 업스트림 파이프라인
d.box(324, 160, 312, 286, PAPER2, RULE, 1.0, 6)
d.t(340, 182, "업스트림 통신 제어 파이프라인", 12, ACC, KR, "start", 600)

# 2열 상단: 연결 수립
d.box(336, 196, 288, 64, PAPER2, RULE, 0.9, 4)
d.t(348, 216, "1단계: TCP 연결 수립 (Handshake)", 11, INK, KR, "start", 600)
d.t(348, 234, "Nginx: proxy_connect_timeout (60s)", 11, MUTED, MONO, "start")
d.t(348, 250, "HAProxy: timeout connect", 11, MUTED, MONO, "start")

# 2열 중단: 응답 수신
d.box(336, 270, 288, 76, PAPER2, RULE, 0.9, 4)
d.t(348, 290, "2단계: 응답 수신 (헤더 전 초과만 504)", 11, INK, KR, "start", 600)
d.t(348, 308, "Nginx: proxy_read_timeout (60s)", 11, MUTED, MONO, "start")
d.t(348, 324, "HAProxy: timeout server", 11, MUTED, MONO, "start")
d.t(348, 338, "ngx_http_upstream_next 재시도 판단", 11, SOFT, KR, "start")

# 2열 하단: 페일오버 및 최종 확정
d.box(336, 356, 288, 78, PAPER2, ACC, 1.0, 4)
d.t(348, 376, "3단계: 다음 서버 재시도 또는 확정", 11, ACC, KR, "start", 600)
d.t(348, 394, "proxy_next_upstream error timeout", 11, MUTED, MONO, "start")
d.t(348, 412, "시도 소진: 최종 상태 코드 반환", 11, INK, KR, "start")
d.t(348, 426, "HAProxy 종료 상태: sH, sC", 11, SOFT, MONO, "start")

# 3열: 업스트림 장애 상태 및 생성 코드
# 3-1. 502 Bad Gateway
d.box(660, 160, 272, 84, PAPER2, RULE, 0.9, 6)
d.t(672, 180, "즉각 연결 거부 및 비정상 응답", 12, BAD, KR, "start", 600)
d.t(672, 198, "Connection Refused, TCP RST, 헤더 오류", 11, MUTED, KR, "start")
d.box(672, 206, 248, 28, PAPER2, BAD, 1.0, 4)
d.t(682, 224, "프록시 생성: 502 Bad Gateway", 11, BAD, MONO, "start", 600)

# 3-2. 504 Gateway Timeout
d.box(660, 256, 272, 102, PAPER2, RULE, 0.9, 6)
d.t(672, 276, "연결·응답 헤더 기한 초과", 12, BAD, KR, "start", 600)
d.t(672, 294, "Nginx: connect·read 기한 초과", 11, MUTED, KR, "start")
d.t(672, 310, "HAProxy: sH → 504, sC → 503/504", 11, MUTED, MONO, "start")
d.box(672, 318, 248, 28, PAPER2, BAD, 1.0, 4)
d.t(682, 336, "프록시 생성: 504 Gateway Timeout", 11, BAD, MONO, "start", 600)

# 3-3. 200 OK
d.box(660, 370, 272, 76, PAPER2, RULE, 0.9, 6)
d.t(672, 390, "기한 내 정상 응답 도착", 12, OK, KR, "start", 600)
d.t(672, 408, "HTTP/1.1 200 OK 헤더 및 본문 수신", 11, MUTED, MONO, "start")
d.box(672, 414, 248, 24, PAPER2, OK, 1.0, 4)
d.t(682, 430, "클라이언트 전달: 200 OK", 11, OK, MONO, "start", 600)

# 연결 화살표
# 1열 -> 2열
d.arrow([(300, 298), (324, 298)], MUTED, "ar", 1.2)
# 2열 -> 3열 연결 시도
d.arrow([(636, 202), (660, 202)], BAD, "bad", 1.2)
# 2열 -> 3열 응답 지연 504
d.arrow([(636, 307), (660, 307)], BAD, "bad", 1.2)
# 2열 -> 3열 정상 응답
d.arrow([(636, 408), (660, 408)], OK, "ok", 1.2)

# 범례 (3개 항목으로 폭 960 이내 유지)
d.legend(H - 42, [
    ("클라이언트 전송 제한 (413, 408)", WARN),
    ("업스트림 통신 장애 (502, 504)", BAD),
    ("정상 응답 전달 (200 OK)", OK)
])

out_path = os.path.join(os.path.dirname(__file__), "..", "01-02.chapter-overview.svg")
d.save(out_path)
print("ok generated 01-02.chapter-overview.svg")
