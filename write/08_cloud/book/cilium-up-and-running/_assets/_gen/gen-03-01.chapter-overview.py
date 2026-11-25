# 03-01 개념도 — 도구만 갖춘 상태에서 시작한 클러스터가 NotReady 에서 Hubble 판정 기록까지 다섯 상태를 지나며, 상태 사이를 넘기는 명령과 상태마다 보이는 값을 한 줄기로 잇는다.
# 본문 요구(03-01 「학습 목표」 개요 문단과 「빈 클러스터에서 정책 판정을 보기까지」 표): 시작은 도구 준비(§1), 상태 다섯은 §2~§6, 마지막 상태가 핵심 요약이 고르는 한 줄(정책 판정 기록).
# 값 근거: 03-01 본문 §1 도구 표(brew install), §2 `kubectl get nodes` NotReady ×3 · NetworkReady=false(원문 사본 줄 193~195, 209),
#          §3 `cilium status` cilium 3/3 · cilium-envoy 3/3 · cilium-operator 1/1(원문 사본 줄 384~386), §4 curl 10.96.242.74 · EndpointSlice 10.244.2.127,10.244.2.189,
#          §5 exit 28 · 403 Access denied, §6 policy-verdict:none INGRESS DENIED · ID:8087 <> ID:5834 · TCP Flags: SYN.
# 타입 스펙: type-state — 대상 하나(클러스터)가 국면 다섯을 차례로 지나는 생애 지도다. 고른 이유: 이 장의 줄기가 「상태가 바뀔 때마다 보이는 값이 달라진다」는 일생이라
#             절 하나에 한 칸인 격자로는 상태 사이를 넘기는 명령이 사라진다. 시작 점 하나와 상태 다섯, 마지막 상태에 코랄을 건다. 스펙에 좌표 공식이 없어 stride 92 로 직접 잡았다.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 640


def fam(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "CILIUM UP AND RUNNING · 03-01 OVERVIEW",
      "NotReady 에서 Hubble 의 판정 기록까지",
      "도구만 갖춘 상태에서 시작한 클러스터가 다섯 상태를 지나고, 상태마다 보이는 값이 바뀐다. "
      "NotReady 노드 셋은 Cilium 설치로 cilium 3/3 이 되고, 예제 앱이 서비스 IP 로 응답한 뒤, 정책이 요청을 타임아웃과 403 으로 가르고, Hubble 이 그 판정을 흐름 한 줄로 남긴다.",
      lead="카드는 클러스터의 상태와 그때 보이는 값, 화살표 옆 글자는 다음 상태로 넘기는 명령, 칩은 그 상태를 다루는 절입니다.")

X0, CW, CH, STRIDE, Y0 = 24, 872, 56, 92, 152
AX = 64  # 화살표 줄기 x

# 시작: 도구 준비
d.o.append(f'<circle cx="{AX}" cy="112" r="6" fill="{INK}"/>')
d.t(84, 117, "도구 준비", 13, INK, KR, "start", 600)
d.t(172, 117, "brew install kind cilium-cli hubble helm", 12, MUTED, MONO, "start")
d.chip(520, 112, "§1", MUTED, 11)

states = (
    ("CNI 없는 클러스터", "노드 셋이 일을 받지 못함", INFO, "§2",
     "kubectl get nodes → NotReady ×3", "NetworkReady=false · cni plugin not initialized"),
    ("Cilium 이 설치됨", "Pod 네트워크가 열림", OK, "§3",
     "cilium status → Cilium: OK · Operator: OK", "cilium 3/3 · cilium-envoy 3/3 · cilium-operator 1/1"),
    ("앱이 서비스 IP 로 응답", "정책 전의 기준선", MUTED, "§4",
     "curl 10.96.242.74 → Welcome to nginx!", "endpoints 10.244.2.127 → 10.244.2.127,10.244.2.189"),
    ("정책이 요청을 가름", "라벨 허용과 L7 경로 제한", OK, "§5",
     "unauthorized-client → exit 28", "/50x.html → 403 Access denied"),
    ("판정이 흐름 한 줄로 남음", "Hubble 이 판정을 기록", ACC, "§6",
     "policy-verdict:none INGRESS DENIED", "ID:8087 <> ID:5834 · TCP Flags: SYN"),
)
arrows = (
    "kind create cluster --config kind.yaml",
    "helm install cilium cilium/cilium -n kube-system",
    "nginx-deployment · netshoot-client 배포",
    "CiliumNetworkPolicy ch03-policy 적용",
    "hubble.relay.enabled=true · hubble observe",
)

for i, (title, sub, col, sec, v1, v2) in enumerate(states):
    y = Y0 + i * STRIDE
    if col == ACC:
        d.tone(X0, y, CW, CH, ACC, 6, "12", 1.4)
    elif col == MUTED:
        d.box(X0, y, CW, CH, PAPER2, RULE, 0.9, 6)
    else:
        d.tone(X0, y, CW, CH, col, 6, "14", 1.1)
    d.chip(X0 + 30, y + 28, sec, col, 11)
    d.t(X0 + 64, y + 26, title, 14, INK if col == MUTED else col, KR, "start", 600)
    d.t(X0 + 64, y + 46, sub, 12, MUTED, KR, "start")
    d.line(X0 + 292, y + 10, X0 + 292, y + CH - 10, RULE, 0.8)
    d.t(X0 + 312, y + 26, v1, 12, INK, fam(v1), "start", 600)
    d.t(X0 + 312, y + 46, v2, 12, MUTED, fam(v2), "start")
    # 이 상태로 들어오는 화살표와 라벨
    y_from = 124 if i == 0 else Y0 + (i - 1) * STRIDE + CH + 2
    d.arrow([(AX, y_from), (AX, y - 2)], MUTED, "ar", 1.4)
    d.t(AX + 16, (y_from + y) / 2 + 4, arrows[i], 12, MUTED, fam(arrows[i]), "start")

d.legend(H - 40, [("문제", INFO), ("대응", OK), ("이 편의 한 줄", ACC), ("중립", MUTED)])
d.save("03-01.chapter-overview.svg")
print("ok 03-01 overview")
