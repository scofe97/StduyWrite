# 11-01 §7 — NAT 가 끼는 곳은 목적지가 정한다
# 같은 출발지에서 목적지만 달리한 두 경로 대비. 띠 둘을 같은 좌표로 겹쳐 놓아
# 같은 자리의 칩 값이 어디서 갈리는지 세로로 읽히게 했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1060, 620, "KUBERNETES IN ACTION · 11-01",
      "NAT 가 끼는 곳은 목적지가 정한다",
      "같은 파드에서 출발해도 목적지를 무엇으로 적었느냐에 따라 커널이 하는 일이 갈린다. "
      "파드 IP 는 그대로 지나가고, ClusterIP 는 실제 파드 주소로 바꿔야 비로소 닿는다.",
      "왜 curl 은 되는데 ping 은 안 되는가")

def path_band(y0, label, cy, kernel_sub, dst_in, dst_out, out_c, focal):
    ddx.band(d, y0, y0 + 184, label, x=24, w=1012)
    ddx.node(d, 160, cy, "출발 파드", "10.244.1.5", 200, 76, INFO)
    ddx.node(d, 530, cy, "노드 커널", kernel_sub, 280, 76, focal=focal)
    ddx.node(d, 900, cy, "도착 파드", "10.244.2.9", 200, 76, INFO)
    d.path(f"M 268 {cy} L 380 {cy}", MUTED, 1.5, m="ar")
    d.path(f"M 678 {cy} L 790 {cy}", MUTED, 1.5, m="ar")
    d.chip(325, cy - 30, dst_in, SOFT, 9)
    d.chip(735, cy - 30, dst_out, out_c, 9)

path_band(100, "파드 IP 로 직접 보낼 때", 206,
          "맞는 규칙이 없어 그냥 지나간다", "dst 10.244.2.9", "dst 10.244.2.9", SOFT, False)
path_band(316, "ClusterIP 로 보낼 때", 422,
          "명단에서 하나 골라 DNAT", "dst 10.96.74.151", "dst 10.244.2.9", ACC, True)

d.t(24, 540, "ping 이 안 되는 이유도 여기 있다. DNAT 규칙은 'ClusterIP 와 포트'의 짝에만 걸리는데 "
             "ICMP 에는 포트가 없어 어느 규칙에도 맞지 않고, 패킷이 그대로 버려진다.", 11, MUTED, KR, "start")
d.legend(566, [("파드 주소", INFO), ("바뀐 자리", ACC)])
d.save("11-01-nat-dnat-paths.svg")
print("ok")
