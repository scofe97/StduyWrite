# 타입 스펙: type-sequence — TCP 연결 뒤 TLS 1.3 전체 핸드셰이크 메시지와 첫 요청이 나가기까지의 왕복 수(레인 2, 메시지 10).
# 사실 출처: RFC 9846 §2 메시지 흐름(RFC 8446 을 폐기한 현행 TLS 1.3, 2026-07; ClientHello+key_share, ServerHello+key_share, {EncryptedExtensions}, {Certificate}, {CertificateVerify}, {Finished}, [Application Data]; {} 는 핸드셰이크 키, [] 는 응용 키).
#   메시지 길이는 직접 측정 `openssl s_client -connect example.com:443 -servername example.com -tls1_3 -groups X25519 -msg` (OpenSSL 3.6.4, 2026-10-12T16:33Z).
#   [length] 는 4바이트 핸드셰이크 헤더 포함(ClientHello 헤더 길이 필드 0x05b4 = 출력 [length 05b8] − 4 로 확인). Cipher TLS_AES_256_GCM_SHA384, 서명 ecdsa_secp256r1_sha256.
# Layout conventions: 레인 2·폭 200, 메시지 stride 56(라벨 y-9, 부라벨 y+17), 첫 메시지 y=196, RTT 칩은 클라이언트 레인 안쪽. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sw=1.5):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def chip(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 880, 828
d = SeqKR(W, H, "BYTEBYTEGO · 03-01 §3",
          "첫 요청은 TCP 한 왕복과 TLS 1.3 한 왕복 뒤에 나간다",
          "메시지 길이는 openssl 실측(3.6.4 · 2026-10-12T16:33Z · example.com), 요청 줄은 예시",
          "{ } 는 핸드셰이크 키, [ ] 는 응용 키로 보호된 메시지입니다")
C, S_ = "클라이언트", "서버"
d.lanes([(C, "openssl s_client"), (S_, "example.com:443")], 100, 200)
d.rails(H - 80)

Y0, S = 196, 56
rows = [
    (C, S_, "SYN", MUTED, "ar", None, ""),
    (S_, C, "SYN + ACK", MUTED, "ar", "5 4", ""),
    (C, S_, "ClientHello", MUTED, "ar", None, "key_share X25519 · server_name example.com · 230 B"),
    (S_, C, "ServerHello", MUTED, "ar", "5 4", "key_share X25519 · TLS_AES_256_GCM_SHA384 · 122 B"),
    (S_, C, "{EncryptedExtensions}", INFO, "info", "5 4", "10 B"),
    (S_, C, "{Certificate}", INFO, "info", "5 4", "3686 B"),
    (S_, C, "{CertificateVerify}", INFO, "info", "5 4", "ecdsa_secp256r1_sha256 · 79 B"),
    (S_, C, "{Finished}", INFO, "info", "5 4", "52 B"),
    (C, S_, "{Finished} + [Application Data]", ACC, "acc", None, "예시 요청 · GET /product/electric/phone HTTP/1.1"),
    (S_, C, "[Application Data]", OK, "ok", "5 4", "예시 응답"),
]
for k, (a, b, lab, c, mk, dash, sub) in enumerate(rows):
    d.msg(a, b, lab, Y0 + k * S, c, mk, dash, sub or None)

# 클라이언트 레인 옆 RTT 칩: SYN+ACK 도착 뒤 1, 서버 Finished 도착 뒤 2.
d.chip(C, "1 RTT", Y0 + 1 * S + 28, WARN, 0)
d.chip(C, "2 RTT", Y0 + 7 * S + 28, WARN, 0)

d.legend(H - 56, [("평문", MUTED), ("핸드셰이크 키", INFO), ("응용 키", OK), ("첫 요청", ACC), ("누적 왕복", WARN)])
d.save("03-01.tls-sequence.svg")
