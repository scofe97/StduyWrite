# 06-02 §2 — ImagePolicyWebhook 은 어드미션 단계에서 백엔드에 ImageReview 를 보내 허용 여부를 받고, 백엔드에 닿지 않으면 defaultAllow 로 판정한다.
# 본문 근거: 이 노트 ### 2 「허용한 레지스트리만 들이기」.
# 검증 근거: kind v1.35.0 에서 플러그인을 켜고 백엔드 호스트가 없는 kubeConfigFile 을 줬을 때
#            defaultAllow 생략은 Forbidden(dial tcp: lookup … no such host), defaultAllow: true 는 파드 생성.
# 공식 근거: kubernetes.io/docs/reference/access-authn-authz/admission-controllers 「ImagePolicyWebhook」.
# 타입 스펙: type-swimlane — 백엔드가 답할 때와 닿지 않을 때.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "CKS STUDY GUIDE · 06-02 §2",
      "ImagePolicyWebhook 이 파드를 판정하는 길",
      "위 레인은 파드 생성 요청이 인증과 인가를 지나 ImagePolicyWebhook 에서 백엔드로 ImageReview 를 보내고 allowed 값에 따라 저장되거나 거절되는 흐름이고, "
      "아래 레인은 연결이나 응답에 실패했을 때 defaultAllow 를 생략하거나 false 로 쓰면 거절하는 흐름이다.",
      "백엔드가 답하면 그 답이, 연결·응답에 실패하면 defaultAllow 가 판정합니다")

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


lane(A_Y, "백엔드가 답할 때")
lane_steps(A_Y, [
    ("파드 생성 요청", "kubectl run", INFO),
    ("인증 · 인가 통과", "API 서버", INFO),
    ("ImagePolicyWebhook", "ImageReview 전송", ACC),
    ("백엔드 응답", "allowed: true / false", SOFT),
])
lane(S_Y, "연결·응답에 실패할 때")
lane_steps(S_Y, [
    ("ImagePolicyWebhook", "연결·응답 실패", ACC),
    ("defaultAllow", "생략하면 false", WARN),
    ("거절", "403 Forbidden", BAD),
])

d.legend(392, [("요청과 준비", INFO), ("판정하는 자리", ACC), ("기본값이 정하는 자리", WARN), ("결과", SOFT), ("거절", BAD)])
d.save("06-02.imagepolicywebhook-path.svg")
