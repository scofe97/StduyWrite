# 04-04 A4 — 같은 a.test:4433 에 SNI 만 바꿔 두 번 붙었을 때 갈리는 것. 출력 subject 두 줄의 실측값만 쓴다.
# 타입 스펙: type-flowchart — 서버가 SNI 값으로 인증서를 가르는 판단 하나. focal 은 그 판단(마름모).
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import W, EYEBROW, Flow, ACC, OK, INFO, MUTED, KR, MONO
H = 440
d = Flow(W, H, EYEBROW + "A4", "A4 · SNI 가 인증서를 고른다",
         "접속 주소와 포트는 a.test:4433 하나로 같고 ClientHello 의 SNI 만 a.test·b.test 로 바꾼다. 서버는 그 이름으로 내보낼 인증서를 고르고, cipher suite 은 두 연결이 같다.",
         "인증서를 고를 이름은 암호화 전에 와야 하므로 SNI 는 평문입니다")
# 암호화 전 구간 표시 — ClientHello 와 판단
d.tone(24, 108, 480, 264, INFO, 8, "0a", 1.0)
d.t(40, 128, "암호화 시작 전 · 평문", 11, INFO, KR, "start", 600)
d.step(136, 212, 192, 72, "ClientHello", "-servername 만 바꿈")
d.arrow([(236, 248), (268, 248)], MUTED, "ar", 1.4)
d.diamond(380, 204, 108, 44, "SNI 값", focal=True)
# 두 갈래 — 오른쪽으로 나가 위·아래로 꺾음
d.arrow([(488, 248), (536, 248), (536, 180), (596, 180)], MUTED, "ar", 1.4)
d.arrow([(536, 248), (536, 316), (596, 316)], MUTED, "ar", 1.4)
d.t(544, 172, "a.test", 11, MUTED, MONO, "start", 600)
d.t(544, 336, "b.test", 11, MUTED, MONO, "start", 600)
d.step(728, 144, 256, 72, "subject=CN = a.test", "기본 -cert a.test.crt", c=OK)
d.step(728, 280, 256, 72, "subject=CN = b.test", "-servername b.test · -cert2", c=OK)
d.t(728, 252, "cipher suite 동일", 11, MUTED, KR, "middle", 600)
d.legend(H - 40, [("서버의 인증서 선택", ACC), ("내보낸 인증서", OK), ("평문 구간", INFO)])
d.save("04-04.a4-sni-cert.svg")
