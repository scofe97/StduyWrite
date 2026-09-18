# write/roadmap/data-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 책 넷을 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
# 자료를 소장 책과 05_data/book 의 DDIA 2판 정독 노트로 한정한 판이라,
#   SQL·JPA·QueryDSL 을 다루는 책은 소장본에 없어 걸 자리가 없다.
#   그 축은 05_data 의 자체 노트가 맡고 이 로드맵은 순서를 말하지 않는다.
# 색이 뜻하는 것은 우선순위다. 정독 노트 유무는 적지 않는다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계, 국면, [(책, 읽을 장, [다루는 것 2줄], 우선순위)])
rows = [
    ("1–2", "축과 모델", [
        ("Designing Data-Intensive Applications", "1~9단계", "1~3장", ["운영과 분석·성능·신뢰성", "관계형·문서·그래프 모델"], "필수"),
    ]),
    ("3", "저장 엔진", [
        ("DDIA, 2판", "1~9단계", "4장", ["OLTP 저장과 인덱스", "컬럼 지향·벡터 인덱스"], "필수"),
        ("Database Internals", "3 · 5~8단계", "1~7장", ["B-tree 기초·구현·변형", "파일 포맷·복구·로그 구조"], "추천"),
    ]),
    ("3", "검색 색인", [
        ("Elasticsearch in Action, 2판", "3단계", "3·4 · 7~13장", ["아키텍처·매핑·텍스트 분석", "검색과 집계"], "선택"),
        ("Real-World Cryptography", "1단계", "8장", ["난수와 비밀 관리", "키로 지우는 데이터"], "선택"),
    ]),
    ("4", "인코딩", [
        ("DDIA, 2판", "1~9단계", "5장", ["호환성·Protobuf·Avro", "DB·REST·RPC 데이터플로우"], "필수"),
    ]),
    ("5–6", "복제 · 샤딩 · 트랜잭션", [
        ("DDIA, 2판", "1~9단계", "6~8장", ["복제·샤딩·리밸런싱", "격리 수준과 2PC"], "필수"),
        ("Database Internals", "3 · 5~8단계", "5 · 11~13장", ["복구와 복제 일관성", "안티엔트로피·분산 트랜잭션"], "추천"),
    ]),
    ("7–8", "분산과 합의", [
        ("DDIA, 2판", "1~9단계", "9·10장", ["비신뢰 네트워크와 시계", "선형성·CAP·합의"], "필수"),
        ("Database Internals", "3 · 5~8단계", "9·10 · 14장", ["장애 감지와 리더 선출", "합의 알고리즘"], "추천"),
    ]),
    ("3 · 5 · 7·8", "패턴 카탈로그", [
        ("Patterns of Distributed Systems", "3 · 5 · 7·8단계", "3~7 · 10~12 · 17~29장", ["WAL·세그먼트 로그·하이워터마크", "Paxos·시계·임차·가십"], "추천"),
    ]),
    ("9", "배치와 스트림", [
        ("DDIA, 2판", "1~9단계", "11~13장", ["MapReduce·데이터플로우 엔진", "브로커·CDC·윈도우·언번들링"], "필수"),
    ]),
    ("1·9", "윤리", [
        ("DDIA, 2판", "1~9단계", "14장", ["예측 분석의 편향과 책임", "프라이버시와 데이터 권력"], "선택"),
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
    "WRITE · DATA BOOK FLOW",
    "데이터 책 읽기 흐름",
    "이 로드맵이 쓰는 책 넷을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. DDIA 2판이 척추이고 "
    "Database Internals 가 구현 층을, Patterns of Distributed Systems 가 패턴 카탈로그를 맡는다. "
    "SQL·JPA·QueryDSL 을 다루는 책은 소장본에 없어 걸 자리가 없다. 테두리 색이 우선순위다.",
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
d.save("data-books.svg")
