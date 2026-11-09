# 03-01 §2 — principal 이 요청이 아니라 SVID 의 신원에서 정해지는 흐름.
# 타입 스펙: type-process — 보내는 것 · 정하는 것 · 발급되는 것 세 칸을 화살표가 잇고,
#           칸마다 같은 슬롯(이름 · 줄 셋)이 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 372
d = D(W, H, "LAMPSON LAB · 03-01 §2",
      "요청이 가져가는 것과 돌려받는 것",
      "클라이언트는 X5C 토큰과 principal 요청을 보내고, step-ca 는 SVID 의 SPIFFE ID 로 매핑 한 행을 찾아 그 행대로 인증서를 만든다.",
      "요청한 principal 은 매핑 행 안에 있는지 대조될 뿐 발급 내용을 정하지 않는다")

CW, CH, GAP, X0 = 262, 150, 35, 12
CY = 100
cards = [
    ("클라이언트가 보내는 것", ["X5C 토큰 (SVID 첨부)", "요청 principal 하나 이상", "KeyID = SVID 의 SPIFFE ID"], False),
    ("step-ca 가 정하는 것", ["신원 = 검증된 SVID 의 ID", "매핑 표에서 한 행 찾기", "요청은 그 행 안인지만 대조"], True),
    ("발급되는 인증서", ["KeyID = SPIFFE ID", "principals = 매핑 행 전체", "수명 ≤ 5분 · SVID 수명 안"], False),
]

def cx(i):
    return X0 + i * (CW + GAP)

for i, (name, lines, focal) in enumerate(cards):
    x = cx(i)
    if focal:
        d.o.append(f'<rect x="{x}" y="{CY}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, CY, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, CY + 30, name, 13, ACC if focal else INK, KR, "start", 600)
    for j, ln in enumerate(lines):
        d.t(x + 16, CY + 62 + j * 28, ln, 12, MUTED, KR, "start")

for i in range(2):
    x1, x2 = cx(i) + CW, cx(i + 1)
    d.arrow([(x1 + 3, CY + CH / 2), (x2 - 4, CY + CH / 2)], ACC if i == 0 else MUTED, "acc" if i == 0 else "ar", 1.5)

# 예시 띠 — 요청 하나가 매핑 행 전체가 되는 경우 (AC-04)
EY = 290
d.box(12, EY, W - 24, 52, PAPER2, RULE, 1.0, 8)
d.t(28, EY + 22, "monitor 가 role-readonly@crm 하나만 요청해도", 12, INK, KR, "start", 600)
d.t(28, EY + 42, "→ role-readonly@billing, role-readonly@crm 둘이 발급된다 (AC-04)", 12, MUTED, KR, "start")
d.save("03-01.principal-flow.svg")
