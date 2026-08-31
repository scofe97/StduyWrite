# 05-01 §5 메시를 떠나는 요청이 통과하는 판단.
# 본문: "목적지가 내부 서비스 레지스트리에 있으면 나간다. 없으면 outboundTrafficPolicy 가 가른다 — ALLOW_ANY 면 나가고
# REGISTRY_ONLY 면 막힌다. 막힌 목적지를 열려면 ServiceEntry 로 레지스트리에 항목을 넣는다. 색이 붙은 상자가 그 항목."
# 타입 스펙: type-flowchart — 판단 마름모 둘(≤3 출구), 행동 사각형, 병합점. 예=오른쪽, 아니오=아래. 초점은 ServiceEntry 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 600
d = D(W, H, "ISTIO IN ACTION · 05-01 §5",
      "메시를 떠나는 요청이 통과하는 판단",
      "사이드카가 목적지를 Istio 내부 서비스 레지스트리에서 찾는다. 있으면 통과. 없으면 outboundTrafficPolicy 가 ALLOW_ANY 면 통과, REGISTRY_ONLY 면 차단. 차단된 외부 호스트는 ServiceEntry 로 레지스트리에 넣어 연다.",
      "기본값은 ALLOW_ANY. 저자는 REGISTRY_ONLY 로 바꾸되 L3·L4 차단을 겹치라고 합니다")

CX = 260
d.o.append(f'<rect x="{CX - 110}" y="104" width="220" height="40" rx="20" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, 129, "메시 밖으로 가는 요청", 12, INK, KR, "middle", 600)
d.path(f"M {CX} 144 V 172", MUTED, 1.4, m="ar")
# 마름모 1 — 레지스트리에 있는가
y1, hw, hh = 232, 150, 56
d.o.append(f'<polygon points="{CX},{y1 - hh} {CX + hw},{y1} {CX},{y1 + hh} {CX - hw},{y1}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, y1 - 4, "내부 서비스 레지스트리에", 12, INK, KR, "middle", 600)
d.t(CX, y1 + 14, "목적지가 있는가", 12, INK, KR)
# 예 → 오른쪽 통과
d.path(f"M {CX + hw} {y1} H 612", OK, 1.4, m="ok")
d.t((CX + hw + 612) / 2, y1 - 10, "예", 12, OK, KR)
d.o.append(f'<rect x="616" y="{y1 - 20}" width="200" height="40" rx="20" fill="{OK}22" stroke="{OK}" stroke-width="1.2"/>')
d.t(716, y1 + 5, "통과 — 밖으로 나간다", 12, OK, KR, "middle", 600)
# 아니오 → 아래 마름모 2
d.path(f"M {CX} {y1 + hh} V 344", MUTED, 1.4, m="ar")
d.t(CX + 12, 326, "아니오", 12, MUTED, KR, "start")
y2 = 400
d.o.append(f'<polygon points="{CX},{y2 - hh} {CX + hw},{y2} {CX},{y2 + hh} {CX - hw},{y2}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, y2 - 4, "outboundTrafficPolicy", 12, INK, MONO, "middle", 600)
d.t(CX, y2 + 14, "mode ?", 12, INK, MONO)
# ALLOW_ANY → 오른쪽 위로 통과 상자에 합류
d.path(f"M {CX + hw} {y2} H 560 Q 568 {y2} 568 {y2 - 8} V {y1 + 28}", OK, 1.4, m="ok")
d.t(480, y2 - 10, "ALLOW_ANY (기본값)", 12, OK, KR)
# REGISTRY_ONLY → 아래 차단
d.path(f"M {CX} {y2 + hh} V 484", BAD, 1.4, m="bad")
d.t(CX + 12, 470, "REGISTRY_ONLY", 12, BAD, MONO, "start")
d.o.append(f'<rect x="{CX - 110}" y="488" width="220" height="40" rx="20" fill="{BAD}22" stroke="{BAD}" stroke-width="1.2"/>')
d.t(CX, 513, "차단 — 알 수 없는 목적지", 12, BAD, KR, "middle", 600)
# ServiceEntry — 차단에서 레지스트리로 되돌리는 행동(초점)
d.path(f"M {CX + 110} 508 H 612", ACC, 1.4, m="acc")
d.t((CX + 110 + 612) / 2, 498, "열려면", 12, ACC, KR)
d.o.append(f'<rect x="616" y="476" width="260" height="64" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(746, 500, "ServiceEntry", 14, ACC, MONO, "middle", 600)
d.t(746, 522, "hosts · MESH_EXTERNAL · resolution DNS", 11, ACC, MONO)
d.path(f"M 746 476 V 300 Q 746 292 738 292 H {CX + hw + 12}", ACC, 1.2, m="acc", dash="4 3")
d.t(760, 384, "레지스트리에 항목을 넣는다", 12, ACC, KR, "start")
d.legend(556, [("통과", OK), ("차단", BAD), ("레지스트리에 넣는 항목", ACC)])
d.save("05-01.egress-decision.svg")
