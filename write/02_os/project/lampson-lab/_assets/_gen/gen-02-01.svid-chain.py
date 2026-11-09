# 02-01 §1 — SVID 가 랩 루트까지 이어지는 서명 체인.
# 타입 스펙: type-process — 서명이 한 방향으로 내려가는 네 칸을 화살표가 잇고,
#           칸마다 누가 만들었는지 · 수명이 같은 슬롯으로 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 366
d = D(W, H, "LAMPSON LAB · 02-01 §1",
      "SVID 에서 랩 루트까지 — 서명 체인",
      "랩 루트가 SPIRE 중간 인증서를 서명하고, SPIRE server 의 CA 가 SVID 를 서명한다. step-ca 는 이 체인의 맨 위 하나만 믿는다.",
      "SPIRE 가 CA 키를 바꿔도 맨 위 랩 루트가 그대로라서 step-ca 설정은 흔들리지 않는다")

CW, CH, GAP, X0 = 176, 112, 52, 12
CY = 112
cards = [
    ("랩 루트", ["bootstrap 이 생성", "SPIRE 밖에서 만든 뿌리"]),
    ("SPIRE 중간 인증서", ["랩 루트가 서명", "UpstreamAuthority disk"]),
    ("SPIRE server CA", ["ca_ttl 24h", "ec-p256 키"]),
    ("SVID", ["deployer 5분", "monitor 15분"]),
]

def cx(i):
    return X0 + i * (CW + GAP)

for i, (name, lines) in enumerate(cards):
    x = cx(i)
    focal = (i == 0)
    if focal:
        d.o.append(f'<rect x="{x}" y="{CY}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, CY, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 14, CY + 28, name, 13, ACC if focal else INK, KR, "start", 600)
    for j, ln in enumerate(lines):
        d.t(x + 14, CY + 56 + j * 22, ln, 11, MUTED, KR, "start")

for i in range(3):
    x1, x2 = cx(i) + CW, cx(i + 1)
    d.arrow([(x1 + 3, CY + CH / 2), (x2 - 4, CY + CH / 2)], MUTED, "ar", 1.4)
    d.t((x1 + x2) / 2, CY + CH / 2 - 10, "서명", 11, MUTED, KR, "middle")

# 맨 위 하나만 믿는다 — step-ca 의 X5C roots
bx = cx(0)
d.path(f"M {bx + CW / 2} {CY + CH} V {CY + CH + 40}", ACC, 1.4, m="acc")
d.t(bx + 14, CY + CH + 62, "step-ca X5C provisioner 의 roots", 12, ACC, KR, "start", 600)
d.t(bx + 14, CY + CH + 82, "= 랩 루트 하나", 12, ACC, MONO, "start")

d.t(12, 346, "AC-01 이 SVID 마다 랩 루트까지 체인이 이어지는지 확인한다", 12, SOFT, KR, "start")
d.save("02-01.svid-chain.svg")
