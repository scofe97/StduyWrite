# 01-01-i1-bottleneck — 손님–프록시–서버의 소켓·고루틴과 정체·제한 위치를 보인 I1 병목 지도
# 본문 요구(01-01 I1 slow search starves lookup): 클라이언트–프록시–서버 흐름에서 소켓·고루틴 누적과 제한 유무, 핵심 정체 지점을 아키텍처 지도로 보인다.
# 타입 스펙: type-architecture
# 사실 출처: fakeinv/main.go:38-40,153-157,180-189, proxy.go:19, server.go:3493, transport.go:218,230, ch08-slow-search-starves-lookup.md:15-17,26,27,57,67
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
    "ARCHITECTURE · CH08 I1 BOTTLENECK",
    "손님–프록시–서버 소켓·고루틴과 병목 위치",
    "fakeinv 공유 창구 32칸 독점, 프록시 무제한 수송, 취소 무시로 인한 병목 구조",
    lead="검색 트래픽의 백엔드 창구 독점과 프록시 보호 부재, 취소 무시가 야기한 병목 지도"
)

def dash_box(d, x, y, w, h, fill=PAPER2, stroke=RULE, sw=0.9, r=6, dash="4 3"):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')

# 상단 구분선
d.line(24, 92, 936, 92, RULE, 0.8)

# 1. Zone 배경 (Client, Proxy, Backend)
ZY = 108
ZH = 328

