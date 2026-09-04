# a0-04 §4 Pilot 의 포트가 향하는 두 방향.
# 본문(부록 D.2): 서비스용 넷 — 15010 은 평문이라 "Using this port is not recommended because
#       the traffic can be sniffed", 15012 는 "the same information ... but makes it secure",
#       15014 는 컨트롤 플레인 메트릭, 15017 은 웹훅 서버. 디버그용 둘 — 8080 · 9876.
# 타입 스펙: type-architecture — 컴포넌트 하나가 어느 경계로 무엇을 여는지가 논점이다.
#           존과 컴포넌트로 두 방향을 나란히 두고 같은 것을 여는 둘을 붙여 대조한다.
#           축약: accent 는 저자가 권하지 않는 포트 하나에 걸어 대조가 보이게 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 596
d = D(W, H, "ISTIO IN ACTION · A0-04 §4",
      "같은 것을 여는 포트가 둘인데 하나만 안전하다",
      "istiod 도 서비스를 향한 넷과 사람을 향한 둘로 갈린다. 위의 둘은 같은 것을 노출하고 보안만 "
      "다르므로 선택지가 아니라 권고 하나로 정리된다. 색이 붙은 것이 쓰지 말라고 적힌 쪽이다.",
      "13 장에서 VM 이 동서 게이트웨이를 거쳐 붙던 곳이 15012 입니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    # 존 라벨이 한글이라 8px eyebrow 관례를 쓸 수 없다(계약 하한 11px). 마스크도 함께 키운다.
    tw = int(sum(11 if '가' <= c <= '힣' else 6.9 for c in label)) + 20
    d.o.append(f'<rect x="{x + 12}" y="{y - 9}" width="{tw}" height="18" fill="{PAPER}"/>')
    d.t(x + 20, y + 4, label, 11, SOFT, KR, "start", 600)

PW, PH = 400, 56
def port(x, y, num, what, c=None, bad=False):
    if bad:
        d.o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, PW, PH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 34, num, 14, ACC if bad else (c or INK), MONO, "start", 600)
    d.t(x + 92, y + 34, what, 11, MUTED, KR, "start")

zone(28, 148, 440, 300, "서비스를 향한 넷")
zone(532, 148, 440, 156, "사람을 향한 둘")

port(48, 176, "15010", "xDS · 인증서 발급 — 평문", bad=True)
port(48, 248, "15012", "같은 것을 안전하게", c=OK)
port(48, 320, "15014", "컨트롤 플레인 메트릭")
port(48, 380, "15017", "웹훅 서버 — 주입과 검증", c=INFO)

port(552, 176, "8080", "Pilot 디버그 엔드포인트")
port(552, 236, "9876", "ControlZ 인터페이스")

d.path("M 460 204 L 500 204 L 500 276 L 452 276", MUTED, 1.3, m="ar", dash="4 3")
d.t(504, 244, "같은 것을 준다", 11, SOFT, KR, "start", 600)

d.t(552, 340, "저자의 경고 — 8080 은 민감한 정보를 담아", 11, ACC, KR, "start", 600)
d.t(552, 362, "운영에서 끄기를 권한다", 11, MUTED, KR, "start")
d.t(552, 384, "ENABLE_DEBUG_ON_HTTP=false", 11, INK, MONO, "start")

d.t(28, 488, "15012 는 신원 발급에 TLS 를 쓰고 이후 요청은 상호 인증된다 — 15010 은 트래픽이 스니핑될 수 있다", 11, SOFT, KR, "start")
d.t(28, 512, "15017 은 부록 B 의 MutatingWebhookConfiguration 이 요청을 보내는 자리다", 11, MUTED, KR, "start")
d.legend(536, [("저자가 권하지 않는 포트", ACC), ("그 대신 쓰는 포트", OK), ("주입 · 검증이 오는 자리", INFO)])
d.save("a0-04.pilot-ports.svg")
