# 45-01 「2. CA 서명으로 공개 키를 이름에 묶는 인증서」 — 받는 쪽은 인증서의 발급자 루트가 설치돼 있는지, 그 루트 공개 키로 서명이 확인되는지를 차례로 묻고, 둘 다 통과해야 인증서 속 공개 키를 사이트 이름에 묶어 믿는다.
# 본문 근거: 이 노트 「서명 확인 순서와 루트 키라는 출발점」 절.
# 값 근거: 2026-11-08 openssl 3.6.4 로 루트가 서명한 서버 인증서를 만들어 openssl verify 를 돌렸다.
#   루트를 주면 server.crt: OK / 루트 없이 하면 error 20 unable to get local issuer certificate / DER 한 바이트를 바꾸면 error 7 certificate signature failure.
#   macOS 시스템 루트 목록 158개(security find-certificate -a SystemRootCertificates.keychain | grep -c '"alis"').
#   오류 번호는 OpenSSL 소스 태그 openssl-3.6.0 include/openssl/x509_vfy.h.in 의 X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT_LOCALLY 20, X509_V_ERR_CERT_SIGNATURE_FAILURE 7.
# 공식 근거: RFC 5280 §6(신뢰 앵커 선택은 정책의 문제). OSTEP 57장 §57.3.
# 타입 스펙: type-flowchart — 시작 타원, 판정 마름모 둘, 거부 사각형 둘, 끝 타원, 선행 조건 사각형 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, KR, MONO

W, H = 880, 576
d = D(W, H, "OSTEP · 45-01 §2",
      "서명이 미리 가진 CA 키로 확인되면 공개 키를 믿고 아니면 거부한다",
      "받는 쪽은 사이트에서 server.crt 를 받아 두 가지를 차례로 묻는다. 먼저 발급자 루트가 미리 설치돼 있는지 묻고, 없으면 error 20 으로 거부한다. "
      "있으면 그 루트 공개 키로 tbsCertificate 의 서명이 확인되는지 묻고, 맞지 않으면 error 7 로 거부한다. "
      "둘 다 통과하면 OK 이고 인증서 속 공개 키를 사이트 이름에 묶어 믿는다. 루트 공개 키는 소프트웨어와 함께 설치돼 있어야 하므로 이 확인은 미리 가진 키에서 출발한다.")

CX = 420
DW, DH = 264, 84
CY1, CY2 = 236, 372


def diamond(cy, c, l1, l2):
    pts = f"{CX},{cy - DH // 2} {CX + DW // 2},{cy} {CX},{cy + DH // 2} {CX - DW // 2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(CX, cy - 2, l1, 12.5, INK, KR, "middle", 600)
    d.t(CX, cy + 16, l2, 12.5, INK, KR, "middle", 600)


# 시작
d.tone(CX - 120, 96, 240, 40, SOFT, 20, "14", 1.1)
d.t(CX, 121, "server.crt 수신", 12.5, INK, KR, "middle", 600)
d.arrow([(CX, 138), (CX, CY1 - DH // 2 - 4)], MUTED, "ar", 1.4)
d.chip(CX + 104, 168, "issuer: CN=Demo Root", MUTED, 12)

# 판정 1, 2
diamond(CY1, INFO, "발급자 루트가", "설치돼 있나?")
diamond(CY2, INFO, "서명이 루트 키로", "확인되나?")
d.arrow([(CX, CY1 + DH // 2 + 2), (CX, CY2 - DH // 2 - 4)], MUTED, "ar", 1.4)
d.t(CX + 8, 310, "예", 13, MUTED, KR, "start", 600)
d.chip(CX + 172, 304, "tbs 508바이트 + 서명 256바이트", MUTED, 12)

# 거부 둘
for cy, title, sub in ((CY1, "거부: error 20", "발급자 인증서를 못 찾음"), (CY2, "거부: error 7", "서명 불일치 · 한 바이트 변경")):
    d.tone(620, cy - 32, 216, 64, BAD, 6, "14", 1.1)
    d.t(728, cy - 4, title, 12.5, INK, MONO, "middle", 600)
    d.t(728, cy + 18, sub, 12, MUTED, KR, "middle")
    d.arrow([(CX + DW // 2 + 2, cy), (616, cy)], BAD, "bad", 1.4)
    d.t(CX + DW // 2 + 34, cy - 10, "아니오", 12, BAD, KR, "middle", 600)

# 끝
d.arrow([(CX, CY2 + DH // 2 + 2), (CX, 460)], OK, "ok", 1.6)
d.t(CX + 16, 446, "예", 13, OK, KR, "start", 600)
d.tone(CX - 150, 464, 300, 40, OK, 20, "14", 1.6)
d.t(CX, 489, "OK · 공개 키를 사이트 이름에 묶음", 12.5, INK, KR, "middle", 600)

# 선행 조건: 미리 설치된 루트
d.tone(24, 192, 200, 220, ACC, 6, "14", 1.4)
d.t(124, 276, "미리 설치된 루트", 12.5, INK, KR, "middle", 600)
d.t(124, 300, "root.crt 의 공개 키", 12, MUTED, KR, "middle")
d.t(124, 324, "시스템 루트 158개", 12, MUTED, KR, "middle")
for cy in (CY1, CY2):
    d.arrow([(228, cy), (CX - DW // 2 - 4, cy)], ACC, "acc", 1.4)
d.t(258, CY1 - 10, "루트", 12, ACC, KR, "middle", 600)
d.t(258, CY2 - 10, "루트", 12, ACC, KR, "middle", 600)

d.legend(536, [("받은 것", SOFT), ("판정", INFO), ("믿게 되는 결과", OK), ("미리 있어야 하는 것", ACC), ("거부", BAD)])
d.save("45-01.certificate-chain.svg")
