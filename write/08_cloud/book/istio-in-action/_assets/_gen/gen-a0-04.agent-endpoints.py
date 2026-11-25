# a0-04 §2 15020 아래 갈리는 여섯.
# 본문(부록 D.1.1): /healthz/ready · /stats/prometheus · /quitquitquit · /app-health/ ·
#       /debug/ndsz · /debug/pprof/*. 마지막은 "relevant for Istio developers and not a
#       concern for Istio users".
# 타입 스펙: type-tree — 포트 하나 아래 엔드포인트 여섯이 갈리는 계층을 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 960, 560
d = D(W, H, "ISTIO IN ACTION · A0-04 §2",
      "한 포트가 여섯 엔드포인트를 겸한다",
      "준비 판정 · 메트릭 병합 · 프로세스 종료 · 앱 프로브 대행 · DNS 목록 · 프로파일링이 "
      "모두 15020 아래 있다. 색이 붙은 경로는 Istio 개발자용 프로파일링 자리다.",
      lead="15021 로 온 준비 확인이 결국 첫 번째 경로로 넘어옵니다")

RW, RH = 264, 56
d.box(348, 120, RW, RH, PAPER2, RULE, 1.0, 6)
d.t(348 + RW / 2, 144, "15020", 15, INK, MONO, "middle", 600)
d.t(348 + RW / 2, 166, "에이전트가 여는 포트", 13, MUTED, KR)

LW, LH = 280, 88
COLS, GAP, VGAP, X0, Y0 = 3, 24, 56, 36, 256
EPS = [
    ("/healthz/ready", "Envoy · DNS 프록시 준비 판정", False),
    ("/stats/prometheus", "프록시 · 앱 · 에이전트 메트릭 병합", False),
    ("/quitquitquit", "에이전트 프로세스 종료", False),
    ("/app-health/", "앱 쿠버네티스 헬스 프로브 대행", False),
    ("/debug/ndsz", "DNS 프록시의 호스트명 목록", False),
    ("/debug/pprof/*", "Go 프로파일링 (Istio 개발자용)", True),
]

col_cx = [X0 + c * (LW + GAP) + LW / 2 for c in range(COLS)]
BUS1 = 208
BUS2 = Y0 + LH + VGAP // 2
RAIL = 16

d.path(f"M 480 {120 + RH} L 480 {BUS1}", MUTED, 1.3)
d.path(f"M {col_cx[0]} {BUS1} L {col_cx[-1]} {BUS1}", MUTED, 1.3)
d.path(f"M {col_cx[0]} {BUS1} L {RAIL} {BUS1} L {RAIL} {BUS2} L {col_cx[-1]} {BUS2}", MUTED, 1.3)

for i, (name, sub, focal) in enumerate(EPS):
    r, c = divmod(i, COLS)
    x = X0 + c * (LW + GAP)
    y = Y0 + r * (LH + VGAP)
    cx = col_cx[c]
    d.arrow([(cx, BUS1 if r == 0 else BUS2), (cx, y - 2)], MUTED, "ar", 1.3)
    if focal:
        d.tone(x, y, LW, LH, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 32, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 16, y + 60, sub, 13, MUTED, KR, "start")

d.legend(504, [("Istio 개발자용 (사용자 비대상)", ACC)])
d.save("a0-04.agent-endpoints.svg")
print("ok a0-04.agent-endpoints")
