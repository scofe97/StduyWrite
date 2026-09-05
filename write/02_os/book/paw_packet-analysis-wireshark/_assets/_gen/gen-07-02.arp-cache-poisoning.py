# 07-02 §3 — 한 호스트의 ARP 캐시가 오염되는 과정. 원문 ARP_Duplicate_IP.pcap 의 실제 MAC 을 쓴다.
# 타입 스펙: type-state — 주체 하나(피해 호스트의 ARP 캐시)의 상태 전이.
#           전이 라벨은 캡처에 보이는 프레임이고, focal 은 트래픽이 새는 상태 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 992, 452
X = [24, 264, 504, 744]
SW, SH, Y = 224, 64, 176

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 07-02 §3",
      "ARP 캐시가 오염되는 순서",
      "원문 예제에서 하나의 MAC 이 여러 IP 의 주인이라고 주장한다. ARP 에는 그 주장을 검증할 장치가 없으므로 캐시는 마지막에 들은 말을 믿고, 그 순간부터 트래픽이 남의 손을 거친다.",
      "Wireshark 는 막지 못하고 알려 줄 뿐입니다 — arp.duplicate-address-frame")

def state(i, name, sub, focal=False, c=None):
    x = X[i]
    if focal: d.tone(x, Y, SW, SH, BAD, 8)
    elif c: d.tone(x, Y, SW, SH, c, 8)
    else: d.box(x, Y, SW, SH, PAPER2, RULE, 1.0, 8)
    col = BAD if focal else (c if c else INK)
    d.t(x + SW / 2, Y + 26, name, 12, col, KR, "middle", 600)
    d.t(x + SW / 2, Y + 46, sub, 11, MUTED, MONO)

for i in range(3):
    d.arrow([(X[i] + SW, Y + SH / 2), (X[i + 1] - 4, Y + SH / 2)],
            BAD if i == 1 else MUTED, "bad" if i == 1 else "ar", 1.4)

labels = [("주소를 몰라 물어봄", "응답을 검증할 절차가 없습니다"),
          ("위조 ARP 응답 수신", "10.0.0.7 is at fa:16:3e:bf:22:d0"),
          ("보내는 프레임의 목적지가 바뀜", "Wireshark 가 Warn 을 답니다")]
for i, (lab, sub) in enumerate(labels):
    mx = (X[i] + SW + X[i + 1]) / 2
    d.t(mx, Y - 20, lab, 11, BAD if i == 1 else MUTED, KR)
    d.t(mx, Y + SH + 26, sub, 11, SOFT, MONO if not any("가" <= c <= "힣" for c in sub) else KR)

state(0, "정상", "10.0.0.7 = ...19:5a:cc", c=OK)
state(1, "요청을 보냄", "who has 10.0.0.7")
state(2, "오염됨", "10.0.0.7 = ...bf:22:d0", focal=True)
state(3, "중간자를 거침", "A - 공격자 - B", c=WARN)

d.path(f"M {X[3] + SW / 2} {Y + SH + 48} V {Y + SH + 72} H {X[0] + SW / 2} V {Y + SH + 4}", OK, 1.4, m="ok")
d.t((X[0] + X[3]) / 2 + SW / 2, Y + SH + 66, "진짜 주인의 ARP 가 오거나 캐시가 만료되면 원래대로", 11, OK, KR)

d.legend(H - 60, [("트래픽이 새는 상태", BAD), ("돌아오는 길", OK)])
d.save("07-02.arp-cache-poisoning.svg")
