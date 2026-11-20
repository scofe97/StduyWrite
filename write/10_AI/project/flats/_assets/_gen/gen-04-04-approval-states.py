# 사실 출처: docs/design.md 「Approvals」 · docs/lifecycle-core-contract.md 「Operator authority and frozen approvals」 · internal/store/store.go:123,900-930 · internal/core/lifecycle.go:148,553,570,614-617,646 · internal/core/service.go:1875-1927
# 타입 스펙: type-state
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 10

class DState(D):
    def tag_text(s, x, y, txt, size=11, c=MUTED, weight=400, bg=PAPER):
        w = _w(txt, size)
        s.o.append(f'<rect x="{x - w/2}" y="{y - size - 2}" width="{w}" height="{size + 6}" fill="{bg}"/>')
        s.t(x, y, txt, size, c, _kr(txt), "middle", weight)

    def legend(s, y, items):
        s.line(12, y, s.w - 48, y, RULE, 0.8)
        s.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
        x = 60
        for lab, c in items:
            s.o.append(f'<rect x="{x}" y="{y+12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x + 22, y + 22, lab, 11, MUTED, KR, "start")
            x += 32 + int(_w(lab, 11))

W, H = 1000, 560
d = DState(
    W, H,
    "APPROVAL LIFECYCLE · STATE MACHINE",
    "승인 객체 수명주기 5대 상태 전이 모델",
    "requestFrozen 요청에서 원자적 점유, 동결 값 재검증, 적용 완료 및 stale 거절까지",
    lead="운영자 승인 결정 시점에 동결된 환경을 재확인하여 드리프트와 경합을 차단합니다"
)

# 1. 시작점 (Start dot)
d.o.append(f'<circle cx="28" cy="200" r="5" fill="{SOFT}"/>')
d.arrow([(34, 200), (70, 200)], c=MUTED, m="ar")
d.tag_text(52, 185, "요청", 10, MUTED)

# 2. State: pending (요청 대기)
d.box(70, 150, 190, 100, fill=PAPER2, stroke=WARN, sw=1.3, r=8)
d.t(165, 178, "pending", 14, WARN, MONO, "middle", 600)
d.t(165, 200, "파라미터 동결 · DB 저장", 11, INK, KR, "middle")
d.t(165, 220, "idempotency_key 중복 방지", 10, SOFT, MONO, "middle")
d.t(165, 238, "lifecycle.go:148", 9, MUTED, MONO, "middle")

# Transition: Reject (pending -> rejected)
d.arrow([(165, 250), (165, 360)], c=BAD, m="bad")
d.tag_text(165, 305, "거절 (Reject)", 10, BAD, 600)

# 3. State: rejected (운영자 거절)
d.box(70, 360, 190, 100, fill=PAPER2, stroke=BAD, sw=1.1, r=8)
d.t(165, 388, "rejected", 14, BAD, MONO, "middle", 600)
d.t(165, 410, "운영자 거절 종결", 11, INK, KR, "middle")
d.t(165, 430, "decided_by · 감사 기록", 10, SOFT, KR, "middle")
d.t(165, 448, "store/lifecycle.go:525", 9, MUTED, MONO, "middle")

# Transition: Claim (pending -> applying)
d.arrow([(260, 200), (410, 200)], c=INFO, m="info")
d.tag_text(335, 185, "원자적 점유 (Claim)", 10, INFO, 600)
d.tag_text(335, 215, "단일 결정 보장", 9, MUTED)

# 4. State: applying (실행 및 적용 중)
d.box(410, 150, 200, 100, fill=PAPER2, stroke=INFO, sw=1.3, r=8)
d.t(510, 178, "applying", 14, INFO, MONO, "middle", 600)
d.t(510, 200, "동결 파라미터 재검증", 11, INK, KR, "middle")
d.t(510, 220, "crash 시 재개 대상", 10, SOFT, KR, "middle")
d.t(510, 238, "lifecycle.go:570", 9, MUTED, MONO, "middle")

# 재기동 복구 루프 (resumeApplying)
d.path("M 460 150 C 460 90, 560 90, 560 150", c=SOFT, sw=1.1, m="soft", dash="3 3")
d.tag_text(510, 105, "호스트 재기동: resumeApplying (:553)", 9, SOFT)

# Transition: Finish Success (applying -> approved)
d.arrow([(610, 200), (740, 200)], c=OK, m="ok")
d.tag_text(675, 185, "재검증 통과 & 적용 완료", 10, OK, 600)
d.tag_text(675, 215, "영속 영수증 기록", 9, MUTED)

# 5. State: approved (승인 및 적용 완료)
d.box(740, 150, 200, 100, fill=PAPER2, stroke=OK, sw=1.3, r=8)
d.t(840, 178, "approved", 14, OK, MONO, "middle", 600)
d.t(840, 200, "배포 확정 · 트래픽 전환", 11, INK, KR, "middle")
d.t(840, 220, "result_data 상태 영속", 10, SOFT, KR, "middle")
d.t(840, 238, "lifecycle.go:614", 9, MUTED, MONO, "middle")

# Transition: Finish Failure (applying -> failed)
d.arrow([(510, 250), (510, 410), (740, 410)], c=BAD, m="bad")
d.tag_text(625, 410, "stale_approval (불일치) / 실행 실패", 10, BAD, 600)

# 6. State: failed (검증 불일치 또는 적용 실패)
d.box(740, 360, 200, 100, fill=PAPER2, stroke=BAD, sw=1.1, r=8)
d.t(840, 388, "failed", 14, BAD, MONO, "middle", 600)
d.t(840, 410, "동결 불일치 또는 에러", 11, INK, KR, "middle")
d.t(840, 430, "failure_code 기록 종결", 10, SOFT, KR, "middle")
d.t(840, 448, "lifecycle.go:616", 9, MUTED, MONO, "middle")

# 범례
d.legend(490, [
    ("요청 대기 (pending)", WARN),
    ("실행 중 (applying)", INFO),
    ("정상 완료 (approved)", OK),
    ("거절 및 실패 (rejected/failed)", BAD),
    ("비정상 종료 복구 흐름", SOFT)
])

d.save(str(_HERE.parent / "04-04-approval-states.svg"))
print("ok 04-04-approval-states.svg")
