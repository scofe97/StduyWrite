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
        ("AI Engineering", "1 · 5·6장", ["모델 선택과 토큰 셈법", "프롬프트 · RAG"], "필수"),
    ]),
    ("3–4", "도구와 에이전트", [
        ("Building Applications with AI Agents", "1·2 · 4~6 · 8장", ["도구 사용과 오케스트레이션", "지식 · 메모리 · 다중 에이전트"], "필수"),
    ]),
    ("5", "개발 환경", [
        ("Claude Code Up and Running", "전 7장", ["권한 · 신뢰 경계", "스킬 · 훅 · MCP 연동"], "필수"),
    ]),
    ("6", "GitAIOps", [
        ("AI 인프라 — Claude로", "전 9장", ["ArgoCD · 관측 · 무중단 배포", "멀티테넌시 · 가드레일"], "필수"),
    ]),
    ("7", "평가와 방어", [
        ("AI Engineering", "3·4장", ["평가 방법론", "AI 시스템 채점"], "필수"),
        ("AI Agents", "9 · 12장", ["검증과 측정", "에이전트 시스템 보호"], "필수"),
    ]),
    ("8", "운영", [
        ("AI Agents", "10 · 11 · 13장", ["프로덕션 모니터링", "개선 루프 · 사람과의 협업"], "필수"),
        ("Introducing MLOps", "1 · 3 · 5~8장", ["배포 준비와 되먹임", "모델 거버넌스"], "추천"),
    ]),
    ("8", "서빙 비용", [
        ("AI Engineering", "9 · 10장", ["추론 최적화의 인프라 절반", "아키텍처와 사용자 피드백"], "선택"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · AI BOOK FLOW (DEVOPS)",
    "AI 책 읽기 흐름 — DevOps 축",
    "이 로드맵이 쓰는 책 다섯을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. 통독하는 책은 둘이고 "
    "나머지는 부분 독서다. AI Engineering 의 파인튜닝·데이터셋 두 장은 모델을 만드는 쪽이라 뺐다. "
    "테두리 색이 우선순위다.",
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
d.save("ai-books.svg")
