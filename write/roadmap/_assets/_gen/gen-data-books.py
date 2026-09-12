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
        ("Designing Data-Intensive Applications", "1~3장", ["운영과 분석·성능·신뢰성", "관계형·문서·그래프 모델"], "필수"),
    ]),
    ("3", "저장 엔진", [
        ("DDIA, 2판", "4장", ["OLTP 저장과 인덱스", "컬럼 지향·벡터 인덱스"], "필수"),
        ("Database Internals", "1~7장", ["B-tree 기초·구현·변형", "파일 포맷·복구·로그 구조"], "추천"),
    ]),
    ("3", "검색 색인", [
        ("Elasticsearch in Action, 2판", "3·4 · 7~13장", ["아키텍처·매핑·텍스트 분석", "검색과 집계"], "선택"),
    ]),
    ("4", "인코딩", [
        ("DDIA, 2판", "5장", ["호환성·Protobuf·Avro", "DB·REST·RPC 데이터플로우"], "필수"),
    ]),
    ("5–6", "복제 · 샤딩 · 트랜잭션", [
        ("DDIA, 2판", "6~8장", ["복제·샤딩·리밸런싱", "격리 수준과 2PC"], "필수"),
        ("Database Internals", "5 · 11~13장", ["복구와 복제 일관성", "안티엔트로피·분산 트랜잭션"], "추천"),
    ]),
    ("7–8", "분산과 합의", [
        ("DDIA, 2판", "9·10장", ["비신뢰 네트워크와 시계", "선형성·CAP·합의"], "필수"),
        ("Database Internals", "9·10 · 14장", ["장애 감지와 리더 선출", "합의 알고리즘"], "추천"),
    ]),
    ("5·7·8", "패턴 카탈로그", [
        ("Patterns of Distributed Systems", "3~7 · 10~12 · 17~29장", ["WAL·세그먼트 로그·하이워터마크", "Paxos·시계·임차·가십"], "추천"),
    ]),
    ("9", "배치와 스트림", [
        ("DDIA, 2판", "11~13장", ["MapReduce·데이터플로우 엔진", "브로커·CDC·윈도우·언번들링"], "필수"),
    ]),
    ("1·9", "윤리", [
        ("DDIA, 2판", "14장", ["예측 분석의 편향과 책임", "프라이버시와 데이터 권력"], "선택"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · DATA BOOK FLOW",
    "데이터 책 읽기 흐름",
    "이 로드맵이 쓰는 책 넷을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. DDIA 2판이 척추이고 "
    "Database Internals 가 구현 층을, Patterns of Distributed Systems 가 패턴 카탈로그를 맡는다. "
    "SQL·JPA·QueryDSL 을 다루는 책은 소장본에 없어 걸 자리가 없다. 테두리 색이 우선순위다.",
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
d.save("data-books.svg")
