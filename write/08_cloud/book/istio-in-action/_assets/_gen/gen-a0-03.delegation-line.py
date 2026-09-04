# a0-03 §1 어디서 넘기고 어디서부터 남기는가.
# 본문(부록 C.1): PKI 가 인증서를 발급하고 TLS 가 그것으로 핸드셰이크를 한다. 최종 사용자 인증은
#       애플리케이션의 몫이고 Istio 는 JWT 를 지원한다(9 장 §4). C.2 부터가 SPIFFE 다.
# README 의 경계: 인증·인가 기초는 99_ETC/security, X.509 와 CA 는 Container Security 11 장.
# 타입 스펙: type-layers — 아래에서 위로 쌓인 층 중 어디까지가 남의 몫인지가 논점이다.
#           층을 아래에서 위로 놓고 경계선을 하나 그어 위임과 보유를 가른다.
#           축약: accent 는 이 노트가 시작하는 층 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 940, 572
d = D(W, H, "ISTIO IN ACTION · A0-03 §1",
      "사다리의 위쪽 두 칸만 이 노트가 맡는다",
      "부록 C 는 PKI 에서 시작해 SPIFFE 로 올라간다. 아래 두 층은 이 폴더 밖이 SSOT 라 넘기고, "
      "색이 붙은 층부터 여기서 다룬다. 판별 기준은 Istio 를 쓸 줄 아는 사람에게도 새로운가 하나다.",
      "넘기기 전에 한 줄만 회수합니다 — TLS 는 서버를 클라이언트에게만 증명합니다")

LW, LX = 520, 40
LAYERS = [
    (416, "PKI", "인증서를 발급하고 검증하는 틀", False),
    (336, "TLS", "그 인증서로 핸드셰이크한다", False),
    (232, "SPIFFE", "워크로드에 신원을 주는 규격 넷", True),
    (152, "Istio 의 구현", "auto mTLS · filter metadata", False),
]
for y, name, sub, focal in LAYERS:
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="64" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX, y, LW, 64, PAPER2, RULE, 1.0, 6)
    d.t(LX + 20, y + 26, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(LX + 20, y + 46, sub, 11, MUTED, KR, "start")

CUT = 312
d.line(24, CUT, 916, CUT, ACC, 1.2, "6 4")
d.t(596, CUT - 10, "여기서부터 이 노트가 맡는다", 11, ACC, KR, "start", 600)
d.t(596, CUT + 24, "아래 둘의 SSOT", 11, INFO, KR, "start", 600)
d.t(596, CUT + 46, "99_ETC/security · 01_concepts", 11, MUTED, MONO, "start")
d.t(596, CUT + 66, "Container Security 11 장", 11, MUTED, KR, "start")

d.t(596, 180, "9 장이 리소스 쓰는 법을,", 11, SOFT, KR, "start")
d.t(596, 200, "이 부록이 그 아래 규격을 맡는다", 11, MUTED, KR, "start")

d.t(28, 512, "TLS 핸드셰이크의 결과는 서버 인증과 대칭 키 교환 둘 — 대칭 키를 쓰는 이유는 성능이다", 11, SOFT, KR, "start")
d.legend(532, [("이 노트가 시작하는 층", ACC), ("이 폴더 밖이 맡는 층", INFO)])
d.save("a0-03.delegation-line.svg")
