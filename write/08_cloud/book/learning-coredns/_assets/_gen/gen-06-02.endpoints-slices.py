# 06-02 §3 — 파드 하나가 바뀔 때 다시 보내는 주소 수를 Endpoints 와 EndpointSlice 로 비교한다.
# 소스 근거: Kubernetes 문서 endpoint-slices.md — "no more than 100 endpoints each"(조각당 기본 100),
#            service.md Over-capacity endpoints — "over 1000 backing endpoints ... truncates the data in the Endpoints object".
#            본문 근거: 이 노트 §3 — Endpoints 는 바뀔 때마다 객체 전체를 보낸다, EndpointSlice 는 바뀐 조각만.
#            백엔드 300·3000 은 설명용 예시 수다.
# 타입 스펙: type-bar — 막대 길이가 곧 한 번에 다시 보내는 주소 수다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 06-02 §3",
      "파드 하나가 바뀔 때 다시 오는 주소의 수",
      "Endpoints 는 서비스의 주소를 한 객체에 담아 바뀔 때마다 전체를 보낸다. EndpointSlice 는 기본 100개씩 조각으로 "
      "나눠 바뀐 조각만 보낸다. 현행 Endpoints 는 1000개를 넘으면 잘린다.",
      "주황 막대가 지금 CoreDNS 가 받는 양입니다")

X0, K = 250, 0.18          # px per address — 3000 개 = 540px


def bar(y, n, c, op="40", dash=None, x_from=0):
    x = X0 + x_from * K
    w = n * K
    if dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="3" fill="none" '
                   f'stroke="{c}" stroke-width="1.1" stroke-dasharray="{dash}"/>')
    else:
        d.tone(x, y, w, 24, c, 3, op, 1.1)
    return x + w


groups = [
    (132, "백엔드 300개 서비스", [("Endpoints", 300, MUTED, "300 · 객체 전체"),
                                 ("EndpointSlice", 100, MUTED, "100 · 바뀐 조각 하나")]),
    (262, "백엔드 3000개 서비스", [("Endpoints", 1000, MUTED, None),
                                  ("EndpointSlice", 100, ACC, "100 · 조각 30개 중 하나")]),
]
for gy, title, bars in groups:
    d.t(20, gy, title, 14, INK, KR, "start", 600)
    d.t(X0, gy, "파드 하나가 바뀔 때 다시 보내는 주소", 12, SOFT, KR, "start")
    for j, (nm, n, c, lab) in enumerate(bars):
        y = gy + 16 + j * 46
        d.t(20, y + 17, nm, 13, ACC if c == ACC else INK, MONO, "start", 600)
        end = bar(y, n, c)
        if lab:
            d.t(end + 10, y + 17, lab, 12, ACC if c == ACC else MUTED, KR, "start")
        if nm == "Endpoints" and n == 1000:
            d.t(X0 + 10, y + 17, "1000 · 전체 재전송", 12, INK, KR, "start")
            e2 = bar(y, 2000, BAD, dash="4 4", x_from=1000)
            d.t(X0 + 1000 * K + 12, y + 17, "잘린 2000 · 객체에 없음", 12, BAD, KR, "start")

d.t(20, 400, "조각 하나 · 기본 100 개 · 300 과 3000 은 예시 수 · CoreDNS 는 지금 EndpointSlice 를 감시", 13, MUTED, KR, "start")

d.legend(420, [("한 번에 다시 보내는 주소", MUTED), ("1000 에서 잘린 주소", BAD), ("지금 CoreDNS 가 받는 양", ACC)])
d.save("06-02.endpoints-slices.svg")
