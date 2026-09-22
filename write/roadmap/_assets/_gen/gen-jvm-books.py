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
        ("심층 자바 가상 머신", "1~6단계", "2 · 6~7 · 9장", ["런타임 데이터 영역·객체", "클래스 파일·로더·톰캣·부트 JAR"], "필수"),
    ]),
    ("3–4", "실행과 회수", [
        ("심층 자바 가상 머신", "1~6단계", "3 · 8 · 10·11장", ["도달성·GC 알고리즘·컬렉터", "디스패치·JIT·컴파일러 최적화"], "필수"),
    ]),
    ("3·4", "GC 튜닝", [
        ("Java Performance", "3~6단계", "4~8장", ["JIT·code cache·GC 선택", "힙 분석·footprint·NMT"], "필수"),
    ]),
    ("5·6", "동시성", [
        ("심층 자바 가상 머신", "1~6단계", "12·13장", ["JMM·volatile·가상 스레드", "스레드 안전성·락 최적화"], "필수"),
        ("Java Performance", "3~6단계", "9·10장", ["스레드 풀·ForkJoinPool", "NIO·비동기 호출"], "추천"),
    ]),
    ("6", "측정", [
        ("Java Performance", "3~6단계", "2·3 · 11·12장", ["벤치마크·통계·JMH·프로파일러", "JDBC·JPA·String·Stream 비용"], "필수"),
        ("심층 자바 가상 머신", "1~6단계", "4장", ["jps·jstat·jmap·jstack", "JHSDB·통합 JVM 로깅"], "필수"),
    ]),
    ("7", "진단", [
        ("Troubleshooting Java", "7단계", "1~4 · 7~11장", ["디버거·로그·프로파일러", "스레드 덤프·힙 덤프·GC 로그"], "필수"),
        ("Troubleshooting Java", "7단계", "12·13장", ["분산 추적·실패 모드", "서비스 간 데이터 불일치"], "추천"),
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
    "WRITE · JVM BOOK FLOW",
    "JVM 책 읽기 흐름",
    "책은 셋이고 정독 노트가 자료의 중심이다. 세 권이 단계를 나눠 가지므로 같은 책이 여러 행에 나온다. "
    "심층 자바 가상 머신이 원리를, Java Performance 가 측정과 튜닝을, Troubleshooting Java 가 진단을 맡는다.",
    "위에서 아래로 진행하고, 같은 책이 여러 단계에 나뉘어 걸립니다. 칩은 그 책이 걸치는 단계입니다",
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
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT)])
d.save("jvm-books.svg")
