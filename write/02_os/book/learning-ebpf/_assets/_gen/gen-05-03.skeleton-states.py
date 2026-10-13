# 타입 스펙: type-state — 시작점 하나, 상태 셋(열림 · 적재됨 · 부착됨), 끝점 하나. 전이 이름이 곧 스켈레톤 함수(__open · __load · __attach · __destroy). focal 은 값이 갈리는 '적재됨'.
# 사실 출처: 추출본 src/ebpf5.txt 1414~1427행(open = ELF 를 구조체로, load = 커널에 싣고 CO-RE 수정), 1430~1445행(__open · __load 분리), 1512~1526행(__attach 는 SEC() 에서 부착점을 가져옴).
#   적재 뒤 .data·.bss 를 mmap 으로 공유하고 .rodata 를 얼리는 동작은 libbpf v1.8.0 src/libbpf.c 5380~5445행(populate_internal_map)·15680~15700행(load_skeleton),
#   bpftool-gen.rst(linux v7.2) 100~134행. SEC 이름 ksyscall/execve 는 예제 저장소 91ded4a chapter5/hello-buffer-config.bpf.c.
# Layout conventions: 상태 176×168, x=96·364·632(간격 92), y=116, 전이 화살표 y=200, 시작 점 cx=20, 끝 고리 cx=932. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, SOFT, RULE, PAPER, KR, MONO


def fam(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


W, H = 960, 436
d = D(W, H, "LEARNING EBPF · 05-03 §3",
      "스켈레톤 구조체가 거치는 네 상태와 전이 함수",
      "열림에서는 skel->rodata 와 skel->data 가 사용자 메모리라 초기값을 쓸 수 있고, __load 뒤에는 .data 와 .bss 가 맵과 mmap 으로 공유되며 .rodata 는 frozen 이 되고, __attach 로 execve 에 붙고, __destroy 로 해제된다.",
      "초기값은 열림에서, 적재 뒤 쓰기는 .data · .bss 만")

SW, SH, SY = 176, 168, 116
XS = (96, 364, 632)
MY = SY + SH // 2

STATES = [
    ("열림", INFO, False, [("ELF 바이트 → 구조체", 13, KR), ("skel->rodata", 12, MONO), ("skel->data", 12, MONO), ("사용자 메모리 · 초기값 쓰기", 12, KR)]),
    ("적재됨", ACC, True, [("CO-RE 수정", 13, KR), ("BPF_MAP_CREATE", 12, MONO), ("BPF_PROG_LOAD", 12, MONO), (".data · .bss: mmap 공유", 12, KR), (".rodata: frozen", 12, MONO)]),
    ("부착됨", OK, False, [("ksyscall/execve", 12, MONO), ("execve 에 kprobe 로 부착", 12, KR), ("SEC 이름에서 자동", 12, KR)]),
]
for x, (name, c, foc, lines) in zip(XS, STATES):
    d.tone(x, SY, SW, SH, c, 8, "1F" if foc else "12", 1.4 if foc else 1.2)
    d.t(x + 16, SY + 30, name, 15, c if not foc else ACC, KR, "start", 600)
    for i, (txt, size, f) in enumerate(lines):
        d.t(x + 16, SY + 60 + i * 24, txt, size, INK if i == 0 else MUTED, f, "start")

# 시작 점 · 끝 고리
d.o.append(f'<circle cx="20" cy="{MY}" r="6" fill="{INK}"/>')
d.o.append(f'<circle cx="932" cy="{MY}" r="8" fill="none" stroke="{INK}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="932" cy="{MY}" r="5" fill="{INK}"/>')
d.t(932, MY + 32, "해제", 12, MUTED, KR)

# 전이 — 화살표 위에 함수 이름
TR = [((30, MY), (XS[0] - 4, MY), "__open", 61),
      ((XS[0] + SW + 2, MY), (XS[1] - 6, MY), "__load", 318),
      ((XS[1] + SW + 2, MY), (XS[2] - 6, MY), "__attach", 586),
      ((XS[2] + SW + 2, MY), (916, MY), "__destroy", 864)]
for (a, b, name, chip_x) in TR:
    d.arrow([a, b], MUTED, "ar", 1.5)
    d.chip(chip_x, MY - 26, name, ACC if name == "__load" else MUTED, 12)

# __open_and_load 가 첫 두 전이를 묶는다
BY = SY + SH + 32
d.line(XS[0] + SW // 2, SY + SH + 2, XS[0] + SW // 2, BY, MUTED, 1.2)
d.line(XS[0] + SW // 2, BY, XS[1] + SW // 2, BY, MUTED, 1.2)
d.line(XS[1] + SW // 2, BY, XS[1] + SW // 2, SY + SH + 2, MUTED, 1.2)
d.chip((XS[0] + XS[1] + SW) // 2, BY, "__open_and_load", MUTED, 12)

d.legend(H - 56, [("열림", INFO), ("적재됨", ACC), ("부착됨", OK), ("전이 함수", MUTED)])
d.save("05-03.skeleton-states.svg")
