# write/roadmap/k8s-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 책 열하나를 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택·대체.
#   모든 책을 같은 무게로 늘어놓으면 무엇부터 펴야 하는지가 사라진다.
# 정독 노트 유무는 적지 않는다. 노트 링크는 본문 단계 표가 맡는다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

rows = [
    ("1–3", "오브젝트·워크로드·연결", [
        ("Kubernetes in Action", "1~18장", ["Pod·컨트롤러·볼륨", "Service·Ingress·Gateway API"], "필수"),
        ("Kubernetes Patterns", "2~9 · 12 · 15~24장", ["예측 가능한 요구·배포·probe", "구조 패턴과 격리 패턴"], "추천"),
    ]),
    ("3", "연결 보강", [
        ("Networking and Kubernetes", "4·5장", ["CNI·kube-proxy·정책·DNS", "Service·EndpointSlice·Ingress"], "추천"),
    ]),
    ("4·5 · 7", "자원·내부 구조", [
        ("Production Kubernetes", "3~9 · 12~13장", ["런타임·저장·라우팅·어드미션", "관측·멀티테넌시·오토스케일"], "추천"),
    ]),
    ("5·6", "확장", [
        ("Programming Kubernetes", "1~6 · 9장", ["client-go·CRD·코드 생성", "Operator 와 고급 커스텀 리소스"], "추천"),
        ("Policy as Code", "4·5 · 7·8장", ["OPA 와 Kubernetes", "Gatekeeper 와 Kyverno"], "선택"),
    ]),
    ("6", "보안", [
        ("Container Security", "2~4 · 8·9 · 13장", ["capability·cgroup·namespace", "샌드박싱·경계 파괴·런타임"], "추천"),
        ("CKS Study Guide", "2~7장", ["클러스터·시스템 하드닝", "공급망·런타임 보안"], "선택"),
    ]),
    ("6–7", "운영 관례", [
        ("Kubernetes Best Practices", "3·4 · 8~12 · 17·18장", ["모니터링·RBAC·자원 관리", "정책·멀티클러스터·GitOps"], "추천"),
    ]),
    ("7", "고급 주제", [
        ("Kubernetes Up and Running", "7 · 14~21장", ["Service Discovery·RBAC", "확장·정책·멀티클러스터"], "추천"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · KUBERNETES BOOK FLOW",
    "Kubernetes 책 읽기 흐름",
    "이 로드맵이 쓰는 책 열을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. 통독하는 책은 "
    "Kubernetes in Action 하나이고 나머지는 부분 독서다. 테두리 색이 우선순위다.",
    "위에서 아래로 진행하고, 같은 행의 책은 병행합니다",
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
        d.t(x + 16, y + 16, title, 13, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.o.append(f'<circle cx="{x + 322}" cy="{y + 12}" r="4.5" fill="{MARK[mark]}"/>')
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT)])
d.save("k8s-books.svg")
