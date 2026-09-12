# write/roadmap/go-roadmap.md §책 읽기 흐름.
# 이 로드맵은 보유 노트가 0편이라 책이 자료의 전부다. 다섯 권을 단계 순으로 걸고 읽을 장을 적는다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택·대체.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

rows = [
    ("1–3", "언어", [
        ("Learning Go", "1~11 · 13·14장", ["문법·컬렉션·값 의미론", "인터페이스·에러·제네릭·모듈"], "필수"),
        ("Learn Go with Pocket-Sized Projects", "2~7장", ["작은 프로젝트로 손에 익히기", "제네릭 캐시·CLI"], "대체"),
    ]),
    ("4", "동시성", [
        ("Learn Concurrent Programming with Go", "1~12장", ["스레드·공유·mutex·조건 변수", "채널 패턴·deadlock·atomic"], "필수"),
    ]),
    ("5", "테스트와 성능", [
        ("Learning Go", "15·16장", ["테스트·커버리지", "reflect·unsafe·cgo"], "추천"),
    ]),
    ("6", "네트워크 서비스", [
        ("Network Programming with Go", "1~9 · 11~13장", ["TCP·UDP·소켓·TLS", "HTTP 클라이언트와 서비스"], "필수"),
        ("Cloud Native Go", "4~13장", ["패턴·확장성·느슨한 결합", "복원력·관리성·관측성·보안"], "추천"),
    ]),
    ("5·6", "실습 확장", [
        ("Learn Go with Pocket-Sized Projects", "8~11장 · 부록 D·F", ["동시성 미로·gRPC 서비스", "벤치마킹과 퍼징"], "선택"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · GO BOOK FLOW",
    "Go 책 읽기 흐름",
    "보유 노트가 0편이라 책이 자료의 전부다. 다섯 권을 단계 순으로 걸고 각 책에서 읽을 장을 적었다. "
    "Learning Go 는 1~3단계와 5단계에 나눠 걸린다. 테두리 색이 우선순위다.",
    "위에서 아래로 진행하고, 같은 행의 책은 병행합니다",
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
        d.t(x + 16, y + 16, title, 12, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.o.append(f'<circle cx="{x + 322}" cy="{y + 12}" r="4.5" fill="{MARK[mark]}"/>')
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC)])
d.save("go-books.svg")
