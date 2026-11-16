# 06-02 §2 — 네임스페이스가 만들어지는 실제 길(시스템 콜 → 커널 함수)과, 그렇게 만들어진 것이
#           호스트에 실제로 어떻게 놓여 있는지(sudo lsns 출력)를 한 장에 둔다.
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
#   시스템 콜 셋 — clone(자식 프로세스), unshare(공유된 실행 컨텍스트를 떼어 냄), setns(기존 네임스페이스에 합류).
# 커널 경로(본문 각주 [^nsproxy], kernel/fork.c · kernel/nsproxy.c): clone → copy_process() →
#   copy_namespaces(), unshare → ksys_unshare() → unshare_nsproxy_namespaces(), 둘 다
#   create_new_namespaces() 로 들어간다. 본문 kubectl 경로의 마지막 사용자 공간 단계가 runc 다.
# 값: 본문 `sudo lsns` 출력 그대로 — PID 1 의 기본 일곱(NS 번호·NPROCS)과 NPROCS 1 짜리 셋.
# 타입 스펙: type-layers — 위 층(사용자 공간 → 시스템 콜 → 커널 함수)에서 만들어진 것이 아래 층(호스트의
#           실제 네임스페이스 목록)으로 쌓인다. accent 는 본문이 "실제로 태어나는 순간" 이라 한
#           create_new_namespaces() 하나.
# 축약: 관측 경로는 저자가 든 것 중 하나씩만, 커널 버전 열은 본문 표에 있어 뺐다. setns 를 부르는 쪽은
#       본문이 "기존 프로세스" 라고만 적어 도구 이름을 붙이지 않았다. lsns 출력의 kdevtmpfs·udevd 줄은 생략.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 816
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §2",
      "도구가 무엇이든 같은 커널 함수에서 태어난다",
      "runc 와 unshare 가 각각 clone()·unshare() 시스템 콜을 부르면 커널의 copy_namespaces()·"
      "unshare_nsproxy_namespaces() 를 지나 둘 다 create_new_namespaces() 로 들어간다. setns() 는 "
      "새로 만들지 않고 기존 네임스페이스에 합류한다. 아래는 sudo lsns 출력 그대로로, PID 1 이 쓰는 "
      "기본 네임스페이스 일곱과 그 번호·프로세스 수, 그리고 프로세스 하나짜리 mnt·user 네임스페이스다.",
      "보이는 것을 가리는 커튼이지 보안의 단단한 벽은 아닙니다")

# ── 위: 만드는 길 ─────────────────────────────────────────
C1, C1W = 24, 140          # 사용자 공간
C2, C2W = 196, 132         # 시스템 콜
C3, C3W = 360, 228         # 커널 함수
C4, C4W = 620, 236         # 합류 지점
R0, RS, RH = 136, 56, 44   # 행 y, stride, 높이

d.t(C1, R0 - 16, "사용자 공간", 12, SOFT, KR, "start", 600)
d.t(C2, R0 - 16, "시스템 콜", 12, SOFT, KR, "start", 600)
d.t(C3, R0 - 16, "커널 함수", 12, SOFT, KR, "start", 600)
d.line(C2 - 16, R0 - 28, C2 - 16, R0 + 2 * RS + RH + 4, SOFT, 1, "4 4")

rows = [("runc", "OCI 런타임", "clone()", "copy_namespaces()"),
        ("unshare bash", "명령 한 줄", "unshare()", "unshare_nsproxy_namespaces()"),
        ("기존 프로세스", "", "setns()", None)]
# 연결선은 글자보다 먼저 그린다
for i, (who, sub, sc, kf) in enumerate(rows):
    y = R0 + i * RS + RH / 2
    d.arrow([(C1 + C1W, y), (C2 - 4, y)], MUTED, "ar", 1.3)
    if kf:
        d.arrow([(C2 + C2W, y), (C3 - 4, y)], INFO, "info", 1.3)
        d.arrow([(C3 + C3W, y), (C4 - 4, y)], ACC, "acc", 1.4)
    else:
        d.arrow([(C2 + C2W, y), (C4 - 4, y)], MUTED, "ar", 1.3, "5 4")

for i, (who, sub, sc, kf) in enumerate(rows):
    y = R0 + i * RS
    d.box(C1, y, C1W, RH, PAPER2, MUTED, 1.0, 6)
    fam = KR if any('가' <= ch <= '힣' for ch in who) else MONO
    if sub:
        d.t(C1 + C1W / 2, y + 19, who, 13, INK, fam, "middle", 600)
        d.t(C1 + C1W / 2, y + 36, sub, 11, MUTED, KR)
    else:
        d.t(C1 + C1W / 2, y + 27, who, 13, INK, fam, "middle", 600)
    d.tone(C2, y, C2W, RH, INFO)
    d.t(C2 + C2W / 2, y + 27, sc, 13, INFO, MONO, "middle", 600)
    if kf:
        d.box(C3, y, C3W, RH, PAPER2, INFO, 1.0, 6)
        d.t(C3 + C3W / 2, y + 27, kf, 12, INK, MONO)

