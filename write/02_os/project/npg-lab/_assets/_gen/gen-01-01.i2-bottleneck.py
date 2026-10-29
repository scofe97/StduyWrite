# 01-01-i2-bottleneck — 프록시–백엔드 빈 연결 보관 시간 불일치와 재시도 분기를 보인 I2 병목 지도
# 본문 요구(01-01 근본 원인): 프록시(90s)와 백엔드(1s)의 빈 연결 보관 시간 불일치, readLoop 감지와 shouldRetryRequest 재시도 분기 메커니즘을 보인다.
# 타입 스펙: type-architecture
# 사실 출처: ch08-server-idle-close-post-502.md:28-31,39,83-93,102-105,111,116,123-128, fakeinv/main.go:85-86,376, transport.go:808-852,1009-1013,2431, request.go:1534, server.go:3040-3044
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, KR, MONO

W = 960
H = 504

d = D(
    W,
    H,
    "ARCHITECTURE · CH08 I2 BOTTLENECK",
    "I2 병목 지도: 양쪽 보관 시간 90s·1s, 풀의 readLoop, GET 만 다시 보내는 자리",
    "프록시 IdleConnTimeout 90s와 백엔드 idle_close 1s 불일치, readLoop EOF 감지, shouldRetryRequest 재시도 분기",
    lead="서버의 선행 단절과 프록시의 보관 시간 불일치, GET 재전송과 POST 502 분기 구조"
)

def dash_box(d, x, y, w, h, fill=PAPER2, stroke=RULE, sw=0.9, r=6, dash="4 3"):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')

# 상단 구분선
d.line(24, 92, 936, 92, RULE, 0.8)

# 1. Zone 배경 (Client, Proxy, Backend)
ZY = 108
ZH = 332

