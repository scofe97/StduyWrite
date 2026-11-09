# 04-01 §1 — 인증서의 principal 이 계정의 principal 파일과 맞아야 세션이 열린다.
# 타입 스펙: type-process — 확인 세 칸을 화살표가 잇고, 아래 두 호스트 표가 같은 슬롯(계정 · 파일 내용)으로 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 452
d = D(W, H, "LAMPSON LAB · 04-01 §1",
      "principal 이 역할 계정을 연다 — 확인 세 칸",
      "sshd 는 서명한 CA, 로그인 계정 이름, 그 계정의 principal 파일을 차례로 보고 마지막에 기간을 본다. 아래는 두 호스트의 파일 내용이다.",
      "계정 이름은 로그인하는 쪽이 고르고, principal 은 CA 가 정한다 — 둘이 파일에서 만난다")

CW, CH, GAP, X0, Y = 232, 100, 48, 24, 96
steps = [
    ("1 서명", "user_ca.pub 의 CA 가", "서명했는가"),
    ("2 계정", "operator@host-billing", "→ auth_principals/operator"),
    ("3 이름", "인증서 principal 이 파일에 적혀", "있는가 · 그다음 기간 안인가"),
]
for i, (name, a, b) in enumerate(steps):
    x = X0 + i * (CW + GAP)
    focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 28, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 56, a, 12, MUTED, KR, "start")
    d.t(x + 16, Y + 78, b, 12, MUTED, KR, "start")
    if i < 2:
        d.arrow([(x + CW + 4, Y + CH / 2), (x + CW + GAP - 4, Y + CH / 2)], MUTED, "ar", 1.4)

# 호스트 두 곳의 principal 파일 내용
TW, TX = 416, (24, 440)
TY = 232
rows = ["admin", "operator", "readonly"]
for k, grp in enumerate(["billing", "crm"]):
    x = TX[k]
    d.t(x, TY - 12, f"host-{grp}  (HOST_GROUP={grp})", 12, INK, MONO, "start", 600)
    for j, acct in enumerate(rows):
        y = TY + j * 40
        hit = (grp == "billing" and acct == "operator")
        if hit:
            d.o.append(f'<rect x="{x}" y="{y}" width="{TW}" height="32" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.2"/>')
        else:
            d.box(x, y, TW, 32, PAPER2, RULE, 1.0, 6)
        d.t(x + 12, y + 21, f"auth_principals/{acct}", 11, ACC if hit else MUTED, MONO, "start")
        d.t(x + TW - 12, y + 21, f"role-{acct}@{grp}", 11, ACC if hit else INK, MONO, "end", 600 if hit else 400)

d.t(24, 396, "deployer 의 인증서는 role-operator@billing 하나뿐이라 강조한 한 줄에서만 통과한다", 12, SOFT, KR, "start")
d.t(24, 420, "admin 파일의 role-admin@… 는 CA 가 어떤 신원에게도 발급하지 않는다", 12, SOFT, KR, "start")
d.save("04-01.principal-files.svg")
