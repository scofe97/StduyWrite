# 06-02 §2 — 호스트에 실제로 놓인 네임스페이스(sudo lsns 출력)를 PID 1 의 기본 일곱과
#           프로세스 하나짜리로 나눠 보인다. 만들어지는 길은 06-02.namespaces.svg 가 맡는다.
# 값: 본문 `sudo lsns` 출력 그대로 — PID 1 의 기본 일곱(NS 번호·NPROCS)과 NPROCS 1 짜리 셋.
#   clone 플래그·가리는 것은 본문 플래그 표(원문 "Linux Namespaces" 목록)에서 한 줄씩만 옮겼다. 어디서 보나 열은 본문 표에 있어 뺐다.
# 타입 스펙: type-layers — 행을 위(PID 1 의 일곱)에서 아래(프로세스 하나짜리)로 쌓은 두 묶음. 행마다 같은 칸을 채운다.
#           accent 는 쓰지 않고 프로세스 하나짜리 행만 WARN 으로 구분한다.
# 축약: lsns 출력의 kdevtmpfs·udevd 줄은 생략했다. 관측 경로 열은 본문 표와 겹쳐 뺐다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 586
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §2",
      "PID 1 의 일곱 칸과 프로세스 하나짜리 칸",
      "sudo lsns 출력 그대로다. PID 1 이 쓰는 기본 네임스페이스 일곱은 NPROCS 가 240 을 넘고, "
      "systemd-timesync·systemd-resolve 의 mnt 와 크롬의 user 는 프로세스 하나짜리 네임스페이스다.",
      "컨테이너 없이도 네임스페이스는 이미 여기저기 쓰이고 있습니다")

# ── 아래: 호스트에 실제로 있는 네임스페이스 (sudo lsns) ────────────
TY = 116
d.t(24, TY, "PID 1 /sbin/init 의 네임스페이스 일곱", 13, INK, KR, "start", 600)
d.t(W - 24, TY, "sudo lsns", 12, SOFT, MONO, "end")
XT, XN, XP, XF, XW, XO = 32, 88, 236, 256, 404, 644
HY = TY + 28
for x, lab, a in ((XT, "TYPE", "start"), (XN, "NS", "start"), (XP, "NPROCS", "end"),
                  (XF, "clone 플래그", "start"), (XW, "가리는 것", "start")):
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
d.legend(LY, [("PID 1 의 일곱", INFO), ("프로세스 하나짜리", WARN)])
d.save("06-02.lsns.svg")
print("ok 06-02.lsns", LY)
