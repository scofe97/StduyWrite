# 05-01 §5 메시를 떠나는 요청이 통과하는 판단.
# 본문 근거: 05-01 §5 ("목적지가 내부 서비스 레지스트리에 있으면 나간다. 없으면 outboundTrafficPolicy 가 가른다").
# 값 근거: ch05.txt §5.5 (ALLOW_ANY, REGISTRY_ONLY, ServiceEntry hosts · location: MESH_EXTERNAL · resolution: DNS).
# 타입 스펙: type-flowchart — 판단 마름모 둘(≤3 출구), 행동 사각형, 병합점. 예=오른쪽, 아니오=아래. 초점은 ServiceEntry 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 608
d = D(W, H, "ISTIO IN ACTION · 05-01 §5",
      "메시를 떠나는 요청이 통과하는 판단",
      "사이드카가 목적지를 Istio 내부 서비스 레지스트리에서 찾는다. 있으면 통과. 없으면 outboundTrafficPolicy 가 ALLOW_ANY 면 통과, REGISTRY_ONLY 면 차단. 차단된 외부 호스트는 ServiceEntry 로 레지스트리에 넣어 연다.",
      "기본값은 ALLOW_ANY. REGISTRY_ONLY 로 바꾸면 미등록 목적지가 막힙니다. 우회하는 Pod 는 L3·L4 차단이 맡습니다")

CX = 252
d.o.append(f'<rect x="{CX - 110}" y="104" width="220" height="40" rx="20" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, 129, "메시 밖으로 가는 요청", 13, INK, KR, "middle", 600)
d.path(f"M {CX} 144 V 172", MUTED, 1.4, m="ar")
# 마름모 1 — 레지스트리에 있는가
y1, hw, hh = 232, 152, 56
d.o.append(f'<polygon points="{CX},{y1 - hh} {CX + hw},{y1} {CX},{y1 + hh} {CX - hw},{y1}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, y1 - 4, "내부 서비스 레지스트리에", 13, INK, KR, "middle", 600)
d.t(CX, y1 + 16, "목적지가 있는가", 13, INK, KR)
# 예 → 오른쪽 통과
d.path(f"M {CX + hw} {y1} H 584", OK, 1.4, m="ok")
d.t((CX + hw + 584) / 2, y1 - 12, "예", 13, OK, KR)
d.o.append(f'<rect x="588" y="{y1 - 20}" width="208" height="40" rx="20" fill="{OK}22" stroke="{OK}" stroke-width="1.2"/>')
d.t(692, y1 + 5, "통과 — 밖으로 나간다", 13, OK, KR, "middle", 600)
# 아니오 → 아래 마름모 2
d.path(f"M {CX} {y1 + hh} V 344", MUTED, 1.4, m="ar")
d.t(CX + 12, 326, "아니오", 13, MUTED, KR, "start")
y2 = 400
d.o.append(f'<polygon points="{CX},{y2 - hh} {CX + hw},{y2} {CX},{y2 + hh} {CX - hw},{y2}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, y2 - 4, "outboundTrafficPolicy", 12, INK, MONO, "middle", 600)
d.t(CX, y2 + 14, "mode ?", 12, INK, MONO)
# ALLOW_ANY → 오른쪽 위로 통과 상자 하단 중앙으로 연결
d.path(f"M {CX + hw} {y2} H 684 Q 692 {y2} 692 {y2 - 8} V {y1 + 22}", OK, 1.4, m="ok")
d.t(528, y2 - 12, "ALLOW_ANY (기본값)", 13, OK, KR)
# REGISTRY_ONLY → 아래 차단
d.path(f"M {CX} {y2 + hh} V 484", BAD, 1.4, m="bad")
d.t(CX + 12, 470, "REGISTRY_ONLY", 12, BAD, MONO, "start")
d.o.append(f'<rect x="{CX - 110}" y="488" width="220" height="40" rx="20" fill="{BAD}22" stroke="{BAD}" stroke-width="1.2"/>')
d.t(CX, 513, "차단 — 알 수 없는 목적지", 13, BAD, KR, "middle", 600)
# ServiceEntry — 차단에서 레지스트리로 되돌리는 행동(초점). 오른쪽 외곽(x=844)을 타고 위(y=164)로 우회해 겹침 방지
d.path(f"M {CX + 110} 508 H 584", ACC, 1.4, m="acc")
d.t((CX + 110 + 584) / 2, 496, "열려면", 13, ACC, KR)
d.o.append(f'<rect x="588" y="476" width="288" height="64" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(732, 500, "ServiceEntry", 14, ACC, MONO, "middle", 600)
d.t(732, 522, "hosts · MESH_EXTERNAL · resolution DNS", 11, ACC, MONO)
d.path(f"M 844 476 V 172 Q 844 164 836 164 H 340 Q 332 164 332 172 V 205", ACC, 1.2, m="acc", dash="4 3")
d.t(588, 154, "레지스트리에 넣으면 다음부터 '예'", 13, ACC, KR)
d.legend(564, [("통과", OK), ("차단", BAD), ("레지스트리에 넣는 항목", ACC)])
d.save("05-01.egress-decision.svg")
