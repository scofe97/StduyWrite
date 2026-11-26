# 01-02 §1 — Git 저장소에서 Argo CD(sync)와 Rollout CR 을 거쳐 Argo Rollouts 가 ReplicaSet·Service·Ingress·Istio 가중치를 제어하는 역할 경계.
# 본문 근거: 01-02 §1 「Git 동기화와 점진적 배포의 분리」.
# 공식 근거: argo-rollouts v1.10.2 docs/architecture.md, docs/features/traffic-management/index.md, docs/FAQ.md.
# 타입 스펙: type-architecture — 좌측 Git→Argo CD→Rollout CR 선언 동기화, 우측 Ingress·Istio→Service→ReplicaSet 트래픽 흐름, 상단 컨트롤러의 하단 자원 제어를 한 장에 보인다.
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 960, 476
d = D(
    W,
    H,
    "GITOPS · 01-02",
    "Argo CD 와 Argo Rollouts 의 자원 소유 경계",
    "Git 저장소의 Rollout v2 선언을 Argo CD 가 클러스터의 Rollout CR 로 동기화한다. "
    "Argo Rollouts 컨트롤러는 Rollout CR 을 감시하며 stable 과 canary ReplicaSet 스케일, "
    "stable 과 canary Service 의 selector, 그리고 Ingress 또는 Istio 의 trafficRouting 가중치 90 대 10 을 각각 변경한다. "
    "실트래픽은 Ingress 또는 Istio 에서 90% 와 10% 로 나뉘어 각 Service 를 거쳐 stable 과 canary ReplicaSet 으로 흐른다.",
    "Argo CD 는 Git 선언을 Rollout CR 에 동기화하고, Argo Rollouts 는 클러스터 안의 트래픽과 파드를 전환합니다",
)

# ── 1. 구역 (Zones) ──────────────────────────────────────────────────────
# Zone 1: 클러스터 제어 평면 (상단 컨트롤러 2종)
d.o.append(
    f'<rect x="184" y="92" width="540" height="104" rx="8" fill="{PAPER2}" '
    f'stroke="{RULE}" stroke-width="0.9" stroke-dasharray="5 4"/>'
)
d.t(196, 108, "CONTROL PLANE", 9, SOFT, MONO, "start", 600)

# Zone 2: 클러스터 워크로드·트래픽 자원 (하단)
d.o.append(
    f'<rect x="184" y="232" width="756" height="168" rx="8" fill="{PAPER2}" '
    f'stroke="{RULE}" stroke-width="0.9" stroke-dasharray="5 4"/>'
)
d.t(196, 248, "CLUSTER RESOURCES", 9, SOFT, MONO, "start", 600)

# ── 2. 연결선 (Connectors) — z-order 상 박스보다 먼저 그린다 ────────────
# (a) Git 저장소 -> Argo CD (수평)
d.arrow([(152, 152), (196, 152)], c=INFO, m="info", sw=1.4)
d.t(174, 142, "감지", 13, INFO, KR, "middle", 600)

# (b) Argo CD -> Rollout CR (수직)
d.arrow([(272, 184), (272, 276)], c=INFO, m="info", sw=1.4)
d.chip(272, 214, "sync", INFO, size=11)

# (c) Rollout CR -> Argo Rollouts (직각 우회: 오른쪽 상단 포트 -> 위로 -> 왼쪽 면)
d.arrow([(348, 286), (368, 286), (368, 152), (436, 152)], c=MUTED, m="ar", sw=1.2, dash="4 3")
d.t(376, 218, "감시", 13, MUTED, KR, "start", 600)

# (d) Rollout CR -> stable / canary ReplicaSet (소유 관계, 분리된 포트에서 출발)
d.arrow([(348, 304), (384, 304), (384, 286), (404, 286)], c=MUTED, m="ar", sw=1.2)
d.arrow([(348, 328), (384, 328), (384, 358), (404, 358)], c=MUTED, m="ar", sw=1.2)

# (e) Argo Rollouts -> ReplicaSet 제어 (수직)
d.arrow([(476, 184), (476, 256)], c=ACC, m="acc", sw=1.4)
d.t(468, 218, "스케일", 13, ACC, KR, "end", 600)

# (f) Argo Rollouts -> Service selector 제어 (수직)
d.arrow([(668, 184), (668, 256)], c=ACC, m="acc", sw=1.4)
d.t(676, 218, "selector", 11, ACC, MONO, "start", 600)

