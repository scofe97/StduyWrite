# write/roadmap/devops-roadmap.md §자료 읽기 흐름.
# 이 로드맵이 쓰는 책과 공식 문서를 단계 순으로 걸고 각 자료에서 읽을 범위만 적는다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택·대체.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

rows = [
    ("1·2 · 7·8", "DevOps와 전달 원칙", [
        ("Fundamentals of DevOps and Software Delivery", "1·2 · 7·8단계", "1·2 · 4~6 · 8 · 11장", ["배포 단위·다중 환경", "IaC 원칙·시크릿 관리"], "필수"),
    ]),
    ("1·2 · 6 · 8", "파이프라인 디자인 패턴", [
        ("CI/CD Design Patterns", "1·2 · 6 · 8단계", "1·2 · 4~11 · 13장", ["Push·Pull·DORA 지표", "배포 전략·파이프라인"], "추천"),
    ]),
    ("1·2", "엔지니어링 프랙티스", [
        ("Software Engineering at Google", "1·2단계", "16 · 18 · 20 · 23·24장", ["trunk-based·지속 전달", "빠른 피드백·정적 분석"], "추천"),
    ]),
    ("1~3 · 5·6 · 8", "빌드 도구와 배포 실전", [
        ("DevOps Tools for Java Developers", "1~3 · 5·6 · 8단계", "2·3 · 5~8 · 10장", ["이미지 빌드·아티팩트", "Application CRD·점진 배포"], "추천"),
    ]),
    ("2 · 5 · 8", "CI 자동화와 파이프라인", [
        ("Learning Continuous Integration with Jenkins", "2 · 5 · 8단계", "1~3 · 5·6 · 8~12장", ["Declarative 파이프라인", "환경 승격·인증·시크릿"], "추천"),
    ]),
    ("3 · 8", "컨테이너·공급망 보안", [
        ("Container Security", "3 · 8단계", "6·7장", ["multi-stage 빌드", "취약점 스캔·CVE 차단"], "추천"),
    ]),
    ("4", "패키징", [
        ("Helm 공식 문서", "4단계", "문서 · Charts · Templates", ["차트 구조·템플릿", "values 주입·릴리스"], "추천"),
    ]),
    ("5", "GitOps", [
        ("ArgoCD 공식 문서", "5단계", "문서 · Core · Sync · App of Apps", ["선언적 설정·Sync 전략", "App of Apps 패턴"], "추천"),
    ]),
    ("6", "점진 배포", [
        ("Argo Rollouts", "6단계", "문서 · Architecture · Canary", ["Rollout CRD·카나리", "Blue-Green·지표 분석"], "추천"),
    ]),
    ("7", "인프라를 코드로", [
        ("Terraform Up and Running", "7단계", "1 · 3·4 · 6장", ["IaC 원칙·원격 state", "state locking·모듈"], "추천"),
        ("Infrastructure as Code", "7단계", "1 · 11 · 21장", ["Immutable 인프라", "프로비저닝 연계"], "추천"),
    ]),
    ("7·8", "정책과 거버넌스", [
        ("Policy as Code", "7·8단계", "11·12 · 14장", ["IaC 정책 검사", "공급망 보안·SBOM"], "선택"),
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
    "WRITE · DEVOPS SOURCE FLOW",
    "DevOps 자료 읽기 흐름",
    "이 로드맵이 쓰는 책과 공식 문서를 단계 순으로 걸고 각 자료에서 읽을 범위만 적었다. "
    "Fundamentals of DevOps 로 원칙을 세우고 도구 구현과 인프라 선언을 각 자료로 채운다. "
    "책이 아닌 자료는 범위 앞에 종류를 적었다. 테두리 색이 우선순위다.",
    "위에서 아래로 진행하고, 같은 행의 자료는 병행합니다. 칩은 그 자료가 걸치는 단계입니다",
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
            tsize = 10.5 if len(title) > 35 else 13
            d.t(x + 16, ly + 18, title, tsize, INK, KR, "start", 600)
            d.o.append(f'<circle cx="{x + 316}" cy="{ly + 14}" r="4.5" fill="{MARK[mark]}"/>')
            # 단계는 카드마다 — 같은 주제라도 책마다 자리가 다르다.
            # 단계 문자열이 길어도 카드를 넘지 않도록 오른쪽 정렬로 붙인다
            d.chip(x + CARD_W - 12 - chip_w(stage) / 2, ly + 40, stage, INFO, 10)
            d.t(x + 16, ly + 44, scope, 11, SOFT, MONO, "start")
            d.t(x + 16, ly + 62, topics[0], 12, MUTED, KR, "start")
            d.t(x + 16, ly + 80, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT)])
d.save("devops-books.svg")
