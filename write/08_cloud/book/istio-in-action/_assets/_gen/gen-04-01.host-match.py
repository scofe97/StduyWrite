# 04-01 §2 Host 헤더에 따라 갈리는 두 응답 — 저자가 일부러 실패부터 보이는 실습.
# 본문: "Host: localhost 로 갔고, 게이트웨이도 VirtualService 도 그 호스트를 모르니 404 (VirtualService 적용 뒤의 실험 — blackhole 은 VS 없을 때의 라우트라 여기 안 그린다).
# -H Host: webapp.istioinaction.io 를 붙이면 200. 게이트웨이는 선언된 가상 호스트만 안다."
# 타입 스펙: type-sequence — 주체 셋(curl · 인그레스 게이트웨이 · webapp)의 시간순 메시지. alt 프레임 하나에
#           두 구간. 반환은 점선, coral 은 두 번째 구간의 마지막 200 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 624
d = Seq(W, H, "ISTIO IN ACTION · 04-01 §2",
        "Host 헤더에 따라 갈리는 두 응답",
        "같은 경로를 두 번 부른다. Host: localhost 는 선언된 가상 호스트가 아니라 404 로 끝나고, "
        "Host: webapp.istioinaction.io 는 VirtualService 가 만든 라우트를 타고 webapp 까지 가서 200 을 받는다.",
        "게이트웨이는 Gateway·VirtualService 에 선언된 가상 호스트만 안다")

LX = d.lanes([("curl", "클러스터 밖"), ("인그레스 게이트웨이", "Envoy · 8080"), ("webapp", "istioinaction ns")], y0=104, lane_w=210)
XC, XG, XW = LX["curl"], LX["인그레스 게이트웨이"], LX["webapp"]
d.rails(556)

def call(a, b, label, y, c=MUTED, mk="ar", dash=None):
    x1, x2 = LX[a], LX[b]; s = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 10 * s} {y} L {x2 - 12 * s} {y}", c, 1.5, m=mk, dash=dash)
    d.t((x1 + x2) / 2, y - 8, label, 12, c, KR)

def state(x, txt, y, c, w):
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="5" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, txt, 12, c, KR)

FX, FY, FH = XC - 68, 172, 368
FW = (XW + 68) - FX
d.o.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="4" fill="rgba(245,245,245,0.04)" stroke="rgba(245,245,245,0.22)" stroke-width="1"/>')
d.o.append(f'<rect x="{FX}" y="{FY}" width="40" height="16" rx="2" fill="{PAPER}" stroke="rgba(245,245,245,0.22)" stroke-width="1"/>')
d.t(FX + 20, FY + 12, "ALT", 8, MUTED, MONO)
d.t(XC + 20, FY + 34, "[Host: localhost]", 12, SOFT, KR, "start")

call("curl", "인그레스 게이트웨이", "GET /api/catalog", 236)
state(XG, "선언된 가상 호스트가 아님", 272, WARN, 200)
call("인그레스 게이트웨이", "curl", "404 Not Found", 308, MUTED, "ar", "4 3")

DIV = 340
d.line(FX + 8, DIV, FX + FW - 8, DIV, "rgba(245,245,245,0.20)", 1.0, "4 3")
d.t(XC + 20, DIV + 22, "[Host: webapp.istioinaction.io]", 12, SOFT, KR, "start")

call("curl", "인그레스 게이트웨이", "GET /api/catalog", 404)
call("인그레스 게이트웨이", "webapp", "outbound|8080||webapp…svc.cluster.local", 440)
call("webapp", "인그레스 게이트웨이", "200", 476, MUTED, "ar", "4 3")
call("인그레스 게이트웨이", "curl", "200 + 상품 목록 JSON", 512, ACC, "acc", "4 3")

d.legend(580, [("선언되지 않은 호스트", WARN), ("VirtualService 가 낸 길", ACC)])
d.save("04-01.host-match.svg")
print("h 필요:", 580 + 22 + 16, " 실제:", H)
