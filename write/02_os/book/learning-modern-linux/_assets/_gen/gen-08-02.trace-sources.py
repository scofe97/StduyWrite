# 08-02 §7 — 프로세스 하나의 실행이 유저 공간 함수 → 시스템 콜 → 커널 함수로 내려가는 길에
#           훅 지점(uprobes · 시스템 콜 · kprobes · 커널 트레이스포인트)이 붙고, 거기서 나온 이벤트가
#           시간에 걸쳐 트레이스로 쌓여 strace · perf · 프로파일러가 읽는 구조.
# 원문("Tracing and Profiling"): "in the context of Linux, on a single machine, tracing means capturing
#       the process execution (function calls in user space, syscalls, etc.) over time."
#       소스는 The Linux kernel("Traces can come from functions in the kernel or be triggered by syscalls.
#       Examples include kernel probes (kprobes) or kernel tracepoints.") 와
#       User space("Application function calls, for example via user space probes (uprobes), can act as
#       a source for traces.") 다.
#       용도는 strace 로 디버깅, perf 프론트엔드로 성능 분석(`sudo perf top` 은 프로세스별 요약),
#       경고는 strace 의 오버헤드(프로덕션). eBPF 는 추적 구현의 사실상 표준이 될 것이라는 저자 전망,
#       프로파일링 도구는 pprof · Valgrind · 플레임 그래프, eBPF 기반 지속적 프로파일링 parca.
# 본문 §7: 시스템 콜은 커널이 기능을 드러내는 유일한 통로(2장)이고 추적은 그 통로를 훅 지점으로 쓴다.
#       eBPF 는 커널을 다시 빌드하지 않고 커널 안에서 코드를 돌린다.
# 타입 스펙: type-architecture — 유저 공간 · 시스템 콜 경계 · 커널 구역에 실행 길과 훅을 놓고, 트레이스와
#           그것을 읽는 도구를 잇는다. focal 은 커널 안에서 도는 eBPF.
# 축약/예시: 트레이스 칸의 눈금 위치는 "시간에 걸친 이벤트" 를 보이기 위한 예다. 도구가 어느 훅을 쓰는지는
#       본문에 없어 도구는 트레이스 전체에 잇는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 600
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §7",
      "실행 길 위의 훅에서 트레이스가 나온다",
      "프로세스 하나의 실행은 유저 공간의 함수 호출에서 시스템 콜을 지나 커널 함수로 내려간다. 유저 공간에는 "
      "uprobes, 커널에는 kprobes 와 커널 트레이스포인트가 훅으로 걸리고, 시스템 콜이 커널 추적의 트리거가 된다. "
      "훅에서 나온 이벤트가 시간에 걸쳐 트레이스로 쌓이고 strace(디버깅, 오버헤드 주의)·perf(성능 분석)·"
      "프로파일러가 그것을 읽는다. 커널 안에서 도는 eBPF 가 추적 구현의 표준이 되리라는 것이 저자의 전망이다.",
      "추적은 유저 공간 함수 · 시스템 콜 · 커널 함수에 건 훅에서 시간에 걸친 이벤트를 붙잡는다")

ZX0, ZX1 = 24, 456
EX0, EX1 = 48, 232             # 실행 길 상자
HX0, HX1 = 280, 440            # 훅 상자
TX0, TX1 = 488, 640            # 트레이스
OX0, OX1 = 680, 896            # 도구
UY0, UY1 = 112, 216
SY0, SY1 = 228, 268
KY0, KY1 = 280, 488
ROWS = [(164, INFO), ((SY0 + SY1) / 2, MUTED), (324, WARN), (372, WARN)]   # 훅 줄 y

# ── 구역(선보다 먼저) ────────────────────────────────────────
d.o.append(f'<rect x="{ZX0}" y="{UY0}" width="{ZX1 - ZX0}" height="{UY1 - UY0}" rx="8" fill="{INFO}0A" '
           f'stroke="{INFO}" stroke-width="1.1" stroke-dasharray="5 4"/>')
d.t(ZX0 + 14, UY0 + 18, "유저 공간", 12, INFO, KR, "start", 600)
d.o.append(f'<rect x="{ZX0}" y="{KY0}" width="{ZX1 - ZX0}" height="{KY1 - KY0}" rx="8" fill="{WARN}0A" '
           f'stroke="{WARN}" stroke-width="1.1" stroke-dasharray="5 4"/>')
d.t(ZX0 + 14, KY0 + 18, "커널", 12, WARN, KR, "start", 600)
d.box(ZX0, SY0, ZX1 - ZX0, SY1 - SY0, PAPER2, MUTED, 1.1, 4)
d.t(172, SY0 + 25, "시스템 콜", 13, INK, KR, "start", 600)
d.t(252, SY0 + 25, "유일한 통로 · 커널 추적의 트리거", 12, MUTED, KR, "start")

# ── 연결선(글자·상자보다 먼저) ───────────────────────────────
d.arrow([(140, 194), (140, 302)], INK, "ar", 1.8)                                  # 실행 길
for y, c in ((164, INFO), (324, WARN), (372, WARN)):
    d.line(EX1 + 2, y, HX0 - 2, y, c, 1.2, "3 3")                                 # 실행 길 → 훅
