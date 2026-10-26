"""동적 도구 검색과 alwaysLoad 설정에 따른 도구 컨텍스트 적재 결정 흐름.

# 타입 스펙: type-flowchart
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, INFO, WARN, INK, SOFT, PAPER2, RULE, KR, MONO

W, H = 920, 672
d = D(
    W, H,
    "MCP TOOL SEARCH DECISION",
    "동적 도구 검색과 alwaysLoad 설정에 따른 컨텍스트 적재 흐름",
    "alwaysLoad 설정 및 ENABLE_TOOL_SEARCH 모드에 따른 도구 명세 적재 분기",
    lead="컨텍스트 낭비를 막기 위해 온디맨드 검색을 기본으로 하되 핵심 도구는 사전 로드합니다"
)

CX = 280
RX = 690
BW = 264
BH = 46
DH = 50

def oval(x, y, w, h, txt):
    d.box(x, y, w, h, fill=PAPER2, stroke=RULE, sw=1.1, r=18)
    d.t(x + w / 2, y + h / 2 + 5, txt, 12, INK, KR, "middle", 600)

def dia(cx, cy, w, h, txt):
    d.o.append(f'<path d="M {cx} {cy - h / 2} L {cx + w / 2} {cy} '
               f'L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(cx, cy + 5, txt, 12, INK, MONO if ":" in txt else KR, "middle", 600)

def step(x, y, w, h, txt, sub=None, c=RULE, sw=1.0, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, r=6, op="14", sw=1.4)
    else:
        d.box(x, y, w, h, fill=PAPER2, stroke=c, sw=sw, r=6)
    tc = ACC if focal else INK
    sc = ACC if focal else MUTED
    d.t(x + w / 2, y + (19 if sub else h / 2 + 5), txt, 12, tc, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 35, sub, 12, sc, KR, "middle")

# 1. 시작 노드
oval(CX - 88, 104, 176, 36, "MCP 도구 적재 판정")
d.arrow([(CX, 140), (CX, 165)], MUTED, "ar")

# 2. 결정 1: alwaysLoad: true
dia(CX, 190, BW, DH, "alwaysLoad: true ?")
d.arrow([(CX + BW / 2, 190), (RX - BW / 2, 190)], MUTED, "ar")
d.t((CX + BW / 2 + RX - BW / 2) / 2, 180, "예", 12, MUTED, KR, "middle")
step(RX - BW / 2, 167, BW, BH, "상시 사전 로드 (검색 우회)", "컨텍스트 항시 유지", c=INFO)

d.arrow([(CX, 215), (CX, 255)], MUTED, "ar")
d.t(CX + 14, 238, "아니오", 12, MUTED, KR, "start")

# 3. 결정 2: alwaysLoad: false
dia(CX, 280, BW, DH, "ENABLE_TOOL_SEARCH: false ?")
d.arrow([(CX + BW / 2, 280), (RX - BW / 2, 280)], MUTED, "ar")
d.t((CX + BW / 2 + RX - BW / 2) / 2, 270, "예", 12, MUTED, KR, "middle")
step(RX - BW / 2, 257, BW, BH, "전체 사전 전송 (검색 비활성)", "모든 도구 명세 초반 전송", c=WARN)

d.arrow([(CX, 305), (CX, 345)], MUTED, "ar")
d.t(CX + 14, 328, "아니오", 12, MUTED, KR, "start")

# 4. 결정 3: ENABLE_TOOL_SEARCH: false
dia(CX, 370, BW, DH, "alwaysLoad: false ?")
d.arrow([(CX + BW / 2, 370), (RX - BW / 2, 370)], ACC, "acc")
d.t((CX + BW / 2 + RX - BW / 2) / 2, 360, "예", 12, ACC, KR, "middle", 600)
step(RX - BW / 2, 347, BW, BH, "지연 적재 강제 (검색 대상)", "도구 정의 온디맨드 탐색", c=ACC, focal=True)

d.arrow([(CX, 395), (CX, 435)], MUTED, "ar")
d.t(CX + 14, 418, "아니오", 12, MUTED, KR, "start")

# 5. 결정 4: ENABLE_TOOL_SEARCH: auto
dia(CX, 460, BW, DH, "ENABLE_TOOL_SEARCH: auto ?")
d.arrow([(CX + BW / 2, 460), (RX - BW / 2, 460)], MUTED, "ar")
d.t((CX + BW / 2 + RX - BW / 2) / 2, 450, "예", 12, MUTED, KR, "middle")
step(RX - BW / 2, 437, BW, BH, "임계치 기반 적재 (10%)", "용량 도달 시 지연 전환", c=INFO)

# 6. 기본값 / true -> 온디맨드 도구 검색 (focal)
d.arrow([(CX, 485), (CX, 526)], ACC, "acc", sw=1.4)
d.t(CX + 14, 508, "기본값 / true", 12, ACC, KR, "start", 600)
step(CX - BW / 2, 526, BW, BH, "온디맨드 도구 검색 (기본값)", "모델 요청 시점에만 명세 로드", c=ACC, focal=True)

d.legend(608, [
    ("온디맨드 도구 검색 및 지연 적재 (Focal)", ACC),
    ("사전 로드 및 임계치 적재", INFO),
    ("도구 검색 비활성화", WARN)
])

d.save("03-03.tool-search.svg")
