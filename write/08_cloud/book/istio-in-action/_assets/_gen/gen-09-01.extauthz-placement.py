# 09-01 §8 외부 인가 서비스가 놓일 수 있는 자리.
# 본문(저자 9.5): ExtAuthz 서비스는 메시 안에, 애플리케이션의 사이드카로, 또는 메시 밖에 살 수 있다.
#       호출이 요청 경로 안에서 일어나므로 지연이 늘고, 오버헤드를 줄이려면 사이드카 배치를 고를 수 있다.
# 저자의 실습은 첫 번째(메시 안 별도 서비스)이고, 주소·포트는 컨피그맵 값 그대로다.
# 타입 스펙: type-deployment — 무엇이 어디에 놓이고 어느 포트로 열리는지가 논점이다.
#           존 3 · 노드 4 · 경로 3, accent 는 요청 경로에 끼어드는 호출 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 660
d = D(W, H, "ISTIO IN ACTION · 09-01 §8",
      "판단을 밖으로 내보내면 요청 경로가 하나 길어진다",
      "프록시가 요청을 잠시 멈추고 외부 인가 서비스에 물어본다. 그 서비스가 살 수 있는 자리는 셋이고, "
      "어디에 두든 호출은 요청 경로 안에서 일어난다. 색이 붙은 경로가 늘어나는 지연이다.",
      "저자의 실습은 메시 안 별도 서비스이고, 오버헤드를 줄이려면 사이드카 배치를 고릅니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def node(x, y, w, h, tag, name, sub, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="40" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 32, y + 23, tag, 8, INK, MONO, "middle", 600)
    d.t(x + 62, y + 24, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 62, y + 42, sub, 9, MUTED, MONO, "start")

zone(48, 152, 316, 208, "ISTIOINACTION")
zone(432, 152, 316, 208, "SAME POD")
zone(48, 428, 700, 120, "OUTSIDE THE MESH")

node(68, 184, 276, 68, "POD", "webapp", "app + istio-proxy", focal=True)
node(68, 276, 276, 60, "SVC", "ext-authz", "8000/TCP · 9000/TCP")
node(448, 184, 276, 68, "POD", "webapp", "app + proxy + ext-authz")
node(448, 276, 276, 60, "NOTE", "사이드카 배치", "네트워크 오버헤드가 가장 작다")
node(68, 456, 680, 64, "EXT", "메시 밖 인가 서버", "OPA · Gloo Edge · 자체 구현 — CheckRequest API")

# 요청 경로에 끼어드는 호출
d.path("M 204 252 L 204 274", ACC, 1.6, m="acc")
d.t(216, 268, "요청이 멈춘다", 11, ACC, KR, "start", 600)
d.path("M 588 252 L 588 274", MUTED, 1.2, m="ar")
d.path("M 204 336 L 204 380 L 408 380 L 408 454", INFO, 1.2, m="ar")
d.t(216, 372, "extensionProviders 에 등록한 주소로", 9, MUTED, MONO, "start")

d.t(28, 584, "action: CUSTOM 은 가장 먼저 평가된다 — 외부가 거부하면 DENY·ALLOW 는 볼 일이 없다", 11, SOFT, KR, "start")
d.legend(608, [("요청 경로에 더해지는 지연", ACC), ("설정으로 가리키는 주소", INFO)])
d.save("09-01.extauthz-placement.svg")
