# 타입 스펙: type-layers — 위에서 아래로 소스 한 줄 → libbpf 매크로 셋 → 헬퍼와 clang 내장 → 오브젝트의 CO-RE 재배치 기록. accent 는 clang 내장 층 하나.
# 사실 출처: 추출본 src/ebpf5.txt 1006~1015행(bpf_core_read 정의)·1038~1057행(BPF_CORE_READ 예), libbpf v1.8.0 src/bpf_core_read.h 311~312행(bpf_core_read)·525~529행(BPF_CORE_READ),
#   추출본 1031~1035행(재배치 기록을 적재 때 libbpf 가 고침 — 과정은 05-03).
# Layout conventions: 층 높이 64·stride 96(y=108·204·300·396), 층 폭 840(x=84), 인덱스 태그 x=24, 층 사이 화살표 간격 32. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 556
d = D(W, H, "LEARNING EBPF · 05-02 §4",
      "소스 한 줄은 세 번의 읽기가 되고 오브젝트에 재배치 기록이 남는다",
      "BPF_CORE_READ 한 줄이 bpf_core_read 셋으로 펼쳐지고, 각각이 헬퍼 호출과 clang 내장으로 바뀌어 오브젝트의 .BTF.ext 에 재배치 기록을 남긴다.",
      "맨 아래 층의 기록은 적재 때 libbpf 가 사용합니다")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


LAYERS = [
    ("소스", ["d = BPF_CORE_READ(a, b, c, d)"], INFO, False),
    ("libbpf 매크로", ["bpf_core_read(&b, 8, &a->b)", "bpf_core_read(&c, 8, &b->c)", "bpf_core_read(&d, 8, &c->d)"], INFO, False),
    ("헬퍼와 clang 내장", ["bpf_probe_read_kernel(dst, sz,", "  (const void *)__builtin_preserve_access_index(src))"], ACC, True),
    ("오브젝트 .BTF.ext", ["CO-RE 재배치 기록"], OK, False),
]
for i, (name, lines, c, focal) in enumerate(LAYERS):
    y = 108 + 96 * i
    d.t(24, y + 36, f"L{i + 1}", 9, SOFT, MONO, "start")
    d.tone(84, y, 840, 64, c, 6, "14" if focal else "10", 1.6 if focal else 1.1)
    d.t(104, y + 38, name, 13, INK, fam(name), "start", 600)
    top = y + 38 - 18 * (len(lines) - 1) // 2 + 0
    for k, s in enumerate(lines):
        d.t(344, top + 18 * k, s, 12, MUTED if not focal else INK, fam(s), "start")
    if i < len(LAYERS) - 1:
        d.arrow([(504, y + 64 + 2), (504, y + 96 - 2)], MUTED, "ar", 1.4)

d.legend(H - 56, [("소스·매크로", INFO), ("clang 내장", ACC), ("오브젝트 기록", OK)])
d.save("05-02.core-read-layers.svg")
