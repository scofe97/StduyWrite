# 타입 스펙: type-process — 실습 여섯 단계(환경 준비·kind 클러스터·Cilium 설치·예제 앱·정책·Hubble)를 단계마다 실제 명령·리소스 하나로 보인다.
# 사실 출처: cil3.txt 줄 29~1193 (kind.yaml 줄 138, helm install 줄 312, nginx-service 줄 592, ch03-policy 줄 761, hubble-relay 줄 959), docs.cilium.io/en/stable/ (1.20.2).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 296
d = D(W, H, "CILIUM UP AND RUNNING · 03-01", "kind 에서 Hubble 까지 실습 여섯 단계",
      "기본 CNI 를 끈 클러스터에 Cilium 을 올리고, 앱을 띄워 정책과 관측으로 확인한다",
      "단계마다 실제 명령 하나와 확인 값 하나")

Y_TOP, H_CARD, W_CARD, GAP, X0 = 104, 160, 132, 16, 24
steps = [
    ("01", "환경 준비", "도구 네 개", "kind · helm", "cilium · hubble", INFO),
    ("02", "kind 클러스터", "기본 CNI 끔", "kind.yaml", "NotReady ×3", WARN),
    ("03", "Cilium 설치", "Helm 으로 올림", "helm install", "cilium 1.20.2", OK),
    ("04", "예제 앱", "서비스·클라이언트", "nginx-service", "10.96.242.74", INFO),
    ("05", "정책", "라벨·경로 허용", "ch03-policy", "403 · timeout", ACC),
    ("06", "Hubble 관측", "흐름 확인", "hubble observe", "Relay :4245", OK),
]
for i, (num, title, sub, c1, c2, col) in enumerate(steps):
    x = X0 + i * (W_CARD + GAP)
    cx = x + W_CARD / 2
    if col == ACC:
        d.tone(x, Y_TOP, W_CARD, H_CARD, ACC, r=6, op="12", sw=1.4)
    else:
        d.box(x, Y_TOP, W_CARD, H_CARD, PAPER2, RULE, sw=0.9, r=6)
    d.chip(x + 28, Y_TOP + 20, num, col, size=10)
    d.t(cx, Y_TOP + 56, title, 13, INK, KR, "middle", 600)
    d.t(cx, Y_TOP + 76, sub, 12, MUTED, KR, "middle")
    d.line(x + 12, Y_TOP + 92, x + W_CARD - 12, Y_TOP + 92, RULE, 0.6)
    d.box(x + 8, Y_TOP + 104, W_CARD - 16, 44, PAPER, RULE, sw=0.7, r=4)
    d.t(cx, Y_TOP + 122, c1, 11, col, MONO, "middle", 600)
    d.t(cx, Y_TOP + 140, c2, 11, MUTED, MONO, "middle")
    if i < len(steps) - 1:
        ax = x + W_CARD
        d.arrow([(ax + 2, Y_TOP + 80), (ax + GAP - 2, Y_TOP + 80)], MUTED, "ar", 1.2)

d.save("03-01.chapter-overview.svg")
