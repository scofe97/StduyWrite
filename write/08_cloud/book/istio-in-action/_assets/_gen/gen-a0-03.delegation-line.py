# a0-03 §1 어디서 넘기고 어디서부터 남기는가.
# 값 근거(본문 a0-03 §1, 이 문서가 다루지 않는 것):
#   - PKI 와 TLS 핸드셰이크(서버 인증, 대칭 키 교환)는 인증과 인가 · JWT 설계 · OAuth2 와 OIDC 문서와 Container Security 11장이 SSOT.
#   - 이 노트는 SPIFFE 와 Istio 의 구현(auto mTLS · filter metadata)을 다루며, 리소스 사용법은 9장이 맡는다.
# 타입 스펙: type-layers — 아래에서 위로 쌓인 층 중 어디까지가 남의 몫인지가 논점이다.
#           층을 아래에서 위로 놓고 경계선을 하나 그어 위임과 보유를 가른다.
#           축약: accent 는 이 노트가 시작하는 층 하나에, info 는 폴더 밖 SSOT 층에 건다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 592


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ISTIO IN ACTION · A0-03 §1",
      "사다리의 위쪽 두 칸만 이 노트가 맡는다",
      "PKI 에서 시작해 SPIFFE 로 올라가는 사다리다. 아래 두 층은 이 폴더 밖이 SSOT 라 넘기고, "
      "색이 붙은 층부터 여기서 다룬다. 판별 기준은 Istio 를 쓸 줄 아는 사람에게도 새로운가 하나다.",
      "넘기기 전에 TLS 가 남기는 결과 하나만 짚습니다 — TLS 는 서버를 클라이언트에게만 증명합니다")

LW, LX = 520, 40
LAYERS = [
    (424, "PKI", "인증서를 발급하고 검증하는 틀", "info"),
    (344, "TLS", "그 인증서로 핸드셰이크한다", "info"),
    (232, "SPIFFE", "워크로드에 신원을 주는 규격 넷", "acc"),
    (152, "Istio 의 구현", "auto mTLS · filter metadata", "neutral"),
]
for y, name, sub, kind in LAYERS:
    if kind == "acc":
        d.tone(LX, y, LW, 64, ACC, 6, "14", 1.4)
        nc = ACC
    elif kind == "info":
        d.tone(LX, y, LW, 64, INFO, 6, "14", 1.2)
        nc = INFO
    else:
        d.box(LX, y, LW, 64, PAPER2, RULE, 1.0, 6)
        nc = INK
    d.t(LX + 20, y + 26, name, 14, nc, kr(name), "start", 600)
    d.t(LX + 20, y + 48, sub, 13, MUTED, KR, "start")

CUT = 316
d.line(24, CUT, 936, CUT, ACC, 1.2, "6 4")
d.t(592, CUT - 12, "여기서부터 이 노트가 맡는다", 13, ACC, KR, "start", 600)
d.t(592, CUT + 26, "아래 둘의 SSOT", 13, INFO, KR, "start", 600)
d.t(592, CUT + 50, "인증과 인가 · JWT 설계 · OAuth2 와 OIDC", 13, MUTED, KR, "start")
d.t(592, CUT + 72, "Container Security 11장", 13, MUTED, KR, "start")

d.t(592, 180, "9장이 리소스 설정을,", 13, SOFT, KR, "start")
d.t(592, 202, "이 부록이 내부 동작을 맡는다", 13, MUTED, KR, "start")

d.t(28, 524, "TLS 핸드셰이크 결과: 서버 인증 · 대칭 키 교환(비대칭보다 성능 우위)", 13, SOFT, KR, "start")
d.legend(544, [("이 노트가 시작하는 층", ACC), ("이 폴더 밖이 맡는 층", INFO)])
d.save("a0-03.delegation-line.svg")
print("ok delegation-line")
