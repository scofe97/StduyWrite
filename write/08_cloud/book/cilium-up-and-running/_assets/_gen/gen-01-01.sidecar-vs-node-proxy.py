# 타입 스펙: type-deployment — 한 노드의 Pod 1·2·…·50 기준 사이드카 메시와 노드 프록시 메시 배치 비교.
# 사실 출처: 본문 §4 (L142: Pod 50개면 Envoy 50개, L148: L3/L4 라우팅·로드밸런싱·접근 제어·암호화는 eBPF,
#   L150: L7 처리가 필요할 때만 노드 공유 Envoy·Pod 수와 무관하게 Envoy 1개) · 원서 1장 Service Mesh Without the Sidecars
#   (p.8 host-level Envoy, p.9 Figure 1-3 The sidecarless service mesh model: 왼쪽 Pod 안 Envoy, 오른쪽 노드 Envoy + Cilium).
# Frontend·Payments·Orders 이름과 "고정 메모리" 는 본문에 없어 뺀다 (2026-11-01 검증).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "CILIUM UP AND RUNNING · 01-01 §4", "서비스 메시 아키텍처: 사이드카 vs 노드 프록시",
      "한 노드의 Pod 마다 Envoy 를 주입하는 사이드카 방식과 노드당 Envoy 하나를 공유하는 Cilium 노드 프록시 방식 비교",
      "eBPF L3/L4 직접 처리 및 노드당 단일 Envoy 공유를 통한 L7 일원화")

W_ZONE = 414
H_ZONE = 344
Y_ZONE = 108

# 좌측 영역: 사이드카 방식 (전통적 서비스 메시)
X_L = 30
d.box(X_L, Y_ZONE, W_ZONE, H_ZONE, PAPER2, RULE, sw=0.9, r=8)
d.box(X_L + 12, Y_ZONE + 12, 184, 24, PAPER, WARN, sw=1.0, r=4)
d.t(X_L + 104, Y_ZONE + 28, "사이드카 모델 (Envoy × Pod 수)", 11, WARN, KR, "middle", 600)
d.t(X_L + W_ZONE - 14, Y_ZONE + 28, "Pod마다 프록시 주입", 11, MUTED, KR, "end")

# 사이드카 Pod 3개
pod_w = 390
pod_h = 74
y_pod_l = [Y_ZONE + 48, Y_ZONE + 132, Y_ZONE + 216]
pod_names_l = ["Pod 1", "Pod 2", "… Pod 50"]

for i, y in enumerate(y_pod_l):
    d.box(X_L + 12, y, pod_w, pod_h, PAPER, RULE, sw=0.8, r=6)
    d.t(X_L + 24, y + 18, pod_names_l[i], 10, SOFT, MONO, "start", 600)

    # 앱 컨테이너
    d.box(X_L + 24, y + 26, 170, 36, PAPER, SOFT, sw=0.9, r=4)
    d.t(X_L + 109, y + 49, "애플리케이션 컨테이너", 11, INK, KR, "middle")

    # 사이드카 Envoy
    d.tone(X_L + 204, y + 26, 186, 36, WARN, r=4, op="18", sw=1.0)
    d.t(X_L + 297, y + 49, "Envoy 사이드카 프록시", 11, WARN, KR, "middle", 600)

d.t(X_L + W_ZONE/2, Y_ZONE + 316, "Pod 50개면 Envoy 50개 · 운영 복잡성", 11, WARN, KR, "middle", 600)


# 우측 영역: 노드 프록시 방식 (Cilium 서비스 메시)
X_R = 476
d.box(X_R, Y_ZONE, W_ZONE, H_ZONE, PAPER2, RULE, sw=0.9, r=8)
d.box(X_R + 12, Y_ZONE + 12, 184, 24, PAPER, OK, sw=1.0, r=4)
d.t(X_R + 104, Y_ZONE + 28, "노드 프록시 모델 (Envoy × 1)", 11, OK, KR, "middle", 600)
d.t(X_R + W_ZONE - 14, Y_ZONE + 28, "사이드카 주입 제거", 11, MUTED, KR, "end")

# 노드 프록시 Pod 3개 (순수 앱)
y_pod_r = [Y_ZONE + 48, Y_ZONE + 118, Y_ZONE + 188]
pod_names_r = ["Pod 1", "Pod 2", "… Pod 50"]

for i, y in enumerate(y_pod_r):
    d.box(X_R + 12, y, pod_w, 60, PAPER, RULE, sw=0.8, r=6)
    d.t(X_R + 24, y + 18, pod_names_r[i], 10, SOFT, MONO, "start", 600)
    d.box(X_R + 24, y + 26, 366, 26, PAPER, SOFT, sw=0.9, r=4)
    d.t(X_R + 207, y + 43, "애플리케이션 컨테이너 (단독)", 11, INK, KR, "middle")

# 노드 공유 계층: eBPF 데이터패스 + 노드 Envoy
d.tone(X_R + 12, Y_ZONE + 258, 200, 48, ACC, r=4, op="18", sw=1.2)
d.t(X_R + 112, Y_ZONE + 278, "eBPF 커널 데이터패스", 11, ACC, KR, "middle", 600)
d.t(X_R + 112, Y_ZONE + 294, "L3/L4 라우팅 · LB · 접근 제어", 11, INK, KR, "middle")

d.tone(X_R + 222, Y_ZONE + 258, 180, 48, OK, r=4, op="18", sw=1.2)
d.t(X_R + 312, Y_ZONE + 278, "호스트 공유 Envoy (1대)", 11, OK, KR, "middle", 600)
d.t(X_R + 312, Y_ZONE + 294, "L7 처리가 필요할 때만", 11, INK, KR, "middle")

d.t(X_R + W_ZONE/2, Y_ZONE + 326, "Pod 수와 무관하게 Envoy 1개", 11, OK, KR, "middle", 600)


# 범례
d.legend(474, [
    ("애플리케이션", SOFT),
    ("주입된 사이드카 (N개)", WARN),
    ("eBPF 데이터패스", ACC),
    ("공유 노드 프록시 (1대)", OK),
])

d.save("01-01.sidecar-vs-node-proxy.svg")
