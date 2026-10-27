# 타입 스펙: type-sequence
# 11-02 상호 TLS 핸드셰이크 시퀀스 — 서버의 CertificateRequest 와 양방향 인증 흐름
# 사실 출처: NPG Ch.11 Mutual TLS Authentication, RFC 8446 §4.4 (TLS 1.3 Handshake Protocol)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 1040
d = Seq(W, H, "NPG CH.11 — MUTUAL TLS HANDSHAKE SEQUENCE",
        "상호 TLS 핸드셰이크와 클라이언트 인증서 검증 시퀀스",
        "상호 TLS 핸드셰이크와 클라이언트 인증서 검증 시퀀스",
        "ClientAuth 요구 · CertificateVerify 검증 · RootCAs 와 ClientCAs 교차 신뢰")

y0 = 104
lane_w = 210

LX = {
    "TLS 클라이언트": 220,
    "TLS 서버": 670,
}
d.LX = LX

xc = LX["TLS 클라이언트"]
xs = LX["TLS 서버"]
mx = (xc + xs) / 2

roles = [
    ("TLS 클라이언트", "Dialer · RootCAs 검증"),
    ("TLS 서버", "Listener · ClientCAs 검증"),
]

for name, sub in roles:
    x = LX[name]
    d.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
    d.t(x, y0 + 19, name, 13, INK, KR, "middle", 600)
    d.t(x, y0 + 35, sub, 12, MUTED, KR, "middle")

d.lane_top = y0 + 44

y_rail_end = 964
for x in LX.values():
    d.line(x, d.lane_top + 6, x, y_rail_end, RULE, 1.0, "3 6")

