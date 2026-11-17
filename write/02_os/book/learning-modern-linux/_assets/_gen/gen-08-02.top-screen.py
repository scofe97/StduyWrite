# 08-02 §5 — 실제 top 화면을 줄 그대로 놓고, 네 구역과 키가 화면의 어느 줄·어느 열에 걸리는지 붙인다.
# 실측: debian:12 컨테이너, nice 10 무한 반복문을 띄운 채 `top -b -n 2 -d 1` 의 둘째 프레임(2026-11-10).
#   화면 줄은 본문 출력 블록 그대로다. 요약 줄의 연속 공백만 하나로 줄였고, 프로세스 표는 열마다
#   본문 출력의 열 끝(왼쪽 정렬 열은 열 시작)에 맞춰 낱말 단위로 놓았다.
# 1차 자료(procps-ng top(1)): "m :Memory/Swap-Usage toggle ... 4-way toggle",
#       정렬 키 "M %MEM" · "P %CPU" · "N PID" · "T TIME+" 와 그 키들이 도움말 화면에 나오지 않는다는 설명,
#       "V :Forest-View-Mode toggle".
# 타입 스펙: type-layers — 위에서 아래로 쌓인 화면 구역. 왼쪽 여백에 구역 번호, 오른쪽에 구역 이름과
#           그 줄에 걸리는 키, 아래에 열에 걸리는 정렬 키. focal 은 대문자 M 이 정렬하는 %MEM 열.
import re
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 540
FS, CW = 12, 7.2                      # 터미널 글자 크기와 mono 한 칸 폭(0.6em)
TX0, TX1, TY0 = 72, 688, 104          # 터미널 상자
X0 = TX0 + 16                         # 터미널 글자 시작
LH = 22
ROW = lambda i: TY0 + 26 + i * LH     # i 번째 화면 줄의 baseline

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §5",
      "top 화면의 네 구역과 키가 걸리는 자리",
      "nice 10 반복문이 CPU 하나를 다 쓰는 동안 top -b -n 2 로 받은 둘째 프레임이다. 첫 줄은 uptime, "
      "둘째 줄은 태스크 수, 셋째 줄은 vmstat 과 같은 CPU 축이며 ni 14.8 의 대부분이 반복문의 몫이다. "
      "MiB Mem·MiB Swap 두 줄은 free 와 같은 값이고 소문자 m 이 그 표시를 네 단계로 바꾼다. 아래 표가 "
      "프로세스 목록이며 대문자 M 은 %MEM 열, P 는 %CPU 열로 정렬한다. N·T 는 PID·TIME+ 정렬 키로 도움말 화면에 없다.",
      "메모리 정렬은 대문자 M 이 %MEM 열에 걸고, 소문자 m 은 메모리 두 줄의 표시만 바꾼다")

HEADER = "    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND"
PROCS = ["   3078 root      30  10    2340   1424   1304 R 100.0   0.0   0:02.15 sh",
         "      1 root      20   0    3784   2756   2456 S   0.0   0.0   0:00.00 bash",
         "   3077 root      20   0    2240   1132   1024 S   0.0   0.0   0:00.00 sleep",
         "   3080 root      20   0    8368   4528   2456 R   0.0   0.1   0:00.00 top"]
cols = []                              # (헤더, 앵커, 열 x)
for m in re.finditer(r"\S+", HEADER):
    left = m.group() in ("USER", "COMMAND")
    cols.append((m.group(), "start" if left else "end", X0 + (m.start() if left else m.end()) * CW))


def col_center(name):                  # 열 테두리(열 끝 -39 ~ +2)의 가운데
    h, a, x = next(c for c in cols if c[0] == name)
    return x - 18.5


# ── 터미널 상자와 열 강조(글자보다 먼저) ─────────────────────
TY1 = ROW(10) + 16
d.box(TX0, TY0, TX1 - TX0, TY1 - TY0, PAPER, RULE, 1.1, 8)
# 열 테두리: 열 끝에서 왼쪽 39px · 오른쪽 2px. 두 열 끝이 6칸(43.2px) 떨어져 서로 겹치지 않는다
col_end = {h: x for h, a, x in cols if a == "end"}
for name, c, op, sw, dash in (("%CPU", OK, "0A", 1.0, ' stroke-dasharray="4 3"'), ("%MEM", ACC, "14", 1.4, "")):
    e = col_end[name]
    d.o.append(f'<rect x="{e - 39:.1f}" y="{ROW(6) - 16}" width="41" height="{ROW(10) - ROW(6) + 24}" rx="4" '
               f'fill="{c}{op}" stroke="{c}" stroke-width="{sw}"{dash}/>')

# 정렬 키 → 열: 화살표를 칩보다 먼저
KY = TY1 + 40
for name, c, m in (("%CPU", OK, "ok"), ("%MEM", ACC, "acc")):
    cx = col_center(name)
    d.arrow([(cx, KY - 12), (cx, ROW(10) + 10)], c, m, 1.6 if c is ACC else 1.3)

