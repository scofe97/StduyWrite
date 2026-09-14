# write/roadmap/observability-roadmap.md §책 읽기 흐름.
# 자료를 정독 노트 50편·소장 책 여섯 권·공식 문서로 한정한다.
#   06_observability 의 자체 프로젝트 노트는 순서의 근거로 쓰지 않는다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

rows = [
    ("1·2 · 7", "관점과 계측", [
        ("Observability Engineering", "1·2 · 7단계", "1 · 3 · 5~9장", ["관측 가능성과 구조화 이벤트", "OpenTelemetry 계측·분석"], "필수"),
        ("Observability with Grafana", "1·2 · 4 · 7단계", "1·2장", ["LGTM 스택과 페르소나", "로그·메트릭·트레이스 계측"], "추천"),
    ]),
    ("2 · 4", "트레이싱", [
        ("Distributed Tracing in Practice", "2 · 4단계", "2~6 · 8·9장", ["계측 온톨로지·전파·모범 사례", "배포·오버헤드·샘플링"], "추천"),
    ]),
    ("2·3 · 5·6", "지표 기초", [
        ("Prometheus Up & Running", "2·3 · 5·6단계", "3~5 · 9 · 13~20장", ["계측·exposition·라벨", "PromQL·룰·알림·보안"], "필수"),
    ]),
    ("1 · 3 · 5–7", "Prometheus 운영", [
        ("Mastering Prometheus", "1 · 3 · 5~7단계", "1~15장", ["데이터 모델·TSDB·SD·알림", "샤딩·Thanos·믹스인·SLO"], "필수"),
    ]),
    ("4 · 7", "Grafana 스택", [
        ("Observability with Grafana", "1·2 · 4 · 7단계", "4 · 6~12장", ["Loki·Tempo·대시보드", "IaC·플랫폼·RUM"], "필수"),
    ]),
    ("1 · 5", "운영 판단", [
        ("Site Reliability Engineering", "1 · 5단계", "7~10장", ["SLO 와 에러 버짓", "사고 관리·온콜·포스트모템"], "필수"),
    ]),
    ("4", "로그 검색 백엔드", [
        ("The Definitive Guide to OpenSearch", "4단계", "4·5 · 7 · 13장", ["색인·매핑·검색 API", "분석·시각화·모니터링"], "선택"),
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
    "WRITE · OBSERVABILITY BOOK FLOW",
    "관측 가능성 책 읽기 흐름",
    "자료를 정독 노트 50편과 소장 책 여섯 권, 공식 문서로 한정했다. 같은 책이 여러 단계에 나뉘어 "
    "걸리므로 행이 단계가 아니라 책의 역할로 묶인다. 테두리 색이 우선순위다.",
    "왼쪽 번호는 그 묶음을 읽는 자리이고, 칩은 그 책이 걸치는 단계입니다",
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
d.save("observability-books.svg")
