# 타입 스펙: type-sequence
# 11-02 상호 TLS 핸드셰이크 시퀀스 — 서버의 CertificateRequest 와 양방향 인증 흐름
# 사실 출처: NPG Ch.11 Mutual TLS Authentication, RFC 8446 §4.4 (TLS 1.3 Handshake Protocol)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 596
d = Seq(W, H, "NPG CH.11 — MUTUAL TLS HANDSHAKE SEQUENCE",
        "상호 TLS 핸드셰이크와 클라이언트 인증서 검증 시퀀스",
        "서버가 CertificateRequest 를 보내고 클라이언트가 서명을 증명해 양방향 신뢰를 확립합니다",
        "ClientAuth 요구 · CertificateVerify 검증 · RootCAs 와 ClientCAs 교차 신뢰")

y0 = 104
lane_w = 210

LX = {
    "TLS 클라이언트": 220,
    "TLS 서버": 670,
}
d.LX = LX

roles = [
    ("TLS 클라이언트", "Dialer · RootCAs 피닝"),
    ("TLS 서버", "Listener · ClientCAs 검증"),
]

for name, sub in roles:
    x = LX[name]
    d.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
    d.t(x, y0 + 19, name, 12, INK, KR, "middle", 600)
    d.t(x, y0 + 35, sub, 11, MUTED, KR, "middle")

d.lane_top = y0 + 44

y_bot = 526
for x in LX.values():
    d.line(x, d.lane_top + 6, x, y_bot, RULE, 1.0, "3 6")

# 활성화 바
d.box(LX["TLS 클라이언트"] - 4, 160, 8, 360, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["TLS 서버"] - 4, 160, 8, 360, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 메시지 1: ClientHello
d.msg("TLS 클라이언트", "TLS 서버", "ClientHello", 170, c=INFO, mk="info", sub="key_share · 암호군 제안")

# 메시지 2: ServerHello + EncryptedExtensions
d.msg("TLS 서버", "TLS 클라이언트", "ServerHello · EncryptedExtensions", 215, c=INFO, mk="info", sub="서버 키 공유 파라미터 확정")

# 메시지 3: CertificateRequest (서버의 클라이언트 인증서 요구 — ACC)
d.msg("TLS 서버", "TLS 클라이언트", "CertificateRequest", 260, c=ACC, mk="acc", sub="ClientAuth: RequireAndVerify")

# 메시지 4: 서버 인증서 및 완료
d.msg("TLS 서버", "TLS 클라이언트", "Certificate · CertificateVerify · Finished", 305, c=INFO, mk="info", sub="서버 인증서 체인 및 핸드셰이크 서명")

# 클라이언트 자체 검증: RootCAs
d.selfmsg("TLS 클라이언트", "서버 인증서 검증", 345, c=OK, sub="RootCAs 체인 및 SAN 대조")

# 메시지 5: 클라이언트 인증서 전송
d.msg("TLS 클라이언트", "TLS 서버", "Certificate", 390, c=ACC, mk="acc", sub="clientCert.pem 제시")

# 메시지 6: CertificateVerify + Finished
d.msg("TLS 클라이언트", "TLS 서버", "CertificateVerify · Finished", 440, c=ACC, mk="acc", sub="클라이언트 개인키 서명 증명")

# 서버 자체 검증: ClientCAs + VerifyPeerCertificate
d.selfmsg("TLS 서버", "클라이언트 검증", 482, c=OK, sub="ClientCAs 체인 및 IP·SAN 대조")

# 양방향 통신
d.path(f"M {LX['TLS 클라이언트']+10} 524 L {LX['TLS 서버']-10} 524", OK, 2.0, m="ok")
d.path(f"M {LX['TLS 서버']-10} 524 L {LX['TLS 클라이언트']+10} 524", OK, 2.0, m="ok")
d.t((LX["TLS 클라이언트"] + LX["TLS 서버"]) / 2, 516, "Application Data (상호 인증 암호화 통신)", 11, OK, MONO, "middle", 600)

d.legend(550, [
    ("기본 TLS 1.3 교환", INFO),
    ("상호 인증 확장 (mTLS)", ACC),
    ("로컬 체인 검증 통과", OK),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "11-02.mutual-tls-handshake.svg"))
d.save(out)
print(f"saved: {out}")
