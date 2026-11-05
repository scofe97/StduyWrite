# 06-01 §3 — Hadolint 는 Dockerfile 을 빌드 전에, Kubesec 은 매니페스트를 적용 전에 검사한다.
# 본문 근거: 이 노트 ### 3 「배포 전에 파일을 정적 분석하기」.
# 검증 근거: Docker 29.8.2 에서 hadolint/hadolint(2.15.1)로 Dockerfile 을, kubesec/kubesec:v2.15.0(--platform linux/amd64)으로 Pod 매니페스트를 스캔해
#            DL3006 · DL3045 · DL3007 경고와 score · scoring.critical · scoring.advise 필드를 확인했다.
# 공식 근거: github.com/hadolint/hadolint 2.15.1 README, github.com/controlplaneio/kubesec v2.15.0 README.
# 타입 스펙: type-swimlane — Dockerfile 레인과 매니페스트 레인, 각 레인의 둘째 칸이 검사 게이트.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "CKS STUDY GUIDE · 06-01 §3",
      "정적 분석이 끼는 자리",
      "위 레인은 Dockerfile이 Hadolint 검사를 지나 docker build와 push로 이어지는 순서이고, "
      "아래 레인은 Pod 매니페스트가 Kubesec 검사를 지나 kubectl apply로 이어지는 순서이다.",
      "두 검사는 파일만 있으면 돌아서, 이미지를 빌드하거나 클러스터에 적용하기 전에 문제를 잡습니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, S_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 13, INK, KR if c != ACC else MONO, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 11, MUTED, MONO)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "Dockerfile")
lane_steps(A_Y, [
    ("Dockerfile", "FROM · COPY · RUN", INFO),
    ("hadolint", "DL3006 · DL3045", ACC),
    ("docker build", "이미지 생성", SOFT),
    ("push", "레지스트리에 올림", SOFT),
])
lane(S_Y, "Pod 매니페스트")
lane_steps(S_Y, [
    ("Pod YAML", "securityContext · resources", INFO),
    ("kubesec", "score · advise", ACC),
    ("kubectl apply", "API 서버", SOFT),
    ("파드 실행", "클러스터", SOFT),
])

d.legend(392, [("작성한 파일", INFO), ("검사하는 자리", ACC), ("검사 뒤 단계", SOFT)])
d.save("06-01.static-analysis-gates.svg")
