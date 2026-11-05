# 03-01 §2 — 사람 사용자는 클러스터에 오브젝트가 없다. 개인 키 → CSR → 승인 → 인증서 → kubeconfig 사용자 순으로 신원을 만든다.
# 본문 근거: 이 노트 §2 「사람 사용자는 개인 키와 승인된 인증서로 만듭니다」.
# 검증 근거: kind v1.35.0 에서 openssl genrsa · req, CertificateSigningRequest(signerName kubernetes.io/kube-apiserver-client,
#            expirationSeconds 86400, usages client auth), kubectl certificate approve, set-credentials, auth whoami 를 실행.
# 타입 스펙: type-swimlane — 내 컴퓨터와 클러스터 두 레인을 오가는 순차 단계가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 448
d = D(W, H, "CKS STUDY GUIDE · 03-01 §2",
      "개인 키에서 kubeconfig 사용자까지",
      "내 컴퓨터에서 개인 키와 CSR 을 만들고, 클러스터에서 CertificateSigningRequest 를 승인해 인증서를 받아 와 "
      "kubeconfig 사용자로 등록하는 흐름을 두 레인으로 그린 도식이다.",
      "클러스터로 나가는 것은 CSR 하나뿐이고 개인 키는 내 컴퓨터에 남습니다")

BW, BH, PITCH, X0 = 126, 76, 141, 24
LANE_X, LANE_W = 12, 856
LOC_Y, CLU_Y, LANE_H = 96, 240, 132


def col(i):
    return X0 + i * PITCH


def lane(y, name, c):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{c}0A" stroke="{c}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, c, KR, "start", 600)


def step(i, y, title, sub, c, mono_sub=True, tsize=13):
    x = col(i)
    d.tone(x, y, BW, BH, c, 6, "14", 1.1)
    d.t(x + BW / 2, y + 32, title, tsize, INK, KR, "middle", 600)
    d.t(x + BW / 2, y + 56, sub, 11, MUTED, MONO if mono_sub else KR)


lane(LOC_Y, "내 컴퓨터", INFO)
lane(CLU_Y, "클러스터", SOFT)
LY = LOC_Y + 40
CY = CLU_Y + 40

step(0, LY, "개인 키", "jill.key", INFO)
step(1, LY, "CSR 파일", "jill.csr", INFO)
step(4, LY, "인증서 파일", "jill.crt", INFO)
step(5, LY, "kubeconfig", "사용자 jill", INFO)
step(2, CY, "CSR 오브젝트", "Pending", SOFT)
step(3, CY, "승인", "Approved,Issued", OK)
step(5, CY, "RoleBinding", "group observer", SOFT)

mid = LY + BH / 2
cmid = CY + BH / 2
# 같은 레인 안
d.path(f"M {col(0) + BW} {mid} L {col(1) - 2} {mid}", MUTED, 1.4, m="ar")
d.path(f"M {col(2) + BW} {cmid} L {col(3) - 2} {cmid}", MUTED, 1.4, m="ar")
d.path(f"M {col(4) + BW} {mid} L {col(5) - 2} {mid}", MUTED, 1.4, m="ar")
# 레인 넘기: CSR 내려가기(focal)
cx2 = col(2) + BW / 2
d.path(f"M {col(1) + BW} {mid} L {cx2} {mid} L {cx2} {CY - 2}", ACC, 1.8, m="acc")
d.chip(cx2, LOC_Y + LANE_H + 7, "개인 키 미전송", ACC, 11)
# 승인 → 인증서 올라오기
cx4 = col(4) + BW / 2
d.path(f"M {col(3) + BW} {cmid} L {cx4} {cmid} L {cx4} {LY + BH + 2}", MUTED, 1.4, m="ar")
d.t(cx4 - 8, CLU_Y + 30, "status.certificate", 11, MUTED, MONO, "end")
# kubeconfig 사용자 → 권한 확인
cx5 = col(5) + BW / 2
d.path(f"M {cx5} {LY + BH} L {cx5} {CY - 2}", MUTED, 1.2, m="ar", dash="4 4")
d.chip(cx5, LOC_Y + LANE_H + 7, "auth can-i", MUTED, 11)

d.legend(396, [("내 컴퓨터 쪽", INFO), ("클러스터 쪽", SOFT), ("관리자 승인", OK), ("키가 나가지 않는 전달", ACC)])
d.save("03-01.csr-user-flow.svg")
