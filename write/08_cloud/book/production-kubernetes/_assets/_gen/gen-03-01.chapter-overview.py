# 타입 스펙: type-process
# 03-01.chapter-overview — Pod 하나가 컨테이너로 뜨기까지 kubelet 에서 커널로 내려가는 네 단계
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd import D, INK, MUTED, SOFT, ACC, INFO, OK, KR, MONO

W, H = 1000, 408
X0, CARD_W, GAP = 12, 164, 98
CARD_Y, CARD_H = 112, 188

d = D(W, H, "CHAPTER MAP · 03-01",
      "Pod 하나가 컨테이너로 뜨기까지",
      "kubelet 의 요청이 CRI 와 OCI 를 건너 커널까지 내려가는 네 단계와 각 단계를 맡은 절",
      lead="kubelet → 고수준 런타임 → OCI 런타임 → 리눅스 커널")

CARDS = [
    ("STEP 1", "kubelet", "Pod 를 받아 CRI 로 요청", INFO,
     ["CRI gRPC", "RuntimeService", "ImageService"], "§3"),
    ("STEP 2", "고수준 런타임", "이미지 pull · 컨테이너 구성", ACC,
     ["containerd · CRI-O", "OCI 이미지 명세"], "§2 · §3 · §4"),
    ("STEP 3", "OCI 런타임", "번들로 프로세스 생성", INFO,
     ["runc", "OCI 런타임 명세"], "§2"),
    ("STEP 4", "리눅스 커널", "자원 제한 · 시야 격리", OK,
     ["cgroup", "네임스페이스"], "§1"),
]
EDGES = ["CRI", "OCI 번들", "시스템 콜"]

for i, (step, title, sub, c, bullets, sec) in enumerate(CARDS):
    x = X0 + (CARD_W + GAP) * i
    cx = x + CARD_W / 2
    d.t(cx, CARD_Y - 12, step, 9, SOFT, MONO)
    d.tone(x, CARD_Y, CARD_W, CARD_H, c, 6, "10", 1.4)
    d.t(cx, CARD_Y + 34, title, 14, c, KR, "middle", 600)
    d.line(x + 16, CARD_Y + 50, x + CARD_W - 16, CARD_Y + 50, f"{c}44", 0.9)
    d.t(cx, CARD_Y + 76, sub, 12, INK)
    for j, b in enumerate(bullets):
        d.t(cx, CARD_Y + 112 + j * 24, b, 12, MUTED)
    d.chip(cx, CARD_Y + CARD_H + 28, sec, MUTED, 12)
    if i < len(CARDS) - 1:
        ay = CARD_Y + CARD_H / 2
        d.arrow([(x + CARD_W + 4, ay), (x + CARD_W + GAP - 6, ay)], MUTED, "ar", 1.6)
        d.chip(x + CARD_W + GAP / 2, ay - 22, EDGES[i], MUTED, 12)

d.legend(368, [("호출이 내려가는 층", INFO), ("플랫폼 팀이 고르는 층", ACC), ("커널이 하는 일", OK)])
d.save(str(Path(__file__).resolve().parent.parent / "03-01.chapter-overview.svg"))
print("ok 03-01.chapter-overview")
