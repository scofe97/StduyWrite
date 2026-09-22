# write/roadmap/spring-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 책 다섯을 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
#   통독하는 책은 Spring Start Here 하나뿐이고 나머지는 부분 독서라,
#   범위를 안 적으면 로드맵이 통독을 요구하는 것처럼 읽힌다.
# 같은 책이 여러 단계에 갈려 걸리므로 행은 단계가 아니라 책의 역할로 묶는다.
# 색이 뜻하는 것은 우선순위다. 정독 노트 유무는 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보이고, 노트 링크는 본문 표가 맡는다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계, 국면, [(책, 읽을 장, [다루는 것 2줄], 우선순위)])
rows = [
    ("1–4 · 9", "골격 세우기", [
        ("Spring Start Here", "1~4 · 9단계", "전 15장", ["컨텍스트·와이어링·스코프·AOP", "MVC·REST·트랜잭션·테스트"], "필수"),
    ]),
    ("3–4", "웹과 데이터", [
        ("Spring in Action, 6판", "3~5 · 7~9단계", "2·3 · 7장", ["웹 애플리케이션과 REST", "데이터 다루기"], "필수"),
    ]),
    ("5", "부트 설정", [
        ("Spring in Action, 6판", "3~5 · 7~9단계", "6장 · 부록", ["구성 프로퍼티", "부트스트랩"], "필수"),
        ("Cloud Native Spring in Action", "5·6 · 8·9단계", "4 · 14장", ["외부화 설정 관리", "설정과 비밀 관리"], "추천"),
    ]),
    ("6", "통신과 회복", [
        ("Cloud Native Spring in Action", "5·6 · 8·9단계", "8 · 9장", ["리액티브 — 회복성과 확장성", "API 게이트웨이와 서킷 브레이커"], "추천"),
    ]),
    ("7", "비동기와 리액티브", [
        ("Spring in Action, 6판", "3~5 · 7~9단계", "9 · 11~13장", ["비동기 메시징", "Reactor·리액티브 API·영속성"], "추천"),
        ("The Definitive Guide to Spring Batch", "7단계", "2~4 · 7~9 · 11장", ["잡과 스텝·메타데이터", "리더·프로세서·라이터·스케일링"], "선택"),
    ]),
    ("8", "보안", [
        ("Spring Security in Action, 2판", "8·9단계", "1~16장", ["필터 체인·인증·인가", "CSRF·CORS·OAuth 2·OIDC"], "필수"),
    ]),
    ("8", "운영", [
        ("Spring in Action, 6판", "3~5 · 7~9단계", "15~17장", ["액츄에이터", "관리와 JMX 모니터링"], "필수"),
        ("Cloud Native Spring in Action", "5·6 · 8·9단계", "13장", ["관측과 모니터링", "프로메테우스 연동"], "추천"),
    ]),
    ("9", "테스트와 배포", [
        ("Spring Security in Action, 2판", "8·9단계", "17 · 18장", ["리액티브 보안", "보안 설정 테스트"], "추천"),
        ("Cloud Native Spring in Action", "5·6 · 8·9단계", "6·7 · 15장", ["컨테이너화와 쿠버네티스", "지속 배포와 GitOps"], "추천"),
        ("Spring in Action, 6판", "3~5 · 7~9단계", "18장", ["bootJar 와 배포 산출물", "컨테이너와 쿠버네티스 배포"], "필수"),
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
    "WRITE · SPRING BOOK FLOW",
    "Spring 책 읽기 흐름",
    "이 로드맵이 쓰는 책 다섯을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. Spring Start Here 와 "
    "Spring Security in Action 은 통독하고 나머지는 부분 독서다. 같은 책이 여러 단계에 갈려 걸리므로 "
    "행은 단계가 아니라 책의 역할로 묶었다. 테두리 색이 우선순위다.",
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
d.save("spring-books.svg")
