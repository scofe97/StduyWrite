# 07-02 학습 목표 뒤 전체 지도 — 512
# 원문 7장 서두: "We'll first have a look at common network terms, from the hardware level all the way up
#       to user-facing components such as HTTP and SSH. We'll also discuss the network stack, protocols,
#       and interfaces."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 07-02",
      "포트가 있어야 서비스를 가리킬 수 있고 이름이 있어야 사람이 기억한다",
      "7장 둘째 구간의 절 일곱을 읽는 순서로 이은 지도. 1~4절이 전송 계층이고 5~7절이 DNS 다.",
      "5절이 이 노트의 제목이 가리키는 자리입니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "포트", "기계 안에서 서비스를 가리킨다"),
    ("§2", "TCP", "순서와 재전송을 보장한다"),
    ("§3", "UDP", "단순한 대신 위층에 떠넘긴다"),
    ("§4", "소켓", "포트와 IP 의 짝"),
    ("§5", "DNS 가 푸는 두 문제", "기억과 변경"),
    ("§6", "레코드와 존 파일", "노드에 담기는 데이터"),
    ("§7", "조회", "host 와 dig 로 읽기"),
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
    focal = (i == 4)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 54, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(524, [("숫자 대신 이름을 쓰는 이유", ACC)])
d.save("07-02.chapter-overview.svg")
print("ok 07-02.chapter-overview")
