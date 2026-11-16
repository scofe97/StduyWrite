# 05-01 §7 — cat /proc/cpuinfo 한 번이 지나는 실제 자리. cat 의 fd 3 이 VFS 의 file 을 거쳐 procfs 커널
#           핸들러에 닿고, 핸들러가 RAM 의 CPU 정보를 읽는 순간 텍스트로 만들어 사용자 버퍼에 2664 바이트를
#           채운다. 디스크 블록은 이 경로 어디에도 없다.
# 타입 스펙: type-architecture — 사용자 공간·커널·디스크 세 구역과 그 사이를 건너는 시스템 콜. accent 는 핸들러.
# 근거: 본문 §7 의 strace 실측(Debian 12 aarch64, openat(AT_FDCWD, "/proc/cpuinfo", O_RDONLY) = 3,
#       read(3, "processor\t: 0\nBogoMIPS\t: 48.00…", 131072) = 2664, write(1, …, 2664) = 2664,
#       read(3, "", 131072) = 0)과 "커널 핸들러가 RAM 의 CPU 정보를 그 자리에서 텍스트로 직렬화",
#       "du -sh /proc 은 0". 축약: buf 띠에서 2664 B 칸은 실제 비율(2%)보다 키웠다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 664
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §7",
      "읽는 순간 커널이 내용을 만든다",
      "cat /proc/cpuinfo 는 openat 으로 fd 3 을 받고, read 가 VFS 를 지나 procfs 커널 핸들러에 닿는다. "
      "핸들러는 RAM 의 CPU 정보를 그 자리에서 텍스트로 만들어 사용자 버퍼 buf 에 2664 바이트를 채우고, "
      "cat 은 write 로 같은 2664 바이트를 stdout 에 낸다. 두 번째 read 가 0 을 돌려주면 파일 끝이다. "
      "이 경로에 디스크 블록 읽기는 없고 du -sh /proc 은 0 이다.",
      "procfs 파일에는 디스크 블록이 없다 — 내용은 read 가 올 때 핸들러가 만든다")

# 구역과 열 좌표
UZ = (24, 100, 896, 252)          # 사용자 공간 구역 (x0, y0, x1, y1)
KZ = (24, 312, 896, 472)          # 커널 구역
BY0, BY1 = 128, 240               # 사용자 공간 상자 y
KY0, KY1 = 340, 452               # 커널 상자 y
P = (24 + 16, 280)                # cat 의 fd 테이블
B = (320, 600)                    # buf
T = (720, 896 - 16)               # 터미널
V = (24 + 16, 240)                # VFS
Hd = (320, 600)                   # procfs 핸들러
K = (680, 896 - 16)               # CPU 정보
XO = 140                          # openat 수직선 x
XR = (Hd[0] + Hd[1]) / 2          # read 수직선 x

# 구역 틀
for (x0, y0, x1, y1), name in ((UZ, "사용자 공간"), (KZ, "커널")):
    d.box(x0, y0, x1 - x0, y1 - y0, PAPER, RULE, 1.0, 10)
    d.t(x0 + 16, y0 + 20, name, 12, SOFT, KR, "start", 600)

# 연결선은 상자보다 먼저
d.arrow([(XO, BY1 + 2), (XO, KY0 - 3)], MUTED, "ar", 1.4)
d.t(XO + 12, 276, '1 openat("/proc/cpuinfo",', 12, MUTED, MONO, "start")
d.t(XO + 12, 294, "O_RDONLY) = 3", 12, MUTED, MONO, "start")
d.arrow([(XR, KY0 - 2), (XR, BY1 + 3)], ACC, "acc", 1.8)
d.t(XR + 12, 276, "2 read(3, buf, 131072) = 2664", 12, ACC, MONO, "start", 600)
d.t(XR + 12, 294, '4 read(3, "", 131072) = 0', 12, SOFT, MONO, "start")
d.t(XR + 206, 294, "파일 끝", 12, SOFT, KR, "start")
d.arrow([(B[1] + 2, 196), (T[0] - 3, 196)], MUTED, "ar", 1.4)
d.t((B[1] + T[0]) / 2, 182, "3 write(1, …)", 12, MUTED, MONO)
d.t((B[1] + T[0]) / 2, 216, "= 2664", 12, MUTED, MONO)
d.arrow([(V[1] + 2, 396), (Hd[0] - 3, 396)], MUTED, "ar", 1.4)
d.t((V[1] + Hd[0]) / 2, 386, "read", 12, MUTED, MONO)
d.arrow([(K[0] - 2, 396), (Hd[1] + 3, 396)], INFO, "info", 1.4)
d.t((K[0] + Hd[1]) / 2, 386, "값 읽기", 12, INFO, KR)
# 디스크로는 가지 않는다
DY0, DY1 = 512, 560
d.line(XR, KY1 + 2, XR, DY0 - 2, BAD, 1.2, "3 4")
d.t(XR, 497, "✕", 14, BAD, MONO)
d.t(XR + 16, 496, "블록 I/O 없음", 12, BAD, KR, "start")

