# 타입 스펙: type-data-flow — 단계마다 누가 무엇을 하는지. 칸을 건너는 동안 어느 필드가 다시 쓰이는지.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.1 Figure 6.19 —
#   두 서브넷과 라우터, IP·MAC 주소는 그림의 값 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 552
d = D(W, H, "SECTION 6.4.1 · SENDING A DATAGRAM OFF THE SUBNET",
      "MAC 주소는 홉마다 바뀌고 IP 주소는 그대로입니다",
      "서브넷 1 의 호스트가 서브넷 2 의 호스트로 보낼 때, 첫 프레임의 목적지 MAC 은 최종 목적지가 아니라 첫 홉 라우터의 것이다.",
      "주소는 원문 Figure 6.19 의 값입니다")

NODES = [
    (24, "보내는 호스트", "111.111.111.111", "74-29-9C-E8-FF-55", INFO),
    (376, "라우터", "111.111.111.110 · 222.222.222.220", "E6-E9-00-17-BB-4B · 1A-23-F9-CD-06-9B", MUTED),
    (752, "받는 호스트", "222.222.222.222", "49-BD-D2-C7-56-2A", OK),
]
NW = 224
for x, name, ip, mac, c in NODES:
    w = 320 if name == "라우터" else NW
    d.box(x, 116, w, 76, PAPER2, f"{c}55", 1.2, 6)
    d.t(x + w / 2, 140, name, 12, c, KR, "middle", 600)
    d.t(x + w / 2, 160, ip, 10, INK, MONO)
    d.t(x + w / 2, 178, mac, 10, MUTED, MONO)

d.t(136, 104, "서브넷 1 · 111.111.111/24", 10, SOFT, KR)
d.t(864, 104, "서브넷 2 · 222.222.222/24", 10, SOFT, KR)
d.arrow([(248, 154), (370, 154)], MUTED, "ar", 1.5)
d.arrow([(700, 154), (746, 154)], MUTED, "ar", 1.5)

FY, FH = 232, 148


def frame(x, w, title, dst_mac, src_mac, c):
    d.box(x, FY, w, FH, PAPER2, RULE, 1.0)
    d.t(x + 16, FY + 24, title, 11, INK, KR, "start", 600)
    d.line(x + 16, FY + 34, x + w - 16, FY + 34, RULE, 0.8)
    d.tone(x + 16, FY + 46, w - 32, 40, c, 4, "14", 1.2)
    d.t(x + 24, FY + 62, "목적지 MAC", 10, SOFT, KR, "start")
    d.t(x + w - 24, FY + 62, dst_mac, 11, c, MONO, "end", 600)
    d.t(x + 24, FY + 80, "출발지 MAC", 10, SOFT, KR, "start")
    d.t(x + w - 24, FY + 80, src_mac, 11, c, MONO, "end")
    d.tone(x + 16, FY + 94, w - 32, 40, ACC, 4, "14", 1.2)
    d.t(x + 24, FY + 110, "목적지 IP", 10, SOFT, KR, "start")
    d.t(x + w - 24, FY + 110, "222.222.222.222", 11, ACC, MONO, "end", 600)
    d.t(x + 24, FY + 128, "출발지 IP", 10, SOFT, KR, "start")
    d.t(x + w - 24, FY + 128, "111.111.111.111", 11, ACC, MONO, "end")


frame(24, 452, "서브넷 1 을 지나는 프레임", "E6-E9-00-17-BB-4B", "74-29-9C-E8-FF-55", INFO)
frame(524, 452, "서브넷 2 를 지나는 프레임", "49-BD-D2-C7-56-2A", "1A-23-F9-CD-06-9B", OK)
d.arrow([(480, FY + 74), (518, FY + 74)], MUTED, "ar", 1.4)
d.t(499, FY + 60, "새로", 10, MUTED, KR)

d.line(24, 412, W - 48, 412, RULE, 0.8)
d.t(24, 434, "첫 프레임의 목적지 MAC 을 최종 목적지의 것으로 두면 서브넷 1 의 어느 어댑터도 그 프레임을 위로 올리지 않습니다.",
     11, MUTED, KR, "start")
d.t(24, 452, "데이터그램은 그대로 사라집니다. 그래서 첫 홉 라우터 인터페이스의 MAC 을 ARP 로 먼저 알아냅니다.",
     11, MUTED, KR, "start")
d.t(24, 470, "라우터는 포워딩 표로 나갈 인터페이스를 고르고, 그 인터페이스가 새 프레임을 만들어 다시 ARP 로 목적지 MAC 을 얻습니다.",
     11, MUTED, KR, "start")

d.legend(490, [("칸을 건너도 안 바뀌는 IP", ACC), ("서브넷 1 의 MAC", INFO), ("서브넷 2 의 MAC", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-03.hop-by-hop-frames.svg"
d.save(out)
print("→", out)
