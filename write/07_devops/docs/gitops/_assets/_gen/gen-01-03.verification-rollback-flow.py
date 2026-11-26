# 타입 스펙: type-flowchart
# 2절 카나리 검증과 자동 롤백 흐름 — Health Check 관문과 AnalysisRun 관문을 통과해야 승격하고 실패 시 stable 100% 로 복귀한다
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, BAD, INFO, KR, MONO)

W, H = 880, 804

d = D(
    W, H,
    "GITOPS · CANARY VERIFICATION & AUTO ROLLBACK",
    "카나리 배포의 두 검증 관문과 자동 롤백",
    "setWeight 10 이후 readinessProbe(Health Check)와 AnalysisRun(1분 간격 5회, 5xx < 0.05, failureLimit 2)을 거쳐 50·100% 승격 또는 abort 후 stable 100% 복귀로 갈리는 흐름",
    lead="Health Check 는 요청 수신 가능 여부를, AnalysisRun 은 운영 지표를 검증해 승격 또는 abort 를 결정합니다"
)


def _fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in str(txt)) else MONO


def oval_node(x, y, w, h, title, sub, c, focal=False):
    r = h // 2
    if focal:
        d.tone(x, y, w, h, c, r=r, op="12", sw=1.4)
        tc = c
    else:
        d.box(x, y, w, h, PAPER2, c, 1.2, r)
        tc = INK
    tfam, sfam = _fam(title), _fam(sub)
    d.t(x + w / 2, y + 22, title, 14, tc, tfam, "middle", 600)
    d.t(x + w / 2, y + 40, sub, 12, MUTED, sfam, "middle")


def step_box(x, y, w, h, title, sub, c=RULE):
    d.box(x, y, w, h, PAPER2, c, 1.2, 6)
    tfam, sfam = _fam(title), _fam(sub)
    d.t(x + w / 2, y + 22, title, 14, INK, tfam, "middle", 600)
    d.t(x + w / 2, y + 40, sub, 12, MUTED, sfam, "middle")


def diamond(cx, cy, hw, hh, line1, line2, c=INFO, focal=False):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    if focal:
        d.o.append(f'<polygon points="{pts}" fill="{c}12" stroke="{c}" stroke-width="1.5"/>')
        tc = c
    else:
        d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="1.3"/>')
        tc = INK
    d.t(cx, cy - 4, line1, 14, tc, _fam(line1), "middle", 600)
    d.t(cx, cy + 16, line2, 12, MUTED, _fam(line2), "middle")


CX = 272
RX = 548
RW = 280

# ── Arrows (z-order: behind nodes) ─────────────────────────────────────
# Start -> Gate 1 (Health Check)
d.arrow([(CX, 156), (CX, 196)], MUTED, "ar", 1.3)

# Gate 1 -> Fail (Right)
d.arrow([(CX + 124, 240), (RX, 240)], BAD, "bad", 1.3)
d.t(472, 224, "실패 · NotReady", 13, BAD, KR, "middle", 600)

# Gate 1 -> Pass (Down)
d.arrow([(CX, 284), (CX, 336)], INFO, "info", 1.3)
d.t(CX + 16, 314, "통과 · Ready", 13, INFO, KR, "start", 600)

# Wait -> Gate 2 (AnalysisRun)
d.arrow([(CX, 388), (CX, 428)], MUTED, "ar", 1.3)

# Gate 2 -> Pass (Right)
d.arrow([(CX + 148, 480), (RX, 480)], OK, "ok", 1.4)
d.t(484, 464, "통과 · 5xx < 0.05", 13, OK, KR, "middle", 600)

# 50% -> 100% (Right Down)
d.arrow([(RX + RW // 2, 506), (RX + RW // 2, 560)], OK, "ok", 1.4)
d.t(RX + RW // 2 + 16, 536, "승격 통과", 13, OK, KR, "start", 600)

# Gate 2 -> Fail (Down)
d.arrow([(CX, 532), (CX, 580)], BAD, "bad", 1.4)
d.t(CX + 16, 560, "실패 > 2회", 13, BAD, KR, "start", 600)

# Abort -> Stable 100%
d.arrow([(CX, 632), (CX, 672)], BAD, "bad", 1.4)

# ── Nodes ──────────────────────────────────────────────────────────────
oval_node(CX - 116, 104, 232, 52, "카나리 10%", "setWeight: 10", RULE)

diamond(CX, 240, 124, 44, "Health Check 관문", "readinessProbe 통과?", INFO)
oval_node(RX, 214, RW, 52, "EndpointSlice 제외", "트래픽 차단 · 대기", BAD)

step_box(CX - 120, 336, 240, 52, "안정화 대기", "pause: {duration: 2m}", RULE)

diamond(CX, 480, 148, 52, "AnalysisRun 관문", "1m×5 · 5xx<0.05 · limit2", ACC, focal=True)
step_box(RX, 454, RW, 52, "50% 트래픽 전환", "setWeight: 50", OK)
oval_node(RX, 560, RW, 52, "100% 승격", "단계 완료 · stable", OK)

step_box(CX - 120, 580, 240, 52, "자동 abort", "canary 0% 전환", BAD)
oval_node(CX - 120, 672, 240, 52, "stable 100% 복귀", "트래픽 원복", BAD)

# ── Legend ─────────────────────────────────────────────────────────────
d.legend(748, [
    ("Health Check 관문", INFO),
    ("Analysis 관문", ACC),
    ("승격 · 정상", OK),
    ("중단 · 복귀", BAD),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-03.verification-rollback-flow.svg")
d.save(out_path)
print(f"saved: {out_path}")
