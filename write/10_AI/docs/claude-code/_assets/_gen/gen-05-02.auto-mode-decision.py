"""자동 모드의 4단계 결정 순서와 폴백 전환 조건 결정 트리.

# 타입 스펙: type-flowchart
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 700
d = D(
    W, H,
    "AUTO MODE DECISION FLOW",
    "자동 모드의 판정 순서와 폴백 전환 흐름",
    "명시적 규칙부터 파일 편집, 배경 분류기 심사, 폴백 질문 전환까지의 순차 결정 트리",
    lead="명시적 규칙과 안전한 파일 작업을 먼저 거르고, 잠재적 위험 명령만 배경 분류기가 심사합니다"
)

CX = 320
RX = 700
BW = 248
BH = 48
DW = 336
DH = 52

def oval(x, y, w, h, txt):
    d.box(x, y, w, h, fill=PAPER2, stroke=RULE, sw=1.1, r=18)
    d.t(x + w / 2, y + h / 2 + 5, txt, 12.5, INK, KR, "middle", 600)

def dia(cx, cy, w, h, txt, focal=False):
    c = ACC if focal else RULE
    sw = 1.4 if focal else 1.0
    fill = f"{ACC}14" if focal else PAPER2
    d.o.append(
        f'<path d="M {cx} {cy - h / 2} L {cx + w / 2} {cy} '
        f'L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z" '
        f'fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'
    )
    tc = ACC if focal else INK
    d.t(cx, cy + 5, txt, 12, tc, KR, "middle", 600)

def step(x, y, w, h, txt, sub=None, c=RULE, sw=1.0, focal=False, is_ok=False, is_warn=False, is_bad=False):
    if focal:
        d.tone(x, y, w, h, ACC, r=6, op="14", sw=1.4)
        tc, sc = ACC, ACC
    elif is_ok:
        d.tone(x, y, w, h, OK, r=6, op="14", sw=1.2)
        tc, sc = OK, MUTED
    elif is_warn:
        d.tone(x, y, w, h, WARN, r=6, op="14", sw=1.2)
        tc, sc = WARN, MUTED
    elif is_bad:
        d.tone(x, y, w, h, BAD, r=6, op="14", sw=1.2)
        tc, sc = BAD, MUTED
    else:
        d.box(x, y, w, h, fill=PAPER2, stroke=c, sw=sw, r=6)
        tc, sc = INK, MUTED

    d.t(x + w / 2, y + (19 if sub else h / 2 + 5), txt, 12.5, tc, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 36, sub, 11, sc, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")

# 1. 시작 노드
oval(CX - 88, 100, 176, 36, "작업 실행 요청 접수")
d.arrow([(CX, 136), (CX, 168)], MUTED, "ar")

# 2. 결정 1: 명시적 규칙 (allow / deny)
dia(CX, 194, DW, DH, "1 · 명시적 allow / deny 대조")
# 일치 -> 오른쪽
d.arrow([(CX + DW / 2, 194), (RX - BW / 2, 194)], MUTED, "ar")
d.t((CX + DW / 2 + RX - BW / 2) / 2, 184, "규칙 일치", 11, MUTED, KR, "middle")
step(RX - BW / 2, 170, BW, BH, "allow·deny 규칙 즉시 적용", "예외 있음 (보호 경로 등)")

# 미일치 -> 아래
d.arrow([(CX, 220), (CX, 260)], MUTED, "ar")
d.t(CX + 14, 244, "규칙 없음", 11, MUTED, KR, "start")

# 3. 결정 2: 파일 읽기 또는 로컬 편집
dia(CX, 286, DW, DH, "2 · 파일 읽기 또는 로컬 편집?")
# 일치 -> 오른쪽
d.arrow([(CX + DW / 2, 286), (RX - BW / 2, 286)], OK, "ok", 1.4)
d.t((CX + DW / 2 + RX - BW / 2) / 2, 276, "안전 작업", 11, OK, KR, "middle")
step(RX - BW / 2, 262, BW, BH, "로컬 파일 자동 승인", "소스 읽기·편집 확인 없이 통과", is_ok=True)

# 미일치 -> 아래
d.arrow([(CX, 312), (CX, 352)], MUTED, "ar")
d.t(CX + 14, 336, "셸 명령 등", 11, MUTED, KR, "start")

# 4. 결정 3: 배경 안전 분류기 심사 (focal!)
dia(CX, 378, DW, DH, "3 · 배경 안전 분류기 심사", focal=True)
# 통과 -> 오른쪽
d.arrow([(CX + DW / 2, 378), (RX - BW / 2, 378)], ACC, "acc", 1.4)
d.t((CX + DW / 2 + RX - BW / 2) / 2, 368, "안전 판정", 11, ACC, KR, "middle", 600)
step(RX - BW / 2, 354, BW, BH, "분류기 자율 승인 실행", "의존성 설치 · 테스트 등 통과", focal=True)

# 거절 -> 아래
d.arrow([(CX, 404), (CX, 444)], WARN, "warn", 1.4)
d.t(CX + 14, 428, "위험 감지 · hard_deny 포함", 11, WARN, KR, "start")

# 5. 결정 4: 폴백 임계치 판정
dia(CX, 470, DW, DH, "차단 반복 여부 (폴백 임계치)")
# 도달 -> 오른쪽
d.arrow([(CX + DW / 2, 470), (RX - BW / 2, 470)], WARN, "warn", 1.4)
d.t((CX + DW / 2 + RX - BW / 2) / 2, 460, "임계 도달", 11, WARN, KR, "middle")
step(RX - BW / 2, 446, BW, BH, "대화형 확인 질문 전환", "연속 3회 또는 누적 20회", is_warn=True)

# 미도달 -> 아래
d.arrow([(CX, 496), (CX, 540)], BAD, "bad", 1.4)
d.t(CX + 14, 520, "임계치 미달", 11, BAD, KR, "start")

# 6. 최종 차단 노드
step(CX - BW / 2, 540, BW, BH, "위험 작업 단독 차단", "알림 · Recently denied 재시도", is_bad=True)

# 범례
d.legend(636, [
    ("배경 안전 분류기 심사 (focal)", ACC),
    ("즉시 자동 승인", OK),
    ("대화형 폴백 전환", WARN),
    ("위험 명령 차단", BAD),
])

d.save("05-02.auto-mode-decision.svg")
