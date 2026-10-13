# 타입 스펙: type-architecture — 네 스택을 세로로 나란히 둔다. 위는 사용자 공간 언어, 가운데는 libbpf 를 거치는지, 아래는 bpf() 와 커널 쪽 언어. libbpf 를 거치지 않는 둘은 긴 직접 화살표.
# 사실 출처: libbpfgo README L21~28(CGo 로 libbpf 링크), libbpf-rs v0.27.2 libbpf-rs/Cargo.toml L10(libbpf-sys 래퍼), cilium/ebpf v0.22.0 internal/sys/syscall_other.go L34(SYS_BPF 직접)
#   btf/core.go L17~18(libbpf 에서 파생한 CO-RE), aya v0.14.0 README L45~50(libbpf 없음) · aya-obj/src/btf/relocation.rs(BTF 재배치), ebpf.io Infrastructure(libbpfgo·libbpf-rs CO-RE 지원).
# Layout conventions: 열 w=208·stride 232(x=24·256·488·720), 행 h=44·stride 64(y=136·200·264), bpf() 상자 y=344, 커널 쪽 상자 h=56(y=408). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 544
d = D(W, H, "LEARNING EBPF · 10-02 §2",
      "libbpf 를 거치는 둘과 bpf() 를 직접 부르는 둘",
      "libbpfgo 는 CGo 와 libbpf 를, libbpf-rs 는 libbpf-sys 와 libbpf 를 거쳐 bpf() 에 닿는다. ebpf-go 와 Aya 는 libbpf 없이 직접 닿는다. 커널 쪽 언어는 Aya 만 Rust 이다.",
      "위는 사용자 공간 언어, 아래는 커널 쪽 언어")

STACKS = [
    ("libbpfgo", "Go", ("CGo", "libbpf (C)"), "C", "libbpf 의 CO-RE"),
    ("libbpf-rs", "Rust", ("libbpf-sys", "libbpf (C)"), "C", "libbpf 의 CO-RE"),
    ("ebpf-go", "Go", None, "C", "Go 구현 CO-RE"),
    ("Aya", "Rust", None, "Rust", "Rust 구현 CO-RE"),
]
X0, CW, ST = 24, 208, 232
Y_LANG, Y_A, Y_B, Y_SYS, Y_KERN = 136, 200, 264, 344, 408
SYS_H = 44


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


# 화살표 먼저
for i, (name, lang, mid, kern, core) in enumerate(STACKS):
    cx = X0 + i * ST + CW // 2
    if mid:
        d.arrow([(cx, Y_LANG + 44), (cx, Y_A - 4)], INFO, "info", 1.5)
        d.arrow([(cx, Y_A + 44), (cx, Y_B - 4)], INFO, "info", 1.5)
        d.arrow([(cx, Y_B + 44), (cx, Y_SYS - 4)], INFO, "info", 1.5)
    else:
        d.arrow([(cx, Y_LANG + 44), (cx, Y_SYS - 4)], OK, "ok", 1.8)
        d.chip(cx, 240, "직접 호출", OK, 12)

for i, (name, lang, mid, kern, core) in enumerate(STACKS):
    x = X0 + i * ST
    cx = x + CW // 2
    d.t(cx, 116, name, 15, INK, MONO, "middle", 600)
    d.tone(x, Y_LANG, CW, 44, MUTED, 6, "12", 1.0)
    d.t(cx, Y_LANG + 28, lang, 14, INK, MONO, "middle", 600)
    if mid:
        for y, txt in ((Y_A, mid[0]), (Y_B, mid[1])):
            d.tone(x, y, CW, 44, INFO, 6, "12", 1.2)
            d.t(cx, y + 28, txt, 13, INK, MONO, "middle", 600)
    d.tone(x, Y_SYS, CW, SYS_H, WARN, 6, "12", 1.2)
    d.t(cx, Y_SYS + 28, "bpf() 시스템 콜", 13, INK, KR, "middle", 600)
    focal = kern == "Rust"
    d.tone(x, Y_KERN, CW, 56, ACC if focal else MUTED, 6, "14" if focal else "12", 1.6 if focal else 1.0)
    d.t(cx, Y_KERN + 24, "커널 쪽 " + kern, 13, INK, KR, "middle", 600)
    d.t(cx, Y_KERN + 44, core, 12, MUTED, KR)

d.legend(H - 56, [("libbpf 경유", INFO), ("직접 호출", OK), ("bpf()", WARN), ("커널 쪽도 Rust", ACC)])
d.save("10-02.stack-compare.svg")