# ── 화면 줄 ───────────────────────────────────────────────────
d.t(X0, ROW(0), "top - 05:02:54 up 2:50, 0 user, load average: 1.82, 1.64, 1.41", FS, INFO, MONO, "start")
d.t(X0, ROW(1), "Tasks: 6 total, 2 running, 4 sleeping, 0 stopped, 0 zombie", FS, INK, MONO, "start")
cpu = ["%Cpu(s):", "1.4 us,", "0.5 sy,", "14.8 ni,", "81.9 id,", "0.1 wa,", "0.0 hi,", "1.3 si,", "0.0 st"]
for j, tok in enumerate(cpu):
    x = X0 + (0 if j == 0 else 66 + (j - 1) * 64)
    hot = tok.startswith("14.8")
    d.t(x, ROW(2), tok, FS, OK if hot else INK, MONO, "start", 600 if hot else 400)
d.t(X0, ROW(3), "MiB Mem : 8004.2 total, 5286.1 free, 1884.1 used, 1117.6 buff/cache", FS, WARN, MONO, "start")
d.t(X0, ROW(4), "MiB Swap: 9028.2 total, 9028.2 free, 0.0 used. 6120.1 avail Mem", FS, WARN, MONO, "start")
for h, a, x in cols:
    c = ACC if h == "%MEM" else OK if h == "%CPU" else MUTED
    d.t(round(x, 1), ROW(6), h, FS, c, MONO, a, 600)
for i, line in enumerate(PROCS):
    for (h, a, x), v in zip(cols, line.split()):
        hot = i == 0 and h in ("NI", "%CPU", "COMMAND")
        d.t(round(x, 1), ROW(7 + i), v, FS, OK if hot else INK, MONO, a, 600 if hot else 400)

# ── 왼쪽 여백: 구역 번호와 묶음 괄호 ─────────────────────────
zones = [("1", 0, 0, INFO), ("2", 1, 1, MUTED), ("3", 2, 2, MUTED), ("", 3, 4, WARN), ("4", 6, 10, MUTED)]
for num, a, b, c in zones:
    y0, y1 = ROW(a) - 14, ROW(b) + 5
    d.line(TX0 - 10, y0, TX0 - 10, y1, c, 1.6)
    if num:
        d.t(TX0 - 28, (y0 + y1) / 2 + 5, num, 13, c if c is not MUTED else INK, MONO, "middle", 600)

# ── 오른쪽: 구역 이름과 그 줄에 걸리는 키 ────────────────────
RX = TX1 + 24
notes = [(0, "시스템 요약 = uptime", INFO), (1, "태스크 통계", INK), (2, "CPU 사용 = vmstat 축", INK),
         (3, "free 와 같은 두 줄", WARN), (6, "프로세스 목록 = ps aux", INK)]
for i, txt, c in notes:
    d.line(TX1 + 4, ROW(i) - 4, RX - 6, ROW(i) - 4, RULE, 1.0)
    d.t(RX, ROW(i), txt, 13, c, KR, "start", 600)
for i, k, txt, c in ((4, "m", "표시 4단 토글", WARN), (8, "V", "트리 보기 토글", MUTED), (10, "k", "시그널 보내기", MUTED)):
    d.chip(RX + 12, ROW(i) - 4, k, c, 12)
    d.t(RX + 32, ROW(i), txt, 12, c if c is WARN else MUTED, KR, "start")
d.t(RX, ROW(7) + 2, "ni 14.8 ≈ CPU 8개 중 하나", 12, OK, KR, "start")

# ── 아래: 열에 걸리는 정렬 키 ────────────────────────────────
cxp, cxm = col_center("%CPU"), col_center("%MEM")
d.chip(cxp, KY, "P", OK, 12)
d.t(cxp - 20, KY + 4, "%CPU 순 정렬", 12, OK, KR, "end", 600)
d.chip(cxm, KY, "M", ACC, 12)
d.t(cxm + 20, KY + 4, "%MEM 순 정렬", 12, ACC, KR, "start", 600)

NY = KY + 40
d.t(TX0, NY, "N · T 는 PID · TIME+ 순 정렬, 도움말 화면에 없음 · ? 도움말 · q 끝내기", 12, SOFT, KR, "start")
d.t(TX0, NY + 24, "화면 줄은 본문 top 출력 그대로 · 요약 줄의 연속 공백만 줄임", 11, SOFT, KR, "start")
LEG = NY + 40
d.legend(LEG, [("메모리 정렬 M", ACC), ("반복문 · P", OK),
               ("free 와 같은 줄 · m", WARN), ("uptime 과 같은 줄", INFO)])
assert LEG + 40 <= H, (LEG, H)
d.save("08-02.top-screen.svg")
print("ok 08-02.top-screen")
