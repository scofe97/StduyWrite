# 타입 스펙: type-architecture — 존 둘(사용자 공간 · 커널), 커널 안 판정 지점 셋, 오른쪽 결과 네 갈래. focal 은 LSM 훅.
# 사실 출처: 커널 v7.2 arch/x86/entry/syscalls/syscall_64.tbl 줄 269(257 openat)·280(268 fchmodat),
#   include/linux/entry-common.h 136~141행(입구 작업 순서: __secure_computing → trace_sys_enter),
#   fs/file.c 679행 fd_install, fs/open.c 632행 security_path_chmod, 예제 SEC("lsm/path_chmod")(추출본 src/ebpf9.txt 361~366행),
#   Tetragon v1.7.1 docs/content/en/docs/concepts/tracing-policy/example.md(fd_install · Sigkill), enforcement/_index.md(SIGKILL 동기 종료).
# Layout conventions: 존 x=24·264·776, 호출 행 중심 y=180·324, 판정 상자 w=200, 결과 상자 w=160. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 09-01",
      "openat 과 fchmodat 이 내려가는 길 위의 판정 지점 셋",
      "syscall 입구는 인자를 읽어도 커널이 읽을 때 바뀔 수 있다. fd_install 은 파일 구조체가 채워진 뒤, security_path_chmod 는 inode 를 바꾸기 직전에 불린다. 결과는 허용 · EPERM · SIGKILL · 이벤트 넷이다.",
      "같은 호출을 어느 자리에서 보느냐가 막을 수 있는지를 가른다")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#F5F5F3" fill-opacity="0.025" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(x + 12, y + 20, label, 9, SOFT, MONO, "start")


def node(x, y, w, h, title, sub, c, fam=MONO, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}1F" stroke="{c}" stroke-width="1.4"/>')
    else:
        d.tone(x, y, w, h, c, 6, "12", 1.2)
    ty = y + 28 if sub else y + h // 2 + 5
    d.t(x + w / 2, ty, title, 13, c, fam, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 48, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


zone(24, 108, 200, 320, "USER SPACE")
zone(264, 108, 488, 320, "KERNEL")
zone(776, 108, 160, 320, "OUTCOME")

# 호출 행 — 중심 y = 180, 324
node(40, 148, 168, 64, "openat", "257 · /etc/shadow", INFO)
node(40, 292, 168, 64, "fchmodat", "268 · 0777", INFO)

# 판정 지점
d.tone(280, 156, 200, 180, WARN, 6, "12", 1.2)
d.t(380, 184, "1 · syscall 입구", 13, WARN, KR, "middle", 600)
d.t(380, 210, "seccomp-bpf", 13, INK, MONO)
d.t(380, 230, "값 인자 판정", 13, MUTED, KR)
d.line(292, 244, 468, 244, RULE, 0.8)
d.t(380, 266, "raw_syscalls:sys_enter", 13, INK, MONO)
d.t(380, 286, "syscall 추적 도구", 13, MUTED, KR)
d.chip(380, 316, "인자 복사 전", WARN, 13)

node(520, 148, 200, 64, "fd_install", "2 · Tetragon kprobe", OK)
node(520, 292, 200, 64, "security_path_chmod", "3 · lsm/path_chmod", ACC, MONO, True)

# 결과
node(776, 148, 160, 48, "SIGKILL", None, BAD)
node(776, 212, 160, 56, "이벤트", "사용자 공간 · SIEM", INFO, KR)
node(776, 292, 160, 48, "EPERM", None, BAD)
node(776, 364, 160, 48, "허용", None, OK, KR)

# 화살표
d.arrow([(208, 180), (274, 180)], MUTED, "ar", 1.4)
d.arrow([(208, 324), (274, 324)], MUTED, "ar", 1.4)
d.arrow([(480, 180), (514, 180)], MUTED, "ar", 1.4)
d.arrow([(480, 324), (514, 324)], MUTED, "ar", 1.4)
d.arrow([(722, 172), (770, 172)], BAD, "bad", 1.5)
d.arrow([(722, 200), (748, 200), (748, 240), (770, 240)], INFO, "info", 1.5)
d.arrow([(722, 316), (770, 316)], BAD, "bad", 1.5)
d.arrow([(722, 340), (748, 340), (748, 388), (770, 388)], OK, "ok", 1.5)

d.legend(H - 56, [("인자 복사 전", WARN), ("커널 함수", OK), ("LSM 훅", ACC), ("차단", BAD), ("이벤트", INFO)])
d.save("09-01.chapter-overview.svg")
