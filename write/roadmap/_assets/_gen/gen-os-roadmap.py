# write/roadmap/os-roadmap.md §학습 순서 — OS 학습 로드맵.
# 판형은 data-roadmap 과 같다 — 세로 척추에 국면과 단계를 걸고, 왼쪽에 배우는 개념을,
#   오른쪽에 자료가 다루지 않는 키워드를 뻗는다.
#
# 자료가 두 종류다. 정독 노트가 있는 자리(LML·SysPerf·Container Security·LKP)와
#   소장본만 있고 노트가 없는 자리(How Linux Works·OSC·Learning eBPF·KVM)다.
#   출처의 SSOT 는 본문 §책 읽기 흐름 표이고, 도식은 부제 mono 슬롯으로만 가리킨다.
#
# 절단선은 3단계 뒤에 긋는다 — 1~3 이 컨테이너가 서는 바닥이고 4 부터가 "왜 느린가"다.
#   본문이 "3단계까지가 왜 멈췄나라면 여기는 왜 느린가"라고 적은 자리라 이 선이 편집상 논점이다.
# 타입 스펙: type-tree — 부모(국면)에서 자식(단계)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 48
CH_W, CH_H, CH_GAP = 256, 32, 8
BUS, ROW_GAP, PHASE_GAP = 190, 40, 36
NOTE_H = 76

BADGE = {"필수": INFO, "추천": OK, "선택": SOFT}

# (제목, 부제 mono, 배지, 왼쪽 개념, 오른쪽 자료 밖 키워드, 점선 여부)
# (제목, 부제 mono, 배지, 왼쪽 개념, 오른쪽 자료 밖 키워드, 점선 여부)
phases = [
    ("기반", "1~3단계", INFO, [
        ("1 · Linux 사용", "LML 1~6장 · 노트 16편", "필수",
         ["셸 · 스트림 · 종료 상태",
          "파일 · 권한 · 리다이렉션",
          "모든 것이 파일 — VFS · mount",
          "부팅 · initramfs · systemd",
          "journal · 서비스 의존"],
         ["systemd-analyze", "core dump 저장 경로"], False),

        ("2 · 실행 모델", "kernel 01-01 · SysPerf 3장", "필수",
         ["유저 · 커널 스페이스",
          "시스템 콜 · strace",
          "process · thread · task 구조",
          "signal · 종료 코드 · PID 1",
          "file descriptor · epoll"],
         ["prctl · PR_SET_PDEATHSIG", "vfork · clone3"], False),

        ("3 · 컨테이너 기반", "kernel 01-02~01-07 · 노트 7편", "필수",
         ["namespace 여덟 · unshare",
          "cgroup v2 · PSI · throttling",
          "memory.max · OOM Killer",
          "mount propagation",
          "OverlayFS · user namespace"],
         ["cgroup namespace", "hugetlbfs"], False),
    ]),

    ("자원과 관측", "4~5단계", ACC, [
        ("4 · 성능 분석", "SysPerf 2·6~9장 · 노트 53편", "필수",
         ["USE · RED · 드릴다운",
          "run queue · CFS · context switch",
          "RSS · page cache · swap",
          "block I/O · IOPS · fsync",
          "사용률 · 포화 · 오류 분해"],
         ["blk-cgroup · io.max", "IRQ affinity · irqbalance"], False),

        ("5 · 관측과 보안", "SysPerf 4·13~15장 · CS 2·8·9장", "추천",
         ["/proc · /sys · sar",
          "perf · Ftrace · tracepoint",
          "eBPF · BCC · bpftrace",
          "capability · seccomp",
          "AppArmor · SELinux · rootless"],
         ["Landlock", "eBPF verifier 거절 조건"], False),
    ]),

    ("커널 내부", "6단계", OK, [
        ("6 · 커널 내부", "LKP 6~13장 · 노트 32편", "추천",
         ["VAS · 주소 변환 · KASLR",
          "페이지 할당자 · slab",
          "demand paging · OOM killer",
          "스케줄링 클래스 · CFS 구현",
          "spinlock · atomic · lockdep"],
         ["kdump · crash 분석", "io_uring 제출 · 완료 큐"], False),
    ]),
]

NOTES = {
    "기반":
        "Pod 가 137 로 죽으면 3단계, 서비스가 안 뜨면 1단계가 첫 자리다. 번호는 의존 순서이지 진도가 아니다.",
    "자원과 관측":
        "SysPerf 53편은 통독을 전제하지 않는다. 방법론 2장과 자원별 네 장이 4단계의 몫이다.",
    "커널 내부":
        "정독 노트가 13장 동기화에서 멈춘다. VFS·io_uring·LSM·KVM 은 오른쪽 칩이 가리키는 자리다.",
}
CUT_AFTER = "기반"


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 24