# Zone 0: 손님 (npgload)
d.box(24, ZY, 216, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(36, 130, "손님 npgload", 13, INK, KR, "start", 600)

# Zone 0 내부 상자들
# Box 1: 부하 생성
d.box(36, 148, 192, 60, PAPER2, RULE, 0.9, 6)
d.t(132, 172, "get 50/s · search 5/s", 11, INK, MONO, "middle", 600)
d.t(132, 192, "평소 p99 8ms", 12, MUTED, MONO, "middle")

# Box 2: 클라이언트 기한 [제한: 실선 OK]
d.box(36, 216, 192, 60, PAPER2, OK, 1.2, 6)
d.t(132, 238, "timeout: 30s", 12, OK, MONO, "middle", 600)
d.t(132, 258, "30초 초과 단절", 12, MUTED, KR, "middle")

# Box 3: 단절 관측
d.box(36, 284, 192, 60, PAPER2, RULE, 0.9, 6)
d.t(132, 306, "DC 49150 · UT 0", 12, WARN, MONO, "middle", 600)
d.t(132, 326, "손님 단절", 12, MUTED, KR, "middle")

# Box 4: 장애 증상
d.box(36, 352, 192, 60, PAPER2, RULE, 0.9, 6)
d.t(132, 374, "단건 조회 지연", 12, WARN, KR, "middle", 600)
d.t(132, 394, "p99 8s→30s", 12, MUTED, MONO, "middle")

# Zone 0 → Zone 1 연결선
d.arrow([(240, 168), (280, 168)], c=MUTED, m="ar", sw=1.3)
d.t(260, 158, "HTTP", 11, MUTED, MONO, "middle")

# Zone 1: 프록시 (npgproxy v0)
d.box(280, ZY, 272, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(292, 130, "프록시 npgproxy v0", 13, INK, KR, "start", 600)
d.t(480, 130, "보호 없음", 12, WARN, KR, "start", 600)

# Zone 1 내부 상자들
# Box 1: 연결당 고루틴 및 누적 자원
d.box(292, 148, 248, 60, PAPER2, RULE, 0.9, 6)
d.t(416, 170, "go c.serve", 12, INK, MONO, "middle", 600)
d.t(416, 190, "inflight 913 · HeapAlloc 47MB", 11, WARN, MONO, "middle", 600)

# Box 2: 수송 계층
d.box(292, 216, 248, 48, PAPER2, RULE, 0.9, 6)
d.t(416, 236, "http.DefaultTransport", 12, INK, MONO, "middle", 600)
d.t(416, 252, "proxy.go:19", 11, MUTED, MONO, "middle")

# Box 3: 부재한 보호 장치 3종 [점선 빈 칸: WARN]
dash_box(d, 292, 272, 248, 148, fill="#131820", stroke=WARN, sw=1.0, r=6, dash="4 3")
d.t(416, 296, "[부재] 보호 설정 없음", 13, WARN, KR, "middle", 600)
d.t(416, 326, "ResponseHeaderTimeout 0", 12, INK, MONO, "middle")
d.t(416, 356, "MaxConnsPerHost 0", 12, INK, MONO, "middle")
d.t(416, 386, "경로별 격벽 없음", 12, MUTED, KR, "middle")

# Zone 1 → Zone 2 연결선 (소켓 폭증 번들)
d.t(588, 136, "conns_open", 11, WARN, MONO, "middle", 600)
d.t(588, 148, "2966", 12, WARN, MONO, "middle", 600)
for y in (156, 162, 168, 174, 180):
    d.arrow([(552, y), (624, y)], c=WARN, m="warn", sw=1.3)
d.t(588, 198, "소켓 폭증", 12, WARN, KR, "middle")

# Zone 2: 백엔드 (fakeinv)
d.box(624, ZY, 312, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(636, 130, "백엔드 fakeinv", 13, INK, KR, "start", 600)

# Zone 2 내부 상자들 (세로 흐름 화살표 연결)
# 1) 연결 고루틴 칸 (맨 위)
d.box(636, 144, 288, 36, PAPER2, RULE, 0.9, 6)
d.t(780, 158, "go c.serve", 12, INK, MONO, "middle", 600)
d.t(780, 170, "연결당 고루틴", 11, MUTED, KR, "middle")

# 흐름 화살표: 고루틴 → 대기열 (길이 20px)
d.arrow([(780, 180), (780, 200)], c=MUTED, m="ar", sw=1.3)

# 2) 대기열 칸 [점선 빈 칸: WARN]
dash_box(d, 636, 200, 288, 36, fill="#131820", stroke=WARN, sw=1.0, r=6, dash="4 3")
d.t(780, 214, "queued 2933", 12, WARN, MONO, "middle", 600)
d.t(780, 226, "QueueLimit 0", 11, MUTED, KR, "middle")

# 흐름 화살표: 대기열 → 공유 창구 (길이 20px)
d.arrow([(780, 236), (780, 256)], c=ACC, m="acc", sw=1.4)

# 3) 핵심 병목 지점: 공유 창구 [FOCAL! ACCENT! 실선 제한]
d.tone(636, 256, 288, 56, ACC, 6, "16", 1.6)
d.t(780, 272, "공유 창구 · [제한] Workers 32", 12, ACC, KR, "middle", 600)
d.t(780, 288, "검색 40 > 창구 32", 13, INK, KR, "middle", 600)
d.t(780, 302, "단건 조회 질식", 11, INK, KR, "middle")

# 흐름 화살표: 공유 창구 → 처리 실행 (길이 20px)
d.arrow([(704, 312), (704, 332)], c=MUTED, m="ar", sw=1.3)

# 4A) 처리 칸 (좌측)
d.box(636, 332, 136, 92, PAPER2, RULE, 0.9, 6)
d.t(704, 354, "처리 실행", 12, INK, KR, "middle", 600)
d.t(704, 376, "search 8s", 12, INK, MONO, "middle", 600)
d.t(704, 398, "8s 점유", 11, MUTED, KR, "middle")

# 4B) 취소 무시 칸 (우측 — 처리 칸 옆 배치, 창구 자리를 놓지 않음 표시)
d.box(788, 332, 136, 92, PAPER2, WARN, 1.0, 6)
d.t(856, 352, "취소 무시", 12, WARN, KR, "middle", 600)
d.t(856, 370, "창구 자리를 놓지 않음", 11, WARN, KR, "middle", 600)
d.t(856, 388, "HonorCancel=false", 11, WARN, MONO, "middle")
d.t(856, 402, "worked_after_cancel", 11, WARN, MONO, "middle")
d.t(856, 414, "26204", 11, WARN, MONO, "middle", 600)

# 4. 범례 (Legend)
d.legend(456, [("핵심 병목 (공유 창구)", ACC), ("장애 관측값", WARN), ("제한 기준", OK)])

d.save("01-01-i1-bottleneck.svg")
