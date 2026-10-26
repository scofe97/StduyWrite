"""사용자 직접 호출, 모델 자동 실행, context: fork 격리 실행 여부를 가르는 결정 트리.

# 타입 스펙: type-flowchart
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, INFO, INK, SOFT, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 700
d = D(
    W, H,
    "INVOCATION DECISION",
    "스킬 호출 방식과 실행 모드 결정 트리",
    "disable-model-invocation, user-invocable, context: fork 키 값에 따른 실행 분기",
    lead="부작용 방지와 컨텍스트 보호를 위해 호출 권한과 실행 환경을 분리합니다"
)

CX = 320
RX = 700
BW = 240
BH = 48
DH = 52
DW = 336

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
    d.t(x + w / 2, y + (20 if sub else h / 2 + 5), txt, 12, tc, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 36, sub, 12, sc, KR, "middle")

# 1. 시작 노드
oval(CX - 88, 104, 176, 36, "스킬 정의 및 호출 요청")
d.arrow([(CX, 140), (CX, 176)], MUTED, "ar")

# 2. 결정 1: disable-model-invocation
dia(CX, 202, DW, DH, "disable-model-invocation: true ?")
# Yes -> 오른쪽
d.arrow([(CX + DW / 2, 202), (RX - BW / 2, 202)], MUTED, "ar")
d.t((CX + DW / 2 + RX - BW / 2) / 2, 192, "예", 12, MUTED, KR, "middle")
step(RX - BW / 2, 178, BW, BH, "사용자 직접 호출만 허용", "부작용 방지 (/commit · /deploy)", c=INFO)

# No -> 아래
d.arrow([(CX, 228), (CX, 268)], MUTED, "ar")
d.t(CX + 14, 250, "아니오", 12, MUTED, KR, "start")

# 3. 결정 2: user-invocable
dia(CX, 294, DW, DH, "user-invocable: false ?")
# Yes -> 오른쪽
d.arrow([(CX + DW / 2, 294), (RX - BW / 2, 294)], MUTED, "ar")
d.t((CX + DW / 2 + RX - BW / 2) / 2, 284, "예", 12, MUTED, KR, "middle")
step(RX - BW / 2, 270, BW, BH, "모델 자동 실행만 허용", "슬래시 메뉴 숨김 (배경 지식)", c=INFO)

# No -> 아래
d.arrow([(CX, 320), (CX, 360)], MUTED, "ar")
d.t(CX + 14, 342, "아니오", 12, MUTED, KR, "start")

# 4. 기본 동작
step(CX - BW / 2, 360, BW, BH, "양방향 호출 허용", "사용자 명령 및 모델 자동 매칭", c=INFO)

# 경로 합류 (우측 분기 라인 -> 중앙 결합)
d.path(f"M {RX + BW / 2} 202 L 840 202 L 840 444 L {CX} 444", MUTED, 1.0)
d.path(f"M {RX + BW / 2} 294 L 840 294", MUTED, 1.0)
d.line(CX, 408, CX, 444, RULE, 1.0)
# 합류 점
d.o.append(f'<circle cx="{CX}" cy="444" r="4" fill="{INK}"/>')

# 합류 후 진행
d.arrow([(CX, 444), (CX, 480)], MUTED, "ar")

# 5. 결정 3: context: fork
dia(CX, 506, DW, DH, "context: fork 선언 ?")
# Yes -> 서브에이전트 (focal)
d.arrow([(CX + DW / 2, 506), (RX - BW / 2, 506)], ACC, "acc", sw=1.4)
d.t((CX + DW / 2 + RX - BW / 2) / 2, 496, "예", 12, ACC, KR, "middle", 600)
step(RX - BW / 2, 482, BW, BH, "서브에이전트 격리 실행", "독립 컨텍스트 · 결과만 반환", focal=True)

# No -> 메인 세션 직접 실행
d.arrow([(CX, 532), (CX, 572)], MUTED, "ar")
d.t(CX + 14, 554, "아니오", 12, MUTED, KR, "start")
step(CX - BW / 2, 572, BW, BH, "메인 세션 직접 실행", "대화 컨텍스트에 본문 로드", c=RULE)

# 범례
d.legend(644, [("서브에이전트 격리 실행 (focal)", ACC), ("호출 모드 및 일반 실행", INFO), ("판정 분기 및 기본 흐름", MUTED)])
d.save("03-01.invocation-decision.svg")
