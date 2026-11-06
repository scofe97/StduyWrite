# 01-03-three-guards — 다운스트림 층이 막는 세 자리(몸통 읽기·응답 쓰기 기한·배포 드레인)
# 본문 요구: 손님·프록시·백엔드 세 가로 레인 위에 요청 한 건의 시간 흐름. 막는 자리 셋: 몸통 읽기(J1 느린 손님 → 408 CT), 업스트림을 기다리는 동안 응답 쓰기 기한(J2 → 504 가 나가야 함), 배포 종료(J4 드레인). focal 은 J2.
# 타입 스펙: type-swimlane
# 사실 출처: 01-03.리버스 프록시 다운스트림 층 — 틈 시계·최소 속도·드레인.md:25-33, ADR 0014:9-16,57-65, ch09-slow-post-body.md:33-39, ch09-write-timeout-swallows-504.md:31-38, ch09-deploy-drain-cut.md:34-43
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, BAD, WARN, INFO, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "SWIMLANE · DOWNSTREAM THREE GUARDS",
    "다운스트림 층이 막는 세 자리와 요청 흐름",
    "손님·프록시·백엔드 세 레인 위에서 몸통 읽기·응답 쓰기·배포 드레인이 각 장애를 통제하고 흐름을 완수하는 구조",
    lead="몸통 읽기는 408 CT 로 끊고, 응답 쓰기는 504 누락을 막으며, 드레인은 배포 중 요청을 완수합니다.",
)

# 상단 구분선
d.line(24, 92, 936, 92, RULE, 0.8)

# 가로 수영장 레인 경계 (손님 104~200, 프록시 200~308, 백엔드 308~404)
d.line(24, 104, 936, 104, RULE, 1.0)
d.line(24, 200, 936, 200, RULE, 0.8)
d.line(24, 308, 936, 308, RULE, 0.8)
d.line(24, 404, 936, 404, RULE, 1.0)

# 액터 열 구분선 (x=152)
d.line(152, 104, 152, 404, RULE, 0.8)

# 액터 라벨
d.t(36, 144, "손님", 14, INK, KR, "start", 600)
d.t(36, 166, "npgload", 12, MUTED, MONO, "start")

d.t(36, 248, "리버스 프록시", 14, INK, KR, "start", 600)
d.t(36, 270, "npgproxy", 12, MUTED, MONO, "start")

d.t(36, 350, "백엔드", 14, INK, KR, "start", 600)
d.t(36, 372, "fakeinv", 12, MUTED, MONO, "start")

# 1. 1단계: J1 몸통 읽기 가드 (손님 -> 프록시)
d.box(168, 120, 160, 60, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(248, 144, "요청 전송 (몸통)", 13, INK, KR, "middle", 600)
d.t(248, 164, "2초에 1B 느린 손님", 13, WARN, KR, "middle")

# 손님 -> 프록시 전송 화살표 (수직)
d.arrow([(248, 180), (248, 218)], c=MUTED, m="ar", sw=1.4)

# 프록시 가드 1 상자
d.box(168, 218, 160, 72, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(248, 240, "가드 1 · 몸통 읽기 (J1)", 13, WARN, KR, "middle", 600)
d.t(248, 258, "읽기 틈 10s · 최소 1KB/s", 12, INK, KR, "middle")
d.t(248, 276, "하한 미달 408 CT 차단", 12, BAD, KR, "middle")

# 프록시 -> 백엔드 전달 화살표 (직각)
d.arrow([(328, 254), (380, 254), (380, 332)], c=MUTED, m="ar", sw=1.4)
d.t(354, 242, "정상 전달", 11, MUTED, KR, "middle")

# 2. 2단계: J2 응답 쓰기 기한 가드 (프록시 -> 백엔드 -> 프록시) — focal
# 백엔드 지연 상자
d.box(380, 332, 156, 56, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(458, 354, "백엔드 검색 20s 지연", 13, INFO, KR, "middle", 600)
d.t(458, 372, "업스트림 15s 기한 만료", 12, MUTED, KR, "middle")

# 백엔드 -> 프록시 504 UT 회신 화살표 (직각)
d.arrow([(536, 360), (580, 360), (580, 290)], c=INFO, m="info", sw=1.4)
d.t(612, 344, "504 UT", 11, INFO, MONO, "middle")

# 프록시 가드 2 상자 (ACCENT)
d.tone(480, 216, 220, 74, ACC, r=6, op="14", sw=1.6)
d.t(590, 238, "가드 2 · 응답 쓰기 (J2)", 13, ACC, KR, "middle", 600)
d.t(590, 258, "쓰기 틈 10s (대기 중 미작동)", 13, INK, KR, "middle")
d.t(590, 276, "15.0s 에 504 전송 보장", 13, ACC, KR, "middle", 600)

# 가드 2 -> 가드 3 진행 화살표 (수평)
d.arrow([(700, 253), (736, 253)], c=MUTED, m="ar", sw=1.4)

# 3. 3단계: J4 배포 드레인 가드 (프록시 -> 손님)
# 프록시 가드 3 상자
d.box(736, 216, 188, 74, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(830, 238, "가드 3 · 배포 드레인 (J4)", 13, INFO, KR, "middle", 600)
d.t(830, 258, "드레인 20s (15s 초과)", 13, INK, KR, "middle")
d.t(830, 276, "진행 요청 완수 (exit 0)", 13, OK, KR, "middle")

# 프록시 -> 손님 응답 완료 화살표 (수직)
d.arrow([(830, 216), (830, 180)], c=OK, m="ok", sw=1.4)
d.t(870, 196, "응답 전달", 12, OK, KR, "middle")

# 손님 최종 수신 상자
d.box(736, 120, 188, 60, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(830, 144, "응답 안전 수신", 13, OK, KR, "middle", 600)
d.t(830, 164, "504 · 201 (단절 방지)", 13, MUTED, KR, "middle")

# 범례 (428px 기준선, 높이 492px 안에서 여유 40px)
d.legend(
    428,
    [
        ("응답 쓰기 보호", ACC),
        ("느린 손님 차단", WARN),
        ("배포 드레인 완수", INFO),
        ("정상 수신", OK),
        ("실패 코드", BAD),
    ],
)

d.save("01-03-three-guards.svg")
