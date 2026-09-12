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
    ("1–4", "골격 세우기", [
        ("Spring Start Here", "전 15장", ["컨텍스트·와이어링·스코프·AOP", "MVC·REST·트랜잭션·테스트"], "필수"),
    ]),
    ("3–4", "웹과 데이터", [
        ("Spring in Action, 6판", "2·3 · 7장", ["웹 애플리케이션과 REST", "데이터 다루기"], "필수"),
    ]),
    ("5", "부트 설정", [
        ("Spring in Action, 6판", "6장 · 부록", ["구성 프로퍼티", "부트스트랩"], "필수"),
        ("Cloud Native Spring in Action", "4 · 14장", ["외부화 설정 관리", "설정과 비밀 관리"], "추천"),
    ]),
    ("6", "통신과 회복", [
        ("Cloud Native Spring in Action", "8 · 9장", ["리액티브 — 회복성과 확장성", "API 게이트웨이와 서킷 브레이커"], "추천"),
    ]),
    ("7", "비동기와 리액티브", [
        ("Spring in Action, 6판", "9 · 11~14장", ["비동기 메시징", "Reactor·리액티브 API·RSocket"], "추천"),
        ("The Definitive Guide to Spring Batch", "2~4 · 7~9 · 11장", ["잡과 스텝·메타데이터", "리더·프로세서·라이터·스케일링"], "선택"),
    ]),
    ("8", "보안", [
        ("Spring Security in Action, 2판", "1~16장", ["필터 체인·인증·인가", "CSRF·CORS·OAuth 2·OIDC"], "필수"),
    ]),
    ("8", "운영", [
        ("Spring in Action, 6판", "15~17장", ["액츄에이터", "관리와 JMX 모니터링"], "필수"),
    ]),
    ("9", "테스트와 배포", [
        ("Spring Security in Action, 2판", "17 · 18장", ["리액티브 보안", "보안 설정 테스트"], "추천"),
        ("Cloud Native Spring in Action", "6·7 · 15장", ["컨테이너화와 쿠버네티스", "지속 배포와 GitOps"], "추천"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · SPRING BOOK FLOW",
    "Spring 책 읽기 흐름",
    "이 로드맵이 쓰는 책 다섯을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. 통독하는 책은 "
    "Spring Start Here 하나뿐이고 나머지는 부분 독서다. 같은 책이 여러 단계에 갈려 걸리므로 "
    "행은 단계가 아니라 책의 역할로 묶었다. 테두리 색이 우선순위다.",
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
d.save("spring-books.svg")
