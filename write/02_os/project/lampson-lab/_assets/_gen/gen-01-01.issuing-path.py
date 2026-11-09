# 01-01 §4 — uid 에서 sshd 세션까지 값이 바뀌는 한 줄 경로.
# 타입 스펙: type-process — 값 다섯 칸을 화살표 넷이 잇고, 화살표마다 일하는 쪽(위)과
#           그 걸음에서 걸리는 계정(아래)이 같은 슬롯으로 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 392
d = D(W, H, "LAMPSON LAB · 01-01 §4",
      "uid 에서 세션까지 — 값이 바뀌는 다섯 칸",
      "프로세스의 uid 가 SVID, X5C 토큰, SSH 인증서를 거쳐 역할 계정 세션이 된다. 화살표 위는 일하는 쪽, 아래는 거기서 걸리는 계정.",
      "요청에는 신원을 적는 칸이 없다 — 첫 화살표에서 커널이 uid 를 확인한다")

CW, CH, GAP, X0 = 140, 128, 40, 12
CY = 150
cards = [
    ("1 프로세스", ["uid 1001", "deployer 계정"], False),
    ("2 SVID", ["spiffe://lab/", "client/deployer", "수명 5분"], False),
    ("3 X5C 토큰", ["SVID 를 첨부", "SVID 키로 서명", "공개키와 함께 전송"], False),
    ("4 SSH 인증서", ["KeyID = SPIFFE ID", "role-operator", "@billing · ≤ 5분"], False),
    ("5 세션", ["operator@", "host-billing", "uid 1001(operator)"], False),
]
# 화살표 위(일하는 쪽) · 아래(걸리는 계정)
hops = [
    ("spire-agent", "커널에 uid 확인", ("intruder", "no identity issued")),
    ("lab-ssh-cert", "SVID 키로 서명", None),
    ("step-ca", "매핑이 principal 결정", ("stranger", "no SSH mapping")),
    ("sshd", "CA 서명 · principal 확인", ("admin@", "Permission denied")),
]

def cx(i):
    return X0 + i * (CW + GAP)

for i, (name, lines, focal) in enumerate(cards):
    x = cx(i)
    d.box(x, CY, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 12, CY + 26, name, 13, INK, KR, "start", 600)
    for j, ln in enumerate(lines):
        d.t(x + 12, CY + 54 + j * 22, ln, 11, MUTED, MONO, "start")

for i, (who, what, deny) in enumerate(hops):
    x1 = cx(i) + CW
    x2 = cx(i + 1)
    mx = (x1 + x2) / 2
    first = (i == 0)
    col = ACC if first else MUTED
    mk = "acc" if first else "ar"
    d.arrow([(x1 + 3, CY + CH / 2), (x2 - 4, CY + CH / 2)], col, mk, 1.6 if first else 1.4)
    # 위: 일하는 쪽
    d.line(mx, CY + CH / 2 - 8, mx, 130, RULE, 0.8)
    d.t(mx, 124, who, 12, ACC if first else INK, MONO, "middle", 600)
    d.t(mx, 108, what, 11, ACC if first else MUTED, KR, "middle")
    # 아래: 걸리는 계정
    if deny:
        acct, why = deny
        d.line(mx, CY + CH / 2 + 8, mx, CY + CH + 30, RULE, 0.8, "3 4")
        d.t(mx, CY + CH + 48, acct, 12, INK, MONO, "middle", 600)
        d.t(mx, CY + CH + 66, why, 11, MUTED, MONO, "middle")

d.t(12, 372, "거부는 사유가 남는다 — 마지막 줄은 각 걸음에서 계정이 받는 응답 문구다", 12, SOFT, KR, "start")
d.save("01-01.issuing-path.svg")
