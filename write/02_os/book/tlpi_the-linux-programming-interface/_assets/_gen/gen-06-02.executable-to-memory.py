# 06-02 §1 실행 파일에서 프로세스 메모리로 — BSS 는 파일에 크기만 남고 적재할 때 0 으로 채워진다
# 근거: TLPI 6.3 uninitialized data segment 설명, 연습 6-1(mem_segments.c 의 실행 파일 크기)
# 값 근거: 노트 §1 의 size·ls -l 출력(Debian 13, GCC 14.2, x86-64, 2026-11-11 실측). ms 는 text 1720·data 620·bss 10305568·파일 16280, mi 는 text 1720·data 10240648·bss 65568·파일 10256296.
# 타입 스펙: type-data-flow — 실행 파일의 세그먼트가 로더를 거쳐 프로세스 메모리의 세그먼트로 바뀌는 흐름을 두 실행 파일로 맞댄다
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 500
CW, CH, GAP = 136, 84, 8
LX = [24, 24 + CW + GAP, 24 + 2 * (CW + GAP)]
RX = [528, 528 + CW + GAP, 528 + 2 * (CW + GAP)]
d = D(W, H, "TLPI · 06-02 §1",
      "BSS 는 파일에 크기만 남는다",
      "mem_segments.c 를 컴파일한 실행 파일 ms 와, mbuf 에 초기값을 붙인 mi 가 디스크에서 메모리로 올라가는 과정. 값은 size 와 ls -l 출력이다.",
      "초기값이 없는 mbuf 는 BSS 로 가서 파일이 16,280 바이트이고, 초기값이 붙으면 data 로 옮겨 가 파일이 10,256,296 바이트가 됩니다.")


def cell(x, y, name, size, note, c=None):
    if c:
        d.tone(x, y, CW, CH, c, 6, "1A", 1.2)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, y + 26, name, 13, c or INK, MONO, "middle", 600)
    d.t(x + CW / 2, y + 48, size, 13, INK, MONO if size[0].isdigit() else KR, "middle")
    d.t(x + CW / 2, y + 69, note, 12, MUTED, KR, "middle")


d.t(LX[0], 108, "실행 파일 (디스크)", 13, MUTED, KR, "start", 600)
d.t(RX[0], 108, "프로세스 메모리 (적재 뒤)", 13, MUTED, KR, "start", 600)

rows = [
    ("ms · mbuf 에 초기값 없음", 124, "파일 16,280 B", OK,
     [("text", "1,720 B", "파일에 저장", None), ("data", "620 B", "파일에 저장", None), ("bss", "크기만 기록", "바이트 없음", OK)],
     [("text", "1,720 B", "적재", None), ("data", "620 B", "파일에서 읽음", None), ("bss", "10,305,568 B", "0 으로 채움", OK)]),
    ("mi · mbuf 에 = { 1 }", 292, "파일 10,256,296 B", WARN,
     [("text", "1,720 B", "파일에 저장", None), ("data", "10,240,648 B", "초기값이 파일에 듦", WARN), ("bss", "크기만 기록", "바이트 없음", OK)],
     [("text", "1,720 B", "적재", None), ("data", "10,240,648 B", "파일에서 읽음", WARN), ("bss", "65,568 B", "0 으로 채움", OK)]),
]
for title, ty, chip, cc, left, right in rows:
    d.t(LX[0], ty + 14, title, 14, INK, KR, "start", 600)
    cy = ty + 28
    for i, (n, s, nt, c) in enumerate(left):
        cell(LX[i], cy, n, s, nt, c)
    for i, (n, s, nt, c) in enumerate(right):
        cell(RX[i], cy, n, s, nt, c)
    my = cy + CH / 2
    d.arrow([(LX[2] + CW + 4, my), (RX[0] - 6, my)], SOFT, "soft", 1.4)
    d.t((LX[2] + CW + RX[0]) / 2, my - 10, "로더 적재", 12, MUTED, KR, "middle", 600)
    d.chip(LX[0] + 100, cy + CH + 22, chip, cc, 13, 8)

d.legend(H - 40, [("크기만 기록하는 BSS", OK), ("파일을 키우는 데이터", WARN)])
d.save("06-02.executable-to-memory.svg")
print("ok 06-02.executable-to-memory.svg")
