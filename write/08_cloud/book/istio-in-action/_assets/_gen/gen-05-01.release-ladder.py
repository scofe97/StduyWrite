# 05-01 §1 릴리스가 지나는 상태와 되돌아가는 길 — 저자의 그림 5.2~5.5.
# 본문: "배포된 상태에서 내부 직원에게만 열고, 관찰 결과가 좋으면 비유료·실버 등급 고객으로 넓히고, 결국 전체.
# 어느 상태에서든 기대와 다르면 트래픽을 이전 버전으로 되돌리는 것이 롤백. 색이 붙은 상태가 카나리."
# 타입 스펙: type-state — 주체 하나(릴리스)의 상태 전이. 시작점 · 상태 4 · 롤백 전이 · 종료점. 전이 라벨은 event [guard].
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 396
d = D(W, H, "ISTIO IN ACTION · 05-01 §1",
      "릴리스가 지나는 상태와 되돌아가는 길",
      "새 코드는 먼저 트래픽 없이 배포되고, 내부 직원 → 비유료·실버 고객 → 전체로 릴리스가 넓어진다. 어느 상태에서든 관찰 결과가 나쁘면 트래픽을 이전 버전으로 되돌려 롤백한다.",
      "옛 버전이 대부분을 받고 새 버전이 작은 몫을 받는 동안 지켜보는 자리가 카나리입니다")

SW, SH, Y = 180, 64, 140
xs = [24, 260, 496, 732]          # stride 276, 사이 80px 에 전이 라벨이 든다
states = [("배포됨", "트래픽 0 · 스모크 테스트", False), ("내부 직원", "작은 몫 · 관찰", True), ("비유료 · 실버", "노출 확대", False), ("전체 고객", "릴리스 완료", False)]
# 시작점
d.o.append(f'<circle cx="40" cy="{Y + SH / 2}" r="6" fill="{INK}"/>')
d.path(f"M 46 {Y + SH / 2} H {xs[0] - 2}", MUTED, 1.4, m="ar")
for i, (name, sub, focal) in enumerate(states):
    x = xs[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, Y + 27, name, 14, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, Y + 48, sub, 12, MUTED, KR)
    if i < 3:
        d.path(f"M {x + SW} {Y + SH / 2} H {xs[i + 1] - 2}", MUTED, 1.4, m="ar")
        d.t((x + SW + xs[i + 1]) / 2, Y + SH / 2 - 10, "관찰 양호", 11, SOFT, KR)
# 종료점
ex = xs[3] + SW + 40
d.path(f"M {xs[3] + SW} {Y + SH / 2} H {ex - 10}", MUTED, 1.4, m="ar")
d.o.append(f'<circle cx="{ex}" cy="{Y + SH / 2}" r="8" fill="none" stroke="{INK}" stroke-width="1.4"/><circle cx="{ex}" cy="{Y + SH / 2}" r="5" fill="{INK}"/>')
# 롤백 — 세 상태에서 이전 버전으로 되돌린다. 아래로 나가 왼쪽 상태로 돌아오는 직각 경로
RY = Y + SH + 48
for i in (1, 2, 3):
    x = xs[i]; tx = xs[i - 1] + SW / 2
    d.path(f"M {x + SW / 2} {Y + SH} V {RY - 8 * (i - 1)} H {tx + 16 * i} V {Y + SH + 2}", WARN, 1.2, m="warn", dash="4 3")
d.t(xs[1] + SW / 2, RY + 30, "롤백 [실사용 반응이 기대와 다름] / 트래픽을 이전 버전으로", 12, WARN, KR)
d.t(xs[0], RY + 52, "관찰 = 메트릭·로그로 기대대로 도는지 확인", 12, SOFT, KR, "start")
d.legend(340, [("카나리 — 작은 몫을 지켜보는 상태", ACC), ("롤백", WARN)])
d.save("05-01.release-ladder.svg")
