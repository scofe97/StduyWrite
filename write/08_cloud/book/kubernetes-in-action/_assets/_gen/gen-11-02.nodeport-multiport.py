# 11-02 §1 — 여섯 번호는 두 입구와 한 도착지다
# 본문이 '세 주소를 차례로 밟는 것이 아니다'라고 못박는다. 그래서 3 단 체인으로 그리면 안 되고,
# 두 입구가 한 도착지로 합류하는 Y 형태여야 한다. 프로토콜마다 한 벌씩.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1120, 694, "KUBERNETES IN ACTION · 11-02",
      "여섯 번호는 두 입구와 한 도착지다",
      "NodePort 는 포트 번호를 여섯 개 쓴다. 프로토콜마다 밖에서 들어오는 입구와 안에서 들어오는 입구가 따로 있고, "
      "둘은 같은 파드 포트로 이어진다. 한 요청이 세 번호를 차례로 밟는 것이 아니다.",
      "kiada Service · HTTP 와 HTTPS 각각")

def protocol(y0, name, nodeport, svcport, target):
    ddx.band(d, y0, y0 + 216, name, x=24, w=1072)
    cy = y0 + 108
    for dy, t, s, c in ((-46, f"노드 IP : {nodeport}", "nodePort · 밖에서 들어온다", ACC),
                        (46, f"ClusterIP : {svcport}", "port · 안에서 들어온다", INFO)):
        d.box(70, cy + dy - 31, 300, 62, PAPER2, c, 1.1, 6)
        d.t(220, cy + dy - 6, t, 13, c, KR, "middle", 600)
        d.t(220, cy + dy + 15, s, 11, MUTED, KR)
    d.path(f"M 372 {cy-46} L 480 {cy-46} L 480 {cy} L 748 {cy}", MUTED, 1.5, m="ar")
    d.path(f"M 372 {cy+46} L 480 {cy+46} L 480 {cy}", MUTED, 1.5)
    d.t(614, cy - 14, "같은 파드 목록", 11, SOFT, KR)
    d.box(750, cy - 40, 300, 80, PAPER2, RULE, 1.1, 6)
    d.t(900, cy - 10, f"파드 : {target}", 14, INK, KR, "middle", 600)
    d.t(900, cy + 14, "targetPort · 실제로 듣는 포트", 11, MUTED, KR)

protocol(100, "HTTP", 30080, 80, 8080)
protocol(340, "HTTPS", 30443, 443, 8443)

ddx.focal_tag(d, 560, 590, "두 입구는 각자 파드로 이어진다", 254)
d.t(24, 626, "cluster IP 는 어느 인터페이스에도 붙지 않아 무언가를 경유시킬 실체가 없다. "
             "화살표는 어느 주소로 들어오면 어디에 닿는지의 매핑이지, 한 요청이 밟는 순서가 아니다.",
     11, MUTED, KR, "start")
d.legend(646, [("밖에서 들어오는 문", ACC), ("안에서 들어오는 문", INFO)])
d.save("11-02-nodeport-multiport.svg")
print("ok")
