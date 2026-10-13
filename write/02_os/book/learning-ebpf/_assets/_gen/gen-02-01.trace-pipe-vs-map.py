# 타입 스펙: type-data-flow — 위 절반은 프로그램 둘이 trace_pipe 하나로 섞이는 길, 아래 절반은 프로그램마다 맵이 따로인 길.
# 사실 출처: 추출본 src/ebpf2.txt 224~243행(단일 trace_pipe·문자열만·섞임)·249~254행(맵은 사용자 공간과 공유),
#   커널 v7.2 include/uapi/linux/bpf.h 2021~2032행(`/sys/kernel/tracing/trace_pipe`), kernel/trace/bpf_trace.c 392~409행(trace_bpf_trace_printk).
# Layout conventions: 열 x 는 40·340·660, 행 높이 60, 행 stride 80, 절반 구분선 y=300.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 580
d = D(W, H, "LEARNING EBPF · 02-01 §2", "trace_pipe 는 하나라 줄이 섞이고 맵은 프로그램마다 따로 만든다",
      "위쪽은 프로그램 A 와 B 가 bpf_trace_printk 로 같은 trace_pipe 에 쓴 문자열이 한 흐름으로 섞이는 모습이다. 아래쪽은 같은 두 프로그램이 각자 만든 맵에 쓰고 사용자 공간이 필요한 맵만 골라 읽는 모습이다.",
      "같은 두 프로그램이라도 통로가 다르면 읽는 쪽이 다릅니다")

def node(x, y, w, h, title, sub, c=None, fam=MONO, size=14):
    if c: d.tone(x, y, w, h, c, 6, "14", 1.3)
    else: d.box(x, y, w, h, PAPER2, RULE, 1.0)
    d.t(x + w/2, y + 26, title, size, c or INK, fam, "middle", 600)
    if sub: d.t(x + w/2, y + 46, sub, 11, MUTED, MONO if sub.isascii() else KR)

d.t(40, 116, "trace_pipe 하나", 13, WARN, KR, "start", 600)
d.arrow([(256, 162), (298, 162), (298, 192), (336, 192)], WARN, "warn", 1.5)
d.arrow([(256, 242), (298, 242), (298, 212), (336, 212)], WARN, "warn", 1.5)
d.arrow([(580, 202), (656, 202)], WARN, "warn", 1.5)
node(40, 132, 216, 60, "프로그램 A", "bpf_trace_printk()")
node(40, 212, 216, 60, "프로그램 B", "bpf_trace_printk()")
node(340, 172, 240, 60, "trace_pipe", "/sys/kernel/tracing/trace_pipe", WARN)
d.box(660, 132, 232, 140, PAPER2, WARN, 1.2)
d.t(776, 158, "섞인 문자열 줄", 13, WARN, KR, "middle", 600)
d.t(676, 196, "A", 12, MUTED, MONO, "start", 600)
d.t(700, 196, "bash-5412 … Hello W", 11, INK, MONO, "start")
d.t(676, 236, "B", 12, MUTED, MONO, "start", 600)
d.t(700, 236, "… B 가 쓴 문자열", 11, INK, KR, "start")

d.line(24, 300, W - 24, 300, RULE, 1.0)
d.t(40, 332, "프로그램마다 만든 맵", 13, OK, KR, "start", 600)
for i, (p, m, r) in enumerate((("A", "counter_table", "A 맵의 값"), ("B", "B 의 맵", "B 맵의 값"))):
    y = 352 + i * 80
    d.arrow([(256, y + 30), (336, y + 30)], OK, "ok", 1.5)
    d.arrow([(580, y + 30), (656, y + 30)], OK, "ok", 1.5)
    node(40, y, 216, 60, f"프로그램 {p}", "update()")
    node(340, y, 240, 60, m, "프로그램이 만든 맵", OK, MONO if m.isascii() else KR)
    node(660, y, 232, 60, r, "골라서 읽는다", None, KR)

d.legend(H - 56, [("trace_pipe 길", WARN), ("맵 길", OK)])
d.save("02-01.trace-pipe-vs-map.svg")