# 활성화 바
d.box(xc - 4, 160, 8, 796, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(xs - 4, 160, 8, 796, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 메시지 1: ClientHello
d.path(f"M {xc + 4} 180 L {xs - 4} 180", INFO, 1.5, m="info")
d.t(mx, 171, "ClientHello", 13, INFO, MONO, "middle", 600)
d.t(mx, 197, "key_share · 암호군", 12, MUTED, KR, "middle")

# 메시지 2: ServerHello + EncryptedExtensions
d.path(f"M {xs - 4} 236 L {xc + 4} 236", INFO, 1.5, m="info")
d.t(mx, 227, "ServerHello · EncryptedExtensions", 13, INFO, MONO, "middle", 600)
d.t(mx, 253, "key_share", 12, MUTED, MONO, "middle")

# 메시지 3: CertificateRequest (서버의 클라이언트 인증서 요구 — ACC)
d.path(f"M {xs - 4} 292 L {xc + 4} 292", ACC, 1.5, m="acc")
d.t(mx, 283, "CertificateRequest", 13, ACC, MONO, "middle", 600)
d.t(mx, 309, "ClientAuth: RequireAndVerifyClientCert", 12, MUTED, MONO, "middle")

# 메시지 4: 서버 인증서 및 완료
d.path(f"M {xs - 4} 348 L {xc + 4} 348", INFO, 1.5, m="info")
d.t(mx, 339, "Certificate · CertificateVerify · Finished", 13, INFO, MONO, "middle", 600)
d.t(mx, 365, "serverCert.pem 체인 · serverKey.pem 서명", 12, MUTED, KR, "middle")

# 클라이언트 자체 검증: RootCAs 체인 및 SAN 대조 (실패 시 Dial 오류)
d.path(f"M {xc + 4} 394 L {xc + 54} 394 L {xc + 54} 414 L {xc + 4} 414", OK, 1.4, m="ok")
d.t(xc + 64, 400, "서버 인증서 검증", 13, OK, KR, "start", 600)
d.t(xc + 64, 418, "RootCAs 체인 및 SAN 대조", 12, MUTED, KR, "start")
d.t(xc + 252, 418, "(실패 → Dial 오류)", 12, BAD, KR, "start", 600)

# 메시지 5: 클라이언트 인증서 전송
d.path(f"M {xc + 4} 460 L {xs - 4} 460", ACC, 1.5, m="acc")
d.t(mx, 451, "Certificate", 13, ACC, MONO, "middle", 600)
d.t(mx, 477, "clientCert.pem 제시", 12, MUTED, KR, "middle")

# 메시지 6: CertificateVerify + Finished
d.path(f"M {xc + 4} 516 L {xs - 4} 516", ACC, 1.5, m="acc")
d.t(mx, 507, "CertificateVerify · Finished", 13, ACC, MONO, "middle", 600)
d.t(mx, 533, "clientKey.pem 서명 증명", 12, MUTED, KR, "middle")

# 클라이언트 생명선 표지: tls.Dial 반환 및 Write 성공 (시간 순서상 서버 검증보다 위)
d.line(xc - 16, 548, xc - 4, 548, OK, 1.5)
d.t(xc - 20, 552, "tls.Dial 반환", 12, OK, KR, "end", 600)

d.line(xc - 16, 576, xc - 4, 576, OK, 1.5)
d.t(xc - 20, 580, "Write 성공", 12, OK, KR, "end", 600)

# 서버 자체 검증 1: 기본 검증
d.path(f"M {xs + 4} 598 L {xs + 54} 598 L {xs + 54} 618 L {xs + 4} 618", OK, 1.4, m="ok")
d.t(xs + 64, 604, "기본 검증", 13, OK, KR, "start", 600)
d.t(xs + 64, 622, "체인 · 기간 · ClientAuth 용도", 12, MUTED, KR, "start")

# 서버 자체 검증 2: 이 편이 더함 (FOCAL — ACCENT)
d.tone(xs + 58, 642, 196, 40, ACC, r=4, op="14", sw=1.2)
d.path(f"M {xs + 4} 650 L {xs + 54} 650 L {xs + 54} 670 L {xs + 4} 670", ACC, 1.4, m="acc")
d.t(xs + 64, 656, "이 편이 더함", 13, ACC, KR, "start", 600)
d.t(xs + 64, 674, "접속 주소 ↔ SAN", 12, INK, KR, "start", 600)

# 서버 검증 뒤 alt 틀 (세 분기)
alt_x = 88
alt_w = 784
y_alt_top = 704
y_alt_bot = 952

d.box(alt_x, y_alt_top, alt_w, y_alt_bot - y_alt_top, fill="rgba(245,245,245,0.02)", stroke=RULE, sw=1.0, r=4)
# ALT 오퍼레이터 탭
d.box(alt_x, y_alt_top, 36, 16, fill=PAPER2, stroke=RULE, sw=1.0, r=2)
d.t(alt_x + 18, y_alt_top + 11, "ALT", 8, SOFT, MONO, "middle", 600)

# 분기 1: [통과]
d.t(alt_x + 12, y_alt_top + 36, "[통과]", 11, OK, MONO, "start", 600)
y_app = 764
d.path(f"M {xc + 4} {y_app} L {xs - 4} {y_app}", OK, 1.8, m="ok")
d.path(f"M {xs - 4} {y_app} L {xc + 4} {y_app}", OK, 1.8, m="ok")
d.t(mx, y_app - 9, "Application Data (암호화 통신)", 12, OK, MONO, "middle", 600)

# 구분선 1
div1_y = 792
d.line(alt_x + 8, div1_y, alt_x + alt_w - 8, div1_y, RULE, 1.0, dash="4 3")

# 분기 2: [인증서 없음]
d.t(alt_x + 12, div1_y + 20, "[인증서 없음]", 11, BAD, MONO, "start", 600)
y_r2 = 836
d.path(f"M {xs - 4} {y_r2} L {xc + 4} {y_r2}", BAD, 1.5, m="bad")
d.t(mx, y_r2 - 9, "certificate_required(116)", 12, BAD, MONO, "middle", 600)
d.t(xc + 16, y_r2 + 18, "Read: remote error: tls: certificate required", 12, BAD, MONO, "start", 500)

# 구분선 2
div2_y = 872
d.line(alt_x + 8, div2_y, alt_x + alt_w - 8, div2_y, RULE, 1.0, dash="4 3")

# 분기 3: [SAN 불일치]
d.t(alt_x + 12, div2_y + 20, "[SAN 불일치]", 11, BAD, MONO, "start", 600)
y_r3 = 916
d.path(f"M {xs - 4} {y_r3} L {xc + 4} {y_r3}", BAD, 1.5, m="bad")
d.t(mx, y_r3 - 9, "bad_certificate(42)", 12, BAD, MONO, "middle", 600)
d.t(xc + 16, y_r3 + 18, "Read: remote error: tls: bad certificate", 12, BAD, MONO, "start", 500)

# 범례
y_legend = 984
d.legend(y_legend, [
    ("기본 TLS 1.3 교환", INFO),
    ("상호 인증 확장 (mTLS)", ACC),
    ("검증 통과", OK),
    ("검증 실패 거부", BAD),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "11-02.mutual-tls-handshake.svg"))
d.save(out)
print(f"saved: {out}")
