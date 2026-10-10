# 타입 스펙: type-sequence — 소스 노드의 hr Pod 에서 발생한 패킷이 VXLAN 터널을 거쳐 Egress Gateway 노드로 이동하고, 지정된 egress IP 로 SNAT 되어 외부 서비스로 전달되는 시퀀스.
# 사실 출처: Cilium Up and Running 11장 cil11.txt 줄 504-506(보조 IP 172.18.0.100), 620-653(hr-egress 정책), 724-739(cilium-dbg bpf egress 10.0.2.194 -> 172.18.0.100, gw 172.18.0.3), 776-786(tcpdump egress_vxlan.pcap: 172.18.0.2 > 172.18.0.4.8472, 안쪽 10.244.1.52 > 172.18.0.7:8080)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, INFO, OK, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """한글 라벨을 한글 스택으로 내보내는 Seq 확장."""
    def lanes(s, names, xs, y0=104, lane_w=190):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, MONO, "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.4 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, MONO)


W, H = 920, 580
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 11-01 §3", "Egress Gateway 패킷 전달 시퀀스",
          "Pod 패킷이 터널을 거쳐 게이트웨이 노드에서 egress IP 로 변환되어 외부로 나간다",
          "Pod 패킷이 터널을 거쳐 게이트웨이 노드에서 egress IP 로 변환되어 외부로 나간다")

A = "hr 클라이언트 Pod"
B = "소스 노드"
C = "게이트웨이 노드"
E = "kind-echo-server"

d.lanes([(A, "10.244.1.52"), (B, "172.18.0.2"), (C, "172.18.0.4"), (E, "172.18.0.7:8080")],
        [115, 345, 575, 805], y0=104, lane_w=190)
d.rails(546)

d.msg(A, B, "curl 요청 송신", 180, INK, "ar", sub="src 10.244.1.52 → dst 172.18.0.7")
d.state(B, "CEGP 정책 매칭", 228, ACC)
d.msg(B, C, "VXLAN 터널 전송", 276, ACC, "ar", sub="outer 172.18.0.2 → 172.18.0.4 (포트 8472)")
d.state(C, "SNAT 172.18.0.100 (정책 egressIP)", 324, OK)
d.msg(C, E, "외부 전달", 372, OK, "ar", sub="src 172.18.0.100 → dst 172.18.0.7")
d.msg(E, C, "응답 반환", 424, MUTED, "ar", dash="5 4", sub="dst 172.18.0.100")
d.msg(C, B, "VXLAN 응답 전달", 472, MUTED, "ar", dash="5 4", sub="outer 172.18.0.4 → 172.18.0.2")
d.msg(B, A, "클라이언트 수신", 520, INK, "ar", dash="5 4", sub="dst 10.244.1.52")

d.save("11-01.egress-gateway-sequence.svg")
