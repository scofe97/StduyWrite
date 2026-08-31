# 02-01 §1 설치가 끝난 시점에 서 있는 것.
# 본문(원문 2.1.3): istioctl install 뒤 istio-system 에는 istiod · 인그레스 게이트웨이 · 이그레스 게이트웨이
#       셋이 선다. 이 시점에 데이터 플레인은 아직 없다 — 애플리케이션을 올리고 프록시를 주입해야 생긴다.
#       복제본이 하나씩인 것은 데모 프로파일이고, 운영에서는 다중 복제가 의도된 형태다.
#       애드온은 필수가 아니고 여기서 까는 버전은 데모용이지 운영용이 아니다(7 장이 이 문장을 회수한다).
# 타입 스펙: type-deployment — 무엇이 어느 네임스페이스에 서고 무엇이 아직 없는지가 논점이다.
#           존 3 · 노드 5 · 경로 2, accent 는 아직 비어 있는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1200, 640
d = D(W, H, "ISTIO IN ACTION · 02-01 §1",
      "설치가 끝나도 데이터 플레인은 아직 없다",
      "istioctl install 이 세우는 것은 컨트롤 플레인과 게이트웨이 둘뿐이다. 색이 붙은 자리가 아직 "
      "비어 있고, 애플리케이션을 올려 프록시를 주입해야 채워진다. 애드온은 데모용이라고 저자가 못 박는다.",
      "복제본이 하나씩인 것은 demo 프로파일이고 운영에서는 다중 복제가 의도된 형태입니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def node(x, y, w, h, tag, name, sub, focal=False, faint=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif faint:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{INK}04" '
                   f'stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 5"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="40" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 32, y + 23, tag, 8, INK, MONO, "middle", 600)
    d.t(x + 62, y + 24, name, 13, ACC if focal else (SOFT if faint else INK), KR, "start", 600)
    d.t(x + 62, y + 42, sub, 9, MUTED, MONO, "start")

zone(56, 148, 540, 244, "ISTIO-SYSTEM")
zone(660, 148, 484, 116, "ADDONS · SAMPLES")
zone(660, 296, 484, 96, "APPLICATION NAMESPACE")

node(80, 176, 492, 60, "POD", "istiod", "1/1 · 컨트롤 플레인")
node(80, 244, 492, 60, "POD", "istio-ingressgateway", "1/1 · 들어오는 트래픽")
node(80, 312, 492, 60, "POD", "istio-egressgateway", "1/1 · 나가는 트래픽")
node(684, 176, 436, 60, "ADD", "Grafana · Jaeger · Kiali", "demo only · 7장이 걷어낸다", faint=True)
node(684, 320, 436, 52, "GAP", "데이터 플레인", "아직 없다", focal=True)

d.path("M 572 206 L 640 206 L 640 206 L 680 206", INFO, 1.2, m="info")
d.t(626, 190, "함께 깔지만 필수는 아니다", 9, MUTED, KR, "middle")
d.path("M 572 342 L 640 342 L 640 346 L 680 346", ACC, 1.5, m="acc")
d.t(626, 330, "앱 + 주입이 있어야 생긴다", 9, ACC, KR, "middle", 600)

BY = 424
d.box(56, BY, 1088, 84, PAPER2, RULE, 1.0, 6)
d.t(76, BY + 26, "설치 앞뒤로 붙는 확인 명령", 11, ACC, KR, "start", 600)
d.t(76, BY + 50, "istioctl x precheck   ->   istioctl install --set profile=demo -y   ->   istioctl verify-install", 11, INK, MONO, "start")
d.t(76, BY + 70, "마지막 명령은 설치 매니페스트와 클러스터의 실제 상태를 대조해 어긋난 곳을 알린다", 10, SOFT, KR, "start")

d.t(32, 548, "컨트롤 플레인이 통째로 내려가도 데이터 플레인은 단절 기간을 견디도록 구현돼 있다", 11, SOFT, KR, "start")
d.legend(576, [("아직 비어 있는 자리", ACC), ("필수가 아닌 것", INFO)])
d.save("02-01.install-state.svg")
