# write/roadmap/devops-roadmap.md §학습 순서 — DevOps 학습 로드맵.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다.
#
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이고,
#   소장 목록이 늘면 그 줄만 채운다.
#
# 타입 스펙: type-tree — 부모(단계)에서 자식(개념)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 52
CH_W, CH_H, CH_GAP = 268, 46, 10
BUS, ROW_GAP, PHASE_GAP = 184, 44, 40
NOTE_H = 76
ELBOW = 14

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계 제목, 단계 부제, [왼쪽], [오른쪽])
#   개념 노드 = (개념, 책 챕터 — 없으면 빈 문자열, 우선순위)
stages = [
    ("1 · 전달 모델", "전달 단위와 배포 모델",
     [("배포 단위 · 서버 배포 한계", "Fundamentals of DevOps 1장", "필수"),
      ("버전 관리 · 변경 추적 · Git", "Fundamentals of DevOps 4장", "필수"),
      ("trunk-based · 브랜치 전략", "SE at Google 16장", "필수"),
      ("지속적 전달(CD) vs 지속 배포", "SE at Google 24장", "필수")],
     [("Push · Pull 배포 모델", "CI/CD Design Patterns 1장", "필수"),
      ("dev · stage · prod 환경 격리", "Fundamentals of DevOps 6장", "추천"),
      ("DORA 4대 핵심 지표", "CI/CD Design Patterns 4장", "추천"),
      ("플랫폼 엔지니어링과 IDP", "Fundamentals of DevOps 11장", "선택")]),

    ("2 · CI 파이프라인", "파이프라인 정의와 제어",
     [("CI 파이프라인 원칙 · 빠른 피드백", "Learning CI with Jenkins 1장", "필수"),
      ("빌드 요청과 큐 · 익스큐터 배정", "Learning CI with Jenkins 2장", "필수"),
      ("Scripted vs Declarative PaC", "Learning CI with Jenkins 6·8장", "필수"),
      ("Declarative Pipeline 핵심 구조", "Learning CI with Jenkins 9장", "필수"),
      ("파이프라인 패턴 — 병렬 · 조건", "Learning CI with Jenkins 9장", "필수"),
      ("실패 대응과 sh step 실행 위생", "SE at Google 18장", "추천")],
     [("Agent 분리 · 컨트롤러 구조", "Learning CI with Jenkins 5장", "필수"),
      ("Docker with Pipeline 빌드 격리", "DevOps Tools for Java 5장", "필수"),
      ("동적 Pod 에이전트 프로비저닝", "", "추천"),
      ("Multibranch Pipeline PR 빌드", "Learning CI with Jenkins 12장", "추천"),
      ("정적 분석과 결함 탐지", "SE at Google 20장", "필수"),
      ("Quality Gate 임계치 빌드 게이트", "CI/CD Design Patterns 7장", "필수")]),

    ("3 · 산출물", "이미지 빌드와 불변 식별",
     [("빌드 도구 선택과 컨테이너화", "DevOps Tools for Java 6장", "필수"),
      ("multi-stage · BuildKit 빌드", "Container Security 6장", "필수"),
      ("tag 와 sha256 불변 digest", "Container Security 6장", "필수"),
      ("바이너리 격리와 아티팩트 관리", "DevOps Tools for Java 6장", "필수")],
     [("Nexus Docker Registry 사설 운영", "", "추천"),
      ("Harbor 프로젝트 격리와 복제", "", "추천"),
      ("Artifactory 와 build-info 추적", "DevOps Tools for Java 6장", "선택"),
      ("MinIO 아티팩트 레지스트리 보관", "", "선택")]),

    ("4 · 패키징", "Helm 과 Kustomize 패키징",
     [("Helm 차트 구조와 템플릿 렌더링", "Helm 공식 문서", "필수"),
      ("Helm 릴리스 생애주기와 롤백", "Helm 공식 문서", "추천"),
      ("차트 의존성 관리와 라이프사이클 훅", "Helm 공식 문서", "추천")],
     [("Kustomize base 와 overlays 구조", "Kustomize 공식 문서", "필수"),
      ("Strategic Merge Patch 리소스 패치", "Kustomize 공식 문서", "필수"),
      ("Helm 과 Kustomize 패키징 결합", "", "추천")]),

    ("5 · GitOps", "선언적 상태와 동기화 루프",
     [("선언적 상태와 풀 동기화 루프", "Kubernetes Best Practices 18장", "필수"),
      ("Application CRD 와 대상 클러스터", "DevOps Tools for Java 8장", "필수"),
      ("Sync Waves 와 자동 동기화 제어", "Kubernetes Best Practices 18장", "필수"),
      ("저장소 분리와 staging→prod 승격", "Learning CI with Jenkins 10·11장", "필수")],
     [("GitOps 로 ArgoCD 자체 선언 관리", "ArgoCD 공식 문서", "추천"),
      ("App of Apps 와 ApplicationSet", "Kubernetes Best Practices 18장", "추천"),
      ("AppProject 와 리소스 화이트리스트", "ArgoCD 공식 문서", "추천"),
      ("Image Updater 컨테이너 태그 반영", "", "추천")]),

    ("6 · 점진 배포", "카나리와 롤아웃",
     [("RollingUpdate 한계와 버전 혼재", "CI/CD Design Patterns 6장", "필수"),
      ("Blue-Green 무중단 Service 전환", "CI/CD Design Patterns 6·10장", "필수"),
      ("Canary 트래픽 점진 이동", "CI/CD Design Patterns 6·10장", "필수")],
     [("Argo Rollouts 와 Rollout CRD", "Argo Rollouts", "필수"),
      ("AnalysisTemplate 자동 롤백", "Argo Rollouts", "추천"),
      ("점진적 전달 · 피처 플래그", "DevOps Tools for Java 10장", "추천")]),

    ("7 · 인프라를 코드로", "선언적 인프라와 상태 관리",
     [("IaC 와 Immutable Infrastructure", "Terraform Up and Running 1장", "추천"),
      ("Terraform state 원격 백엔드와 락", "Terraform Up and Running 3장", "추천"),
      ("drift 감지와 Terraform module", "Terraform Up and Running 4·6장", "추천")],
     [("IaC 파이프라인 프로비저닝", "Infrastructure as Code 1장", "추천"),
      ("Cluster API 와 Crossplane 선언", "Production Kubernetes 2장", "선택"),
      ("Security as Code · IaC 정책 검사", "Policy as Code 11·12장", "선택")]),

    ("8 · 파이프라인 보안", "접근 통제와 공급망 보안",
     [("Jenkins 인증 · 인가와 RBAC", "Learning CI with Jenkins 3장", "필수"),
      ("시크릿 바인딩과 최소 권한 원칙", "Learning CI with Jenkins 3장", "필수"),
      ("JCasC 설정 코드화와 GitOps", "", "추천"),
      ("Vault 연동과 JCasC 비밀 치환", "", "추천")],
     [("Rootless 에이전트 · DinD 위험 회피", "DevOps Tools for Java 7장", "추천"),
      ("Xray 취약점 스캔 빌드 게이트", "Container Security 7장", "필수"),
      ("SBOM 생성과 컨테이너 이미지 서명", "Policy as Code 14장", "추천"),
      ("감사 추적과 CI/CD 안티패턴 방지", "CI/CD Design Patterns 13장", "추천")]),
]

