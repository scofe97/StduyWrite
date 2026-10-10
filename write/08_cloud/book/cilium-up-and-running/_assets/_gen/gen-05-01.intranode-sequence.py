# 타입 스펙: type-sequence — 같은 노드 pod-a → pod-b ping 의 echo request·reply 가 거치는 장치 네 레인과 eBPF 프로그램 칩. 레인은 장치, 메시지는 패킷 한 번의 이동.
# 사실 출처: Cilium Up and Running 5장 cil5.txt 줄 92-101(Pod IP·ping), 120-181(eth0@if24·lxc*@if23·lxcc5b0a1b7ddfb), 260-277(bpftool net show cil_from_container), 304-317(tcpdump -i lxcc5b0a1b7ddfb, 요청·응답이 이 장치에서 잡힘)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """한글 라벨을 한글 스택으로, 글자는 12px 로 내보내는 Seq."""
    def lanes(s, names, xs, y0=104, lane_w=196):
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
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.4 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, MONO)


W, H = 920, 620
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 05-01 §1", "같은 노드 Pod 간 ping 이 거치는 장치",
          "pod-a 에서 pod-b 로 echo request, 되돌아오는 echo reply — 장치 이름과 eBPF 프로그램", "pod-a 에서 pod-b 로 echo request, 되돌아오는 echo reply — 장치 이름과 eBPF 프로그램")
A, B, C, E = "pod-a eth0", "lxcbee302eb186c", "lxcc5b0a1b7ddfb", "pod-b eth0"
d.lanes([(A, "10.244.1.203"), (B, "ifindex 24"), (C, "ifindex 26"), (E, "10.244.1.69")],
        [120, 340, 560, 780])
d.rails(588)

d.msg(A, B, "echo request", 188, MUTED, "ar", sub="10.244.1.203 → 10.244.1.69")
d.state(B, "cil_from_container", 236, ACC)
d.msg(B, C, "redirect", 288, MUTED, "ar", sub="정책 · 연결 추적 조회")
d.msg(C, E, "echo request", 348, MUTED, "ar")
d.msg(E, C, "echo reply", 404, MUTED, "ar", dash="5 4", sub="10.244.1.69 → 10.244.1.203")
d.state(C, "cil_from_container", 460, INFO)
d.msg(C, B, "redirect", 516, MUTED, "ar", dash="5 4")
d.msg(B, A, "echo reply", 572, MUTED, "ar", dash="5 4")
d.save("05-01.intranode-sequence.svg")
