# 01-03-two-clocks — 백엔드 대기 15초에서 전체 시계 WriteTimeout 과 쓰기 틈 시계의 동작 차이
# 본문 요구: 같은 요청 위에 두 줄: 위 줄 WriteTimeout(전체 시계, 헤더를 다 읽은 순간 시작해 업스트림 대기까지 셈 → 504 전에 끊김), 아래 줄 틈 시계(쓰기가 될 때마다 0 으로 다시 잼). 초 값은 리허설 J2 기록의 값만.
# 타입 스펙: type-timeline
# 사실 출처: 01-03.리버스 프록시 다운스트림 층 — 틈 시계·최소 속도·드레인.md:37-48, ADR 0014:14,44-48,61-62, ch09-write-timeout-swallows-504.md:19-21,33-38,43-46, server.go:1029-1031
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
    "TIMELINE · CH09 J2 WRITE TIMEOUT VS IDLE GAP",
    "전체 시계 WriteTimeout 과 쓰기 틈 시계의 15초 동작 비교",
    "동일한 백엔드 검색 지연 20초 요청에서 전체 시계는 15초에 소켓을 끊어 504를 삼키고, 쓰기 틈 시계는 대기 중 시계가 돌지 않아 504 응답을 정상 전달하는 시간축",
    lead="전체 시계는 백엔드 대기까지 합산해 504 전에 끊기지만, 틈 시계는 쓰기 마디마다 다시 재어 504를 전송합니다.",
)

# 상단 구분선
d.line(24, 92, 936, 92, RULE, 0.8)

# 1초당 36px, t=0s 는 x=152, t=20s 는 x=872 (왼쪽 여백 30px 이상 확보)
def X(sec):
    return round(152 + sec * 36, 1)

# 1. 윗줄: 전체 시계 (WriteTimeout 15s) — 왼쪽 여백 30px
d.t(140, 142, "전체 시계", 13, BAD, KR, "end", 600)
d.t(140, 160, "WriteTimeout 15s", 11, MUTED, MONO, "end")

# 0s ~ 15.0s: 백엔드 대기 시간 합산 구간
d.tone(X(0), 124, X(15) - X(0), 48, INFO, r=6, op="14", sw=1.2)
d.t((X(0) + X(15)) / 2, 153, "백엔드 대기 15s 합산 (server.go:1029)", 13, INFO, KR, "middle", 600)

# 15.001s: WriteTimeout 만료 소켓 단절
d.o.append(f'<circle cx="{X(15)}" cy="148" r="5" fill="{BAD}"/>')
d.tone(X(15) + 8, 124, 216, 48, BAD, r=6, op="18", sw=1.4)
d.t(X(15) + 116, 144, "15.001s 소켓 단절", 13, BAD, KR, "middle", 600)
d.t(X(15) + 116, 162, "손님 eof 26건 · 504 삼킴", 12, BAD, KR, "middle")

# 2. 중간: 시간축 기준선 (Timeline Baseline) 및 눈금
base_y = 224
d.line(136, base_y, 896, base_y, RULE, 1.0)

for sec, lab in (
    (0, "0s (헤더 완료)"),
    (5, "5s"),
    (10, "10s"),
    (15, "15.0s (업스트림 만료)"),
    (20, "20s (검색 지연)"),
):
    x = X(sec)
    d.line(x, base_y - 4, x, base_y + 4, RULE, 1.0)
    d.t(x, base_y + 20, lab, 12, MUTED, MONO if sec in (5, 10) else KR, "middle")

# 3. 아랫줄: 쓰기 틈 시계 (10s · ADR 0014) — 왼쪽 여백 30px
d.t(140, 290, "쓰기 틈 시계", 13, ACC, KR, "end", 600)
d.t(140, 308, "10s (ADR 0014)", 11, MUTED, MONO, "end")

# 0s ~ 15.0s: 백엔드 대기 중 시계 미작동 구간
d.box(X(0), 272, X(15) - X(0), 48, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.t((X(0) + X(15)) / 2, 301, "대기 중 쓰기 시계 미작동 (쓰기 발생 시만 10s 잼)", 13, MUTED, KR, "middle")

# 15.0s: 504 응답 쓰기 완료
d.o.append(f'<circle cx="{X(15)}" cy="296" r="6" fill="{ACC}"/>')
d.tone(X(15) + 8, 272, 216, 48, ACC, r=6, op="18", sw=1.6)
d.t(X(15) + 116, 292, "15.0s 에 504 전송", 13, ACC, KR, "middle", 600)
d.t(X(15) + 116, 310, "손님 504 33건 정상 도착", 12, OK, KR, "middle", 600)

# 4. 하단 비교 요약 상자
d.box(152, 356, 764, 44, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(343, 383, "전체 시계: 손님 eof 26건 단절", 13, BAD, KR, "middle", 600)
d.line(534, 362, 534, 394, RULE, 0.8)
d.t(725, 383, "쓰기 틈 시계: 손님 504 33건 도착", 13, OK, KR, "middle", 600)

# 범례
d.legend(
    428,
    [
        ("쓰기 틈 504 전송", ACC),
        ("WriteTimeout 소켓 단절", BAD),
        ("업스트림 대기 구간", INFO),
        ("정상 도착", OK),
    ],
)

d.save("01-03-two-clocks.svg")
