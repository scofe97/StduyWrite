# a0-04 §2 15020 아래 갈리는 여섯.
# 본문(부록 D.1.1): /healthz/ready · /stats/prometheus · /quitquitquit · /app-health/ ·
#       /debug/ndsz · /debug/pprof/*. 마지막은 "relevant for Istio developers and not a
#       concern for Istio users".
# 타입 스펙: type-tree — 포트 하나 아래 엔드포인트가 갈리는 계층이 논점이다. 루트에서 가지를
#           내리고 잎에 한 줄 설명을 단다.
#           축약: 여섯을 쓰임으로 두 줄에 나눠 놓고, accent 는 사용자 관심사가 아닌 것 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 596
d = D(W, H, "ISTIO IN ACTION · A0-04 §2",
      "한 포트가 여섯 가지를 겸한다",
      "준비 판정 · 메트릭 병합 · 프로세스 종료 · 앱 프로브 대행 · DNS 목록 · 프로파일링이 모두 "
      "15020 아래 있다. 색이 붙은 것만 사용자의 관심사가 아니라고 저자가 못 박는다.",
      "15021 로 온 준비 확인이 결국 여기 첫 칸으로 넘어옵니다")

RW, RH = 260, 56
d.box(370, 128, RW, RH, PAPER2, RULE, 1.0, 6)
d.t(370 + RW / 2, 152, "15020", 15, INK, MONO, "middle", 600)
d.t(370 + RW / 2, 172, "에이전트가 여는 포트", 11, MUTED, KR)

LW, LH = 300, 84
COLS, GAP, VGAP, X0, Y0 = 3, 20, 48, 40, 268
EPS = [
    ("/healthz/ready", "Envoy 와 DNS 프록시에 프로브를 돌린다", False),
    ("/stats/prometheus", "프록시 · 앱 · 자기 메트릭을 합쳐 낸다", False),
    ("/quitquitquit", "파일럿 에이전트 프로세스를 죽인다", False),
    ("/app-health/", "앱이 정의한 헬스 프로브를 대신 실행한다", False),
    ("/debug/ndsz", "DNS 프록시가 아는 호스트명 목록", False),
    ("/debug/pprof/*", "Go 프로파일링 — Istio 개발자용", True),
]
# 여섯은 모두 15020 의 형제다. 둘째 줄로 접은 것이지 첫째 줄의 하위가 아니므로
# 줄 사이에 화살표를 두지 않고, 왼쪽 레일로 돌아 둘째 버스를 따로 먹인다.
BUS, BUS2 = 216, Y0 + LH + VGAP // 2
RAIL = 20
d.path(f"M 500 {128 + RH} L 500 {BUS}", MUTED, 1.3)
d.path(f"M 190 {BUS} L 810 {BUS}", MUTED, 1.3)
d.path(f"M 190 {BUS} L {RAIL} {BUS} L {RAIL} {BUS2} L 190 {BUS2}", MUTED, 1.3)
d.path(f"M 190 {BUS2} L 810 {BUS2}", MUTED, 1.3)
for i, (name, sub, focal) in enumerate(EPS):
    r, c = divmod(i, COLS)
    x = X0 + c * (LW + GAP); y = Y0 + r * (LH + VGAP)
    d.arrow([(x + LW / 2, BUS if r == 0 else BUS2), (x + LW / 2, y - 2)], MUTED, "ar", 1.3)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 30, name, 12, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 16, y + 56, sub, 11, MUTED, KR, "start")
d.t(28, 508, "kubectl exec deploy/webapp -c istio-proxy -- curl localhost:15020/stats/prometheus", 11, INK, MONO, "start")
d.t(28, 532, "응답에 istio_agent 로 시작하는 것과 envoy 로 시작하는 것이 함께 나오면 합쳐진 것이다", 11, SOFT, KR, "start")
d.legend(556, [("사용자의 관심사가 아닌 것", ACC)])
d.save("a0-04.agent-endpoints.svg")