# 합류 지점: 위 두 행을 덮는 focal, 아래 행은 기존 네임스페이스
FY, FH = R0, RS + RH
d.o.append(f'<rect x="{C4}" y="{FY}" width="{C4W}" height="{FH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(C4 + C4W / 2, FY + 40, "create_new_namespaces()", 13, ACC, MONO, "middle", 600)
d.t(C4 + C4W / 2, FY + 62, "새 네임스페이스가 생기는 곳", 12, INK, KR)
SY = R0 + 2 * RS
d.o.append(f'<rect x="{C4}" y="{SY}" width="{C4W}" height="{RH}" rx="6" fill="none" '
           f'stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="5 4"/>')
d.t(C4 + C4W / 2, SY + 27, "기존 네임스페이스에 합류", 12, MUTED, KR)

# ── 아래: 호스트에 실제로 있는 네임스페이스 (sudo lsns) ────────────
TY = SY + RH + 48
d.t(24, TY, "PID 1 /sbin/init 의 네임스페이스 일곱", 13, INK, KR, "start", 600)
d.t(W - 24, TY, "sudo lsns", 12, SOFT, MONO, "end")
XT, XN, XP, XF, XW, XO = 32, 88, 236, 256, 404, 644
HY = TY + 28
for x, lab, a in ((XT, "TYPE", "start"), (XN, "NS", "start"), (XP, "NPROCS", "end"),
                  (XF, "clone 플래그", "start"), (XW, "가리는 것", "start"), (XO, "어디서 보나", "start")):
    d.t(x, HY, lab, 11, SOFT, KR if any('가' <= ch <= '힣' for ch in lab) else MONO, a, 600)
d.line(24, HY + 10, W - 24, HY + 10, RULE, 1)

ns = [("cgroup", "4026531835", "251", "CLONE_NEWCGROUP", "네임스페이스 안의 cgroups", "/proc/$PID/cgroup"),
      ("pid", "4026531836", "245", "CLONE_NEWPID", "PID 번호 공간", "/proc/$PID/status"),
      ("user", "4026531837", "245", "CLONE_NEWUSER", "안팎의 UID·GID 매핑", "/proc/$PID/uid_map"),
      ("uts", "4026531838", "251", "CLONE_NEWUTS", "호스트명 · NIS 도메인명", "uname -n"),
      ("ipc", "4026531839", "251", "CLONE_NEWIPC", "System V IPC · 메시지 큐", "/proc/sysvipc"),
      ("mnt", "4026531840", "241", "CLONE_NEWNS", "파일시스템 마운트 지점", "/proc/$PID/mounts"),
      ("net", "4026531992", "244", "CLONE_NEWNET", "장치 · IP · 라우팅 · 포트", "/proc/net")]
RY, RR = HY + 16, 32
for i, (ty, no, np, fl, what, where) in enumerate(ns):
    y = RY + i * RR
    if i % 2 == 0:
        d.box(24, y, W - 48, RR, PAPER2, "none", 0, 4)
    by = y + RR / 2 + 5
    d.t(XT, by, ty, 12.5, INK, MONO, "start", 600)
    d.t(XN, by, no, 12, INFO, MONO, "start")
    d.t(XP, by, np, 12, MUTED, MONO, "end")
    d.t(XF, by, fl, 12, MUTED, MONO, "start")
    d.t(XW, by, what, 12, INK, KR, "start")
    d.t(XO, by, where, 12, SOFT, MONO, "start")

# NPROCS 1 짜리 — 같은 종류의 다른 칸
OY = RY + len(ns) * RR + 36
d.t(24, OY, "같은 종류의 다른 칸 — 프로세스 하나짜리", 13, INK, KR, "start", 600)
one = [("mnt", "4026532316", "1", "684", "systemd-timesync"),
       ("mnt", "4026532491", "1", "688", "systemd-resolve"),
       ("user", "4026532250", "1", "5319", "/opt/google/chrome/nacl_he")]
for i, (ty, no, np, pid, cmd) in enumerate(one):
    y = OY + 14 + i * RR
    d.o.append(f'<rect x="24" y="{y}" width="{W - 48}" height="{RR - 4}" rx="4" '
               f'fill="{WARN}0D" stroke="{WARN}" stroke-width="0.8"/>')
    by = y + (RR - 4) / 2 + 5
    d.t(XT, by, ty, 12.5, WARN, MONO, "start", 600)
    d.t(XN, by, no, 12, INFO, MONO, "start")
    d.t(XP, by, np, 12, MUTED, MONO, "end")
    d.t(XF, by, f"PID {pid}", 12, MUTED, MONO, "start")
    d.t(XW, by, cmd, 12, INK, MONO, "start")

LY = OY + 14 + len(one) * RR + 16
d.legend(LY, [("사용자 공간", MUTED), ("시스템 콜 · 커널", INFO), ("생기는 자리", ACC),
              ("프로세스 하나짜리", WARN)])
d.save("06-02.namespaces.svg")
print("ok 06-02.namespaces", LY)
