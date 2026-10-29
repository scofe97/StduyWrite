# 01-02-two-layers — 다운스트림·업스트림 두 층과 응답 헤더 전송 전후 실패 처리의 두 갈래
# 본문 요구: 손님 → 프록시 → 백엔드 가로 셋. 다운스트림(9장)·업스트림(8장) 구간과 헤더 전후 실패 두 갈래. focal 은 헤더 보낸 뒤 연결 끊김.
# 타입 스펙: type-architecture
# 사실 출처: 0011-reverse-proxy-product.md:11-15,26-29,33-37, 0012-upstream-deadlines-and-pool.md:103, proxy.go:16,34-42, accesslog.go:50-57, doc.go:8-12
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, WARN, BAD, INFO, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "ARCHITECTURE · DOWNSTREAM & UPSTREAM LAYERS",
    "다운스트림·업스트림 두 층과 프록시 실패의 두 갈래",
    "손님-프록시-백엔드 구조에서 다운스트림과 업스트림의 분리와 응답 헤더 전송 전후 실패 분기",
    lead="응답 헤더 전송 전 실패는 상태 코드로 알리고, 헤더 전송 뒤 실패는 panic 으로 연결을 끊습니다.",
)

# 상단 구분선 (4의 배수)
d.line(24, 92, 936, 92, RULE, 0.8)

ZY = 108
ZH = 328

