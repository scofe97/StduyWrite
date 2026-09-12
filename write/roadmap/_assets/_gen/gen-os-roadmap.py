# write/roadmap/os-roadmap.md §학습 순서 — OS 학습 로드맵.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다. 단계에만 배지를 달던 앞 판은 한 단계 안에서
#   무엇이 뼈대이고 무엇이 곁가지인지 말하지 못했다.
#
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이고,
#   소장 목록이 늘면 그 줄만 채운다. 정독 노트 편수는 도식에 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보다. 노트 링크는 본문 단계 표가 맡는다.
#
# 대체(ACC)는 같은 자리를 두 자료가 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
# 타입 스펙: type-tree — 부모(단계)에서 자식(개념)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 52
CH_W, CH_H, CH_GAP = 268, 46, 10
BUS, ROW_GAP, PHASE_GAP = 184, 44, 40
NOTE_H = 76
ELBOW = 14

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계 제목, 단계 부제, [왼쪽], [오른쪽])
#   개념 노드 = (개념, 책 챕터 — 없으면 빈 문자열, 우선순위)
stages = [
    ("1 · Linux 사용", "명령을 치는 자리에서 시작한다",
     [("셸 · 스트림 · 변수 · 종료 상태", "The Linux Command Line 1·5~8장", "필수"),
      ("파일 · 권한 · 리다이렉션", "The Linux Command Line 4·6·9장", "필수"),
      ("모든 것이 파일 — VFS · mount", "How Linux Works 3·4장", "필수"),
      ("부팅 · initramfs · systemd", "How Linux Works 5·6장", "필수"),
      ("journal · 서비스 의존", "How Linux Works 7장", "필수")],
     [("커널이 맡는 일과 맡지 않는 일", "Operating System Concepts 1·2장", "필수"),
      ("명령 조합 · 파이프라인", "Efficient Linux 1·5·7장", "추천"),
      ("셸 스크립트가 조용히 실패하는 법", "The Linux Command Line 7장", "추천"),
      ("systemd-analyze 로 부팅 쪼개기", "", "선택"),
      ("core dump 저장 경로", "", "선택")]),

    ("2 · 실행 모델", "애플리케이션이 하는 일은 시스템 콜이다",
     [("유저 · 커널 스페이스 · 시스템 콜", "Operating System Concepts 2장", "필수"),
      ("process · thread · task 구조", "Operating System Concepts 3·4장", "필수"),
      ("signal · 종료 코드 137 · 143", "The Linux Command Line 10장", "필수"),
      ("zombie · PID 1", "How Linux Works 8장", "필수"),
      ("file descriptor · ulimit", "", "필수"),
      ("주소 공간 · heap · stack", "Operating System Concepts 8장", "필수"),
      ("mmap · 공유 메모리 · COW", "Operating System Concepts 9장", "추천")],
     [("strace 로 시스템 콜 세기", "", "필수"),
      ("epoll · 논블로킹 I/O", "Operating System Concepts 13장", "추천"),
      ("event loop · readiness 모델", "", "추천"),
      ("배압 · 큐 길이", "", "추천"),
      ("동기화 · 교착 · 조건 변수", "Operating System Concepts 5·7장", "추천"),
      ("prctl · PR_SET_PDEATHSIG", "", "선택"),
      ("vfork · clone3", "", "선택")]),

    ("3 · 컨테이너 기반", "컨테이너는 새 기술이 아니라 조합이다",
     [("namespace 여덟 · unshare", "Container Security 4장", "필수"),
      ("cgroup v2 · controller · PSI", "Container Security 3장", "필수"),
      ("memory.max · OOM Killer", "", "필수"),
      ("cpu.max · cpu.stat · throttling", "", "필수"),
      ("mount propagation", "", "필수")],
     [("OverlayFS · copy-on-write", "", "필수"),
      ("user namespace · rootless", "Container Security 4장", "추천"),
      ("시스템 콜 · 권한 · capability", "Container Security 2장", "추천"),
      ("cgroup namespace", "", "선택"),
      ("hugetlbfs", "", "선택")]),

    ("4 · 성능 분석", "느리다는 말을 사용률·포화·오류로 쪼갠다",
     [("USE · RED · 드릴다운", "", "필수"),
      ("run queue · CFS · context switch", "Operating System Concepts 6장", "필수"),
      ("RSS · VSS · PSS · page cache", "Operating System Concepts 8·9장", "필수"),
      ("block I/O · IOPS · fsync", "Operating System Concepts 10장", "필수"),
      ("파일 시스템 캐시 · 유형", "Operating System Concepts 11·12장", "추천")],
     [("throughput · tail latency · P99", "Systems Performance 2장", "필수"),
      ("coordinated omission", "", "필수"),
      ("flame graph · 프로파일 네 축", "Systems Performance 6장", "추천"),
      ("malloc · arena · 단편화", "", "추천"),
      ("load average · softirq · swap", "", "추천"),
      ("steal time · CPU quota", "Systems Performance 11장", "추천"),
      ("blk-cgroup · IRQ affinity", "", "선택")]),

    ("5 · 관측과 보안", "증상마다 맞는 창이 다르다",
     [("procfs · sysfs · sar", "", "필수"),
      ("perf — 샘플링과 이벤트", "", "필수"),
      ("Ftrace — tracefs · 트레이서", "", "추천"),
      ("eBPF · BCC · bpftrace", "Learning eBPF 3장", "추천"),
      ("verifier · CO-RE · BTF", "Learning eBPF 5·6장", "추천")],
     [("capability · seccomp", "Container Security 2장", "필수"),
      ("샌드박싱 세 갈래", "Container Security 8장", "추천"),
      ("설정 하나로 무너지는 경계", "Container Security 9장", "추천"),
      ("AppArmor · SELinux", "Operating System Concepts 14·15장", "선택"),
      ("eBPF 보안 활용", "Learning eBPF 9장", "선택"),
      ("Landlock", "", "선택")]),

    ("6 · 커널 내부", "바깥에서 보던 커널의 안으로 들어간다",
     [("VAS · 주소 변환 · KASLR", "Operating System Concepts 8·9장", "추천"),
      ("페이지 할당자 · GFP 플래그", "", "추천"),
      ("slab · kmalloc · vmalloc", "", "추천"),
      ("demand paging · OOM killer", "Operating System Concepts 9장", "추천"),
      ("스케줄링 클래스 · CFS 구현", "Operating System Concepts 6장", "추천")],
     [("page table · 가용 공간 관리", "Operating System Concepts 8·9장", "추천"),
      ("spinlock · mutex · 임계 구역", "Operating System Concepts 5장", "추천"),
      ("atomic · lock-free · lockdep", "", "선택"),
      ("하이퍼바이저 · VM · 자원 배분", "Virtualization Essentials 1~3장", "선택"),
      ("KVM 구조 · 성능 튜닝", "Mastering KVM 1·2·15장", "대체"),
      ("kdump · crash 분석", "", "선택"),
      ("io_uring · VFS 구현 · LSM 훅", "", "선택")]),
]