for (y, c), x0 in zip(ROWS, (HX1, ZX1, HX1, HX1)):
    d.arrow([(x0 + 2, y), (TX0 - 4, y)], c, {INFO: "info", MUTED: "ar", WARN: "warn"}[c], 1.3)
for y in (148, 236, 340):
    d.arrow([(TX1 + 2, y), (OX0 - 4, y)], MUTED, "ar", 1.3)

# ── 실행 길 ──────────────────────────────────────────────────
d.box(EX0, 136, EX1 - EX0, 56, PAPER2, RULE, 1.1, 6)
d.t(EX0 + 14, 160, "앱 함수 호출", 13, INK, KR, "start", 600)
d.t(EX0 + 14, 180, "프로세스의 실행", 12, MUTED, KR, "start")
d.box(EX0, 304, EX1 - EX0, 88, PAPER2, RULE, 1.1, 6)
d.t(EX0 + 14, 328, "커널 함수", 13, INK, KR, "start", 600)
d.t(EX0 + 14, 348, "커널 안의 함수", 12, MUTED, KR, "start")

# ── 훅 ───────────────────────────────────────────────────────
for y0, h, name, sub, c in ((136, 56, "uprobes", "유저 공간 프로브", INFO),
                            (304, 40, "kprobes", "", WARN), (352, 40, "tracepoints", "", WARN)):
    d.box(HX0, y0, HX1 - HX0, h, PAPER2, c, 1.2, 6)
    d.t(HX0 + 12, y0 + (24 if sub else 25), name, 13, c, MONO, "start", 600)
    if sub:
        d.t(HX0 + 12, y0 + 44, sub, 12, MUTED, KR, "start")
d.t(HX1 - 10, 329, "커널 프로브", 12, MUTED, KR, "end")

# eBPF (focal) — 커널 안에서 도는 코드
d.tone(EX0, 412, HX1 - EX0, 60, ACC, 6, "14", 1.4)
d.t(EX0 + 14, 438, "eBPF", 15, ACC, MONO, "start", 600)
d.t(EX0 + 76, 438, "커널 재빌드 없이 커널 안에서 도는 코드", 12, INK, KR, "start")
d.t(EX0 + 76, 458, "추적 구현의 사실상 표준(저자 전망)", 12, ACC, KR, "start")

# ── 트레이스 ─────────────────────────────────────────────────
d.box(TX0, UY0, TX1 - TX0, 392 - UY0 + 16, PAPER, RULE, 1.1, 8)
d.t(TX0 + 12, UY0 + 22, "트레이스", 13, INK, KR, "start", 600)
d.t(TX1 - 12, UY0 + 22, "시간 →", 12, SOFT, KR, "end")
TICKS = [(4, 22, 30, 70, 96, 104), (10, 44, 52, 88, 118), (16, 28, 60, 64, 100, 124), (36, 40, 76, 112)]
for (y, c), ts in zip(ROWS, TICKS):
    d.line(TX0 + 12, y, TX1 - 12, y, RULE, 0.8)
    for t in ts:
        d.o.append(f'<rect x="{TX0 + 12 + t}" y="{y - 7}" width="3" height="14" rx="1" fill="{c}"/>')

# ── 도구 ─────────────────────────────────────────────────────
d.box(OX0, 112, OX1 - OX0, 72, PAPER2, BAD, 1.1, 6)
d.t(OX0 + 14, 136, "strace", 13, INK, MONO, "start", 600)
d.t(OX0 + 80, 136, "디버깅", 12, MUTED, KR, "start")
d.t(OX0 + 14, 164, "오버헤드 · 프로덕션 주의", 12, BAD, KR, "start")
d.box(OX0, 200, OX1 - OX0, 72, PAPER2, OK, 1.1, 6)
d.t(OX0 + 14, 224, "perf", 13, INK, MONO, "start", 600)
d.t(OX0 + 56, 224, "성능 분석 프론트엔드", 12, MUTED, KR, "start")
d.t(OX0 + 14, 252, "sudo perf top", 12, OK, MONO, "start")
d.t(OX0 + 120, 252, "프로세스별 요약", 12, MUTED, KR, "start")
d.box(OX0, 288, OX1 - OX0, 104, PAPER2, OK, 1.1, 6)
d.t(OX0 + 14, 312, "프로파일링", 13, INK, KR, "start", 600)
d.t(OX0 + 14, 334, "자주 호출되는 구간", 12, MUTED, KR, "start")
d.t(OX0 + 14, 356, "pprof · Valgrind", 12, OK, MONO, "start")
d.t(OX0 + 14, 378, "parca", 12, ACC, MONO, "start", 600)
d.t(OX0 + 60, 378, "eBPF 기반 · 지속적", 12, MUTED, KR, "start")

d.t(ZX0, 516, "분산 추적(OpenTelemetry · Jaeger)은 이 책의 범위 밖 · 여기는 단일 기계의 추적", 12, SOFT, KR, "start")
d.t(ZX0, 540, "트레이스 칸의 눈금 위치는 예 · 도구는 훅별이 아니라 트레이스 전체에 이음", 11, SOFT, KR, "start")
LEG = 556
d.legend(LEG, [("유저 공간 훅", INFO), ("커널 훅", WARN), ("읽는 도구", OK), ("오버헤드 경고", BAD)])
assert LEG + 40 <= H, (LEG, H)
d.save("08-02.trace-sources.svg")
print("ok 08-02.trace-sources")
