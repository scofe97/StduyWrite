# 01-01 §2 — Wireshark 설치본이 실제로는 프로그램 여럿이라는 것, 그리고 캡처를 누가 하는가.
# 타입 스펙: type-architecture — 시스템의 구성요소와 연결. 위에서 아래로 한 방향 흐름을 잡고,
#           focal 은 캡처를 실제로 수행하는 dumpcap 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 568
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §2",
      "Wireshark 설치본의 구성",
      "GUI 와 tshark 는 앞단이고 캡처 자체는 dumpcap 이 맡는다. dumpcap 은 libpcap 을 거쳐 커널 패킷 소켓에 닿고, 결과를 pcapng 파일로 남긴다.",
      "화살표 방향이 캡처 경로이고, 점선은 저장된 파일을 다시 여는 오프라인 경로입니다")

def node(x, y, w, h, title, sub, focal=False, c=None):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, w, h, c, 8)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    col = ACC if focal else (c if c else INK)
    d.t(x + w / 2, y + 26, title, 14, col, KR, "middle", 600)
    d.t(x + w / 2, y + 46, sub, 12, MUTED, MONO)

CX, BW, BH = 280, 280, 60                 # 본 열: 중심 280, 폭 280 → x 140..420
BX = CX - BW / 2
Y_GUI, Y_DUMP, Y_PCAP, Y_KERN = 128, 248, 344, 440
TX, TW = 500, 200                         # tshark
FX, FW = 560, 220                         # pcapng 파일

# 연결선을 먼저 — z-order 가 상자를 위에 올린다
d.arrow([(CX, Y_GUI + BH), (CX, Y_DUMP - 4)], MUTED, "ar", 1.4)
d.path(f"M {TX + TW / 2} {Y_GUI + BH} V {Y_DUMP - 32} H {CX + 80} V {Y_DUMP - 4}",
       MUTED, 1.4, m="ar")
d.arrow([(CX, Y_DUMP + BH), (CX, Y_PCAP - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_PCAP + BH), (CX, Y_KERN - 4)], MUTED, "ar", 1.4)
d.arrow([(BX + BW, Y_DUMP + BH / 2), (FX - 4, Y_DUMP + BH / 2)], MUTED, "ar", 1.4)
d.path(f"M {FX + FW / 2} {Y_DUMP} V 104 H {CX} V {Y_GUI - 4}",
       INFO, 1.0, m="info", dash="4,3")

node(BX, Y_GUI, BW, BH, "Wireshark GUI", "표시 · 분석 · 통계")
node(TX, Y_GUI, TW, BH, "tshark", "CLI · 원격 터미널")
node(BX, Y_DUMP, BW, BH, "dumpcap", "캡처 엔진 · 단독 실행 가능", focal=True)
node(BX, Y_PCAP, BW, BH, "libpcap · Npcap", "캡처 라이브러리")
node(BX, Y_KERN, BW, BH, "커널 패킷 소켓 · NIC", "en0 · eth0")
node(FX, Y_DUMP, FW, BH, "pcapng 파일", "저장 · 재분석", c=INFO)

d.t(CX + 92, Y_DUMP - 40, "캡처 위임", 11, MUTED, KR, "start")
d.t(CX + 200, Y_GUI - 32, "오프라인 읽기", 11, INFO, KR, "middle")

d.legend(520, [("캡처를 수행하는 프로그램", ACC), ("저장된 파일", INFO)])
d.save("01-01.wireshark-stack.svg")
