# 12-01 §7 지역 우선 라우팅과 클러스터 간 페일오버 — 원문 12.3.7.
# 본문(원문 12.3.7): 기본은 라운드 로빈이라 두 클러스터에 고르게 나뉜다. 클라우드가 노드에 붙인 지역 라벨을
#       istiod 가 읽어 워크로드의 locality 를 채우는데, 그것이 쓰이려면 수동적 헬스 체크가 있어야 한다.
#       이상값 감지를 켠 DestinationRule 을 적용하면 엔드포인트에 priority 가 붙는다. 가장 높은 우선순위는
#       0 이고 명시되지 않으면 그 값이라, 가까운 westus 쪽에는 priority 가 없고 eastus 쪽에 1 이 붙는다.
#       ERROR_RATE 를 1 로 두어 west 를 실패시키면 이상값 감지가 그것을 불건강으로 보고 다음 우선순위인
#       east 로 넘긴다.
# 저자는 페일오버까지만 실습으로 보이고 원래 클러스터로 되돌아오는 장면은 적지 않는다 — 그래서 복귀 전이를 그리지 않는다.
# 타입 스펙: type-state — 유한 상태와 전이가 논점이다. 시작은 채운 점, 전이마다 라벨,
#           coral 은 독자가 주목할 상태 하나(페일오버가 실제로 일어난 자리).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 524
d = D(W, H, "ISTIO IN ACTION · 12-01 §7",
      "가까운 곳부터 쓰고 죽으면 넘긴다",
      "같은 서비스가 두 클러스터에 있을 때 기본은 고르게 나누는 것이고, 이상값 감지를 켜야 지역 정보가 "
      "쓰인다. 색이 붙은 상태가 우선순위 0 이 죽어 1 로 넘어간 자리다.",
      "지역 정보만으로는 부족하고 수동적 헬스 체크가 있어야 발동합니다")

SW, SH = 216, 68
Y = 176
XS = [40, 364, 688, 968]
def state(i, label, sub, c=None, focal=False, w=SW):
    x = XS[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{w}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{w}" height="{SH}" rx="8" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, Y, w, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, Y + 28, label, 12, ACC if focal else (c or INK), KR, "middle", 600)
    d.t(x + w / 2, Y + 48, sub, 9, MUTED, MONO)

d.o.append(f'<circle cx="16" cy="{Y + SH / 2}" r="6" fill="{INK}"/>')
state(0, "양쪽에 고르게", "round robin")
state(1, "가까운 쪽만 쓴다", "priority 0 · westus")
state(2, "먼 쪽으로 넘어간다", "priority 1 · eastus", focal=True)

def lab(x, y, txt, c=MUTED):
    lw = len(txt) * 11 + 12
    d.o.append(f'<rect x="{x - lw / 2}" y="{y - 13}" width="{lw}" height="18" rx="3" fill="{PAPER}"/>')
    d.t(x, y, txt, 11, c, KR, "middle", 600)

d.arrow([(XS[0] + SW, Y + SH / 2), (XS[1] - 2, Y + SH / 2)], MUTED, "ar", 1.4)
lab((XS[0] + SW + XS[1]) / 2, Y - 16, "이상값 감지를 켠다")
d.arrow([(XS[1] + SW, Y + SH / 2), (XS[2] - 2, Y + SH / 2)], ACC, "acc", 1.5)
lab((XS[1] + SW + XS[2]) / 2, Y - 16, "가까운 쪽이 죽는다", ACC)
# 복귀 전이는 그리지 않는다 — 12 장은 페일오버까지만 보이고 되돌아오는 장면을 적지 않는다.

BY = 292
d.box(20, BY, W - 48, 92, PAPER2, RULE, 1.0, 6)
d.t(36, BY + 26, "엔드포인트에 붙는 우선순위", 11, ACC, KR, "start", 600)
d.t(36, BY + 50, '"locality": { "region": "westus", "zone": "0" }                    priority 없음 = 0', 11, INK, MONO, "start")
d.t(36, BY + 70, '"priority": 1,  "locality": { "region": "eastus", "zone": "0" }', 11, MUTED, MONO, "start")

d.t(24, 420, "지역 라벨은 클라우드가 노드에 붙여 둔 것이고 istiod 가 그것을 읽어 워크로드에 채운다", 11, SOFT, KR, "start")
d.t(24, 444, "위는 원문 출력에서 두 호스트의 locality 와 priority 만 뽑아 줄인 것이다 — 실제 출력에는 address · stats · weight 가 함께 나온다", 11, MUTED, KR, "start")
d.legend(468, [("페일오버가 실제로 일어난 자리", ACC), ("우선순위가 정한 순서", MUTED)])
d.save("12-01.locality-failover.svg")
