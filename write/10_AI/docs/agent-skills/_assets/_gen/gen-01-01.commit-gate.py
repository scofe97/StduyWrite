"""스킬 커밋 관문의 판정과 실행 흐름."""
# 타입 스펙: type-flowchart
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 868
d = D(
    W, H,
    "PRE-COMMIT HOOK · DECISION FLOWCHART",
    "스킬 커밋 관문의 판정 흐름과 분기 논리",
    "staged 경로 감지부터 corepack 확인, 검증 명령 실행 및 통과 문구 대조까지의 제어",
    lead="스킬 경로가 staged일 때만 corepack 환경과 검증 명령 및 통과 문구를 엄격히 확인합니다"
)

# 보조 함수
def oval(x, y, w, h, title, sub=None, c=MUTED, fill=PAPER2, sw=1.2, is_coral=False):
    if is_coral:
        d.tone(x, y, w, h, ACC, r=h // 2, op="18", sw=1.4)
        tc = ACC
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h // 2}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')
        tc = c if c in (OK, BAD, INFO) else INK
    d.t(x + w / 2, y + (16 if sub else h / 2 + 5), title, 13, tc, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 33, sub, 12, MUTED, MONO if any(ch.isascii() and ch.isalnum() for ch in sub) else KR, "middle")

def rect_box(x, y, w, h, title, sub=None, c=RULE, fill=PAPER2, sw=1.2, is_coral=False):
    if is_coral:
        d.tone(x, y, w, h, ACC, r=6, op="18", sw=1.5)
        tc = ACC
    else:
        d.box(x, y, w, h, fill=fill, stroke=c, sw=sw, r=6)
        tc = INK
    d.t(x + w / 2, y + (18 if sub else h / 2 + 5), title, 13, tc, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 36, sub, 12, MUTED, MONO, "middle")

def diamond(cx, cy, hw, hh, title, sub=None, c=RULE):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + (-3 if sub else 5), title, 13, INK, KR, "middle", 600)
    if sub:
        d.t(cx, cy + 15, sub, 12, MUTED, MONO, "middle")

# 기하 레이아웃 상수
CX = 400         # 메인 판단 축 X
LX = 140         # 좌측 통과/우회 축 X
RX = 720         # 우측 차단 축 X
DW, DH = 84, 32  # 마름모 반폭, 반높이 (168 x 64)
BW, BH = 176, 44 # 타원 크기

# Y 좌표 (모두 4의 배수)
Y_START = 120
Y_D1 = 216      # staged 경로 검사
Y_D2 = 328      # corepack 존재 확인
Y_ACT = 432     # 검증 실행
Y_D3 = 536      # 종료 코드 확인
Y_D4 = 648      # 통과 문구 확인
Y_END = 752     # 최종 통과 타원
Y_LEG = 824     # 범례 기준선

# ── 화살표 (선 먼저) ───────────────────────────────────

# 1. Start -> D1 (수직 하향)
d.arrow([(CX, Y_START + 22), (CX, Y_D1 - DH)], MUTED, "ar", 1.4)

# 2. Start -> 우회 (--no-verify)
d.path(f"M {CX - 75} {Y_START} L {LX} {Y_START} L {LX} {Y_D1 - BH // 2 - 4}", INFO, 1.4, m="info")
d.chip((CX - 75 + LX) / 2, Y_START - 14, "--no-verify", INFO, 12)

