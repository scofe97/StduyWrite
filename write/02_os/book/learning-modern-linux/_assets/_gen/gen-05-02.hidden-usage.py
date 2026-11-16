# 05-02 §7 — 지워졌지만 열린 파일. 프로세스의 fd 3 이 /mnt/h/big 의 아이노드를 잡고 있어, rm(unlink)으로
#           디렉터리의 이름은 사라졌어도 64 MiB 데이터 블록은 할당된 채 남는다. du 는 디렉터리 트리를 돌아
#           이름만 세고(1M), df 는 슈퍼블록의 할당 블록 수를 읽어(65M Used) 둘이 어긋나는 실제 자리.
# 타입 스펙: type-architecture — 프로세스·디렉터리·아이노드·데이터 블록·슈퍼블록과 두 도구가 읽는 자리.
#           accent 는 블록을 붙잡는 fd 3.
# 근거: 본문 §7 「지워졌지만 열린 파일에 의한 불일치」의 실측(ls -l /proc/4462/fd 의
#       "3 -> /mnt/h/big (deleted)", tail -f, 64MiB big, du -sm /mnt/h → 1M, df -BM /mnt/h → 65M Used,
#       : > /proc/4462/fd/3 뒤 Used 65M → 1M)과 unlink(2)·링크 수 0·슈퍼블록 할당 블록 카운터 설명.
# 예시: 디렉터리의 다른 항목(…)과 블록 띠의 칸 수는 그림을 위한 것이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 620
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §7",
      "이름은 지워졌는데 블록은 fd 가 붙잡고 있다",
      "PID 4462(tail -f)의 fd 3 이 /mnt/h/big 의 아이노드를 열고 있다. rm 은 unlink(2)로 디렉터리의 "
      "이름 big 만 지워 링크 수가 0 이 되지만, 열린 참조가 남아 64 MiB 데이터 블록은 할당된 채다. "
      "du 는 디렉터리 트리를 돌아 1M 만 세고, df 는 슈퍼블록의 할당 블록 수를 읽어 65M Used 를 보인다. "
      ": > /proc/4462/fd/3 으로 파일을 비우면 Used 가 1M 으로 떨어진다.",
      "du 는 이름을 세고 df 는 할당된 블록을 센다 — 이름 없는 열린 파일이 그 차이다")

# ── 위 줄: du · 프로세스 · df ─────────────────────────────────
TY, TH = 104, 92
COLS = {"du": (24, 264), "proc": (312, 608), "df": (656, 896)}
cdu = sum(COLS["du"]) / 2
cpr = sum(COLS["proc"]) / 2
cdf = sum(COLS["df"]) / 2

# 컨테이너와 아래 줄 좌표
FX0, FX1, FY0, FY1 = 24, 896, 232, 488
DIR = (48, 264, 288, 448)          # 디렉터리
INO = (336, 584, 368, 448)         # 아이노드
SB = (656, 872, 288, 336)          # 슈퍼블록
BLK = (656, 872, 368, 448)         # 데이터 블록

# 화살표·연결선은 상자보다 먼저
d.box(FX0, FY0, FX1 - FX0, FY1 - FY0, PAPER, RULE, 1.0, 10)
d.t(FX0 + 16, FY1 - 12, "/mnt/h 에 마운트된 파일시스템", 13, INK, KR, "start", 600)
d.arrow([(cdu, TY + TH + 2), (cdu, DIR[2] - 3)], INFO, "info", 1.4)
d.t(cdu + 10, FY0 + 44, "트리를 돎", 12, INFO, KR, "start")
d.arrow([(cdf, TY + TH + 2), (cdf, SB[2] - 3)], WARN, "warn", 1.4)
d.t(cdf + 10, FY0 + 44, "카운터를 읽음", 12, WARN, KR, "start")
d.arrow([(cpr, TY + TH + 2), (cpr, INO[2] - 3)], ACC, "acc", 1.8)
d.t(cpr + 12, 316, "열린 참조", 12, ACC, KR, "start", 600)
d.line(cdf, SB[3] + 2, cdf, BLK[2] - 2, WARN, 1.1, "3 3")
d.t(cdf + 10, SB[3] + 22, "64 MiB 포함", 12, WARN, KR, "start")
d.arrow([(INO[1] + 2, 408), (BLK[0] - 3, 408)], MUTED, "ar", 1.4)
d.t((INO[1] + BLK[0]) / 2, 398, "포인터", 12, MUTED, KR)
# 디렉터리 항목 big → 아이노드: 끊긴 링크
d.line(DIR[1] + 2, 408, INO[0] - 2, 408, BAD, 1.2, "3 4")
d.t((DIR[1] + INO[0]) / 2, 413, "✕", 14, BAD, MONO)

