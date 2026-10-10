# 타입 스펙: type-data-flow — 세 가지 HTTP 요청이 L7 정규식 매치 규칙을 거쳐 200 허용과 403 차단 응답으로 갈라지는 데이터 흐름. 포커스는 허용되는 /api 규칙 행.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 99-104(경로별 응답), 115-123(L7 HTTP 규칙), 131-163(403 Forbidden, server: envoy, Access denied), 170-176(정규식 매치 동작)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
CW, GAPX, X0 = 260, 40, 20
XS = [X0 + i * (CW + GAPX) for i in range(3)]
RH, Y0, STRIDE = 100, 148, 120

d = D(W, H, "CILIUM UP AND RUNNING · 13-01 §2", "HTTP 규칙은 메서드와 경로 정규식으로 판정한다",
      "webserver 로 향하는 세 요청이 L7 규칙을 거쳐 200 허용과 403 차단으로 갈린다",
      "webserver 로 향하는 세 요청이 L7 규칙을 거쳐 200 허용과 403 차단으로 갈린다")

for x, nm in zip(XS, ["클라이언트 요청", "L7 HTTP 규칙 (정규식)", "Envoy 판정 및 응답"]):
    d.box(x, 96, CW, 32, PAPER2, SOFT, 1.0)
    d.t(x + CW / 2, 117, nm, 13, INK, KR, "middle", 600)

rows = [
    (["curl webserver", "GET / HTTP/1.1"],
     ["path: /api (완전 일치)", "하위·루트 경로 불일치"],
     ["403 Forbidden", '본문 "Access denied" · envoy'],
     False, BAD),
    (["curl webserver/api", "GET /api HTTP/1.1"],
     ["method: GET · path: /api", "메서드·경로 정규식 일치"],
     ["200 OK", '본문 "API" · 백엔드 전달'],
     True, OK),
    (["curl webserver/admin", "GET /admin HTTP/1.1"],
     ["path: /api (완전 일치)", "관리자 경로 불일치"],
     ["403 Forbidden", '본문 "Access denied" · envoy'],
     False, BAD),
]

for i, (req, rule, res, focal, tone_col) in enumerate(rows):
    y = Y0 + i * STRIDE
    for j, lines in enumerate([req, rule, res]):
        x = XS[j]
        if focal and j == 1:
            d.tone(x, y, CW, RH, ACC, r=6, op="14", sw=1.4)
        elif j == 2:
            d.tone(x, y, CW, RH, tone_col, r=6, op="10", sw=1.1)
        else:
            d.box(x, y, CW, RH, PAPER2, RULE, 0.9)

        y1 = y + 42 if len(lines) > 1 else y + RH / 2 + 4
        for k, ln in enumerate(lines):
            col = INK if k == 0 else MUTED
            if j == 2 and k == 0:
                col = tone_col
            elif focal and j == 1 and k == 0:
                col = ACC
            fam = KR if any("가" <= c <= "힣" for c in ln) else MONO
            d.t(x + CW / 2, y1 + k * 26, ln, 12, col, fam, "middle", 600 if k == 0 else 400)

    for j in range(2):
        d.arrow([(XS[j] + CW + 4, y + RH / 2), (XS[j + 1] - 6, y + RH / 2)], MUTED, "ar", 1.5)

d.save("13-01.http-filtering.svg")