CUT_AFTER = 2          # 3단계 뒤에 "변경을 산출물로" ↔ "산출물을 클러스터로" 절단선
NOTES = {
    2: "1~3단계는 변경을 산출물로 선언 · 4단계부터는 클러스터 배포",
    5: "클러스터 런타임은 k8s-roadmap · 관측 지표는 observability-roadmap",
}


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 28


ROOT_Y = 116 + 190
y = ROOT_Y + 52 + PHASE_GAP
for i, (_t, _s, left, right) in enumerate(stages):
    y += row_h(left, right) + ROW_GAP
    if i in NOTES:
        y += NOTE_H
    if i == CUT_AFTER:
        y += 56
H = y + 84

d = D(W, H, "WRITE · DEVOPS ROADMAP",
      "DevOps 학습 로드맵",
      "코드 변경에서 클러스터 반영·인프라 선언까지 이어지는 전달 축이다. "
      "변경을 불변 산출물로 패키징해 GitOps 로 배포하고 점진적으로 트래픽을 열며 인프라와 공급망 보안을 굳힌다. "
      "척추에 단계 여덟을 걸고 개념을 좌우로 뻗었다. 노드의 주인공은 개념이고 아래 줄은 "
      "그 개념을 다루는 책의 장이다. 점 색이 우선순위이고, 책 줄이 비면 아직 자료가 없는 자리다.",
      "노드는 개념, 아래 줄은 그 개념을 다루는 책의 장입니다")

