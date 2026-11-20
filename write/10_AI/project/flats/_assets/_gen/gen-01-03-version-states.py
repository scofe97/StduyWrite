# 사실 출처: docs/design.md 「Model and flows」 Version model, internal/core/lifecycle.go:1686,1734, internal/core/service.go:1337,1434,1988
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

W, H = 980, 560
d = DState(
    W, H,
    "LIFECYCLE · STATE TRANSITIONS",
    "Website · Page 수명주기 상태 전이 모델",
    "Draft 초안에서 불변 Version 생성, 배포 활성화, 롤백 및 임시 미리보기까지의 상태 머신",
    "버전 보관과 배포 승인을 분리해 불변 산출물 확정과 실시간 트래픽 영향을 독립 통제"
)

# 1. 시작점 (Start dot)
d.o.append(f'<circle cx="30" cy="180" r="6" fill="{INK}"/>')
d.arrow([(36, 180), (60, 180)], c=MUTED, m="ar")

# 2. State 1: Draft (초안)
d.box(60, 140, 180, 80, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(150, 166, "Draft (초안)", 13, INK, KR, "middle", 600)
d.t(150, 184, "draft-revs/<rev>", 10, MUTED, MONO, "middle")
d.t(150, 202, "Private · 작업 복사본", 10, INFO, KR, "middle")

# Self-loop: save-draft
d.path("M 110 140 C 110 80, 190 80, 190 140", c=MUTED, sw=1.2, m="ar")
d.tag_text(150, 96, "save-draft (rev++)", 10, MUTED)

# 3. Transition: create_version (Draft -> Version v1)
d.arrow([(240, 180), (360, 180)], c=WARN, m="warn")
d.tag_text(300, 168, "create_version", 11, WARN, 600)
d.tag_text(300, 196, "[승인 apr-...]", 10, MUTED)

# 4. State 2: Version v1 (불변 보관)
d.box(360, 140, 180, 80, fill=PAPER2, stroke=MUTED, sw=1.0, r=8)
d.t(450, 166, "Version v1 (저장)", 13, INK, KR, "middle", 600)
d.t(450, 184, "versions/1/ (불변)", 10, MUTED, MONO, "middle")
d.t(450, 202, "live_version = 0 (비활성)", 10, SOFT, MONO, "middle")

# 5. Transition: deploy (Version v1 -> Live v1)
d.arrow([(540, 180), (670, 180)], c=OK, m="ok")
d.tag_text(605, 168, "deploy", 11, OK, 600)
d.tag_text(605, 196, "[승인 apr-...]", 10, MUTED)

# 6. State 3: Live v1 (활성 서비스)
d.box(670, 140, 190, 80, fill=PAPER2, stroke=OK, sw=1.5, r=8)
d.t(765, 166, "Live v1 (활성)", 13, OK, KR, "middle", 600)
d.t(765, 184, "live_version = 1", 10, INK, MONO, "middle")
d.t(765, 202, "<slug>.localhost:7879", 10, MUTED, MONO, "middle")

# 7. State 6: Preview (임시 검증) - 좌하단
d.box(60, 340, 200, 80, fill=PAPER2, stroke=INFO, sw=1.0, r=8)
d.t(160, 366, "Preview (임시 엔드포인트)", 12, INFO, KR, "middle", 600)
d.t(160, 384, "<slug>-<rand>.localhost", 10, MUTED, MONO, "middle")
d.t(160, 402, "격리 데이터 · TTL 24h", 10, SOFT, KR, "middle")

# Preview branch from Draft (n=0)
d.arrow([(110, 220), (110, 340)], c=INFO, m="info", dash="3 3")
d.tag_text(110, 280, "preview (n=0)", 9, INFO)

# Preview branch from Version v1 (n=1)
d.path("M 380 220 C 340 280, 230 280, 230 340", c=INFO, sw=1.0, m="info", dash="3 3")
d.tag_text(290, 280, "preview (n=1)", 9, INFO)

# 8. Transition from Live v1 to Version v2
d.path("M 720 220 C 720 280, 480 280, 480 340", c=WARN, sw=1.2, m="warn")
d.tag_text(590, 280, "새 초안 → create_version [승인]", 10, WARN)

# 9. State 4: Version v2 (신규 저장) - 중하단
d.box(360, 340, 180, 80, fill=PAPER2, stroke=MUTED, sw=1.0, r=8)
d.t(450, 366, "Version v2 (저장)", 13, INK, KR, "middle", 600)
d.t(450, 384, "versions/2/ (불변)", 10, MUTED, MONO, "middle")
d.t(450, 402, "신규 스냅샷 대기", 10, SOFT, KR, "middle")

# 10. Transition: deploy v2 (Version v2 -> Live v2)
d.arrow([(540, 380), (670, 380)], c=ACC, m="acc")
d.tag_text(605, 368, "deploy v2", 11, ACC, 600)
d.tag_text(605, 396, "[승인 apr-...]", 10, MUTED)

# 11. State 5: Live v2 (신규 활성 서비스) - 우하단
d.box(670, 340, 190, 80, fill=PAPER2, stroke=ACC, sw=1.5, r=8)
d.t(765, 366, "Live v2 (활성)", 13, ACC, KR, "middle", 600)
d.t(765, 384, "live_version = 2", 10, INK, MONO, "middle")
d.t(765, 402, "사본 헬스 → DB 스냅샷", 10, MUTED, KR, "middle")

# 12. Rollback Transition: Live v2 -> Live v1
d.path("M 860 370 C 930 370, 930 190, 860 190", c=BAD, sw=1.4, m="bad")
d.tag_text(915, 268, "rollback [승인]", 10, BAD, 600)
d.tag_text(915, 286, "CAS 포인터 복구", 9, MUTED)

# 범례 (Legend)
d.legend(475, [
    ("초안 / 미리보기 (격리)", INFO),
    ("승인 대기 / 전이", WARN),
    ("활성 서비스 (Live)", OK),
    ("신규 배포 승격", ACC),
    ("롤백 복구 (CAS)", BAD)
])

out_path = _HERE.parent / "01-03-version-states.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
