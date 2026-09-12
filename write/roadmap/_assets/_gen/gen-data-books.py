# write/roadmap/data-roadmap.md §책 읽기 흐름.
# 자체 노트 79편이 1~7단계를 맡고 책 셋이 3·8~10단계를 맡는다.
#   그래서 책 카드가 뒷단계에 몰린다 — 앞단계의 빈자리는 노트가 채운다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

rows = [
    ("2–3", "모델과 저장 엔진", [
        ("Designing Data-Intensive Applications", "3~5장", ["관계형·문서·그래프 모델", "LSM·B-tree·인코딩"], "추천"),
        ("Database Internals", "2~7장", ["B-tree 구현·페이지 분할", "WAL·복구·로그 구조 저장"], "추천"),
    ]),
    ("5", "트랜잭션", [
        ("Designing Data-Intensive Applications", "8장", ["ACID·격리 수준·스냅샷", "Write Skew·2PC"], "필수"),
    ]),
    ("8", "복제와 샤딩", [
        ("Designing Data-Intensive Applications", "6·7장", ["단일·다중 리더·리더리스", "키 범위·해시 샤딩·리밸런싱"], "필수"),
    ]),
    ("9", "분산과 합의", [
        ("Designing Data-Intensive Applications", "9·10장", ["부분 실패·시계·시스템 모델", "선형성·CAP·합의"], "필수"),
        ("Patterns of Distributed Systems", "8·11·12·14장", ["Majority Quorum·Paxos", "Replicated Log·합의 패턴"], "추천"),
    ]),
    ("10", "배치와 스트림", [
        ("Designing Data-Intensive Applications", "11~13장", ["배치·MapReduce·데이터플로우", "브로커·CDC·스트림 처리"], "추천"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · DATA BOOK FLOW",
    "데이터 책 읽기 흐름",
    "자체 노트 79편이 1~7단계를 맡고 책 셋이 3단계와 8~10단계를 맡는다. 그래서 책 카드가 뒷단계에 "
    "몰린다 — 앞단계의 빈자리는 노트가 채운다. 테두리 색이 우선순위다.",
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
        d.t(x + 16, y + 16, title, 11, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.o.append(f'<circle cx="{x + 322}" cy="{y + 12}" r="4.5" fill="{MARK[mark]}"/>')
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT)])
d.save("data-books.svg")