# Zone 0: 손님 (npgload)
d.box(24, ZY, 192, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(36, 130, "손님 npgload", 13, INK, KR, "start", 600)

# Zone 0 내부 상자들
# Box 1: 부하 생성
d.box(36, 148, 168, 64, PAPER2, RULE, 0.9, 6)
d.t(120, 174, "POST 1/s · GET 1/s", 12, INK, MONO, "middle", 600)
d.t(120, 196, "poisson 10분", 12, MUTED, KR, "middle")

# Box 2: GET 결과 관측
d.tone(36, 224, 168, 64, OK, 6, "12", 1.0)
d.t(120, 250, "GET 0 / 1,199", 13, OK, MONO, "middle", 600)
d.t(120, 272, "단건 조회 성공", 12, OK, KR, "middle", 600)

# Box 3: POST 502 관측
d.tone(36, 300, 168, 80, WARN, 6, "12", 1.0)
d.t(120, 324, "POST 56 / 1,206", 13, WARN, MONO, "middle", 600)
d.t(120, 346, "502 flags=UC", 12, WARN, MONO, "middle", 600)
d.t(120, 366, "idle 807~973ms", 11, MUTED, MONO, "middle")

# Zone 0 → Zone 1 연결선
d.arrow([(204, 180), (248, 180)], c=MUTED, m="ar", sw=1.3)
d.t(226, 170, "HTTP", 11, MUTED, MONO, "middle")

# Zone 1 → Zone 0 (502 응답)
d.arrow([(248, 346), (204, 346)], c=WARN, m="warn", sw=1.3)
d.t(226, 336, "502", 11, WARN, MONO, "middle")

# Zone 1: 프록시 (npgproxy v0)
d.box(248, ZY, 352, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(260, 130, "프록시 npgproxy v0", 13, INK, KR, "start", 600)
d.t(588, 130, "DefaultTransport", 11, MUTED, MONO, "end")

# Zone 1 상단: 빈 연결 풀
d.box(260, 148, 328, 76, PAPER2, RULE, 0.9, 6)
d.t(272, 166, "빈 연결 풀", 12, INK, KR, "start", 600)
d.t(576, 166, "IdleConnTimeout 90s", 12, MUTED, MONO, "end")

# 풀 내부 연결 슬롯
d.box(272, 176, 144, 38, fill="#11161D", stroke=RULE, sw=0.8, r=4)
d.t(344, 200, "conn 1 [readLoop]", 11, INK, MONO, "middle")

d.box(432, 176, 144, 38, fill="#11161D", stroke=RULE, sw=0.8, r=4)
d.t(504, 200, "conn 2 [readLoop]", 11, INK, MONO, "middle")

# Zone 1 하단: 갈림길 (shouldRetryRequest)
# EOF 감지 트리거 상자
d.box(260, 236, 328, 32, PAPER2, RULE, 0.9, 6)
d.t(424, 256, "shouldRetryRequest", 12, INK, MONO, "middle", 600)

# 트리거 -> 분기 화살표
d.arrow([(339, 268), (339, 280)], c=WARN, m="warn", sw=1.3)
d.arrow([(509, 268), (509, 280)], c=OK, m="ok", sw=1.3)

# 분기 B (좌측): POST 502
d.tone(260, 280, 158, 144, WARN, 6, "10", 1.0)
d.t(339, 314, "POST (비멱등)", 12, WARN, KR, "middle", 600)
d.t(339, 346, "isReplayable false", 11, INK, MONO, "middle")
d.t(339, 378, "재전송 불가 → UC", 12, WARN, KR, "middle", 600)

# 분기 A (우측): GET 재전송
d.tone(430, 280, 158, 144, OK, 6, "10", 1.0)
d.t(509, 308, "GET (멱등)", 12, OK, KR, "middle", 600)
d.t(509, 336, "isReplayable true", 11, INK, MONO, "middle")
d.t(509, 364, "새 연결 재전송", 12, OK, KR, "middle", 600)

# GET 재전송 미계측 점선 꼬리표
dash_box(d, 436, 384, 146, 28, fill="#11161D", stroke=MUTED, sw=0.8, r=4, dash="3 3")
d.t(509, 402, "GET 재전송 미계측", 11, MUTED, KR, "middle")

# 핵심 병목 (focal 1곳): 90s ≠ 1s 보관 시간 불일치
d.tone(612, 152, 120, 68, ACC, 6, "16", 1.6)
d.t(672, 178, "90s ≠ 1s", 14, ACC, MONO, "middle", 600)
d.t(672, 202, "보관 시간 불일치", 12, ACC, KR, "middle", 600)

# 풀 -> focal 연결선
d.arrow([(588, 186), (612, 186)], c=MUTED, m="ar", sw=1.3)

# 백엔드 -> focal 연결선
d.arrow([(756, 186), (732, 186)], c=WARN, m="warn", sw=1.3)

# focal -> 트리거 (경합 EOF 감지 흐름)
d.arrow([(672, 220), (672, 252), (588, 252)], c=ACC, m="acc", sw=1.4)
d.t(630, 244, "경합 EOF", 11, ACC, KR, "middle")

# GET 재전송 -> 백엔드 (새 연결 흐름)
d.arrow([(588, 364), (756, 364)], c=OK, m="ok", sw=1.3)
d.t(672, 356, "재전송", 11, OK, KR, "middle")

# Zone 2: 백엔드 (fakeinv)
d.box(744, ZY, 192, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(756, 130, "백엔드 fakeinv", 13, INK, KR, "start", 600)

# Zone 2 내부 상자들
# Box 1: 서버 빈 연결 보관 시간
d.box(756, 148, 168, 104, PAPER2, RULE, 0.9, 6)
d.t(840, 168, "idle_close 1s", 12, WARN, MONO, "middle", 600)
d.t(840, 188, "idleTimer", 11, INK, MONO, "middle")
d.t(840, 208, "FIN 송신 (100ms)", 11, WARN, KR, "middle")
d.t(840, 228, "IdleTimeout 흉내", 11, MUTED, MONO, "middle")

# Box 2: 백엔드 관측 기록
d.box(756, 268, 168, 156, PAPER2, RULE, 0.9, 6)
d.t(840, 310, "실패 POST 미도달", 12, WARN, KR, "middle", 600)
d.t(840, 364, "GET 정상 처리", 12, OK, KR, "middle", 600)
d.t(840, 396, "차이 55 ≈ UC 56", 11, MUTED, KR, "middle")

# 4. 범례 (Legend)
d.legend(456, [("핵심 원인 (90s ≠ 1s)", ACC), ("장애 관측값 (POST 502)", WARN), ("재전송 성공 (GET)", OK)])

d.save("01-01-i2-bottleneck.svg")
