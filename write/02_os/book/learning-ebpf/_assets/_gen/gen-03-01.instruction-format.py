# 타입 스펙: type-nested — 64비트 bpf_insn 구조체의 비트 분할과 16바이트 와이드 즉시값 명령 구조
# 사실 출처: v7.2 include/uapi/linux/bpf.h L80~86, RFC 9669 §3, 본문 §1
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 480
d = D(W, H, "LEARNING EBPF · 03-01 §1",
      "eBPF 명령어 구조와 16바이트 와이드 즉시값 인코딩",
      "기본 bpf_insn 은 64비트 5개 필드로 구성되며 64비트 상수는 16바이트 와이드 명령을 씁니다",
      "opcode 8비트 · 레지스터 4비트 쌍 · 오프셋 16비트 · 즉시값 32비트")

# 좌측: struct bpf_insn 기본 64비트 상자
LX, LY, LW, LH = 36, 110, 468, 290
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0, 8)
d.t(LX + 16, LY + 24, "struct bpf_insn (64비트 / 8바이트)", 12, INK, MONO, "start", 600)
d.t(LX + LW - 16, LY + 24, "기본 단일 슬롯", 11, SOFT, KR, "end")

# 비트 슬롯들 (code: 8, dst: 4, src: 4, off: 16, imm: 32)
FX = LX + 16
FY = LY + 44
FIELDS = [
    ("code", "8-bit", 64, ACC),
    ("dst", "4-bit", 44, OK),
    ("src", "4-bit", 44, INFO),
    ("off", "16-bit", 84, WARN),
    ("imm", "32-bit", 200, INFO),
]

cur_x = FX
for name, bits, fw, c in FIELDS:
    d.tone(cur_x, FY, fw, 56, c, 4, "15", 1.0)
    d.t(cur_x + fw//2, FY + 24, name, 12, c, MONO, "middle", 600)
    d.t(cur_x + fw//2, FY + 44, bits, 11, MUTED, MONO, "middle")
    cur_x += fw

# 실제 명령 대응: b7 02 00 00 0f 00 00 00 (r2 = 15)
EY = LY + 120
d.t(LX + 16, EY, "실제 명령 바이트 대응: b7 02 00 00 0f 00 00 00", 11, MUTED, MONO, "start")

BYTES = [
    ("0xb7", "ALU64|MOV", 64, ACC),
    ("0x2", "r2", 44, OK),
    ("0x0", "-", 44, INFO),
    ("0x0000", "0", 84, WARN),
    ("0x0000000f", "15", 200, INFO),
]

cur_x = FX
for hexval, mean, fw, c in BYTES:
    d.box(cur_x, EY + 12, fw, 52, PAPER, RULE, 0.9, 4)
    d.t(cur_x + fw//2, EY + 32, hexval, 11, INK, MONO, "middle", 600)
    d.t(cur_x + fw//2, EY + 50, mean, 11, c, KR, "middle")
    cur_x += fw

# 결과 해석
d.box(FX, LY + 210, LW - 32, 48, PAPER, OK, 1.0, 6)
d.t(FX + 16, LY + 238, "해석: r2 = 15", 13, OK, MONO, "start", 600)
d.t(FX + LW - 48, LY + 238, "dst = imm (즉시값 15를 레지스터 r2 에 대입)", 11, MUTED, KR, "end")


# 우측: 와이드 16바이트 명령 (두 슬롯)
RX, RY, RW, RH = 524, 110, 360, 290
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.0, 8)
d.t(RX + 16, RY + 24, "와이드 명령 (16바이트 / 2슬롯)", 12, INK, MONO, "start", 600)
d.t(RX + RW - 16, RY + 24, "64비트 즉시값 적재", 11, WARN, KR, "end")

# 슬롯 1
S1_Y = RY + 44
d.tone(RX + 16, S1_Y, RW - 32, 60, ACC, 6, "10", 1.0)
d.t(RX + 28, S1_Y + 22, "슬롯 1 (8B)", 11, SOFT, KR, "start")
d.t(RX + RW - 28, S1_Y + 22, "18 06 00 00 00 00 00 00", 11, MUTED, MONO, "end")
d.t(RX + 28, S1_Y + 44, "code=0x18 (LD|IMM|DW) · dst=r6 · imm_lo=0", 11, INK, MONO, "start")

# 슬롯 2
S2_Y = RY + 116
d.tone(RX + 16, S2_Y, RW - 32, 60, INFO, 6, "10", 1.0)
d.t(RX + 28, S2_Y + 22, "슬롯 2 (8B 의사 명령)", 11, SOFT, KR, "start")
d.t(RX + RW - 28, S2_Y + 22, "00 00 00 00 00 00 00 00", 11, MUTED, MONO, "end")
d.t(RX + 28, S2_Y + 44, "code=0x0 · dst=0 · off=0 · imm_hi=0", 11, INK, MONO, "start")

# 와이드 명령 결과
d.box(RX + 16, RY + 210, RW - 32, 48, PAPER, WARN, 1.0, 6)
d.t(RX + 28, RY + 238, "해석: r6 = 0 ll", 13, WARN, MONO, "start", 600)
d.t(RX + RW - 28, RY + 238, "64비트 전체 즉시값 적재", 11, MUTED, KR, "end")

d.legend(H - 46, [
    ("명령어 opcode", ACC),
    ("목적지 dst", OK),
    ("출처 src", INFO),
    ("오프셋 off", WARN),
])

d.save("03-01.instruction-format.svg")
