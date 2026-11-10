# 08-02 §7 — 추적이 어디에 훅을 걸고 어떤 도구가 그것을 읽는가.
# 원문("Tracing and Profiling"): "in the context of Linux, on a single machine, tracing means capturing
#       the process execution (function calls in user space, syscalls, etc.) over time."
#       소스는 The Linux kernel("Traces can come from functions in the kernel or be triggered by syscalls.
#       Examples include kernel probes (kprobes) or kernel tracepoints.") 와
#       User space("Application function calls, for example via user space probes (uprobes), can act as
#       a source for traces.") 다.
#       용도는 "Debugging a program using, for example, the strace tracing tool" 과
#       "Performance analysis with a frontend, using perf" 다.
#       경고는 "You may be tempted to use strace everywhere; however, you should be aware of the overhead
#       it causes. This is particularly relevant for production environments."
#       전망은 "it seems that eBPF ... will become the de facto standard to implement tracing, especially
#       for custom cases. It has a rich ecosystem and growing vendor support."
# 타입 스펙: type-architecture — 구성요소와 그 연결. 유저 공간과 커널이라는 두 구역에 훅 지점을 놓고
#           도구가 어느 지점을 읽는지 잇는다. 축약: 프로파일링 도구 목록은 본문 산문이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 524
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §7",
      "추적은 유저 공간과 커널 양쪽에 훅을 건다",
      "추적 소스 둘을 유저 공간과 커널 경계 위에 놓고, 그 훅을 읽는 도구를 오른쪽에 붙인 것.",
      "추적의 구현은 eBPF 쪽으로 모이고 있습니다")

ZX, ZW = 24, 520
UY, UH = 116, 132
KY, KH = 276, 176
d.o.append(f'<rect x="{ZX}" y="{UY}" width="{ZW}" height="{UH}" rx="8" fill="{INFO}0A" '
           f'stroke="{INFO}" stroke-width="1.1" stroke-dasharray="5 4"/>')
d.t(ZX + 16, UY + 22, "유저 공간", 11, INFO, KR, "start", 600)
d.o.append(f'<rect x="{ZX}" y="{KY}" width="{ZW}" height="{KH}" rx="8" fill="{WARN}0A" '
           f'stroke="{WARN}" stroke-width="1.1" stroke-dasharray="5 4"/>')
d.t(ZX + 16, KY + 22, "커널", 11, WARN, KR, "start", 600)

d.box(ZX + 24, UY + 36, 216, 72, PAPER2, RULE, 1.1, 6)
d.t(ZX + 40, UY + 62, "애플리케이션 함수 호출", 13, INK, KR, "start", 600)
d.t(ZX + 40, UY + 84, "내 코드의 함수", 11, MUTED, KR, "start")
d.box(ZX + 272, UY + 36, 216, 72, PAPER2, INFO, 1.2, 6)
d.t(ZX + 288, UY + 62, "uprobes", 13, INFO, MONO, "start", 600)
d.t(ZX + 288, UY + 84, "유저 공간 프로브", 11, MUTED, KR, "start")
d.arrow([(ZX + 240, UY + 72), (ZX + 268, UY + 72)], INFO, "info", 1.2)

d.box(ZX + 24, KY + 36, 216, 60, PAPER2, RULE, 1.1, 6)
d.t(ZX + 40, KY + 60, "커널 함수", 13, INK, KR, "start", 600)
d.t(ZX + 40, KY + 80, "커널 안의 함수", 11, MUTED, KR, "start")
d.box(ZX + 24, KY + 106, 216, 60, PAPER2, RULE, 1.1, 6)
d.t(ZX + 40, KY + 130, "시스템 콜", 13, INK, KR, "start", 600)
d.t(ZX + 40, KY + 150, "유저 → 커널 경계", 11, MUTED, KR, "start")
d.box(ZX + 272, KY + 36, 216, 60, PAPER2, WARN, 1.2, 6)
d.t(ZX + 288, KY + 60, "kprobes", 13, WARN, MONO, "start", 600)
d.t(ZX + 288, KY + 80, "커널 프로브", 11, MUTED, KR, "start")
d.box(ZX + 272, KY + 106, 216, 60, PAPER2, WARN, 1.2, 6)
d.t(ZX + 288, KY + 130, "tracepoints", 13, WARN, MONO, "start", 600)
d.t(ZX + 288, KY + 150, "커널에 미리 심은 지점", 11, MUTED, KR, "start")
d.arrow([(ZX + 240, KY + 66), (ZX + 268, KY + 66)], WARN, "warn", 1.2)
d.arrow([(ZX + 240, KY + 136), (ZX + 268, KY + 136)], WARN, "warn", 1.2)

TX, TW = ZX + ZW + 20, W - (ZX + ZW + 20) - 24
d.box(TX, UY, TW, 132, PAPER, RULE, 1.1, 8)
d.t(TX + 16, UY + 26, "읽는 도구", 12.5, INK, KR, "start", 600)
d.t(TX + 16, UY + 52, "strace", 13, MUTED, MONO, "start", 600)
d.t(TX + 16, UY + 70, "프로그램 디버깅", 11, MUTED, KR, "start")
d.t(TX + 16, UY + 96, "perf", 13, OK, MONO, "start", 600)
d.t(TX + 16, UY + 114, "성능 분석 프론트엔드", 11, MUTED, KR, "start")

d.tone(TX, KY, TW, 176, ACC, 8, "12", 1.4)
d.t(TX + 16, KY + 28, "eBPF", 15, ACC, MONO, "start", 600)
for j, (k, v) in enumerate([("훅", "uprobes · kprobes"), ("", "tracepoints"),
                             ("프로파일러", "parca")]):
    if k:
        d.t(TX + 16, KY + 58 + j * 26, k, 11, SOFT, KR, "start")
    d.t(TX + 92, KY + 58 + j * 26, v, 11.5, MUTED, MONO, "start")

d.legend(H - 44, [("앞으로의 표준", ACC), ("유저 공간 훅", INFO),
                  ("커널 훅", WARN), ("성능 분석 프론트엔드", OK)])
d.save("08-02.trace-sources.svg")
print("ok 08-02.trace-sources")
