# 사실 출처: docs/revision-store.md 「Schema」「Quotas and retention」, internal/core/design.go:1293
# 타입 스펙: type-timeline
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "REVISION TIMELINE · ROLLBACK & QUOTA RETENTION",
    "불변 리비전 누적과 롤백, 쿼터 보존 타임라인",
    "리비전 1~4 생성 후 리비전 3으로 롤백하여 신규 5번을 생성하고 unpinned 항목을 정리하는 순서",
    "과거 이력은 덮어쓰지 않고 새 리비전으로 누적하며 핀·최신 항목은 자동 삭제에서 보호"
)

# 메인 타임라인 수평 레일
TL_Y = 240
d.line(48, TL_Y, W - 48, TL_Y, RULE, 1.6)

# 5개 리비전 노드 X 좌표
NODES = [
    (110, "rev 1", "created", "초기 생성", MUTED, False),
    (260, "rev 2", "agent", "에이전트 수정", INFO, False),
    (410, "rev 3", "person", "사람 편집 확정", WARN, True),  # Pinned!
    (560, "rev 4", "agent", "후속 변경", INFO, False),
    (750, "rev 5", "rollback", "rev 3 내용 복원", OK, False),
]

for x, rev, kind, desc, c, is_pin in NODES:
    # 타임라인 눈금
    d.line(x, TL_Y - 10, x, TL_Y + 10, c, 2.0)
    
    # 상단: 리비전 카드
    d.box(x - 55, TL_Y - 110, 110, 80, fill=PAPER2, stroke=c, sw=1.2)
    d.t(x, TL_Y - 88, rev, 13, INK, MONO, "middle", 600)
    d.t(x, TL_Y - 72, f"kind: {kind}", 10, c, MONO, "middle")
    d.t(x, TL_Y - 54, desc, 9, MUTED, KR, "middle")
    
    # 핀 표시 (rev 3)
    if is_pin:
        d.chip(x, TL_Y - 120, "PINNED (보존)", WARN, 9, pad=5)

# 롤백 점프 곡선: rev 3 -> rollback_revision 3 -> rev 5
d.chip(600, 56, "rollback_revision 3 (승인 불요)", OK, 11, pad=8)
d.t(600, 80, "이력 삭제 없이 rev 3 내용 복제", 10, INK, KR, "middle")
d.path("M 465 160 C 495 80, 685 80, 695 160", c=OK, sw=1.8, m="ok", dash="4 4")

# 하단: 쿼터 초과 시 자동 정리 (Retention) 영역
d.box(48, 310, W - 96, 120, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(68, 334, "쿼터 및 자동 보존 정책 · revision_quota 100 · pin_quota 20", 12, INK, KR, "start", 600)
d.line(68, 346, W - 68, 346, RULE, 0.8)

# 3가지 핵심 규칙 상자
R1_X = 68
R2_X = 360
R3_X = 650
RW = 240

# 규칙 1: unpinned 오래된 리비전 자동 정리
d.box(R1_X, 358, RW, 58, fill=PAPER, stroke=BAD, sw=0.8, r=4)
d.t(R1_X + 12, 378, "1. 100개 초과 시 자동 정리", 10, BAD, KR, "start", 600)
d.t(R1_X + 12, 396, "오래된 unpinned 리비전 삭제 (rev 1, 2…)", 9, MUTED, KR, "start")

# 규칙 2: PIN 리비전 영구 보호
d.box(R2_X, 358, RW, 58, fill=PAPER, stroke=WARN, sw=0.8, r=4)
d.t(R2_X + 12, 378, "2. 핀 리비전 (rev 3) 보호", 10, WARN, KR, "start", 600)
d.t(R2_X + 12, 396, "리비전 쿼터 미차감 · 자동 삭제 제외", 9, MUTED, KR, "start")

# 규칙 3: 최신 리비전 절대 보존
d.box(R3_X, 358, RW, 58, fill=PAPER, stroke=OK, sw=0.8, r=4)
d.t(R3_X + 12, 378, "3. 최신 리비전 (rev 5) 보존", 10, OK, KR, "start", 600)
d.t(R3_X + 12, 396, "쿼터가 1이어도 최신 리비전은 유지", 9, MUTED, KR, "start")

# 하단 범례
d.legend(460, [
    ("초기 생성", MUTED),
    ("에이전트 변경", INFO),
    ("사람 편집 (Pin)", WARN),
    ("롤백 복제 신규", OK),
    ("자동 삭제 대상", BAD)
])

out_path = _HERE.parent / "01-04-revision-timeline.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
