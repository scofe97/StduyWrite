# write/os-roadmap.md §도입 — DevOps 엔지니어를 위한 OS 학습 로드맵.
# OS 는 01_language 밖, 02_os·08_cloud·99_ETC 에 걸쳐 있어 문서를 write/ 직계에 둔다.
# 판형은 network-roadmap·go-roadmap 과 같다 — 세로 척추에 국면과 단계를 걸고 개념을 좌우로 뻗는다.
# 점선 박스는 책이 다루지 않아 공식 문서·minzkn 정리본으로 채울 키워드다.
# 순서 축은 "매일 만지는 것부터 아래로" 다 — 셸 → 부팅·서비스 → 격리 → 관측 → 커널.
# 네트워크 스택은 network-roadmap 이 맡으므로 여기서는 단계로 두지 않는다(중복 회피).
# 절단선은 국면 4 뒤에 긋는다 — 사용자 목표가 "DevOps 범위를 먼저 다 배우고 나서 확장" 이라
#   0~9 와 10~15 를 가르는 선이 이 로드맵의 편집상 논점이다.
# 타입 스펙: type-tree — 부모에서 자식으로 갈라지는 계층. coral 은 격리와 자원 국면 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, KR, MONO

SX = 500
NODE_W, NODE_H = 296, 48
CH_W, CH_H, CH_GAP = 232, 32, 8
BUS, ROW_GAP, PHASE_GAP = 182, 40, 36

phases = [
    ("손과 셸", "0~1단계", INFO, [
        ("0 · The Linux Command Line 3판", "1~11장",
         ["리다이렉션과 파이프", "권한과 소유권"], ["프로세스와 잡 제어", "환경변수와 셸 확장"],
         ["set -euo pipefail", "man 절 번호 읽기"]),
        ("1 · Efficient Linux at the Command Line", "1~9장 · 2022",
         ["명령을 조합하는 여섯 방식", "히스토리와 재실행"], ["원라이너 조립", "텍스트 파일을 자료로"],
         ["xargs 와 process substitution", "awk 한 줄 관용구"]),
    ]),
    ("부팅에서 서비스까지", "2~4단계", INFO, [
        ("2 · How Linux Works 3판", "1~4장 · 2021",
         ["커널과 유저 스페이스 경계", "디바이스와 sysfs"], ["디스크 · 파티션 · 파일시스템", "마운트와 fstab"],
         ["overlayfs 와 union mount", "LVM 과 스냅샷"]),
        ("3 · How Linux Works 3판", "5~7장",
         ["부트로더와 initramfs", "systemd 유닛과 의존"], ["저널 로깅과 시간", "사용자와 세션"],
         ["systemd 공식 man", "journalctl 로 장애 추적"]),
        ("4 · How Linux Works · Learning Modern Linux", "8장 · 4~5장",
         ["프로세스와 자원 사용", "ulimit 과 nice"], ["접근 제어와 파일 권한", "파일시스템 계층"],
         ["/proc 와 /sys 읽기", "OOM killer 가 고르는 기준"]),
    ]),
    ("격리와 자원", "5~6단계", ACC, [
        ("5 · Container Security", "2~4장 · 2판 2025",
         ["시스템 콜과 capability", "cgroup 으로 자원 제한"], ["namespace 로 격리", "루트 디렉토리 바꾸기"],
         ["cgroup v2 공식 문서", "seccomp 프로파일"]),
        ("6 · Learning Modern Linux · Container Security", "2·6장 · 5·8·9장",
         ["커널이 주는 프리미티브", "컨테이너 런타임의 조립"], ["샌드박싱 세 갈래", "설정 하나로 무너지는 격리"],
         ["rootless 컨테이너", "AppArmor · SELinux"]),
    ]),
    ("관측과 성능", "7~9단계", INFO, [
        ("7 · Systems Performance 2판", "2~4장 · 2020",
         ["USE 방법론", "지연과 포화의 정의"], ["운영체제가 재는 것", "관측 도구의 계보"],
         ["부하 평균을 오해하지 않기", "관측의 관측"]),
        ("8 · Systems Performance 2판", "6~9장",
         ["CPU 스케줄러와 런큐", "메모리와 페이지 캐시"], ["파일시스템 지연", "디스크 I/O 와 큐"],
         ["압박 지표 PSI", "cgroup 별 자원 통계"]),
        ("9 · Systems Performance 2판", "13~15장",
         ["perf 로 프로파일", "Ftrace 로 커널 추적"], ["BCC 와 bpftrace"],
         ["플레임 그래프 읽기", "프로덕션에서의 오버헤드"]),
    ]),
    ("커널로 내려가기", "10~12단계", INFO, [
        ("10 · Learning eBPF", "1~3 · 6·7·9장 · 2023",
         ["프로그램 구조와 맵", "verifier 가 거는 제약"], ["훅 타입과 붙는 자리", "런타임 보안 관측"],
         ["CO-RE 와 BTF", "bpftool"]),
        ("11 · minzkn 리눅스 커널 정리", "1~5절",
         ["빌드 환경과 커널 모듈", "모놀리식 구조와 시스템 콜"], ["태스크와 스케줄러", "버디 · SLAB · NUMA"],
         ["EEVDF 스케줄러", "TLB 와 페이지 테이블"]),
        ("12 · minzkn 리눅스 커널 정리", "6~9절",
         ["인터럽트와 softirq", "스핀락 · 뮤텍스 · RCU"], ["VFS 와 페이지 캐시", "커널 네트워크 스택"],
         ["워크큐와 지연 실행", "seqlock 과 lock-free"]),
    ]),
]

