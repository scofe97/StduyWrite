# 02-01-reload-vs-restart — 프로세스 재시작 소켓 공백과 관리 API 무중단 설정 교체 시간축 비교
# 본문 요구: 두 줄을 같은 가로축에: 위 줄 재시작(듣는 소켓이 비는 약 3.0초, 그동안 refused 최대 초당 97,183건), 아래 줄 관리 API /load(새 서버를 먼저 띄우고 SO_REUSEPORT 로 같은 포트에 소켓 하나 더 → 겹친 구간 → 옛 서버 종료, 교체 97ms·50ms, refused 0, 초당 약 1,500건 성공). focal 은 위 줄의 빈 구간.
# 타입 스펙: type-timeline
# 사실 출처: 02-01.프록시 운영 — 무중단 설정 교체·인증서 사슬·모듈 등록부.md:48-56, ch10-e1-restart-vs-reload.md:22-26,45-56,86-93, caddy listeners.go L115-121
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "TIMELINE · RELOAD VS RESTART",
    "프로세스 재시작 소켓 공백과 관리 API 무중단 교체 비교",
    "재시작 시 소켓 공백 3.0초 동안 refused 최대 97,183건 발생과 관리 API SO_REUSEPORT 무중단 교체의 수치 비교 시간축",
    lead="재시작은 듣는 소켓 공백 동안 연결 거절을 유발하나, 관리 API /load 는 소켓 중첩으로 무중단을 달성합니다.",
)

# 1. 왼쪽 트랙 구분 상자 (x = 24 ~ 156)
# 위 줄 라벨 상자 (재시작)
d.box(24, 116, 132, 92, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(90, 146, "재시작 방식", 14, INK, KR, "middle", 600)
d.t(90, 170, "SIGTERM 수신", 13, MUTED, KR, "middle")
d.t(90, 192, "문 닫고 공사", 13, WARN, KR, "middle")

# 아래 줄 라벨 상자 (관리 API /load)
d.box(24, 288, 132, 108, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.t(90, 318, "관리 API /load", 13, INFO, MONO, "middle", 600)
d.t(90, 342, "SO_REUSEPORT", 13, MUTED, MONO, "middle")
d.t(90, 364, "전체 50~97ms", 13, OK, KR, "middle")

# 2. 중앙 시간축 기준선 (y = 246)
BASE_Y = 246
d.line(168, BASE_Y, 936, BASE_Y, RULE, 1.0)

# 시간 눈금 및 점 (0s, 1.0s, 2.0s, 3.0s, 4.0s)
ticks = [
    (184, "0s", MUTED),
    (360, "1.0s", SOFT),
    (536, "2.0s", SOFT),
    (712, "3.0s", OK),
    (888, "4.0s", MUTED),
]
for tx, lab, col in ticks:
    d.line(tx, BASE_Y - 4, tx, BASE_Y + 4, SOFT, 0.8)
    d.o.append(f'<circle cx="{tx}" cy="{BASE_Y}" r="4" fill="{col}"/>')
    d.t(tx, BASE_Y + 18, lab, 12, col, MONO, "middle", 600)
d.t(212, BASE_Y + 18, "재시작 경과", 12, SOFT, KR, "start")

# 3. 위 줄: 재시작 (y = 116 ~ 208)
# 소켓 공백 구간 3.0초 (t=0..3.0s, x: 184..712, 폭 528) — FOCAL
d.tone(184, 116, 528, 92, ACC, r=6, op="14", sw=1.6)
d.t(448, 144, "소켓 공백 약 3.0초", 14, ACC, KR, "middle", 600)
d.t(448, 168, "커널 즉각 RST 회신 (0.1ms)", 13, INK, KR, "middle")
d.t(448, 192, "refused 최대 97,183/s", 14, ACC, MONO, "middle", 600)

# 소켓 공백 종료 후 새 프로세스 정상 복귀 (t > 3.0s, x: 724..936, 폭 212)
d.box(724, 116, 212, 92, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(830, 144, "새 프로세스 바인드", 13, OK, KR, "middle", 600)
d.t(830, 168, "포트 :8000 수락", 13, INK, KR, "middle")
d.t(830, 192, "성공 1,269/s", 13, OK, KR, "middle")

# 4. 아래 줄: 관리 API /load (y = 288 ~ 396)
# 1단계: 새 서버 선행 기동 및 소켓 바인드 (x: 184..432, 폭 248)
d.box(184, 288, 248, 108, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(308, 314, "새 서버 선행 기동", 13, INFO, KR, "middle", 600)
d.t(308, 338, "SO_REUSEPORT 바인드", 13, INK, MONO, "middle")
d.t(308, 362, "소켓 추가 (:8000)", 13, MUTED, KR, "middle")
d.t(308, 384, "공백 0ms", 13, OK, KR, "middle")

# 전이 화살표 1 -> 2
d.arrow([(432, 342), (448, 342)], c=MUTED, m="ar", sw=1.4)

# 2단계: 소켓 겹친 구간 및 드레인 (x: 448..684, 폭 236)
d.box(448, 288, 236, 108, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(566, 314, "소켓 겹침", 13, INFO, KR, "middle", 600)
d.t(566, 338, "새 연결 즉시 수락", 13, INK, KR, "middle")
d.t(566, 362, "옛 서버 드레인", 13, MUTED, KR, "middle")
d.t(566, 384, "요청 완수 후 종료", 13, MUTED, KR, "middle")

# 전이 화살표 2 -> 3
d.arrow([(684, 342), (700, 342)], c=OK, m="ok", sw=1.4)

# 3단계: 무중단 교체 완료 수치 (x: 700..936, 폭 236)
d.tone(700, 288, 236, 108, OK, r=6, op="14", sw=1.4)
d.t(818, 314, "무중단 교체 완료", 13, OK, KR, "middle", 600)
d.t(818, 338, "교체 97ms · 50ms", 13, INK, KR, "middle")
d.t(818, 362, "refused 0건", 13, OK, MONO, "middle", 600)
d.t(818, 384, "성공 약 1,500/s", 13, OK, KR, "middle")

# 5. 범례 (y = 428)
d.legend(
    428,
    [
        ("소켓 공백 (focal)", ACC),
        ("정상 성공", OK),
        ("소켓 중첩", INFO),
        ("재시작 경고", WARN),
    ],
)

out_path = ASSETS_DIR / "02-01-reload-vs-restart.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
