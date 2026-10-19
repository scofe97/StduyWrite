# 타입 스펙: type-data-flow
# 사실 출처: NPG Ch.11 Listing 11-12~11-15, crypto/x509, crypto/ecdsa, RFC 7468 §10
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 430
d = D(W, H, "NPG CH.11 — CERTIFICATE GENERATION DATA FLOW",
      "x509 템플릿과 ECDSA 키 생성 및 PEM 인코딩 흐름",
      "호스트 인자를 SAN 슬라이스로 파싱하고 비대칭키와 템플릿을 자체 서명하여 파일로 출력합니다",
      "net.ParseIP 분기 · P-256 비대칭키 쌍 · CreateCertificate DER · PEM 블록 저장")

y0, box_h = 108, 236
bw = 180
gap = 54

# Stage 1: 입력 및 SAN 파싱
s1_x = 24
d.box(s1_x, y0, bw, box_h, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(s1_x + 16, y0 + 22, "STAGE 1", 9, INFO, MONO, "start", 600)
d.t(s1_x + bw / 2, y0 + 44, "호스트 인자 입력", 12, INK, KR, "middle", 600)
d.t(s1_x + bw / 2, y0 + 62, "SAN 대상 주소 파싱", 11, MUTED, KR, "middle")

d.box(s1_x + 10, y0 + 74, bw - 20, 102, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s1_x + 16, y0 + 96, "-host localhost,127.0.0.1", 9, INFO, MONO, "start")
d.t(s1_x + 16, y0 + 118, "net.ParseIP(h)", 9, INK, MONO, "start")
d.t(s1_x + 16, y0 + 140, "IP -> IPAddresses", 10, OK, MONO, "start")
d.t(s1_x + 16, y0 + 160, "Host -> DNSNames", 10, OK, MONO, "start")

d.t(s1_x + bw / 2, y0 + 198, "Go 1.15+ SAN 기준", 11, MUTED, KR, "middle")
d.t(s1_x + bw / 2, y0 + 218, "CommonName 미사용", 11, MUTED, KR, "middle")

# 화살표 1: Stage 1 -> Stage 2
gap1_x = s1_x + bw
d.line(gap1_x, y0 + 124, gap1_x + gap, y0 + 124, c=MUTED, sw=1.4)
d.arrow([(gap1_x + gap - 12, y0 + 124), (gap1_x + gap, y0 + 124)], c=MUTED, m="ar", sw=1.4)
d.t(gap1_x + gap / 2, y0 + 114, "SAN 목록", 11, MUTED, KR, "middle")

# Stage 2: 템플릿 및 키 쌍 생성
s2_x = gap1_x + gap
d.box(s2_x, y0, bw, box_h, fill=PAPER2, stroke=ACC, sw=1.2, r=8)
d.t(s2_x + 16, y0 + 22, "STAGE 2", 9, ACC, MONO, "start", 600)
d.t(s2_x + bw / 2, y0 + 44, "템플릿 및 키 생성", 12, INK, KR, "middle", 600)
d.t(s2_x + bw / 2, y0 + 62, "x509.Certificate", 10, MUTED, MONO, "middle")

d.box(s2_x + 10, y0 + 74, bw - 20, 102, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s2_x + 16, y0 + 96, "SerialNumber < 2^128", 9, INK, MONO, "start")
d.t(s2_x + 16, y0 + 118, "DigitalSignature | CertSign", 9, INK, MONO, "start")
d.t(s2_x + 16, y0 + 140, "Ext: ClientAuth, ServerAuth", 9, ACC, MONO, "start")
d.t(s2_x + 16, y0 + 160, "ecdsa.GenerateKey(P256)", 9, OK, MONO, "start")

d.t(s2_x + bw / 2, y0 + 198, "비대칭 키 쌍 생성", 11, MUTED, KR, "middle")
d.t(s2_x + bw / 2, y0 + 218, "자체 서명 권한 IsCA", 11, MUTED, KR, "middle")

# 화살표 2: Stage 2 -> Stage 3
gap2_x = s2_x + bw
d.line(gap2_x, y0 + 124, gap2_x + gap, y0 + 124, c=ACC, sw=1.4)
d.arrow([(gap2_x + gap - 12, y0 + 124), (gap2_x + gap, y0 + 124)], c=ACC, m="acc", sw=1.4)
d.t(gap2_x + gap / 2, y0 + 114, "템플릿·키", 11, ACC, KR, "middle")

# Stage 3: DER 자체 서명 및 직렬화
s3_x = gap2_x + gap
d.box(s3_x, y0, bw, box_h, fill=PAPER2, stroke=WARN, sw=1.2, r=8)
d.t(s3_x + 16, y0 + 22, "STAGE 3", 9, WARN, MONO, "start", 600)
d.t(s3_x + bw / 2, y0 + 44, "DER 서명 직렬화", 12, INK, KR, "middle", 600)
d.t(s3_x + bw / 2, y0 + 62, "ASN.1 바이트 생성", 11, MUTED, KR, "middle")

d.box(s3_x + 10, y0 + 74, bw - 20, 102, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s3_x + 16, y0 + 96, "x509.CreateCertificate()", 9, WARN, MONO, "start", 600)
d.t(s3_x + 16, y0 + 118, "-> cert DER 서명 바이트", 11, INK, KR, "start")
d.t(s3_x + 16, y0 + 140, "MarshalPKCS8PrivateKey()", 9, WARN, MONO, "start", 600)
d.t(s3_x + 16, y0 + 160, "-> key DER 개인키 바이트", 11, INK, KR, "start")

d.t(s3_x + bw / 2, y0 + 198, "암호학적 서명 완료", 11, MUTED, KR, "middle")
d.t(s3_x + bw / 2, y0 + 218, "바이너리 DER 블록", 11, MUTED, KR, "middle")

# 화살표 3: Stage 3 -> Stage 4
gap3_x = s3_x + bw
d.line(gap3_x, y0 + 124, gap3_x + gap, y0 + 124, c=OK, sw=1.4)
d.arrow([(gap3_x + gap - 12, y0 + 124), (gap3_x + gap, y0 + 124)], c=OK, m="ok", sw=1.4)
d.t(gap3_x + gap / 2, y0 + 114, "DER", 11, OK, MONO, "middle")

# Stage 4: PEM 인코딩 파일 출력
s4_x = gap3_x + gap
d.box(s4_x, y0, bw, box_h, fill=PAPER2, stroke=OK, sw=1.2, r=8)
d.t(s4_x + 16, y0 + 22, "STAGE 4", 9, OK, MONO, "start", 600)
d.t(s4_x + bw / 2, y0 + 44, "PEM 파일 디스크 저장", 12, INK, KR, "middle", 600)
d.t(s4_x + bw / 2, y0 + 62, "pem.Encode 출력", 11, MUTED, KR, "middle")

d.box(s4_x + 10, y0 + 74, bw - 20, 102, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s4_x + 16, y0 + 96, "cert.pem (CERTIFICATE)", 9, OK, MONO, "start")
d.t(s4_x + 16, y0 + 118, "key.pem (PRIVATE KEY)", 9, OK, MONO, "start")
d.t(s4_x + 16, y0 + 140, "key 파일 권한 0600", 11, ACC, KR, "start")
d.t(s4_x + 16, y0 + 160, "LoadX509KeyPair 로드", 11, INK, KR, "start")

d.t(s4_x + bw / 2, y0 + 198, "서버·클라이언트 쌍", 11, MUTED, KR, "middle")
d.t(s4_x + bw / 2, y0 + 218, "상호 인증 준비 완료", 11, OK, KR, "middle")

d.legend(374, [
    ("호스트 파싱 (SAN)", INFO),
    ("템플릿 및 키 생성", ACC),
    ("DER 직렬화", WARN),
    ("PEM 인코딩 파일", OK),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "11-02.cert-generation-flow.svg"))
d.save(out)
print(f"saved: {out}")