# 1. Zone 배경 (손님, 프록시, 백엔드 가로 셋)
# Zone 0: 손님 (npgload) — x: 24 ~ 192 (w: 168)
d.box(24, ZY, 168, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(36, 132, "손님 npgload", 14, INK, KR, "start", 600)

# Zone 1: 프록시 (npgproxy) — x: 288 ~ 712 (w: 424)
d.box(288, ZY, 424, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(300, 132, "리버스 프록시 npgproxy", 14, INK, KR, "start", 600)
d.t(700, 132, "httputil.ReverseProxy", 13, MUTED, MONO, "end")

# Zone 2: 백엔드 (fakeinv) — x: 808 ~ 936 (w: 128)
d.box(808, ZY, 128, ZH, fill="#11161D", stroke=RULE, sw=0.8, r=8)
d.t(820, 132, "백엔드 fakeinv", 14, INK, KR, "start", 600)

# 2. 구간 헤더 칩 (다운스트림 9장 · 업스트림 8장) — gap 영역에 배치하여 Zone 과 겹침 방지
# 다운스트림 구간 (x: 194 ~ 286, center: 240)
d.box(194, 116, 92, 32, PAPER2, INFO, 1.0, 4)
d.t(240, 136, "다운스트림(9장)", 11, INFO, KR, "middle", 600)

# 업스트림 구간 (x: 714 ~ 806, center: 760)
d.box(714, 116, 92, 32, PAPER2, INFO, 1.0, 4)
d.t(760, 136, "업스트림(8장)", 11, INFO, KR, "middle", 600)

# 3. 내부 상자 및 흐름
# --- 1행: 정상 요청 전달 경로 (HTTP Request) ---
# Zone 0 상자 (x: 36, w: 144)
d.box(36, 156, 144, 56, PAPER2, RULE, 0.9, 6)
d.t(108, 180, "HTTP 요청", 14, INK, KR, "middle", 600)
d.t(108, 200, "클라이언트 송신", 13, MUTED, KR, "middle")

# Zone 1 상단 상자 (ReverseProxy 요청 전달, x: 300, w: 400)
d.box(300, 156, 400, 56, PAPER2, RULE, 0.9, 6)
d.t(500, 178, "요청 전달 · Rewrite", 14, INK, KR, "middle", 600)
d.t(500, 198, "URL 갱신 · Transport 호출", 13, MUTED, KR, "middle")

# Zone 2 상자 (x: 820, w: 104)
d.box(820, 156, 104, 56, PAPER2, RULE, 0.9, 6)
d.t(872, 180, "요청 수신", 14, INK, KR, "middle", 600)
d.t(872, 200, "업스트림 처리", 13, MUTED, KR, "middle")

# 화살표: 손님 -> 프록시
d.arrow([(180, 184), (300, 184)], c=MUTED, m="ar", sw=1.4)
d.t(240, 174, "요청 전송", 13, MUTED, KR, "middle")

# 화살표: 프록시 -> 백엔드
d.arrow([(700, 184), (820, 184)], c=MUTED, m="ar", sw=1.4)
d.t(760, 174, "전송", 13, MUTED, KR, "middle")

# --- 2행: 갈래 1 — 응답 헤더 전송 전 실패 (ErrorHandler) ---
# Zone 2 에러 원인 상자
d.box(820, 240, 104, 76, PAPER2, RULE, 0.9, 6)
d.t(872, 264, "응답 실패", 14, WARN, KR, "middle", 600)
d.t(872, 286, "dial·타임아웃", 13, WARN, KR, "middle")
d.t(872, 304, "헤더 전송 전", 13, MUTED, KR, "middle")

# Zone 1 갈래 1 상자: ErrorHandler
d.box(300, 240, 400, 76, PAPER2, WARN, 1.0, 6)
d.t(500, 264, "헤더 전송 전 실패 · ErrorHandler", 14, WARN, KR, "middle", 600)
d.t(500, 286, "classify 판정 → 상태 코드 결정", 13, INK, KR, "middle")
d.t(500, 304, "502 · 503 · 504 반환", 13, WARN, KR, "middle")

# Zone 0 갈래 1 결과 상자
d.box(36, 240, 144, 76, PAPER2, RULE, 0.9, 6)
d.t(108, 264, "상태 코드 수신", 14, WARN, KR, "middle", 600)
d.t(108, 286, "502 · 503 · 504", 14, WARN, MONO, "middle", 600)
d.t(108, 304, "정상 에러 응답", 13, MUTED, KR, "middle")

# 화살표: 백엔드 -> 프록시 (헤더 전 실패)
d.arrow([(820, 278), (700, 278)], c=WARN, m="warn", sw=1.4)
d.t(760, 268, "실패", 13, WARN, KR, "middle")

# 화살표: 프록시 -> 손님 (상태 코드 전달)
d.arrow([(300, 278), (180, 278)], c=WARN, m="warn", sw=1.4)
d.t(240, 268, "상태 코드", 13, WARN, KR, "middle")

# --- 3행: 갈래 2 — 응답 헤더 전송 뒤 실패 (FOCAL! panic ErrAbortHandler) ---
# Zone 2 에러 원인 상자
d.box(820, 336, 104, 80, PAPER2, RULE, 0.9, 6)
d.t(872, 360, "본문 단절", 14, BAD, KR, "middle", 600)
d.t(872, 382, "EOF·RST 단절", 13, BAD, MONO, "middle")
d.t(872, 400, "헤더 전송 뒤", 13, MUTED, KR, "middle")

# Zone 1 갈래 2 상자 (FOCAL! ACCENT!)
d.tone(300, 336, 400, 80, ACC, 6, "14", 1.6)
d.t(500, 360, "헤더 전송 뒤 실패 · panic(ErrAbortHandler)", 14, ACC, KR, "middle", 600)
d.t(500, 382, "본문 복사 중단 · ErrorHandler 미경유", 13, ACC, KR, "middle", 600)
d.t(500, 400, "손님 연결 즉시 단절", 13, MUTED, KR, "middle")

# Zone 0 갈래 2 결과 상자
d.box(36, 336, 144, 80, PAPER2, RULE, 0.9, 6)
d.t(108, 360, "연결 단절 감지", 14, BAD, KR, "middle", 600)
d.t(108, 382, "상태 코드 없음", 14, BAD, KR, "middle", 600)
d.t(108, 400, "TCP 연결 끊김", 13, MUTED, KR, "middle")

# 화살표: 백엔드 -> 프록시 (본문 단절)
d.arrow([(820, 376), (700, 376)], c=ACC, m="acc", sw=1.4)
d.t(760, 366, "단절", 13, ACC, KR, "middle")

# 화살표: 프록시 -> 손님 (연결 끊김)
d.arrow([(300, 376), (180, 376)], c=ACC, m="acc", sw=1.6)
d.t(240, 366, "연결 끊김", 13, ACC, KR, "middle")

# 4. 범례 (Legend)
d.legend(448, [("핵심 단절 (focal)", ACC), ("헤더 전 실패 (상태 코드)", WARN), ("네트워크 구간", INFO)])

d.save("01-02-two-layers.svg")
