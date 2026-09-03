# 10-01 §1 요청 하나에 관여하는 것들 — 원문 그림 10.1 + 10.1 절의 실습 시나리오.
# 본문(원문 10 장 도입): 요청을 처리하는 데 참여하는 것은 넷이다. istiod(데이터 플레인을 원하는 상태로
#       동기화), 인그레스 게이트웨이(클러스터로 트래픽을 들인다), 서비스 프록시(접근 제어 + 다운스트림에서
#       로컬 애플리케이션으로), 애플리케이션 자신(요청 처리, 또 다른 upstream 호출).
#       10.1: 사람이 읽는 CRD 가 Envoy 설정으로 번역돼 데이터 플레인에 적용되며, 적용 뒤 동작이 기대와
#       다르면 가장 흔한 원인은 잘못 설정한 것이다. 저자의 예제는 DestinationRule 이 없어 subset 클러스터가
#       정의되지 않은 상황이다.
# 타입 스펙: type-architecture — 구성요소와 연결. 존 셋(사람이 쓰는 설정 · 컨트롤 플레인 · 요청 경로),
#           초점 1곳(빠져 있는 DestinationRule), 직각 연결선.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 612
d = D(W, H, "ISTIO IN ACTION · 10-01 §1",
      "요청 하나에 넷이 관여하고 하나가 비어 있다",
      "사람이 쓴 리소스를 istiod 가 Envoy 설정으로 번역해 데이터 플레인에 내려보내고, 요청은 게이트웨이와 "
      "사이드카를 거쳐 애플리케이션에 닿는다. 색이 붙은 자리가 저자의 예제에서 빠져 있는 리소스다.",
      "전부를 디버깅할 시간이 없기 때문에 어디부터 볼지가 이 장의 내용입니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
    lw = len(label) * 12 + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 12 + lw / 2, y + 17, label, 12, SOFT, KR)

def node(x, y, w, h, title, subs, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="5 5"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, y + 26, title, 14, ACC if focal else INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w / 2, y + 48 + i * 18, s, 12, ACC if focal else MUTED, KR)

zone(24, 116, 252, 328, "사람이 쓰는 리소스")
zone(320, 176, 216, 148, "컨트롤 플레인")
zone(548, 116, 428, 328, "요청 경로")

GW = (24, 148, 252, 68)
VS = (24, 244, 252, 68)
DR = (24, 340, 252, 88)
IS = (340, 208, 176, 88)
CL = (568, 148, 200, 60)
IG = (568, 240, 200, 76)
SP = (568, 356, 200, 76)
AP = (800, 356, 176, 76)

def cy(n): return n[1] + n[3] / 2

for n in (GW, VS, DR):
    c = ACC if n is DR else MUTED
    m = "acc" if n is DR else "ar"
    # 버스는 리소스 오른쪽(276)과 istiod 왼쪽(340) 사이에 둔다. 380 은 istiod(340~516)
    # 안쪽이라 꺾임과 화살촉이 상자 뒤로 숨었다.
    d.path(f"M {n[0] + n[2]} {cy(n)} H 308 V {cy(IS)} H {IS[0] - 2}", c, 1.2, m=m)

# 668 은 IG · SP(둘 다 568~768) 안쪽이라 두 화살표가 통째로 상자 뒤에 가려졌고,
# 하필 IG 의 가로 중앙과 같아 아래 요청 흐름 화살표와도 겹쳤다. istiod 오른쪽(516)과
# 상자 왼쪽(568) 사이인 544 로 옮겨 하나의 줄기에서 둘로 갈라지게 한다.
d.path(f"M {IS[0] + IS[2]} {cy(IS)} H 544 V {cy(IG)} H {IG[0] - 2}", INFO, 1.2, m="info")
d.path(f"M {IS[0] + IS[2]} {cy(IS)} H 544 V {cy(SP)} H {SP[0] - 2}", INFO, 1.2, m="info")

d.path(f"M {CL[0] + CL[2] / 2} {CL[1] + CL[3]} V {IG[1] - 2}", MUTED, 1.2, m="ar")
d.path(f"M {IG[0] + IG[2] / 2} {IG[1] + IG[3]} V {SP[1] - 2}", MUTED, 1.2, m="ar")
d.path(f"M {SP[0] + SP[2]} {cy(SP)} H {AP[0] - 2}", MUTED, 1.2, m="ar")

node(*GW, "Gateway", ["8080 을 연다"])
node(*VS, "VirtualService", ["20% / 80% 로 나눈다"])
node(*DR, "DestinationRule", ["subset 을 정의한다", "예제에는 없다"], focal=True)
node(*IS, "istiod", ["번역과 동기화"])
node(*CL, "curl", ["Host 헤더로 호출"])
node(*IG, "인그레스 게이트웨이", ["트래픽을 들인다"])
node(*SP, "서비스 프록시", ["접근 제어 · 전달"])
node(*AP, "catalog", ["요청을 처리한다"])

d.t(32, 480, "왼쪽 리소스를 istiod 가 읽어 xDS 로 게이트웨이와 사이드카에 내려보낸다 — 저자의 예제는 그중 하나가 빈 채로 돈다", 11, SOFT, KR, "start")
d.t(32, 504, "subset 클러스터가 정의되지 않아 모든 요청이 503 으로 끝나고, 넷 중 어디가 원인인지는 아직 모른다", 11, MUTED, KR, "start")
d.legend(532, [("예제에서 빠져 있는 리소스", ACC), ("istiod 가 내려보내는 설정", INFO)])
d.save("10-01.request-participants.svg")
