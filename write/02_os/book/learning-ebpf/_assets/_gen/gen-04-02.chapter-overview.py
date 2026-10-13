# 타입 스펙: type-architecture — 사용자 공간 fd 와 커널 대상을 세 줄(부착 · perf 버퍼판 · 링 버퍼판)로 대응시키고, 둘을 잇는 호출 이름을 화살표 위에 단다.
# 사실 출처: 추출본 ebpf4.txt 640~710행(fd 6 hello · fd 7 kprobe perf 이벤트 · ioctl SET_BPF), 714~780행(fd 8~11 perf 링 · map_fd=4 · ppoll),
#   826~893행(링 버퍼 맵 fd 4 · max_entries=4096 · epoll fd 8 · epoll_ctl · epoll_pwait), 250~251행(output max_entries=4).
#   예제 저장소 chapter4/hello-buffer-config.py · hello-ring-buffer-config.py (HEAD 232a36a)
# Layout conventions: 노드 폭 256·높이 64, 존 둘(사용자 · 커널) 폭 288, 줄 stride 136(y=148·284·420), 화살표 y 는 줄 상단 +24(→)·+48(←). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 596
d = D(W, H, "LEARNING EBPF · 04-02",
      "fd 6·7·8~11 이 커널 대상과 만나는 세 줄",
      "kprobe 는 fd 7 에 ioctl 로 프로그램 6 을 붙이고, perf 버퍼판은 CPU 마다 링을 맵 fd 4 에 꽂고 ppoll 로 기다리며, 링 버퍼판은 맵 fd 4 를 epoll 인스턴스 fd 8 에 등록한다.",
      "붙이는 줄 하나와 받는 줄 둘")

UZ = (16, 84, 288, 416)    # 사용자 공간
KZ = (656, 84, 288, 416)   # 커널
for (x, y, w, h), name in ((UZ, "USER SPACE"), (KZ, "KERNEL")):
    d.box(x, y, w, h, PAPER2, RULE, 0.9, 8)
    d.t(x + 12, y + 20, name, 9, SOFT, MONO, "start")

NW, NH = 256, 64
UX, KX = 32, 672
ROWS = (148, 284, 420)


def node(x, y, title, sub, c):
    d.tone(x, y, NW, NH, c, 6, "12", 1.2)
    d.t(x + NW / 2, y + 28, title, 14, c, KR if any("가" <= ch <= "힣" for ch in title) else MONO, "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


def tag(y, txt):
    d.t(UX, y - 12, txt, 13, MUTED, KR, "start", 600)


# 줄 A — 부착
ya = ROWS[0]
tag(ya, "부착")
node(UX, ya, "fd 7 · kprobe 이벤트", "fd 6 · hello 프로그램", OK)
node(KX, ya, "execve kprobe", "type=6 · 동적 PMU", INFO)
d.arrow([(UX + NW + 2, ya + 32), (KX - 6, ya + 32)], ACC, "acc", 1.8)
d.chip(480, ya + 12, "ioctl(7, PERF_EVENT_IOC_SET_BPF, 6)", ACC, 12)

# 줄 B — perf 버퍼판
yb = ROWS[1]
tag(yb, "perf 버퍼판")
node(UX, yb, "fd 8~11 · perf 링", "CPU 0~3 마다 하나", OK)
node(KX, yb, "output 맵 · fd 4", "PERF_EVENT_ARRAY · 칸 4", INFO)
d.arrow([(UX + NW + 2, yb + 24), (KX - 6, yb + 24)], MUTED, "ar", 1.5)
d.chip(480, yb + 8, "BPF_MAP_UPDATE_ELEM map_fd=4", MUTED, 12)
d.arrow([(KX - 2, yb + 48), (UX + NW + 6, yb + 48)], INFO, "info", 1.5)
d.chip(480, yb + 66, "ppoll", INFO, 12)

# 줄 C — 링 버퍼판
yc = ROWS[2]
tag(yc, "링 버퍼판")
node(UX, yc, "fd 8 · epoll 인스턴스", "fd 4 를 등록", OK)
node(KX, yc, "output 맵 · fd 4", "RINGBUF · 4096", INFO)
d.arrow([(UX + NW + 2, yc + 24), (KX - 6, yc + 24)], MUTED, "ar", 1.5)
d.chip(480, yc + 8, "epoll_ctl(8, EPOLL_CTL_ADD, 4)", MUTED, 12)
d.arrow([(KX - 2, yc + 48), (UX + NW + 6, yc + 48)], INFO, "info", 1.5)
d.chip(480, yc + 66, "epoll_pwait(8)", INFO, 12)

d.legend(H - 56, [("사용자 공간 fd", OK), ("커널 대상", INFO), ("부착 호출", ACC)])
d.save("04-02.chapter-overview.svg")
