# 07-02 §5 — 도메인 이름 공간의 트리와, 각 층을 누가 돌보는가.
# 원문("DNS"): "The DNS is a worldwide, hierarchical naming system for hosts and services on the internet."
#   Domain name space: "A tree structure with . as the root and each tree node and leaf containing
#       information about a certain space. The labels (63 bytes maximum length) along the path from a leaf
#       to the root is what we call a fully qualified domain name (FQDN). For example, demo.mhausenblas.info.
#       is an FQDN with the so-called top-level domain .info. Note that the right-most dot, the root, is
#       often left off."
#   "at its root sit 13 root servers that manage the records for the top-level domains."
#   TLD 넷 — Infrastructure · Generic(gTLD) · Country-code(ccTLD) · Sponsored(sTLD).
#   "each entity (Afilias or me) only looks after its part, and no coordination is required. For example,
#       to create the demo subdomain, I only had to change my DNS settings for the zone, without asking
#       anyone at Afilias for support or permissions. This seemingly simple fact is the core of the
#       decentralized nature of DNS and is what makes it so scalable."
# 주의: 원문은 인프라 TLD 의 예로 example 과 localhost 를 들지만 IANA 루트 존에서 infrastructure 로
#       분류된 TLD 는 .arpa 하나다. 도식은 .arpa 를 적고 원문 표기를 정오로 병기한다.
# 타입 스펙: type-tree — 뿌리에서 잎으로 내려가는 포함 관계, 직교 연결. accent 는 조율 없이
#           각자 자기 부분만 돌본다는 사실이 드러나는 자리. 축약: TLD 는 종류마다 하나씩만 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 752
d = D(W, H, "LEARNING MODERN LINUX · 07-02 §5",
      "각자 자기 부분만 돌보고 조율은 없다",
      "잎에서 뿌리까지의 라벨을 이은 것이 FQDN 이다. 층마다 관리 주체가 다르고 서로 허락을 "
      "구하지 않는데, 그 단순한 사실이 DNS 를 확장 가능하게 만든다.",
      "라벨 하나의 최대 길이는 63바이트입니다")

RX, RY, RW, RH = 372, 152, 136, 46
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.1, 8)
d.t(RX + RW / 2, RY + 20, "루트 · \".\"", 13, INK, MONO, "middle", 600)
d.t(RX + RW / 2, RY + 38, "루트 서버 13", 10.5, MUTED, KR)

TW, TGAP, TY, BUS = 196, 12, 258, 226
tlds = [
    ("인프라", ".arpa", "IAB 가 관리", WARN),
    ("일반 gTLD", ".org · .com", "세 글자 이상", INFO),
    ("국가 ccTLD", ".kr · .de", "두 글자 ISO 코드", INFO),
    ("후원 sTLD", ".aero · .gov", "자격을 제한한다", INFO),
]
for i, (kind, name, note, col) in enumerate(tlds):
    x = 24 + i * (TW + TGAP)
    cx = x + TW / 2
    d.path(f"M {RX + RW / 2} {RY + RH} L {RX + RW / 2} {BUS} L {cx} {BUS} L {cx} {TY - 2}",
           col, 1.2, m="ar")
    d.box(x, TY, TW, 76, PAPER2, col, 1.2, 6)
    d.t(x + TW / 2, TY + 26, kind, 13, col, KR, "middle", 600)
    d.t(x + TW / 2, TY + 48, name, 12, INK, MONO)
    d.t(x + TW / 2, TY + 68, note, 10.5, MUTED, KR)

# .info 갈래를 아래로 이어 FQDN 을 만든다
IX = 24 + 1 * (TW + TGAP)
CHW = TW * 2 + TGAP
chain = [(".info", "Afilias 가 관리하는 일반 TLD", 380),
         ("mhausenblas.info", "저자가 산 도메인", 440),
         ("demo.mhausenblas.info", "저자가 만든 서브도메인", 500)]
for i, (name, note, y) in enumerate(chain):
    focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{IX}" y="{y}" width="{CHW}" height="52" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(IX, y, CHW, 52, PAPER2, RULE, 1.0, 6)
    d.t(IX + 16, y + 24, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(IX + CHW - 16, y + 42, note, 10.5, MUTED, KR, "end")
    src_y = TY + 76 if i == 0 else chain[i - 1][2] + 52
    d.path(f"M {IX + CHW / 2} {src_y} L {IX + CHW / 2} {y - 2}", MUTED, 1.2, m="ar")

BY = 576
d.o.append(f'<rect x="24" y="{BY}" width="416" height="76" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(44, BY + 26, "허락을 구하지 않는다", 13, ACC, KR, "start", 600)
d.t(44, BY + 48, "demo 서브도메인을 만들려고 Afilias 의 누구에게도", 11.5, ACC, KR, "start")
d.t(44, BY + 66, "지원이나 허가를 요청할 필요가 없었습니다.", 11.5, MUTED, KR, "start")

d.tone(456, BY, 400, 76, WARN)
d.t(476, BY + 26, "원문 정오 — 인프라 TLD 의 예", 13, INK, KR, "start", 600)
d.t(476, BY + 48, "저자는 example 과 localhost 를 드는데, IANA 루트 존에서", 11.5, MUTED, KR, "start")
d.t(476, BY + 66, "infrastructure 로 분류된 것은 .arpa 하나뿐입니다.", 11.5, MUTED, KR, "start")

d.legend(692, [("확인이 필요한 분류", WARN), ("나머지 TLD 종류", INFO),
               ("조율 없이 각자 돌보는 자리", ACC)])
d.save("07-02.dns-tree.svg")
print("ok 07-02.dns-tree")
