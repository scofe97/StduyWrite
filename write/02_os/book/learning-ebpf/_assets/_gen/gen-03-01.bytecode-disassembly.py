# 타입 스펙: type-data-flow — C 소스 세 블록이 디스어셈블리 명령 바이트와 옵코드 해석으로 변환되는 흐름
# 사실 출처: 《Learning eBPF》 Ch.3 6~8쪽(llvm-objdump -S hello.bpf.o 12슬롯 역어셈블.
#   7쪽: bpf_printk 줄 five lines · counter++ three lines · return two lines), RFC 9669, 본문 §3(185행 슬롯 12개, 189행 15 = 14바이트 + NUL)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 03-01 §3",
      "C 소스에서 바이트코드 오프셋과 디스어셈블리로의 변환",
      "C 소스 세 블록과 12개 바이트코드 슬롯 및 역어셈블 대응 관계",
      "C 소스 줄 · 8바이트 슬롯 오프셋 · opcode 바이트 · 역어셈블 해석")

# 좌측 C 소스 3개 블록
SX, SW = 24, 304
BLOCKS = [
    ("bpf_printk()", 'bpf_printk("Hello World %d", counter);', INFO, 110, 160),
    ("counter++", "counter++;", WARN, 274, 96),
    ("return", "return XDP_PASS;", OK, 374, 61),
]

for title, code, c, y, h in BLOCKS:
    d.tone(SX, y, SW, h, c, 6, "12", 1.2)
    d.t(SX + 14, y + 24, title, 13, c, MONO, "start", 600)
    d.t(SX + 14, y + 46, code, 11, INK, MONO, "start")

# 우측 디스어셈블리 명령 행들 (10개 라인: 오프셋 0, 2, 3, 5, 6 / 7, 8, 9 / 10, 11)
MX, MW = 348, 584
ROWS = [
    # (offset, hex_first, asm, note, c)
    ("0:", "18 (LD_IMM64)", "r6 = 0 ll", "전역 변수 counter 맵 자리 (2슬롯)", INFO),
    ("2:", "61 (LDX_MEM)", "r3 = *(u32 *)(r6 + 0)", "counter 값 읽기", INFO),
    ("3:", "18 (LD_IMM64)", "r1 = 0 ll", "형식 문자열 맵 자리 (2슬롯)", INFO),
    ("5:", "b7 (ALU64|MOV)", "r2 = 15", "형식 문자열 14B + NUL 1B", INFO),
    ("6:", "85 (CALL)", "call 6", "헬퍼 bpf_trace_printk 호출", INFO),
    ("7:", "61 (LDX_MEM)", "r1 = *(u32 *)(r6 + 0)", "counter 값 다시 읽기", WARN),
    ("8:", "07 (ALU64|ADD)", "r1 += 1", "카운터 1 증가", WARN),
    ("9:", "63 (STX_MEM)", "*(u32 *)(r6 + 0) = r1", "증가된 값 메모리 저장", WARN),
    ("10:", "b7 (ALU64|MOV)", "r0 = 2", "XDP_PASS 반환값", OK),
    ("11:", "95 (EXIT)", "exit", "프로그램 실행 종료", OK),
]

RY0 = 110
R_STRIDE = 33

for i, (off, op, asm, desc, c) in enumerate(ROWS):
    ry = RY0 + i * R_STRIDE
    d.box(MX, ry, MW, 28, PAPER2, RULE, 0.8, 4)
    d.t(MX + 10, ry + 18, off, 11, SOFT, MONO, "start")
    d.t(MX + 44, ry + 18, op, 11, c, MONO, "start", 600)
    d.t(MX + 190, ry + 18, asm, 11, INK, MONO, "start")
    d.t(MX + MW - 12, ry + 18, desc, 12, MUTED, KR, "end")

# 소스 블록 -> 디스어셈블리 연결 화살표
d.arrow([(SX + SW + 2, 110 + 80), (MX - 4, 110 + 80)], INFO, "info", 1.4)
d.arrow([(SX + SW + 2, 274 + 48), (MX - 4, 274 + 48)], WARN, "warn", 1.4)
d.arrow([(SX + SW + 2, 374 + 30), (MX - 4, 374 + 30)], OK, "ok", 1.4)

d.legend(H - 46, [
    ("bpf_printk · 5명령 7슬롯", INFO),
    ("counter++ · 3명령 3슬롯", WARN),
    ("return · 2명령 2슬롯", OK),
])

d.save("03-01.bytecode-disassembly.svg")
