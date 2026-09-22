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
        ("Learning Go", "1~5단계", "1~11 · 13·14장", ["문법·컬렉션·값 의미론", "인터페이스·에러·제네릭·모듈"], "필수"),
        ("Learn Go with Pocket-Sized Projects", "1·2·5·6단계", "2~7장", ["작은 프로젝트로 손에 익히기", "제네릭 캐시·CLI"], "선택"),
    ]),
    ("4", "동시성", [
        ("Learn Concurrent Programming with Go", "4단계", "1~12장", ["스레드·공유·mutex·조건 변수", "채널 패턴·deadlock·atomic"], "필수"),
        ("Learning Go", "1~5단계", "12장", ["goroutine·channel·select", "Go 다운 동시성 관용구"], "필수"),
    ]),
    ("5", "테스트와 성능", [
        ("Learning Go", "1~5단계", "15장", ["table-driven·test double", "커버리지·golden file"], "필수"),
    ]),
    ("6", "네트워크 서비스", [
        ("Network Programming with Go", "6단계", "1~9 · 11~13장", ["TCP·UDP·소켓·TLS", "HTTP 클라이언트와 서비스"], "필수"),
        ("Cloud Native Go", "6단계", "4~13장", ["패턴·확장성·느슨한 결합", "복원력·관리성·관측성·보안"], "추천"),
    ]),
    ("5·6", "실습 확장", [
        ("Learn Go with Pocket-Sized Projects", "1·2·5·6단계", "8~11장 · 부록 D·F", ["동시성 미로·gRPC 서비스", "벤치마킹과 퍼징"], "선택"),
    ]),
]

W, TOP = 1000, 168
COLS, CARD_W, CARD_H = 2, 334, 96          # 카드 폭은 가장 긴 책 제목이 정한다
COL_GAP, LINE_GAP, ROW_GAP = 28, 22, 36    # 한 주제가 여러 줄로 접힐 때의 간격

def chip_w(t, size=10, pad=7):
    """dd.chip 의 폭 공식. 칩을 카드 오른쪽에 맞춰 붙이려면 폭을 미리 알아야 한다."""
    kr = any('가' <= c <= '힣' for c in str(t))
    return len(str(t)) * (size * 1.0 if kr else size * 0.62) + pad * 2

def lines_of(cards):
    """한 주제의 카드를 2열씩 끊어 줄로 나눈다. 주제당 권수 상한은 없다."""
    return [cards[k:k + COLS] for k in range(0, len(cards), COLS)]

def row_h(cards):
    n = len(lines_of(cards))
    return n * CARD_H + (n - 1) * LINE_GAP + ROW_GAP

row_y, _acc = [], TOP
for _r in rows:
    row_y.append(_acc)
    _acc += row_h(_r[-1])
H = _acc + 72
d = D(
    W,
    H,
    "WRITE · GO BOOK FLOW",
    "Go 책 읽기 흐름",
    "정독 노트가 없어 책이 자료의 전부다. 책을 단계 순으로 걸고 각 책에서 읽을 장을 적었다. "
    "Learning Go 는 1~3단계와 4·5단계에 나눠 걸린다. 테두리 색이 우선순위다.",
    "위에서 아래로 진행하고, 같은 행의 책은 병행합니다. 칩은 그 책이 걸치는 단계입니다",
)
d.line(126, row_y[0] + 38, 126, row_y[-1] + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = row_y[i]
    groups = lines_of(cards)
    box_h = len(groups) * CARD_H + (len(groups) - 1) * LINE_GAP - 20
    d.box(30, y, 192, box_h, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + box_h / 2 + 12, phase, 15, INK, KR, "middle", 600)
    if len(groups) > 1:
        d.line(240, y + 38, 240, y + (len(groups) - 1) * (CARD_H + LINE_GAP) + 38, RULE, 1.0)
    for g, line_cards in enumerate(groups):
        ly = y + g * (CARD_H + LINE_GAP)
        d.line(222, ly + 38, 258, ly + 38, RULE, 1.0)
        for j, (title, stage, scope, topics, mark) in enumerate(line_cards):
            x = 258 + j * (CARD_W + COL_GAP)
            if j:
                d.line(x - COL_GAP, ly + 38, x, ly + 38, RULE, 1.0)
            d.box(x, ly - 8, CARD_W, CARD_H, PAPER, MARK[mark], 1.2)
            d.t(x + 16, ly + 18, title, 13, INK, KR, "start", 600)
            d.o.append(f'<circle cx="{x + 316}" cy="{ly + 14}" r="4.5" fill="{MARK[mark]}"/>')
            # 단계는 카드마다 — 같은 주제라도 책마다 자리가 다르다.
            # 단계 문자열이 길어도 카드를 넘지 않도록 오른쪽 정렬로 붙인다
            d.chip(x + CARD_W - 12 - chip_w(stage) / 2, ly + 40, stage, INFO, 10)
            d.t(x + 16, ly + 44, scope, 11, SOFT, MONO, "start")
            d.t(x + 16, ly + 62, topics[0], 12, MUTED, KR, "start")
            d.t(x + 16, ly + 80, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC)])
d.save("go-books.svg")
