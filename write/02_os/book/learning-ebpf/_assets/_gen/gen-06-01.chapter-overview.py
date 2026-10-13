# 타입 스펙: type-process — 주체 없는 단계 지도. 다섯 단계가 칸마다 같은 자리(단계명 · 실제 값 · 절)에 반복되고 마지막 단계만 통과/거부 둘로 갈린다.
# 사실 출처: 추출본 src/ebpf6.txt 139~140행(processed 61 insns … mark_read 3), 113~259행(로그 출력·마지막 줄이 이유),
#   예제 chapter6/hello-verifier.bpf.c(오브젝트 이름·SEC), 커널 v7.2 kernel/bpf/verifier.c 17367행(too large), 18611행(통계 줄).
# 축약: semantic-patterns 「Stage framework with semantic slots」 — 주체 없이 단계·값·절 슬롯만 반복한다.
# Layout conventions: 행 stride 64, 행 높이 48, 단계명 열 x=24 w=176, 값 열 x=216 w=552, 절 열 x=784 w=152. 모든 좌표 4의 배수.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, MUTED, INK, PAPER2, RULE, KR, MONO

W = 960
Y0, STRIDE, RH = 108, 64, 48
rows = [
    ("1 · 입력", "hello-verifier.bpf.o", MONO, "§1", INFO),
    ("2 · 적재 요청", "bpf(BPF_PROG_LOAD)", MONO, "§2", INFO),
    ("3 · 경로 탐색", "bpf_reg_state R0~R10 · push · pop · 가지치기", MONO, "§1", ACC),
    ("4 · 로그 출력", "kernel_log_buf · libbpf_set_print()", MONO, "§2", INFO),
]
LEG_Y = Y0 + 5 * STRIDE + 8
H = LEG_Y + 56

d = D(W, H, "LEARNING EBPF · 06-01",
      "오브젝트 하나가 적재되거나 거부되기까지의 다섯 단계",
      "판정은 실행이 아니라 경로 탐색에서 나온다. 마지막 줄 하나가 통과와 거부를 가른다.",
      "단계마다 같은 칸: 단계명 · 실제 값 · 이 노트의 절")


def row(i, name, val, fam, sec, c):
    y = Y0 + i * STRIDE
    if c == ACC:
        d.tone(24, y, 176, RH, ACC, 6, "18", 1.4)
        d.tone(216, y, 552, RH, ACC, 6, "12", 1.4)
    else:
        d.box(24, y, 176, RH, PAPER2, RULE, 0.9, 6)
        d.box(216, y, 552, RH, PAPER2, RULE, 0.9, 6)
    d.t(36, y + 30, name, 13, ACC if c == ACC else INK, KR, "start", 600)
    d.t(232, y + 30, val, 13, INK, fam, "start")
    d.chip(860, y + 24, sec, MUTED, 12)
    if i < 4:
        d.arrow([(112, y + RH), (112, y + STRIDE)], MUTED, "ar", 1.4)


for i, (n, v, f, s, c) in enumerate(rows):
    row(i, n, v, f, s, c)

# 판정 행 — 통과와 거부 둘
y = Y0 + 4 * STRIDE
d.box(24, y, 176, RH, PAPER2, RULE, 0.9, 6)
d.t(36, y + 30, "5 · 판정", 13, INK, KR, "start", 600)
d.tone(216, y, 268, RH, OK, 6, "12", 1.2)
d.t(228, y + 22, "processed 61 insns", 12, OK, MONO, "start", 600)
d.t(228, y + 40, "(limit 1000000) → 적재", 13, OK, MONO, "start")
d.tone(500, y, 268, RH, BAD, 6, "12", 1.2)
d.t(512, y + 22, "로그 마지막 줄", 12, BAD, KR, "start", 600)
d.t(512, y + 40, "= 거부 이유 → 거부", 13, BAD, KR, "start")
d.chip(860, y + 24, "§2", MUTED, 12)

d.legend(LEG_Y, [("단계", INFO), ("경로 탐색", ACC), ("통과", OK), ("거부", BAD)])
d.save("06-01.chapter-overview.svg")