LX, LY, LW, LH = 40, 96, 380, 190
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "선수 지식 — 누락 불가"),
                                ("추천", "권장 실무 지식 — 누락 시 큰 비용"),
                                ("선택", "목표 수립 시 학습"),
                                ("대체", "같은 자리 — 택일")]):
    cy = LY + 54 + i * 26
    c = MARK[lab]
    d.o.append(f'<circle cx="{LX + 24}" cy="{cy}" r="5" fill="{c}"/>')
    d.t(LX + 40, cy + 4, lab, 12, c, KR, "start", 600)
    d.t(LX + 78, cy + 4, txt, 12, MUTED, KR, "start")
d.t(LX + 16, LY + 172, "책 줄이 비면 미배정 자리 — 개념 우선", 12, SOFT, KR, "start")

RX, RY, RW, RH = 580, 96, 380, 190
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("k8s-roadmap", "클러스터 오브젝트 · admission · 런타임 보안"),
        ("observability-roadmap", "대시보드 · 메트릭 · 관측 설정 코드화"),
        ("ai-roadmap", "GitAIOps — AI 와 함께 선언하고 배포하기"),
        ("spring-roadmap", "bootJar · Layered JAR 프레임워크 빌드"),
        ("os-roadmap", "cgroup · namespace 의 커널 격리 구현")]):
    cy = RY + 50 + i * 27
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 14, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 52, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 32, "여기서 시작", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 52, SX, H - 120, RULE, 1.4)


def draw_stage(title, sub, left, right, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (concept, book, mark) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * ELBOW) - (CH_W if side == "left" else 0)
            c = MARK[mark]
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * ELBOW, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.o.append(f'<circle cx="{bx + 15}" cy="{cy - 8}" r="4.5" fill="{c}"/>')
            d.t(bx + 28, cy - 4, concept, 12, INK, KR, "start")
            d.t(bx + 28, cy + 14, book if book else "책 없음 — 채울 자리", 10,
                SOFT if book else MARK["선택"], MONO, "start")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, INFO, 1.2)
    d.t(SX, mid - 4, title, 14, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, KR)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


y = ROOT_Y + 52 + PHASE_GAP
for i, (title, sub, left, right) in enumerate(stages):
    y += draw_stage(title, sub, left, right, y) + ROW_GAP
    if i in NOTES:
        y += draw_note(NOTES[i], y)
    if i == CUT_AFTER:
        d.line(40, y + 12, SX - 235, y + 12, WARN, 1.4, "6 5")
        d.line(SX + 235, y + 12, W - 40, y + 12, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 230}" y="{y}" width="460" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 16, "1~3단계는 변경을 산출물로 · 4단계부터는 산출물을 클러스터로", 12, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT),
                  ("변경과 클러스터 반영의 경계", WARN)])
d.save("devops-roadmap.svg")
