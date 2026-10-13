# 타입 스펙: type-layers — 위에서 아래로 [사용자] · [도구] · [eBPF 플랫폼] · [커널 훅]. 도구와 플랫폼 사이를 점선 경계로 가려 사용자에게 eBPF 층이 보이지 않음을 보인다. focal 은 eBPF 플랫폼.
# 사실 출처: 추출본 src/ebpf11.txt 213~226행(도구를 쓰지 eBPF 를 직접 쓰지 않는다), 도구 이름은 본 편 §4 · 09-01 Tetragon · 10-01 bpftrace · container-security 13-01 Falco · cilium 01-01,
#   훅 이름은 v7.2 bpf.h(BPF_PROG_TYPE_LIRC_MODE2 L1083 등) · HID-BPF v6.3 · sched_ext v6.12, 플랫폼 요소는 verifier · JIT · 맵 · 헬퍼 · kfunc(kfuncs.rst).
# Layout conventions: 층 h=72, stride 84(y=100·184·268·352), 폭 800(x=80), 왼쪽 인덱스 태그 · 층 이름 · 오른쪽 칩 목록. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 11-01 §4",
      "사용자는 도구까지만 보고 eBPF 층은 그 아래 가려져 있다",
      "kubectl 과 대시보드 아래에 Cilium · Falco 같은 도구가 있고, 도구는 verifier · JIT · 맵 · 헬퍼 · kfunc 를 공유하며 XDP · LSM 같은 커널 훅에 붙는다.",
      "위에서 아래로 사용자, 도구, eBPF 플랫폼, 커널 훅")

LAYERS = [
    ("L4", "사용자", "kubectl · 대시보드", MUTED, False),
    ("L3", "도구", "Cilium · Falco · Tetragon · bpftrace · Pixie", INFO, False),
    ("L2", "eBPF 플랫폼", "verifier · JIT · 맵 · 헬퍼 · kfunc", ACC, True),
    ("L1", "커널 훅", "XDP · TC · kprobe · LSM · HID · sched_ext", OK, False),
]
for i, (tag, name, chips, c, focal) in enumerate(LAYERS):
    y = 100 + i * 84
    d.o.append(f'<rect x="80" y="{y}" width="800" height="72" rx="6" fill="{c}{"1F" if focal else "12"}" stroke="{c}" stroke-width="{1.6 if focal else 1.0}"/>')
    d.t(96, y + 24, tag, 9, SOFT, MONO, "start")
    d.t(96, y + 48, name, 16, INK, KR, "start", 600)
    d.t(864, y + 42, chips, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in chips) else MONO, "end")

# 사용자 · 도구 위쪽이 보이는 구간, 도구 아래는 가려지는 구간 — 점선 경계
by = 100 + 2 * 84 - 6
d.line(48, by, 912, by, BAD, 1.4, "6 5")
d.chip(480, by, "여기부터 사용자에게 보이지 않음", BAD, 12)

d.legend(H - 56, [("사용자", MUTED), ("도구", INFO), ("eBPF 플랫폼", ACC), ("커널 훅", OK), ("보이지 않는 경계", BAD)])
d.save("11-01.visibility-layers.svg")
