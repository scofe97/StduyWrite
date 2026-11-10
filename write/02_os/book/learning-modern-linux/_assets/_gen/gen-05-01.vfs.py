# 05-01 §4 — read() 시스템 콜 한 번이 VFS 를 지나 ext4 와 procfs 로 갈라지는 시퀀스.
# 타입 스펙: type-sequence — 클라이언트 시스템 콜 호출이 VFS 간접 층을 거쳐 ext4(디스크)와 procfs(RAM)로 분기하는 시퀀스.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §4",
      "단일 시스템 콜 read() 가 VFS 를 거쳐 갈라지는 흐름",
      "같은 read() 시스템 콜이 VFS 간접 층을 지나 로컬 ext4 블록 I/O 와 "
      "가짜 procfs 커널 메모리 직렬화로 분기하는 시퀀스.",
      "VFS 는 시스템 콜과 파일시스템 구현 사이의 간접 층")

# 6개 참여자 라이프라인
actors = [
    ("User App", "cat 호출", 80, INK),
    ("VFS", "vfs_read", 230, ACC),
    ("ext4", "read_iter 구현", 390, OK),
    ("Block I/O", "dm-0 → sda2", 540, MUTED),
    ("procfs", "seq_read", 680, INFO),
    ("Kernel RAM", "내부 상태 직렬화", 815, WARN),
]

TOP_Y = 120
BOT_Y = 480

for name, sub, x, col in actors:
    d.box(x - 52, TOP_Y, 104, 44, PAPER2, col, 1.2, 6)
    d.t(x, TOP_Y + 18, name, 12, col, MONO if col != INK else KR, "middle", 600)
    d.t(x, TOP_Y + 34, sub, 11, MUTED, KR, "middle")
    d.line(x, TOP_Y + 44, x, BOT_Y, RULE, 1.0, "4 4")

# 1. ext4 갈래 (/myfile 읽기)
y1 = 186
d.t(80, y1 - 8, "1. cat 일반 파일 (로컬 블록)", 11, OK, KR, "start", 600)
d.arrow([(80, y1), (228, y1)], OK, "ok", 1.2)
d.t(155, y1 + 14, "read(fd_ext4)", 10, OK, MONO, "middle")

y2 = 214
d.arrow([(230, y2), (388, y2)], OK, "ok", 1.2)
d.t(310, y2 - 4, "ext4_file_read_iter()", 10, OK, MONO, "middle")

y3 = 242
d.arrow([(390, y3), (538, y3)], MUTED, "ar", 1.2)
d.t(465, y3 - 4, "submit_bio() 디스크 블록", 11, MUTED, KR, "middle")

y4 = 270
d.arrow([(540, y4), (392, y4)], MUTED, "ar", 1.2, dash="3 3")
d.t(465, y4 - 4, "4096B 데이터 블록", 11, MUTED, KR, "middle")

y5 = 298
d.arrow([(390, y5), (82, y5)], OK, "ok", 1.2, dash="3 3")
d.t(235, y5 - 4, "버퍼 데이터 반환", 11, OK, KR, "middle")

# 구분 가로선
d.line(40, 324, W - 40, 324, RULE, 0.8, "2 2")

# 2. procfs 갈래 (/proc/cpuinfo 읽기)
y6 = 348
d.t(80, y6 - 8, "2. cat /proc/cpuinfo (가짜 파일시스템)", 11, INFO, KR, "start", 600)
d.arrow([(80, y6), (228, y6)], INFO, "info", 1.2)
d.t(155, y6 + 14, "read(fd_proc)", 10, INFO, MONO, "middle")

y7 = 376
d.arrow([(230, y7), (678, y7)], INFO, "info", 1.2)
d.t(455, y7 - 4, "proc_reg_read_iter() (seq_file)", 10, INFO, MONO, "middle")

y8 = 404
d.arrow([(680, y8), (813, y8)], WARN, "warn", 1.2)
d.t(747, y8 - 4, "RAM CPU 상태 읽기", 11, WARN, KR, "middle")

y9 = 432
d.arrow([(815, y9), (682, y9)], WARN, "warn", 1.2, dash="3 3")
d.t(747, y9 - 4, "2664B 텍스트 직렬화", 11, WARN, KR, "middle")

y10 = 460
d.arrow([(680, y10), (82, y10)], INFO, "info", 1.2, dash="3 3")
d.t(380, y10 - 4, "즉석 생성 텍스트 반환 (디스크 I/O 0회)", 11, INFO, KR, "middle")

# 하단 요약 카드
BY = 500
BW = W - 48
d.box(24, BY, BW, 72, PAPER2, ACC, 1.2, 8)
d.t(44, BY + 24, "VFS 의 간접 층 추상화", 13.5, ACC, KR, "start", 600)
d.t(44, BY + 46, "클라이언트 관점 — open · read · stat 균일한 시스템 콜 손잡이", 11.5, INK, KR, "start")
d.t(44, BY + 64, "ext4 는 블록 계층으로, procfs 는 메모리 핸들러로 분기", 11, MUTED, KR, "start")

d.legend(588, [("로컬 ext4 블록 I/O", OK), ("VFS 공통 추상 층", ACC),
               ("procfs 및 커널 RAM", INFO), ("직렬화 생성", WARN)])
d.save("05-01.vfs.svg")
print("ok 05-01.vfs")
