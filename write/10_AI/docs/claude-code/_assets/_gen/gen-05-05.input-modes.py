# 사실 출처: 05-05.Interactive Features·Output Styles·Status Line·Settings.md:52-160 · 원문 chunk-05-05.md:221-269
# 타입 스펙: type-state
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 460
d = D(
    W, H,
    "INTERACTIVE INPUT · STATE MACHINE",
    "대화형 입력 모드 전이 구조",
    "Vim 조작 모드와 Bash·음성 입력 간의 키 입력 전이와 복귀 경로",
    lead="키 입력과 이벤트에 따라 입력·Bash·음성 입력 상태로 전이되며, Vim 모드를 켜면 일반·비주얼 상태가 더해집니다"
)

# 1. 시작 마커 (세션 진입)
d.t(490, 102, "세션 진입", 11, SOFT, fam=KR, anchor="middle", weight=600)
d.o.append(f'<circle cx="490" cy="116" r="5" fill="{INK}"/>')
d.arrow([(490, 122), (490, 174)], MUTED, "ar", 1.4)

# 2. 전이 화살표 및 라벨 (겹치는 구간을 수평 평행선으로, 라벨은 선 바깥에)

# Visual <-> Normal (수직 전이)
d.arrow([(190, 258), (190, 186)], MUTED, "ar", 1.4)
d.t(162, 226, "v · V", 11, MUTED, fam=MONO, anchor="middle")
d.arrow([(250, 186), (250, 258)], MUTED, "ar", 1.4)
d.t(290, 226, "Esc · y · d", 11, MUTED, fam=MONO, anchor="middle")

# Visual -> Insert (c 치환, 직각)
d.arrow([(300, 152), (450, 152), (450, 174)], MUTED, "ar", 1.4)
d.t(375, 144, "c (치환)", 11, MUTED, fam=KR, anchor="middle")

# Normal <-> Insert
d.arrow([(410, 268), (302, 268)], MUTED, "ar", 1.4)
d.t(376, 260, "Esc", 11, MUTED, fam=MONO, anchor="middle")
d.arrow([(300, 286), (408, 286)], OK, "ok", 1.4)
d.t(376, 304, "i · a · o", 11, OK, fam=MONO, anchor="middle")

# Insert <-> Bash
d.arrow([(570, 186), (678, 186)], INFO, "info", 1.4)
d.t(624, 178, "! 접두사", 11, INFO, fam=KR, anchor="middle")
d.arrow([(680, 204), (572, 204)], MUTED, "ar", 1.4)
d.t(626, 222, "Enter 실행", 11, MUTED, fam=KR, anchor="middle")

# Insert <-> Voice
d.arrow([(570, 268), (678, 268)], ACC, "acc", 1.4)
d.t(624, 260, "키 누름", 11, ACC, fam=KR, anchor="middle")
d.arrow([(680, 286), (572, 286)], OK, "ok", 1.4)
d.t(626, 304, "키 놓음", 11, OK, fam=KR, anchor="middle")

# 3. 상태 노드 박스
# Vim 모드를 켠 경우에만 있는 상태 묶음 (점선)
d.o.append(f'<rect x="124" y="96" width="216" height="244" rx="10" fill="none" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="5 4"/>')
d.t(134, 112, "Vim 모드 켠 경우", 11, SOFT, fam=KR, anchor="start", weight=600)

d.box(140, 120, 160, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(220, 146, "비주얼 모드 (Visual)", 13, INK, fam=KR, anchor="middle", weight=600)
d.t(220, 168, "텍스트 선택 (v · V)", 11, MUTED, fam=KR, anchor="middle")

d.box(140, 258, 160, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(220, 284, "일반 모드 (Normal)", 13, INK, fam=KR, anchor="middle", weight=600)
d.t(220, 306, "커서 이동 · Vim 명령", 11, MUTED, fam=KR, anchor="middle")

d.tone(410, 176, 160, 120, ACC, r=8, op="16", sw=1.4)
d.t(490, 230, "입력 모드 (Insert)", 14, ACC, fam=KR, anchor="middle", weight=600)
d.t(490, 252, "프롬프트 작성 · 편집", 11, INK, fam=KR, anchor="middle")

d.box(680, 150, 160, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(760, 176, "Bash 모드", 13, INK, fam=KR, anchor="middle", weight=600)
d.t(760, 198, "! 셸 명령 즉시 실행", 11, MUTED, fam=KR, anchor="middle")

d.box(680, 258, 160, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(760, 284, "음성 입력 (Voice)", 13, INK, fam=KR, anchor="middle", weight=600)
d.t(760, 306, "푸시투톡 녹음", 11, MUTED, fam=KR, anchor="middle")

# 4. 범례
d.legend(396, [
    ("기본 입력 상태 (Focal)", ACC),
    ("Vim 조작 모드", MUTED),
    ("셸 · 음성 입력 모드", INFO),
    ("복귀 및 완료 전이", OK),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05-05.input-modes.svg"))
d.save(out)
print(f"saved: {out}")
