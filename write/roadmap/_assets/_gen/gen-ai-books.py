# write/roadmap/ai-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 책 다섯을 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
#   통독하는 책은 둘뿐이라, 범위를 안 적으면 로드맵이 통독을 요구하는 것처럼 읽힌다.
# AI Engineering 은 7·8장(파인튜닝·데이터셋 구축)을 뺀다 — 모델을 만드는 쪽이라
#   이 로드맵의 축 바깥이다. 같은 이유로 소장본 중 Build a LLM (From Scratch) 는 걸지 않는다.
# 색이 뜻하는 것은 우선순위다. 정독 노트 유무는 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보이고, 노트 링크는 본문 표가 맡는다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계, 국면, [(책, 읽을 장, [다루는 것 2줄], 우선순위)])
rows = [
    ("1–2", "모델과 컨텍스트", [
        ("AI Engineering", "1·2 · 7·8단계", "1 · 5·6장", ["모델 선택과 토큰 셈법", "프롬프트 · RAG"], "필수"),
    ]),
    ("3–4", "도구와 에이전트", [
        ("Building Applications with AI Agents", "3·4 · 7·8단계", "1·2 · 4~6 · 8장", ["도구 사용과 오케스트레이션", "지식 · 메모리 · 다중 에이전트"], "필수"),
    ]),
    ("3 · 5", "개발 환경", [
        ("Claude Code Up and Running", "3 · 5단계", "전 7장", ["권한 · 신뢰 경계", "스킬 · 훅 · MCP 연동"], "필수"),
    ]),
    ("5·6", "GitAIOps", [
        ("AI 인프라 — Claude로", "5·6단계", "전 9장", ["ArgoCD · 관측 · 무중단 배포", "멀티테넌시 · 가드레일"], "필수"),
    ]),
    ("7", "평가와 방어", [
        ("AI Engineering", "1·2 · 7·8단계", "3·4장", ["평가 방법론", "AI 시스템 채점"], "필수"),
        ("AI Agents", "3·4 · 7·8단계", "9 · 12장", ["검증과 측정", "에이전트 시스템 보호"], "필수"),
    ]),
    ("8", "운영", [
        ("AI Agents", "3·4 · 7·8단계", "10 · 11 · 13장", ["프로덕션 모니터링", "개선 루프 · 사람과의 협업"], "필수"),
        ("Introducing MLOps", "8단계", "1 · 3 · 5~8장", ["배포 준비와 되먹임", "모델 거버넌스"], "추천"),
    ]),
    ("8", "서빙 비용", [
        ("AI Engineering", "1·2 · 7·8단계", "9 · 10장", ["추론 최적화의 인프라 절반", "아키텍처와 사용자 피드백"], "선택"),
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
    "WRITE · AI BOOK FLOW (DEVOPS)",
    "AI 책 읽기 흐름 — DevOps 축",
    "이 로드맵이 쓰는 책 다섯을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. 통독하는 책은 둘이고 "
    "나머지는 부분 독서다. AI Engineering 의 파인튜닝·데이터셋 두 장은 모델을 만드는 쪽이라 뺐다. "
    "테두리 색이 우선순위다.",
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
d.save("ai-books.svg")