tail = [
    ("13 · minzkn 리눅스 커널 정리", "10~13절",
     ["블록 I/O 와 io_uring", "KVM 과 컨테이너 런타임"], ["LSM 과 무결성 검증", "ftrace · KASAN · crash"],
     ["Device Mapper", "TPM 과 IMA/EVM"]),
    ("14 · Operating System Concepts", "3~9장 · 9판 2012",
     ["프로세스와 스레드", "동기화와 교착"], ["CPU 스케줄링 이론", "가상 메모리 이론"],
     ["10판(2018)이 최신", "이론 보강용으로만"]),
    ("15 · Learning Modern Linux · SRE 2판", "8·9장 · 실무",
     ["관측 가능성 도구", "커널 튜닝과 sysctl"], ["SLO 와 신뢰성 실무"],
     ["장애 대응과 회고", "용량 계획"]),
]

NOTE_H = 76
NOTES = {'부팅에서 서비스까지': '장애를 만났을 때 여는 순서 그대로다. 로그를 보고, 유닛과 마운트를 보고, 그다음 자원 제한을 본다.', '관측과 성능': '도구부터 배우면 도구 목록만 남는다. USE 방법론을 먼저 세워야 어떤 도구를 왜 쓰는지가 정해진다.'}

def ph_note(name):
    return NOTES.get(name)

def row_h(left, right, extra):
    n = max(len(left), len(right) + len(extra))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 24

y = 116 + 96 + 48 + PHASE_GAP
for _n, _, _, steps in phases:
    y += NODE_H + ROW_GAP
    for s in steps:
        y += row_h(s[2], s[3], s[4]) + ROW_GAP
    y += (NOTE_H if ph_note(_n) else 0) + PHASE_GAP - ROW_GAP
y += 56
for s in tail:
    y += row_h(s[2], s[3], s[4]) + ROW_GAP
H, W = y + 76, 1000

d = D(W, H, "WRITE · OS ROADMAP",
      "DevOps 엔지니어를 위한 OS 학습 로드맵",
      "매일 만지는 것에서 시작해 아래로 내려간다. 0~9 단계가 DevOps 로서 쓰는 범위이고, 절단선 아래 10~15 가 확장이다. "
      "셸에서 부팅과 서비스, 격리와 자원, 관측과 성능을 지나 커널 내부로 간다. 실선 박스는 책이 다루는 개념이고, 점선 박스는 공식 문서와 minzkn 정리본으로 채울 키워드다. "
      "네트워크 스택은 network-roadmap 이 맡는다.",
      "0~9 가 DevOps 범위입니다. 절단선 아래는 그 뒤에 여는 확장입니다")

