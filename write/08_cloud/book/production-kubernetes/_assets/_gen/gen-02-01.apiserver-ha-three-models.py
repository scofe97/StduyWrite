# 타입 스펙: type-process
# 02-01.apiserver-ha-three-models — API 서버 단일 주소 고가용성 세 모델 비교
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, KR, MONO

W, H = 1000, 420
X0, GAP, CARD_Y, CARD_H = 16, 28, 132, 224
CARD_W = (W - 32 - X0 - GAP * 2) / 3

d = D(W, H, "HA COMPARISON · 02-01",
      "API 서버 고가용성을 위한 세 가지 해결: 외부 LB · VIP · 노드 로컬 프록시",
      "kubeconfig server 필드의 단일 주소 제약을 푸는 세 가지 해결. "
      "외부 전용 L4 LB, 컨트롤 플레인 VIP+keepalived, 워커 노드 로컬 프록시를 "
      "두는 위치와 운영 트레이드오프 비교.",
      lead="단일 주소 제약 → 장치를 어디에 두느냐에 따른 세 가지 해결")

CARDS = [
    ("해결 A", "노드 밖 외부 L4 LB", "단일 인프라 집중형", INFO,
     ["· 배치: 클러스터 외부 전용 LB 머신",
      "· 분산: HAProxy L4 TCP 패스스루",
      "· 강점: 단순한 구조와 명확한 관리 경계",
      "· 약점: 외부 LB 자체가 단일 장애점(SPOF)",
      "· 특징: 마스터 내부 kubectl 도 영향"]),
    ("해결 B", "VIP + keepalived", "가상 IP 페일오버형", OK,
     ["· 배치: 컨트롤 플레인 노드 3대",
      "· 분산: VRRP 선출 마스터의 HAProxy",
      "· 강점: 전용 LB 없이 단일 장애점 제거",
      "· 약점: keepalived·VRRP 운영 복잡성",
      "· 채택: kubeadm HA 문서 예시 · OpenShift 온프레미스"]),
    ("해결 C", "노드 로컬 프록시", "워커 분산 프록시형", INFO,
     ["· 배치: 각 워커 노드 localhost:6443",
      "· 분산: 워커마다 nginx 로컬 프록시",
      "· 강점: 외부 LB 인프라 없이 노드별 분산",
      "· 약점: 클러스터 외부 kubectl 직접 접근 불가",
      "· 채택: Kubespray 기본값 (사람용 진입점 분리)"]),
]

for i, (tag, title, sub, c, bullets) in enumerate(CARDS):
    x = X0 + (CARD_W + GAP) * i
    cx = x + CARD_W / 2
    d.t(cx, 118, tag, 9, SOFT, MONO)
    d.tone(x, CARD_Y, CARD_W, CARD_H, c, 6, "10", 1.4)
    d.t(cx, 166, title, 14, c, KR, "middle", 600)
    d.line(x + 18, 182, x + CARD_W - 18, 182, f"{c}44", 0.9)
    d.t(cx, 206, sub, 11, INK)
    for j, b in enumerate(bullets):
        d.t(x + 18, 236 + j * 24, b, 11, MUTED, KR, "start")

d.legend(380, [("외부 / 로컬 프록시 모델", INFO), ("VIP 페일오버 모델", OK)])
d.save("02-01.apiserver-ha-three-models.svg")
print("ok 02-01.apiserver-ha-three-models")
