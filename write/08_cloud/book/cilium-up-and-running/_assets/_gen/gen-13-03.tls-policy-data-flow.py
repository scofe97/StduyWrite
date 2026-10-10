# 타입 스펙: type-data-flow — 요청 경로 값이 TLS 종료, L7 규칙 판정을 거쳐 200 OK 또는 403 Forbidden 응답이 되는 데이터 흐름.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 1158-1210(정책: host cilium.io · path /blog/.*), 1212-1224(curl -sI 결과 200 OK · 200 OK · 403 Forbidden), 1226-1231(curl 인증서 오류 없음)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, SOFT, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 920, 500
CW, GAPX, X0 = 196, 32, 24
XS = [X0 + i * (CW + GAPX) for i in range(4)]
RH, Y0, STRIDE = 88, 148, 112

d = D(W, H, "CILIUM UP AND RUNNING · 13-03 §3", "경로 값이 규칙을 거쳐 응답 코드가 되는 흐름",
      "같은 host 와 포트라도 path 가 /blog/.* 와 맞으면 200 OK, 맞지 않으면 403 Forbidden 이 돌아온다",
      "같은 host 와 포트라도 path 가 /blog/.* 와 맞으면 200 OK, 맞지 않으면 403 Forbidden 이 돌아온다")

heads = [("https://cilium.io + 경로", RULE, 1.0), ("terminatingTLS", RULE, 1.0),
         ("L7 규칙 host cilium.io", ACC, 1.4), ("curl 응답", RULE, 1.0)]
for x, (nm, sc, sw) in zip(XS, heads):
    d.box(x, 96, CW, 32, PAPER2, sc, sw)
    d.t(x + CW / 2, 117, nm, 13, INK, MONO if nm.isascii() else KR, "middle", 600)

rows = [
    (["/blog/"], ["일치"], ["HTTP/1.1 200 OK"], OK),
    (["/blog/2025/05/20/", "cilium-l7-policies/"], ["일치"], ["HTTP/1.1 200 OK"], OK),
    (["/ (경로 없음)"], ["불일치"], ["HTTP/1.1 403 Forbidden"], BAD),
]

for i, (p_path, p_match, p_res, col) in enumerate(rows):
    y = Y0 + i * STRIDE
    cells = [
        (p_path, None, [MONO] * len(p_path)),
        (["cilium-io-cert", "curl 인증서 오류 없음"], None, [MONO, KR]),
        (["path /blog/.*", p_match[0]], None, [MONO, KR]),
        (p_res, col, [MONO]),
    ]
    for j, (lines, tone, fams) in enumerate(cells):
        x = XS[j]
        if tone:
            d.tone(x, y, CW, RH, tone, r=6, op="14", sw=1.3)
        else:
            d.box(x, y, CW, RH, PAPER2, RULE, 0.9)
        n = len(lines)
        y1 = y + RH / 2 + 4 - (n - 1) * 12
        for k, ln in enumerate(lines):
            c_text = tone if tone else (col if (j == 2 and k == 1) else (INK if k == 0 else MUTED))
            d.t(x + CW / 2, y1 + k * 24, ln, 12, c_text, fams[k], "middle", 600 if k == 0 or j == 2 else 400)
    for j in range(3):
        d.arrow([(XS[j] + CW + 4, y + RH / 2), (XS[j + 1] - 6, y + RH / 2)], MUTED, "ar", 1.5)

d.save("13-03.tls-policy-data-flow.svg")
