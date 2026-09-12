# write/roadmap/os-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 책 열을 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
#   통독하는 책이 하나도 없다 — 전부 부분 독서라, 범위를 안 적으면 로드맵이 통독을 요구하는 것처럼 읽힌다.
# 색이 뜻하는 것은 진입 시점이 아니라 자료의 상태다 —
#   ACC 는 정독 노트가 write/ 에 있는 책, INFO 는 소장본만 있고 노트가 없는 책이다.
# Linux Kernel Programming 은 반대 경우다 — 노트 32편이 있고 Drive 소장본이 없다. 부제에 적는다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, PAPER, PAPER2, RULE, SOFT, D

# (단계, 국면, [(책, 읽을 범위, [다루는 것 2줄], 노트 있음)])
rows = [
    ("1", "Linux 사용", [
        ("Learning Modern Linux", "1~6장 · 정독 노트 16편", ["커널·셸·접근 제어", "파일시스템·부팅·컨테이너"], True),
        ("The Linux Command Line", "1~11장", ["셸·리다이렉션·권한", "프로세스와 환경"], False),
    ]),
    ("1", "명령줄 보조", [
        ("How Linux Works", "1~8장", ["장치·디스크·파일시스템", "부팅과 유저 스페이스 시작"], False),
        ("Efficient Linux at the Command Line", "1~8장", ["명령 조합·파이프라인", "부모·자식·환경"], False),
    ]),
    ("2", "실행 모델", [
        ("Operating System Concepts", "3~9 · 13장", ["프로세스·스레드·동기화", "스케줄링·메모리·I/O"], False),
    ]),
    ("3", "컨테이너 기반", [
        ("Container Security", "2~4장 · 정독 노트 17편", ["시스템 콜·권한·capability", "cgroup·namespace·루트"], True),
    ]),
    ("4", "성능 분석", [
        ("Systems Performance", "2 · 6~9장 · 정독 노트 53편", ["방법론 20종·USE", "CPU·메모리·파일시스템·디스크"], True),
    ]),
    ("5", "관측", [
        ("Systems Performance", "4 · 13~15장", ["관측 도구 커버리지", "perf·Ftrace·BPF"], True),
        ("Learning eBPF", "3 · 5~7 · 9장", ["프로그램 구조·CO-RE·BTF", "verifier·보안"], False),
    ]),
    ("5", "격리 강화", [
        ("Container Security", "8·9장 · 정독 노트 17편", ["샌드박싱 세 갈래", "설정 하나로 무너지는 경계"], True),
    ]),
    ("6", "커널 내부", [
        ("Linux Kernel Programming", "6~13장 · 노트 32편 · 소장본 없음", ["메모리 관리·할당자", "스케줄러·동기화"], True),
    ]),
    ("6", "가상화", [
        ("Virtualization Essentials", "1~3 · 7·8장", ["하이퍼바이저와 VM", "CPU·메모리 배분"], False),
        ("Mastering KVM Virtualization", "1·2 · 15장", ["Linux 가상화와 KVM", "성능 튜닝"], False),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · OS BOOK FLOW",
    "OS 책 읽기 흐름",
    "이 로드맵이 쓰는 책 열을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. 통독하는 책은 없다. "
    "주황은 정독 노트가 write/ 에 있는 책, 파랑은 소장본만 있고 노트가 없는 책이다.",
    "위에서 아래로 진행하고, 같은 행의 책은 병행합니다",
)
d.line(126, TOP + 38, 126, TOP + (len(rows) - 1) * ROW_H + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = TOP + i * ROW_H
    d.box(30, y, 192, 76, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + 51, phase, 15, INK, KR, "middle", 600)
    for j, (title, scope, topics, has_note) in enumerate(cards):
        x = 258 + j * 362
        d.line(222 if j == 0 else x - 28, y + 38, x, y + 38, RULE, 1.0)
        d.box(x, y - 8, 334, 96, PAPER, ACC if has_note else INFO, 1.2)
        d.t(x + 16, y + 16, title, 13, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("정독 노트 있음", ACC), ("소장본만", INFO)])
d.save("os-books.svg")
