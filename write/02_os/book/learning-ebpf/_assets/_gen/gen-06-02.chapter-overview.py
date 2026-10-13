# 타입 스펙: type-flowchart — 세 줄의 판정 흐름(헬퍼 호출 · 메모리 접근 · 루프·종료). 줄마다 검사 칸이 이어지고 칸 아래로 거부 메시지가 갈라지며 끝은 통과 하나.
# 사실 출처: 06-02 본문 §1(cannot use helper · GPL-restricted · type=fp expected=map_ptr), §2(value_size=16 off=16 size=1 · map_value_or_null · invalid bpf_context access),
#   §3(i < c 가 1,000,000 한도에 닿음 · R0 !read_ok · unreachable insn). 커널 v7.2 verifier.c 10194·10200·3110행, cfg.c 626행(본문 링크).
# Layout conventions: 입력 x=24 w=152, 검사 칸 x=216·424·632 w=176 h=48, 통과 x=840 w=96, 거부 칸은 검사 칸 아래 20px 간격 h=48. 모든 좌표 4의 배수.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, MUTED, INK, PAPER2, RULE, KR, MONO

W = 960
Y0, STRIDE, CH, RJ = 108, 144, 48, 48
XS = [216, 424, 632]
CW = 176
LEG_Y = Y0 + 3 * STRIDE + 4
H = LEG_Y + 56

d = D(W, H, "LEARNING EBPF · 06-02",
      "헬퍼 호출 · 메모리 접근 · 루프가 통과하기까지의 검사",
      "검사 칸마다 한 가지가 거부되며, 모든 칸을 지난 호출만 통과한다.",
      "줄 = 증명할 대상 · 칸 = 검사 · 아래 = 거부 메시지")

rows = [
    ("헬퍼 호출", "§1",
     [("유형 허용?", ["cannot use helper"]),
      ("gpl_only?", ["GPL-restricted"]),
      ("arg1_type?", ["expected=map_ptr"])]),
    ("메모리 접근", "§2",
     [("범위 증명?", ["value_size=16", "off=16 size=1"]),
      ("null 검사?", ["map_value_or_null"]),
      ("컨텍스트 필드?", ["invalid bpf_context", "access"])]),
    ("루프 · 종료", "§3",
     [("상한 있음?", ["i < c → 1,000,000"]),
      ("R0 초기화?", ["R0 !read_ok"]),
      ("도달 가능?", ["unreachable insn"])]),
]

for i, (name, sec, checks) in enumerate(rows):
    y = Y0 + i * STRIDE
    d.tone(24, y, 152, CH, ACC, 6, "18", 1.4)
    d.t(100, y + 30, name, 13, ACC, KR, "middle", 600)
    d.chip(100, y + CH + 20, sec, MUTED, 12)
    prev = 176
    for j, (q, msgs) in enumerate(checks):
        x = XS[j]
        d.box(x, y, CW, CH, PAPER2, RULE, 0.9, 6)
        d.t(x + CW / 2, y + 30, q, 13, INK, MONO if q.startswith("gpl") or q.startswith("arg1") or q.startswith("R0") else KR, "middle", 600)
        d.arrow([(prev, y + CH / 2), (x, y + CH / 2)], MUTED, "ar", 1.4)
        d.arrow([(x + CW / 2, y + CH), (x + CW / 2, y + CH + 20)], BAD, "ar", 1.2)
        d.tone(x, y + CH + 20, CW, RJ, BAD, 6, "12", 1.1)
        if len(msgs) == 1:
            d.t(x + CW / 2, y + CH + 20 + 30, msgs[0], 12, BAD, MONO, "middle")
        else:
            d.t(x + CW / 2, y + CH + 20 + 22, msgs[0], 12, BAD, MONO, "middle")
            d.t(x + CW / 2, y + CH + 20 + 40, msgs[1], 12, BAD, MONO, "middle")
        prev = x + CW
    d.arrow([(prev, y + CH / 2), (840, y + CH / 2)], MUTED, "ar", 1.4)
    d.tone(840, y, 96, CH, OK, 6, "14", 1.2)
    d.t(888, y + 30, "통과", 13, OK, KR, "middle", 600)

d.legend(LEG_Y, [("증명할 대상", ACC), ("거부", BAD), ("통과", OK)])
d.save("06-02.chapter-overview.svg")
