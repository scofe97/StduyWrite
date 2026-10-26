"""되감기·요약(/compact)·새 세션 중 무엇을 고를지 판정 질문과 답.

# 타입 스펙: type-flowchart
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 840, 560
d = D(
    W, H,
    "DECISION FLOW · REWIND OR COMPACT",
    "상황별 되감기·요약·새 세션 선택 판단 흐름",
    "구현 실패·컨텍스트 용량 부족·목표 달성 여부에 따른 상황별 대처",
    lead="구현이 틀어지면 되감고, 용량이 부족하면 압축하며, 목표를 마치면 새 세션을 엽니다 (예시 판단 순서)"
)

CX = 230
RX = 570
BW = 250
BH = 44

def oval(x, y, w, h, title, sub=None, fill=PAPER2, stroke=RULE, sw=1.0, is_coral=False, title_c=INK):
    if is_coral:
        d.tone(x, y, w, h, ACC, r=20, op="16", sw=1.4)
        c_t = ACC
    else:
        d.box(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=20)
        c_t = title_c
    d.t(x + w / 2, y + (18 if sub else h / 2 + 5), title, 12.5, c_t, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 33, sub, 11, INK if is_coral else MUTED, KR, "middle")

def dia(cx, cy, w, h, txt):
    d.o.append(f'<path d="M {cx} {cy - h / 2} L {cx + w / 2} {cy} '
               f'L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, txt, 12, INK, KR, "middle", 600)

DW = 160
DH = 50

# 1. 화살표 (선 먼저)
# 시작 -> D1
d.arrow([(CX, 136), (CX, 172)], MUTED, "ar", 1.3)

# D1 Yes (우측)
d.arrow([(CX + DW / 2, 198), (RX - BW / 2, 198)], ACC, "acc", 1.5)
d.chip(CX + 120, 188, "예", ACC, 11, 4)

# D1 No (아래)
d.arrow([(CX, 198 + DH / 2), (CX, 288 - DH / 2)], MUTED, "ar", 1.3)
d.chip(CX + 24, 243, "아니오", MUTED, 11, 4)

# D2 Yes (우측 - Focal!)
d.arrow([(CX + DW / 2, 288), (RX - BW / 2, 288)], WARN, "warn", 1.3)
d.chip(CX + 120, 278, "예", WARN, 11, 4)

# D2 No (아래)
d.arrow([(CX, 288 + DH / 2), (CX, 378 - DH / 2)], MUTED, "ar", 1.3)
d.chip(CX + 24, 333, "아니오", MUTED, 11, 4)

# D3 Yes (우측)
d.arrow([(CX + DW / 2, 378), (RX - BW / 2, 378)], OK, "ok", 1.3)
d.chip(CX + 120, 368, "예", OK, 11, 4)

# D3 No (아래)
d.arrow([(CX, 378 + DH / 2), (CX, 442)], MUTED, "ar", 1.3)
d.chip(CX + 24, 423, "아니오", MUTED, 11, 4)

# 2. 시작 노드 (Oval)
oval(CX - 110, 96, 220, 40, "작업 상태 및 컨텍스트 점검", "예시 판단 순서")

# 3. 판단 다이아몬드 노드 (3단계)
dia(CX, 198, DW, DH, "최근 구현·방향 실패?")
dia(CX, 288, DW, DH, "컨텍스트 공간 부족?")
dia(CX, 378, DW, DH, "목표 기능 검증 완료?")

# 4. 결과 노드 (우측 Oval 분기들)
# 분기 1: 새 세션 시작
oval(RX - BW / 2, 176, BW, BH, "되감기 (Rewind)", "Esc 두 번 · 문제 직전 체크포인트", is_coral=True)

# 분기 2: 되감기 (Focal!)
oval(RX - BW / 2, 266, BW, BH, "요약 압축 (/compact)", "대화 이력 요약", stroke=WARN, sw=1.1, title_c=WARN)

# 분기 3: 요약 압축
oval(RX - BW / 2, 356, BW, BH, "새 세션 시작", "커밋 후 새 세션", stroke=OK, sw=1.1, title_c=OK)

# 5. 기본 진행 노드 (하단 Oval)
oval(CX - 110, 442, 220, BH, "현재 세션 작업 지속", "기존 컨텍스트 유지 루프")

# 6. 범례
d.legend(514, [
    ("오류 복구 되감기 (Focal)", ACC),
    ("목표 달성 새 세션", OK),
    ("컨텍스트 요약 압축", WARN),
    ("세션 유지", MUTED),
])

out_path = _HERE.parent / "05-01.rewind-or-compact.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
