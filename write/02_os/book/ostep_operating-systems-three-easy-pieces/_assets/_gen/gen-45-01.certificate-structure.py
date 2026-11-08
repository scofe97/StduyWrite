# 45-01 「2. CA 서명으로 공개 키를 이름에 묶는 인증서」 — 인증서(DER 788바이트)는 tbsCertificate·서명 알고리즘·서명 값 셋을 감싼다. 서명은 tbsCertificate 508바이트에 대해서만 계산하고, 이름과 공개 키가 그 안에 있어 한 바이트만 바꿔도 확인이 실패한다.
# 본문 근거: 이 노트 「인증서에 든 것과 서명 범위」 절.
# 값 근거: 2026-11-08 이 기기의 openssl 3.6.4 로 만든 server.der 를 openssl asn1parse -inform DER 로 읽었다.
#   0: SEQUENCE hl=4 l=784 / 4: SEQUENCE hl=4 l=504 (tbsCertificate, tbs.der 508바이트) / 512: SEQUENCE hl=2 l=13 (서명 알고리즘) / 527: BIT STRING hl=4 l=257 (서명 값, sig.bin 256바이트).
#   한 바이트 변경 시 openssl verify 가 error 7 certificate signature failure. 오류 번호는 OpenSSL 소스 태그 openssl-3.6.0 include/openssl/x509_vfy.h.in 의 X509_V_ERR_CERT_SIGNATURE_FAILURE 7.
# 공식 근거: RFC 5280 §4.1.1.3 — 서명은 DER 로 인코딩한 tbsCertificate 에 대해 계산한다.
# 타입 스펙: type-nested — 인증서 바깥 고리 안에 tbsCertificate·서명 알고리즘·서명 값, 그 안에 필드.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, ACC, BAD, INFO, KR, MONO, PAPER, PAPER2, RULE

W, H = 880, 452


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "OSTEP · 45-01 §2",
      "서명은 이름과 공개 키가 든 tbsCertificate 를 덮는다",
      "인증서 server.der 는 788바이트이고 tbsCertificate, 서명 알고리즘, 서명 값 셋을 감싼다. "
      "tbsCertificate 는 바이트 4에서 511까지 508바이트이며 발급자 이름, 서버 이름, 공개 키, 유효 기간, 대체 이름이 들어 있다. "
      "서명 값은 바이트 527에서 787까지 261바이트로 머리 4바이트와 미사용 비트 1바이트와 서명 256바이트이며 tbsCertificate 바깥에 붙고, 그 입력은 tbsCertificate 이다. "
      "서버 이름 한 글자만 바꿔도 서명 확인이 error 7 로 실패한다.")

# 바깥 고리
d.box(12, 92, 852, 292, "#0D1117", RULE, 1.0, 8)
d.t(28, 114, "server.der 788바이트 = 머리 4 + 본문 784", 12, SOFT, MONO, "start", 600)

# tbsCertificate — focal
d.tone(36, 132, 508, 216, ACC, 6, "14", 1.6)
d.t(52, 156, "tbsCertificate", 13, INK, MONO, "start", 600)
d.t(52, 174, "바이트 4–511 · 508바이트", 12, MUTED, KR, "start")

fields = [
    ("issuer", "CN=Demo Root", INFO),
    ("subject", "CN=demo.local", BAD),
    ("공개 키", "RSA 2048", INFO),
    ("유효 기간", "30일", INFO),
    ("SAN", "DNS:demo.local", INFO),
    ("그 밖에", "serial · version", INFO),
]
for k, (key, val, c) in enumerate(fields):
    col, row = k % 2, k // 2
    x, y = 52 + col * 244, 188 + row * 44
    d.box(x, y, 228, 36, PAPER, c if c == BAD else RULE, 1.4 if c == BAD else 0.9, 4)
    d.t(x + 10, y + 23, key, 12, MUTED, kr(key), "start")
    d.t(x + 84, y + 23, val, 12, INK, kr(val), "start")

d.chip(290, 332, "한 바이트만 바꿔도 error 7 (서명 실패)", BAD, 12)

# 서명 알고리즘
d.tone(560, 132, 108, 96, SOFT, 6, "14", 1.1)
d.t(614, 158, "서명 알고리즘", 12, INK, KR, "middle", 600)
d.t(614, 180, "512–526", 12, MUTED, MONO, "middle")
d.t(614, 200, "15바이트", 12, MUTED, KR, "middle")

# 서명 값
d.tone(684, 132, 156, 216, INFO, 6, "14", 1.4)
d.t(762, 158, "서명 값", 13, INK, KR, "middle", 600)
d.t(762, 180, "527–787", 12, MUTED, MONO, "middle")
d.t(762, 200, "261바이트", 12, MUTED, KR, "middle")
d.t(762, 232, "머리 4 + 미사용 비트 1", 12, MUTED, KR, "middle")
d.t(762, 252, "+ 서명 256바이트", 12, MUTED, KR, "middle")

# 서명 입력
d.arrow([(290, 352), (290, 368), (762, 368), (762, 352)], ACC, "acc", 1.6)
d.chip(526, 368, "CA 개인 키로 서명", ACC, 12)

d.legend(412, [("서명이 덮는 범위", ACC), ("서명 값", INFO), ("서명 알고리즘", SOFT), ("바꾸면 깨지는 필드", BAD)])
d.save("45-01.certificate-structure.svg")
