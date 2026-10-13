# 타입 스펙: type-data-flow — C 소스 세 블록이 디스어셈블리 명령 바이트와 옵코드 해석으로 변환되는 흐름
# 사실 출처: llvm-objdump -S hello.bpf.o 출력, RFC 9669, 본문 §3
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 03-01 §3",
      "C 소스에서 바이트코드 오프셋과 디스어셈블리로의 변환",
      "Clang 이 생성한 12개 명령 슬롯이 소스코드 세 블록에 매핑되어 실행됩니다",
      "C 소스 줄 · 8바이트 슬롯 오프셋 · opcode 바이트 · 의사 명령 해석")

# 좌측 C 소스 3개 블록
SX, SW = 36, 260
BLOCKS = [
    ("bpf_printk()", "bpf_printk(\"...%d\", counter);", INFO, 110, 150),
    ("counter++", "counter++;", WARN, 274, 96),
    ("return", "return XDP_PASS;", OK, 384, 70),
]

for title, code, c, y, h in BLOCKS:
    d.tone(SX, y, SW, h, c, 6, "12", 1.2)
    d.t(SX + 14, y + 24, title, 13, c, MONO, "start", 600)
    d.t(SX + 14, y + 46, code, 11, INK, MONO, "start")

# 우측 디스어셈블리 명령 행들 (10개 라인: 오프셋 0, 2, 3, 5, 6 / 7, 8, 9 / 10, 11)
MX, MW = 340, 584
ROWS = [
    # (offset, hex_first, asm, note, block_idx)
    ("0:", "18 (LD_IMM64)", "r6 = 0 ll", "전역 변수 counter 맵 자리 (2슬롯)", 0, INFO),
    ("2:", "61 (LDX_MEM)", "r3 = *(u32 *)(r6 + 0)", "counter 값 역참조", 0, INFO),
    ("3:", "18 (LD_IMM64)", "r1 = 0 ll", "형식 문자열 맵 자리 (2슬롯)", 0, INFO),
    ("5:", "b7 (ALU64_MOV)", "r2 = 15", "문자열 길이 15 바이트", 0, ACC),
    ("6:", "85 (CALL)", "call 6", "헬퍼 bpf_trace_printk 호출", 0, OK),
    ("7:", "61 (LDX_MEM)", "r1 = *(u32 *)(r6 + 0)", "counter 값 다시 읽기", 1, WARN),
    ("8:", "07 (ALU64_ADD)", "r1 += 1", "카운터 1 증가", 1, WARN),
    ("9:", "63 (STX_MEM)", "*(u32 *)(r6 + 0) = r1", "증가된 값 메모리 저장", 1, WARN),
    ("10:", "b7 (ALU64_MOV)", "r0 = 2", "XDP_PASS 반환값", 2, OK),
    ("11:", "95 (EXIT)", "exit", "프로그램 실행 종료", 2, MUTED),
]

RY0 = 110
R_STRIDE = 33

for i, (off, op, asm, desc, bidx, c) in enumerate(ROWS):
    ry = RY0 + i * R_STRIDE
    d.box(MX, ry, MW, 28, PAPER2, RULE, 0.8, 4)
    d.t(MX + 10, ry + 18, off, 11, SOFT, MONO, "start")
    d.t(MX + 44, ry + 18, op, 11, c, MONO, "start", 600)
    d.t(MX + 200, ry + 18, asm, 11, INK, MONO, "start")
    d.t(MX + MW - 12, ry + 18, desc, 11, MUTED, KR, "end")

# 소스 블록 -> 디스어셈블리 연결 화살표
d.arrow([(SX + SW + 2, 110 + 75), (MX - 4, 110 + 75)], INFO, "info", 1.4)
d.arrow([(SX + SW + 2, 274 + 48), (MX - 4, 274 + 48)], WARN, "warn", 1.4)
d.arrow([(SX + SW + 2, 384 + 35), (MX - 4, 384 + 35)], OK, "ok", 1.4)

d.legend(H - 46, [
    ("출력 함수 호출 묶음", INFO),
    ("즉시값 대입 및 헬퍼", ACC),
    ("카운터 증가 묶음", WARN),
    ("반환 및 종료", OK),
])

d.save("03-01.bytecode-disassembly.svg")
