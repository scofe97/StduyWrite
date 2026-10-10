# 타입 스펙: type-deployment — 노드 내 Pod 3개 기준 사이드카 메시와 노드 프록시 메시 배치 비교.
# 사실 출처: Cilium Up and Running 1장 Service Mesh Without the Sidecars (§Figure 1-3).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "CILIUM UP AND RUNNING · 01-01 §4", "서비스 메시 아키텍처: 사이드카 vs 노드 프록시",
      "노드 내 Pod 3개 배포 시 사이드카 주입 방식의 자원 중복과 Cilium 노드 프록시 일원화 비교",
      "eBPF 가 L3/L4 를 직접 처리하고 L7 프록시를 노드당 하나로 공유합니다")

W_ZONE = 414
H_ZONE = 344
Y_ZONE = 108

# 좌측 영역: 사이드카 방식 (전통적 서비스 메시)
X_L = 30
d.box(X_L, Y_ZONE, W_ZONE, H_ZONE, PAPER2, RULE, sw=0.9, r=8)
d.box(X_L + 12, Y_ZONE + 12, 184, 24, PAPER, WARN, sw=1.0, r=4)
d.t(X_L + 104, Y_ZONE + 28, "사이드카 모델 (Envoy × 3)", 11, WARN, KR, "middle", 600)
d.t(X_L + W_ZONE - 14, Y_ZONE + 28, "Pod마다 프록시 주입", 11, MUTED, KR, "end")

# 사이드카 Pod 3개
pod_w = 390
pod_h = 74
y_pod_l = [Y_ZONE + 48, Y_ZONE + 132, Y_ZONE + 216]
pod_names_l = ["Pod 1 (Frontend)", "Pod 2 (Payments)", "Pod 3 (Orders)"]

for i, y in enumerate(y_pod_l):
    d.box(X_L + 12, y, pod_w, pod_h, PAPER, RULE, sw=0.8, r=6)
    d.t(X_L + 24, y + 18, pod_names_l[i], 10, SOFT, MONO, "start", 600)

    # 앱 컨테이너
    d.box(X_L + 24, y + 26, 170, 36, PAPER2, RULE, sw=0.8, r=4)
    d.t(X_L + 109, y + 49, "애플리케이션 컨테이너", 11, INK, KR, "middle")

    # 사이드카 Envoy
    d.tone(X_L + 204, y + 26, 186, 36, WARN, r=4, op="18", sw=1.0)
    d.t(X_L + 297, y + 49, "Envoy 사이드카 프록시", 11, WARN, KR, "middle", 600)

d.t(X_L + W_ZONE/2, Y_ZONE + 316, "프록시 자원 N배 복제 · 운영 복잡성 증가", 11, WARN, KR, "middle", 600)


# 우측 영역: 노드 프록시 방식 (Cilium 서비스 메시)
X_R = 476
d.box(X_R, Y_ZONE, W_ZONE, H_ZONE, PAPER2, RULE, sw=0.9, r=8)
d.box(X_R + 12, Y_ZONE + 12, 184, 24, PAPER, OK, sw=1.0, r=4)
d.t(X_R + 104, Y_ZONE + 28, "노드 프록시 모델 (Envoy × 1)", 11, OK, KR, "middle", 600)
d.t(X_R + W_ZONE - 14, Y_ZONE + 28, "사이드카 주입 제거", 11, MUTED, KR, "end")

# 노드 프록시 Pod 3개 (순수 앱)
y_pod_r = [Y_ZONE + 48, Y_ZONE + 118, Y_ZONE + 188]
pod_names_r = ["Pod 1 (Frontend)", "Pod 2 (Payments)", "Pod 3 (Orders)"]

for i, y in enumerate(y_pod_r):
    d.box(X_R + 12, y, pod_w, 60, PAPER, RULE, sw=0.8, r=6)
    d.t(X_R + 24, y + 18, pod_names_r[i], 10, SOFT, MONO, "start", 600)
    d.box(X_R + 24, y + 26, 366, 26, PAPER2, RULE, sw=0.8, r=4)
    d.t(X_R + 207, y + 43, "애플리케이션 컨테이너 (단독)", 11, INK, KR, "middle")

# 노드 공유 계층: eBPF 데이터패스 + 노드 Envoy
d.tone(X_R + 12, Y_ZONE + 258, 200, 48, ACC, r=4, op="18", sw=1.2)
d.t(X_R + 112, Y_ZONE + 278, "eBPF 커널 데이터패스", 11, ACC, KR, "middle", 600)
d.t(X_R + 112, Y_ZONE + 294, "L3/L4 포워딩 · 커널 처리", 11, INK, KR, "middle")

d.tone(X_R + 222, Y_ZONE + 258, 180, 48, OK, r=4, op="18", sw=1.2)
d.t(X_R + 312, Y_ZONE + 278, "호스트 공유 Envoy (1대)", 11, OK, KR, "middle", 600)
d.t(X_R + 312, Y_ZONE + 294, "L7 정책 처리 시에만 위임", 11, INK, KR, "middle")

d.t(X_R + W_ZONE/2, Y_ZONE + 326, "노드당 고정 메모리 · 커널 레벨 패킷 처리", 11, OK, KR, "middle", 600)


# 범례
d.legend(474, [
    ("애플리케이션", INK),
    ("주입된 사이드카 (N개)", WARN),
    ("eBPF 데이터패스", ACC),
    ("공유 노드 프록시 (1대)", OK),
])

d.save("01-01.sidecar-vs-node-proxy.svg")
