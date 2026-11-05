# 03-01 §3 — 파드는 기본으로 ServiceAccount 토큰 볼륨을 받고, automountServiceAccountToken: false 로 그 볼륨이 통째로 빠진다.
# 본문 근거: 이 노트 §3 「ServiceAccount 토큰은 기본으로 파드에 들어옵니다」.
# 검증 근거: kind v1.35.0 에서 Pod 의 volumes 에 kube-api-access-<suffix> 가 생기고 ca.crt · namespace · token 이 마운트됨을 확인,
#            automountServiceAccountToken: false 파드에는 볼륨과 /var/run/secrets/kubernetes.io/serviceaccount 가 없음을 확인.
# 공식 근거: kubernetes.io/docs/concepts/security/service-accounts/ — ServiceAccount 어드미션 컨트롤러가 파드에 투사 볼륨을 추가하고 kubelet 이 TokenRequest 로 받은 serviceAccountToken · configMap kube-root-ca.crt · downwardAPI 를 투사.
# 타입 스펙: type-architecture — 같은 ServiceAccount 와 파드를 두 상태로 맞대어 구성요소의 있고 없음을 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 448
d = D(W, H, "CKS STUDY GUIDE · 03-01 §3",
      "ServiceAccount 토큰이 파드에 들어가는 길",
      "같은 ServiceAccount api-call 과 Pod service-list 를 기본 상태와 automountServiceAccountToken: false 상태로 나란히 놓고, "
      "볼륨이 마운트되는 모양과 빠지는 모양, 파드 밖에서 쓸 토큰을 따로 발급하는 길을 그린 도식이다.",
      "자동 마운트를 끄면 토큰 볼륨뿐 아니라 ca.crt 도 함께 빠집니다")


def panel(x, title, fam):
    d.box(x, 104, 420, 280, PAPER2, RULE, 0.9, 8)
    d.t(x + 16, 128, title, 12, MUTED, fam, "start", 600)


def sa(x):
    d.box(x, 142, 364, 46, PAPER2, RULE, 1.0, 6)
    d.t(x + 182, 171, "ServiceAccount api-call", 14, INK, KR, "middle", 600)


# 왼쪽 — 기본
panel(12, "기본 동작", KR)
sa(40)
d.path("M 222 188 L 222 230", MUTED, 1.4, m="ar")
d.box(40, 232, 364, 140, PAPER2, RULE, 1.0, 8)
d.t(56, 256, "Pod service-list", 14, INK, KR, "start", 600)
d.tone(56, 266, 332, 78, WARN, 6, "14", 1.1)
d.t(68, 285, "volume kube-api-access-<suffix>", 11, WARN, MONO, "start", 600)
for j, txt in enumerate(["serviceAccountToken", "configMap kube-root-ca.crt", "downwardAPI namespace"]):
    d.t(68, 304 + j * 16, txt, 11, MUTED, MONO, "start")
d.t(56, 362, "/var/run/secrets/kubernetes.io/serviceaccount", 11, MUTED, MONO, "start")

# 오른쪽 — 자동 마운트 끔
panel(448, "automountServiceAccountToken: false", MONO)
sa(476)
d.path("M 566 188 L 566 230", MUTED, 1.4, m="ar")
d.box(476, 232, 180, 140, PAPER2, RULE, 1.0, 8)
d.t(492, 256, "Pod service-list", 14, INK, KR, "start", 600)
d.tone(492, 266, 148, 78, OK, 6, "14", 1.1)
d.t(566, 301, "볼륨 없음", 14, OK, KR, "middle", 600)
d.t(566, 322, "마운트 경로 없음", 12, MUTED, KR)

d.path("M 764 188 L 764 230", ACC, 1.6, m="acc")
d.chip(764, 209, "kubectl create token", ACC, 11)
d.box(688, 232, 152, 140, PAPER2, RULE, 1.0, 8)
d.t(764, 258, "클러스터 밖 호출자", 13, INK, KR, "middle", 600)
d.t(764, 280, "CI · curl", 12, MUTED, MONO)
d.t(764, 316, "Authorization:", 11, MUTED, MONO)
d.t(764, 334, "Bearer <token>", 11, MUTED, MONO)

d.legend(404, [("자동 마운트된 볼륨", WARN), ("마운트 없음", OK), ("토큰 발급", ACC)])
d.save("03-01.sa-token-mount.svg")