CUT_AFTER = 2          # 3단계 뒤에 "왜 멈췄나" ↔ "왜 느린가" 절단선
NOTES = {
    2: "Pod 가 137 로 죽으면 3단계, 서비스가 안 뜨면 1단계가 첫 자리다. 번호는 의존 순서다.",
    5: "책 줄이 빈 노드는 아직 자료가 없는 자리다. 소장 목록이 늘면 그 줄만 채운다.",
}


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 28


ROOT_Y = 116 + 190
y = ROOT_Y + 52 + PHASE_GAP
for i, (_t, _s, left, right) in enumerate(stages):
    y += row_h(left, right) + ROW_GAP
    if i in NOTES:
        y += NOTE_H
    if i == CUT_AFTER:
        y += 56
H = y + 84

d = D(W, H, "WRITE · OS ROADMAP",
      "OS 학습 로드맵",
      "Linux 운영에서 실행 모델과 격리로 내려간 뒤 성능·관측·커널 내부로 이어진다. 척추에 단계 "
      "여섯을 걸고 개념을 좌우로 뻗었다. 노드의 주인공은 개념이고 아래 줄은 그 개념을 다루는 책의 "
      "장이다. 점 색이 우선순위이고, 책 줄이 비면 아직 자료가 없는 자리다.",
      "노드는 개념, 아래 줄은 그 개념을 다루는 책의 장입니다")

LX, LY, LW, LH = 40, 96, 380, 190
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만"),
                                ("대체", "같은 자리 — 하나만 고릅니다")]):
    cy = LY + 54 + i * 26
    c = MARK[lab]
    d.o.append(f'<circle cx="{LX + 24}" cy="{cy}" r="5" fill="{c}"/>')
    d.t(LX + 40, cy + 4, lab, 12, c, KR, "start", 600)
    d.t(LX + 78, cy + 4, txt, 12, MUTED, KR, "start")
d.t(LX + 16, LY + 172, "책 줄이 비면 아직 자료가 없는 자리 — 개념이 먼저입니다", 12, SOFT, KR, "start")

RX, RY, RW, RH = 580, 96, 380, 190
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("network-roadmap", "netns 이후의 패킷 경로"),
        ("k8s-roadmap", "오브젝트 배포와 클러스터 운영"),
        ("07_devops", "이미지 포맷과 OCI 표준"),
        ("Linux Kernel Programming 1~5장", "커널 빌드와 모듈 개발 환경")]):
    cy = RY + 56 + i * 33
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 52, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 32, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 52, SX, H - 120, RULE, 1.4)


def draw_stage(title, sub, left, right, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (concept, book, mark) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * ELBOW) - (CH_W if side == "left" else 0)
            c = MARK[mark]
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * ELBOW, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.o.append(f'<circle cx="{bx + 15}" cy="{cy - 8}" r="4.5" fill="{c}"/>')
            d.t(bx + 28, cy - 4, concept, 12, INK, KR, "start")
            d.t(bx + 28, cy + 14, book if book else "책 없음 — 채울 자리", 10,
                SOFT if book else MARK["선택"], MONO, "start")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, INFO, 1.2)
    d.t(SX, mid - 4, title, 14, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, KR)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


y = ROOT_Y + 52 + PHASE_GAP
for i, (title, sub, left, right) in enumerate(stages):
    y += draw_stage(title, sub, left, right, y) + ROW_GAP
    if i in NOTES:
        y += draw_note(NOTES[i], y)
    if i == CUT_AFTER:
        d.line(40, y + 12, W - 40, y + 12, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 235}" y="{y}" width="470" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~3단계는 왜 멈췄나 · 4단계부터는 왜 느린가", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("멈춤과 느림의 경계", WARN)])
d.save("os-roadmap.svg")
