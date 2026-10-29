# 01-01-i1-fix — 고친 뒤 요청 경로: 검색은 줄 7칸에서 거르고 단건 조회는 24칸 풀로 지나간다
# 본문 요구(01-01 I1 고친 뒤): 검색 줄 상한 7이 떠난 작업을 막고 단건 조회 경로가 살아난 구조를 보인다.
# 타입 스펙: type-flowchart — 손님 → 줄 → 풀 → 백엔드 창구 → 결과, 검색·단건 두 행. focal 은 검색 줄 7칸.
# 사실 출처: ch08-slow-search-starves-lookup.md 재확인(결정 6 뒤 10:33~10:34), ADR 0012 결정 1·2·6
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, RULE, ACC, WARN, OK, KR, MONO
from ddk import node, harrow, varrow, kr

W = 960
H = 492

# 5열: 폭 합 112+136+136+152+216 = 752, 간격 4칸 × 40 = 160, 좌우 여백 24 → 960
XA, WA = 24, 112
XB, WB = 176, 136
XC, WC = 352, 136
XD, WD = 528, 152
XE, WE = 720, 216

Y_REJ, H_REJ = 104, 52
Y_S, H_ROW = 184, 76
Y_G = 300

d = D(
    W,
    H,
    "FLOW · CH08 I1 FIX",
    "고친 뒤 요청 경로",
    "검색은 프록시 줄 7칸을 넘으면 503 UO 로 거절되고, 단건 조회는 24칸 풀로 백엔드 창구 32칸에 닿아 초당 50건 모두 200 이 되는 경로",
    lead="검색은 줄 7칸과 풀 8칸에서 걸러져 떠난 작업이 쌓이지 않고, 단건 조회는 자기 풀 24칸으로 지나갑니다.",
)

# 거절 노드와 화살표
node(d, XB, Y_REJ, WB, H_REJ, "503 (UO)", "초당 4.38건 거절", c=WARN)
varrow(d, XB + WB / 2, Y_S, Y_REJ + H_REJ, c=WARN, m="warn", label="7칸 초과")

# 검색 행
node(d, XA, Y_S, WA, H_ROW, "검색 요청", "초당 5건")
node(d, XB, Y_S, WB, H_ROW, "검색 줄", "7칸", c=ACC, focal=True)
node(d, XC, Y_S, WC, H_ROW, "검색 풀", "8칸")
node(d, XE, Y_S, WE, H_ROW, "200 · UT", "초당 0.53건 · 0.48건")
for x1, x2 in ((XA + WA, XB), (XB + WB, XC), (XC + WC, XD), (XD + WD, XE)):
    harrow(d, x1 + 3, x2 - 3, Y_S + H_ROW / 2)

# 단건 행
node(d, XA, Y_G, WA, H_ROW, "단건 조회", "초당 50건")
node(d, XB, Y_G, WB, H_ROW, "그 밖 줄", "1024칸")
node(d, XC, Y_G, WC, H_ROW, "그 밖 풀", "24칸 (단건 조회 포함)")
node(d, XE, Y_G, WE, H_ROW, "200", "초당 50건 · p99 최대 119ms", c=OK)
for x1, x2 in ((XA + WA, XB), (XB + WB, XC), (XC + WC, XD), (XD + WD, XE)):
    harrow(d, x1 + 3, x2 - 3, Y_G + H_ROW / 2)

# 백엔드 창구: 두 행에 걸친 상자
by, bh = Y_S, Y_G + H_ROW - Y_S
d.box(XD, by, WD, bh)
cx = XD + WD / 2
d.t(cx, by + bh / 2 - 22, "백엔드 창구", 14, INK, KR, "middle", 600)
d.t(cx, by + bh / 2 - 2, "동시 처리 32칸", 12, MUTED, KR, "middle")
d.t(cx, by + bh / 2 + 22, "취소 무시", 12, WARN, KR, "middle", 600)
d.t(cx, by + bh / 2 + 42, "떠난 뒤 작업 0.46/s", 12, MUTED, KR, "middle")

# 프록시 안 구간 표시
zy = Y_G + H_ROW + 20
d.line(XB, zy, XC + WC, zy, RULE, 1.0)
d.t((XB + XC + WC) / 2, zy + 20, "프록시 안 · 요청 전체 15초 기한", 12, MUTED, KR, "middle")

d.legend(zy + 40, [("핵심 상한 (focal)", ACC), ("거절 응답", WARN), ("정상 응답", OK)])

d.save("01-01-i1-fix.svg")
