# 타입 스펙: type-sequence — 참여자 넷(xdp-hello-ebpf · xdp-hello · 커널 · 패킷), 메시지 여덟. focal 은 attach 한 줄.
# 사실 출처: aya-rs/book a4dad9e examples/xdp-hello — xdp-hello-ebpf/src/main.rs(#[xdp] xdp_hello · try_xdp_hello · info! · XDP_PASS · XDP_ABORTED),
#   xdp-hello/src/main.rs L10(iface 기본 eth0), L26~29(Ebpf::load(include_bytes_aligned!)), L50~53(program_mut("xdp_hello") · load() · attach(&opt.iface, XdpMode::default())),
#   aya v0.14.0 aya-build/src/lib.rs L69~87(bpfel-unknown-none), aya/src/sys/bpf.rs L1320~1321(BPF_PROG_LOAD), README L45~50.
# Layout conventions: 레인 폭 176·중심 x=120·376·632·856, 메시지 stride 56~64(y=196부터), 레일 하단 H-80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


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
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="20" fill="{PAPER}"/>')
            s.t(mx, y + 19, sub, 13, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None, mk="ar"):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m=mk)
        s.t(x + 68, y - 4, label, 13, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 15, sub, 13, MUTED, _kr(sub), "start")


W, H = 960, 752
d = SeqKR(W, H, "LEARNING EBPF · 10-02 §3",
          "Rust 두 크레이트가 하나의 XDP 프로그램을 빌드하고 붙인다",
          "xdp-hello-ebpf 를 rustc 와 bpf-linker 가 ELF 로 만들고, xdp-hello 가 그 ELF 를 포함해 읽어 load 와 attach 를 부른다. 패킷이 오면 xdp_hello 가 로그를 남기고 XDP_PASS 를 돌려준다.",
          "인터페이스 이름 기본값은 eth0")

A, B, K, P = "xdp-hello-ebpf", "xdp-hello", "커널", "패킷"
d.LX = {A: 120, B: 376, K: 632, P: 856}
for nm, sub in ((A, "커널 쪽 크레이트"), (B, "사용자 공간 크레이트"), (K, "XDP 훅"), (P, "eth0 에 도착")):
    x = d.LX[nm]
    d.box(x - 88, 100, 176, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 12, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

d.selfmsg(A, "rustc · bpf-linker", 196, WARN, "bpfel-unknown-none")
d.msg(A, B, "include_bytes_aligned!", 268, MUTED, "ar", sub="ELF xdp-hello")
d.selfmsg(B, "Ebpf::load", 340, INFO, "program_mut(xdp_hello)")
d.msg(B, K, "load()", 408, INFO, "info", sub="BPF_PROG_LOAD")
d.msg(B, K, "attach(\"eth0\", XdpMode::default())", 480, ACC, "acc", sub="XDP 훅에 부착")
d.msg(P, K, "패킷 도착", 544, MUTED, "ar", sub="eth0")
d.selfmsg(K, "try_xdp_hello", 592, OK, "received a packet", mk="ok")
d.msg(K, P, "XDP_PASS", 648, OK, "ok", dash="5 4", sub="그대로 통과")

d.legend(H - 56, [("빌드", WARN), ("적재", INFO), ("부착", ACC), ("프로그램 실행", OK)])
d.save("10-02.aya-xdp-sequence.svg")
