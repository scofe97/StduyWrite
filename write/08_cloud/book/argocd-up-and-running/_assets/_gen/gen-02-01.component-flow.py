# 02-01 §2 — Argo CD 는 저장소의 선언을 Repository Server 가 매니페스트로 만들고, Application Controller 가 클러스터의 실제 상태와 비교한다.
#            사용자·CLI·CI/CD 는 API server 를 거쳐 Application 리소스를 다루고, 그 리소스를 같은 컨트롤러가 감시한다.
# 본문 근거: 이 노트 ### 2 「구성 요소와 요청 흐름」.
# 검증 근거: kind v1.35.0 에 v3.6.1 manifests/install.yaml 을 적용해 Deployment 6개와 StatefulSet argocd-application-controller 가 Running 이 되는 것,
#            3개 CRD(applications·applicationsets·appprojects) 등록, 초기 admin 비밀번호로 argocd login 성공을 확인.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/architecture.md(API server·Repository Server·Application Controller 의 책임),
#            high_availability.md("argocd-application-controller uses argocd-repo-server to get generated manifests and Kubernetes API server to get the actual cluster state",
#            "Redis is only used as a disposable cache"), user-management/index.md(번들 Dex), notifications/index.md, applicationset/index.md.
# 타입 스펙: type-swimlane — 세 레인(선언의 길·사용자의 길·함께 설치되는 서비스).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 580
d = D(W, H, "ARGO CD UP AND RUNNING · 02-01 §2",
      "Argo CD 구성 요소가 선언을 클러스터에 닿게 하는 길",
      "위 레인은 Git 이나 Helm 저장소를 Repository Server 가 매니페스트로 바꾸고 Application Controller 가 그 결과와 대상 클러스터의 실제 상태를 비교하는 흐름이다. "
      "가운데 레인은 UI, CLI, 외부 CI/CD 가 API server 를 거쳐 Application 리소스를 다루고 같은 Application Controller 가 그 리소스를 감시하는 흐름이다. "
      "아래 레인은 Redis, Dex, Notifications, ApplicationSet controller 가 함께 설치되는 서비스라는 것을 보인다.",
      "선언과 실제 상태를 비교하는 곳은 Application Controller 하나입니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, B_Y, C_Y = 96, 244, 392


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items, arrows=True):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 12.5, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 11, MUTED, KR)
        if arrows and i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "선언이 클러스터에 닿는 길")
lane_steps(A_Y, [
    ("저장소", "Git · Helm", INFO),
    ("Repository Server", "매니페스트 생성", INFO),
    ("Application Controller", "실제 상태와 목표 상태 비교", ACC),
    ("대상 클러스터", "Kubernetes API", SOFT),
])
lane(B_Y, "사용자와 외부 시스템이 닿는 길")
lane_steps(B_Y, [
    ("UI · CLI · CI/CD", "API 호출", INFO),
    ("API server", "gRPC · REST", INFO),
    ("Application 리소스", "CRD 로 등록된 리소스", SOFT),
    ("Application Controller", "리소스 감시와 동기화", ACC),
])
lane(C_Y, "함께 설치되는 서비스")
lane_steps(C_Y, [
    ("Redis", "휘발성 캐시", SOFT),
    ("Dex", "SSO 중계", SOFT),
    ("Notifications controller", "외부로 알림", SOFT),
    ("ApplicationSet controller", "Application 일괄 생성", SOFT),
], arrows=False)

d.legend(540, [("입구와 중간 서비스", INFO), ("비교와 동기화가 일어나는 자리", ACC), ("리소스·대상·부가 서비스", SOFT)])
d.save("02-01.component-flow.svg")
