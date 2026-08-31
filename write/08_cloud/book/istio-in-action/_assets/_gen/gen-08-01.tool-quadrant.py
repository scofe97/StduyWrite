# 08-01 §1 Grafana · Jaeger · Kiali 가 답하는 질문의 자리.
# 본문 근거: 저자 8.3 "Kiali is different from Grafana in that it focuses on building a directed graph
#            of how the services interact with each other with live-updating metrics. Grafana is great
#            at dashboards with gauges, counters, charts, and more but does not present an interactive
#            drawing or map of the services in the cluster." → 축 둘(재료 · 그리는 대상)이 여기서 나온다.
# 네 번째 칸(개별 요청을 수치로)은 이 장이 비워 둔다. Envoy 액세스 로그가 그 자리이고 10 장이 맡는다.
# 타입 스펙: type-quadrant — 2×2 격자. 축 라벨은 팁마다 한 단어(Jobs-minimal, 화살표 글리프 · 괄호 금지),
#           항목은 r=4 점 + 라벨, 초점 하나(coral). 항목이 축선을 걸치지 않게 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "ISTIO IN ACTION · 08-01 §1",
      "세 화면은 재료도 그리는 것도 다르다",
      "가로축은 무엇을 재료로 삼는가, 세로축은 무엇을 그리는가. 저자가 Kiali 를 꺼내며 Grafana 와의 "
      "차이부터 못 박은 문장에서 이 두 축이 나온다. 색이 붙은 것이 이 장의 절반을 쓰는 화면이다.",
      "개별 요청을 수치로 보는 자리는 이 장이 비워 둡니다 — 10 장의 액세스 로그입니다")

CX, CY = 500, 340
AX0, AX1 = 176, 824          # 가로축 양 끝
AY0, AY1 = 152, 520          # 세로축 양 끝

# 축 — 팁이 바깥을 향하는 화살표 둘
d.path(f"M {CX} {AY1} L {CX} {AY0}", INK, 1.2, m="ar")
d.path(f"M {AX0} {CY} L {AX1} {CY}", INK, 1.2, m="ar")
d.line(CX, AY1, CX, CY, INK, 1.2)
d.line(AX0, CY, CX, CY, INK, 1.2)

# 축 라벨 — 팁 바깥, 한 단어
d.t(CX, AY0 - 14, "관계", 9, INK, MONO, "middle", 400)
d.t(CX, AY1 + 22, "수치", 9, INK, MONO, "middle", 400)
d.t(AX0 - 14, CY + 4, "집계", 9, INK, MONO, "end", 400)
d.t(AX1 + 14, CY + 4, "개별", 9, INK, MONO, "start", 400)

def item(x, y, name, sub, focal=False, dx=14, anchor="start"):
    c = ACC if focal else MUTED
    d.o.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
    d.t(x + dx, y - 3, name, 13, ACC if focal else INK, KR, anchor, 600)
    d.t(x + dx, y + 14, sub, 9, MUTED, MONO, anchor)

item(320, 232, "Kiali", "prometheus -> graph")
item(688, 216, "Jaeger", "spans -> one trace", focal=True)
item(340, 432, "Grafana", "prometheus -> panels")
item(676, 440, "Envoy access log", "ch.10 · not covered here")

# 칸 이름 — 축선에서 떨어뜨려 모서리에
d.t(196, 176, "집계에서 관계로", 10, SOFT, KR, "start")
d.t(804, 176, "한 요청의 관계", 10, SOFT, KR, "end")
d.t(196, 500, "집계된 값", 10, SOFT, KR, "start")
d.t(804, 500, "한 요청의 값", 10, SOFT, KR, "end")

d.t(32, 576, "Prometheus 는 Kiali 의 선택지가 아니라 먼저 깔려 있어야 하는 하드 의존이다", 11, SOFT, KR, "start")
d.legend(596, [("이 장의 절반이 쓰이는 화면", ACC), ("나머지 화면", MUTED)])
d.save("08-01.tool-quadrant.svg")
