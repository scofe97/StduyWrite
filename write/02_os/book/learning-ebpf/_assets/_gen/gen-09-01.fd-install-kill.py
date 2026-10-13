# 타입 스펙: type-sequence — 참여자 넷(cat · 커널 · Tetragon 프로그램 · tetragon 에이전트), 갈래 둘(monitor 이벤트 · enforce SIGKILL). focal 은 bpf_send_signal(SIGKILL) 한 줄.
# 사실 출처: 커널 v7.2 fs/file.c 679행 fd_install(unsigned int fd, struct file *file), include/uapi/linux/bpf.h 4231행 bpf_send_signal(u32 sig),
#   Tetragon v1.7.1 docs/content/en/docs/concepts/tracing-policy/example.md(fd_install · args index 0 int · index 1 file · matchArgs · Sigkill)·
#   mode.md(policy-mode monitor · enforce, monitoring 에서는 enforcement 동작 생략)·enforcement/_index.md(SIGKILL 은 프로세스를 동기 종료, 연산 완료까지 막는 보장은 아님),
#   selectors.md 줄 744~749(Sigkill 은 커널 BPF 코드에서 직접 실행). fd 번호 3 · cat 은 설명용 예시다.
# Layout conventions: 레인 중심 x=120·360·600·840, 메시지 stride 56~64, 갈래 구분선 y=476·608. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 13)/2}" y="{y - 23}" width="{_w(label, 13)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="18" fill="{PAPER}"/>')
            s.t(mx, y + 18, sub, 13, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 13, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 14, sub, 13, MUTED, _kr(sub), "start")


W, H = 960, 840
d = SeqKR(W, H, "LEARNING EBPF · 09-01 §5",
          "fd_install 에서 일치하면 monitor 는 알리고 enforce 는 죽인다",
          "cat 이 /etc/shadow 를 열면 커널이 file 을 채운 뒤 fd_install(3, file) 을 부르고 kprobe 가 Tetragon 프로그램을 돌린다. monitor 는 이벤트만 올려 open 이 이미 끝난 뒤 도착하고, enforce 는 같은 자리에서 SIGKILL 을 보내 사용자 공간으로 돌아가기 전에 프로세스를 끝낸다.",
          "같은 판정이 모드에 따라 이벤트 아니면 종료가 됩니다")

d.LX = {"cat": 120, "커널": 360, "프로그램": 600, "에이전트": 840}
for key, nm, sub in (("cat", "cat", "root · 사용자 공간"), ("커널", "커널", "openat · fd_install"),
                     ("프로그램", "Tetragon 프로그램", "kprobe · fd_install"), ("에이전트", "tetragon 에이전트", "사용자 공간")):
    x = d.LX[key]
    d.box(x - 100, 100, 200, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 13, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

d.msg("cat", "커널", "openat", 196, INFO, "info", sub="/etc/shadow")
d.selfmsg("커널", "file 채움", 252, MUTED, "struct file")
d.selfmsg("커널", "fd_install(3, file)", 316, MUTED, "fd 3 · file")
d.msg("커널", "프로그램", "kprobe", 380, MUTED, "ar", sub="fd_install")
d.selfmsg("프로그램", "Prefix /etc/", 436, MUTED, "matchArgs index 1")

# 갈래 A
d.line(24, 484, W - 24, 484, RULE, 0.8)
d.t(24, 506, "A · monitor", 13, INFO, KR, "start", 600)
d.msg("프로그램", "에이전트", "이벤트", 548, INFO, "info", sub="open 은 이미 끝남")

# 갈래 B
d.line(24, 596, W - 24, 596, RULE, 0.8)
d.t(24, 618, "B · enforce", 13, BAD, KR, "start", 600)
d.msg("프로그램", "커널", "bpf_send_signal(SIGKILL)", 660, ACC, "acc", sub="커널 안 · 동기")
d.msg("커널", "cat", "종료", 716, BAD, "bad", dash="5 4", sub="사용자 공간 복귀 전")

d.legend(H - 56, [("monitor", INFO), ("SIGKILL 전송", ACC), ("종료", BAD)])
d.save("09-01.fd-install-kill.svg")
