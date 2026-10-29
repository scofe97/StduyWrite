# 01-01-i3-fix — 고친 뒤 연결 일생: 동시 50 중 24는 풀을 쓰고 26은 기다리며, 돌아온 연결이 닫히지 않고 재사용된다
# 본문 요구(01-01 I3 고친 뒤): 빈 연결 상한 = 동시 연결 상한(24)이라 응답을 마친 연결이 풀로 돌아와 대기 요청에 바로 넘어가는 구조를 보인다.
# 타입 스펙: type-flowchart — 동시 50 요청 → 사용 중 24칸 → 풀 반환 → 빈 연결 풀 24 → 결과, 아래 행에 프록시 안 대기 26. focal 은 빈 연결 풀 24.
# 사실 출처: ch08-port-exhaustion-time-wait.md 재확인(동시 50, 60초), ADR 0012 결정 2
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, ACC, WARN, OK, KR, MONO
from ddk import node

W = 960
H = 468

# 5열: 폭 합 128+168+176+168+216 = 856, 간격 4칸 × 26 = 104 → 960, 좌우 여백 0 이라 폭을 줄여 맞춘다
XA, WA = 24, 120
XB, WB = 184, 160
XC, WC = 384, 168
XD, WD = 592, 160
XE, WE = 792, 144

Y1, H_ROW = 140, 76
Y2 = 292

d = D(
    W,
    H,
    "FLOW · CH08 I3 FIX",
    "고친 뒤 연결 일생",
    "동시 50 요청 중 24개는 풀의 연결을 쓰고 26개는 프록시 안에서 기다리며, 응답을 마친 연결이 닫히지 않고 풀로 돌아와 기다리던 요청에 바로 넘어가는 흐름",
    lead="빈 연결 상한과 동시 연결 상한을 24 로 맞추었으므로 연결이 닫히지 않고 돌아와 재사용됩니다.",
)

# 위 행: 사용 중 → 반환 → 풀
node(d, XA, Y1, WA, H_ROW, "동시 50 요청", "60초 부하")
node(d, XB, Y1, WB, H_ROW, "사용 중 24칸", "칸 24 안에서 왕복")
node(d, XC, Y1, WC, H_ROW, "본문 닫기", "연결을 풀에 반환")
node(d, XD, Y1, WD, H_ROW, "빈 연결 풀 24", "닫지 않음", c=ACC, focal=True)
node(d, XE, Y1, WE, H_ROW, "TIME_WAIT 최대 24", "(v0 28,213)", c=OK)
d.t(XE + WE / 2, Y1 + H_ROW + 22, "502 0건", 13, OK, KR, "middle", 600)

# 아래 행: 프록시 안 대기
node(d, XB, Y2, WB, H_ROW, "프록시 안 대기", "약 26개 요청")

cy1 = Y1 + H_ROW / 2
for x1, x2 in ((XA + WA, XB), (XB + WB, XC), (XC + WC, XD), (XD + WD, XE)):
    d.arrow([(x1 + 3, cy1), (x2 - 3, cy1)], SOFT, "soft", 1.3)

# 동시 50 → 대기 (아래로 꺾음)
cx_a = XA + WA / 2
cy2 = Y2 + H_ROW / 2
d.arrow([(cx_a, Y1 + H_ROW + 3), (cx_a, cy2), (XB - 3, cy2)], MUTED, "ar", 1.3)
d.t(cx_a + 8, (Y1 + H_ROW + cy2) / 2 + 4, "24 초과", 12, MUTED, KR, "start")

# 풀 → 대기 요청에 즉시 재사용 (대기 → 풀 방향)
px = XD + WD / 2
d.arrow([(XB + WB + 3, cy2), (px, cy2), (px, Y1 + H_ROW + 3)], WARN, "warn", 1.3)
d.t((XB + WB + px) / 2, cy2 - 10, "빈 칸 즉시 재사용", 12, WARN, KR, "middle", 600)

d.legend(404, [("핵심 상한 (focal)", ACC), ("차례를 기다리는 요청", WARN), ("정상 결과", OK)])

d.save("01-01-i3-fix.svg")
