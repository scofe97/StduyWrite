# 05-02 §방법 ③ 각주 — loopback 이 무엇인가
# 본문: "보통의 통신은 랜카드를 거쳐 밖으로 나가지만, loopback 으로 보낸 패킷은 물리
#        네트워크로 나가지 않고 커널 안에서 곧바로 자기에게 되돌아옵니다(loop back = 되돌아옴).
#        port-forward 에서 kubelet 이 Pod 의 이 loopback 장치를 통해 컨테이너에 붙기 때문에,
#        컨테이너 입장에서는 요청이 자기 자신에게서 온 것처럼 보여 Client IP 가 127.0.0.1 로 찍힙니다."
# 타입 스펙: 같은 출발점에서 두 경로가 갈리는 대비이므로 레인 둘. 어디서 갈리는지가 요점이라
#           갈림점(커널 네트워크 스택)을 두 레인이 공유하게 두고 그 뒤만 다르게 그린다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 580
d = D(W, H, "KUBERNETES IN ACTION · 05-02",
      "loopback 은 커널 안에서 자기에게 되돌아오는 통로다",
      "보통의 패킷은 랜카드를 거쳐 물리 네트워크로 나가지만, loopback 으로 보낸 패킷은 밖으로 "
      "나가지 않고 커널 안에서 곧바로 자기에게 돌아온다. 주소는 127.0.0.1, 이름은 localhost 다.",
      lead="받는 쪽이 보는 출발지가 자기 자신이 되는 것이 port-forward 의 127.0.0.1 이다")

# 갈림 라벨을 문장으로 쓰면 코리도어(80px)를 넘어 상자를 덮는다 — 칩으로 줄이고
# 목적지 상자가 뜻을 지게 한다. 밖으로 나간 뒤는 칩 하나로 끝낸다(상자를 더 두면 겹친다).
BW, BH = 190, 76        # 오른쪽 끝 칩이 띠(24~976)를 넘지 않도록 상자를 줄였다
PROC, STACK = (140, 300), (400, 300)
NIC = (760, 224)
LO = (760, 376)
SPINE = 560

ddx.band(d, 104, 520, "갈림은 커널 안에서 일어난다 — 목적지 주소 하나가 경로를 가른다")

def box(cx, cy, t, s, c, w=BW):
    d.box(cx - w // 2, cy - BH // 2, w, BH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 8, ddx.fit(t, 13, w - 18, t), 13, c,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(s, 10, w - 14, t), 10, SOFT, KR)

box(*PROC, "프로세스", "패킷을 보낸다", INFO, w=180)
box(*STACK, "커널 네트워크 스택", "목적지 주소로 갈린다", INFO, w=220)
box(*NIC, "랜카드 eth0", "물리 네트워크로 나간다", MUTED)
box(*LO, "loopback 장치 lo", "커널 안에서 회송한다", ACC)

d.path(f"M 236 {PROC[1]} L {STACK[0]-110-10} {STACK[1]}", MUTED, 1.5, m="ar")

# 두 갈래 — 줄기는 중립, 팔은 각자의 색
d.path(f"M {STACK[0]+110+6} {STACK[1]} L {SPINE} {STACK[1]}", MUTED, 1.4)
d.path(f"M {SPINE} {NIC[1]} L {SPINE} {LO[1]}", MUTED, 1.4)
d.path(f"M {SPINE} {NIC[1]} L {NIC[0]-BW//2-10} {NIC[1]}", MUTED, 1.5, m="ar")
d.chip(607, NIC[1], "밖으로", MUTED, 11)
d.path(f"M {SPINE} {LO[1]} L {LO[0]-BW//2-10} {LO[1]}", ACC, 1.8, m="acc")
d.chip(607, LO[1], "127.0.0.1", ACC, 11)

d.path(f"M {NIC[0]+BW//2+6} {NIC[1]} L 892 {NIC[1]}", MUTED, 1.5, m="ar")
d.chip(930, NIC[1], "밖의 서버", MUTED, 11)

# 되돌아옴 — lo 에서 프로세스로 회송
d.path(f"M {LO[0]-BW//2-6} {LO[1]+18} L {PROC[0]} {LO[1]+18} L {PROC[0]} {PROC[1]+BH//2+10}",
       ACC, 1.8, m="acc")
d.chip(400, LO[1] + 18, "랜카드로 안 나간다 — 커널 안에서 자기에게 회송", ACC, 11)

d.t(36, 462, "그래서 받는 쪽이 보는 출발지는 127.0.0.1 이다.", 12, MUTED, KR, "start")
d.t(36, 484, "port-forward 에서 kubelet 이 Pod 의 이 lo 로 붙으므로 컨테이너는 요청이 "
             "자기에게서 온 것으로 본다.", 12, MUTED, KR, "start")
d.legend(540, [("보내는 쪽과 커널", INFO), ("loopback 경로", ACC)])
d.save("05-02-loopback-concept.svg")
print("ok loopback-concept")
