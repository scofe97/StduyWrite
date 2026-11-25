# a0-02 §1 사이드카를 이루는 부품 넷.
# 값 근거(본문 §1 · 부록 B 도입):
#   - istio-agent(pilot agent): Envoy 기동, 신원 부트스트랩, 컨트롤 플레인 양방향 연결.
#   - 로컬 DNS 프록시: 에이전트에 더해진 부품, 사이드카 모드 기본 꺼짐(Ambient 1.25+ 기본 켜짐).
#   - Envoy 프록시: 에이전트가 사이드카 컨테이너 안에서 프로세스로 기동.
#   - istio-init: init 컨테이너로 먼저 돌아 iptables 규칙을 세워 프록시를 요청 경로에 앉힘.
# 타입 스펙: type-deployment — 경계(Pod · Sidecar Container · Control Plane) 안 배치와 기동·연결 관계.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 560
d = D(W, H, "ISTIO IN ACTION · A0-02 §1",
      "Envoy 는 부품 넷 중 하나이고 스스로 뜨지 않는다",
      "파드 안에 애플리케이션, istio-init, 사이드카 컨테이너가 서고, 사이드카 컨테이너 안에 istio-agent 와 "
      "Envoy 와 로컬 DNS 프록시가 돈다. istio-init 이 iptables 로 요청 경로에 Envoy 를 앉힌다.",
      lead="점선 테두리는 파드·컨테이너·컨트롤 플레인 경계, 코랄색은 요청 경로에 앉히는 자리입니다.")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 22, label, 12, SOFT, MONO, "start", 600)


def node(x, y, w, h, tag, name, sub, focal=False, c=None):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "14", 1.4)
    elif c:
        d.tone(x, y, w, h, c, 6, "12", 1.2)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="48" height="18" rx="3" fill="{INK}14"/>')
    d.t(x + 36, y + 25, tag, 11, INK, MONO, "middle", 600)
    d.t(x + 72, y + 26, name, 14, ACC if focal else (c or INK), KR if any("가" <= ch <= "힣" for ch in name) else MONO, "start", 600)
    d.t(x + 72, y + 48, sub, 13, MUTED, KR, "start")


zone(24, 116, 480, 360, "POD")
zone(560, 116, 376, 136, "CONTROL PLANE")

node(44, 152, 440, 64, "APP", "애플리케이션 컨테이너", "애플리케이션 코드 실행")
node(44, 244, 440, 64, "INIT", "istio-init", "먼저 돌아 iptables 규칙을 세운다", focal=True)

# 사이드카 컨테이너 내부: istio-agent, envoy, local DNS proxy
d.o.append(f'<rect x="44" y="332" width="440" height="128" rx="6" fill="{INK}07" '
           f'stroke="{INK}44" stroke-width="1"/>')
d.t(60, 354, "SIDECAR CONTAINER", 12, SOFT, MONO, "start", 600)

# local dns proxy (optional / disabled by default in sidecar)
d.o.append(f'<rect x="60" y="366" width="98" height="80" rx="4" fill="{INK}04" '
           f'stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(109, 392, "DNS 프록시", 13, SOFT, KR, "middle", 600)
d.t(109, 416, "기본 꺼짐", 13, MUTED, KR, "middle")
d.t(109, 434, "이름 해석", 13, MUTED, KR, "middle")

# envoy
d.box(172, 366, 108, 80, PAPER2, RULE, 1.0, 4)
d.t(226, 392, "envoy", 13, INK, MONO, "middle", 600)
d.t(226, 416, "요청 처리", 13, MUTED, KR, "middle")
d.t(226, 434, "설정 수신", 13, MUTED, KR, "middle")

# istio-agent (istiod 쪽 오른쪽 가장자리에 둔다)
d.box(294, 366, 176, 80, PAPER2, RULE, 1.0, 4)
d.t(382, 390, "istio-agent", 13, INK, MONO, "middle", 600)
d.t(382, 412, "Envoy 기동 · 신원", 13, MUTED, KR, "middle")
d.t(382, 432, "부트스트랩 · 인증서 순환", 13, MUTED, KR, "middle")

d.arrow([(294, 406), (282, 406)], MUTED, "ar", 1.3)

node(580, 156, 336, 68, "CP", "istiod", "설정과 인증서를 내려보낸다", c=INFO)

# istio-agent <-> istiod (양방향: 서로 반대 방향 화살표 둘)
d.path("M 470 398 L 532 398 L 532 180 L 578 180", INFO, 1.4, m="info")
d.path("M 578 200 L 546 200 L 546 414 L 470 414", INFO, 1.4, m="info")
d.t(558, 290, "양방향 연결", 13, INFO, KR, "start", 600)
d.t(558, 312, "설정 · 인증서", 13, MUTED, KR, "start")

# istio-init -> envoy (iptables 로 앱 트래픽을 Envoy 로 돌림)
d.path("M 226 308 L 226 364", ACC, 1.5, m="acc")
d.t(242, 326, "트래픽을 Envoy 로 돌린다", 13, ACC, KR, "start", 600)

d.legend(504, [("Envoy 를 요청 경로에 앉히는 자리", ACC), ("설정과 인증서가 오는 곳", INFO)])
d.save("a0-02.sidecar-parts.svg")
print("ok sidecar-parts")
