# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, PAPER, PAPER2, RULE, SOFT, D

rows = [
    ("1", "Linux 사용", [("Learning Modern Linux", "1단계 기둥 · 셸에서 서비스까지", ["파일·권한·스트림", "boot·systemd·journal"])]),
    ("2–3", "실행·컨테이너", [("Systems Performance", "2단계 진입 · 3장", ["커널·시스템 콜", "인터럽트·프로세스"]), ("Container Security", "3단계 진입 · 3·4장", ["cgroup·namespace", "루트 디렉토리"])]),
    ("4–5", "성능·관측", [("Systems Performance", "4·5단계 기둥 · 2·6~9·13~15장", ["방법론·CPU·메모리·I/O", "perf·Ftrace·BPF"]), ("Container Security", "5단계 기둥 · 2·8·9장", ["capability·seccomp", "샌드박싱·격리 파괴"])]),
    ("6", "커널 내부", [("Linux Kernel Programming", "6단계 기둥 · 2단계에 6장 먼저", ["프로세스·메모리 관리", "스케줄러·동기화"])]),
]

W, TOP, ROW_H = 1000, 160, 132
H = TOP + len(rows) * ROW_H + 68
d = D(W, H, "WRITE · OS BOOK FLOW", "OS 책 읽기 흐름", "단계 표에 연결된 책만 사용해 읽는 시점, 범위, 핵심 주제를 배치했습니다.", "위에서 아래로 진행하고, 같은 행의 책은 병행합니다")
d.line(126, TOP + 38, 126, TOP + (len(rows) - 1) * ROW_H + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = TOP + i * ROW_H
    d.box(30, y, 192, 76, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + 51, phase, 15, INK, KR, "middle", 600)
    for j, (title, timing, topics) in enumerate(cards):
        x = 258 + j * 362
        d.line(222 if j == 0 else x - 28, y + 38, x, y + 38, RULE, 1.0)
        d.box(x, y - 8, 334, 96, PAPER, ACC if i == 0 and j == 0 else INFO, 1.2)
        d.t(x + 16, y + 16, title, 14, INK, KR, "start", 600)
        d.t(x + 16, y + 39, timing, 13, SOFT, KR, "start")
        d.t(x + 16, y + 62, topics[0], 13, MUTED, KR, "start")
        d.t(x + 16, y + 81, topics[1], 13, MUTED, KR, "start")
d.legend(H - 44, [("첫 진입", ACC), ("단계별 독서", INFO)])
d.save("os-books.svg")
