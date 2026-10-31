"""스킬 수명 주기 상태와 은퇴 기록 전이 상태 기계."""
# 타입 스펙: type-state
# 사실 출처: C2 91-114, 241-255 · dalcom docs/specs/skill-lifecycle.md
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "SKILL LIFECYCLE · STATE MACHINE",
    "스킬 수명 주기 상태와 은퇴 전이",
    "초안부터 검증 사다리 통과와 격리·은퇴 종결",
    lead="5단계 검증 사다리와 결함 격리, 은퇴 스킬은 catalog.yml retired: 로 기록",
)

# 1. 불법 전이 (10개 규정) 안내 상자 및 차단 호
d.box(748, 350, 184, 76, fill=PAPER2, stroke=BAD, sw=1.0, r=6)
d.t(840, 372, "10개 불법 전이 규정", 12.5, BAD, KR, "middle", 600)
d.t(840, 394, "Drafted to Shipped", 11, MUTED, MONO, "middle")
d.t(840, 412, "Quarantined to Shipped", 11, MUTED, MONO, "middle")

# 불법 전이 점프 차단선 (아크)
d.path("M 104 230 C 104 64, 876 64, 876 230", BAD, 1.4, m="bad", dash="4 4")
d.t(490, 84, "건너뛰기 금지", 12.5, BAD, KR, "middle")

# 2. 시작 마커
d.o.append(f'<circle cx="18" cy="262" r="5" fill="{INK}"/>')
d.arrow([(24, 262), (48, 262)], MUTED, "ar", 1.4)

# 3. 정상 사다리 전이 (T1 ~ T4)
# T1: Drafted -> Contracted
d.arrow([(160, 262), (236, 262)], MUTED, "ar", 1.4)
d.t(198, 250, "frontmatter", 11, MUTED, MONO, "middle")
d.t(198, 276, "exit 0", 11, MUTED, MONO, "middle")

# T2: Contracted -> Manifested
d.arrow([(348, 262), (424, 262)], MUTED, "ar", 1.4)
d.t(386, 250, "manifests", 11, MUTED, MONO, "middle")
d.t(386, 276, "--check 0", 11, MUTED, MONO, "middle")

# T3: Manifested -> Routable
d.arrow([(536, 262), (612, 262)], MUTED, "ar", 1.4)
d.t(574, 250, "routes", 11, MUTED, MONO, "middle")
d.t(574, 276, "exit 0", 11, MUTED, MONO, "middle")

# T4: Routable -> Shipped
d.arrow([(724, 262), (820, 262)], OK, "ok", 1.4)
d.t(772, 250, "surfaces", 11, OK, MONO, "middle")
d.t(772, 276, "--check 0", 11, OK, MONO, "middle")

# 4. 격리 (Quarantined) 전이 (T7, T8)
# T7: Contracted, Manifested, Routable -> Quarantined (한 줄로 모아 진입)
d.path("M 316 230 L 316 204 L 480 204", WARN, 1.4)
d.path("M 644 230 L 644 204 L 480 204", WARN, 1.4)
d.arrow([(480, 230), (480, 176)], WARN, "warn", 1.4)
d.t(536, 194, "gate exit 1", 11, WARN, MONO, "middle")

# T8: Quarantined -> Contracted 복귀
d.path("M 424 150 L 264 150 L 264 230", OK, 1.4, m="ok")
d.t(344, 138, "수정 복귀 (exit 0)", 12.5, OK, KR, "middle")

# 5. 은퇴 경로 전이 (T5: Drafted -> Merged, T6: Drafted -> Purged)
d.path("M 148 294 L 148 318 L 292 318 L 292 356", ACC, 1.4, m="ar")
d.path("M 292 318 L 436 318 L 436 356", ACC, 1.4, m="ar")
d.t(216, 310, "은퇴 전이", 12.5, ACC, KR, "middle")

# 6. 체크포인트 복원 전이 (T9, T10)
# T9: Any state -> Restored (쓰기 검증 실패 시 체크포인트 바이트 복원)
d.path("M 380 442 L 104 442 L 104 408", INFO, 1.4, m="info")
d.t(240, 430, "모든 상태 · 쓰기 검증 실패", 12.5, INFO, KR, "middle")

# T10: Restored -> Drafted (작업 재개)
d.arrow([(76, 356), (76, 294)], INFO, "info", 1.4)
d.t(110, 328, "작업 재개", 12.5, INFO, KR, "middle")

# 7. 내 저장소 도입 영역 (catalog.yml retired: 기록) 및 은퇴 연결 점선
d.line(492, 382, 512, 382, c=ACC, sw=1.2, dash="3 3")
d.box(512, 350, 220, 76, fill=PAPER2, stroke=ACC, sw=1.4, r=8)
d.t(622, 374, "catalog.yml retired: 기록", 12.5, ACC, KR, "middle", 600)
d.t(622, 404, "name·reason·replacement·source", 10.5, MUTED, MONO, "middle")

# 8. 상태 노드 (9개 상태)
# 정상 사다리 5단계
d.box(48, 230, 112, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(104, 266, "Drafted", 13, INK, MONO, "middle", 600)

d.box(236, 230, 112, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(292, 266, "Contracted", 13, INK, MONO, "middle", 600)

d.box(424, 230, 112, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(480, 266, "Manifested", 13, INK, MONO, "middle", 600)

d.box(612, 230, 112, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(668, 266, "Routable", 13, INK, MONO, "middle", 600)

d.box(820, 230, 112, 64, fill=PAPER2, stroke=OK, sw=1.4, r=8)
d.t(870, 266, "Shipped", 13, OK, MONO, "middle", 600)
d.o.append(f'<circle cx="916" cy="246" r="6" fill="none" stroke="{OK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="916" cy="246" r="3" fill="{OK}"/>')

# 예외 상태: Quarantined
d.box(424, 124, 112, 52, fill=PAPER2, stroke=WARN, sw=1.1, r=8)
d.t(480, 154, "Quarantined", 12.5, WARN, MONO, "middle", 600)

# 복원 상태: Restored
d.box(48, 356, 112, 52, fill=PAPER2, stroke=INFO, sw=1.1, r=8)
d.t(104, 386, "Restored", 12.5, INFO, MONO, "middle", 600)

# 종결 은퇴 상태: Merged
d.box(236, 356, 112, 52, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(286, 386, "Merged", 12.5, INK, MONO, "middle", 600)
d.o.append(f'<circle cx="332" cy="374" r="6" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="332" cy="374" r="3" fill="{MUTED}"/>')

# 종결 은퇴 상태: Purged
d.box(380, 356, 112, 52, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(430, 386, "Purged", 12.5, INK, MONO, "middle", 600)
d.o.append(f'<circle cx="476" cy="374" r="6" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="476" cy="374" r="3" fill="{MUTED}"/>')

# 9. 범례
d.legend(472, [
    ("정상 사다리", OK),
    ("게이트 격리", WARN),
    ("복원 상태", INFO),
    ("내 저장소 도입", ACC),
    ("불법 전이 차단", BAD),
])

output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-01.skill-lifecycle.svg"))
d.save(output_path)
print(f"Generated: {output_path}")
