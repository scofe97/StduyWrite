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
    ("1–2", "관점과 계측", [
        ("Observability Engineering", "1 · 3 · 5~9장", ["관측 가능성과 구조화 이벤트", "OpenTelemetry 계측·분석"], "필수"),
        ("Observability with Grafana", "1·2장", ["LGTM 스택과 페르소나", "로그·메트릭·트레이스 계측"], "추천"),
    ]),
    ("2 · 4", "트레이싱", [
        ("Distributed Tracing in Practice", "2~6 · 8·9장", ["계측 온톨로지·전파·모범 사례", "배포·오버헤드·샘플링"], "추천"),
    ]),
    ("2–3", "지표 기초", [
        ("Prometheus Up & Running", "3~5 · 9 · 13~20장", ["계측·exposition·라벨", "PromQL·룰·알림·보안"], "필수"),
    ]),
    ("3 · 5–7", "Prometheus 운영", [
        ("Mastering Prometheus", "1~15장", ["데이터 모델·TSDB·SD·알림", "샤딩·Thanos·믹스인·SLO"], "필수"),
    ]),
    ("4 · 7", "Grafana 스택", [
        ("Observability with Grafana", "4 · 6~12장", ["Loki·Tempo·대시보드", "IaC·플랫폼·RUM"], "필수"),
    ]),
    ("5", "운영 판단", [
        ("Site Reliability Engineering", "7~10장", ["SLO 와 에러 버짓", "사고 관리·온콜·포스트모템"], "필수"),
    ]),
    ("4", "로그 검색 백엔드", [
        ("The Definitive Guide to OpenSearch", "4·5 · 7 · 13장", ["색인·매핑·검색 API", "분석·시각화·모니터링"], "선택"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · OBSERVABILITY BOOK FLOW",
    "관측 가능성 책 읽기 흐름",
    "자료를 정독 노트 50편과 소장 책 여섯 권, 공식 문서로 한정했다. 같은 책이 여러 단계에 나뉘어 "
    "걸리므로 행이 단계가 아니라 책의 역할로 묶인다. 테두리 색이 우선순위다.",
    "왼쪽 번호는 그 책이 걸리는 단계입니다",
)
d.line(126, TOP + 38, 126, TOP + (len(rows) - 1) * ROW_H + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = TOP + i * ROW_H
    d.box(30, y, 192, 76, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + 51, phase, 13, INK, KR, "middle", 600)
    for j, (title, scope, topics, mark) in enumerate(cards):
        x = 258 + j * 362
        d.line(222 if j == 0 else x - 28, y + 38, x, y + 38, RULE, 1.0)
        d.box(x, y - 8, 334, 96, PAPER, MARK[mark], 1.2)
        d.t(x + 16, y + 16, title, 12, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.o.append(f'<circle cx="{x + 322}" cy="{y + 12}" r="4.5" fill="{MARK[mark]}"/>')
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT)])
d.save("observability-books.svg")