# du
x0, x1 = COLS["du"]
d.box(x0, TY, x1 - x0, TH, PAPER2, INFO, 1.2, 8)
d.t(x0 + 16, TY + 24, "du -sm /mnt/h", 13, INFO, MONO, "start", 600)
d.t(x0 + 16, TY + 54, "1M", 22, INFO, MONO, "start", 600)
d.t(x0 + 16, TY + 76, "이름이 있는 파일만", 12, MUTED, KR, "start")
# df
x0, x1 = COLS["df"]
d.box(x0, TY, x1 - x0, TH, PAPER2, WARN, 1.2, 8)
d.t(x0 + 16, TY + 24, "df -BM /mnt/h", 13, WARN, MONO, "start", 600)
d.t(x0 + 16, TY + 54, "65M Used", 22, WARN, MONO, "start", 600)
d.t(x0 + 16, TY + 76, "할당된 블록 전부", 12, MUTED, KR, "start")
# 프로세스와 fd 테이블
x0, x1 = COLS["proc"]
d.box(x0, TY, x1 - x0, TH, PAPER2, RULE, 1.0, 8)
d.t(x0 + 16, TY + 24, "PID 4462", 13, INK, MONO, "start", 600)
d.t(x0 + 92, TY + 24, "tail -f · fd 테이블", 12, MUTED, KR, "start")
d.o.append(f'<rect x="{x0 + 16}" y="{TY + 40}" width="{x1 - x0 - 32}" height="36" rx="4" '
           f'fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
d.t(x0 + 28, TY + 63, "3 -> /mnt/h/big (deleted)", 13, ACC, MONO, "start", 600)

# 디렉터리
x0, x1, y0, y1 = DIR
d.box(x0, y0, x1 - x0, y1 - y0, PAPER2, INFO, 1.1, 6)
d.t(x0 + 14, y0 + 22, "디렉터리 /mnt/h", 13, INK, KR, "start", 600)
d.o.append(f'<rect x="{x0 + 12}" y="{y0 + 40}" width="{x1 - x0 - 24}" height="32" rx="4" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 3"/>')
d.t(x0 + 26, y0 + 61, "… 다른 이름", 12, SOFT, KR, "start")
d.o.append(f'<rect x="{x0 + 12}" y="{y0 + 92}" width="{x1 - x0 - 24}" height="32" rx="4" '
           f'fill="{BAD}14" stroke="{BAD}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(x0 + 26, y0 + 113, "big", 13, BAD, MONO, "start", 600)
d.line(x0 + 22, y0 + 108, x0 + 58, y0 + 108, BAD, 1.4)
d.t(x0 + 70, y0 + 113, "rm → unlink(2)", 12, BAD, MONO, "start")
d.t(x0 + 14, y0 + 148, "이름만 사라짐", 12, MUTED, KR, "start")

# 아이노드
x0, x1, y0, y1 = INO
d.tone(x0, y0, x1 - x0, y1 - y0, WARN, 6)
d.t((x0 + x1) / 2, y0 + 24, "big 의 아이노드", 13, WARN, KR, "middle", 600)
d.t((x0 + x1) / 2, y0 + 48, "링크 수 0", 13, INK, KR)
d.t((x0 + x1) / 2, y0 + 68, "열린 참조 남음 → 해제 안 됨", 12, MUTED, KR)

# 슈퍼블록
x0, x1, y0, y1 = SB
d.box(x0, y0, x1 - x0, y1 - y0, PAPER2, WARN, 1.1, 6)
d.t((x0 + x1) / 2, y0 + 20, "슈퍼블록", 13, INK, KR, "middle", 600)
d.t((x0 + x1) / 2, y0 + 38, "할당 블록 카운터", 12, MUTED, KR)

# 데이터 블록 띠
x0, x1, y0, y1 = BLK
d.box(x0, y0, x1 - x0, y1 - y0, PAPER2, BAD, 1.1, 6)
n, cw = 8, (x1 - x0 - 24) / 8
for i in range(n):
    d.o.append(f'<rect x="{x0 + 12 + i * cw + 1:.1f}" y="{y0 + 12}" width="{cw - 2:.1f}" height="24" rx="2" '
               f'fill="{BAD}33" stroke="{BAD}" stroke-width="0.8"/>')
d.t((x0 + x1) / 2, y0 + 58, "데이터 블록 64 MiB", 13, INK, KR, "middle", 600)
d.t((x0 + x1) / 2, y0 + 74, "아직 할당됨", 12, BAD, KR, "middle")

# 해결 한 줄
RY = FY1 + 36
d.t(24, RY, ": > /proc/4462/fd/3", 13, OK, MONO, "start", 600)
d.t(200, RY, "fd 손잡이로 0바이트로 자름 → df Used 65M → 1M", 13, OK, KR, "start")
d.t(24, RY + 32, "PID·fd·크기·du·df 값은 본문 실측 그대로 · 디렉터리의 다른 이름과 블록 칸 수는 예시",
    11, SOFT, KR, "start")
LEG = RY + 52
d.legend(LEG, [("du 가 보는 자리", INFO), ("df 가 보는 자리", WARN), ("붙잡힌 블록", BAD), ("회수", OK)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-02.hidden-usage.svg")
print("ok 05-02.hidden-usage")