READ_KINDS = [('책이 다루는 개념', 'book'), ('공식 문서 · minzkn 정리본', 'extra')]

# 좌상단 읽는 법 상자 — roadmap.sh 판형의 범례 자리
LX, LY, LW, LH = 40, 96, 320, 84
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for _i, (_txt, _kind) in enumerate(READ_KINDS):
    _cy = LY + 46 + _i * 20
    if _kind == "extra":
        d.o.append(f'<rect x="{LX + 16}" y="{_cy - 8}" width="18" height="14" rx="3" fill="{PAPER}" '
                   f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="3 3"/>')
    else:
        d.o.append(f'<rect x="{LX + 16}" y="{_cy - 8}" width="18" height="14" rx="3" '
                   f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(LX + 44, _cy + 3, _txt, 13, MUTED, KR, "start")

def draw_note(text, y):
    d.o.append(f'<rect x="120" y="{y}" width="760" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(140, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(140, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H

ROOT_Y = 116 + 96
d.box(SX - 130, ROOT_Y, 260, 48, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 30, "매일 만지는 것부터", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 48, SX, H - 100, RULE, 1.4)

def draw_step(title, chap, left, right, extra, y):
    h = row_h(left, right, extra)
    mid = y + h / 2
    for side, items in (("left", [(v, False) for v in left]),
                        ("right", [(v, False) for v in right] + [(v, True) for v in extra])):
        if not items:
            continue
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (label, dashed) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * 34) - (CH_W if side == "left" else 0)
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * 34, cy, RULE, 1.0)
            if dashed:
                d.o.append(f'<rect x="{bx}" y="{cy - CH_H/2}" width="{CH_W}" height="{CH_H}" rx="6" '
                           f'fill="{PAPER}" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
                d.t(bx + CH_W / 2, cy + 5, label, 13, SOFT, KR, "middle")
            else:
                d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
                d.t(bx + CH_W / 2, cy + 5, label, 13, MUTED, KR, "middle")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, RULE, 1.0)
    d.t(SX, mid - 4, title, 13, INK, KR, "middle", 600)
    d.t(SX, mid + 14, chap, 12, SOFT, MONO)
    return h

def draw_phase(name, stage, color, steps, y):
    if color is ACC:
        d.tone(SX - NODE_W / 2, y, NODE_W, NODE_H, ACC, 6, "16", 1.4)
    else:
        d.box(SX - NODE_W / 2, y, NODE_W, NODE_H, PAPER, color, 1.2)
    d.t(SX, y + 22, name, 15, ACC if color is ACC else INK, KR, "middle", 600)
    d.t(SX, y + 40, stage, 12, SOFT, MONO)
    y += NODE_H + ROW_GAP
    for s in steps:
        y += draw_step(*s, y) + ROW_GAP
    if ph_note(name):
        y += draw_note(ph_note(name), y)
    return y + PHASE_GAP - ROW_GAP

y = ROOT_Y + 48 + PHASE_GAP
for ph in phases[:4]:                       # DevOps 로서 매일 쓰는 범위
    y = draw_phase(*ph, y)

# DevOps 범위와 그 너머를 가르는 절단선 — 사용자 목표가 "먼저 다 배우고 나서 확장" 이다
d.line(40, y + 20, W - 40, y + 20, WARN, 1.4, "6 5")
d.o.append(f'<rect x="{SX - 156}" y="{y + 8}" width="312" height="22" rx="4" fill="{PAPER}"/>')
d.t(SX, y + 25, "0~9 까지가 DevOps 범위 · 아래는 확장", 13, WARN, KR)
y += 56

y = draw_phase(*phases[4], y)               # 커널로 내려가기
for s in tail:
    y += draw_step(*s, y) + ROW_GAP

d.legend(H - 68, [("책이 다루는 개념", INFO), ("DevOps 핵심", ACC), ("공식 문서 · minzkn", SOFT)])
d.save("os-roadmap.svg")
