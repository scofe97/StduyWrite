# 05-02 심화 학습 — DNS 를 나르는 네 방식을 암호화 여부 × 포트 성격의 2×2 로 놓는다. UDP 53 과 TCP 53 은
# 같은 칸이다 — 전송(UDP · TCP)은 읽히느냐를 정하지 않고, TLS 를 씌웠느냐가 정한다.
# 본문 요구: 학습자가 "평문인 건 UDP 도 마찬가지 아닌가" 를 물었다(후보 20). 전송과 암호화가 다른 축임을 보인다.
# 근거: RFC 7858 §1 · §3.1(평문 DNS 는 엿보기에 노출, DoT 는 853) · RFC 8484 §1(DoH 는 https URI 로 TLS)
#       · RFC 9110 §4.2.2(https 기본 포트 443). TCP 53 이 평문으로 읽히는 것은 2026-09-21 dig +tcp 실측.
# 타입 스펙: type-quadrant — 두 축 위의 위치. 칸마다 이름과 설명을 담는 2×2 판(consultant variant)이다.
#           focal 은 UDP 53 과 TCP 53 이 함께 놓인 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

W, H = 880, 648
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 DEEP DIVE",
      "전송과 암호화는 다른 축",
      "DNS 를 나르는 네 방식을 암호화 여부와 포트 성격으로 놓았다. UDP 53 과 TCP 53 은 전송만 다를 뿐 둘 다 평문이라 같은 칸에 든다. DoT 는 전용 포트 853 에서 TLS 로 감싸고, DoH 는 HTTPS 로 실려 일반 웹 트래픽과 같은 443 을 쓴다.",
      "UDP 53 과 TCP 53 은 같은 칸입니다 — 읽히느냐는 TLS 를 씌웠느냐가 정합니다")

CX, CY = 440, 336                  # 축의 교차점
CW, CH, GAP = 300, 152, 24         # 칸 크기 · 교차점에서 칸까지
TIP = 196                          # 교차점에서 화살 끝까지 (세로)
TIPX = 356                         # 교차점에서 화살 끝까지 (가로)

# 축 — 교차점에서 네 방향으로
for (x2, y2) in [(CX, CY - TIP), (CX, CY + TIP), (CX - TIPX, CY), (CX + TIPX, CY)]:
    d.arrow([(CX, CY), (x2, y2)], INK, "soft", 1.2)
d.t(CX, CY - TIP - 12, "암호화", 12, INK, KR, "middle", 600)
d.t(CX, CY + TIP + 24, "평문", 12, INK, KR, "middle", 600)
d.t(CX - TIPX - 12, CY + 4, "전용 포트", 12, INK, KR, "end", 600)
d.t(CX + TIPX + 12, CY + 4, "443 공유", 12, INK, KR, "start", 600)

CELLS = [  # (열, 행, 모서리 태그, 제목, 설명 두 줄, focal)
    (0, 0, "01 · 암호화 / 전용 포트", "DoT",             ["TCP 853 · TLS 로 감쌈", "포트로 가려냄 · 내용은 못 읽음"], False),
    (1, 0, "02 · 암호화 / 443 공유",  "DoH",             ["TCP 443 · HTTPS 안의 DNS", "일반 웹 트래픽과 같은 포트"],   False),
    (0, 1, "03 · 평문 / 전용 포트",   "UDP 53 · TCP 53", ["전송만 다름 · 둘 다 평문", "dns 필터로 질의 이름이 읽힘"], True),
    (1, 1, "04 · 평문 / 443 공유",    "해당 없음",        ["DoH 는 https URI 로만 실림", "RFC 8484"],                 False),
]
for col, row, tag, title, lines, focal in CELLS:
    x = CX + GAP if col else CX - GAP - CW
    y = CY + GAP if row else CY - GAP - CH
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 6)
        c = INK if title != "해당 없음" else MUTED
    d.t(x + 16, y + 24, tag, 12, ACC if focal else SOFT, KR, "start", 600)
    d.t(x + 16, y + 60, title, 16, c, kr(title), "start", 600)
    for k, ln in enumerate(lines):
        d.t(x + 16, y + 92 + k * 22, ln, 12, MUTED, kr(ln), "start")

d.legend(H - 56, [("전송이 달라도 같은 칸", ACC)])
d.save("05-02.dns-transport-crypto.svg")
