# 10-04 §4 — 어느 층에 프로브를 걸 것인가. 층마다 얻는 것과 잃는 것이 다르다.
# 타입 스펙: type-layers — 애플리케이션에서 드라이버까지 추적 지점이 내려가는 층 지도다.
#           축약: OSI 층이 아니라 추적 지점이라 인덱스 태그를 층 이름으로 쓰지 않고 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 552
BX, BW, BH, Y0, STRIDE = 132, 700, 60, 116, 68

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-04 §4",
       "어느 층에 프로브를 걸 것인가",
       "층마다 이벤트 소스가 다르고, 프로세스를 짚을 수 있는 정도도 다르다. 소켓 층은 책임 프로세스가 아직 on-CPU 라 누가 했는지가 분명하다.",
       "가능하면 tracepoint 를 씁니다 — kprobe 는 커널 버전에 따라 함수명이 바뀝니다")

BANDS = [
    ("01", "애플리케이션 프로토콜", "uprobes", "누가 했는지 분명", None),
    ("02", "소켓", "syscall tracepoint", "책임 프로세스가 on-CPU", ACC),
    ("03", "TCP", "tcp tracepoint · kprobe", "프로토콜 내부가 보임", None),
    ("04", "UDP · IP", "kprobe", "프로세스 식별이 약함", None),
    ("05", "패킷 · qdisc · 드라이버", "skb · net tracepoint", "소켓 없는 이벤트도 보임", None),
]

for i, (n, name, src, note, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 36, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 46, src, 13, MUTED, MONO, "start")
    d.t(BX + BW - 20, y + 36, note, 13, c if c else SOFT, KR, "end")

d.t(BX - 100, Y0 + 4, "프로세스", 13, SOFT, KR, "start")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 4 * STRIDE + BH - 28)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 108, Y0 + 4 * STRIDE + BH - 4, "프로토콜", 13, SOFT, KR, "start")

YB = Y0 + 5 * STRIDE + 20
d.t(BX - 108, YB, "깊은 kprobe 는 프로세스 엔드포인트가 on-CPU 가 아닐 수 있어 pid·comm 이 무관할 수 있습니다",
    13, MUTED, KR, "start")

d.legend(YB + 28, [("누가 했는지가 분명한 층", ACC), ("나머지 층", MUTED)])
d.save("10-04.bpftrace-layers.svg")
