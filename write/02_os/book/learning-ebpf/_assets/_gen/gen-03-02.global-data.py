# 타입 스펙: type-data-flow — 행 둘(.bss · .rodata) × 열 셋(오브젝트 섹션 · 맵 · 명령). 값이 열마다 모양을 바꿔 명령에 이어진다.
# 사실 출처: 추출본 ebpf3.txt 793~911행(bpftool map list · map dump 의 "counter": 11127 · "hello.____fmt"),
#   03-01 §4 xlated 줄(r6 = map[id:165][0]+0 · r1 = map[id:166][0]+0 · r2 = 15),
#   v7.2 include/uapi/linux/bpf.h L1434(BPF_F_RDONLY_PROG 0x80) · L1441(BPF_F_MMAPABLE 0x400).
# Layout formulas(type-data-flow §2) 변형: 레인 2 · lane_h 152 · node 216×104 · 열 간격 44.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 496
d = D(W, H, "LEARNING EBPF · 03-02 §3",
      "전역 변수와 문자열은 두 배열 맵에 산다",
      "counter 는 맵 165 의 값 4B 로, 형식 문자열은 맵 166 의 값 15B 로 적재되고 명령이 맵을 가리켜 읽고 쓴다.",
      "hello.bpf.o 의 두 섹션이 맵 두 개와 명령 둘로 이어집니다")

NX = [140, 400, 660]
NW, NH = 216, 104
HEAD = ["오브젝트 섹션", "맵", "명령"]
for i, x in enumerate(NX):
    d.box(x + NW / 2 - 56, 96, 112, 20, PAPER2, RULE, 0.9, 10)
    d.t(x + NW / 2, 110, HEAD[i], 12, MUTED, KR, "middle", 600)

LANES = [
    (128, ".bss", "전역 변수", [
        (INFO, ".bss", ["counter", "", ""]),
        (ACC, "165 hello.bss", ["value 4 B", "counter 11127", "flags 0x400"]),
        (OK, "r6 = map[id:165][0]+0", ["*(u32 *)(r6 +0)", "counter 읽기 · 쓰기", ""]),
    ]),
    (280, ".rodata", "문자열 상수", [
        (INFO, ".rodata", ['"Hello World %d"', "", ""]),
        (WARN, "166 hello.rodata", ["value 15 B", "hello.____fmt", "flags 0x80 · frozen"]),
        (OK, "r1 = map[id:166][0]+0", ["r2 = 15", "헬퍼 인자", ""]),
    ]),
]
for top, name, sub, nodes in LANES:
    for x, (c, title, lines) in zip(NX, nodes):
        y = top + 24
        d.tone(x, y, NW, NH, c, 6, "12", 1.4 if c == ACC else 1.2)
        d.t(x + NW / 2, y + 26, title, 13, c, MONO, "middle", 600)
        ly = y + 48
        for ln in lines:
            if not ln:
                continue
            kr = any("가" <= ch <= "힣" for ch in ln)
            d.t(x + NW / 2, ly, ln, 12, MUTED, KR if kr else MONO)
            ly += 18
    yc = top + 24 + NH // 2
    d.arrow([(NX[0] + NW + 4, yc), (NX[1] - 8, yc)], MUTED, "ar", 1.5)
    d.arrow([(NX[1] + NW + 4, yc), (NX[2] - 8, yc)], MUTED, "ar", 1.5)

d.legend(H - 56, [("오브젝트 섹션", INFO), ("카운터가 사는 맵", ACC), ("문자열이 사는 맵", WARN), ("맵을 가리키는 명령", OK)])
d.save("03-02.global-data.svg")
