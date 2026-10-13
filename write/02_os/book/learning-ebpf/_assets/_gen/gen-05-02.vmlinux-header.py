# 타입 스펙: type-data-flow — 실행 중 커널의 BTF 가 bpftool 을 거쳐 vmlinux.h 가 되고, 포함된 헤더가 오브젝트의 .BTF 가 되는 흐름. focal 은 vmlinux.h 머리의 pragma 한 줄.
# 사실 출처: 추출본 src/ebpf5.txt 569~579행(bpftool btf list: ID 1 vmlinux 5842973B), 595행(bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h), 602~607행(오브젝트의 BTF 와 적재 때 비교),
#   Linux v7.2 tools/bpf/bpftool/btf.c 778~783행(include guard 뒤 #ifndef BPF_NO_PRESERVE_ACCESS_INDEX 안의 #pragma clang attribute push (__attribute__((preserve_access_index)), apply_to = record)).
# Layout conventions: 상단 상자 다섯 y=100·h=112, 폭 144·stride 192(x=24·216·408·600·792), 화살표 간격 48, 주석 상자 y=256·h=56. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 404
d = D(W, H, "LEARNING EBPF · 05-02 §1",
      "커널 BTF 가 vmlinux.h 를 거쳐 오브젝트의 .BTF 가 된다",
      "bpftool 이 실행 중인 커널의 BTF 를 C 헤더로 뽑고, 그 헤더를 포함해 컴파일한 오브젝트에 빌드 때의 구조체 배치가 BTF 로 남는다.",
      "값이 단계마다 이름을 바꿔 가며 이어집니다")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


def card(x, title, lines, c, focal=False):
    d.tone(x, 100, 144, 112, c, 6, "14" if focal else "12", 1.6 if focal else 1.2)
    d.t(x + 72, 128, title, 13, INK, fam(title), "middle", 600)
    for i, s in enumerate(lines):
        d.t(x + 72, 154 + 20 * i, s, 12, MUTED, fam(s), "middle")


card(24, "커널 BTF", ["/sys/kernel/btf/", "vmlinux · ID 1", "5842973B"], INFO)
card(216, "bpftool", ["btf dump file", "format c"], MUTED)
card(408, "vmlinux.h", ["커널 타입 전부", "머리의 pragma"], ACC, True)
card(600, "#include", ['"vmlinux.h"', "hello-buffer-", "config.bpf.c"], MUTED)
card(792, "오브젝트", [".bpf.o", ".BTF 섹션", "빌드 때 배치"], OK)

for x in (168, 360, 552, 744):
    d.arrow([(x + 2, 156), (x + 44, 156)], MUTED, "ar", 1.5)

# vmlinux.h 맨 앞 줄 — focal 주석
d.line(480, 212, 480, 256, ACC, 1.2)
d.tone(216, 256, 720, 56, ACC, 6, "12", 1.4)
d.t(576, 280, "#pragma clang attribute push", 12, MUTED, MONO, "middle")
d.t(576, 300, "(__attribute__((preserve_access_index)), apply_to = record)", 12, INK, MONO, "middle", 600)

d.legend(H - 56, [("커널이 가진 BTF", INFO), ("도구·소스", MUTED), ("논지: 모든 구조체에 붙는 속성", ACC), ("결과", OK)])
d.save("05-02.vmlinux-header.svg")
