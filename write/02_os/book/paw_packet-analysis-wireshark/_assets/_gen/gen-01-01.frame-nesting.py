# 01-01 §1 「그래서 아래 층을 봅니다」 — 이더넷 프레임이 IP 패킷을 담는 포함 관계와, 그중 누가 어디까지 받는가.
# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. 바깥부터 이더넷 프레임 → IP 패킷 → TCP 세그먼트 → 페이로드.
#           "MAC 다음이 IP" 라는 순차 감각을 겹 구조로 바로잡는 것이 목적이라 링을 가로로 겹친다.
#           축약: 링 라벨을 스펙의 mono eyebrow 대신 한글 이름 + 디섹터 이름(Ethernet II · IPv4 · TCP) 한 줄로
#           쓴다 — tshark -V 출력의 줄 이름과 이어 읽게 하려는 것이다. 헤더 칸은 각 링의 왼쪽, FCS 는 바깥
#           링의 오른쪽에 둔다. 링 밖 아래의 범위 막대 둘은 계층의 일부가 아니라 x 정렬로 읽는 주석이다.
#           focal 은 가장 안쪽 링이 아니라 분석기가 받는 범위 막대 — 이 소절의 논점이 "누가 어디까지 받나" 다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 512
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §1",
      "프레임이 패킷을 담는 모양",
      "이더넷 프레임 안에 IP 패킷, 그 안에 TCP 세그먼트, 그 안에 페이로드가 들어 있는 포함 관계. 패킷 분석기는 이더넷 헤더부터 페이로드까지 받고 끝의 FCS 는 대개 전달받지 못하며, 애플리케이션에는 페이로드만 올라간다.",
      "IP 헤더는 MAC 주소 다음 칸이 아니라 프레임 몸통 안에 있습니다 — 분석기는 바깥 봉투째 받습니다")

# 링: 위 32(이름 자리) · 아래 16 · 좌우 16 씩 일정하게 들여쓴다. 모든 좌표 4 의 배수.
RINGS = [  # (이름, x, y, w, h)
    ("이더넷 프레임 · Ethernet II", 24, 112, 832, 224),
    ("IP 패킷 · IPv4",              176, 144, 560, 176),
    ("TCP 세그먼트 · TCP",           320, 176, 400, 128),
]
for i, (name, x, y, w, h) in enumerate(RINGS):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" fill-opacity="{0.25 + i * 0.2:.2f}" '
               f'stroke="{RULE}" stroke-opacity="{["0.45", "0.70", "1"][i]}" stroke-width="1.1"/>')
    d.t(x + 16, y + 22, name, 13, [SOFT, MUTED, INK][i], KR, "start", 600)

def cell(x, y, w, h, title, subs, c=None):
    if c:
        d.tone(x, y, w, h, c, 6)
    else:
        d.box(x, y, w, h, PAPER, RULE, 1.0, 6)
    ty = y + h / 2 - 8 * len(subs)
    d.t(x + w / 2, ty, title, 13, c if c else INK, KR, "middle", 600)
    for k, s in enumerate(subs):
        d.t(x + w / 2, ty + 20 + 18 * k, s, 12, MUTED, KR)

cell(40, 144, 120, 176, "이더넷 헤더", ["목적지 MAC", "출발지 MAC"])
cell(192, 176, 112, 128, "IP 헤더", ["출발지 IP", "목적지 IP"])
cell(336, 208, 104, 80, "TCP 헤더", ["포트 · 플래그"])
cell(456, 208, 248, 80, "페이로드", ["애플리케이션 데이터"], c=INFO)
cell(752, 144, 88, 176, "FCS", ["오류 검사"])

# 범위 막대 — 링 경계와 x 를 맞춘다
BA_Y, BB_Y, BH = 360, 408, 32
d.o.append(f'<rect x="40" y="{BA_Y}" width="696" height="{BH}" rx="4" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(56, BA_Y + 21, "분석기가 받는 범위 · 이더넷 헤더부터 페이로드까지", 13, ACC, KR, "start", 600)
d.o.append(f'<rect x="752" y="{BA_Y}" width="88" height="{BH}" rx="4" '
           f'fill="none" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4,3"/>')
d.t(796, BA_Y + 21, "대개 빠짐", 12, SOFT, KR, "middle")
d.tone(456, BB_Y, 248, BH, INFO, 4)
d.t(580, BB_Y + 21, "애플리케이션이 받는 범위", 12, INFO, KR, "middle", 600)

d.legend(464, [("분석기가 받는 범위", ACC), ("애플리케이션이 받는 범위", INFO)])
d.save("01-01.frame-nesting.svg")
