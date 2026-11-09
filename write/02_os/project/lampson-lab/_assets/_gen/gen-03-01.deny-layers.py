# 03-01 §3 — 요청이 거부되는 네 층과 각 층이 남기는 응답 문구.
# 타입 스펙: type-layers — 층 넷이 세로로 쌓이고, 층마다 무엇을 보는지 · 걸렸을 때 남는 문구 ·
#           확인하는 AC 가 같은 열로 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 560
d = D(W, H, "LAMPSON LAB · 03-01 §3",
      "거부가 일어나는 네 층",
      "토큰, 템플릿, policy, 수명이 각각 다른 것을 보고, 걸리면 층마다 다른 문구로 거부한다. 순서는 가정하지 않는다.",
      "신원과 매핑을 읽는 층은 템플릿이다 — 거부 문구의 대부분이 여기서 나온다")

X0, RW, RH, GAP = 12, W - 24, 96, 10
Y0 = 104
d.t(X0 + 16, Y0 - 8, "층", 11, SOFT, KR, "start")
d.t(X0 + 176, Y0 - 8, "무엇을 보나", 11, SOFT, KR, "start")
d.t(X0 + 436, Y0 - 8, "걸렸을 때 남는 문구", 11, SOFT, KR, "start")
rows = [
    ("1 X5C 토큰", "AC-08 · AC-10",
     ["체인이 랩 루트로 이어지나", "토큰을 한 번만 쓰나"],
     ["error verifying x5c certificate", "chain in token", "token already used"], False),
    ("2 템플릿", "AC-06 · AC-07",
     ["신원이 매핑에 있나", "요청 principal 이 매핑 안인가", "KeyID 가 SPIFFE ID 인가"],
     ["has no SSH mapping", "is not mapped for", "key id ... is not the SVID's SPIFFE ID"], True),
    ("3 policy", "AC-05",
     ["role-admin 은 deny 목록", "허용 목록 밖은 서명하지 않음"],
     ['email name "..." not allowed', "실제 step-ca 에서는 템플릿이 먼저", "is never issued 로 막음"], False),
    ("4 수명", "AC-09",
     ["인증서 끝 ≤ SVID 만료 시각", "요청 길이 ≤ 5분 상한"],
     ["provisioning credential expiration", "greater than maximum accepted duration", "for selected provisioner of 5m"], False),
]
for i, (name, ac, what, resp, focal) in enumerate(rows):
    y = Y0 + i * (RH + GAP)
    if focal:
        d.o.append(f'<rect x="{X0}" y="{y}" width="{RW}" height="{RH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(X0, y, RW, RH, PAPER2, RULE, 1.0, 8)
    d.t(X0 + 16, y + 30, name, 14, ACC if focal else INK, KR, "start", 600)
    d.t(X0 + 16, y + 54, ac, 11, ACC if focal else SOFT, MONO, "start")
    for j, ln in enumerate(what):
        d.t(X0 + 176, y + 28 + j * 22, ln, 12, MUTED, KR, "start")
    for j, ln in enumerate(resp):
        d.t(X0 + 436, y + 28 + j * 22, ln, 11, MUTED, MONO, "start")

d.t(12, 540, "정책 층은 일회용 step-ca 로 따로 확인한다 — AC-05 가 무엇이든 서명하는 템플릿을 끼워 본다", 12, SOFT, KR, "start")
d.save("03-01.deny-layers.svg")
