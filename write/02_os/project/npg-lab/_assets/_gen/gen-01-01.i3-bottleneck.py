# 01-01-i3-bottleneck — 호스트당 빈 연결 2개 제한과 상한 없는 연결 생성으로 인한 프록시 출발 포트 고갈 병목 지도
# 본문 요구(01-01 근본 원인): I3 병목 지도: 호스트당 빈 연결 2, 연결 상한 없음, 프록시 쪽 TIME_WAIT 와 출발 포트
# 타입 스펙: type-architecture
# 사실 출처: ch08-port-exhaustion-time-wait.md:5-6,17-27,45-50,68-76,87-92, transport.go:45-56,60,99,1034-1037,1040-1045,1115,1515-1516,1568,2049
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, WARN, OK, KR, MONO

W = 960
H = 504

d = D(
    W,
    H,
    "ARCHITECTURE · CH08 I3 BOTTLENECK",
    "I3 병목 지도: 빈 연결 2개와 프록시 포트 고갈",
    "호스트당 빈 연결 2 제한과 상한 없는 재연결로 프록시 포트가 고갈되는 병목 구조",
    lead="호스트당 빈 연결 2개 제한, 상한 없는 dial, 프록시 TIME_WAIT 누적으로 인한 포트 고갈 지도"
)

def dash_box(d, x, y, w, h, fill=PAPER2, stroke=RULE, sw=0.9, r=6, dash="4 3"):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')

# 상단 구분선
d.line(24, 92, 936, 92, RULE, 0.8)

# 1. Zone 배경 (Client, Proxy, Backend)
ZY = 108
ZH = 328

# Zone 0: 손님 (npgload)
d.box(24, ZY, 200, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(36, 130, "손님 npgload", 13, INK, KR, "start", 600)

# Zone 0 내부 상자들 (Zone 2 와 y·h 대칭)
# Box 1: 부하 생성
d.box(36, 148, 176, 64, PAPER2, RULE, 0.9, 6)
d.t(124, 172, "-c 50 닫힌 고리", 13, INK, KR, "middle", 600)
d.t(124, 194, "inflight 50", 12, MUTED, MONO, "middle")

# Box 2: 초반 정상 구간
d.box(36, 224, 176, 76, PAPER2, OK, 1.0, 6)
d.t(124, 250, "처음 9초: 200", 13, OK, KR, "middle", 600)
d.t(124, 274, "p99 19~44ms", 12, MUTED, MONO, "middle")

# Box 3: 9초 후 장애 관측
d.box(36, 312, 176, 104, PAPER2, WARN, 1.0, 6)
d.t(124, 338, "9초 후: 502", 13, WARN, KR, "middle", 600)
d.t(124, 362, "UF 37,381", 12, WARN, MONO, "middle", 600)
d.t(124, 386, "p99 200~330ms", 12, MUTED, MONO, "middle")

# Zone 0 → Zone 1 연결선
d.arrow([(224, 176), (264, 176)], c=MUTED, m="ar", sw=1.3)
d.t(244, 162, "HTTP", 11, MUTED, MONO, "middle")
d.t(244, 194, "-c 50", 11, MUTED, MONO, "middle")

# Zone 1: 프록시 (npgproxy v0)
d.box(264, ZY, 440, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(276, 130, "프록시 npgproxy v0", 13, INK, KR, "start", 600)

# Zone 1 내부 상단: getConn 판단 바
d.box(276, 144, 416, 24, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(484, 160, "getConn 갈림", 13, INK, KR, "middle", 600)

# Zone 1 좌측 박스: 연결 풀 및 반환 만원 시 능동 닫힘
d.box(276, 176, 200, 104, fill=PAPER2, stroke=OK, sw=1.0, r=6)
d.t(376, 196, "[남기는 쪽 2]", 13, OK, KR, "middle", 600)
d.t(376, 218, "MaxIdleConnsPerHost 2", 12, INK, MONO, "middle")
d.t(376, 240, "만원: pconn.close", 13, WARN, KR, "middle")
d.t(376, 262, "[먼저 닫는 쪽에 TIME_WAIT]", 13, WARN, KR, "middle", 600)

# Zone 1 우측 박스: 무제한 다이얼 (점선 빈 칸)
dash_box(d, 492, 176, 200, 104, fill="#131820", stroke=WARN, sw=1.0, r=6, dash="4 3")
d.t(592, 196, "[여는 쪽 상한 없음]", 13, WARN, KR, "middle", 600)
d.t(592, 218, "MaxConnsPerHost 0", 12, INK, MONO, "middle")
d.t(592, 240, "새 연결 1,364/s", 13, WARN, KR, "middle")
d.t(592, 262, "48개 dial", 13, MUTED, KR, "middle")

# Zone 1 상단 → Focal 연결 화살표 (20px)
d.arrow([(376, 280), (376, 300)], c=WARN, m="warn", sw=1.3)
d.arrow([(592, 280), (592, 300)], c=WARN, m="warn", sw=1.3)

# Zone 1 하단: 핵심 병목 지점 - 프록시 호스트 칸 [FOCAL! ACCENT!]
d.tone(276, 300, 416, 120, ACC, 6, "14", 1.6)
d.t(288, 322, "프록시 호스트", 13, ACC, KR, "start", 600)

d.t(288, 344, "TIME_WAIT 28,213 (17:53) · 60s", 12, WARN, MONO, "start", 600)
d.t(288, 366, "출발 포트 약 28,232", 13, INK, KR, "start", 600)
d.t(288, 388, "cannot assign requested address", 12, WARN, MONO, "start", 600)
d.t(288, 408, "새 연결 0 (17:53)", 13, WARN, KR, "start", 600)
d.t(468, 408, "UF 37,381 (16:47)", 13, WARN, KR, "start", 600)

# Zone 1 → Zone 2 연결선
d.arrow([(704, 204), (744, 204)], c=MUTED, m="ar", sw=1.3)
d.t(724, 190, "TCP", 11, MUTED, MONO, "middle")
d.t(724, 222, ":9090", 11, MUTED, MONO, "middle")

# Zone 2: 백엔드 (fakeinv)
d.box(744, ZY, 192, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(756, 130, "백엔드 fakeinv", 13, INK, KR, "start", 600)

# Zone 2 내부 상자들 (Zone 0 과 y·h 대칭)
# Box 1: 대상 서비스
d.box(756, 148, 168, 64, PAPER2, RULE, 0.9, 6)
d.t(840, 184, ":9090 단건 조회", 13, INK, KR, "middle")

# Box 2: 열린 연결 추이
d.box(756, 224, 168, 76, PAPER2, RULE, 0.9, 6)
d.t(840, 250, "열린 소켓 52 → 10", 13, INK, KR, "middle", 600)
d.t(840, 274, "TIME_WAIT 안 남음", 12, OK, KR, "middle", 600)

# Box 3: 수동 닫힘 (TIME_WAIT 없음)
d.box(756, 312, 168, 104, PAPER2, OK, 1.0, 6)
d.t(840, 350, "수동 닫힘", 13, INK, KR, "middle", 600)
d.t(840, 376, "프록시 FIN 수신", 13, MUTED, KR, "middle")

# 4. 범례 (Legend)
d.legend(456, [("핵심 병목 (프록시 포트 고갈)", ACC), ("장애 관측값", WARN), ("정상·제한 기준", OK)])

d.save("01-01-i3-bottleneck.svg")
