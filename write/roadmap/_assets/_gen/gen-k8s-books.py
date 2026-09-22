# write/roadmap/k8s-roadmap.md §자료 읽기 흐름.
# 이 로드맵이 쓰는 책 열두 권을 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택·대체.
#   모든 책을 같은 무게로 늘어놓으면 무엇부터 펴야 하는지가 사라진다.
# 정독 노트 유무는 적지 않는다. 노트 링크는 본문 단계 표가 맡는다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

rows = [
    ("1–6", "오브젝트·워크로드·연결", [
        ("Kubernetes in Action", "1~5단계", "1·2 · 4~18장", ["Pod·컨트롤러·볼륨", "Service·Ingress·Gateway API"], "필수"),
        ("Kubernetes Patterns", "1~4 · 6단계", "2~9 · 12·13 · 15~24장", ["예측 가능한 요구·배포·probe", "구조 패턴과 격리 패턴"], "추천"),
    ]),
    ("3", "연결 보강", [
        ("Networking and Kubernetes", "3단계", "4·5장", ["CNI·kube-proxy·정책·DNS", "Service·EndpointSlice·Ingress"], "추천"),
    ]),
    ("4–7", "자원·내부 구조", [
        ("Production Kubernetes", "4~7단계", "3~10 · 12~13장", ["런타임·저장·라우팅·어드미션", "관측·신원·멀티테넌시"], "추천"),
    ]),
    ("5·6", "확장", [
        ("Programming Kubernetes", "5·6단계", "1~6 · 9장", ["client-go·CRD·코드 생성", "Operator 와 고급 커스텀 리소스"], "추천"),
    ]),
    ("6", "보안", [
        ("Container Security", "6단계", "1~4 · 8·9 · 13장", ["위협 모델·capability·격리", "샌드박싱·경계 파괴·런타임"], "추천"),
        ("CKS Study Guide", "6단계", "2~7장", ["클러스터·시스템 하드닝·PSS", "공급망·감사 로그·Falco"], "추천"),
        ("Learning eBPF", "6단계", "9장", ["eBPF 보안 활용", "Tetragon·BPF LSM"], "선택"),
        ("Kubernetes 보안 문서 묶음", "6단계", "문서 · 네 편", ["PSS·Security Checklist", "Auditing·저장 암호화"], "추천"),
        ("CIS Kubernetes Benchmark", "6단계", "문서 · kube-bench", ["Control Plane·Worker 항목", "자동 점검 도구"], "추천"),
        ("KISA 클라우드 취약점 점검 가이드", "6단계", "문서 · 2.26~2.28절", ["Docker·Master·Worker 절", "진단 기준과 조치"], "선택"),
        ("런타임 탐지 문서", "6단계", "문서 · Falco·Tetragon", ["규칙 기반 탐지", "eBPF 강제와 탐지"], "선택"),
        ("EKS Best Practices for Security", "6단계", "문서 · 가이드 전편", ["IRSA·Pod Identity", "봉투 암호화·제어부 로그"], "추천"),
    ]),
    ("6·7", "정책과 코드화", [
        ("Policy as Code", "6·7단계", "4·5 · 7·8 · 11·12 · 14장", ["OPA·Gatekeeper·Kyverno", "Terraform·공급망 정책"], "선택"),
        ("Terraform Up and Running", "7단계", "1·3·4·6장", ["IaC·불변 인프라", "state·module·비밀"], "추천"),
    ]),
    ("6–7", "운영 관례", [
        ("Kubernetes Best Practices", "6·7단계", "3·4 · 8~12 · 17·18장", ["모니터링·RBAC·자원 관리", "정책·멀티클러스터·GitOps"], "추천"),
    ]),
    ("1 · 3–7", "여러 단계 보강", [
        ("Kubernetes Up and Running", "1 · 3~7단계", "4 · 7 · 14~21장", ["kubectl·Service Discovery·RBAC", "저장·확장·정책·멀티클러스터"], "추천"),
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
    "WRITE · KUBERNETES SOURCE FLOW",
    "Kubernetes 자료 읽기 흐름",
    "이 로드맵이 쓰는 책과 문서를 단계 순으로 걸고 각 자료에서 읽을 범위만 적었다. Kubernetes in Action 은 "
    "3장만 빼고 통독하고 나머지는 부분 독서다. 책이 아닌 자료는 범위 앞에 종류를 적었다. 테두리 색이 우선순위다.",
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
            d.t(x + 16, ly + 18, title, 13, INK, KR, "start", 600)
            d.o.append(f'<circle cx="{x + 316}" cy="{ly + 14}" r="4.5" fill="{MARK[mark]}"/>')
            # 단계는 카드마다 — 같은 주제라도 책마다 자리가 다르다.
            # 단계 문자열이 길어도 카드를 넘지 않도록 오른쪽 정렬로 붙인다
            d.chip(x + CARD_W - 12 - chip_w(stage) / 2, ly + 40, stage, INFO, 10)
            d.t(x + 16, ly + 44, scope, 11, SOFT, MONO, "start")
            d.t(x + 16, ly + 62, topics[0], 12, MUTED, KR, "start")
            d.t(x + 16, ly + 80, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT)])
d.save("k8s-books.svg")
