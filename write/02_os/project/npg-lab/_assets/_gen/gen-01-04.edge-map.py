# 01-04-edge-map — 앞단 층이 막는 세 자리와 요청 전달 지도
# 본문 요구: 가로로 손님 → Caddy(앞단) → npgproxy → fakeinv. 앞단이 정하는 세 자리를 각 홉 위에 슬롯으로: 어느 규칙이 받는가(route), 손님 주소를 누구 말로 믿는가(XFF), 어느 뒤쪽 서버로 보내는가(health). 8장 업스트림 층·9장 다운스트림 층이 맡은 구간은 회색 띠로만. focal 은 앞단 Caddy.
# 타입 스펙: type-process
# 사실 출처: 01-04.리버스 프록시 앞단 층 — 규칙 고르기·전달 헤더 신뢰·건강 검사.md:31-40, ADR 0015:25-29,53-58, ADR 0016:17-25, ADR 0017:17-29, ADR 0018:13-33
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "PROCESS · EDGE ARCHITECTURE & THREE GUARDS",
    "앞단 층이 막는 세 자리와 요청 전달 지도",
    "손님·앞단·프록시·백엔드 네 홉 위에서 규칙 선택·헤더 신뢰·건강 검사가 경계를 보호하는 구조",
    lead="앞단 Caddy 가 규칙을 고르고, 위조 헤더를 차단하며, 정상 인스턴스로만 트래픽을 넘깁니다.",
)

# 상단 구분선 (4의 배수 y=92)
d.line(24, 92, 936, 92, RULE, 0.8)

# 1. 네 단계 헤더 상자 (손님 24..188, 앞단 240..472, 프록시 524..716, 백엔드 768..936)
# 손님 (npgload)
d.box(24, 104, 164, 60, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(106, 128, "손님", 14, INK, KR, "middle", 600)
d.t(106, 148, "npgload", 12, MUTED, MONO, "middle")

# Caddy (앞단 리버스 프록시) — FOCAL (accent 테두리 + tone)
d.tone(240, 104, 232, 60, ACC, r=6, op="14", sw=1.6)
d.t(356, 128, "앞단 Caddy", 14, ACC, KR, "middle", 600)
d.t(356, 148, ":8000 (관문)", 12, INK, MONO, "middle")

# npgproxy (리버스 프록시)
d.box(524, 104, 192, 60, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(620, 128, "리버스 프록시", 14, INK, KR, "middle", 600)
d.t(620, 148, "npgproxy :28080", 12, MUTED, MONO, "middle")

# fakeinv (백엔드)
d.box(768, 104, 168, 60, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(852, 128, "백엔드", 14, INK, KR, "middle", 600)
d.t(852, 148, "fakeinv :29090", 12, MUTED, MONO, "middle")

# 단계 사이 연결 화살표 (수평)
d.arrow([(188, 134), (240, 134)], c=MUTED, m="ar", sw=1.4)
d.t(214, 124, "요청", 11, MUTED, KR, "middle")

d.arrow([(472, 134), (524, 134)], c=MUTED, m="ar", sw=1.4)
d.t(498, 124, "전달", 11, MUTED, KR, "middle")

d.arrow([(716, 134), (768, 134)], c=MUTED, m="ar", sw=1.4)
d.t(742, 124, "호출", 11, MUTED, KR, "middle")

# 2. 담당 층 구간 띠 (y=176, h=24)
# 10장 앞단 층 (손님 ~ 앞단)
d.box(24, 176, 448, 24, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(248, 192, "앞단 층 (10장)", 11, ACC, KR, "middle", 600)

# 9장 다운스트림 층 (회색 띠)
d.box(524, 176, 192, 24, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(620, 192, "다운스트림 층 (9장)", 11, MUTED, KR, "middle")

# 8장 업스트림 층 (회색 띠)
d.box(768, 176, 168, 24, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(852, 192, "업스트림 층 (8장)", 11, MUTED, KR, "middle")

# 3. 세 슬롯 (규칙 route · 헤더 XFF · 건강 health)
# --- 슬롯 1: 어느 규칙이 받는가 (route) ---
d.box(24, 216, 164, 60, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(106, 250, "/v1/devices", 13, INK, MONO, "middle")

d.tone(240, 216, 232, 60, ACC, r=4, op="10", sw=1.2)
d.t(356, 250, "npg_route 선택", 13, ACC, KR, "middle", 600)

d.box(524, 216, 192, 60, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(620, 250, "X-Edge-Route: npg", 12, MUTED, MONO, "middle")

d.box(768, 216, 168, 60, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(852, 250, "200 OK 응답", 12, MUTED, KR, "middle")

d.arrow([(188, 246), (240, 246)], c=MUTED, m="ar", sw=1.2)
d.arrow([(472, 246), (524, 246)], c=MUTED, m="ar", sw=1.2)
d.arrow([(716, 246), (768, 246)], c=MUTED, m="ar", sw=1.2)

# --- 슬롯 2: 손님 주소를 누구 말로 믿는가 (XFF) ---
d.box(24, 288, 164, 60, fill=PAPER2, stroke=WARN, sw=0.9, r=4)
d.t(106, 322, "XFF: 203.0.113.195", 11, WARN, MONO, "middle")

d.tone(240, 288, 232, 60, ACC, r=4, op="10", sw=1.2)
d.t(356, 322, "위조 삭제 · 127.0.0.1", 13, ACC, KR, "middle", 600)

d.box(524, 288, 192, 60, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(620, 322, "신뢰 대역 비움", 12, MUTED, KR, "middle")

d.box(768, 288, 168, 60, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(852, 322, "XFF: [127.0.0.1]", 11, MUTED, MONO, "middle")

d.arrow([(188, 318), (240, 318)], c=WARN, m="warn", sw=1.2)
d.arrow([(472, 318), (524, 318)], c=OK, m="ok", sw=1.2)
d.arrow([(716, 318), (768, 318)], c=MUTED, m="ar", sw=1.2)

# --- 슬롯 3: 어느 뒤쪽 서버로 보내는가 (health) ---
d.box(24, 360, 164, 60, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(106, 394, "손님 10명 요청", 12, INK, KR, "middle")

d.tone(240, 360, 232, 60, ACC, r=4, op="10", sw=1.2)
d.t(356, 394, "능동 1s · 재시도 100ms", 13, ACC, KR, "middle", 600)

d.box(524, 360, 192, 60, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(620, 394, "/healthz (503)", 12, MUTED, MONO, "middle")

d.box(768, 360, 168, 60, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(852, 394, "5xx 0건 완수", 12, MUTED, KR, "middle")

d.arrow([(188, 390), (240, 390)], c=MUTED, m="ar", sw=1.2)
d.arrow([(472, 390), (524, 390)], c=OK, m="ok", sw=1.2)
d.arrow([(716, 390), (768, 390)], c=MUTED, m="ar", sw=1.2)

# 범례
d.legend(
    444,
    [
        ("앞단 focal 통제", ACC),
        ("정상 전달 · 통과", OK),
        ("위조 주장 · 주의", WARN),
        ("앞선 8·9장 구간", MUTED),
    ],
)

d.save(str(ASSETS_DIR / "01-04-edge-map.svg"))
