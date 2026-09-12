# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, PAPER, PAPER2, RULE, SOFT, D

rows = [
    ("1", "문법", [("A Tour of Go", "1단계 전 · 전체 실습", ["문법·함수", "slice·map·method"]), ("Learning Go 2판", "1단계 · 1~6장", ["문법·컬렉션", "값 의미론"])]),
    ("2–3", "타입·도구", [("Learning Go 2판", "2–3단계 · 7~11, 13~14장", ["interface·error", "module·toolchain"]), ("Effective Go", "3단계 · 관용구", ["package·naming", "composition·receiver"])]),
    ("3", "리뷰", [("100 Go Mistakes", "3단계 · 사례 중심", ["slice·nil", "leak·context"])]),
    ("4", "동시성", [("Learn Concurrent Programming", "4단계 · 1~12장", ["goroutine·sync", "channel·memory model"])]),
    ("5", "검증", [("Learn Go with Tests", "5단계 · 필요한 장 실습", ["table test·double", "fuzz·benchmark"]), ("Learning Go 2판", "5단계 · 15~16장", ["test·profile", "runtime·GC"])]),
    ("6", "서비스", [("Network Programming with Go", "6단계 · 1~9장", ["TCP/UDP·HTTP", "timeout·resolver"]), ("Cloud Native Go 2판", "6단계 · 4~13장", ["shutdown·resilience", "observability·security"])]),
]

W, TOP, ROW_H = 1000, 160, 124
H = TOP + len(rows) * ROW_H + 68
d = D(W, H, "WRITE · GO BOOK FLOW", "Go 책 읽기 흐름", "문법부터 서비스까지 단계 표에 명시된 책과 읽을 범위를 연결했습니다.", "위에서 아래로 진행하고, 같은 행의 책은 병행합니다")
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
        d.t(x + 16, y + 16, title, 13, INK, KR, "start", 600)
        d.t(x + 16, y + 39, timing, 13, SOFT, KR, "start")
        d.t(x + 16, y + 62, topics[0], 13, MUTED, KR, "start")
        d.t(x + 16, y + 81, topics[1], 13, MUTED, KR, "start")
d.legend(H - 44, [("첫 진입", ACC), ("단계별 독서", INFO)])
d.save("go-books.svg")
