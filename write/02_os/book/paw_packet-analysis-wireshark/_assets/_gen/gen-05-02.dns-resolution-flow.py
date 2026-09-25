# 05-02 §1 — 이름 하나를 풀 때 질의가 누구를 거치고, 그중 어느 구간이 클라이언트 캡처에 잡히는가.
# 본문 요구: "앱이 이름을 물으면 OS 안의 stub 리졸버가 재귀 리졸버에 질의를 보냅니다(2). 재귀 리졸버는 캐시를
#            먼저 보고(3), 없으면 루트·TLD·권한 서버를 차례로 물어 위임을 따라갑니다(4). 응답은 RA 를 켜고
#            돌아옵니다(5). 클라이언트에서 잡은 캡처에는 2단계와 5단계 두 줄뿐입니다."
#            논지가 순서보다 경계(캡처 지점 안팎)라서 시퀀스 대신 존으로 나눈 노드 그래프로 그린다
#            (visual-diagram-selection 「주고받는 흐름은 논지로 시퀀스와 노드 그래프를 가른다」).
# 타입 스펙: type-architecture — 클라이언트 PC 존과 인터넷 존, 그 경계의 캡처 지점. 재귀 리졸버에서 서버 셋으로
#           가는 별 모양 연결은 직각 경로. 번호 칩은 본문 다섯 단계와 같다. focal(accent)은 캡처에 찍히는 두 줄.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 576
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §1",
      "이름 하나가 풀리는 길",
      "클라이언트 PC 안에서 앱이 stub 리졸버에 이름을 넘기면(1), stub 은 캡처 지점을 지나 재귀 리졸버에 RD=1 질의를 "
      "보낸다(2). 재귀 리졸버는 캐시를 먼저 보고(3), 없으면 루트, TLD, 권한 서버를 차례로 물어 위임을 따라간다(4). "
      "권한 서버의 답은 TTL 동안 캐시에 남고, 재귀 리졸버는 RA=1 응답을 돌려준다(5). 클라이언트 캡처에 찍히는 것은 2와 5뿐이다.",
      "클라이언트 PC 에서 잡으면 2 와 5 만 보이고, 4 는 재귀 리졸버 너머에서 오갑니다")

ZONE = "rgba(245,245,245,0.22)"

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.03)" '
               f'stroke="{ZONE}" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 20, label, 11, MUTED, KR, "start", 600)

def node(x, y, w, h, name, sub, c=None):
    d.box(x, y, w, h)
    d.t(x + w / 2, y + 24, name, 13, INK, KR, "middle", 600)
    if sub:
        fam = KR if any("가" <= ch <= "힣" for ch in sub) else MONO
        d.t(x + w / 2, y + 44, sub, 11, c or MUTED, fam)

# 존 — 경계가 이 도식의 논지다
zone(24, 200, 328, 216, "클라이언트 PC")
zone(436, 112, 500, 360, "인터넷 · 클라이언트 캡처에 안 보이는 구간")

# 캡처 지점 — 두 존 사이
CX = 386
d.line(CX, 176, CX, 480, ACC, 1.4, "4 4")
d.t(CX, 164, "캡처 지점", 12, ACC, KR, "middle", 600)
d.t(CX, 496, "클라이언트 NIC", 11, MUTED, KR, "middle")

# 연결을 먼저 그려 상자 뒤로 보낸다
# 1 · 5 — 앱 ↔ stub (선에 안 나감)
d.arrow([(160, 292), (204, 292)], MUTED, "ar", 1.3)
d.arrow([(204, 308), (164, 308)], MUTED, "ar", 1.0, "4 3")
d.chip(182, 272, "1", MUTED)
# 2 · 5 — stub ↔ 재귀 리졸버 (캡처에 찍힘)
d.arrow([(320, 292), (448, 292)], ACC, "acc", 1.6)
d.arrow([(452, 308), (324, 308)], ACC, "acc", 1.4, "4 3")
d.t(411, 282, "RD=1", 11, ACC, MONO, "middle", 600)
d.t(411, 326, "RA=1", 11, ACC, MONO, "middle", 600)
d.chip(338, 272, "2", ACC)
d.chip(338, 328, "5", ACC)

# 4 — 재귀 리졸버 ↔ 루트·TLD·권한 (직각 경로, 요청 실선 · 응답 점선)
RX = 600          # 재귀 리졸버 오른쪽 변
SX = 728          # 서버 상자 왼쪽 변
d.path(f"M {RX} 256 H 648 V 172 H {SX - 2}", INFO, 1.4, m="info")
d.path(f"M {SX} 188 H 664 V 268 H {RX + 2}", MUTED, 1.0, m="ar", dash="4 3")
d.path(f"M {RX} 294 H {SX - 2}", INFO, 1.4, m="info")
d.path(f"M {SX} 306 H {RX + 2}", MUTED, 1.0, m="ar", dash="4 3")
d.path(f"M {RX} 344 H 648 V 428 H {SX - 2}", INFO, 1.4, m="info")
d.path(f"M {SX} 412 H 664 V 332 H {RX + 2}", OK, 1.2, m="ok", dash="4 3")
for y, dy in ((172, -14), (294, -14), (428, 14)):
    d.chip(700, y + dy, "4", INFO)

# 상자
node(48, 272, 112, 56, "앱", "getaddrinfo()")
node(208, 272, 112, 56, "stub 리졸버", "OS 안")
node(452, 232, 148, 136, "재귀 리졸버", "8.8.8.8 · ISP")
d.tone(464, 300, 124, 52, WARN, 6, op="10", sw=1.1)
d.t(526, 322, "3 · 캐시 · TTL 동안", 11, WARN, KR, "middle", 600)
d.t(526, 340, "적중 시 4 생략", 11, MUTED, KR, "middle")
node(SX, 144, 184, 60, "루트 서버", "위임 · com. NS")
node(SX, 272, 184, 60, "TLD 서버 · com.", "위임 · google.com. NS")
node(SX, 392, 184, 60, "권한 서버 · google.com.", "A 레코드 · TTL", OK)

d.legend(H - 48, [("캡처에 찍히는 질의·응답", ACC), ("재귀 리졸버가 대신 묻는 질의", INFO),
                  ("권한 있는 답", OK), ("재귀 리졸버의 캐시", WARN)])
d.save("05-02.dns-resolution-flow.svg")
