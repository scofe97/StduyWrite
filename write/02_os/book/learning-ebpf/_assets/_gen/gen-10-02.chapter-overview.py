# 타입 스펙: type-tree — 뿌리 하나, 사용자 공간 언어 둘(Go · Rust), 잎 일곱(라이브러리). 잎 안에 기반과 커널 쪽 언어를 두 줄로 둔다. 깊이 3.
# 사실 출처: cilium/ebpf v0.22.0 internal/sys/syscall_other.go L34(bpf() 직접), aquasecurity/libbpfgo README L21~28(libbpf + CGo),
#   libbpf-rs v0.27.2 README L3(libbpf 래퍼) · libbpf-bootstrap examples/rust/profile/build.rs(커널 쪽 C), aya v0.14.0 README L45~50(libbpf·BCC 없음),
#   gobpf 16120a1 README L5~7(BCC 바인딩, 마지막 커밋 2022-10-05), foniod/redbpf archived=true, rust-bpf/rust-bcc README L3(Unmaintained).
# Layout conventions: 잎 w=116·h=92·stride 128(x=36부터), 언어 노드 w=160·h=44, 뿌리 w=240·h=44. 연결선은 직각 버스. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 480
d = D(W, H, "LEARNING EBPF · 10-02",
      "사용자 공간 언어마다 라이브러리가 갈리고 기반과 커널 쪽 언어가 다르다",
      "Go 에는 gobpf · ebpf-go · libbpfgo, Rust 에는 libbpf-rs · Aya · redbpf · rust-bcc 가 있다. 커널 쪽도 Rust 인 것은 Aya 와 redbpf 둘이다.",
      "잎마다 기반(둘째 줄)과 커널 쪽 언어(셋째 줄)")

LX0, LW, LH, ST = 36, 116, 92, 128
LEAVES = [
    ("gobpf", "BCC", "커널 C 문자열", WARN),
    ("ebpf-go", "bpf() 직접", "커널 C", OK),
    ("libbpfgo", "libbpf + CGo", "커널 C", OK),
    ("libbpf-rs", "libbpf", "커널 C", OK),
    ("Aya", "bpf() 직접", "커널 Rust", ACC),
    ("redbpf", "bitcode 변환", "커널 Rust", BAD),
    ("rust-bcc", "BCC", "커널 C 문자열", BAD),
]
cx = [LX0 + i * ST + LW // 2 for i in range(7)]
go_c = (cx[0] + cx[2]) // 2
rs_c = (cx[3] + cx[6]) // 2
root_c = (go_c + rs_c) // 2
ROOT_Y, LANG_Y, LEAF_Y = 100, 196, 292

# 연결선 먼저
d.line(root_c, ROOT_Y + 44, root_c, 172, MUTED, 1.2)
d.line(go_c, 172, rs_c, 172, MUTED, 1.2)
for c in (go_c, rs_c):
    d.line(c, 172, c, LANG_Y, MUTED, 1.2)
d.line(go_c, LANG_Y + 44, go_c, 268, MUTED, 1.2)
d.line(rs_c, LANG_Y + 44, rs_c, 268, MUTED, 1.2)
d.line(cx[0], 268, cx[2], 268, MUTED, 1.2)
d.line(cx[3], 268, cx[6], 268, MUTED, 1.2)
for x in cx:
    d.line(x, 268, x, LEAF_Y, MUTED, 1.2)

d.box(root_c - 120, ROOT_Y, 240, 44, PAPER2, RULE, 1.0)
d.t(root_c, ROOT_Y + 28, "사용자 공간 라이브러리", 15, INK, KR, "middle", 600)
for c, name in ((go_c, "Go"), (rs_c, "Rust")):
    d.box(c - 80, LANG_Y, 160, 44, PAPER2, RULE, 1.0)
    d.t(c, LANG_Y + 28, name, 15, INK, MONO, "middle", 600)

for i, (name, base, kern, col) in enumerate(LEAVES):
    x = LX0 + i * ST
    d.tone(x, LEAF_Y, LW, LH, col, 6, "14" if col == ACC else "12", 1.6 if col == ACC else 1.2)
    d.t(x + LW / 2, LEAF_Y + 26, name, 13, INK, MONO, "middle", 600)
    d.t(x + LW / 2, LEAF_Y + 50, base, 12, MUTED, KR if any("가" <= c <= "힣" for c in base) else MONO)
    d.t(x + LW / 2, LEAF_Y + 72, kern, 12, MUTED, KR)

d.legend(H - 56, [("활성", OK), ("유지 멈춤", WARN), ("보관됨 · Unmaintained", BAD), ("양쪽 Rust · 활성", ACC)])
d.save("10-02.chapter-overview.svg")
