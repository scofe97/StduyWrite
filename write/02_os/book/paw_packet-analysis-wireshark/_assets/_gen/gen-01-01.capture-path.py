# 01-01 §1 — 받은 프레임이 드라이버 위에서 두 갈래로 올라가고, 분석기는 그 갈림 자리에서 사본을 받는다.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준 다섯. 아래로 갈수록 선에 가깝다.
#           focal 은 분석기가 실제로 서는 층 하나(패킷 소켓 · BPF).
#           축약: 스펙의 층 한 줄(이름 · 서브라벨) 대신 층 안에 두 열의 노드를 둔다 — 왼쪽 열이 정상 경로,
#           오른쪽 열이 분석기 경로다. 둘을 한 장에 세워야 "소켓 API 아래 · 드라이버 위" 와
#           §2 의 GUI · tshark · dumpcap · libpcap 분업이 같은 층 위에서 읽힌다.
#           층 번호는 OSI 계층 번호(L2 · L3)와 섞이지 않게 L 접두어 없이 아래에서부터 01~05 로 적는다.
#           본문 "위 그림의 다섯 층 가운데 … 아래에서 두 번째, 커널의 패킷 소켓 층" 이 층 수와 위치를 고정한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 568
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §1",
      "분석기가 가로채는 층",
      "받은 프레임이 NIC 드라이버 위에서 두 갈래로 올라가는 다섯 층. 왼쪽 정상 경로는 커널 프로토콜 스택이 헤더를 벗긴 뒤 소켓 API 로 올리고, 오른쪽 분석기 경로는 그 아래 패킷 소켓 · BPF 에서 프레임 사본을 받아 libpcap 과 dumpcap 을 거쳐 GUI · tshark 로 간다.",
      "왼쪽이 애플리케이션이 받는 길, 오른쪽이 분석기가 받는 길입니다 — 둘은 프로토콜 스택보다 아래에서 갈라집니다")

LX, LW, LH = 80, 776, 72                  # 층 x · 폭 · 높이. stride = LH (스타일 계약: 폭 880 에서 12px 가 1.36%)
Y0 = 136
NH = 48                                   # 노드 높이 — 층 안 위아래 여백 12
LCX, LNX, LNW = 272, 144, 256             # 왼쪽 열: 중심 · x · 폭
RCX, RNX, RNW = 544, 464, 160             # 오른쪽 열: 중심 · x · 폭
GX, GW = 672, 168                         # 05 층의 GUI · tshark
BOUNDARY = Y0 + 2 * LH                    # 04 과 03 사이 — 사용자 공간 / 커널

def band_y(i): return Y0 + i * LH         # i=0 이 맨 위(05), i=4 가 맨 아래(01)
def node_y(i): return band_y(i) + (LH - NH) / 2
def mid(i): return band_y(i) + LH / 2

# 층 다섯 — focal 은 02(i=3) 하나
for i in range(5):
    y = band_y(i)
    if i == 3:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 1.0, 6)
    d.t(LX + 16, y + 40, f"0{5 - i}", 9, ACC if i == 3 else SOFT, MONO, "start", 600)

# 열 머리
d.t(LCX, Y0 - 12, "정상 경로", 12, SOFT, KR, "middle", 600)
d.t((RNX + GX + GW) / 2, Y0 - 12, "분석기 경로", 12, SOFT, KR, "middle", 600)

# 사용자 공간 / 커널 경계
d.line(12, BOUNDARY, LX + LW, BOUNDARY, SOFT, 1.0, dash="4,3")
d.t(12, Y0 + 28, "사용자", 11, SOFT, KR, "start")
d.t(12, Y0 + 46, "공간", 11, SOFT, KR, "start")
d.t(12, BOUNDARY + 28, "커널", 11, SOFT, KR, "start")

# 연결선을 먼저 — 받는 방향이라 화살표가 위를 향한다
# 정상 경로: 드라이버 → (02 에서 갈림) → 프로토콜 스택 → 소켓 API → 애플리케이션
d.arrow([(LCX, node_y(4)), (LCX, node_y(2) + NH + 4)], MUTED, "ar", 1.4)
d.arrow([(LCX, node_y(2)), (LCX, node_y(1) + NH + 4)], MUTED, "ar", 1.4)
d.arrow([(LCX, node_y(1)), (LCX, node_y(0) + NH + 4)], MUTED, "ar", 1.4)
# 분석기 경로: 갈림점 → 패킷 소켓 · BPF → (스택 우회) → libpcap → dumpcap → GUI · tshark
d.arrow([(LCX + 4, mid(3)), (RNX - 4, mid(3))], INFO, "info", 1.4)
d.arrow([(RCX, node_y(3)), (RCX, node_y(1) + NH + 4)], INFO, "info", 1.4)
d.arrow([(RCX, node_y(1)), (RCX, node_y(0) + NH + 4)], INFO, "info", 1.4)
d.arrow([(RNX + RNW, mid(0)), (GX - 4, mid(0))], INFO, "info", 1.4)
d.o.append(f'<circle cx="{LCX}" cy="{mid(3)}" r="4" fill="{INFO}"/>')

def node(x, i, w, title, sub, c=INK):
    y = node_y(i)
    d.box(x, y, w, NH, PAPER2 if i != 3 else PAPER, RULE, 1.0, 6)
    d.t(x + w / 2, y + 20, title, 14, c, KR, "middle", 600)
    d.t(x + w / 2, y + 38, sub, 12, MUTED, KR)

node(LNX, 0, LNW, "애플리케이션", "curl · 브라우저 · 서버 프로세스")
node(LNX, 1, LNW, "소켓 API", "socket() · read() · write()")
node(LNX, 2, LNW, "커널 프로토콜 스택", "이더넷 · IP · TCP 헤더 제거")
node(RNX, 0, RNW, "dumpcap", "캡처 엔진")
node(GX, 0, GW, "GUI · tshark", "해독 · 표시")
node(RNX, 1, RNW, "libpcap · Npcap", "캡처 라이브러리")
node(RNX, 3, RNW, "패킷 소켓 · BPF", "프레임 사본", ACC)
node(LNX, 4, GX + GW - LNX, "NIC 드라이버 · 물리 인터페이스", "en0 · eth0 · 선")

d.t(RCX + 12, mid(2) + 4, "스택 우회", 12, INFO, KR, "start")
d.t(LCX + 12, mid(3) + 22, "사본 분기", 12, INFO, KR, "start")

d.legend(Y0 + 5 * LH + 24, [("분석기가 서는 층", ACC), ("프레임 사본 경로", INFO)])
d.save("01-01.capture-path.svg")
