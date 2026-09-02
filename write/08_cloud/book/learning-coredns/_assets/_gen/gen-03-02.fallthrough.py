# 03-02 §7 — fallthrough 가 없을 때와 있을 때 질의가 어디서 끝나는가.
# 원문 근거: "when a plug-in has been given authority for a zone, it provides a response for any
#            query in that zone. If the requested name does not exist, it will return the DNS
#            response code NXDOMAIN. If the name exists but there is no data of the specified type,
#            it will return an empty answer (also known as NODATA, although that is not a real
#            response code). In some cases, however, we might want to give another plug-in a chance
#            to answer the query. That is what the fallthrough option does."
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리이고 분기마다 라벨을 단다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, INFO, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING COREDNS · 03-02 §7",
      "fallthrough 는 대답을 다음 플러그인에 넘긴다",
      "존에 권한을 받은 플러그인은 그 존의 질의에 무엇이든 답을 내놓는다. 이름이 없으면 NXDOMAIN, "
      "이름은 있고 타입이 없으면 빈 응답이다. fallthrough 는 그 두 자리에서 대답을 넘길 기회를 만든다.",
      "색이 붙은 갈래만 다른 플러그인에 닿습니다")

CX = 300
def diamond(cy, label, focal=False):
    hw, hh = 152, 46
    c = ACC if focal else MUTED
    d.path(f"M {CX} {cy-hh} L {CX+hw} {cy} L {CX} {cy+hh} L {CX-hw} {cy} Z", c, 1.4 if focal else 1.0)
    d.t(CX, cy + 4, label, 13, ACC if focal else INK, KR, "middle", 600)

def box(x, cy, w, label, sub, color=None):
    if color:
        d.tone(x, cy - 28, w, 56, color, 6, "14", 1.2)
    else:
        d.box(x, cy - 28, w, 56, PAPER2, RULE, 1.0)
    d.t(x + w / 2, cy - 4, label, 13, color or INK, KR, "middle", 600)
    d.t(x + w / 2, cy + 15, sub, 12, MUTED)

d.o.append(f'<rect x="{CX-140}" y="92" width="280" height="44" rx="20" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(CX, 120, "권한을 받은 플러그인이 질의를 받는다", 13, INK, KR, "middle", 600)

d.arrow([(CX, 136), (CX, 172)], MUTED, "ar", 1.4)
diamond(218, "이름과 타입이 다 있나")
d.arrow([(CX + 152, 218), (592, 218)], MUTED, "ar", 1.4)
d.t(456, 206, "예", 12, SOFT, KR)
box(596, 218, 260, "레코드로 응답", "여기서 끝난다", OK)

d.arrow([(CX, 264), (CX, 316)], MUTED, "ar", 1.4)
d.t(CX + 14, 296, "아니오", 12, SOFT, KR, "start")
diamond(362, "fallthrough 가 있나", focal=True)
d.arrow([(CX, 408), (CX, 460)], MUTED, "ar", 1.4)
d.t(CX + 14, 440, "아니오", 12, SOFT, KR, "start")
box(CX - 160, 490, 320, "NXDOMAIN 또는 빈 응답", "이름이 없으면 앞, 타입이 없으면 뒤", INFO)

d.path("M 452 362 L 588 362", ACC, 1.6, m="acc")
d.t(520, 350, "예", 12, ACC, KR)
box(596, 362, 260, "다음 플러그인에 넘긴다", "그쪽이 답할 기회를 얻는다", ACC)

d.t(20, 552, "빈 응답을 NODATA 라 부르기도 하지만 저자는 그것이 실제 응답 코드는 아니라고 못 박습니다", 13, MUTED, KR, "start")

d.legend(572, [("대답을 넘기는 갈래", ACC), ("여기서 끝나는 응답", OK), ("없다고 답하는 응답", INFO)])
d.save("03-02.fallthrough.svg")
