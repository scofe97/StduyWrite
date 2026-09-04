# 14-01 §8 프록시가 레지스트리에서 모듈을 직접 당겨 온다 — 원문 14.5.5.
# 본문(원문 14.5.5): WasmPlugin 은 httpbin 워크로드를 selector 로 고르고 모듈 URL(oci · file 또는 https)을
#       지정해 Wasm 필터를 Istio 데이터 플레인에 싣는다. "이 예제에서는 모듈을 OCI 규격 레지스트리에서
#       곧장 당겨 온다 — 앞 절에서 이미 발행했고, 이 설정에서 그것을 레지스트리에서 프록시로 직접
#       내려받는다." 적용한 뒤 httpbin 을 부르면 응답 헤더 hello 가 world! 값으로 온다. 저자는 Wasm 이면
#       언어를 골라 Envoy 를 확장하고 모듈을 런타임에 동적으로 로드할 수 있으며, Istio 에서는 WasmPlugin
#       으로 선언적으로 싣는다고 닫는다.
# 당겨 오는 주체는 컨트롤 플레인이 아니라 프록시다 — 그래서 레지스트리로 가는 화살표가 사이드카에서 나간다.
# 타입 스펙: type-deployment — 무엇이 어디에 놓이고 무엇이 어디서 오는지가 논점이다.
#           존 3 · 노드 5 · 경로 3, accent 는 선언 하나로 그 일이 일어나게 만드는 자리.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "ISTIO IN ACTION · 14-01 §8",
      "좌표를 찍는 대신 워크로드와 URL 만 적는다",
      "3 절의 EnvoyFilter 가 Envoy 이름으로 자리를 찍어야 했다면, 여기서는 고를 워크로드와 모듈의 주소만 "
      "적는다. 색이 붙은 리소스가 그 선언이고, 모듈을 당겨 오는 것은 컨트롤 플레인이 아니라 프록시다.",
      "저자가 장을 닫으며 쓰는 낱말이 '선언적으로' 입니다")

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
    # 부제는 태그 칩 아래 줄이라 칩을 피해 들여쓸 이유가 없다. x+62 로 두면
    # "selector · pluginName · url" 이 상자 오른쪽 변에 정확히 닿아 url 이 잘려 보인다.
    d.t(x + 16, y + 42, sub, 11, MUTED, MONO, "start")

zone(40, 140, 280, 236, "CONTROL PLANE")
zone(364, 140, 276, 236, "DATA PLANE")
zone(688, 140, 276, 236, "OCI REGISTRY")

node(60, 168, 240, 68, "CRD", "WasmPlugin", "selector · pluginName · url", focal=True)
node(60, 264, 240, 68, "CFG", "istiod", "고른 워크로드에 내려보낸다")
node(384, 216, 240, 68, "POD", "httpbin 사이드카", "모듈을 런타임에 로드한다")
node(708, 168, 236, 68, "IMG", "istioinaction-demo", "레이어 하나가 .wasm 모듈")
node(708, 264, 236, 68, "META", "runtime-config.json", "호환 Envoy 버전 · ABI")

d.path("M 180 236 V 260", MUTED, 1.2, m="ar")
d.path("M 300 298 H 332 V 250 H 380", INFO, 1.3, m="info")
d.path("M 624 240 H 656 V 202 H 704", ACC, 1.5, m="acc")
d.t(352, 232, "설정", 11, INFO, KR, "middle", 600)
d.t(656, 186, "url 이 가리키는 곳", 11, ACC, KR, "middle", 600)

BY = 412
d.box(40, BY, 924, 92, PAPER2, RULE, 1.0, 6)
d.t(56, BY + 26, "저자가 드는 URL 스킴 셋", 11, ACC, KR, "start", 600)
d.t(56, BY + 50, "oci  ·  file  ·  https", 12, INK, MONO, "start")
d.t(56, BY + 72, "적용한 뒤 httpbin 을 부르면 응답 헤더에 hello: world! 가 붙어 온다", 11, SOFT, KR, "start")

d.t(24, 548, "3 절과 견주면 — 거기서는 방향 · 포트 · 네트워크 필터 · 서브필터를 Envoy 이름으로 찍어야 했다", 11, SOFT, KR, "start")
d.legend(568, [("선언 하나로 그 일이 일어나는 자리", ACC), ("컨트롤 플레인이 내려보내는 것", INFO)])
d.save("14-01.wasmplugin-pull.svg")
