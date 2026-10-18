# 타입 스펙: type-sequence
# 사실 출처: RFC 8446 §2 (Protocol Overview), §4.1.2 (Client Hello),
#   §4.1.3 (Server Hello), §4.2.8 (Key Share), §4.4 (Server Parameters),
#   §7.1 (Key Schedule).
import pathlib
import sys
import os

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqKR(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 20}" width="{_w(label, 11)}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 10)/2}" y="{y + 4}" width="{_w(sub, 10)}" height="15" fill="{PAPER}"/>')
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub))

    def bi_msg(s, a, b, label, y, c=OK, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        s.o.append(f'<path d="M {x1 + 12} {y} L {x2 - 12} {y}" fill="none" stroke="{c}" stroke-width="1.5" marker-start="url(#ok_left)" marker-end="url(#ok)"/>')
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 20}" width="{_w(label, 11)}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 10)/2}" y="{y + 4}" width="{_w(sub, 10)}" height="15" fill="{PAPER}"/>')
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub))

W, H = 960, 750
d = SeqKR(W, H, "TLS 1.3 · 1-RTT HANDSHAKE FLOW",
          "TLS 1.3 핸드셰이크와 암호화 경계",
          "ClientHello와 ServerHello 교환 즉시 핸드셰이크 암호화 키를 도출하여 서버 인증서와 서명 메시지를 암호화하고, Finished 검증 후 애플리케이션 데이터 통신을 시작합니다.",
          "ClientHello와 ServerHello 교환 직후부터 모든 제어 메시지가 암호화됩니다")

NAMES = (
    ("클라이언트 (브라우저)", "client_random · key_share"),
    ("서버 (웹 서버 / 프록시)", "server_random · 인증서 서명")
)
d.LX = {"client": 240, "server": 720}
KEYS = ["client", "server"]

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 120, 100, 240, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 136, sub, 10, MUTED, _kr(sub))

d.lane_top = 144
d.rails(H - 68)

# 1. ClientHello (plaintext)
d.msg("client", "server", "ClientHello [평문]", 180, INFO, "info",
      sub="random · cipher_suites · key_share · SNI · ALPN")

# 2. ServerHello (plaintext)
d.msg("server", "client", "ServerHello [평문]", 238, INFO, "info",
      sub="random · cipher_suite · key_share")

# Handshake Key Derivation Boundary
d.box(260, 274, 440, 26, fill=PAPER2, stroke=ACC, sw=1.1, r=4)
d.t(480, 291, "ECDHE 공유 비밀 → handshake_traffic_secret 활성화", 10, ACC, MONO, "middle", 600)

# 3. EncryptedExtensions (encrypted)
d.msg("server", "client", "{EncryptedExtensions} [암호화]", 336, OK, "ok",
      sub="ALPN 협상 결과 · 서버 확장 파라미터")

# 4. Certificate (encrypted)
d.msg("server", "client", "{Certificate} [암호화]", 390, OK, "ok",
      sub="서버 X.509 인증서 체인 (Leaf + Intermediate)")

# 5. CertificateVerify (encrypted)
d.msg("server", "client", "{CertificateVerify} [암호화]", 444, WARN, "warn",
      sub="트랜스크립트 해시 전자 서명 (도메인 소유 증명)")

# 6. Finished (encrypted)
d.msg("server", "client", "{Finished} [암호화]", 498, OK, "ok",
      sub="전체 트랜스크립트 무결성 HMAC 검증")

# Application Key Derivation Boundary
d.box(260, 534, 440, 26, fill=PAPER2, stroke=OK, sw=1.1, r=4)
d.t(480, 551, "master_secret → application_traffic_secret 활성화", 10, OK, MONO, "middle", 600)

# 7. Client Finished (encrypted)
d.msg("client", "server", "{Finished} [암호화]", 594, OK, "ok",
      sub="클라이언트 트랜스크립트 HMAC 검증 완료")

# 8. Application Data (encrypted)
d.bi_msg("client", "server", "[Application Data] (양방향 대칭 암호화)", 648, OK,
         sub="HTTP/1.1 · HTTP/2 평문 요청·응답 암호화 전송")

# 범례
d.legend(698, [
    ("평문 핸드셰이크", INFO),
    ("암호화 핸드셰이크", OK),
    ("트랜스크립트 서명", WARN),
    ("키 도출 경계", ACC),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01-tls13-handshake.svg"))
d.save(out)
print(f"saved: {out}")
