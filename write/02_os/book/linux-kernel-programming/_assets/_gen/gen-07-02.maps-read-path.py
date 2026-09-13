# 07-02 §2 — cat /proc/self/maps 한 줄이 어디서 만들어져 나오는가.
# 본문이 요구한 형태: "read() 시스템 콜 → VFS 가 procfs 콜백으로 라우팅 → 모든 VMA 를 순회 → cat 이 stdout 에 dump".
# 타입 스펙: type-sequence — 주체 넷 사이의 시간순 메시지. 한 줄이 VMA 하나에서 나온다는 것이 논점이다.
import sys; sys.path.insert(0, ".")
from ddk import SeqK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 976, 700

d = SeqK(W, H, "LINUX KERNEL PROGRAMMING · 07-02 §2",
         "maps 한 줄은 VMA 하나에서 나옵니다",
         "cat /proc/self/maps 의 커널 경로. read() 시스템 콜이 VFS 를 거쳐 procfs 콜백으로 라우팅되고, 콜백이 프로세스의 VMA 체인을 순회하며 매핑마다 한 줄씩 만들어 user space 로 보낸다.",
         "그래서 maps 줄 수가 곧 그 프로세스의 VMA 개수입니다")

d.lanes([("cat", "user space"), ("VFS", "kernel"), ("procfs", "pseudo fs"), ("VMA 체인", "mm->mmap")], 104, 188)

d.msg("cat", "VFS", "read()", 192, INFO, sub="시스템 콜로 커널에 들어갑니다")
d.msg("VFS", "procfs", "route", 252, MUTED, sub="파일이 아니라 콜백입니다")
d.msg("procfs", "VMA 체인", "traverse", 312, ACC, "acc", sub="red-black tree 를 순회합니다")
d.msg("VMA 체인", "procfs", "vm_start · vm_end · vm_flags · vm_file", 376, MUTED, dash="4 4")
d.selfmsg("procfs", "per VMA", 440, ACC, sub="매핑 하나가 한 줄이 됩니다")
d.msg("procfs", "cat", "copy_to_user", 500, OK, "ok", sub="한 줄씩 user space 로 넘깁니다")
d.selfmsg("cat", "write(1)", 556, OK, sub="stdout 에 그대로 dump 합니다")

d.rails(584)

d.t(24, 616, "커널 VAS 는 VMA 로 관리되지 않아 이 경로로는 안 보입니다 — 그래서 §3 이 LKM 을 씁니다.", 13, MUTED, KR, "start")

d.legend(644, [("유저 → 커널", INFO), ("VMA 순회 — 이 절의 논점", ACC), ("되돌아오는 길", OK)])
d.save("07-02.maps-read-path.svg")
print("ok 07-02.maps-read-path")
