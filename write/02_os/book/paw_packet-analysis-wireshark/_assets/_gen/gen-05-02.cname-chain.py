# 05-02 §2 — 원문 DNS-Packet.pcap 예제의 CNAME 체인. 질의 한 줄에 답 두 줄이 오고, 첫 줄이 이름을 다른
# 이름으로 넘기며 둘째 줄이 그 이름의 AAAA 주소를 준다. 값은 원문 그대로다.
# 본문 요구: "ipv6.google.com 의 정규 이름이 ipv6.l.google.com 이고, ipv6.l.google.com 의 AAAA 주소가
#            2404:6800:4007:805::200e 라는 두 줄입니다" · "응답 줄이 여럿일 때 어느 것이 최종 답인지는
#            이렇게 체인을 따라가 확인합니다." CNAME 의 뜻은 RFC 1034 §3.6.2.
# 타입 스펙: type-sequence — 클라이언트와 이름 서버 사이의 질의·응답. 응답 섹션은 아래에 계단으로 펴서
#           앞 줄의 오른쪽 이름이 다음 줄의 왼쪽 이름이 되는 모습을 보인다. focal 은 CNAME 한 줄.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO
class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, KR)
    def lanes(s, names, y0=104, lane_w=210):
        LX = Seq.lanes(s, [(nm, "") for nm, _ in names], y0, lane_w)
        for nm, sub in names:
            s.t(LX[nm], y0 + 37, sub, 12, MUTED, _kr(sub))
        return LX

W, H = 940, 608
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §2",
          "질의 한 줄에 답 두 줄 — CNAME 체인",
          "원문 DNS-Packet.pcap 예제. 클라이언트가 이름 서버 8.8.4.4 에 ipv6.google.com 의 AAAA 를 묻고, 응답 섹션에 두 줄이 온다. 첫 줄은 ipv6.google.com 이 별칭이고 정규 이름이 ipv6.l.google.com 이라고 알리고, 둘째 줄이 ipv6.l.google.com 의 AAAA 주소를 준다.",
          "첫 줄이 이름을 넘기고 둘째 줄이 주소를 줍니다 — 앞 줄의 오른쪽 이름이 다음 줄의 왼쪽 이름입니다")

d.lanes([("클라이언트", "리졸버"), ("이름 서버", "8.8.4.4")], y0=104, lane_w=220)
d.rails(292)
d.msg("클라이언트", "이름 서버", "AAAA  ipv6.google.com", 200, INFO, "info", sub="질의 섹션 한 줄")
d.msg("이름 서버", "클라이언트", "응답", 256, MUTED, "ar", dash="5 4", sub="응답 섹션 두 줄 · 아래")

# 응답 섹션 — 계단
BX, BY, BW, BH = 24, 316, W - 48, 208
d.box(BX, BY, BW, BH, PAPER, RULE, 1.0, 6)
d.t(BX + 16, BY + 24, "응답 섹션", 12, SOFT, KR, "start", 600)

NW, NH = 180, 40                   # 이름 칸
TAG_X = 48                         # 줄 번호 열
X1 = 128                           # 첫 이름 칸
GAP = 88                           # 이름 칸 사이 (타입 라벨 자리)
X2 = X1 + NW + GAP                 # 둘째 이름 칸
X3 = X2 + NW + GAP                 # 주소 칸
AW = BX + BW - 16 - X3             # 주소 칸 폭
R1, R2 = BY + 64, BY + 144         # 두 줄의 위쪽 y

def name_box(x, y, w, txt, c=None):
    if c: d.tone(x, y, w, NH, c, 6)
    else: d.box(x, y, w, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 25, txt, 13, c if c else INK, MONO, "middle", 600)

# 답 1 — CNAME
d.t(TAG_X, R1 + 25, "답 1", 12, MUTED, KR, "start", 600)
name_box(X1, R1, NW, "ipv6.google.com")
d.arrow([(X1 + NW + 4, R1 + NH / 2), (X2 - 4, R1 + NH / 2)], ACC, "acc", 1.7)
d.t(X1 + NW + GAP / 2, R1 + NH / 2 - 10, "CNAME", 12, ACC, MONO, "middle", 600)
name_box(X2, R1, NW, "ipv6.l.google.com")

# 같은 이름이 다음 줄로 내려간다
d.line(X2 + NW / 2, R1 + NH + 4, X2 + NW / 2, R2 - 4, SOFT, 1.0, "3 4")
d.t(X2 + NW / 2 + 12, (R1 + NH + R2) / 2 + 4, "같은 이름", 12, SOFT, KR, "start")

# 답 2 — AAAA
d.t(TAG_X, R2 + 25, "답 2", 12, MUTED, KR, "start", 600)
name_box(X2, R2, NW, "ipv6.l.google.com")
d.arrow([(X2 + NW + 4, R2 + NH / 2), (X3 - 4, R2 + NH / 2)], OK, "ok", 1.7)
d.t(X2 + NW + GAP / 2, R2 + NH / 2 - 10, "AAAA", 12, OK, MONO, "middle", 600)
name_box(X3, R2, AW, "2404:6800:4007:805::200e", OK)

d.legend(H - 56, [("이름을 넘기는 줄", ACC), ("최종 주소", OK), ("질의", INFO)])
d.save("05-02.cname-chain.svg")
