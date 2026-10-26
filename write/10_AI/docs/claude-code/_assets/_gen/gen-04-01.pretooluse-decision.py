"""PreToolUse 이벤트의 의사결정(allow/deny/ask/defer) 분기와 우선순위 흐름.

# 타입 스펙: type-flowchart
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 780, 560
d = D(
    W, H,
    "PRETOOLUSE DECISION · PRECEDENCE PIPELINE",
    "PreToolUse 판정 우선순위와 의사결정 흐름",
    "다중 훅이 경합할 때의 판정 평가 순서 (deny > defer > ask > allow)",
    lead="여러 훅의 판정이 충돌할 때 시스템은 가장 안전한 차단 규칙부터 순서대로 평가합니다"
)

CX = 200
RX = 420
BW = 300
BH = 44

def oval(x, y, w, h, title, sub=None, fill=PAPER2, stroke=RULE, sw=1.0, is_coral=False):
    if is_coral:
        d.tone(x, y, w, h, ACC, r=20, op="18", sw=1.4)
        c_title, c_sub = ACC, ACC
    else:
        d.box(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=20)
        c_title, c_sub = INK, MUTED
    d.t(x + w / 2, y + (18 if sub else h / 2 + 5), title, 12.5, c_title, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 33, sub, 11, c_sub, MONO if ":" in sub or "deny" in sub or "allow" in sub or "ask" in sub or "defer" in sub else KR, "middle")

def dia(cx, cy, w, h, txt):
    d.o.append(f'<path d="M {cx} {cy - h / 2} L {cx + w / 2} {cy} '
               f'L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, txt, 12, INK, KR, "middle", 600)

# 1. 연결 화살표 (선 먼저 그리기)
# 시작 → D1 (길이: 166 - 126 = 40px)
d.arrow([(CX, 126), (CX, 166)], MUTED, "ar", 1.3)

# D1 분기 (cy=192, 수평: 285 -> 420, 길이 135px)
d.arrow([(CX + 85, 192), (RX, 192)], BAD, "bad", 1.3)
d.chip(CX + 115, 182, "예", BAD, 11, 4)

# D1 -> D2 (218 -> 270, 길이 52px)
d.arrow([(CX, 218), (CX, 270)], MUTED, "ar", 1.3)
d.chip(CX + 24, 244, "아니오", MUTED, 11, 4)

# D2 분기 (cy=296, 수평: 285 -> 420, 길이 135px)
d.arrow([(CX + 85, 296), (RX, 296)], WARN, "warn", 1.3)
d.chip(CX + 115, 286, "예", WARN, 11, 4)

# D2 -> D3 (322 -> 374, 길이 52px)
d.arrow([(CX, 322), (CX, 374)], MUTED, "ar", 1.3)
d.chip(CX + 24, 348, "아니오", MUTED, 11, 4)

# D3 분기 (cy=400, 수평: 285 -> 420, 길이 135px)
d.arrow([(CX + 85, 400), (RX, 400)], INFO, "info", 1.3)
d.chip(CX + 115, 390, "예", INFO, 11, 4)

# D3 -> 최종 (426 -> 476, 길이 50px)
d.arrow([(CX, 426), (CX, 476)], OK, "ok", 1.3)
d.chip(CX + 24, 451, "아니오", OK, 11, 4)

# 2. 시작 노드 (Oval)
oval(CX - 100, 86, 200, 40, "PreToolUse 판정 수집", "다중 훅 반환값 취합")

# 3. 판단 다이아몬드 (순서: deny > defer > ask)
dia(CX, 192, 170, 52, "deny 포함 여부")
dia(CX, 296, 170, 52, "defer 포함 여부")
dia(CX, 400, 170, 52, "ask 포함 여부")

# 4. 판정 결과 노드 (우측 결과들: Oval)
oval(RX, 170, BW, BH, "도구 호출 차단", 'deny 확정 · Claude 사유 전달', stroke=BAD, sw=1.1)
oval(RX, 274, BW, BH, "도구 실행 지연", 'defer 확정 · -p 모드·단일 호출 · 재개 가능', stroke=WARN, sw=1.1)
oval(RX, 378, BW, BH, "사용자 승인 요청", 'ask 확정 · 대화상자 확인', stroke=INFO, sw=1.1)

# 5. 최종 Happy path (하단 결과: Oval with Coral Accent)
oval(CX - 150, 476, 300, BH, "권한 프롬프트 생략", 'allow 확정 · deny·ask 규칙 별도 평가', is_coral=True)

out_path = _HERE.parent / "04-01.pretooluse-decision.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
