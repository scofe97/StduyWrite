# a0-04 §4 Pilot(istiod) 포트의 경계와 보안 배치.
# 본문(부록 D.2 & Istio 1.32 Application Requirements):
#   서비스용 넷(15010 평문 비권장 · 15012 TLS/mTLS 권장 · 15014 메트릭 · 15017 웹훅, 443->15017)
#   디버깅·인트로스펙션용 둘(8080 HTTP 디버그 deprecated · 9876 localhost ControlZ).
# 타입 스펙: type-deployment — 외부 호출원(워크로드·API 서버·도구)과 istiod 파드 경계, 포트별 프로토콜·보안을 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 960, 648
d = D(W, H, "ISTIO IN ACTION · A0-04 §4",
      "istiod 포트의 경계와 15010·15012 보안 분기",
      "워크로드·API 서버·운영 도구가 istiod 파드의 여섯 포트에 붙는 경계와 역할을 보인다. "
      "같은 xDS 를 여는 15010 과 15012 중 평문인 15010 은 권하지 않고 15012 를 쓴다.",
      lead="15012 는 TLS 로 신원을 발급하고 이후 요청을 상호 인증합니다")

# 왼쪽 호출원 구역
d.t(28, 122, "호출 주체", 13, SOFT, KR, "start", 600)
d.o.append(f'<rect x="24" y="132" width="296" height="428" rx="8" fill="{INK}05" '
           f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')

def caller(y, title, sub, c=None):
    if c:
        d.tone(40, y, 264, 68, c, 6, "12", 1.2)
    else:
        d.box(40, y, 264, 68, PAPER2, RULE, 1.0, 6)
    d.t(56, y + 28, title, 13, c or INK, KR, "start", 600)
    d.t(56, y + 50, sub, 13, MUTED, KR, "start")

caller(172, "사이드카", "xDS 설정 · 인증서 요청")
caller(312, "Prometheus", "컨트롤 플레인 메트릭 수집")
caller(392, "K8s API 서버", "사이드카 주입 · 리소스 검증", c=INFO)
caller(476, "운영자 (port-forward)", "로컬 터널로 상태 · 로그 조회")

# 오른쪽 istiod 파드 경계
d.t(448, 122, "istiod 파드", 13, SOFT, KR, "start", 600)
d.o.append(f'<rect x="444" y="132" width="492" height="428" rx="8" fill="{INK}05" '
           f'stroke="{INK}44" stroke-width="1.2"/>')
d.chip(896, 152, "POD", SOFT, 10)

PW, PH = 456, 48
def port_row(y, port, desc, c=None, focal=False):
    if focal:
        d.tone(462, y, PW, PH, ACC, 6, "12", 1.4)
    elif c:
        d.tone(462, y, PW, PH, c, 6, "12", 1.2)
    else:
        d.box(462, y, PW, PH, PAPER2, RULE, 1.0, 6)
    d.t(478, y + 30, port, 14, ACC if focal else (c or INK), MONO, "start", 600)
    d.t(550, y + 30, desc, 13, INK if (focal or c) else MUTED, KR, "start")

port_row(172, "15010", "xDS · 인증서 (평문 · 비권장)", focal=True)
port_row(232, "15012", "xDS · 인증서 (TLS / mTLS 권장)", c=OK)
port_row(312, "15014", "컨트롤 플레인 메트릭", None)
port_row(384, "15017", "웹훅 서버 (Service 443 전달)", c=INFO)
port_row(444, "8080", "Pilot 디버그 (폐기 예정 · HTTP)", None)
port_row(496, "9876", "ControlZ (localhost 인트로스펙션)", None)

# 직각 연결선
d.path("M 304 196 L 460 196", ACC, 1.3, m="acc", dash="4 3")
d.t(382, 184, "평문 위험", 13, ACC, KR, "middle", 600)

d.arrow([(304, 220), (364, 220), (364, 256), (460, 256)], OK, "ok", 1.5)
d.t(382, 276, "mTLS 권장", 13, OK, KR, "middle", 600)

d.arrow([(304, 344), (364, 344), (364, 336), (460, 336)], MUTED, "ar", 1.3)

d.arrow([(304, 412), (364, 412), (364, 408), (460, 408)], INFO, "info", 1.4)
d.t(382, 434, "HTTPS:443", 11, INFO, MONO, "middle")

d.arrow([(304, 496), (364, 496), (364, 468), (460, 468)], MUTED, "ar", 1.3)
d.arrow([(304, 516), (364, 516), (364, 520), (460, 520)], MUTED, "ar", 1.3)

d.legend(588, [("평문이라 권하지 않는 포트", ACC), ("운영 권장 mTLS 포트", OK), ("API 서버 웹훅 경로", INFO)])
d.save("a0-04.pilot-ports.svg")
print("ok a0-04.pilot-ports")