ROOT_Y = 116 + 180
y = ROOT_Y + 48 + PHASE_GAP
for name, _s, _c, steps in phases:
    y += NODE_H + ROW_GAP
    for st in steps:
        y += row_h(st[3], st[4]) + ROW_GAP
    if NOTES.get(name):
        y += NOTE_H
    y += PHASE_GAP - ROW_GAP
    if name == CUT_AFTER:
        y += 56
H = y + 80

d = D(W, H, "WRITE · OS ROADMAP",
      "OS 학습 로드맵",
      "Linux 운영에서 시작해 실행 모델과 격리로 내려간 뒤 성능·관측·커널 내부로 이어진다. 척추에 "
      "국면 셋과 단계 여섯을 걸고, 배우는 개념을 왼쪽에 자료가 다루지 않는 키워드를 오른쪽에 "
      "뻗었다. 1~3단계가 컨테이너가 서는 바닥이고 4단계부터가 왜 느린가를 재는 축이다.",
      "1~3 은 왜 멈췄나, 4 부터는 왜 느린가입니다. 번호는 의존 순서이지 진도가 아닙니다")

LX, LY, LW, LH = 40, 96, 336, 180
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만")]):
    cy = LY + 56 + i * 28
    c = BADGE[lab]
    d.o.append(f'<rect x="{LX + 16}" y="{cy - 9}" width="34" height="17" rx="4" '
               f'fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(LX + 33, cy + 3, lab, 11, c, KR)
    d.t(LX + 60, cy + 3, txt, 13, MUTED, KR, "start")
d.t(LX + 16, LY + 148, "왼쪽 — 배우는 개념 · 오른쪽 — 자료 밖 키워드", 12, SOFT, KR, "start")
d.t(LX + 16, LY + 166, "부제 — 그 단계가 쓰는 자료와 장 범위", 12, SOFT, KR, "start")

RX, RY, RW, RH = 624, 96, 336, 180
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("network-roadmap", "netns 이후의 패킷 경로"),
        ("k8s-roadmap", "오브젝트 배포와 클러스터 운영"),
        ("07_devops", "이미지 포맷과 OCI 표준"),
        ("LKP 1~5장", "커널 빌드와 모듈 개발 환경")]):
    cy = RY + 56 + i * 32
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 48, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 30, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 48, SX, H - 116, RULE, 1.4)


def draw_step(title, sub, badge, left, right, dashed, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        if not items:
            continue
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, label in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * 14) - (CH_W if side == "left" else 0)
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * 14, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.t(bx + CH_W / 2, cy + 5, label, 12, MUTED, KR, "middle")
    if dashed:
        d.o.append(f'<rect x="{SX - NODE_W/2}" y="{mid - NODE_H/2}" width="{NODE_W}" '
                   f'height="{NODE_H}" rx="6" fill="{PAPER}" stroke="{SOFT}" '
                   f'stroke-width="1.0" stroke-dasharray="4 4"/>')
    else:
        d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, RULE, 1.0)
    c = BADGE[badge]
    d.o.append(f'<rect x="{SX - NODE_W/2 + 12}" y="{mid - NODE_H/2 + 8}" width="34" height="17" '
               f'rx="4" fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(SX - NODE_W / 2 + 29, mid - NODE_H / 2 + 20, badge, 11, c, KR)
    d.t(SX + 12, mid - 4, title, 13, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, MONO)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


def draw_phase(name, stage, color, steps, y):
    if color is ACC:
        d.tone(SX - NODE_W / 2, y, NODE_W, NODE_H, ACC, 6, "16", 1.4)
    else:
        d.box(SX - NODE_W / 2, y, NODE_W, NODE_H, PAPER, color, 1.2)
    d.t(SX, y + 22, name, 15, ACC if color is ACC else INK, KR, "middle", 600)
    d.t(SX, y + 40, stage, 12, SOFT, MONO)
    y += NODE_H + ROW_GAP
    for st in steps:
        y += draw_step(*st, y) + ROW_GAP
    if NOTES.get(name):
        y += draw_note(NOTES[name], y)
    return y + PHASE_GAP - ROW_GAP


y = ROOT_Y + 48 + PHASE_GAP
for ph in phases:
    y = draw_phase(*ph, y)
    if ph[0] == CUT_AFTER:
        d.line(40, y + 20, W - 40, y + 20, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 235}" y="{y + 8}" width="470" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 25, "1~3단계는 왜 멈췄나 · 4단계부터는 왜 느린가", 13, WARN, KR)
        y += 56

d.legend(H - 68, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("자원 구간", ACC),
                  ("멈춤과 느림의 경계", WARN)])
d.save("os-roadmap.svg")
