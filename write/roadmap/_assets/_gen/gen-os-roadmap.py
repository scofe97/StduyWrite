# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

W = 1000
SX = 500
TOP = 164
STRIDE = 156
STAGE_W = 300
STAGE_H = 64
SIDE_W = 300
SIDE_H = 92

stages = [
    (
        "1",
        "Linux 사용",
        "필수",
        INFO,
        ["셸 · 파일 · 권한", "부팅 · systemd", "journal · mount"],
        ["파일과 서비스 상태를", "명령과 로그로 확인합니다"],
    ),
    (
        "2",
        "실행 모델",
        "필수",
        INFO,
        ["process · thread · syscall", "signal · PID 1", "file descriptor · epoll"],
        ["종료와 자원 고갈을", "프로세스 상태에서 찾습니다"],
    ),
    (
        "3",
        "컨테이너 기반",
        "필수",
        INFO,
        ["namespace · cgroup v2", "OOM Killer · PSI", "mount · OverlayFS"],
        ["격리와 제한이 컨테이너를", "만드는 방식을 설명합니다"],
    ),
    (
        "4",
        "성능 분석",
        "필수",
        INFO,
        ["scheduler · run queue", "RSS · page cache", "block I/O · fsync"],
        ["병목을 사용률 · 포화 · 오류로", "분해해 원인을 찾습니다"],
    ),
    (
        "5",
        "관측과 보안",
        "추천",
        OK,
        ["/proc · perf · Ftrace", "eBPF · bpftrace", "capability · seccomp · LSM"],
        ["증상에 맞는 관측 도구와", "보안 경계를 고릅니다"],
    ),
    (
        "6",
        "커널 내부",
        "추천",
        OK,
        ["interrupt · locking · RCU", "VFS · allocator · io_uring", "KVM · crash analysis"],
        ["운영 증상을 커널 자료구조와", "실행 경로까지 연결합니다"],
    ),
]

H = TOP + STRIDE * len(stages) + 92
d = D(
    W,
    H,
    "WRITE · OS ROADMAP",
    "OS 학습 로드맵",
    "Linux 사용에서 시작해 실행 모델, 컨테이너 기반, 성능, 관측과 보안, 커널 내부로 내려가는 여섯 단계입니다.",
    "왼쪽은 핵심 키워드, 가운데는 단계, 오른쪽은 완료 기준입니다",
)

d.box(SX - 116, 96, 232, 44, PAPER2, RULE, 1.0)
d.t(SX, 123, "여섯 단계를 순서대로 봅니다", 14, INK, KR, "middle", 600)
d.line(SX, 140, SX, TOP + STRIDE * (len(stages) - 1) + STAGE_H, RULE, 1.4)

for index, (number, title, priority, color, keywords, completion) in enumerate(stages):
    y = TOP + index * STRIDE
    mid = y + STAGE_H / 2
    left_y = mid - SIDE_H / 2
    right_y = left_y

    d.line(330, mid, SX - STAGE_W / 2, mid, RULE, 1.0)
    d.line(SX + STAGE_W / 2, mid, 670, mid, RULE, 1.0)

    d.box(30, left_y, SIDE_W, SIDE_H, PAPER2, RULE, 0.9)
    d.t(46, left_y + 20, "핵심 키워드", 13, SOFT, KR, "start", 600)
    for line_index, keyword in enumerate(keywords):
        d.t(46, left_y + 42 + line_index * 18, keyword, 13, MUTED, KR, "start")

    if index == 3:
        d.tone(SX - STAGE_W / 2, y, STAGE_W, STAGE_H, ACC, 6, "14", 1.4)
    else:
        d.box(SX - STAGE_W / 2, y, STAGE_W, STAGE_H, PAPER, color, 1.2)
    d.t(SX - 128, y + 25, number, 12, color, MONO, "start", 600)
    d.t(SX + 6, y + 26, title, 15, ACC if index == 3 else INK, KR, "middle", 600)
    d.t(SX + 6, y + 49, priority, 13, color, KR)

    d.box(670, right_y, SIDE_W, SIDE_H, PAPER2, RULE, 0.9)
    d.t(686, right_y + 20, "완료 기준", 13, SOFT, KR, "start", 600)
    for line_index, line in enumerate(completion):
        d.t(686, right_y + 48 + line_index * 20, line, 13, MUTED, KR, "start")

d.legend(H - 52, [("필수", INFO), ("추천", OK), ("운영 핵심", ACC)])
d.save("os-roadmap.svg")
