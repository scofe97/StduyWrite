"""메인 세션과 서브에이전트의 컨텍스트 토큰 격리 및 결과 요약 반환 구조.

# 타입 스펙: type-architecture
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 920, 480
d = D(
    W, H,
    "CONTEXT ISOLATION ARCHITECTURE",
    "메인 세션과 서브에이전트의 컨텍스트 토큰 격리",
    "메인 세션의 대화 맥락을 보존하고 서브에이전트가 소모한 수만 토큰 중 요약 결과만 수신하는 구조",
    lead="하위 작업의 방대한 파일 탐색과 터미널 출력을 격리해 메인 세션의 토큰 고갈을 방지합니다"
)

# 1. 상단 영역: 메인 대화 세션
d.box(40, 96, 840, 136, fill=PAPER, stroke=RULE, sw=0.8, r=8)
d.box(56, 102, 148, 16, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(130, 114, "MAIN SESSION ZONE", 8, SOFT, MONO, "middle")

# 메인 좌측 카드: 사용자 지시 및 작업 계획
d.box(64, 124, 344, 96, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(236, 154, "사용자 지시 및 작업 계획", 13, INK, KR, "middle", 600)
d.t(236, 178, "핵심 목표 수립 · 작업 분할", 12, MUTED, KR, "middle")
d.t(236, 198, "핵심 대화 기록 보존", 12, SOFT, KR, "middle")

# 메인 우측 카드 (Focal! ACC): 메인 컨텍스트 보존
d.tone(512, 124, 344, 96, ACC, r=6, op="14", sw=1.4)
d.chip(576, 146, "토큰 보존", ACC, 11)
d.t(684, 174, "메인 컨텍스트 유지", 14, INK, KR, "middle", 600)
d.t(684, 198, "수만 토큰 차단 · 요약 보고서 수신", 12, INK, KR, "middle")

# 메인 내부 작업 통제 연결 화살표
d.arrow([(408, 172), (504, 172)], MUTED, "ar", 1.4)
d.t(456, 160, "작업 통제", 12, MUTED, KR, "middle", 600)

# 2. 하단 영역: 격리 서브에이전트
d.box(40, 280, 840, 136, fill=PAPER, stroke=RULE, sw=0.8, r=8)
d.box(56, 286, 164, 16, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(138, 298, "ISOLATED SUBAGENTS", 8, SOFT, MONO, "middle")

# 서브에이전트 1 카드
d.box(64, 308, 368, 96, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.chip(136, 332, "Clean slate", INFO, 11)
d.t(248, 360, "서브에이전트 1 (코드 분석)", 13, INK, KR, "middle", 600)
d.t(248, 384, "파일 검색 및 터미널 출력 격리", 12, MUTED, KR, "middle")

# 서브에이전트 2 카드
d.box(488, 308, 368, 96, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.chip(560, 332, "Clean slate", INFO, 11)
d.t(672, 360, "서브에이전트 2 (빌드 검증)", 13, INK, KR, "middle", 600)
d.t(672, 384, "빌드 로그 및 단위 테스트 격리", 12, MUTED, KR, "middle")

# 3. 연결선 (영역 간 채널 y=232 ~ 280)
# 메인 좌측 -> 서브에이전트 1 위임 화살표
d.arrow([(236, 220), (236, 300)], MUTED, "ar", 1.4)
d.t(244, 260, "하위 작업 위임", 12, MUTED, KR, "start")

# 서브에이전트 1 -> 메인 우측 (Focal) 요약 반환 (직교 굴절선)
d.path("M 380 308 V 264 Q 380 256 388 256 H 576 Q 584 256 584 248 V 228", ACC, 1.4, m="acc", dash="4 3")
d.t(480, 246, "분석 요약 반환", 12, ACC, KR, "middle", 600)

# 서브에이전트 2 -> 메인 우측 (Focal) 요약 반환 (수직선)
d.path("M 720 308 L 720 228", ACC, 1.4, m="acc", dash="4 3")
d.t(728, 260, "검증 결과 반환", 12, ACC, KR, "start", 600)

# 4. 범례
d.legend(440, [
    ("메인 대화 흐름", INK),
    ("격리 서브에이전트", INFO),
    ("요약 보고서 반환 (Focal)", ACC),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-02.context-isolation.svg"))
d.save(out)
print(f"saved: {out}")
