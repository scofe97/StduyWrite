# 타입 스펙: type-process
# 02-01.chapter-overview — 2장 배포 모델 전체 지도
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, KR, MONO

W, H = 1000, 392
X0, GAP, CARD_Y, CARD_H = 12, 26, 132, 196
CARD_W = (W - 48 - X0 - GAP * 3) / 4

d = D(W, H, "CHAPTER MAP · 02-01",
      "쿠버네티스 배포 모델과 고가용성 인프라 전체 지도",
      "02-01편의 전체 구조. 배포 모델 선택에서 출발해 아키텍처 토폴로지 설계, "
      "머신 부트스트랩과 업그레이드, 그리고 API 서버 단일 주소 고가용성 보강까지의 흐름.",
      lead="배포 전략 선택 → 아키텍처 토폴로지 → 머신과 수명주기 → 고가용성 보강")

CARDS = [
    ("§1·2", "배포 전략", "자체 구축과 도구 선택", INFO,
     ["· 매니지드 대 직접 구축", "· 엔지니어링 비용 저울질", "· 기성 도구와 맞춤 자동화"]),
    ("§3·4", "인프라 토폴로지", "가용성과 네트워크 경계", INFO,
     ["· etcd 배치와 노드 풀", "· 컨트롤 플레인 장애 격리", "· API 와 인그레스 LB 분리"]),
    ("§5·6", "머신과 수명주기", "부트스트랩과 업그레이드", INFO,
     ["· 불변 머신 이미지", "· kubelet 과 정적 파드", "· 세 가지 업그레이드 전략"]),
    ("§7",   "보강 · 고가용성", "주소 한 칸과 세 해결", OK,
     ["· 단일 주소 한계 극복", "· 외부 LB · VIP · 노드 로컬 프록시", "· 파드 전용 통신 경로"]),
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
    if i < len(CARDS) - 1:
        d.path(f"M {x+CARD_W+3} {CARD_Y+CARD_H/2} L {x+CARD_W+GAP-4} {CARD_Y+CARD_H/2}",
               MUTED, 1.6, m="ar")

d.legend(352, [("원서 배포 아키텍처", INFO), ("책 밖 고가용성 보강", OK)])
d.save("02-01.chapter-overview.svg")
print("ok 02-01.chapter-overview")
