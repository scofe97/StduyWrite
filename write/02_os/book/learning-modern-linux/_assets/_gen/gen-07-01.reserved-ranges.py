# 07-01 §6 — 예약된 IPv4 대역과 그 대역이 컨테이너 환경에서 나타나는 자리.
# 원문("IPv4" 예약 주소): "127.0.0.0 — This subnet is reserved for local addresses, with the most prominent
#       one being the loopback address 127.0.0.1."
#       "169.254.0.0/16 (169.254.0.0 to 169.254.255.255) — These are link local addresses, meaning packets
#       sent there should not be forwarded to other parts of the network. Some cloud providers such as
#       Amazon Web Services use this for special services (metadata)."
#       "224.0.0.0/24 (224.0.0.0 to 239.255.255.255) — This range is reserved for multicast."
#       RFC 1918 — 10.0.0.0~10.255.255.255(10/8), 172.16.0.0~172.31.255.255(172.16/12),
#       192.168.0.0~192.168.255.255(192.168/16). "A private IP range means that the IP addresses in it are
#       not routable on the public internet."
#       "0.0.0.0 ... from a server perspective, [it] refers to all IPv4 addresses present in the machine."
# 주의: 멀티캐스트 행의 접두사는 원문이 /24 라 적지만 괄호 안 범위와 맞지 않는다. 224=11100000,
#       239=11101111 이라 공통 상위 4비트로 /4 가 맞다. 도식은 원문 표기를 적고 정오를 함께 표시한다.
# 타입 스펙: type-dp-security-matrix — 행(대역) × 열(무엇인가 · 컨테이너에서 어디에 나타나나)의 격자.
#           accent 는 실무에서 사고가 가장 잦은 한 행. 축약: RFC 1918 셋은 한 행으로 묶었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 680
d = D(W, H, "LEARNING MODERN LINUX · 07-01 §6",
      "예약된 대역은 쿠버네티스 문서 곳곳에 다시 나타난다",
      "저자가 꼽은 예약 대역 넷을, 컨테이너 환경에서 실제로 마주치는 자리와 나란히 놓은 것. "
      "왼쪽은 원문 그대로이고 오른쪽은 노트가 이은 것이다.",
      "0.0.0.0 은 그 기계의 모든 IPv4 주소를 뜻합니다")

LX, LW, C1, C2 = 24, 236, 272, 316
HY, RY, RH = 172, 196, 62
for name, x, w in [("무엇인가", LX + LW, C1), ("컨테이너에서 만나는 자리", LX + LW + C1, C2)]:
    d.t(x + w / 2, HY, name, 12, MUTED, KR, "middle", 600)
d.line(LX, HY + 12, LX + LW + C1 + C2, HY + 12, RULE, 1)

rows = [
    ("127.0.0.0", "로컬 주소용 서브넷", "127.0.0.1 에 바인딩하면 파드 밖에서 안 닿는다", 1, INFO),
    ("169.254.0.0/16", "링크 로컬 · 전달되지 않음", "169.254.169.254 로 노드 메타데이터를 읽는다", 0, OK),
    ("224.0.0.0/4", "멀티캐스트", "원문은 /24 라 적는다 — 아래 띠 참조", 0, WARN),
    ("10/8 · 172.16/12 · 192.168/16", "RFC 1918 사설 · 공개망에서 라우팅 안 됨",
     "파드 CIDR 과 서비스 CIDR 이 여기에서 잘린다", 0, OK),
    ("0.0.0.0", "그 기계의 모든 IPv4 주소", "컨테이너 앱은 여기에 바인딩해야 한다", 0, INFO),
]
for r, (rng, what, where, focal, col) in enumerate(rows):
    y = RY + r * RH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW + C1 + C2}" height="{RH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.3"/>')
    elif r % 2 == 0:
        d.box(LX, y, LW + C1 + C2, RH, PAPER2, "none", 0, 4)
    c = ACC if focal else col
    d.t(LX + 14, y + RH / 2 + 5, rng, 12, c, MONO, "start", 600)
    d.t(LX + LW + C1 / 2, y + RH / 2 + 5, what, 11.5, ACC if focal else MUTED, KR)
    d.t(LX + LW + C1 + C2 / 2, y + RH / 2 + 5, where, 11.5, ACC if focal else INK, KR)

BY = RY + len(rows) * RH + 12
d.line(LX, BY - 6, LX + LW + C1 + C2, BY - 6, RULE, 1)
d.tone(LX, BY, LW + C1 + C2, 68, WARN)
d.t(LX + 20, BY + 26, "원문 정오 — 멀티캐스트 접두사", 12.5, INK, KR, "start", 600)
d.t(LX + 20, BY + 46,
    "원문은 224.0.0.0/24 라 적고 괄호에 224.0.0.0 ~ 239.255.255.255 를 적어 서로 맞지 않습니다.",
    11.5, MUTED, KR, "start")
d.t(LX + 20, BY + 64,
    "224 는 11100000 이고 239 는 11101111 이라 공통 상위 네 비트로 /4 가 맞습니다.",
    11.5, MUTED, KR, "start")

d.legend(BY + 100, [("주소 자체의 성격", INFO), ("망 안에서만 도는 것", OK),
                    ("표기를 확인해야 하는 곳", WARN), ("사고가 가장 잦은 곳", ACC)])
d.save("07-01.reserved-ranges.svg")
print("ok 07-01.reserved-ranges")
