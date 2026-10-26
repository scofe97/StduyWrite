"""git worktree 기반 서브에이전트 작업 격리 및 자동 정리 흐름.

# 타입 스펙: type-flowchart
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO

W, H = 920, 620
MID = 460
d = D(
    W, H,
    "WORKTREE ISOLATION FLOWCHART",
    "git worktree 서브에이전트 작업 격리 및 자동 정리",
    "코드 변경 여부에 따라 임시 워크트리가 자동 삭제되거나 디스크에 보존되는 흐름",
    lead="메인 작업 트리를 오염시키지 않고 변경이 있을 때만 워크트리를 보존합니다"
)

# 1. 시작 타원
d.box(MID - 144, 96, 288, 40, fill=PAPER2, stroke=RULE, sw=1.0, r=20)
d.t(MID, 121, "서브에이전트 실행 (isolation: worktree)", 12, INK, MONO, "middle", 600)

# 2. 전용 워크트리 생성 단계
d.arrow([(MID, 136), (MID, 164)], MUTED, "ar", 1.4)
d.box(MID - 160, 164, 320, 52, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(MID, 186, "전용 워크트리 및 브랜치 생성", 13, INK, KR, "middle", 600)
d.t(MID, 204, "메인 작업 트리와 분리된 디렉터리", 12, MUTED, KR, "middle")

# 3. 격리 디렉터리 작업 수행 단계
d.arrow([(MID, 216), (MID, 244)], MUTED, "ar", 1.4)
d.box(MID - 160, 244, 320, 52, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(MID, 266, "격리 환경에서 작업 수행", 13, INK, KR, "middle", 600)
d.t(MID, 284, "파일 읽기·수정·빌드·테스트", 12, MUTED, KR, "middle")

# 4. 판단 마름모: 변경 여부
d.arrow([(MID, 296), (MID, 328)], MUTED, "ar", 1.4)
d.o.append(f'<polygon points="{MID},328 {MID+112},372 {MID},416 {MID-112},372" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.2"/>')
d.t(MID, 366, "코드 변경 발생", 13, INK, KR, "middle", 600)
d.t(MID, 384, "여부 판정", 12, MUTED, KR, "middle")

# 5. 분기 좌측: 아니오 (변경 없음)
LCX = 232
d.arrow([(MID - 112, 372), (LCX, 372), (LCX, 428)], SOFT, "soft", 1.3)
d.t((MID - 112 + LCX) // 2, 360, "아니오 (변경 없음)", 12, WARN, KR, "middle", 600)

d.box(LCX - 156, 436, 312, 52, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(LCX, 458, "임시 워크트리 및 브랜치 자동 삭제", 13, INK, KR, "middle", 600)
d.t(LCX, 476, "변경 없으면 자동 정리", 12, MUTED, KR, "middle")

d.arrow([(LCX, 488), (LCX, 520)], SOFT, "soft", 1.3)
d.box(LCX - 124, 520, 248, 40, fill=PAPER2, stroke=RULE, sw=1.0, r=20)
d.t(LCX, 545, "작업 종료 (정리 완료)", 13, INK, KR, "middle", 600)

# 6. 분기 우측: 예 (변경 발생 - Focal! ACC)
RCX = 688
d.arrow([(MID + 112, 372), (RCX, 372), (RCX, 428)], ACC, "acc", 1.4)
d.t((MID + 112 + RCX) // 2, 360, "예 (변경 발생)", 12, ACC, KR, "middle", 600)

d.tone(RCX - 156, 436, 312, 52, ACC, r=6, op="14", sw=1.4)
d.t(RCX, 458, "워크트리 보존", 13, INK, KR, "middle", 600)
d.t(RCX, 476, "변경이 있으면 디스크에 남음", 12, ACC, KR, "middle")

d.arrow([(RCX, 488), (RCX, 520)], SOFT, "soft", 1.3, "4 4")
d.o.append(f'<rect x="{RCX - 132}" y="520" width="264" height="40" rx="20" fill="{PAPER2}" stroke="{OK}" stroke-width="1.2" stroke-dasharray="4 4"/>')
d.t(RCX, 545, "경로·브랜치 보고 (미확인)", 13, MUTED, KR, "middle", 600)

# 7. 범례
d.legend(580, [
    ("시작·종료", RULE),
    ("격리 실행 단계", INFO),
    ("자동 정리", WARN),
    ("변경 있음 · 보존", ACC),
    ("미확인", OK),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-02.worktree-isolation.svg"))
d.save(out)
print(f"saved: {out}")
