# 11-01 §5 포화가 어느 방향의 트래픽과 함께 오르는가가 처방을 가른다.
# 본문(원문 11.2.1): "When incoming traffic causes saturation, the performance bottleneck is due to the
#       rate of changes, and the resolution is to increase the batching of events or scale up. If saturation
#       correlates with outgoing traffic, the resolution is to scale out the control plane so that each pilot
#       has fewer instances to manage, and to define Sidecar resources for every workload."
#       그리고 11.4 — 포화가 아닌데 지연만 오르면 자원이 최적으로 쓰이지 않는 것이므로 동시 푸시 수를 올린다.
# 타입 스펙: type-flowchart — 판단 논리. 타원(시작·끝) · 마름모(판단, 출구 둘) · 사각형(행동).
#           예는 오른쪽, 아니오는 아래, 모든 갈래에 라벨, accent 는 갈래 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 888
d = D(W, H, "ISTIO IN ACTION · 11-01 §5",
      "포화가 어느 쪽과 함께 오르는가가 처방을 가른다",
      "CPU 포화만 보면 무엇을 해야 할지 정해지지 않는다. 들어오는 트래픽과 나가는 트래픽 중 어느 쪽과 "
      "함께 오르는지가 처방을 가른다. 색이 붙은 갈래가 저자가 첫 손잡이로 지목한 쪽이다.",
      "포화가 아닌데 지연만 오르면 자원이 남는다는 뜻입니다")

def oval(x, y, w, h, label, sub=None):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 22)
    if sub:
        d.t(x + w / 2, y + h / 2 - 2, label, 13, INK, KR, "middle", 600)
        d.t(x + w / 2, y + h / 2 + 18, sub, 9, MUTED, MONO)
    else:
        d.t(x + w / 2, y + h / 2 + 5, label, 13, INK, KR, "middle", 600)

def step(x, y, w, h, label, sub, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 26, label, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 46, sub, 11, MUTED, KR, "middle")

def diamond(cx, cy, l1, l2, focal=False):
    c = ACC if focal else RULE
    d.o.append(f'<path d="M {cx-170} {cy} L {cx} {cy-56} L {cx+170} {cy} L {cx} {cy+56} Z" '
               f'fill="{ACC + "0C" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1}"/>')
    d.t(cx, cy - 4, l1, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, cy + 16, l2, 12, ACC if focal else INK, KR, "middle", 600)

CA, CB = 330, 860

oval(CA - 180, 112, 300, 56, "지연이 늘었다", "proxy convergence time")
diamond(CA, 268, "CPU 사용률이", "90% 를 넘나")
step(CB - 180, 236, 300, 68, "동시 푸시 수를 올린다", "자원이 남는데 안 쓰고 있다")
diamond(CA, 440, "들어오는 트래픽과", "함께 오르나")
step(CB - 180, 408, 300, 68, "배칭을 늘리거나 수직 확장", "설정 생성이 병목이다")
diamond(CA, 612, "나가는 트래픽과", "함께 오르나", focal=True)
step(CB - 180, 580, 300, 68, "Sidecar 정의 + 수평 확장", "배포 대상과 크기가 병목이다", focal=True)
oval(CA - 180, 712, 300, 56, "플랫폼 쪽을 의심한다", "API 서버 · 연결")

d.arrow([(CA, 168), (CA, 208)], MUTED, "ar", 1.4)
d.arrow([(CA + 170, 268), (CB - 182, 268)], MUTED, "ar", 1.4)
d.arrow([(CA, 324), (CA, 380)], MUTED, "ar", 1.4)
d.arrow([(CA + 170, 440), (CB - 182, 440)], MUTED, "ar", 1.4)
d.arrow([(CA, 496), (CA, 552)], MUTED, "ar", 1.4)
d.arrow([(CA + 170, 612), (CB - 182, 612)], ACC, "acc", 1.5)
d.arrow([(CA, 668), (CA, 708)], MUTED, "ar", 1.4)

d.t((CA + CB) / 2, 254, "아니오", 12, MUTED, KR, "middle", 600)
d.t((CA + CB) / 2, 426, "예", 12, MUTED, KR, "middle", 600)
d.t((CA + CB) / 2, 598, "예", 12, ACC, KR, "middle", 600)
d.t(CA + 24, 356, "예", 12, MUTED, KR, "start", 600)
d.t(CA + 24, 528, "아니오", 12, MUTED, KR, "start", 600)
d.t(CA + 24, 694, "아니오", 12, MUTED, KR, "start", 600)

d.t(28, 804, "저자의 우선순위 — 자원을 늘리는 것은 Sidecar 와 발견 범위와 배칭을 다 손본 뒤의 마지막 수단이다", 11, SOFT, KR, "start")
d.legend(828, [("Sidecar 가 먼저 오는 갈래", ACC), ("나머지 갈래", MUTED)])
d.save("11-01.traffic-direction.svg")
