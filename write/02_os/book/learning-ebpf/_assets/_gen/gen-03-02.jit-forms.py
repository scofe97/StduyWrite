# 타입 스펙: type-process — counter++ 한 줄이 오브젝트 바이트·xlated·JIT 출력 세 단계를 지나며 모양이 바뀌는 과정
# 사실 출처: 추출본 ebpf3.txt 600~667행(JIT 덤프 0x60~0x70 줄), 03-01 노트 §3·§4 의 슬롯 7·8·9 와 xlated 7~9번,
#   bpftool prog show 의 xlated 96B · jited 148B(03-01 §4 출력 · 추출본 ebpf3.txt 파생 값),
#   arm64 JIT 는 명령 37개 × 4B = 148B(덤프 오프셋 0x00~0x90).
# Layout conventions(type-process): 단계 3 · 단계 폭 216 · 단계 간격 80 · 행 3 · stride 52. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 448
d = D(W, H, "LEARNING EBPF · 03-02 §1",
      "같은 counter++ 가 세 번 모양을 바꾼다",
      "오브젝트 파일의 8바이트 슬롯이 적재되어 xlated 명령이 되고, JIT 가 arm64 명령 세 줄로 옮긴다.",
      "슬롯 7·8·9 의 읽기 · 더하기 · 쓰기")

SX = [96, 392, 688]
SW = 216
STAGES = [
    ("컴파일 직후", "오브젝트 파일", INFO,
     ["61 61 00 00 00 00 00 00", "07 01 00 00 01 00 00 00", "63 16 00 00 00 00 00 00"]),
    ("검증 뒤 xlated", "bpftool prog dump xlated", WARN,
     ["(61) r1 = *(u32 *)(r6 +0)", "(07) r1 += 1", "(63) *(u32 *)(r6 +0) = r1"]),
    ("JIT 결과 arm64", "bpftool prog dump jited", ACC,
     ["ldr w0, [x19, x10]", "add x0, x0, #1", "str w0, [x19, x10]"]),
]
ROW_LABEL = ["읽기", "더하기", "쓰기"]

TOP = 104
HH = 232
for x, (title, sub, c, rows) in zip(SX, STAGES):
    d.tone(x, TOP, SW, HH, c, 6, "12", 1.4 if c == ACC else 1.2)
    d.t(x + SW / 2, TOP + 28, title, 14, c, KR, "middle", 600)
    d.t(x + SW / 2, TOP + 48, sub, 12, MUTED, MONO if sub.isascii() else KR)
    for i, r in enumerate(rows):
        y = TOP + 68 + i * 52
        d.box(x + 8, y, SW - 16, 40, PAPER, RULE, 0.9, 4)
        d.t(x + SW / 2, y + 25, r, 12, INK, MONO)

for i, lab in enumerate(ROW_LABEL):
    d.t(12, TOP + 68 + i * 52 + 25, lab, 12, MUTED, KR, "start")

yc = TOP + HH // 2
d.arrow([(SX[0] + SW + 4, yc), (SX[1] - 8, yc)], MUTED, "ar", 1.5)
d.chip((SX[0] + SW + SX[1]) / 2, yc - 20, "적재", MUTED, 12)
d.arrow([(SX[1] + SW + 4, yc), (SX[2] - 8, yc)], ACC, "acc", 1.6)
d.chip((SX[1] + SW + SX[2]) / 2, yc - 20, "JIT", ACC, 12)

d.t(SX[0] + SW / 2, TOP + HH + 32, "슬롯당 8 B", 12, MUTED, KR)
d.t(SX[1] + SW / 2, TOP + HH + 32, "12 슬롯 = 96 B", 12, WARN, KR)
d.t(SX[2] + SW / 2, TOP + HH + 32, "명령 37개 = 148 B", 12, ACC, KR)

d.legend(H - 56, [("컴파일 직후", INFO), ("xlated", WARN), ("JIT 결과", ACC)])
d.save("03-02.jit-forms.svg")
