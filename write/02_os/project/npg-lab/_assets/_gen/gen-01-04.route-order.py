# 01-04-route-order — 첫 일치 규칙 순서와 가려진 라우트 분기 대조
# 본문 요구: 같은 요청 /v1/devices 가 두 규칙 목록을 지나는 두 줄: 위 줄 첫 일치(매처 없는 docs 라우트가 0번 → 404 docs, npgproxy 0건), 아래 줄 ADR 0016 의 순서(매처 있는 것 앞, 매처 없는 것 맨 끝 하나 → npgproxy 200). 각 규칙 칸에 통과·잡힘·건너뜀 표시. 최장 접두사 일치는 오른쪽 작은 대조 칸 하나(라우팅 표·Go ServeMux). focal 은 위 줄의 잡힌 자리.
# 타입 스펙: type-flowchart
# 사실 출처: 01-04.리버스 프록시 앞단 층 — 규칙 고르기·전달 헤더 신뢰·건강 검사.md:47-56, ADR 0016:9-25,57-62, ch10-e2-route-order.md:8-11,65-71, server.go:2551-2553
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, BAD, INFO, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "FLOWCHART · ROUTE EVALUATION TRACES",
    "첫 일치 규칙 순서와 가려진 라우트 분기",
    "같은 /v1/devices 요청이 매처 없는 0번 라우트에 잡혀 404가 되는 위 줄과 매처 순서로 200을 얻는 아래 줄 대조",
    lead="순서가 곧 의미인 첫 일치에서는 매처 있는 규칙을 앞에 두고, 매처 없는 규칙은 맨 끝에 둡니다.",
)

# 상단 구분선 (4의 배수 y=92)
d.line(24, 92, 936, 92, RULE, 0.8)

# 1. 왼쪽 공통 요청 상자 (x=24, y=200, w=112, h=100)
d.box(24, 200, 112, 100, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(80, 228, "동일 요청", 13, INK, KR, "middle", 600)
d.t(80, 252, "/v1/devices", 12, INK, MONO, "middle")
d.t(80, 276, "두 목록 평가", 11, MUTED, KR, "middle")

# 2. 위 줄: 첫 일치 E2 변형 1 (y=108..232)
d.t(176, 122, "위 줄: 첫 일치 (docs 0번)", 12, MUTED, KR, "start", 600)

# routes[0] docs 라우트 — FOCAL (accent 테두리 + tone)
d.tone(176, 136, 208, 84, ACC, r=6, op="14", sw=1.6)
d.t(280, 162, "0번 · docs 라우트", 13, ACC, KR, "middle", 600)
d.t(280, 184, "매처 없음", 12, INK, KR, "middle")
d.t(280, 204, "잡힘 · 404 docs 종결", 11, BAD, KR, "middle", 600)

# 위 줄 결과 상자 (x=696, y=146, w=84, h=64)
d.box(696, 146, 84, 64, fill=PAPER2, stroke=BAD, sw=1.2, r=6)
d.t(738, 172, "404 docs", 13, BAD, MONO, "middle", 600)
d.t(738, 194, "npg 0건", 11, MUTED, KR, "middle")

# routes[0] -> 결과 화살표 (우회 직각 경로)
d.arrow([(384, 160), (416, 160), (416, 124), (672, 124), (672, 178), (696, 178)], c=BAD, m="bad", sw=1.4)
d.t(544, 116, "404 docs", 11, BAD, MONO, "middle")

# routes[0] 와 routes[1] 사이 미도달 표시
d.line(384, 188, 448, 188, c=BAD, sw=1.2, dash="3 3")
d.t(416, 180, "미도달", 11, BAD, KR, "middle")

# routes[1] npg 라우트 (가려짐)
d.box(448, 136, 208, 84, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
d.t(552, 162, "1번 · npg 라우트", 13, MUTED, KR, "middle", 600)
d.t(552, 184, "매처 없음", 12, MUTED, KR, "middle")
d.t(552, 204, "건너뜀 · 가려진 규칙", 11, BAD, KR, "middle", 600)

# 3. 가운데 구분선 (대시선)
d.line(176, 240, 780, 240, RULE, 0.6, dash="4 4")

# 4. 아래 줄: ADR 0016 순서 (y=252..384)
d.t(176, 266, "아래 줄: ADR 0016 순서", 12, MUTED, KR, "start", 600)

# routes[0] docs 라우트 (매처 있음)
d.box(176, 280, 208, 84, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(280, 306, "0번 · docs 라우트", 13, INK, KR, "middle", 600)
d.t(280, 328, "매처 /docs/*", 12, MUTED, MONO, "middle")
d.t(280, 348, "통과 · 불일치", 11, OK, KR, "middle", 600)

# routes[0] -> routes[1] 통과 화살표
d.arrow([(384, 322), (448, 322)], c=OK, m="ok", sw=1.4)
d.t(416, 312, "통과", 11, OK, KR, "middle")

# routes[1] npg 라우트 (정상 매칭)
d.box(448, 280, 208, 84, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(552, 306, "1번 · npg 라우트", 13, OK, KR, "middle", 600)
d.t(552, 328, "매처 없음", 12, INK, KR, "middle")
d.t(552, 348, "잡힘 · 정상 전달", 11, OK, KR, "middle", 600)

# routes[1] -> 아래 줄 결과 화살표
d.arrow([(656, 322), (696, 322)], c=OK, m="ok", sw=1.4)
d.t(676, 312, "전달", 11, OK, KR, "middle")

# 아래 줄 결과 상자 (x=696, y=290, w=84, h=64)
d.box(696, 290, 84, 64, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(738, 316, "200 OK", 13, OK, MONO, "middle", 600)
d.t(738, 338, "npg 200", 11, OK, KR, "middle")

# 왼쪽 공통 요청 상자에서 분기하는 화살표 (직각)
d.arrow([(136, 230), (156, 230), (156, 178), (176, 178)], c=MUTED, m="ar", sw=1.4)
d.arrow([(136, 270), (156, 270), (156, 322), (176, 322)], c=MUTED, m="ar", sw=1.4)

# 5. 오른쪽 최장 접두사 일치 대조 칸 (x=816, y=104, w=120, h=320)
d.box(816, 104, 120, 320, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.t(876, 128, "대조 · 최장 접두사", 12, INFO, KR, "middle", 600)
d.line(828, 140, 924, 140, RULE, 0.8)

d.t(876, 168, "라우팅 표", 12, INK, KR, "middle", 600)
d.t(876, 190, "longest prefix", 11, MUTED, MONO, "middle")
d.line(836, 208, 916, 208, RULE, 0.8)

d.t(876, 236, "Go ServeMux", 12, INK, KR, "middle", 600)
d.t(876, 258, "구체적 패턴 우선", 11, MUTED, KR, "middle")
d.line(836, 276, 916, 276, RULE, 0.8)

d.t(876, 310, "작성 순서 무관", 12, OK, KR, "middle", 600)
d.t(876, 336, "가려짐 없음", 11, OK, KR, "middle")

# 범례
d.legend(
    444,
    [
        ("위 줄 focal 잡힘", ACC),
        ("정상 일치 · 통과", OK),
        ("미도달 · 가려짐", BAD),
        ("최장 접두사 대조", INFO),
    ],
)

d.save(str(ASSETS_DIR / "01-04-route-order.svg"))
