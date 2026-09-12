# write/roadmap/os-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 책 열을 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
#   통독하는 책이 하나도 없다 — 전부 부분 독서라, 범위를 안 적으면 로드맵이 통독을 요구하는 것처럼 읽힌다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택·대체. 모든 책을 같은 무게로 늘어놓으면
#   열하나 중 무엇부터 펴야 하는지가 사라진다. 정독 노트 유무는 적지 않는다.
# 대체는 같은 자리를 다른 책이 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계, 국면, [(책, 읽을 장, [다루는 것 2줄], 우선순위)])
rows = [
    ("1–3", "Linux 사용", [
        ("Learning Modern Linux", "1~6장", ["커널·셸·접근 제어", "파일시스템·부팅·컨테이너"], "필수"),
        ("The Linux Command Line", "1~11장", ["셸·리다이렉션·권한", "프로세스와 환경"], "필수"),
    ]),
    ("1·2", "명령줄 보조", [
        ("How Linux Works", "1~8장", ["장치·디스크·파일시스템", "부팅과 유저 스페이스 시작"], "추천"),
        ("Efficient Linux at the Command Line", "1~8장", ["명령 조합·파이프라인", "부모·자식·환경"], "대체"),
    ]),
    ("2 · 4 · 6", "실행 모델", [
        ("Operating System Concepts", "1~9 · 13~16장", ["프로세스·스레드·동기화", "스케줄링·메모리·I/O"], "추천"),
        ("OSTEP (무료 공개판)", "가상화 · 병행성 · 지속성", ["프로세스·스케줄링·주소 공간", "페이징·TLB·파일시스템"], "필수"),
    ]),
    ("3", "컨테이너 기반", [
        ("Container Security", "2~4장", ["시스템 콜·권한·capability", "cgroup·namespace·루트"], "필수"),
    ]),
    ("4", "성능 분석", [
        ("Systems Performance", "2 · 6~9장", ["방법론 20종·USE", "CPU·메모리·파일시스템·디스크"], "필수"),
    ]),
    ("3–5", "Linux 인터페이스", [
        ("Linux Kernel Docs (공식)", "proc · cgroup-v2 · psi", ["/proc/stat·meminfo·PID", "cgroup v2 파일과 PSI"], "필수"),
    ]),
    ("5", "관측", [
        ("Systems Performance", "4 · 13~15장", ["관측 도구 커버리지", "perf·Ftrace·BPF"], "필수"),
        ("Learning eBPF", "3 · 5~7 · 9장", ["프로그램 구조·CO-RE·BTF", "verifier·보안"], "추천"),
    ]),
    ("5", "격리 강화", [
        ("Container Security", "8·9장", ["샌드박싱 세 갈래", "설정 하나로 무너지는 경계"], "추천"),
    ]),
    ("2 · 6", "커널 내부", [
        ("Linux Kernel Programming", "6~13장", ["메모리 관리·할당자", "스케줄러·동기화"], "추천"),
    ]),
    ("6", "가상화", [
        ("Virtualization Essentials", "1~3 · 7·8장", ["하이퍼바이저와 VM", "CPU·메모리 배분"], "선택"),
        ("Mastering KVM Virtualization", "1·2 · 15장", ["Linux 가상화와 KVM", "성능 튜닝"], "대체"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · OS BOOK FLOW",
    "OS 책 읽기 흐름",
    "이 로드맵이 쓰는 책 열셋을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. 통독하는 책은 없다. "
    "테두리 색이 우선순위이고, 대체는 같은 자리를 다른 책이 대신 채우는 경우다.",
    "위에서 아래로 진행하고, 같은 행의 책은 병행합니다",
)
d.line(126, TOP + 38, 126, TOP + (len(rows) - 1) * ROW_H + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = TOP + i * ROW_H
    d.box(30, y, 192, 76, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + 51, phase, 15, INK, KR, "middle", 600)
    for j, (title, scope, topics, mark) in enumerate(cards):
        x = 258 + j * 362
        d.line(222 if j == 0 else x - 28, y + 38, x, y + 38, RULE, 1.0)
        d.box(x, y - 8, 334, 96, PAPER, MARK[mark], 1.2)
        d.t(x + 16, y + 16, title, 13, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.o.append(f'<circle cx="{x + 322}" cy="{y + 12}" r="4.5" fill="{MARK[mark]}"/>')
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC)])
d.save("os-books.svg")