# (g) Argo Rollouts -> Ingress · Istio (오른쪽 -> 아래로, 직각 L자)
d.arrow([(708, 152), (868, 152), (868, 276)], c=ACC, m="acc", sw=1.4)
d.t(792, 142, "trafficRouting", 11, ACC, MONO, "middle", 600)

# (h) Service -> ReplicaSet (트래픽 전달)
d.arrow([(596, 286), (556, 286)], c=OK, m="ok", sw=1.4)
d.arrow([(596, 358), (556, 358)], c=WARN, m="warn", sw=1.4)

# (i) Ingress · Istio -> Service (가중치 90 / 10 트래픽 분배)
d.arrow([(800, 286), (740, 286)], c=OK, m="ok", sw=1.4)
d.t(770, 276, "90%", 12, OK, MONO, "middle", 600)

d.arrow([(800, 358), (740, 358)], c=WARN, m="warn", sw=1.4)
d.t(770, 348, "10%", 12, WARN, MONO, "middle", 600)

# ── 3. 컴포넌트 노드 (Components) ────────────────────────────────────────
# Git 저장소 (외부)
d.box(24, 120, 128, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(88, 146, "Git 저장소", 14, INK, KR, "middle", 600)
d.t(88, 168, "Rollout v2", 11, MUTED, MONO, "middle")

# Argo CD (INFO)
d.tone(196, 120, 152, 64, INFO, r=6, op="14", sw=1.2)
d.t(272, 146, "Argo CD", 14, INFO, MONO, "middle", 600)
d.t(272, 168, "선언 동기화", 13, MUTED, KR, "middle")

# Argo Rollouts (ACC focal 1곳)
d.tone(436, 120, 272, 64, ACC, r=6, op="12", sw=1.4)
d.t(572, 146, "Argo Rollouts", 14, ACC, MONO, "middle", 600)
d.t(572, 168, "점진적 배포 컨트롤러", 13, MUTED, KR, "middle")

# Rollout CR
d.tone(196, 276, 152, 68, INFO, r=6, op="10", sw=1.1)
d.t(272, 302, "Rollout CR", 14, INK, MONO, "middle", 600)
d.t(272, 324, "setWeight: 10", 11, INFO, MONO, "middle")

# stable ReplicaSet (OK)
d.tone(404, 256, 152, 60, OK, r=6, op="12", sw=1.1)
d.t(480, 280, "stable ReplicaSet", 12, OK, MONO, "middle", 600)
d.t(480, 302, "v1 · 100% 유지", 13, MUTED, KR, "middle")

# canary ReplicaSet (WARN)
d.tone(404, 328, 152, 60, WARN, r=6, op="12", sw=1.1)
d.t(480, 352, "canary ReplicaSet", 12, WARN, MONO, "middle", 600)
d.t(480, 374, "v2 · 10% 스케일", 13, MUTED, KR, "middle")

# stable Service (OK)
d.tone(596, 256, 144, 60, OK, r=6, op="10", sw=1.1)
d.t(668, 280, "stable Service", 12, OK, MONO, "middle", 600)
d.t(668, 302, "hash: v1", 11, MUTED, MONO, "middle")

# canary Service (WARN)
d.tone(596, 328, 144, 60, WARN, r=6, op="10", sw=1.1)
d.t(668, 352, "canary Service", 12, WARN, MONO, "middle", 600)
d.t(668, 374, "hash: v2", 11, MUTED, MONO, "middle")

# Ingress · Istio
d.box(800, 276, 132, 92, fill=PAPER, stroke=RULE, sw=1.1, r=6)
d.t(866, 304, "Ingress · Istio", 13, INK, MONO, "middle", 600)
d.t(866, 326, "trafficRouting", 11, ACC, MONO, "middle")
d.t(866, 348, "가중치 90 / 10", 13, MUTED, KR, "middle")

# ── 4. 범례 ────────────────────────────────────────────────────────────
d.legend(
    420,
    [
        ("Argo CD 동기화", INFO),
        ("Rollouts 제어", ACC),
        ("stable 90%", OK),
        ("canary 10%", WARN),
    ],
)

out_path = (
    sys.argv[1]
    if len(sys.argv) > 1
    else str(pathlib.Path(__file__).resolve().parent.parent / "01-02.argocd-rollouts-ownership.svg")
)
d.save(out_path)
print("ok 01-02.argocd-rollouts-ownership.svg")
