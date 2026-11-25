# 04-01 §4 세 TLS 모드에서 TLS 가 어디서 끝나는가.
# 본문 요구: 클라이언트 → 게이트웨이 → 백엔드 경로에서 SIMPLE·MUTUAL 은 게이트웨이가 TLS 를 종료하고,
#           PASSTHROUGH 는 SNI 만 읽어 백엔드까지 TLS 를 유지한다. 모드 옆에 Gateway protocol 과 VirtualService 매칭 값.
# 값 근거: 04-01 §4·§5 및 ch04.txt 4.3.1(SIMPLE, tls.key·tls.crt), 4.3.3(MUTUAL, ca.crt, --cert·--key),
#           4.4.2(PASSTHROUGH, sniHosts, simple-tls-service-1/2), 4.3.1 Auto mTLS 구간(webapp), protocol HTTPS·TLS, http·Host.
# 타입 스펙: type-architecture — 세 행(모드)마다 같은 세 칸(클라이언트·게이트웨이·백엔드)을 직교 화살표로 잇고
#           TLS 가 끝나는 칸 하나를 코랄 focal 로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 504
d = D(W, H, "ARCHITECTURE · 04-01 §4",
      "세 TLS 모드 — TLS 는 어디서 끝나는가",
      "SIMPLE 과 MUTUAL 은 게이트웨이가 인증서를 갖고 TLS 를 종료하며 MUTUAL 은 ca.crt 로 클라이언트까지 검증한다. "
      "PASSTHROUGH 는 게이트웨이가 SNI 만 읽고 백엔드까지 TLS 를 유지해 백엔드가 종료한다.",
      lead="코랄 칸이 TLS가 끝나는 곳이고 초록 화살표가 암호화 구간입니다. 모드 이름 옆에 Gateway의 protocol과 VirtualService 매칭 값을 적었습니다.")

CX, CW = 20, 150          # 클라이언트 칸
GX, GW = 340, 240         # 게이트웨이 칸
BX, BW = 740, 200         # 백엔드 칸
BOX_H = 72
rows = [
    dict(mode="SIMPLE", meta="protocol HTTPS · http·Host",
         c_sub="서버 인증서 확인", a1="TLS", a1s="서버 인증서 제시",
         g_title="게이트웨이 · TLS 종료", g_sub="tls.key · tls.crt", g_focal=True,
         a2="Auto mTLS", a2s="양쪽에 사이드카가 있을 때",
         b_title="webapp", b_sub="사이드카 서비스", b_focal=False),
    dict(mode="MUTUAL", meta="protocol HTTPS · http·Host",
         c_sub="자기 인증서도 제시", a1="TLS", a1s="클라이언트 인증서 제시",
         g_title="게이트웨이 · TLS 종료", g_sub="ca.crt로 클라이언트 검증", g_focal=True,
         a2="Auto mTLS", a2s="양쪽에 사이드카가 있을 때",
         b_title="webapp", b_sub="사이드카 서비스", b_focal=False),
    dict(mode="PASSTHROUGH", meta="protocol TLS · tls·sniHosts",
         c_sub="백엔드 인증서 확인", a1="TLS", a1s="ClientHello에 SNI",
         g_title="게이트웨이 · SNI만 읽음", g_sub="인증서 없음 · 종료 안 함", g_focal=False,
         a2="TLS", a2s="종료 없이 통과",
         b_title="백엔드 · TLS 종료", b_sub="simple-tls-service-1 / 2", b_focal=True),
]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def cell(x, y, w, title, sub, c, focal):
    if focal:
        d.tone(x, y, w, BOX_H, ACC, 6, "1e", 1.4)
        tc = ACC
    else:
        d.tone(x, y, w, BOX_H, c, 6, "14", 1.1)
        tc = INK if c == MUTED else c
    d.t(x + w / 2, y + 30, title, 14, tc, kr(title), "middle", 600)
    d.t(x + w / 2, y + 52, sub, 13, MUTED, kr(sub), "middle")


TOP0, STRIDE = 96, 118
for i, r in enumerate(rows):
    top = TOP0 + i * STRIDE
    y = top + 24
    d.t(CX, top + 14, r["mode"], 13, INK, MONO, "start", 600)
    d.t(CX + 128 if r["mode"] == "SIMPLE" else CX + 142 if r["mode"] == "MUTUAL" else CX + 178, top + 14,
        r["meta"], 11, MUTED, MONO, "start")
    cell(CX, y, CW, "클라이언트", r["c_sub"], INFO, False)
    cell(GX, y, GW, r["g_title"], r["g_sub"], MUTED, r["g_focal"])
    cell(BX, y, BW, r["b_title"], r["b_sub"], MUTED, r["b_focal"])
    ay = y + BOX_H / 2
    d.arrow([(CX + CW, ay), (GX, ay)], OK, "ok", 1.5)
    d.t((CX + CW + GX) / 2, ay - 9, r["a1"], 12, OK, MONO, "middle", 600)
    d.t((CX + CW + GX) / 2, ay + 19, r["a1s"], 12, MUTED, kr(r["a1s"]), "middle")
    d.arrow([(GX + GW, ay), (BX, ay)], OK, "ok", 1.5)
    d.t((GX + GW + BX) / 2, ay - 9, r["a2"], 12, OK, MONO, "middle", 600)
    d.t((GX + GW + BX) / 2, ay + 19, r["a2s"], 12, MUTED, kr(r["a2s"]), "middle")

d.legend(H - 44, [
    ("클라이언트", INFO),
    ("TLS가 끝나는 칸", ACC),
    ("그 밖의 칸", MUTED),
    ("암호화 구간(화살표)", OK),
])
d.save("04-01.tls-modes.svg")
print("ok 04-01 tls-modes")
