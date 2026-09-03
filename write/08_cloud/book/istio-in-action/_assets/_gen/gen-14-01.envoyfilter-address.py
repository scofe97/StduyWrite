# 14-01 §3 EnvoyFilter 가 패치할 자리를 좁혀 가는 경로 — 원문 14.2 의 tap 예제.
# 본문(원문 14.2): 이 예제에서는 인바운드 리스너(SIDECAR_INBOUND)의 HTTP_FILTER 임을 지정하고,
#       8080 포트에 묶인 리스너의 HCM 을 고르고, 그 HCM 의 HTTP 필터 체인에서 envoy.filters.http.router
#       를 고른다. 그 필터를 고른 이유는 새 필터를 바로 그 앞에 놓기 위해서다. patch 절에서는 앞 절에서
#       고른 필터 앞에 설정을 병합한다 — envoy.filters.http.tap 이 라우터 앞에 들어간다.
#       EnvoyFilter 는 선언된 네임스페이스의 모든 워크로드에 적용되며 istio-system 에 만들면 메시 전체다.
#       좁히려면 workloadSelector 를 쓴다.
# 타입 스펙: type-tree — 위에서 아래로 갈수록 범위가 좁아지는 계층. 노드는 왼쪽 정렬,
#           가지는 직각 엘보, 깊이 6, coral 은 최종적으로 꽂히는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 792
d = D(W, H, "ISTIO IN ACTION · 14-01 §3",
      "좌표를 여섯 번 좁혀야 한 자리가 정해진다",
      "네임스페이스에서 시작해 라벨 · 방향 · 포트 · 네트워크 필터 · 서브필터로 내려가면 패치할 자리 하나가 "
      "남는다. 색이 붙은 마디가 새 필터가 실제로 들어가는 곳이다.",
      "저자가 이 리소스를 쓰려면 Envoy 이름 규약에 익숙해야 한다고 적는 이유입니다")

NX, NW, NH, Y0, STEP = 176, 500, 60, 128, 84
nodes = [
    ("NAMESPACE", "istioinaction", "생략하면 이 네임스페이스의 모든 워크로드"),
    ("workloadSelector", "app: webapp", "여기서 폭발 반경이 정해진다"),
    ("context", "SIDECAR_INBOUND", "들어오는 쪽 리스너"),
    ("listener.portNumber", "8080", "그 포트에 묶인 리스너"),
    ("filterChain.filter", "envoy.filters.network.http_connection_manager", "네트워크 필터 중 HCM"),
    ("subFilter", "envoy.filters.http.router", "HCM 의 HTTP 필터 체인에서 종단 필터"),
]
for i, (key, val, note) in enumerate(nodes):
    y = Y0 + i * STEP
    d.box(NX, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(NX + 20, y + 25, key, 9, SOFT, MONO, "start", 600)
    d.t(NX + 20, y + 45, val, 12, INK, MONO, "start", 600)
    d.t(NX + NW + 24, y + 36, note, 11, MUTED, KR, "start")
    if i < len(nodes) - 1:
        d.path(f"M {NX + 40} {y + NH} V {y + STEP - 2}", MUTED, 1.2, m="ar")
    d.t(NX - 24, y + 36, f"{i + 1}", 10, SOFT, MONO, "end", 600)

PY_ = Y0 + len(nodes) * STEP
d.path(f"M {NX + 40} {PY_ - STEP + NH} V {PY_ - 2}", ACC, 1.5, m="acc")
d.o.append(f'<rect x="{NX}" y="{PY_}" width="{NW}" height="{NH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(NX + 20, PY_ + 25, "patch.operation", 9, ACC, MONO, "start", 600)
d.t(NX + 20, PY_ + 45, "INSERT_BEFORE  ->  envoy.filters.http.tap", 12, ACC, MONO, "start", 600)
d.t(NX + NW + 24, PY_ + 36, "라우터 바로 앞에 끼운다", 11, ACC, KR, "start")

d.t(24, 728, "저자의 경고 셋 — 하위 호환을 가정하지 말 것 · 다른 Istio 리소스가 전부 번역된 뒤에 적용됨 · 잘못 쓰면 데이터 플레인 전체가 내려감", 11, SOFT, KR, "start")
d.legend(748, [("새 필터가 실제로 들어가는 자리", ACC), ("좌표를 좁히는 마디", MUTED)])
d.save("14-01.envoyfilter-address.svg")
