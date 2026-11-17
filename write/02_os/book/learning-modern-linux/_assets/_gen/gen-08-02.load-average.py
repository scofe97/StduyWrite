# 08-02 §2 — 같은 부하 평균이 CPU 수에 따라 CPU 하나에 걸린 몫이 달라진다.
# 1차 자료(procps-ng uptime(1)): "Load averages are not normalized for the number of CPUs in a system,
#       so a load average of 1 means a single CPU system is loaded all the time while on a 4 CPU system
#       it means it was idle 75% of the time."
# 실측: debian:12 컨테이너 `uptime; nproc` → load average 1.37, 1.38, 1.30 · nproc 8 (2026-11-10).
#       위 띠는 그 출력 줄을 그대로 옮겼고, 셋째 행은 1분 값 1.37 을 CPU 8개로 나눈 것이다.
# 앞 두 행은 man page 의 예다. 센 대상(runnable · uninterruptible 프로세스)은 본문 §2 의 문장이다.
# 타입 스펙: type-bar — 칸 하나가 CPU 하나이고, 칸을 채운 높이가 load ÷ CPU 수에 정비례한다.
#           축약: 부하가 CPU 들에 고르게 나뉜다고 보고 칸마다 같은 높이로 채웠다. 실제 스케줄러의
#           CPU 별 분배는 출력에 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §2",
      "부하 평균을 CPU 수로 나눈 몫",
      "uptime 출력의 load average 1.37, 1.38, 1.30 은 1·5·15분 평균이고, 센 것은 실행 가능하거나 "
      "인터럽트 불가 상태인 프로세스 수다. 이 값은 CPU 수로 정규화되지 않는다. 칸 하나를 CPU 하나로 그리면 "
      "load 1.00 은 CPU 1개에서 칸을 가득 채우고, CPU 4개에서는 칸마다 0.25 만 채워 75% 가 논다. "
      "컨테이너 실측 1.37 을 nproc 8 로 나누면 칸마다 0.17 이다.",
      "값을 읽기 전에 그 기계의 CPU 수부터 확인합니다")

# 1. 출력 줄 — 본문의 uptime; nproc 출력을 그대로 옮긴다
SX, SY, SH, FS = 24, 96, 40, 13
CW = FS * 0.59                                  # mono 한 글자 폭(렌더 실측 ≈ 0.59em)
# SVG 는 연속 공백을 하나로 접으므로 접힌 모양으로 적어 1분·5분·15분 태그 위치를 맞춘다
line = "05:00:07 up 2:47, 0 user, load average: 1.37, 1.38, 1.30"
d.box(SX, SY, 600, SH, PAPER2, RULE, 0.9, 6)
d.t(SX + 8, SY + 25, line, FS, INK, MONO, "start")
d.box(SX + 616, SY, 120, SH, PAPER2, RULE, 0.9, 6)
d.t(SX + 628, SY + 25, "nproc → 8", FS, INK, MONO, "start")
for tok, tag, c in (("1.37", "1분", ACC), ("1.38", "5분", SOFT), ("1.30", "15분", SOFT)):
    cx = SX + 8 + (line.index(tok) + 2) * CW
    d.t(cx, SY + SH + 18, tag, 12, c, KR)
d.t(SX, SY + SH + 44, "센 것 = runnable + 인터럽트 불가(I/O 대기) 프로세스 수", 12, MUTED, KR, "start")

# 2. CPU 칸 — 칸 하나 = CPU 하나, 채운 높이 = load ÷ CPU 수
GX, CELL, GAP, CH = 264, 48, 8, 64
Y0, STRIDE = 216, 104
ROWS = [
    (1, 1.00, "man page 의 예", "1.00 ÷ 1 = 1.00", "내내 바쁨", INFO, False),
    (4, 1.00, "man page 의 예", "1.00 ÷ 4 = 0.25", "75% 유휴", INFO, False),
    (8, 1.37, "컨테이너 실측", "1.37 ÷ 8 = 0.17", "nproc 8", ACC, True),
]
for i, (n, load, src, calc, note, col, focal) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    share = load / n
    d.t(24, y + 26, f"CPU {n}개 · load {load:.2f}", 13, ACC if focal else INK, MONO, "start", 600)
    d.t(24, y + 46, src, 12, MUTED, KR, "start")
    for j in range(n):
        x = GX + j * (CELL + GAP)
        d.box(x, y, CELL, CH, PAPER2, col, 1.3 if focal else 1.0, 4)
        fh = CH * min(share, 1.0)
        d.o.append(f'<rect x="{x + 2}" y="{y + CH - fh:.1f}" width="{CELL - 4}" height="{fh - 2:.1f}" '
                   f'rx="2" fill="{col}{"66" if focal else "55"}"/>')
    vx = GX + 8 * (CELL + GAP) + 16
    d.t(vx, y + 26, calc, 13, col, MONO, "start", 600)
    d.t(vx, y + 46, note, 12, MUTED, KR, "start")

d.t(24, Y0 + 3 * STRIDE + 8, "칸 하나 = CPU 하나 · 채운 높이 = load ÷ CPU 수 · 고르게 나뉜다고 본 축약",
    11, SOFT, KR, "start")
d.legend(H - 48, [("man page 의 예", INFO), ("컨테이너 실측", ACC)])
d.save("08-02.load-average.svg")
print("ok 08-02.load-average")
