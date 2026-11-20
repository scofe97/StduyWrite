# 사실 출처: docs/network-provider-lifecycle.md 「Contract」「Manager」「Shutdown」 · internal/expose/provider/manager.go:27-33,512,562,606,693,887,1217
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
    "NETWORK PROVIDER · STATE MACHINE",
    "제공자 경로 수명주기 5대 상태 전이 모델",
    "unavailable 초기 상태에서 비동기 starting, ready 서빙, error 및 stopped 종료 정리까지",
    lead="호스트 권한과 flat 허용이 일치할 때만 전이가 유효하게 진행됩니다"
)

# 1. 시작점 (Start dot)
d.o.append(f'<circle cx="20" cy="220" r="5" fill="{SOFT}"/>')
d.arrow([(26, 220), (40, 220)], c=MUTED, m="ar")

# 2. State: unavailable (초기 미구성 / 미허용)
d.box(40, 175, 140, 90, fill=PAPER2, stroke=SOFT, sw=1.1, r=8)
d.t(110, 202, "unavailable", 13, INK, MONO, "middle", 600)
d.t(110, 224, "manager.go:32", 10, MUTED, MONO, "middle")
d.t(110, 246, "백엔드 미구성 · 미허용", 10, SOFT, KR, "middle")

# Transition: ServeExposure (unavailable -> starting)
d.arrow([(180, 220), (290, 220)], c=ACC, m="acc")
d.tag_text(235, 204, "ServeExposure", 10, ACC, 600)
d.tag_text(235, 236, "호스트+flat 허용", 9, MUTED)

# 3. State: starting (비동기 등록 대기)
d.box(290, 175, 140, 90, fill=PAPER2, stroke=WARN, sw=1.2, r=8)
d.t(360, 202, "starting", 13, WARN, MONO, "middle", 600)
d.t(360, 224, "manager.go:29", 10, MUTED, MONO, "middle")
d.t(360, 246, "비동기 리스너·인증서 대기", 10, SOFT, KR, "middle")

# Transition: starting -> ready
d.arrow([(430, 210), (540, 210)], c=OK, m="ok")
d.tag_text(485, 196, "바인딩·인증 성공", 10, OK, 600)

# Transition: starting -> error (아래로 꺾임)
d.path("M 360 265 L 360 395 L 540 395", c=BAD, sw=1.2, m="bad")
d.tag_text(450, 395, "등록·인증 실패", 10, BAD, 600)

# 4. State: ready (서빙 활성)
d.box(540, 175, 140, 90, fill=PAPER2, stroke=OK, sw=1.5, r=8)
d.t(610, 202, "ready", 13, OK, MONO, "middle", 600)
d.t(610, 224, "manager.go:28", 10, MUTED, MONO, "middle")
d.t(610, 246, "트래픽 수신 · URL 유효", 10, OK, KR, "middle")

# 5. State: error (장애 상태)
d.box(540, 350, 140, 90, fill=PAPER2, stroke=BAD, sw=1.2, r=8)
d.t(610, 377, "error", 13, BAD, MONO, "middle", 600)
d.t(610, 399, "manager.go:30", 10, MUTED, MONO, "middle")
d.t(610, 421, "에러 기록 · 실패 보고", 10, SOFT, KR, "middle")

# Transition: ready -> stopped (우측으로)
d.path("M 680 240 L 815 285", c=MUTED, sw=1.2, m="ar")
d.tag_text(748, 226, "StopPublicRoutes", 10, MUTED, 600)

# Transition: error -> stopped (우측 상단으로)
d.path("M 680 395 L 815 305", c=MUTED, sw=1.2, m="ar")
d.tag_text(748, 365, "정리 후 관찰 제거", 9, MUTED)

# 6. State: stopped (종료 정리)
d.box(815, 245, 140, 90, fill=PAPER2, stroke=MUTED, sw=1.0, r=8)
d.t(885, 272, "stopped", 13, MUTED, MONO, "middle", 600)
d.t(885, 294, "manager.go:31", 10, MUTED, MONO, "middle")
d.t(885, 316, "정상 종료 · stale 관찰 표지", 10, SOFT, KR, "middle")

# 범례
d.legend(486, [
    ("정상 서비스 상태 (Live)", OK),
    ("비동기 등록 대기 (Starting)", WARN),
    ("장애 및 오류 상태 (Error)", BAD),
    ("초기/정리 상태 (Teardown)", MUTED),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-02-provider-states.svg"))
d.save(out)
print(f"saved: {out}")
