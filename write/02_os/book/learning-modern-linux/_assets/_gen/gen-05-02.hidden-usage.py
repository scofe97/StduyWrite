# 05-02 §7 — 삭제된 파일을 프로세스가 열고 있을 때 VFS 구조와 df/du 불일치.
# 타입 스펙: type-data-flow — 프로세스 fd -> Inode -> 데이터 블록 참조가 유지되어
#           du(디렉터리 트리 순회)는 1M, df(슈퍼블록 블록 카운트)는 65M 로 어긋나는 구조.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §7",
      "열린 파일 삭제 시 VFS 참조 유지와 df · du 불일치",
      "rm 은 디렉터리 항목(dentry)만 지우고 i_nlink 를 0 으로 만듭니다. "
      "프로세스(PID 4462)가 fd 3 으로 inode 를 참조하고 있으면 블록(64MiB)이 반환되지 않아 df 와 du 가 어긋납니다.",
      "실측: big (64MiB) 삭제 후 du 1M vs df 65M, : > /proc/PID/fd/3 으로 공간 즉시 회수")

# 상단: 프로세스 영역
PX, PY, PW, PH = 40, 120, 360, 140
d.box(PX, PY, PW, PH, PAPER2, INFO, 1.2, 8)
d.t(PX + 20, PY + 28, "프로세스 (PID 4462 : tail -f)", 13.5, INFO, KR, "start", 600)
d.t(PX + 20, PY + 52, "열린 파일 디스크립터 (File Table)", 11, SOFT, KR, "start")
d.o.append(f'<rect x="{PX + 16}" y="{PY + 66}" width="{PW - 32}" height="32" rx="5" '
           f'fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>')
d.t(PX + 28, PY + 87, "fd 3 -> /mnt/h/big (deleted)", 11.5, WARN, MONO, "start")
d.t(PX + 20, PY + 120, "procfs 가 (deleted) 로 표시하며 오픈 참조(i_count >= 1) 유지", 11, MUTED, KR, "start")

# 상단 우측: 관측 도구 관점 (du vs df)
OX, OY, OW, OH = 440, 120, 400, 140
d.box(OX, OY, OW, OH, PAPER2, ACC, 1.2, 8)
d.t(OX + 20, OY + 28, "관측 도구의 측정 기준 차이 (실측값)", 13.5, ACC, KR, "start", 600)
d.line(OX + 14, OY + 38, OX + OW - 14, OY + 38, RULE, 1)

# du 설명
d.t(OX + 20, OY + 60, "du -sm /mnt/h : 1M", 13, OK, MONO, "start", 600)
d.t(OX + 20, OY + 79, "디렉터리 트리를 돌며 셈 — 이름이 지워진 파일은 못 셈", 11, MUTED, KR, "start")

# df 설명
d.t(OX + 20, OY + 104, "df -BM /mnt/h : 65M Used", 13, BAD, MONO, "start", 600)
d.t(OX + 20, OY + 123, "파일시스템의 할당 블록 수 — 아직 점유 중인 블록까지 셈", 11, MUTED, KR, "start")

# 중간/하단: VFS 객체 3개 (Dentry, Inode, Data Blocks)
VY = 290
VW = 240
VH = 140

# 1. Dentry (삭제됨)
D1X = 40
d.box(D1X, VY, VW, VH, PAPER2, BAD, 1.2, 8)
d.t(D1X + 20, VY + 28, "디렉터리 엔트리 (dentry)", 13, BAD, KR, "start", 600)

d.t(D1X + 20, VY + 50, "/mnt/h/big", 11, INK, MONO, "start")
d.line(D1X + 14, VY + 62, D1X + VW - 14, VY + 62, RULE, 1)
d.t(D1X + 20, VY + 84, "상태: rm 에 의해 제거됨", 11, BAD, KR, "start", 600)
d.t(D1X + 20, VY + 104, "ls 에 보이지 않음", 11, MUTED, KR, "start")
d.t(D1X + 20, VY + 122, "i_nlink = 0 (하드링크 제거)", 11, SOFT, MONO, "start")

# 2. Inode (열려있음)
D2X = 320
d.box(D2X, VY, VW, VH, PAPER2, WARN, 1.2, 8)
d.t(D2X + 20, VY + 28, "아이노드 (inode)", 13, WARN, KR, "start", 600)
d.t(D2X + 20, VY + 50, "ext4 Inode (i_count >= 1)", 11, INK, MONO, "start")
d.line(D2X + 14, VY + 62, D2X + VW - 14, VY + 62, RULE, 1)
d.t(D2X + 20, VY + 84, "파일 메타데이터 및 블록 포인터 유지", 11, INK, KR, "start")
d.t(D2X + 20, VY + 104, "프로세스 참조 중이므로 메모리 상주", 11, MUTED, KR, "start")
d.t(D2X + 20, VY + 122, "마지막 fd 가 닫힐 때 블록 해제", 11, SOFT, KR, "start")

# 3. Data Blocks (점유 지속)
D3X = 600
d.box(D3X, VY, VW, VH, PAPER2, BAD, 1.2, 8)
d.t(D3X + 20, VY + 28, "데이터 블록 (Blocks)", 13, BAD, KR, "start", 600)
d.t(D3X + 20, VY + 50, "64 MiB (67,108,864 바이트)", 11, INK, MONO, "start")
d.line(D3X + 14, VY + 62, D3X + VW - 14, VY + 62, RULE, 1)
d.t(D3X + 20, VY + 84, "비트맵상 할당(Allocated) 상태 유지", 11, INK, KR, "start")
d.t(D3X + 20, VY + 104, "free 블록 수로 돌아가지 않음", 11, MUTED, KR, "start")
d.t(D3X + 20, VY + 122, "디스크 용량 반환되지 않음 (df 65M)", 11, BAD, KR, "start")

# 화살표 연결: 프로세스 -> inode
d.arrow([(360, PY + PH), (360, VY - 2)], WARN, "warn", 1.4)
d.t(370, PY + PH + 19, "오픈 참조 (fd 3)", 11, WARN, KR, "start")

# 화살표: inode -> data blocks
d.arrow([(D2X + VW, VY + VH / 2), (D3X - 2, VY + VH / 2)], BAD, "bad", 1.4)
d.t((D2X + VW + D3X) / 2, VY + VH / 2 - 8, "포인터", 11, MUTED, KR, "middle")

# 하단 해결 조치 박스
SY = 456
d.box(40, SY, W - 80, 72, PAPER2, OK, 1.2, 8)
d.t(56, SY + 24, "해결 조치: 버려도 되는 내용이면 fd 로 비워 즉시 회수 (실측)", 13, OK, KR, "start", 600)
d.t(56, SY + 46, "명령: : > /proc/4462/fd/3", 11.5, INK, MONO, "start")
d.t(56, SY + 64, "결과: 크기 67108864 -> 0 바이트, df Used 65M -> 1M (프로세스를 죽이지 않고)", 11, OK, KR, "start")

d.legend(552, [("오픈 참조 유지 (누수 원인)", WARN), ("삭제 / 미반환 블록", BAD), ("즉시 회수 조치", OK)])
d.save("05-02.hidden-usage.svg")
print("ok 05-02.hidden-usage")
