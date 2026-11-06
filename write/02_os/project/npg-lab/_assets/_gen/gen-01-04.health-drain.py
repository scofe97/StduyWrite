# 01-04-health-drain — 프록시 재시작 드레인 지연과 건강 검사·재시도 비교 시간축
# 본문 요구: 가로축 프록시1 재시작 시각 기준 초. 위 줄 프록시1: /healthz 503 draining 5초(-drain-delay, 이 실습 값) → 옛 소켓 닫힘 → 다시 뜸. 가운데 줄 능동 검사: 1초 간격·시간제한 500ms 로 503 을 보고 뺌. 아래 줄 판별 결과: 판1 검사 없음(옛 소켓이 닫힌 뒤 1초 안에 502 186건·29건), 판2 능동 검사, 판3 재시도(5xx 0, 10건만 약 106ms). 값은 노트 ## 건강 검사 와 E4 기록의 값만. focal 은 판1 의 502 몰림.
# 타입 스펙: type-timeline
# 사실 출처: 01-04.리버스 프록시 앞단 층 — 규칙 고르기·전달 헤더 신뢰·건강 검사.md:137-175, ADR 0018:13-33,48-52, ch10-e4-health-check-and-retry.md:17-19,32-35,82-96
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
H = 620

d = D(
    W,
    H,
    "TIMELINE · DRAIN DELAY & HEALTH CHECK COMPARISON",
    "프록시 재시작 드레인과 건강 검사·재시도 비교 시간축",
    "프록시1 재시작 시각 0s 기준 5초 드레인 지연과 능동 검사의 503 감지 주기, 검사 없음(판1, 502 몰림 focal)·능동 검사(판2, 503 분산)·재시도(판3, 5xx 0건)의 결과 비교",
    lead="드레인은 팻말을 거는 시간이며, 능동 검사는 비정상을 빼고 재시도는 틈새 에러를 구제합니다.",
)

# 1. 상단: 프록시1 생애주기 (y = 112 ~ 152)
d.box(24, 116, 100, 32, fill=PAPER2, stroke=RULE, sw=1.0, r=4)
d.t(74, 137, "프록시1", 13, INK, KR, "middle", 600)

# 0s ~ 5s: 드레인 5초 (x: 140 ~ 640)
d.tone(140, 116, 500, 32, WARN, r=4, op="14", sw=1.0)
d.t(390, 137, "/healthz 503 draining (드레인 5초)", 13, WARN, KR, "middle", 600)

# 5.03s ~ 7s: 새 프록시1 기동 (x: 644 ~ 840)
d.tone(644, 116, 196, 32, OK, r=4, op="14", sw=1.0)
d.t(742, 137, "다시 뜸 (새 프록시1)", 13, OK, KR, "middle", 600)

# 2. 가운데 줄: 능동 검사 (Caddy) (y = 164 ~ 204)
d.box(24, 168, 100, 32, fill=PAPER2, stroke=RULE, sw=1.0, r=4)
d.t(74, 189, "능동 검사", 13, INK, KR, "middle", 600)

# 0s ~ 1.2s: 정상 감지 (x: 140 ~ 260)
d.tone(140, 168, 120, 32, OK, r=4, op="14", sw=1.0)
d.t(200, 189, "정상 감지", 13, OK, KR, "middle")

# 1.2s ~ 6.2s: 503 감지 후 라우팅 제외 (x: 260 ~ 760)
d.tone(260, 168, 500, 32, INFO, r=4, op="14", sw=1.0)
d.t(510, 189, "503 감지 → 프록시1 라우팅 제외", 13, INFO, KR, "middle", 600)

# 6.2s ~ 7s: 복귀 (x: 760 ~ 840)
d.tone(760, 168, 80, 32, OK, r=4, op="14", sw=1.0)
d.t(800, 189, "복귀", 13, OK, KR, "middle")

# 3. 시간축 기준선 (y = 232)
BASE_Y = 232
d.line(60, BASE_Y, 900, BASE_Y, RULE, 1.0)

# 0s ~ 7s 눈금 및 레이블 (x = 140 + 100*t)
ticks = [
    (0, "0s", "재시작 신호", MUTED),
    (1, "1s", None, SOFT),
    (2, "2s", None, SOFT),
    (3, "3s", None, SOFT),
    (4, "4s", None, SOFT),
    (5, "5s", "옛 소켓 닫힘", BAD),
    (6, "6s", None, SOFT),
    (7, "7s", None, SOFT),
]

for t, sec, desc, c in ticks:
    x = 140 + t * 100
    d.line(x, BASE_Y - 4, x, BASE_Y + 4, c, 1.0)
    d.o.append(f'<circle cx="{x}" cy="{BASE_Y}" r="3" fill="{c}"/>')
    d.t(x, BASE_Y + 18, sec, 13, c, MONO, "middle", 600)
    if desc:
        d.t(x, BASE_Y + 34, desc, 13, c, KR, "middle")

# 4. 아래 줄: 세 판 결과 비교 (y = 284 ~ 528)
# 판1: 검사 없음 (focal: 502 몰림)
d.box(24, 288, 100, 48, fill=PAPER2, stroke=INFO, sw=1.0, r=4)
d.t(74, 318, "판1 검사 없음", 13, INFO, KR, "middle", 600)

d.tone(140, 288, 490, 48, PAPER2, r=4, op="20", sw=1.0)
d.t(385, 318, "드레인 5초간 실패 0건", 13, MUTED, KR, "middle")

# focal 상자 (x: 636..816, y: 288..336)
d.tone(636, 288, 180, 48, ACC, r=6, op="20", sw=1.4)
d.t(726, 308, "502 몰림 (refused)", 13, ACC, KR, "middle", 600)
d.t(726, 326, "186건 · 29건 (1초 안)", 13, ACC, KR, "middle", 600)

# 판2: 능동 검사 (503 분산)
d.box(24, 352, 100, 48, fill=PAPER2, stroke=WARN, sw=1.0, r=4)
d.t(74, 382, "판2 능동 검사", 13, WARN, KR, "middle", 600)

d.tone(140, 352, 700, 48, WARN, r=4, op="12", sw=1.0)
d.t(240, 382, "틈새 502 없음", 13, OK, KR, "middle")
d.t(560, 382, "503 105건 분산 (초당 5~27건)", 13, WARN, KR, "middle", 600)

# 판3: 재시도 (5xx 0건)
d.box(24, 416, 100, 48, fill=PAPER2, stroke=OK, sw=1.0, r=4)
d.t(74, 446, "판3 재시도", 13, OK, KR, "middle", 600)

d.tone(140, 416, 700, 48, OK, r=4, op="14", sw=1.2)
d.t(340, 446, "5xx 0건 (전부 성공)", 13, OK, KR, "middle", 600)

d.tone(636, 422, 194, 36, INFO, r=4, op="18", sw=1.0)
d.t(733, 444, "10건 약 106ms (100ms 대기)", 12, INFO, KR, "middle")

# 범례
d.legend(
    574,
    [
        ("정상 / 성공", OK),
        ("드레인 / 503 분산", WARN),
        ("소켓 닫힘", BAD),
        ("정보 / 지연", INFO),
        ("502 몰림 (focal)", ACC),
    ],
)

out = ASSETS_DIR / "01-04-health-drain.svg"
d.save(out)
print(f"saved: {out}")
