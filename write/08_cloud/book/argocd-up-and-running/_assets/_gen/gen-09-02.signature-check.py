# 09-02 §2 — 프로젝트에 소스 무결성 정책이 있으면 repo-server 가 대상 리비전의 GnuPG 서명을 키링과 대조하고, 프로젝트 정책의 키 목록과 한 번 더 대조한다. 서명이 없거나 공개 키가 키링에 없거나 허용 목록 밖의 키이면 ComparisonError 로 거부된다.
# 본문 근거: 이 노트 ### 2 「GPG 서명 검증」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 클러스터 안 SSH Git 서버의 저장소를 소스로 삼아 확인했다.
#            AppProject 에 sourceIntegrity.git.policies 의 gpg(mode head, keys [키 A])를 두고 대상 리비전만 바꿔 가며 확인한 결과는 다음과 같다.
#            서명 없는 커밋은 `GIT/GPG: Failed verifying revision … unsigned (key_id=)`, 공개 키를 아직 등록하지 않은 키로 서명한 커밋은 `signed with key not in keyring (key_id=…)`,
#            키링에는 있으나 정책 keys 에 없는 키(키 B)로 서명한 커밋은 `signed with unallowed key (key_id=…)` 였다. 키 A 로 서명한 커밋만 sync 가 Succeeded 였다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/source-integrity.md, docs/user-guide/source-integrity-git-gpg.md("The `gpg` verification policy").
# 타입 스펙: type-architecture — 왼쪽 요청에서 오른쪽 판정으로 가는 한 방향 흐름, 가운데 칸 아래로 갈라지는 거부 세 가지.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 440
d = D(W, H, "ARGO CD UP AND RUNNING · 09-02 §2",
      "커밋이 서명 검증을 지나는 길",
      "왼쪽의 대상 리비전은 먼저 repo-server 의 GnuPG 키링에서 서명을 확인받는다. 서명이 없으면 unsigned, 서명한 공개 키가 키링에 없으면 key not in keyring 으로 거부된다. "
      "키링에서 확인된 서명은 프로젝트 정책의 키 목록과 한 번 더 대조된다. 목록에 없는 키이면 unallowed key 로 거부되고, 목록에 있는 키이면 허용되어 sync 가 진행된다.",
      "서명은 키링과 프로젝트 정책에서 두 번 걸러집니다")

A_X, A_W = 24, 150
B_X, B_W = 214, 200
C_X, C_W = 454, 216
O_X, O_W = 708, 148
MID = 170
BOX_Y, BOX_H = 112, 116

# 대상 리비전
d.tone(A_X, BOX_Y, A_W, BOX_H, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, BOX_Y + 36, "대상 리비전", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, BOX_Y + 64, "브랜치·태그·커밋", 12, MUTED)
d.t(A_X + A_W / 2, BOX_Y + 90, "targetRevision", 11.5, MUTED, MONO)

# 키링 확인
d.box(B_X, BOX_Y, B_W, BOX_H, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, BOX_Y + 36, "서명 확인", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, BOX_Y + 64, "repo-server 의 GnuPG 키링", 12, MUTED)
d.t(B_X + B_W / 2, BOX_Y + 90, "argocd-gpg-keys-cm", 11.5, MUTED, MONO)

# 정책 대조
d.tone(C_X, BOX_Y, C_W, BOX_H, ACC, 6, "14", 1.4)
d.t(C_X + C_W / 2, BOX_Y + 36, "정책 키 대조", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, BOX_Y + 64, "프로젝트가 믿는 키 목록", 12, MUTED)
d.t(C_X + C_W / 2, BOX_Y + 90, "sourceIntegrity.git.policies", 11.5, MUTED, MONO)

# 허용
d.tone(O_X, BOX_Y + 28, O_W, 60, OK, 6, "14", 1.2)
d.t(O_X + O_W / 2, BOX_Y + 56, "허용", 12.5, INK, KR, "middle", 600)
d.t(O_X + O_W / 2, BOX_Y + 76, "sync 진행", 12, MUTED)

# 화살표
d.path(f"M {A_X + A_W + 2} {MID} L {B_X - 2} {MID}", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W + 2} {MID} L {C_X - 2} {MID}", MUTED, 1.4, m="ar")
d.path(f"M {C_X + C_W + 2} {MID} L {O_X - 2} {MID}", MUTED, 1.4, m="ar")

# 거부 세 가지
RY, RH = 290, 62
rejects = [
    (24, 176, B_X + 40, "서명 없음", "unsigned"),
    (214, 200, B_X + B_W / 2 + 40, "키링에 없는 키", "key not in keyring"),
    (454, 216, C_X + C_W / 2, "허용되지 않은 키", "unallowed key"),
]
d.t(484, 272, "ComparisonError", 11.5, BAD, MONO)
for x, w, sx, t1, t2 in rejects:
    d.tone(x, RY, w, RH, BAD, 6, "14", 1.2)
    d.t(x + w / 2, RY + 28, t1, 12.5, INK, KR, "middle", 600)
    d.t(x + w / 2, RY + 49, t2, 11.5, MUTED, MONO)
cx_a = rejects[0][0] + rejects[0][1] / 2
d.path(f"M {B_X + 40} {BOX_Y + BOX_H + 2} L {B_X + 40} 258 L {cx_a} 258 L {cx_a} {RY - 2}", MUTED, 1.4, m="ar")
cx_b = rejects[1][0] + rejects[1][1] / 2
d.path(f"M {cx_b + 40} {BOX_Y + BOX_H + 2} L {cx_b + 40} {RY - 2}", MUTED, 1.4, m="ar")
cx_c = rejects[2][0] + rejects[2][1] / 2
d.path(f"M {cx_c} {BOX_Y + BOX_H + 2} L {cx_c} {RY - 2}", MUTED, 1.4, m="ar")

d.legend(388, [("리비전", INFO), ("키링 확인", PAPER2), ("정책 대조", ACC), ("허용", OK), ("거부", BAD)])
d.save("09-02.signature-check.svg")
