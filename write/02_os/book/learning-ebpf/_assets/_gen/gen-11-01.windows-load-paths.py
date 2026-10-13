# 타입 스펙: type-process — 같은 ELF 에서 세 갈래(네이티브 · JIT · 인터프리터). 값이 카드마다 바뀐다: ELF → 검증 → C → COFF → PE → 서명된 .sys → 적재.
# 사실 출처: ebpf-for-windows v1.6.0 README L32~50(세 방식 · eBPFSvc 가 JIT · 인터프리터는 디버그 빌드만) · L110~126(HVCI 에서 JIT 불가),
#   docs/NativeCodeGeneration.md L26~31(Convert-BpfToNative.ps1 -FileName my_program → my_program.sys) · L44~78(단계 1~6: ELF · 검증 · C 생성 · COFF · PE 링크 · 서명),
#   docs/GettingStarted.md L153~159(ebpfcore.sys 실행 컨텍스트 · ebpfsvc.exe 가 검증·JIT).
# Layout conventions: 카드 w=96·h=64·stride 116(x=20부터), 띠 h=108 · y=88·208·328, 카드 y=띠+28. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 516
d = D(W, H, "LEARNING EBPF · 11-01 §2",
      "같은 ELF 가 세 갈래로 적재되고 HVCI 를 켠 릴리스 환경에서는 네이티브만 돈다",
      "my_program 의 ELF 는 PREVAIL 검증 뒤 bpf2c 로 서명된 .sys 가 되거나, eBPFSvc 가 uBPF 로 JIT 하거나, 디버그 빌드에서만 인터프리터로 돈다.",
      "위는 네이티브, 가운데는 JIT, 아래는 인터프리터")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


def band(y, name, c):
    d.box(12, y, 936, 108, PAPER2, c, 0.9, 8)
    d.t(24, y + 18, name, 9, SOFT, MONO, "start")


def card(col, y, c, l1, l2, focal=False, dash=False):
    x = 20 + col * 116
    d.tone(x, y, 96, 64, c, 6, "1F" if focal else "12", 1.6 if focal else 1.2)
    if dash:
        d.o[-1] = d.o[-1].replace("/>", ' stroke-dasharray="5 4"/>')
    d.t(x + 48, y + 28, l1, 11, INK, fam(l1), "middle", 600)
    d.t(x + 48, y + 48, l2, 12, MUTED, fam(l2))
    return x


def link(col_a, col_b, y, c="ar", dash=None, col=MUTED):
    xa = 20 + col_a * 116 + 98
    xb = 20 + col_b * 116 - 2
    d.arrow([(xa, y), (xb, y)], col, c, 1.5, dash)


# 네이티브
band(88, "NATIVE", OK)
Y1 = 116
steps = [("my_program", "ELF", INFO), ("PREVAIL", "검증", OK), ("bpf2c", "C 생성", WARN), ("C 컴파일러", "COFF", WARN),
         ("링커", "PE", WARN), ("서명", "서명된 PE", WARN), ("my_program", ".sys 드라이버", ACC), ("ebpfcore.sys", "실행 컨텍스트", OK)]
for i, (a, b, c) in enumerate(steps):
    card(i, Y1, c, a, b, focal=(i == 6))
for i in range(7):
    link(i, i + 1, Y1 + 32, "acc" if i == 5 else "ar", None, ACC if i == 5 else MUTED)

# JIT
band(208, "JIT", INFO)
Y2 = 236
card(0, Y2, INFO, "my_program", "ELF")
card(1, Y2, INFO, "eBPFSvc.exe", "PREVAIL 검증")
card(2, Y2, WARN, "uBPF", "JIT")
card(3, Y2, OK, "ebpfcore.sys", "실행 컨텍스트")
for i in range(3):
    link(i, i + 1, Y2 + 32)
d.chip(640, Y2 + 32, "HVCI 환경에서 JIT 불가", BAD, 12)

# 인터프리터
band(328, "INTERPRETER", MUTED)
Y3 = 356
card(0, Y3, MUTED, "my_program", "ELF", dash=True)
card(1, Y3, MUTED, "eBPFSvc.exe", "PREVAIL 검증", dash=True)
card(2, Y3, MUTED, "uBPF", "인터프리터", dash=True)
card(3, Y3, MUTED, "ebpfcore.sys", "실행 컨텍스트", dash=True)
for i in range(3):
    link(i, i + 1, Y3 + 32, "ar", "5 4")
d.chip(640, Y3 + 32, "디버그 빌드만", MUTED, 12)

d.legend(H - 56, [("입력 ELF", INFO), ("변환 도구", WARN), ("검증", OK), ("서명된 드라이버", ACC), ("HVCI 불가", BAD)])
d.save("11-01.windows-load-paths.svg")
