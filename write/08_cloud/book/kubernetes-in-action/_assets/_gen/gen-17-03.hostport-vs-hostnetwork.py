# 17-03 §2 — 무엇이 사라졌는지가 차이다
# 캡션이 두 경로를 구성 요소로 서술한다 — 한쪽은 portmap DNAT 와 veth 를 거치고, 다른 쪽은
# 변환도 veth 도 없다. 그러니 같은 골격에서 사라진 조각이 보이는 대비여야 한다.
# 타입 스펙: type-architecture.md — 두 밴드가 같은 입구에서 출발해 지나는 구성 요소(노드 포트 · portmap DNAT · veth · 컨테이너)를
#           늘어놓는다. 단계가 아니라 패킷이 통과하는 구성 요소라 process 가 아니라 architecture 다.
#           아래 밴드에서 두 칸이 사라진 것이 이 그림의 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 668, "KUBERNETES IN ACTION · 17-03",
      "변환과 건널목이 있느냐 없느냐",
      "hostPort 는 파드가 자기 netns 를 그대로 가진 채 노드 포트만 빌린다. hostNetwork 는 파드가 "
      "노드 netns 안으로 들어가므로 변환할 것도 건널 것도 없다.",
      "파드가 자기 IP 를 갖느냐가 갈림길이다")

def road(y0, label, steps, c, focal, note):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1172, focal=focal, bar=ACC if focal else None)
    BW, GP = 240, 44
    X0 = 90
    CX = [X0 + BW // 2 + i * (BW + GP) for i in range(len(steps))]
    for cx, (t, s) in zip(CX, steps):
        d.box(cx - BW // 2, y0 + 72, BW, 84, PAPER2, c, 1.1, 6)
        d.t(cx, y0 + 104, ddx.fit(t, 12, BW - 16, t), 12, c, KR, "middle", 600)
        d.t(cx, y0 + 130, ddx.fit(s, 10, BW - 14, s), 10, MUTED, KR)
    for a, b in zip(CX, CX[1:]):
        d.path(f"M {a+BW//2+5} {y0+114} L {b-BW//2-9} {y0+114}", MUTED, 1.4, m="ar")
    # x=1080 은 4 단 행의 마지막 상자(942~1182) 안이라 제목·부제와 겹쳤다. 단 수가 행마다
    # 다르므로 상자 오른쪽이 아니라 상자 아래 띠 가운데에 둔다 — 두 행이 같은 자리를 쓴다.
    d.t(610, y0 + 180, note, 11, c, KR)

road(100, "hostPort — 파드는 자기 netns 를 가진다", [
    ("노드 포트", "9090"), ("portmap DNAT", "목적지를 파드 IP 로"),
    ("veth 를 건넌다", "파드 netns 로"), ("컨테이너", "10.244.1.7:9090"),
], INFO, False, "변환 한 번 · 홉 하나")

road(340, "hostNetwork — 파드가 노드 netns 안에 있다", [
    ("노드 포트", "9090"), ("컨테이너", "노드 소켓에 바로"),
], ACC, True, "변환도 veth 도 없다")

d.t(24, 596, "대신 hostNetwork 는 그 포트를 노드에서 점유한다. 같은 포트를 쓰는 레플리카를 한 노드에 "
             "둘 수 없고, 임의 포트에 바인딩할 수 있어 노출면도 넓다.", 11, MUTED, KR, "start")
d.legend(620 - 4, [("거쳐 간다", INFO), ("바로 닿는다", ACC)])
d.save("17-03-hostport-vs-hostnetwork.svg")
print("ok")
