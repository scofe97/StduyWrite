# write/roadmap/jvm-roadmap.md §책 읽기 흐름.
# 책은 셋뿐이고 정독 노트가 171편이다. 세 권이 단계를 나눠 가지므로 같은 책이 여러 행에 나온다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

rows = [
    ("1–2", "구조와 로딩", [
        ("심층 자바 가상 머신", "2 · 6~7 · 9장", ["런타임 데이터 영역·객체", "클래스 파일·로더·톰캣·부트 JAR"], "필수"),
    ]),
    ("3–4", "실행과 회수", [
        ("심층 자바 가상 머신", "3 · 8 · 10·11장", ["도달성·GC 알고리즘·컬렉터", "디스패치·JIT·컴파일러 최적화"], "필수"),
    ]),
    ("4", "GC 튜닝", [
        ("Java Performance", "4~8장", ["JIT·code cache·GC 선택", "힙 분석·footprint·NMT"], "필수"),
    ]),
    ("5", "동시성", [
        ("심층 자바 가상 머신", "12·13장", ["JMM·volatile·가상 스레드", "스레드 안전성·락 최적화"], "필수"),
        ("Java Performance", "9·10장", ["스레드 풀·ForkJoinPool", "NIO·비동기 호출"], "추천"),
    ]),
    ("6", "측정", [
        ("Java Performance", "2·3 · 11·12장", ["벤치마크·통계·JMH·프로파일러", "JDBC·JPA·String·Stream 비용"], "필수"),
    ]),
    ("7", "진단", [
        ("Troubleshooting Java", "1~4 · 7~11장", ["디버거·로그·프로파일러", "스레드 덤프·힙 덤프·GC 로그"], "필수"),
        ("Troubleshooting Java", "12·13장", ["분산 추적·실패 모드", "서비스 간 데이터 불일치"], "추천"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · JVM BOOK FLOW",
    "JVM 책 읽기 흐름",
    "책은 셋뿐이고 정독 노트가 171편이다. 세 권이 단계를 나눠 가지므로 같은 책이 여러 행에 나온다. "
    "심층 자바 가상 머신이 원리를, Java Performance 가 측정과 튜닝을, Troubleshooting Java 가 진단을 맡는다.",
    "위에서 아래로 진행하고, 같은 책이 여러 단계에 나뉘어 걸립니다",
)
d.line(126, TOP + 38, 126, TOP + (len(rows) - 1) * ROW_H + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = TOP + i * ROW_H
    d.box(30, y, 192, 76, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + 51, phase, 14, INK, KR, "middle", 600)
    for j, (title, scope, topics, mark) in enumerate(cards):
        x = 258 + j * 362
        d.line(222 if j == 0 else x - 28, y + 38, x, y + 38, RULE, 1.0)
        d.box(x, y - 8, 334, 96, PAPER, MARK[mark], 1.2)
        d.t(x + 16, y + 16, title, 13, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.o.append(f'<circle cx="{x + 322}" cy="{y + 12}" r="4.5" fill="{MARK[mark]}"/>')
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT)])
d.save("jvm-books.svg")
