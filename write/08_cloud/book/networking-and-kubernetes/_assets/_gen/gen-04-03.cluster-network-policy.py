# 04-03.cluster-network-policy — 클러스터 관리자의 규칙이 개발자의 NetworkPolicy 앞뒤에 놓인다
# 본문 요구: 「표준 정책 밖의 규칙과 확장」 — ClusterNetworkPolicy 의 평가 순서는 Admin 티어 → NetworkPolicy 티어 → Baseline 티어,
#           CNP 는 Admin 과 Baseline 을 쓴다. 액션은 Accept·Deny·Pass 이고 Pass 는 현재 티어의 남은 규칙을 건너뛰어 다음 티어로 넘긴다.
#           같은 티어에서는 priority 값이 작은 ClusterNetworkPolicy 가 먼저. CNP 는 선택된 Pod 를 암묵적으로 격리하지 않는다.
# 타입 스펙: type-layers — 평가 순서대로 쌓은 세 티어. 각 줄은 이름 · 규칙의 주인 · 규칙이 하는 일을 같은 자리에 반복한다.
#           focal 은 개발자가 쓰는 NetworkPolicy 티어 하나. 출처: network-policy-api.sigs.k8s.io/api-overview (2026-11-08 조회)
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 628
d = D(W, H, "CLUSTERNETWORKPOLICY · THREE TIERS",
      "클러스터 관리자의 규칙이 개발자의 NetworkPolicy 앞뒤에 놓인다",
      "트래픽은 Admin 티어, NetworkPolicy 티어, Baseline 티어 순으로 평가된다. ClusterNetworkPolicy 는 Admin 과 Baseline 두 티어를 쓰고 "
      "액션은 Accept·Deny·Pass 이며 Pass 는 현재 티어의 남은 규칙을 건너뛰어 다음 티어로 넘긴다.",
      lead="Admin 이 Accept·Deny 로 판정하지 않은 트래픽만 개발자의 정책에 닿습니다")

COL = [(40, 252), (332, 344), (716, 244)]
HY, Y0, RH, STRIDE = 136, 152, 104, 140
for (x, w), name in zip(COL, ("티어", "규칙", "넘기는 조건")):
    d.t(x + w // 2, HY, name, 12, SOFT, KR, "middle", 600)

TIERS = [
    ("1 · Admin 티어", "ClusterNetworkPolicy", INFO,
     ("priority 값이 작은 정책 먼저", "액션 Accept · Deny · Pass"),
     ("Pass 는 남은 규칙을 건너뜀", "다음 티어로 넘김")),
    ("2 · NetworkPolicy 티어", "네임스페이스 개발자의 정책", ACC,
     ("선택된 Pod 는 허용 목록만 통과", "선택 안 된 Pod 는 Baseline 으로"),
     ("선택되지 않은 Pod 는", "다음 티어로 넘어감")),
    ("3 · Baseline 티어", "ClusterNetworkPolicy", WARN,
     ("priority 값이 작은 정책 먼저", "앞 티어가 판정하지 않은 트래픽"),
     ("마지막 티어", "더 넘길 곳이 없음")),
]
for i, (name, owner, c, rule, nxt) in enumerate(TIERS):
    y = Y0 + i * STRIDE
    focal = c is ACC
    for j, (x, w) in enumerate(COL):
        if focal:
            d.tone(x, y, w, RH, ACC, 6, "1F", 1.6)
        else:
            d.box(x, y, w, RH, PAPER2, c if j == 0 else RULE, 1.2 if j == 0 else 0.9, 6)
    tc = ACC if focal else INK
    x, w = COL[0]
    d.t(x + 20, y + 40, ddx.fit(name, 14, w - 36, name), 14, tc, KR, "start", 600)
    d.t(x + 20, y + 68, ddx.fit(owner, 12, w - 36, owner), 12, ACC if focal else MUTED, KR, "start")
    x, w = COL[1]
    d.t(x + 20, y + 44, ddx.fit(rule[0], 13, w - 36, rule[0]), 13, tc, KR, "start", 600)
    d.t(x + 20, y + 72, ddx.fit(rule[1], 12, w - 36, rule[1]), 12, MUTED, KR, "start")
    x, w = COL[2]
    d.t(x + 20, y + 44, ddx.fit(nxt[0], 13, w - 36, nxt[0]), 13, tc, KR, "start", 600)
    d.t(x + 20, y + 72, ddx.fit(nxt[1], 12, w - 36, nxt[1]), 12, MUTED, KR, "start")
    if i < 2:
        ax = COL[0][0] + COL[0][1] // 2
        d.arrow([(ax, y + RH + 3), (ax, y + STRIDE - 5)], SOFT, "soft", 1.4)

d.t(40, Y0 + 3 * STRIDE - 16, "ClusterNetworkPolicy 는 선택한 Pod 를 암묵적으로 격리하지 않음", 12, MUTED, KR, "start")
d.legend(588, [("관리자의 앞 규칙", INFO), ("개발자의 정책", ACC), ("관리자의 뒤 규칙", WARN)])
d.save("04-03.cluster-network-policy.svg")
print("ok cluster-network-policy")
