# 07-01 학습 목표 뒤 전체 지도 — 7장 첫 구간의 절 여덟을 읽는 순서로 잇는다.
# 원문 7장 서두: "We'll first have a look at common network terms, from the hardware level all the way up
#       to user-facing components such as HTTP and SSH. We'll also discuss the network stack, protocols,
#       and interfaces."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 07-01",
      "결국은 선과 공기를 타고 다니는 비트다",
      "7장 첫 구간의 절 여덟을 읽는 순서로 이은 지도. 1~2절이 태도와 뼈대이고, "
      "3~4절이 링크 계층, 5~8절이 인터넷 계층이다.",
      "1절이 이 노트의 제목이 가리키는 자리입니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "추상이 잊게 만드는 것", "왜 층을 기억해야 하는가"),
    ("§2", "네 층과 헤더", "캡슐화는 어느 방향인가"),
    ("§3", "링크 계층", "비트가 신호가 되는 곳"),
    ("§4", "ARP", "MAC 과 IP 를 잇는 다리"),
    ("§5", "인터넷 계층과 IPv4", "32비트를 어디에서 자르나"),
    ("§6", "예약된 대역들", "컨테이너에서 매일 보는 셋"),
    ("§7", "IPv6 와 ICMP", "고갈의 답과 도달 확인"),
    ("§8", "라우팅", "이 패킷을 어디로 보낼까"),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 10
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.3, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 0)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 54, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(524, [("추상 아래에 무엇이 있는가", ACC)])
d.save("07-01.chapter-overview.svg")
print("ok 07-01.chapter-overview")
