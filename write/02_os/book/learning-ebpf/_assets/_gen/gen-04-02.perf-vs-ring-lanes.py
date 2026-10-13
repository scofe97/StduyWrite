# 타입 스펙: type-swimlane — 레인 둘(perf 버퍼 · 링 버퍼)에 같은 방향으로 호출 네 단계를 늘어놓아, CPU 마다 반복되는 앞 세 단계와 한 번뿐인 앞 세 단계를 맞대 본다.
# 사실 출처: 추출본 ebpf4.txt 721~772행(perf_event_open ×4 · ioctl ENABLE ×4 · BPF_MAP_UPDATE_ELEM map_fd=4 ×4 · ppoll([{fd=8…}…{fd=11…}], 4, …)),
#   826~827행(BPF_MAP_CREATE RINGBUF key_size=0 max_entries=4096 … = 4), 867·876·884행(epoll_create1 = 8 · epoll_ctl(8, EPOLL_CTL_ADD, 4, …) · epoll_pwait(8, …)).
#   BCC v0.37.0 src/cc/export/helpers.h 232~248행(max_entries = 페이지 수 × PAGE_SIZE).
# Layout conventions: 단계 폭 168·높이 72, 단계 x=164·360·556·752(stride 196), 레인 y=132·316(band 160~180), 레인 라벨 열 x=24~140, 반복 고리는 마지막 단계 아래 ㄷ자. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 548
d = D(W, H, "LEARNING EBPF · 04-02 §3",
      "perf 버퍼는 호출이 CPU 마다 반복되고 링 버퍼는 한 번이다",
      "perf 버퍼는 perf_event_open · ioctl ENABLE · BPF_MAP_UPDATE_ELEM 이 CPU 수만큼 반복되고 ppoll 이 fd 네 개를 매번 넘긴다. 링 버퍼는 맵을 만들고 epoll 에 한 번 등록한 뒤 epoll_pwait 로 기다린다.",
      "같은 일을 하는 두 길의 호출 수")

XS = (164, 360, 556, 752)
SW, SH = 168, 72
LY = (132, 316)

# 레인 구분선과 라벨
for y in (112, 272, 452):
    d.line(24, y, W - 24, y, RULE, 0.8)
for ly, name, sub in ((LY[0], "perf 버퍼", "CPU 마다 링 하나"), (LY[1], "링 버퍼", "맵 하나")):
    d.t(24, ly + 30, name, 13, INK, KR, "start", 600)
    d.t(24, ly + 52, sub, 13, MUTED, KR, "start")


def step(x, y, title, sub, c):
    d.tone(x, y, SW, SH, c, 6, "12", 1.2)
    d.t(x + SW / 2, y + 32, title, 12, c, MONO, "middle", 600)
    d.t(x + SW / 2, y + 54, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


def link(y):
    for i in range(3):
        d.arrow([(XS[i] + SW + 2, y + SH // 2), (XS[i + 1] - 6, y + SH // 2)], MUTED, "ar", 1.5)


def repeat(y, label, c):
    x1, x0 = XS[3] + 120, XS[3] + 48
    yb = y + SH
    d.arrow([(x1, yb + 2), (x1, yb + 24), (x0, yb + 24), (x0, yb + 6)], c, "info", 1.4, "5 4")
    d.chip((x0 + x1) / 2, yb + 42, label, c, 13)


y1, y2 = LY
link(y1); link(y2)
step(XS[0], y1, "perf_event_open", "× 4 · fd 8~11", WARN)
step(XS[1], y1, "PERF_EVENT_IOC_ENABLE", "× 4", WARN)
step(XS[2], y1, "BPF_MAP_UPDATE_ELEM", "map_fd=4 · × 4", WARN)
step(XS[3], y1, "ppoll", "fd 8·9·10·11", INFO)
repeat(y1, "반복 · fd 4개 전달", INFO)

step(XS[0], y2, "BPF_MAP_CREATE", "4096 → fd 4", OK)
step(XS[1], y2, "epoll_create1", "= fd 8", OK)
step(XS[2], y2, "epoll_ctl", "ADD fd 4 · 한 번", ACC)
step(XS[3], y2, "epoll_pwait", "epoll fd 8", INFO)
repeat(y2, "반복 · fd 8 만 전달", INFO)

d.legend(H - 56, [("CPU 마다 × 4", WARN), ("한 번", OK), ("fd 등록", ACC), ("대기 호출", INFO)])
d.save("04-02.perf-vs-ring-lanes.svg")
