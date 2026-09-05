# 06-02 §2 — 네임스페이스 일곱이 각각 무엇을 가리고 어디에서 관측되는가.
# 원문("Linux Namespaces") 플래그 목록 축자:
#   CLONE_NEWNS      "Use for filesystem mount points. Visible via /proc/$PID/mounts. Supported since
#                     Linux 2.4.19."
#   CLONE_NEWUTS     "Use to create hostname and (NIS) domain name isolation. Visible via uname -n and
#                     hostname -f. Supported since Linux 2.6.19."
#   CLONE_NEWIPC     "... System V IPC objects or POSIX message queues. Visible via /proc/sys/fs/mqueue,
#                     /proc/sys/kernel, and /proc/sysvipc. Supported since Linux 2.6.19."
#   CLONE_NEWPID     "Use for PID number space isolation ... via /proc/$PID/status. Supported since
#                     Linux 2.6.24."
#   CLONE_NEWNET     "... network devices, IP addresses, IP routing tables, and port numbers. You can
#                     view it via ip netns list, /proc/net, and /sys/class/net. Supported since 2.6.29."
#   CLONE_NEWUSER    "Use to map UID+GIDs inside/outside the namespace ... /proc/$PID/uid_map and
#                     /proc/$PID/gid_map. Supported since Linux 3.8."
#   CLONE_NEWCGROUP  "Use to manage cgroups in a namespace ... /sys/fs/cgroup, /proc/cgroups, and
#                     /proc/$PID/cgroup. Supported since Linux 4.6."
#   저자 단서 — "Isolation in this context is mostly about what a process sees, not necessarily a hard
#   boundary (from a security perspective)."
# 타입 스펙: type-dp-security-matrix — 행(네임스페이스) × 열(무엇을 가리나 · 어디서 보나 · 커널)의
#           격자. accent 는 파드의 성립 조건이 되는 두 행 중 공유되는 쪽. 축약: 관측 경로는 저자가
#           든 것 중 대표 하나씩만 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 712
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §2",
      "일곱 개의 커튼과, 그 커튼을 확인하는 파일들",
      "네임스페이스는 온전히 자원 가시성에 관한 것이다. 무엇을 가렸는지 확인하는 방법이 "
      "거의 전부 파일을 읽는 일이라는 점이 5장과 이어진다.",
      "저자는 이 격리가 보안 관점의 단단한 경계는 아니라고 단서를 답니다")

LX, LW = 24, 208
C1, C2, C3 = 268, 240, 92
HY, RY, RH = 172, 196, 48
cols = [("무엇을 가리는가", C1), ("어디에서 보나", C2), ("커널", C3)]
x = LX + LW
for name, w in cols:
    d.t(x + w / 2, HY, name, 12, MUTED, KR, "middle", 600)
    x += w
d.line(LX, HY + 12, LX + LW + C1 + C2 + C3, HY + 12, RULE, 1)

rows = [
    ("CLONE_NEWNS", "파일시스템 마운트 지점", "/proc/$PID/mounts", "2.4.19", 0),
    ("CLONE_NEWUTS", "호스트명과 NIS 도메인명", "uname -n", "2.6.19", 0),
    ("CLONE_NEWIPC", "System V IPC · POSIX 메시지 큐", "/proc/sysvipc", "2.6.19", 0),
    ("CLONE_NEWPID", "PID 번호 공간", "/proc/$PID/status", "2.6.24", 0),
    ("CLONE_NEWNET", "장치 · IP · 라우팅 · 포트", "ip netns list", "2.6.29", 1),
    ("CLONE_NEWUSER", "안팎의 UID·GID 매핑", "/proc/$PID/uid_map", "3.8", 0),
    ("CLONE_NEWCGROUP", "네임스페이스 안의 cgroups", "/proc/$PID/cgroup", "4.6", 0),
]
for r, (flag, what, where, ver, focal) in enumerate(rows):
    y = RY + r * RH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW + C1 + C2 + C3}" height="{RH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.3"/>')
    elif r % 2 == 0:
        d.box(LX, y, LW + C1 + C2 + C3, RH, PAPER2, "none", 0, 4)
    col = ACC if focal else INK
    d.t(LX + 14, y + RH / 2 + 5, flag, 12.5, col, MONO, "start", 600)
    d.t(LX + LW + C1 / 2, y + RH / 2 + 5, what, 12, ACC if focal else MUTED, KR)
    d.t(LX + LW + C1 + C2 / 2, y + RH / 2 + 5, where, 11.5, SOFT, MONO)
    d.t(LX + LW + C1 + C2 + C3 / 2, y + RH / 2 + 5, ver, 12, OK, MONO)

BY = RY + len(rows) * RH + 12
d.line(LX, BY - 6, LX + LW + C1 + C2 + C3, BY - 6, RULE, 1)
d.o.append(f'<rect x="{LX}" y="{BY}" width="{LW + C1 + C2 + C3}" height="72" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(LX + 20, BY + 28, "파드가 성립하는 근거가 이 표의 두 줄 차이입니다", 13.5, ACC, KR, "start", 600)
d.t(LX + 20, BY + 50, "한 파드의 컨테이너들은 CLONE_NEWNET 을 공유하므로 localhost 로 서로를 부릅니다.",
    12, ACC, KR, "start")
d.t(LX + 20, BY + 68, "그런데 CLONE_NEWNS 는 공유하지 않으므로 파일시스템은 따로 봅니다.",
    11.5, MUTED, KR, "start")

d.legend(BY + 104, [("관측되는 커널 버전", OK), ("파드가 공유하는 것", ACC)])
d.save("06-02.namespaces.svg")
print("ok 06-02.namespaces")
