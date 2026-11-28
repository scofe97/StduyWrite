# 06-02 §2 — 네임스페이스가 만들어지는 실제 길(시스템 콜 → 커널 함수)과, 그렇게 만들어진 것이
#           (호스트에 놓인 모양인 sudo lsns 출력은 gen-06-02.lsns.py 가 따로 그린다)
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
# 값: 본문 kubectl 경로·시스템 콜 셋·커널 함수 이름 그대로. sudo lsns 출력은 06-02.lsns.svg 로 옮겼다(2026-11-29).
# 타입 스펙: type-layers — 위 층(사용자 공간 → 시스템 콜 → 커널 함수)에서 만들어진 것이 아래 층(호스트의
#           실제 네임스페이스 목록)으로 쌓인다. accent 는 본문이 "실제로 태어나는 순간" 이라 한
#           create_new_namespaces() 하나.
# 축약: 관측 경로는 저자가 든 것 중 하나씩만, 커널 버전 열은 본문 표에 있어 뺐다. setns 를 부르는 쪽은
#       본문이 "기존 프로세스" 라고만 적어 도구 이름을 붙이지 않았다. lsns 출력의 kdevtmpfs·udevd 줄은 생략.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 372
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §2",
      "도구가 무엇이든 같은 커널 함수에서 태어난다",
      "runc 와 unshare 가 각각 clone()·unshare() 시스템 콜을 부르면 커널의 copy_namespaces()·"
      "unshare_nsproxy_namespaces() 를 지나 둘 다 create_new_namespaces() 로 들어간다. setns() 는 "
      "새로 만들지 않고 기존 네임스페이스에 합류한다.",
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

LY = SY + RH + 32
d.legend(LY, [("사용자 공간", MUTED), ("시스템 콜 · 커널", INFO), ("생기는 자리", ACC)])
d.save("06-02.namespaces.svg")
print("ok 06-02.namespaces", LY)
