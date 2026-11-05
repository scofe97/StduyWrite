# 02-01 §3 — HTTPS 는 Ingress 컨트롤러까지이고, 그 뒤 Service 와 Pod 구간은 평문 HTTP 다.
# 본문 근거: 이 노트 §3 「TLS 는 Ingress 컨트롤러에서 끝나고 그 뒤는 평문입니다」.
# 책 쪽: "the communication typically uses unencrypted HTTP network communication as soon as it passes the Ingress" /
#        Example 2-4(t75 의 nginx-deployment·accounting-service) · Example 2-5(accounting-secret, kubernetes.io/tls) ·
#        Example 2-6(accounting-ingress, spec.tls[] 와 rules).
# 타입 스펙: type-architecture — 신뢰 경계(암호화 구간과 평문 구간)로 구성요소를 묶는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, WARN, INFO, KR, MONO

W, H = 960, 572
d = D(W, H, "CKS STUDY GUIDE · 02-01 §3",
      "TLS 종료 지점과 암호화 경계",
      "클라이언트에서 Ingress 컨트롤러까지는 HTTPS 443 으로 오가고, 컨트롤러가 인증서와 키로 TLS 를 끝낸 뒤 "
      "Service 와 Pod 까지는 평문 HTTP 80 으로 전달되는 경로를 그린 구조도다.",
      "인증서와 키는 Secret 에 두고, 컨트롤러가 읽어 TLS 를 끝냅니다")

BX = 380  # 컨트롤러 중심 x — 두 구간 사이의 신뢰 경계
CW = 168
CXL = BX - CW / 2
CXR = CXL + CW
BAND_Y, BAND_H = 100, 200
d.box(12, BAND_Y, CXL - 8 - 12, BAND_H, OK + "0E", OK + "55", 0.9)
d.box(CXR + 8, BAND_Y, 948 - (CXR + 8), BAND_H, WARN + "0E", WARN + "55", 0.9)
d.t(28, BAND_Y + 28, "HTTPS 구간", 13, OK, KR, "start", 600)
d.t(CXR + 24, BAND_Y + 28, "평문 HTTP 구간", 13, WARN, KR, "start", 600)

Y, BH = 192, 76
MID = Y + BH / 2


def node(x, w, title, sub, c=INK, fam=KR):
    d.box(x, Y, w, BH, PAPER2, RULE, 1.0)
    d.t(x + w / 2, Y + 32, title, 15, c, KR, "middle", 600)
    d.t(x + w / 2, Y + 54, sub, 12, MUTED, fam)


node(24, 168, "curl 클라이언트", "accounting.example.com")
# 컨트롤러는 두 구간 사이에 놓여 경계 노릇을 한다
d.tone(CXL, Y - 12, CW, BH + 24, ACC, 6, "26", 1.6)
d.t(BX, Y + 30, "Ingress 컨트롤러", 15, ACC, KR, "middle", 600)
d.t(BX, Y + 54, "TLS 종료 지점", 12, MUTED, KR)
node(556, 168, "Service", "accounting-service:80", INK, MONO)
node(812, 124, "Pod ×3", "nginx-deployment", INK, MONO)

d.path(f"M 192 {MID} L {CXL - 2} {MID}", OK, 1.8, m="ok")
d.chip((192 + CXL) / 2, MID - 22, "HTTPS 443", OK, 12)
d.path(f"M {CXL + CW} {MID} L 554 {MID}", WARN, 1.8, m="warn")
d.chip((CXL + CW + 554) / 2, MID - 22, "HTTP 80", WARN, 12)
d.path(f"M 724 {MID} L 810 {MID}", WARN, 1.8, m="warn")
d.chip(767, MID - 22, "HTTP 80", WARN, 12)

# 구성 리소스 → 컨트롤러
RY, RH = 436, 68
d.box(196, RY, 176, RH, INFO + "14", INFO, 1.2)
d.t(284, RY + 28, "Ingress", 15, INFO, KR, "middle", 600)
d.t(284, RY + 50, "accounting-ingress", 12, MUTED, MONO)
d.box(388, RY, 204, RH, INFO + "14", INFO, 1.2)
d.t(490, RY + 28, "Secret", 15, INFO, KR, "middle", 600)
d.t(490, RY + 50, "accounting-secret", 12, MUTED, MONO)
d.path(f"M 332 {RY} L 332 {Y + BH + 14}", INFO, 1.4, m="info", dash="5 4")
d.chip(332, 340, "spec.tls · rules", INFO, 12)
d.path(f"M 428 {RY} L 428 {Y + BH + 14}", INFO, 1.4, m="info", dash="5 4")
d.chip(428, 384, "tls.crt · tls.key", INFO, 12)

d.legend(528, [("암호화 구간", OK), ("평문 구간", WARN), ("TLS 종료 지점", ACC), ("설정 리소스", INFO)])
d.save("02-01.tls-termination.svg")
