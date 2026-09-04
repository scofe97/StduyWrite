# a0-02 §1 사이드카를 이루는 넷.
# 본문(부록 B 도입): Istio agent(pilot agent) 가 Envoy 를 띄우고 신원을 부트스트랩하며 컨트롤
#       플레인과 양방향 연결을 유지한다. local DNS proxy 는 최근에 더해졌고 기본은 꺼짐.
#       Envoy 는 에이전트가 사이드카 컨테이너 안에서 프로세스로 띄운다. istio-init 은 init
#       컨테이너로 먼저 돌아 Iptable 규칙을 세워 프록시를 요청 경로에 끼운다.
# 타입 스펙: type-deployment — 무엇이 어느 경계 안에 서고 무엇이 무엇을 띄우는지가 논점이다.
#           존 2 · 노드 5 · 경로 3, accent 는 요청 경로에 프록시를 앉히는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "ISTIO IN ACTION · A0-02 §1",
      "Envoy 는 넷 중 하나이고 스스로 뜨지 않는다",
      "사이드카 컨테이너 안에 에이전트와 Envoy 가 있고 그 밖에 init 컨테이너가 따로 선다. "
      "에이전트가 Envoy 를 띄우고 설정을 넣으며, 색이 붙은 컨테이너가 Envoy 를 요청 경로에 앉힌다.",
      "저자는 사이드카를 그냥 프록시라 부르는 것을 제유라고 적습니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 14
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def node(x, y, w, h, tag, name, sub, focal=False, faint=False, c=None):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif faint:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{INK}04" '
                   f'stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 5"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="44" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 34, y + 23, tag, 8, INK, MONO, "middle", 600)
    d.t(x + 66, y + 24, name, 13, ACC if focal else (SOFT if faint else (c or INK)), KR, "start", 600)
    d.t(x + 66, y + 42, sub, 11, MUTED, KR, "start")

zone(28, 148, 480, 300, "POD")
zone(560, 148, 412, 128, "CONTROL PLANE")

node(48, 184, 440, 60, "APP", "애플리케이션 컨테이너", "우리 코드")
node(48, 268, 440, 60, "INIT", "istio-init", "먼저 돌아 Iptable 규칙을 세운다", focal=True)

d.o.append(f'<rect x="48" y="348" width="440" height="80" rx="6" fill="{INK}07" '
           f'stroke="{INK}44" stroke-width="1"/>')
d.t(64, 366, "SIDECAR CONTAINER", 8, SOFT, MONO, "start", 600)
d.t(64, 392, "istio-agent", 12, INK, MONO, "start", 600)
d.t(64, 412, "Envoy 를 띄우고 신원을 부트스트랩한다", 11, MUTED, KR, "start")
d.t(300, 392, "envoy", 12, INK, MONO, "start", 600)
d.t(300, 412, "에이전트가 설정을 넣는다", 11, MUTED, KR, "start")
d.o.append(f'<rect x="288" y="360" width="188" height="60" rx="4" fill="none" '
           f'stroke="{RULE}" stroke-width="1"/>')
d.arrow([(276, 392), (284, 392)], MUTED, "ar", 1.3)

node(580, 184, 372, 60, "CP", "istiod", "설정과 인증서를 내려보낸다", c=INFO)

d.path("M 488 398 L 528 398 L 528 214 L 576 214", INFO, 1.3, m="info", dash="5 4")
d.t(534, 300, "양방향 연결", 11, INFO, KR, "start", 600)
d.t(534, 322, "최신 설정을 받는다", 11, MUTED, KR, "start")

d.path("M 268 268 L 268 250", ACC, 1.5, m="acc")
d.t(284, 260, "트래픽을 프록시로 돌린다", 11, ACC, KR, "start", 600)

d.t(28, 484, "로컬 DNS 프록시는 에이전트에 나중에 더해진 부품이다 — 기본은 꺼짐이고 설치할 때 켠다", 11, SOFT, KR, "start")
d.t(28, 508, "저자가 든 Envoy 가 무력한 예 셋 — 요청 경로에 앉기 · 신원 부트스트랩 · 인증서 순환", 11, MUTED, KR, "start")
d.legend(532, [("Envoy 를 요청 경로에 앉히는 자리", ACC), ("설정과 인증서가 오는 곳", INFO)])
d.save("a0-02.sidecar-parts.svg")
