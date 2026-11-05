# 05-01 §1 — 파드 수준 securityContext 와 컨테이너 수준 securityContext 가 겹치면 컨테이너 값이 이긴다.
# 본문 근거: 이 노트 ### 1 「securityContext 로 컨테이너의 OS 권한 정하기」.
# 검증 근거: kind v1.35.0(kubectl 1.33)에서 파드 runAsUser 1000·runAsGroup 3000·fsGroup 2000, 컨테이너 runAsUser 1500 으로
#            파드를 띄우고 `id` 가 uid=1500 gid=3000 groups=2000,3000 을 내는 것을 확인.
# 공식 근거: kubernetes.io 「Configure a Security Context for a Pod or Container」 — 컨테이너 설정은 겹칠 때 파드 설정을 덮어쓴다.
# 타입 스펙: type-data-flow — 두 입력(파드·컨테이너)이 한 결과(프로세스의 실제 값)로 모인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 372
d = D(W, H, "CKS STUDY GUIDE · 05-01 §1",
      "securityContext 가 합쳐지는 길",
      "파드의 securityContext 와 컨테이너의 securityContext 가 한 컨테이너 프로세스의 uid, gid, 보조 그룹으로 합쳐지는 도식이다. "
      "같은 필드가 겹치면 컨테이너 값이 파드 값을 덮어쓰고, 겹치지 않는 필드는 그대로 남는다.",
      "같은 필드가 겹치면 컨테이너 값이 이기고, 겹치지 않는 필드는 파드 값이 그대로 남습니다")

PX, PW = 24, 316
RX, RW = 484, 372


def card(y, h, title, rows, c):
    d.tone(PX, y, PW, h, c, 6, "14", 1.2)
    d.t(PX + 14, y + 24, title, 13, INK, KR, "start", 600)
    for i, (k, v) in enumerate(rows):
        d.t(PX + 14, y + 50 + i * 22, k, 11, MUTED, MONO, "start")
        d.t(PX + PW - 14, y + 50 + i * 22, v, 11, INK, MONO, "end")


card(96, 112, "파드 spec.securityContext",
     [("runAsUser", "1000"), ("runAsGroup", "3000"), ("fsGroup", "2000")], INFO)
card(228, 70, "컨테이너 securityContext", [("runAsUser", "1500")], SOFT)

# 합류 화살표
d.path(f"M {PX + PW + 2} 152 L 380 152 L 380 214 L {RX - 2} 214", MUTED, 1.4, m="ar")
d.path(f"M {PX + PW + 2} 263 L 424 263 L 424 150 L {RX - 2} 150", ACC, 1.6, m="acc")
d.chip(424, 250, "덮어씀", ACC, 11)

# 결과 카드
d.tone(RX, 96, RW, 202, ACC, 6, "14", 1.4)
d.t(RX + 14, 120, "컨테이너 프로세스의 실제 값", 13, INK, KR, "start", 600)
rows = [("uid=1500", "컨테이너 runAsUser 가 이김"),
        ("gid=3000", "겹치지 않아 파드 값 그대로"),
        ("groups=2000,3000", "fsGroup 이 보조 그룹으로 붙음")]
for i, (k, v) in enumerate(rows):
    y = 154 + i * 44
    d.t(RX + 14, y, k, 12, INK, MONO, "start", 600)
    d.t(RX + 14, y + 20, v, 11, MUTED, KR, "start")

d.legend(318, [("파드 수준", INFO), ("컨테이너 수준", SOFT), ("합친 결과", ACC)])
d.save("05-01.security-context-merge.svg")
