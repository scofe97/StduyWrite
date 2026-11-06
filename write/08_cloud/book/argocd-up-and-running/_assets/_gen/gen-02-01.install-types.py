# 02-01 §3 — 설치 매니페스트는 질문 둘로 좁힌다: API server·UI·SSO 가 필요한가(아니면 core), Argo CD 가 자기 클러스터에도 배포하는가(예면 클러스터 범위, 아니면 네임스페이스 범위).
#            범위가 정해지면 평가·데모는 비HA, 운영은 ha/ 매니페스트를 고른다.
# 본문 근거: 이 노트 ### 3 「설치 유형 고르기」.
# 검증 근거: v3.6.1 의 install.yaml·namespace-install.yaml·ha/install.yaml·core-install.yaml 을 내려받아 Deployment·StatefulSet·CRD 와 replicas 를 직접 셈.
#            kind v1.35.0 에서 namespace-install.yaml 적용 직후 CRD 0개 → manifests/crds 를 따로 적용하면 3개, core-install.yaml 은 Pod 4개(application-controller·applicationset-controller·redis·repo-server)와 argocd login --core 성공.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/installation.md, core.md.
# 타입 스펙: type-flowchart — 질문 노드와 결과 노드.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 490
d = D(W, H, "ARGO CD UP AND RUNNING · 02-01 §3",
      "두 질문으로 설치 매니페스트를 고르는 길",
      "첫 질문은 API server, UI, SSO 가 필요한지 묻고 아니오면 core-install.yaml 이다. 예이면 둘째 질문으로 Argo CD 가 자기가 도는 클러스터에도 배포하는지 묻는다. "
      "예이면 평가나 데모에는 install.yaml, 운영에는 ha/install.yaml 이다. 아니오이면 평가나 데모에는 namespace-install.yaml, 운영에는 ha/namespace-install.yaml 이고 CRD 는 따로 설치한다.",
      "범위를 정한 뒤 운영 환경이면 ha/ 매니페스트로 바꿉니다")

QW, QH = 230, 76
Q1X, Q1Y = 20, 192
Q2X, Q2Y = 294, 278
LX, LW = 600, 260
E1, E2 = 272, 560          # 꺾이는 세로선 x
Q1C, Q2C = Q1Y + QH / 2, Q2Y + QH / 2

CORE_Y, CORE_H = 100, 86
A_Y, A_H = 204, 100
B_Y, B_H = 324, 108


def question(x, y, cap, l1, l2):
    d.tone(x, y, QW, QH, INFO, 6, "14", 1.2)
    d.t(x + 14, y + 20, cap, 11, MUTED, KR, "start", 600)
    d.t(x + 14, y + 42, l1, 12.5, INK, KR, "start", 600)
    d.t(x + 14, y + 61, l2, 12.5, INK, KR, "start", 600)


def leaf(y, h, c, title, rows, note=None):
    d.tone(LX, y, LW, h, c, 6, "14", 1.6 if c == ACC else 1.1)
    d.t(LX + 16, y + 26, title, 13, INK, KR, "start", 600)
    ry = y + 50
    for lab, name in rows:
        if lab:
            d.t(LX + 16, ry, lab, 11, MUTED, KR, "start")
        d.t(LX + (72 if lab else 16), ry, name, 11.5, INK, MONO, "start")
        ry += 20
    if note:
        d.t(LX + 16, ry, note, 11, WARN, KR, "start")


question(Q1X, Q1Y, "질문 1 · 기능 범위", "API server·UI·SSO 가", "필요한가?")
question(Q2X, Q2Y, "질문 2 · 배포 범위", "Argo CD 가 자기 클러스터에도", "배포하는가?")

leaf(CORE_Y, CORE_H, SOFT, "core 설치", [("", "core-install.yaml"), ("", "API server·UI·SSO·알림 없음")])
leaf(A_Y, A_H, ACC, "클러스터 범위 multi-tenant", [("평가·데모", "install.yaml"), ("운영", "ha/install.yaml")])
leaf(B_Y, B_H, WARN, "네임스페이스 범위 multi-tenant",
     [("평가·데모", "namespace-install.yaml"), ("운영", "ha/namespace-install.yaml")], "CRD 는 따로 설치")

# 질문 1 → core(아니오) / 질문 2(예)
d.path(f"M {Q1X + QW} {Q1C} L {E1} {Q1C} L {E1} {CORE_Y + CORE_H / 2} L {LX - 2} {CORE_Y + CORE_H / 2}", MUTED, 1.4, m="ar")
d.path(f"M {E1} {Q1C} L {E1} {Q2C} L {Q2X - 2} {Q2C}", MUTED, 1.4, m="ar")
d.chip(440, CORE_Y + CORE_H / 2, "아니오", MUTED)
d.chip(E1, (Q1C + Q2C) / 2 + 14, "예", MUTED)
# 질문 2 → 클러스터 범위(예) / 네임스페이스 범위(아니오)
d.path(f"M {Q2X + QW} {Q2C} L {E2} {Q2C} L {E2} {A_Y + A_H / 2} L {LX - 2} {A_Y + A_H / 2}", MUTED, 1.4, m="ar")
d.path(f"M {E2} {Q2C} L {E2} {B_Y + B_H / 2} L {LX - 2} {B_Y + B_H / 2}", MUTED, 1.4, m="ar")
d.chip(E2, (Q2C + A_Y + A_H / 2) / 2, "예", MUTED)
d.chip(E2, (Q2C + B_Y + B_H / 2) / 2 + 14, "아니오", MUTED)

d.legend(450, [("질문", INFO), ("실습에서 쓰는 설치", ACC), ("추가 작업이 있는 설치", WARN), ("부가 기능 없는 설치", SOFT)])
d.save("02-01.install-types.svg")
