# 타입 스펙: type-data-flow — 같은 FQDN 정책 아래 세 요청(허용된 이름 cilium.io · 허용 안 된 이름 example.com · DNS 를 거치지 않는 --resolve)이 DNS 프록시와 IP 캐시 매핑을 지나 연결 결과로 갈리는 흐름.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 597-640(fqdn-egress: toFQDNs matchName cilium.io · 80/443 · rules.dns matchPattern "*"), 줄 645-663(curl cilium.io HTTP/2 200 · example.com timed out 1001ms), 줄 664-675(--resolve example.com:443:23.220.75.245 timed out 1001ms)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
CW, GAPX, X0 = 196, 32, 24
XS = [X0 + i * (CW + GAPX) for i in range(4)]
RH, Y0, STRIDE = 100, 148, 124

d = D(W, H, "CILIUM UP AND RUNNING · 13-02 §2", "이름 질의는 모두 통과해도 연결은 응답 IP 로만 열린다",
      "DNS 규칙이 *  이므로 example.com 도 해석되지만, 그 응답 IP 에는 허용 규칙이 붙지 않아 연결이 시간 초과됩니다",
      "DNS 규칙이 *  이므로 example.com 도 해석되지만, 그 응답 IP 에는 허용 규칙이 붙지 않아 연결이 시간 초과됩니다")

for x, nm in zip(XS, ["요청", "DNS 프록시", "IP 캐시 매핑", "연결 결과"]):
    d.box(x, 96, CW, 32, PAPER2, SOFT, 1.0)
    d.t(x + CW / 2, 117, nm, 13, INK, KR, "middle", 600)

rows = [
    (["curl cilium.io", "A 질의 → TCP 443"], ['matchPattern "*"', "통과 · 응답 IP 기록"],
     ["응답 IP ↔ cilium.io", "identity 등록"], ["HTTP/2 200", "TCP 443 허용"], OK, True),
    (["curl example.com", "A 질의 → TCP 443"], ['matchPattern "*"', "통과 · 응답 IP 기록"],
     ["ipcache 갱신 없음", "고르는 셀렉터 없음"], ["curl: (28) 1001ms", "연결 시간 초과"], BAD, False),
    (["curl --resolve", "→ 23.220.75.245:443"], ["DNS 질의 없음", "프록시를 거치지 않음"],
     ["이 IP 의 매핑 없음", "FQDN identity 없음"], ["curl: (28) 1001ms", "연결 시간 초과"], BAD, False),
]

for i, (p_req, p_dns, p_map, p_res, col, focal) in enumerate(rows):
    y = Y0 + i * STRIDE
    for j, lines in enumerate([p_req, p_dns, p_map, p_res]):
        x = XS[j]
        if j == 3:
            d.tone(x, y, CW, RH, col, r=6, op="14", sw=1.3)
        elif j == 2 and focal:
            d.tone(x, y, CW, RH, ACC, r=6, op="12", sw=1.4)
        else:
            d.box(x, y, CW, RH, PAPER2, RULE, 0.9)
        y1 = y + 38
        for k, ln in enumerate(lines):
            c_text = col if (j == 3 and k == 0) else (ACC if (j == 2 and focal and k == 0) else (INK if k == 0 else MUTED))
            fam = KR if any("가" <= c <= "힣" for c in ln) else MONO
            d.t(x + CW / 2, y1 + k * 24, ln, 12, c_text, fam, "middle", 600 if k == 0 else 400)
    for j in range(3):
        d.arrow([(XS[j] + CW + 4, y + RH / 2), (XS[j + 1] - 6, y + RH / 2)], MUTED, "ar", 1.5)

d.save("13-02.fqdn-query-outcomes.svg")
