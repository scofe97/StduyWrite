# 본문 요구: ## 3. DefaultTransport 기본값 읽기 요약 바로 아래 지도. "DefaultTransport 필드는 무엇을 재고 세느냐로 세 묶음이고, 개수 묶음의 둘은 리터럴에 없어 0 의 뜻으로 정해진다"가 한눈에.
# 타입 스펙: type-nested
# 사실 출처: go1.25.1 src/net/http/transport.go:45-56, src/net/http/transport.go:60, src/net/http/transport.go:1040-1045, src/net/http/transport.go:1568, src/net/tcpsock.go:136-148, src/net/dial.go:171-190
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 552

d = D(W, H,
      "HTTP DEFAULTTRANSPORT FIELD MAP",
      "DefaultTransport 필드 분류와 기본값",
      "DefaultTransport 필드는 시간을 잰다, 개수를 센다, 길과 프로토콜을 정한다의 세 묶음이며 개수 묶음의 둘은 리터럴에 없어 0 의 기본 동작으로 정해진다",
      "시간·개수·경로 세 묶음으로 나뉘며 개수 묶음의 둘은 리터럴에 없어 0 의 뜻으로 결정됩니다")

# 바깥 상자: DefaultTransport (*Transport)
RX, RY, RW, RH = 24, 100, 912, 388
d.box(RX, RY, RW, RH, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(RX + 20, RY + 24, "DefaultTransport (*Transport)", 13, INK, fam=MONO, anchor="start", weight=600)
d.t(RX + RW - 20, RY + 24, "net/http/transport.go:45-56", 11, SOFT, fam=MONO, anchor="end")

# 왼쪽 묶음: 시간을 잰다 (5개 필드)
T_X, T_Y, T_W, T_H = 44, 136, 424, 336
d.box(T_X, T_Y, T_W, T_H, fill=PAPER, stroke=INFO, sw=1.0, r=6)
d.t(T_X + 16, T_Y + 22, "시간을 잰다 (타임아웃 · 주기 5개)", 12, INFO, fam=KR, anchor="start", weight=600)
d.line(T_X + 16, T_Y + 34, T_X + T_W - 16, T_Y + 34, RULE, 0.7)

time_fields = [
    ("Dialer.Timeout", "30s", "소켓 연결 수립 제한"),
    ("TLSHandshakeTimeout", "10s", "TLS 핸드셰이크 제한"),
    ("ExpectContinueTimeout", "1s", "100-continue 응답 대기"),
    ("IdleConnTimeout", "90s", "유휴 연결 보관 후 폐기"),
    ("Dialer.KeepAlive", "30s", "TCP keepalive 유휴 탐침 시작"),
]

for i, (name, val, desc) in enumerate(time_fields):
    cy = 178 + i * 58
    d.box(T_X + 16, cy, T_W - 32, 50, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
    d.t(T_X + 28, cy + 21, name, 12, INK, fam=MONO, anchor="start", weight=600)
    d.t(T_X + T_W - 28, cy + 21, val, 12, INFO, fam=MONO, anchor="end", weight=600)
    d.t(T_X + 28, cy + 39, desc, 11, SOFT, fam=KR, anchor="start")

# 오른쪽 위 묶음: 개수를 센다 (3개 필드 · focal)
C_X, C_Y, C_W, C_H = 492, 136, 424, 208
d.box(C_X, C_Y, C_W, C_H, fill=PAPER, stroke=ACC, sw=1.2, r=6)
d.t(C_X + 16, C_Y + 22, "개수를 센다 (연결 한도 3개 · focal)", 12, ACC, fam=KR, anchor="start", weight=600)
d.line(C_X + 16, C_Y + 34, C_X + C_W - 16, C_Y + 34, RULE, 0.7)

# MaxIdleConns (명시적 리터럴)
d.box(C_X + 16, 178, C_W - 32, 48, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(C_X + 28, 199, "MaxIdleConns", 12, INK, fam=MONO, anchor="start", weight=600)
d.t(C_X + C_W - 28, 199, "100 (빈 연결, 전 호스트)", 11, INK, fam=KR, anchor="end", weight=600)
d.t(C_X + 28, 216, "전체 호스트 유휴 연결 총합", 11, SOFT, fam=KR, anchor="start")

# MaxIdleConnsPerHost (focal 1)
d.o.append(f'<rect x="{C_X + 16}" y="234" width="{C_W - 32}" height="48" rx="4" fill="{ACC}14" stroke="{ACC}" stroke-width="1.3" stroke-dasharray="4 3"/>')
d.t(C_X + 28, 255, "MaxIdleConnsPerHost", 12, ACC, fam=MONO, anchor="start", weight=600)
d.t(C_X + C_W - 28, 255, "리터럴에 없음 → 0 → 2", 11, ACC, fam=KR, anchor="end", weight=600)
d.t(C_X + 28, 272, "호스트당 기본 2개 보관 (focal)", 11, ACC, fam=KR, anchor="start")

# MaxConnsPerHost (focal 2)
d.o.append(f'<rect x="{C_X + 16}" y="290" width="{C_W - 32}" height="48" rx="4" fill="{ACC}14" stroke="{ACC}" stroke-width="1.3" stroke-dasharray="4 3"/>')
d.t(C_X + 28, 311, "MaxConnsPerHost", 12, ACC, fam=MONO, anchor="start", weight=600)
d.t(C_X + C_W - 28, 311, "리터럴에 없음 → 0 → 무제한", 11, ACC, fam=KR, anchor="end", weight=600)
d.t(C_X + 28, 328, "호스트당 총 연결 제한 없음 (focal)", 11, ACC, fam=KR, anchor="start")

# 오른쪽 아래 묶음: 길과 프로토콜을 정한다 (2개 필드)
P_X, P_Y, P_W, P_H = 492, 356, 424, 116
d.box(P_X, P_Y, P_W, P_H, fill=PAPER, stroke=OK, sw=1.0, r=6)
d.t(P_X + 16, P_Y + 22, "길과 프로토콜을 정한다 (2개)", 12, OK, fam=KR, anchor="start", weight=600)
d.line(P_X + 16, P_Y + 34, P_X + P_W - 16, P_Y + 34, RULE, 0.7)

proto_fields = [
    ("Proxy", "ProxyFromEnvironment", "환경변수 프록시 자동 탐색"),
    ("ForceAttemptHTTP2", "true", "HTTP/2 연결 자동 협상"),
]

for i, (name, val, desc) in enumerate(proto_fields):
    cy = 396 + i * 36
    d.box(P_X + 16, cy, P_W - 32, 30, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
    d.t(P_X + 28, cy + 20, name, 12, INK, fam=MONO, anchor="start", weight=600)
    d.t(P_X + P_W - 28, cy + 20, val, 12, OK, fam=MONO, anchor="end", weight=600)

# 범례
d.legend(504, [
    ("리터럴 없음 0 대체 (focal)", ACC),
    ("시간 설정 (타임아웃 · 주기)", INFO),
    ("경로 및 프로토콜 설정", OK),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01.dt-field-map.svg"))
d.save(out_path)
