# 05-01 §1 릴리스가 지나는 상태와 되돌아가는 길.
# 본문 근거: 05-01 §1 ("배포된 상태에서 내부 직원에게만 열고, 관찰 결과가 좋으면 비유료·실버 등급 고객으로 넓히고, 결국 전체").
# 값 근거: ch05.txt §5.1.1 (배포=트래픽 0·스모크 테스트, 내부 직원 → 비유료·실버 고객 → 전체 고객, 롤백).
# 타입 스펙: type-state — 주체 하나(릴리스)의 상태 전이. 시작점 · 상태 4 · 롤백 전이 · 종료점. 전이 라벨은 event [guard].
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 448
d = D(W, H, "ISTIO IN ACTION · 05-01 §1",
      "릴리스가 지나는 상태와 되돌아가는 길",
      "새 코드는 먼저 트래픽 없이 배포되고, 내부 직원 → 비유료·실버 고객 → 전체로 릴리스가 넓어진다. 어느 상태에서든 관찰 결과가 나쁘면 트래픽을 이전 버전으로 되돌려 롤백한다.",
      "옛 버전이 대부분을 받고 새 버전이 작은 몫을 받는 동안 지켜보는 단계가 카나리입니다")

SW, SH, Y = 168, 68, 140
xs = [44, 260, 476, 692]          # stride 216, 사이 48px 간격
states = [("배포됨", "트래픽 0 · 스모크", False), ("내부 직원", "작은 몫 · 관찰", True), ("비유료 · 실버", "노출 확대", False), ("전체 고객", "릴리스 완료", False)]
# 시작점
d.o.append(f'<circle cx="16" cy="{Y + SH / 2}" r="6" fill="{INK}"/>')
d.path(f"M 24 {Y + SH / 2} H {xs[0] - 2}", MUTED, 1.4, m="ar")
for i, (name, sub, focal) in enumerate(states):
    x = xs[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, Y + 28, name, 14, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, Y + 50, sub, 12, MUTED, KR)
    if i < 3:
        d.path(f"M {x + SW} {Y + SH / 2} H {xs[i + 1] - 2}", MUTED, 1.4, m="ar")
        d.t((x + SW + xs[i + 1]) / 2, Y + SH / 2 - 12, "양호", 12, SOFT, KR)
# 종료점
ex = xs[3] + SW + 36
d.path(f"M {xs[3] + SW} {Y + SH / 2} H {ex - 10}", MUTED, 1.4, m="ar")
d.o.append(f'<circle cx="{ex}" cy="{Y + SH / 2}" r="8" fill="none" stroke="{INK}" stroke-width="1.4"/><circle cx="{ex}" cy="{Y + SH / 2}" r="5" fill="{INK}"/>')
# 롤백 — 세 상태에서 이전 버전으로 되돌린다. 한 노드로 모아 화살표가 서로 얽히지 않게 한다.
RY = Y + SH + 70
RX0, RW0, RH0 = xs[1], xs[3] + SW - xs[1], 52
d.o.append(f'<rect x="{RX0}" y="{RY}" width="{RW0}" height="{RH0}" rx="8" fill="{WARN}12" stroke="{WARN}" stroke-width="1.2"/>')
for i in (1, 2, 3):
    cx = xs[i] + SW / 2
    d.path(f"M {cx} {Y + SH} V {RY - 2}", WARN, 1.2, m="warn", dash="4 3")
d.t(RX0 + RW0 / 2, RY + 22, "이전 버전", 14, WARN, KR, "middle", 600)
d.t(RX0 + RW0 / 2, RY + 42, "롤백 [실사용자 반응이 기대와 다름] — 트래픽을 되돌린다", 13, WARN, KR)
d.t(xs[0], RY + RH0 + 28, "관찰 = 메트릭·로그로 기대대로 도는지 확인", 12, SOFT, KR, "start")
d.legend(RY + RH0 + 56, [("카나리 — 작은 몫을 지켜보는 상태", ACC), ("롤백", WARN)])
d.save("05-01.release-ladder.svg")
