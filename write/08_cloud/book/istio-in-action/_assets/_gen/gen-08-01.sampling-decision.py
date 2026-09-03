# 08-01 §5 요청 하나가 추적될지 정해지는 순서.
# 저자는 세 규칙을 서로 다른 자리에 적었다. 헤더가 있으면 진행 중 트레이스로 본다(8.2.1),
# sampling 비율로 수집 빈도를 정한다(8.2.5), x-envoy-force-trace 는 그 요청을 무조건 잡는다(8.2.5).
# 이 도식은 그 셋을 요청 하나의 관점으로 이은 것이다. 저자가 이 순서를 한 줄로 적은 곳은 없다.
# 강제 추적 마름모의 "내부 요청" 조건은 저자가 아니라 Envoy 공식 문서에서 왔다(적대적 검증 2026-08-31 지적).
# 타입 스펙: type-flowchart — 판단 논리. 타원(시작·끝) · 마름모(판단, ≤3 출구) · 사각형(행동) ·
#           합류점은 작은 점. 예는 오른쪽, 아니오는 아래, 모든 갈래에 라벨, accent 는 갈래 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 912
d = D(W, H, "ISTIO IN ACTION · 08-01 §5",
      "이 요청이 추적될지 정해지는 순서",
      "저자가 세 자리에 나눠 적은 규칙을 요청 하나의 관점으로 이었다. 색이 붙은 갈래가 샘플링을 낮게 "
      "두고도 원하는 요청만 붙잡는 손잡이다. 저자가 이 순서를 한 줄로 적은 곳은 없다.",
      "demo 프로파일은 100% 입니다 — 운영에 그대로 두면 안 되는 값입니다")

def oval(x, y, w, h, label):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 20)
    d.t(x + w / 2, y + h / 2 + 5, label, 13, INK, KR, "middle", 600)

def step(x, y, w, h, label, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + h / 2 + 5, label, 13, ACC if focal else INK, KR, "middle", 600)

def diamond(cx, cy, l1, l2):
    d.o.append(f'<path d="M {cx-150} {cy} L {cx} {cy-52} L {cx+150} {cy} L {cx} {cy+52} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(cx, cy - 4, l1, 12, INK, KR, "middle", 600)
    d.t(cx, cy + 16, l2, 12, INK, KR, "middle", 600)

CA, CB = 360, 830

oval(CA - 130, 116, 260, 44, "요청이 프록시에 닿는다")
diamond(CA, 240, "추적 헤더가", "이미 붙어 있나")
step(CB - 150, 212, 300, 56, "진행 중 트레이스로 본다")
step(CA - 150, 320, 300, 56, "새 트레이스를 시작한다")
d.o.append(f'<circle cx="{CA}" cy="402" r="4" fill="{MUTED}"/>')
diamond(CA, 496, "x-envoy-force-trace 가", "내부 요청에 실렸나")
step(CB - 150, 468, 300, 56, "무조건 수집한다", focal=True)
diamond(CA, 656, "sampling 비율", "안에 드나")
oval(CB - 140, 634, 280, 44, "스팬을 보낸다")
oval(CA - 110, 768, 220, 44, "버린다")

d.arrow([(CA, 160), (CA, 186)], MUTED, "ar", 1.4)
d.arrow([(CA, 292), (CA, 318)], MUTED, "ar", 1.4)
d.arrow([(CA, 376), (CA, 396)], MUTED, "ar", 1.4)
d.arrow([(CA, 408), (CA, 442)], MUTED, "ar", 1.4)
d.arrow([(CA, 548), (CA, 602)], MUTED, "ar", 1.4)
d.arrow([(CA, 708), (CA, 766)], MUTED, "ar", 1.4)
d.arrow([(CA + 150, 240), (CB - 152, 240)], MUTED, "ar", 1.4)
d.arrow([(CA + 150, 496), (CB - 152, 496)], ACC, "acc", 1.5)
d.arrow([(CA + 150, 656), (CB - 142, 656)], MUTED, "ar", 1.4)
d.path(f"M {CB} 268 L {CB} 402 L {CA + 12} 402", MUTED, 1.2, m="ar")
d.path(f"M {CB} 524 L {CB} 630", ACC, 1.4, m="acc")

d.t((CA + CB) / 2, 228, "예", 12, MUTED, KR, "middle", 600)
d.t((CA + CB) / 2, 484, "예", 12, ACC, KR, "middle", 600)
d.t((CA + CB) / 2, 644, "예", 12, MUTED, KR, "middle", 600)
d.t(CA + 22, 308, "아니오", 12, MUTED, KR, "start", 600)
d.t(CA + 22, 578, "아니오", 12, MUTED, KR, "start", 600)
d.t(CA + 22, 740, "아니오", 12, MUTED, KR, "start", 600)

d.t(32, 836, "\"내부 요청\" 조건은 저자가 아니라 Envoy 공식 문서에서 왔다 — 저자는 이 전제를 적지 않는다", 11, SOFT, KR, "start")
d.legend(856, [("낮은 샘플링에서도 붙잡는 갈래", ACC)])
d.save("08-01.sampling-decision.svg")
