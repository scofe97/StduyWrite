# 07-01 §6 차원 조합 하나가 시계열 한 줄이 되는 판단.
# 본문: "차원이 하나라도 다르면 같은 메트릭이 새 줄로 갈립니다." 원문의 200 → 5 · 500 → 3 두 줄이 그 결과다.
# 타입 스펙: type-flowchart — 판단과 두 갈래가 논점이다. 시작·끝은 타원, 단계는 사각, 판단은 마름모,
#           예는 오른쪽 아니오는 아래, 모든 갈래에 라벨, accent 는 가장 결과가 큰 갈래 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1040, 688
d = D(W, H, "ISTIO IN ACTION · 07-01 §6",
      "차원 조합 하나가 시계열 한 줄이 된다",
      "속성 값이 차원을 채우고, 그 조합이 이미 있는 줄과 같은지에 따라 값이 오르거나 줄이 하나 늘어난다. "
      "색이 붙은 갈래가 카디널리티를 키우는 쪽이다.",
      "차원을 더하기 전에 그 차원이 가질 수 있는 값의 개수를 셉니다")

def oval(x, y, w, h, label, sub=None):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 20)
    d.t(x + w / 2, y + (h / 2 + 5 if not sub else 24), label, 13, INK, KR, "middle", 600)
    if sub: d.t(x + w / 2, y + 42, sub, 9, MUTED, MONO)

def step(x, y, w, h, label, sub=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    col = ACC if focal else INK
    d.t(x + w / 2, y + (h / 2 + 5 if not sub else 26), label, 13, col, KR, "middle", 600)
    if sub: d.t(x + w / 2, y + 46, sub, 9, MUTED, MONO)

# 시작
oval(250, 96, 240, 44, "요청이 프록시를 지난다")
# 단계 둘
step(230, 168, 280, 60, "Envoy 속성을 읽는다", "request.method · response.code")
step(230, 256, 280, 60, "차원 값을 채운다", "reporter · source_workload …")
# 판단 — 마름모
d.o.append(f'<path d="M 220 380 L 370 328 L 520 380 L 370 432 Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(370, 376, "이 차원 조합의", 12, INK, KR, "middle", 600)
d.t(370, 396, "줄이 이미 있나", 12, INK, KR, "middle", 600)
# 갈래
step(700, 352, 280, 56, "그 줄의 값을 +1")
step(230, 464, 280, 60, "새 줄을 만든다", "시계열이 하나 늘어난다", focal=True)
# 끝
oval(620, 568, 380, 44, "노출되는 시계열")

d.arrow([(370, 140), (370, 166)], MUTED, "ar", 1.4)
d.arrow([(370, 228), (370, 254)], MUTED, "ar", 1.4)
d.arrow([(370, 316), (370, 326)], MUTED, "ar", 1.4)
d.arrow([(520, 380), (698, 380)], MUTED, "ar", 1.4)
d.t(600, 368, "예", 12, MUTED, KR, "middle", 600)
d.arrow([(370, 432), (370, 462)], ACC, "acc", 1.5)
d.t(392, 452, "아니오", 12, ACC, KR, "start", 600)
d.path("M 840 408 L 840 566", MUTED, 1.2, m="ar")
d.path("M 370 524 L 370 590 L 618 590", ACC, 1.4, m="acc")

d.t(560, 452, "두 줄에서 다른 것은 response_code 하나", 11, SOFT, KR, "start")
d.t(560, 476, 'istio_requests_total{ … response_code="200" … } 5', 11, MUTED, MONO, "start")
d.t(560, 498, 'istio_requests_total{ … response_code="500" … } 3', 11, MUTED, MONO, "start")

d.legend(644, [("카디널리티를 키우는 갈래", ACC)])
d.save("07-01.dimension-split.svg")
