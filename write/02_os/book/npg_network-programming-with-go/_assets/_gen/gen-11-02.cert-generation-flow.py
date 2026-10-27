# 타입 스펙: type-nested
# 확인 주체: 클라이언트는 serverCert 의 서명·기간·ServerAuth·SAN(노트 258줄, verify.go 204~206), 서버 기본 검증은 clientCert 의 서명·기간·ClientAuth(256줄), §3 콜백은 clientCert SAN(276줄)
# 사실 출처: NPG Ch.11 §2 Listing 11-12~11-15, RFC 7468 §10, crypto/x509, crypto/ecdsa
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 880
d = D(W, H, "NPG CH.11 — CERTIFICATE & KEY NESTED STRUCTURE",
      "x509 템플릿과 ECDSA 키 생성 및 PEM 인코딩 흐름",
      "호스트 인자와 ECDSA 키 쌍이 x509 템플릿과 DER 및 PEM 중첩 층으로 매핑되는 구조",
      "net.ParseIP 분기 · P-256 키 쌍 · x509 DER 서명 · PEM 파일 인코딩")

# ── 왼쪽: 입력 둘 (호스트 인자 · 키 쌍 생성) ──────────────────────────────
x_in, w_in = 24, 252

# 입력 1: 호스트 인자 및 SAN 파싱 분기
y_in1, h_in1 = 108, 148
d.box(x_in, y_in1, w_in, h_in1, fill=PAPER2, stroke=INFO, sw=1.1, r=8)
d.t(x_in + 12, y_in1 + 20, "호스트 인자 입력", 12, INK, KR, "start", 600)
d.box(x_in + 12, y_in1 + 32, w_in - 24, 24, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(x_in + 20, y_in1 + 48, "-host localhost,127.0.0.1", 10, INFO, MONO, "start")
d.t(x_in + 12, y_in1 + 74, "net.ParseIP(h) 분기", 11, MUTED, KR, "start")

# Branch 1: "localhost"
d.box(x_in + 12, y_in1 + 84, w_in - 24, 26, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(x_in + 20, y_in1 + 101, "nil (호스트명)", 11, MUTED, KR, "start")
d.t(x_in + w_in - 20, y_in1 + 101, '"localhost"', 11, INFO, MONO, "end")

# Branch 2: "127.0.0.1"
d.box(x_in + 12, y_in1 + 114, w_in - 24, 26, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(x_in + 20, y_in1 + 131, "IP (주소)", 11, MUTED, KR, "start")
d.t(x_in + w_in - 20, y_in1 + 131, '"127.0.0.1"', 11, INFO, MONO, "end")

# 입력 2: ECDSA 비대칭 키 생성
y_in2, h_in2 = 280, 156
d.box(x_in, y_in2, w_in, h_in2, fill=PAPER2, stroke=OK, sw=1.1, r=8)
d.t(x_in + 12, y_in2 + 20, "ECDSA 키 쌍 생성", 12, INK, KR, "start", 600)
d.box(x_in + 12, y_in2 + 32, w_in - 24, 24, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(x_in + 20, y_in2 + 48, "ecdsa.GenerateKey(P256)", 10, OK, MONO, "start")
d.t(x_in + 12, y_in2 + 74, "crypto/rand 난수", 11, MUTED, KR, "start")

# Key 1: priv.PublicKey
d.box(x_in + 12, y_in2 + 84, w_in - 24, 26, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(x_in + 20, y_in2 + 101, "공개키", 11, MUTED, KR, "start")
d.t(x_in + w_in - 20, y_in2 + 101, "priv.PublicKey", 11, OK, MONO, "end")

# Key 2: priv
d.box(x_in + 12, y_in2 + 116, w_in - 24, 26, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(x_in + 20, y_in2 + 133, "개인키", 11, MUTED, KR, "start")
d.t(x_in + w_in - 20, y_in2 + 133, "priv", 11, OK, MONO, "end")

# ── 오른쪽 위: cert.pem 중첩 해부도 (PEM ⊃ DER ⊃ 템플릿 필드) ───────────
x1, y1, w1, h1 = 384, 108, 552, 456
# 겹 1: PEM
d.box(x1, y1, w1, h1, fill=PAPER2, stroke=OK, sw=1.1, r=8)
d.t(x1 + 16, y1 + 20, "PEM · cert.pem", 12, OK, MONO, "start", 600)
d.t(x1 + w1 - 16, y1 + 20, "-----BEGIN CERTIFICATE-----", 9, MUTED, MONO, "end")

# 겹 2: DER
x2, y2, w2, h2 = x1 + 24, y1 + 32, w1 - 48, h1 - 44
d.box(x2, y2, w2, h2, fill=PAPER, stroke=INFO, sw=1.0, r=8)
d.t(x2 + 16, y2 + 20, "DER · x509.CreateCertificate", 12, INFO, MONO, "start", 600)
d.t(x2 + w2 - 16, y2 + 20, "ASN.1 바이트", 11, MUTED, KR, "end")

# 겹 3: 템플릿 필드
x3, y3, w3, h3 = x2 + 24, y2 + 32, w2 - 48, h2 - 44
d.box(x3, y3, w3, h3, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(x3 + 16, y3 + 20, "x509.Certificate 템플릿", 12, INK, KR, "start", 600)

slot_x = x3 + 12
slot_w = w3 - 24

# helper for verifier chip
def chip_badge(cx, cy, txt, c, w):
    d.o.append(f'<rect x="{cx}" y="{cy}" width="{w}" height="18" rx="4" '
               f'fill="{c}18" stroke="{c}" stroke-width="0.9"/>')
    d.t(cx + w / 2, cy + 13, txt, 11, c, KR, "middle", 500)

# Row 0: SerialNumber (y=202)
d.box(slot_x, 202, slot_w, 26, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(slot_x + 12, 219, "SerialNumber", 11, INK, MONO, "start")
d.t(slot_x + slot_w - 12, 219, "128비트 난수", 11, MUTED, KR, "end")

# Row 1: 유효 기간 (y=236) — 확인: 서버 기본 검증
d.box(slot_x, 236, slot_w, 26, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(slot_x + 12, 253, "유효 기간", 11, INK, KR, "start")
chip_badge(slot_x + 72, 240, "서버 기본 검증", OK, 88)
chip_badge(slot_x + 166, 240, "클라이언트", INFO, 68)
d.t(slot_x + slot_w - 12, 253, "AddDate(10, 0, 0)", 11, MUTED, MONO, "end")

# Row 2: KeyUsage (y=270)
d.box(slot_x, 270, slot_w, 26, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(slot_x + 12, 287, "KeyUsage", 11, INK, MONO, "start")
d.t(slot_x + slot_w - 12, 287, "DigitalSignature · CertSign", 11, MUTED, MONO, "end")

# Row 3: ExtKeyUsage (y=304, height=50) — 확인: ServerAuth=클라이언트 / ClientAuth=서버 기본 검증
d.box(slot_x, 304, slot_w, 50, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(slot_x + 12, 333, "ExtKeyUsage", 11, INK, MONO, "start", 600)
# Tier 1: ServerAuth (클라이언트 확인)
chip_badge(slot_x + 104, 309, "클라이언트", INFO, 68)
d.t(slot_x + slot_w - 12, 322, "ServerAuth", 11, MUTED, MONO, "end")
# Tier 2: ClientAuth (서버 기본 검증 · FOCAL)
chip_badge(slot_x + 104, 331, "서버 기본 검증", OK, 88)
d.o.append(f'<rect x="{slot_x + slot_w - 108}" y="330" width="96" height="20" rx="4" '
           f'fill="{ACC}18" stroke="{ACC}" stroke-width="1.2"/>')
d.t(slot_x + slot_w - 60, 344, "ClientAuth", 11, ACC, MONO, "middle", 600)

# Row 4: IsCA (y=362)
d.box(slot_x, 362, slot_w, 26, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(slot_x + 12, 379, "IsCA", 11, INK, MONO, "start")
d.t(slot_x + slot_w - 12, 379, "true", 11, MUTED, MONO, "end")

# Row 5: SAN DNSNames (y=396) — 확인: §3 콜백
d.box(slot_x, 396, slot_w, 26, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(slot_x + 12, 413, "SAN DNSNames", 11, INFO, MONO, "start", 600)
chip_badge(slot_x + 116, 400, "§3 콜백", WARN, 58)
chip_badge(slot_x + 180, 400, "클라이언트", INFO, 68)
d.t(slot_x + slot_w - 12, 413, '"localhost"', 11, INFO, MONO, "end", 600)

# Row 6: SAN IPAddresses (y=430) — 확인: §3 콜백
d.box(slot_x, 430, slot_w, 26, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(slot_x + 12, 447, "SAN IPAddresses", 11, INFO, MONO, "start", 600)
chip_badge(slot_x + 130, 434, "§3 콜백", WARN, 58)
chip_badge(slot_x + 194, 434, "클라이언트", INFO, 68)
d.t(slot_x + slot_w - 12, 447, '"127.0.0.1"', 11, INFO, MONO, "end", 600)

# Row 7: 공개키 (y=464)
d.box(slot_x, 464, slot_w, 26, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(slot_x + 12, 481, "공개키", 11, OK, KR, "start", 600)
d.t(slot_x + slot_w - 12, 481, "P-256", 11, OK, MONO, "end", 600)

# Row 8: 서명 (y=498) — 확인: 서버 기본 검증
d.box(slot_x, 498, slot_w, 26, fill=PAPER, stroke=MUTED, sw=0.9, r=4)
d.t(slot_x + 12, 515, "서명", 11, MUTED, KR, "start", 600)
chip_badge(slot_x + 50, 502, "서버 기본 검증", OK, 88)
chip_badge(slot_x + 144, 502, "클라이언트", INFO, 68)
d.t(slot_x + slot_w - 12, 515, "자기 개인키 (&template)", 11, MUTED, KR, "end")

# ── 오른쪽 아래: key.pem 중첩 해부도 (PEM ⊃ PKCS#8 DER ⊃ 개인키) ─────────
kx1, ky1, kw1, kh1 = 384, 584, 552, 140
# 겹 1: PEM
d.box(kx1, ky1, kw1, kh1, fill=PAPER2, stroke=OK, sw=1.1, r=8)
d.t(kx1 + 16, ky1 + 20, "PEM · key.pem (권한 0600 · -rw-------)", 12, OK, KR, "start", 600)
d.t(kx1 + kw1 - 16, ky1 + 20, "-----BEGIN PRIVATE KEY-----", 9, MUTED, MONO, "end")

# 겹 2: PKCS#8 DER
kx2, ky2, kw2, kh2 = kx1 + 24, ky1 + 32, kw1 - 48, kh1 - 44
d.box(kx2, ky2, kw2, kh2, fill=PAPER, stroke=INFO, sw=1.0, r=8)
d.t(kx2 + 16, ky2 + 20, "PKCS#8 DER · x509.MarshalPKCS8PrivateKey", 12, INFO, MONO, "start", 600)
d.t(kx2 + kw2 - 16, ky2 + 20, "PKCS#8 ASN.1 바이트", 11, MUTED, KR, "end")

# 겹 3: 개인키
kx3, ky3, kw3, kh3 = kx2 + 24, ky2 + 32, kw2 - 48, kh2 - 44
d.box(kx3, ky3, kw3, kh3, fill=PAPER2, stroke=OK, sw=1.0, r=8)
d.box(kx3 + 12, ky3 + 8, kw3 - 24, 28, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(kx3 + 24, ky3 + 26, "개인키", 12, OK, KR, "start", 600)
d.t(kx3 + kw3 - 24, ky3 + 26, "P-256 개인키", 11, OK, KR, "end", 600)

# ── 화살표 (값의 이동) ──────────────────────────────────────────────────
# 1. "localhost" -> SAN DNSNames (row 5: y=409)
d.arrow([(x_in + w_in, y_in1 + 97), (356, y_in1 + 97), (356, 409), (slot_x, 409)], c=INFO, m="info", sw=1.4)

# 2. "127.0.0.1" -> SAN IPAddresses (row 6: y=443)
d.arrow([(x_in + w_in, y_in1 + 127), (340, y_in1 + 127), (340, 443), (slot_x, 443)], c=INFO, m="info", sw=1.4)

# 3. priv.PublicKey -> 공개키 (row 7: y=477)
d.arrow([(x_in + w_in, y_in2 + 97), (324, y_in2 + 97), (324, 477), (slot_x, 477)], c=OK, m="ok", sw=1.4)

# 4. priv -> 서명 (row 8: y=511, 점선, "서명")
d.arrow([(x_in + w_in, y_in2 + 129), (308, y_in2 + 129), (308, 511), (slot_x, 511)], c=MUTED, m="ar", sw=1.4, dash="4 3")
d.t(346, 501, "서명", 11, MUTED, KR, "middle")

# 5. priv -> key.pem 안쪽 개인키 (y=672)
d.arrow([(x_in + w_in // 2, y_in2 + h_in2), (x_in + w_in // 2, ky3 + 22), (kx3 + 12, ky3 + 22)], c=OK, m="ok", sw=1.4)

# ── 하단: 도구 실행 한 줄 ───────────────────────────────────────────────
y_cmd = 744
d.box(24, y_cmd, 912, 48, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(40, y_cmd + 29, "도구 실행", 12, INK, KR, "start", 600)
d.t(112, y_cmd + 29, "go run generate.go -host localhost,127.0.0.1", 11, INFO, MONO, "start")
d.t(920, y_cmd + 29, "서버: serverCert.pem · 클라이언트: clientCert.pem", 11, MUTED, KR, "end")

# ── 범례 ────────────────────────────────────────────────────────────────
d.legend(816, [
    ("ClientAuth (클라이언트 인증)", ACC),
    ("서버 기본 검증", OK),
    ("§3 콜백", WARN),
    ("클라이언트", INFO),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "11-02.cert-generation-flow.svg"))
d.save(out)
print(f"saved: {out}")
