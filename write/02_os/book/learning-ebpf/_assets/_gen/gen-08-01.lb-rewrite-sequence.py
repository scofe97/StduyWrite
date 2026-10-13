# 타입 스펙: type-sequence — 참여자 넷(client .4 · LB .5 · backend A .2 · backend B .3), 메시지 여섯과 점선 대안 하나. focal 은 LB 안의 주소 고침 두 번.
# 사실 출처: lizrice/lb-from-scratch xdp_lb_kern.c (HEAD 6f57f1c) 3~8행(IP_ADDRESS 매크로, BACKEND_A 2·BACKEND_B 3·CLIENT 4·LB 5)·34~53행(saddr 가 CLIENT 면 bpf_ktime_get_ns() % 2 로 백엔드를 고르고
#   iph->daddr·eth->h_dest[5] 를 바꿈, 아니면 CLIENT 로, iph->saddr = LB, iph_csum, XDP_TX), Makefile 12~16행(xdpgeneric 으로 eth0 에 붙임),
#   추출본 ebpf8.txt 311~330행(client·LB·backend 둘 구성)·410~419행(주소를 고치고 XDP_TX).
# Layout conventions: 레인 중심 x 128·368·608·848, 메시지 stride 64(y=196 시작). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 12)/2}" y="{y - 23}" width="{_w(label, 12)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 11)/2}" y="{y + 5}" width="{_w(sub, 11)}" height="18" fill="{PAPER}"/>')
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 12, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 13, sub, 11, MUTED, _kr(sub), "start")

W, H = 960, 640
d = SeqKR(W, H, "LEARNING EBPF · 08-01 §3", "로드밸런서는 주소를 고쳐 쓰고 XDP_TX 로 같은 인터페이스에 되돌린다",
          "client 172.17.0.4 가 LB 172.17.0.5 로 보낸 TCP 패킷을 LB 의 eth0 XDP 프로그램이 src 를 .5, dst 를 .2 또는 .3 으로 고치고 h_dest[5] 를 같은 숫자로 바꾼 뒤 XDP_TX 로 되돌린다. 백엔드의 응답 src .2 dst .5 는 src .5 dst .4 로 고쳐 같은 방식으로 되돌린다.",
          "요청은 백엔드로, 응답은 클라이언트로 같은 인터페이스에서 되돌아갑니다")

NAMES = (("client", "172.17.0.4"), ("LB · eth0 XDP", "172.17.0.5"), ("backend A", "172.17.0.2"), ("backend B", "172.17.0.3"))
d.LX = {"client": 128, "LB": 368, "A": 608, "B": 848}
KEYS = ["client", "LB", "A", "B"]
for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 108, 100, 216, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 11, MUTED, MONO)
d.lane_top = 144
d.rails(H - 80)

d.msg("client", "LB", "TCP · src .4 → dst .5", 196, MUTED, "ar")
d.selfmsg("LB", "주소 고침 · XDP_TX", 252, ACC, "daddr .2 · h_dest[5]=2")
d.msg("LB", "A", "src .5 → dst .2", 316, OK, "ok", sub="ktime 짝수")
d.msg("LB", "B", "src .5 → dst .3", 360, INFO, "info", dash="6 4", sub="ktime 홀수")
d.msg("A", "LB", "응답 src .2 → dst .5", 428, MUTED, "ar")
d.selfmsg("LB", "주소 고침 · XDP_TX", 488, ACC, "daddr .4 · h_dest[5]=4")
d.msg("LB", "client", "src .5 → dst .4", 548, OK, "ok")

d.legend(H - 56, [("주소 고침", ACC), ("백엔드 A", OK), ("백엔드 B", INFO)])
d.save("08-01.lb-rewrite-sequence.svg")
