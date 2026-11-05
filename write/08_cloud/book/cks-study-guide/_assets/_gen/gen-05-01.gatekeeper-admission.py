# 05-01 §3 — Gatekeeper 는 ConstraintTemplate 과 Constraint 를 먼저 등록해 두고, 요청이 어드미션에 오면 웹훅이 판정한다.
# 본문 근거: 이 노트 ### 3 「OPA Gatekeeper 로 조직 정책 강제하기」.
# 검증 근거: kind v1.35.0 에 Gatekeeper v3.23.1 을 설치해 K8sRequiredLabels 템플릿과 Constraint 를 적용했고,
#            app 레이블 없는 네임스페이스 생성이 validation.gatekeeper.sh 웹훅에서 Forbidden 으로 거절되는 것을 확인.
# 공식 근거: open-policy-agent.github.io/gatekeeper 「How to use Gatekeeper」.
# 타입 스펙: type-swimlane — 정책 등록 레인과 요청 판정 레인.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "CKS STUDY GUIDE · 05-01 §3",
      "Gatekeeper 정책이 요청을 막는 길",
      "위 레인은 ConstraintTemplate 에서 CRD 가 만들어지고 Constraint 객체가 생기는 정책 등록 순서이고, "
      "아래 레인은 kubectl 요청이 인증, 인가를 지나 Gatekeeper 웹훅에서 허용 또는 거절되는 요청 판정 순서이다.",
      "먼저 규칙을 등록해 두면, 이후 모든 요청이 어드미션 웹훅에서 그 규칙으로 판정됩니다")

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
        d.t(x + BW / 2, by + 32, title, 13, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 11, MUTED, MONO)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "정책 등록")
lane_steps(A_Y, [
    ("ConstraintTemplate", "Rego + 스키마", INFO),
    ("CRD 생성", "K8sRequiredLabels", INFO),
    ("Constraint 작성", "labels: [app]", SOFT),
])
lane(S_Y, "요청 판정")
lane_steps(S_Y, [
    ("kubectl create ns", "governed-ns", INFO),
    ("인증 · 인가 통과", "API 서버", INFO),
    ("어드미션 웹훅", "validation.gatekeeper.sh", ACC),
    ("허용 또는 거절", "저장 / 403 Forbidden", SOFT),
])

d.legend(392, [("요청과 준비", INFO), ("저장 또는 결과", SOFT), ("규칙을 평가하는 자리", ACC)])
d.save("05-01.gatekeeper-admission.svg")
