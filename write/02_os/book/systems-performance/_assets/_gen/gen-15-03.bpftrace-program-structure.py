# 15-03 §1 — 지연을 재는 프로그램은 늘 같은 모양이다.
# 타입 스펙: type-process — 시작 프로브에서 종료 프로브까지 상태가 이어지는 단계 지도.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 500
CW, CH, GAP, X0, Y = 280, 176, 32, 40, 140

d = DK(W, H, "SYSTEMS PERFORMANCE · 15-03 §1",
       "지연 측정은 늘 같은 모양이다",
       "시작에서 시각을 남기고, 끝에서 그 차이를 집계한다. 어느 계층을 재든 이 세 단계가 반복된다.",
       "@start[tid] 로 스레드마다 시각을 따로 들고 있는 것이 핵심입니다")

STEPS = [
    ("01", "시작 프로브", INFO, ["k:vfs_read { ", "  @start[tid] = nsecs;", "}"],
     "스레드별로 시각을 남깁니다"),
    ("02", "종료 프로브 · 필터", ACC, ["kr:vfs_read", "  /@start[tid]/ {", "  ...", "}"],
     "시작을 본 스레드만 통과"),
    ("03", "집계 · 정리", OK, ["@ns = hist(nsecs", "      - @start[tid]);", "delete(@start[tid]);"],
     "차이를 모으고 지웁니다"),
]
for i, (n, name, c, code, foot) in enumerate(STEPS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.o.append(f'<rect x="{x + 16}" y="{Y + 16}" width="22" height="18" rx="9" fill="{c}" stroke="{c}" stroke-width="1"/>')
    d.t(x + 27, Y + 29, n, 9, PAPER, MONO)
    d.t(x + 48, Y + 29, name, 14, c, KR, "start", 600)
    for j, l in enumerate(code):
        d.t(x + 16, Y + 58 + j * 18, l, 12, MUTED, MONO, "start")
    d.t(x + 16, Y + CH - 18, foot, 13, c, KR, "start")
    if i < 2:
        d.arrow([(x + CW, Y + CH / 2), (x + CW + GAP - 8, Y + CH / 2)], MUTED, "ar", 1.3)

YB = Y + CH + 44
d.t(X0, YB, "추적 시작 전부터 진행 중이던 I/O 는 끝만 보입니다 — 델타가 now - 0 이 되어 터무니없이 커집니다", 13, MUTED, KR, "start")
d.t(X0, YB + 24, "delete 를 빼면 맵이 계속 자라 커널 메모리를 먹습니다", 13, WARN, KR, "start")

d.legend(YB + 48, [("시작을 본 것만 거르는 자리", ACC), ("시각을 남기는 자리", INFO), ("모으는 자리", OK), ("빠뜨리기 쉬운 것", WARN)])
d.save("15-03.bpftrace-program-structure.svg")
