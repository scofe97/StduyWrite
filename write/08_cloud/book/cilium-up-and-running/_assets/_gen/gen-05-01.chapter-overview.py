# 타입 스펙: type-flowchart — 패킷 한 개가 호스트 veth 의 cil_from_container 에서 출발해 같은 노드 직행(§1), native routing(§2), VXLAN(§3), Geneve(§4) 로 갈리는 분기 흐름도.
# 사실 출처: Cilium Up and Running 5장 ch05.txt 줄 98-101(10.244.1.203→10.244.1.69, ttl=63), 260-277(cil_from_container), 486-494(10.10.0.32/27 via 172.18.0.2), 698-710(172.18.0.3→172.18.0.4 UDP 8472, 10.244.0.185→10.244.1.212, +50B), 940-955(192.168.10.5→192.168.10.4 UDP 6081, 10.0.0.125→10.0.2.75, TLV DSR)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 760
d = D(W, H, "CILIUM UP AND RUNNING · 05-01 OVERVIEW",
      "패킷 하나가 목적지 Pod 에 닿는 세 길 (터널은 두 종류)",
      "같은 노드인지는 패킷마다 판정하고, 다른 노드로 가는 길은 설치 때 고른 라우팅 모드를 따릅니다",
      "같은 노드인지는 패킷마다 판정하고, 다른 노드로 가는 길은 설치 때 고른 라우팅 모드를 따릅니다")

CX = 200


def diamond(cx, cy, hw, hh, lines):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{SOFT}" stroke-width="1.1"/>')
    if len(lines) == 1:
        d.t(cx, cy + 5, lines[0], 13, INK, KR, "middle", 600)
    else:
        d.t(cx, cy - 5, lines[0], 13, INK, KR, "middle", 600)
        d.t(cx, cy + 15, lines[1], 13, INK, KR, "middle", 600)


def outcome(y, sec, title, line1, line2, tone):
    x, w, h = 480, 448, 84
    d.tone(x, y, w, h, tone, r=6, op="14", sw=1.1)
    d.chip(x + w - 24, y + 16, sec, tone, 11)
    d.t(x + 16, y + 26, title, 14, tone, KR, "start", 600)
    d.t(x + 16, y + 48, line1, 12, INK, MONO, "start")
    d.t(x + 16, y + 70, line2, 13, MUTED, KR, "start")


# 1. Start (oval rx=20)
d.box(80, 96, 240, 44, PAPER2, SOFT, 1.1, r=20)
d.t(CX, 115, "Pod eth0 출발", 13, INK, KR, "middle", 600)
d.t(CX, 132, "예: 10.244.1.203 (pod-a)", 11, MUTED, MONO, "middle")
d.arrow([(CX, 140), (CX, 166)], MUTED, "ar", 1.4)

# 2. Common eBPF judgment (focal ACC)
d.tone(48, 168, 304, 56, ACC, r=6, op="14", sw=1.4)
d.chip(332, 184, "§1", ACC, 11)
d.t(188, 192, "lxc* · cil_from_container", 13, ACC, MONO, "middle", 600)
d.t(CX, 213, "tcx/ingress 신원·정책·연결 추적 판정", 13, MUTED, KR, "middle")
d.arrow([(CX, 224), (CX, 254)], ACC, "acc", 1.4)

# 3. Decision 1: same node?
diamond(CX, 296, 112, 40, ["같은 노드 Pod 인가?"])
d.arrow([(312, 296), (478, 296)], OK, "ok", 1.4)
d.t(396, 286, "예 · 맵 일치", 13, OK, KR, "middle", 600)
outcome(254, "§1", "같은 노드 직행 · eBPF 리다이렉트",
        "lxcbee302eb186c → lxcc5b0a1b7ddfb → pod-b",
        "10.244.1.203 → 10.244.1.69 · 추가 헤더 0B", OK)

d.arrow([(CX, 336), (CX, 382)], MUTED, "ar", 1.4)
d.t(214, 364, "아니오 (다른 노드)", 13, MUTED, KR, "start", 600)

# 4. Decision 2: native routing?
diamond(CX, 424, 120, 40, ["하부 망이 PodCIDR 을", "라우팅하는가?"])
d.arrow([(320, 424), (478, 424)], OK, "ok", 1.4)
d.t(398, 414, "예 · L2·정적·BGP", 13, OK, KR, "middle", 600)
outcome(382, "§2", "native routing · 커널 경로표 전달",
        "10.10.0.32/27 via 172.18.0.2 dev eth0",
        "Pod IP 그대로 송출 · 추가 헤더 0B", OK)

d.arrow([(CX, 464), (CX, 510)], WARN, "warn", 1.4)
d.t(214, 492, "아니오 (터널 캡슐화)", 13, WARN, KR, "start", 600)

# 5. Decision 3: Geneve option?
diamond(CX, 552, 116, 40, ["DSR 등 TLV 옵션이", "필요한가?"])
d.arrow([(316, 552), (478, 552)], WARN, "warn", 1.4)
d.t(398, 542, "아니오 (기본값)", 13, WARN, KR, "middle", 600)
outcome(508, "§3", "VXLAN 터널 · cilium_vxlan",
        "외부 172.18.0.3 → 172.18.0.4 · UDP 8472",
        "내부 10.244.0.185 → 10.244.1.212 · +50B", WARN)

d.arrow([(CX, 592), (CX, 650), (478, 650)], WARN, "warn", 1.4)
d.t(214, 624, "예 (TLV 옵션)", 13, WARN, KR, "start", 600)
outcome(608, "§4", "Geneve 터널 · cilium_geneve",
        "외부 192.168.10.5 → 192.168.10.4 · UDP 6081",
        "내부 10.0.0.125 → 10.0.2.75 · TLV 옵션(DSR)", WARN)

LEG_Y = 716
d.legend(LEG_Y, [("공통 판정 (핵심)", ACC), ("추가 헤더 없음", OK), ("터널 헤더 비용", WARN)])
d.save("05-01.chapter-overview.svg")