# 사용자 공간 — cat 의 fd 테이블
x0, x1 = P
d.box(x0, BY0, x1 - x0, BY1 - BY0, PAPER2, RULE, 1.0, 8)
d.t(x0 + 14, BY0 + 22, "cat 의 fd 테이블", 13, INK, KR, "start", 600)
d.o.append(f'<rect x="{x0 + 12}" y="{BY0 + 38}" width="{x1 - x0 - 24}" height="28" rx="4" '
           f'fill="none" stroke="{RULE}" stroke-width="0.9"/>')
d.t(x0 + 24, BY0 + 57, "1 → stdout", 12, MUTED, MONO, "start")
d.o.append(f'<rect x="{x0 + 12}" y="{BY0 + 74}" width="{x1 - x0 - 24}" height="28" rx="4" '
           f'fill="{INFO}1A" stroke="{INFO}" stroke-width="1.1"/>')
d.t(x0 + 24, BY0 + 93, "3 → /proc/cpuinfo", 13, INK, MONO, "start", 600)

# 사용자 공간 — buf
x0, x1 = B
d.box(x0, BY0, x1 - x0, BY1 - BY0, PAPER2, ACC, 1.1, 8)
d.t(x0 + 14, BY0 + 22, "buf", 13, INK, MONO, "start", 600)
d.t(x0 + 48, BY0 + 22, "cat 의 사용자 버퍼", 12, MUTED, KR, "start")
BX0, BX1, BYB = x0 + 14, x1 - 14, BY0 + 40
d.o.append(f'<rect x="{BX0}" y="{BYB}" width="{BX1 - BX0}" height="20" rx="3" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="3 3"/>')
d.o.append(f'<rect x="{BX0}" y="{BYB}" width="28" height="20" rx="3" fill="{ACC}55" '
           f'stroke="{ACC}" stroke-width="1"/>')
d.t(BX0 + 40, BYB + 15, "2664 B 채움", 12, ACC, KR, "start", 600)
d.t(BX1 - 10, BYB + 15, "131072 B 요청", 12, SOFT, MONO, "end")
d.t(x0 + 14, BY0 + 92, r'"processor\t: 0\nBogoMIPS…"', 12, MUTED, MONO, "start")

# 사용자 공간 — 터미널
x0, x1 = T
d.box(x0, BY0, x1 - x0, BY1 - BY0, PAPER2, RULE, 1.0, 8)
d.t(x0 + 14, BY0 + 22, "터미널", 13, INK, KR, "start", 600)
d.t(x0 + 14, BY0 + 46, "stdout", 12, MUTED, MONO, "start")
d.t(x0 + 14, BY0 + 92, "2664 B 표시", 12, MUTED, KR, "start")

# 커널 — VFS
x0, x1 = V
d.box(x0, KY0, x1 - x0, KY1 - KY0, PAPER2, RULE, 1.0, 8)
d.t(x0 + 14, KY0 + 22, "VFS", 13, INK, MONO, "start", 600)
d.t(x0 + 14, KY0 + 46, "fd 3 의 file", 12, MUTED, KR, "start")
d.t(x0 + 14, KY0 + 92, "procfs 로 넘김", 12, SOFT, KR, "start")

# 커널 — procfs 핸들러 (focal)
x0, x1 = Hd
d.tone(x0, KY0, x1 - x0, KY1 - KY0, ACC, 8, "1F", 1.4)
d.t(x0 + 14, KY0 + 22, "procfs 커널 핸들러", 13, ACC, KR, "start", 600)
d.t(x0 + 14, KY0 + 46, "read 가 온 순간 텍스트로 만듦", 12, INK, KR, "start")
d.t(x0 + 14, KY0 + 92, "2664 B 생성 → buf 로 복사", 12, MUTED, KR, "start")

# 커널 — CPU 정보
x0, x1 = K
d.tone(x0, KY0, x1 - x0, KY1 - KY0, INFO, 8)
d.t(x0 + 14, KY0 + 22, "CPU 정보", 13, INFO, KR, "start", 600)
d.t(x0 + 14, KY0 + 46, "RAM 의 커널 자료구조", 12, INK, KR, "start")
d.t(x0 + 14, KY0 + 92, "processor · BogoMIPS", 12, MUTED, MONO, "start")

# 디스크 — 거치지 않음
d.o.append(f'<rect x="{UZ[0]}" y="{DY0}" width="{UZ[2] - UZ[0]}" height="{DY1 - DY0}" rx="8" '
           f'fill="none" stroke="{BAD}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(UZ[0] + 16, DY0 + 29, "디스크 블록", 13, BAD, KR, "start", 600)
d.t(UZ[0] + 112, DY0 + 29, "이 경로에 없음", 12, MUTED, KR, "start")
d.t(UZ[2] - 16, DY0 + 29, "du -sh /proc → 0", 13, BAD, MONO, "end", 600)

d.t(24, 592, "strace 실측 · Debian 12 aarch64 · 공유 라이브러리 줄은 뺌 · buf 의 2664 B 칸은 읽히게 키움",
    11, SOFT, KR, "start")
LEG = 612
d.legend(LEG, [("RAM 의 커널 자료구조", INFO), ("내용을 만드는 핸들러", ACC), ("거치지 않는 디스크", BAD)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.pseudo-fs.svg")
print("ok 05-01.pseudo-fs")
