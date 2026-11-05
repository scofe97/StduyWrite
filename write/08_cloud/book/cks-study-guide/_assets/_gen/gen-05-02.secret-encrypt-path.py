# 05-02 §1 — Secret 은 API 서버가 첫 provider 로 암호화해 etcd 에 쓰고, 읽을 때 접두어가 가리키는 키로 복호화한다.
# 본문 근거: 이 노트 ### 1 「1. etcd 암호화로 Secret 지키기」.
# 검증 근거: kind v1.35.0 에서 aescbc EncryptionConfiguration 을 kube-apiserver 정적 파드에 연결하고,
#            etcdctl 로 새 Secret 의 값이 k8s:enc:aescbc:v1:key1: 접두어로 시작하는 암호문임을 확인.
#            기존 Secret 은 kubectl replace 뒤에 같은 접두어로 바뀌는 것을 확인.
# 공식 근거: kubernetes.io 「Encrypting Confidential Data at Rest」.
# 타입 스펙: type-swimlane — 쓰기·읽기·etcd 직접 읽기 세 레인이 같은 열 격자 위에서 오간다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 552
d = D(W, H, "CKS STUDY GUIDE · 05-02 §1",
      "Secret 이 etcd 에 쓰이고 읽히는 길",
      "kubectl 이 보낸 Secret 을 kube-apiserver 가 EncryptionConfiguration 의 첫 provider 로 암호화해 etcd 에 쓰고, "
      "읽을 때는 접두어가 가리키는 키로 복호화하는 두 레인과, etcdctl 로 etcd 를 직접 읽으면 접두어와 암호문만 보이는 레인을 그린 도식이다.",
      "키는 API 서버 설정 파일에만 있으므로 etcd 데이터만 손에 넣어서는 평문을 얻지 못합니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 120
W_Y, R_Y, E_Y = 96, 232, 368


def col(i):
    return X0 + i * PITCH


def lane(y, name, c=SOFT):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{c}0A" stroke="{c}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def box(i, y, title, sub, c, mono=True):
    x, by = col(i), y + 34
    d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
    d.t(x + BW / 2, by + 32, title, 13, INK, KR, "middle", 600)
    d.t(x + BW / 2, by + 56, sub, 11, MUTED, MONO if mono else KR)


def right(i, y):
    my = y + 34 + BH / 2
    d.path(f"M {col(i) + BW + 2} {my} L {col(i + 1) - 2} {my}", MUTED, 1.4, m="ar")


def left(i, y):
    my = y + 34 + BH / 2
    d.path(f"M {col(i + 1) - 2} {my} L {col(i) + BW + 2} {my}", MUTED, 1.4, m="ar")


lane(W_Y, "쓰기")
box(0, W_Y, "kubectl", "create secret", INFO)
box(1, W_Y, "kube-apiserver", "EncryptionConfiguration", SOFT)
box(2, W_Y, "첫 provider 로 암호화", "aescbc · key1", ACC)
box(3, W_Y, "etcd", "k8s:enc:aescbc:v1:key1:", SOFT)
for i in range(3):
    right(i, W_Y)

lane(R_Y, "읽기")
box(0, R_Y, "kubectl", "get secret", INFO)
box(1, R_Y, "kube-apiserver", "평문 Secret 응답", SOFT, False)
box(2, R_Y, "접두어의 키로 복호화", "aescbc · key1", ACC)
box(3, R_Y, "etcd", "접두어 + 암호문", SOFT, False)
for i in range(3):
    left(i, R_Y)

lane(E_Y, "컨트롤 플레인 노드에서 etcd 를 직접 읽을 때 (암호화를 켠 뒤)", WARN)
box(2, E_Y, "etcdctl get", "--cacert --cert --key", WARN)
box(3, E_Y, "접두어 + 암호문", "키 파일 없이는 읽을 수 없음", SOFT, False)
right(2, E_Y)

d.legend(504, [("명령을 내는 쪽", INFO), ("API 서버·저장소", SOFT), ("암호화·복호화", ACC), ("etcd 직접 접근", WARN)])
d.save("05-02.secret-encrypt-path.svg")