# 3. D1 아니오 -> 무관한 커밋 통과 (좌측 수평)
d.path(f"M {CX - DW} {Y_D1} L {LX + BW // 2 + 4} {Y_D1}", OK, 1.4, m="ok")
d.chip((CX - DW + LX + BW // 2) / 2, Y_D1 - 14, "아니오", MUTED, 12)

# 4. D1 예 -> D2 (수직 하향)
d.arrow([(CX, Y_D1 + DH), (CX, Y_D2 - DH)], MUTED, "ar", 1.4)
d.chip(CX + 28, (Y_D1 + DH + Y_D2 - DH) / 2, "예", MUTED, 12)

# 5. D2 아니오 -> 환경 미비 차단 (우측 수평)
d.path(f"M {CX + DW} {Y_D2} L {RX - BW // 2 - 4} {Y_D2}", BAD, 1.4, m="bad")
d.chip((CX + DW + RX - BW // 2) / 2, Y_D2 - 14, "아니오", BAD, 12)

# 6. D2 예 -> Action (수직 하향)
d.arrow([(CX, Y_D2 + DH), (CX, Y_ACT - 24)], MUTED, "ar", 1.4)
d.chip(CX + 28, (Y_D2 + DH + Y_ACT - 24) / 2, "예", MUTED, 12)

# 7. Action -> D3 (수직 하향)
d.arrow([(CX, Y_ACT + 24), (CX, Y_D3 - DH)], ACC, "acc", 1.4)

# 8. D3 아니오 -> 검증 오류 차단 (우측 수평)
d.path(f"M {CX + DW} {Y_D3} L {RX - BW // 2 - 4} {Y_D3}", BAD, 1.4, m="bad")
d.chip((CX + DW + RX - BW // 2) / 2, Y_D3 - 14, "아니오", BAD, 12)

# 9. D3 예 -> D4 (수직 하향)
d.arrow([(CX, Y_D3 + DH), (CX, Y_D4 - DH)], MUTED, "ar", 1.4)
d.chip(CX + 28, (Y_D3 + DH + Y_D4 - DH) / 2, "예", MUTED, 12)

# 10. D4 아니오 -> 문구 누락 차단 (우측 수평)
d.path(f"M {CX + DW} {Y_D4} L {RX - BW // 2 - 4} {Y_D4}", BAD, 1.4, m="bad")
d.chip((CX + DW + RX - BW // 2) / 2, Y_D4 - 14, "아니오", BAD, 12)

# 11. D4 예 -> 최종 통과 (수직 하향)
d.arrow([(CX, Y_D4 + DH), (CX, Y_END - 22)], OK, "ok", 1.5)
d.chip(CX + 28, (Y_D4 + DH + Y_END - 22) / 2, "예", OK, 12)

# ── 노드 그리기 ─────────────────────────────────────────

# 시작 노드
oval(CX - 75, Y_START - 22, 150, 44, "git commit", "커밋 실행", MUTED)

# D1: staged 경로 검사
diamond(CX, Y_D1, DW, DH, "스킬 경로 staged?", "diff --cached", RULE)

# 좌측 통과 노드
oval(LX - BW // 2, Y_D1 - BH // 2, BW, BH, "커밋 진행 (exit 0)", "스킬 미포함 커밋", OK)

# D2: corepack 확인
diamond(CX, Y_D2, DW, DH, "corepack 확인", "command -v", RULE)

# 우측 차단 1: corepack 미비
oval(RX - BW // 2, Y_D2 - BH // 2, BW, BH, "커밋 차단 (exit 1)", "환경 미비", BAD)

# Action: 검증 실행 (Focal!)
rect_box(CX - 140, Y_ACT - 24, 280, 48, "검증 및 README 검사", "validate & check", ACC, is_coral=True)

# D3: 종료 코드 확인
diamond(CX, Y_D3, DW, DH, "종료 코드 0?", "status == 0", RULE)

# 우측 차단 2: 검증 오류
oval(RX - BW // 2, Y_D3 - BH // 2, BW, BH, "커밋 차단 (exit 1)", "검증 실패", BAD)

# D4: 통과 문구 확인
diamond(CX, Y_D4, DW, DH, "통과 문구 2종 대조?", "passed & up to date", RULE)

# 우측 차단 3: 문구 누락
oval(RX - BW // 2, Y_D4 - BH // 2, BW, BH, "커밋 차단 (exit 1)", "문구 누락", BAD)

# 최종 통과 노드
oval(CX - BW // 2, Y_END - 22, BW, 44, "커밋 통과 (exit 0)", "검증 완료", OK)

# 범례 (Y_LEG = 824)
d.legend(Y_LEG, [
    ("통과 (exit 0)", OK),
    ("차단 (exit 1)", BAD),
    ("검증 실행 (focal)", ACC),
    ("우회 경로", INFO),
])

d.save(str(_HERE.parent / "01-01.commit-gate.svg"))
