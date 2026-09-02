# 02-01 §6 — 질의를 받은 DNS 서버가 답을 만들기까지 밟는 판단 순서.
# 원문 근거: 권한 있는 존이면 직접 응답 / 포워더를 쓰도록 설정된 서버는 "first looks in its
#            authoritative zone data and cache for an answer, and if it doesn't find one, it forwards
#            the query to its forwarder" / 그렇지 않으면 루트 힌트에서 시작해 referral 을 따라간다
#            (= recursion) / 리졸버는 재귀 질의를, 서버끼리는 기본적으로 비재귀(반복) 질의를 보낸다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리이고 분기마다 라벨을 단다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, INFO, KR, MONO

W, H = 880, 720
d = D(W, H, "LEARNING COREDNS · 02-01 §6",
      "질의를 받은 서버가 밟는 판단 순서",
      "권한과 캐시를 먼저 보고, 포워더가 설정돼 있으면 넘기고, 아니면 루트부터 참조를 따라간다. "
      "맨 아래 갈래만이 재귀이며 그 일을 지는 것은 질의를 받은 첫 서버 하나다.",
      "마름모에서 오른쪽이 예, 아래가 아니오입니다")

CX = 300
def diamond(cy, label, sub=None, focal=False):
    hw, hh = 132, 44
    c = ACC if focal else MUTED
    d.path(f"M {CX} {cy-hh} L {CX+hw} {cy} L {CX} {cy+hh} L {CX-hw} {cy} Z", c, 1.4 if focal else 1.0)
    d.t(CX, cy - 2, label, 13, ACC if focal else INK, KR, "middle", 600)
    if sub: d.t(CX, cy + 18, sub, 12, MUTED)

def box(x, cy, w, label, sub, color=None):
    if color:
        d.tone(x, cy - 26, w, 52, color, 6, "14", 1.2)
    else:
        d.box(x, cy - 26, w, 52, PAPER2, RULE, 1.0)
    d.t(x + w / 2, cy - 2, label, 13, color or INK, KR, "middle", 600)
    d.t(x + w / 2, cy + 17, sub, 12, MUTED)

d.o.append(f'<rect x="{CX-100}" y="90" width="200" height="44" rx="20" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(CX, 118, "질의를 받는다", 14, INK, KR, "middle", 600)

d.arrow([(CX, 134), (CX, 168)], MUTED, "ar", 1.4)
diamond(212, "권한 있는 존인가")
d.arrow([(CX + 132, 212), (596, 212)], MUTED, "ar", 1.4)
d.t(468, 200, "예", 12, SOFT, KR)
box(600, 212, 256, "존 데이터로 확정 응답", "authoritative", OK)

d.arrow([(CX, 256), (CX, 300)], MUTED, "ar", 1.4)
d.t(CX + 14, 282, "아니오", 12, SOFT, KR, "start")
diamond(344, "캐시에 있는가")
d.arrow([(CX + 132, 344), (596, 344)], MUTED, "ar", 1.4)
d.t(468, 332, "예", 12, SOFT, KR)
box(600, 344, 256, "캐시로 응답", "TTL 이 남은 동안", INFO)

d.arrow([(CX, 388), (CX, 432)], MUTED, "ar", 1.4)
d.t(CX + 14, 414, "아니오", 12, SOFT, KR, "start")
diamond(476, "포워더가 설정됐는가")
d.arrow([(CX + 132, 476), (596, 476)], MUTED, "ar", 1.4)
d.t(468, 464, "예", 12, SOFT, KR)
box(600, 476, 256, "포워더에 재귀 질의", "서버가 서버에 재귀를 보내는 유일한 경우", INFO)

d.arrow([(CX, 520), (CX, 564)], MUTED, "ar", 1.4)
d.t(CX + 14, 546, "아니오", 12, SOFT, KR, "start")
d.tone(CX - 156, 564, 312, 60, ACC, 6, "12", 1.4)
d.t(CX, 590, "루트 힌트에서 시작해 참조를 따라간다", 14, ACC, KR, "middle", 600)
d.t(CX, 611, "이 갈래만이 recursion", 12, MUTED)

d.t(600, 578, "참조를 돌려주는 서버들은", 13, MUTED, KR, "start")
d.t(600, 600, "재귀를 하지 않는다 — 갖고 있는", 13, MUTED, KR, "start")
d.t(600, 622, "NS 레코드로 답할 뿐이다", 13, MUTED, KR, "start")

d.legend(652, [("재귀를 지는 갈래", ACC), ("확정 응답", OK), ("남에게 기대는 응답", INFO)])
d.save("02-01.server-decision.svg")
