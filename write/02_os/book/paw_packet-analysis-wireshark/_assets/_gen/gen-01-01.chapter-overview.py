# 01-01 학습 목표 뒤 전체 지도 — 절 넷을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 이름 · 그 절이 답하는 질문)이 반복되고
#           화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로
#           놓는다 (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례). 데이터 칩 없음.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 396
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01",
      "패킷 분석기와 Wireshark — 읽는 순서",
      "1장 노트의 절 넷을 읽는 순서로 이은 지도. 분석기가 서는 자리에서 출발해 Wireshark 의 구성과 캡처 전 관문을 지나, 이 도구가 못 하는 일로 닫는다.",
      "앞 세 칸이 왜 이 도구인지를 잇고, 마지막 칸이 이 도구의 경계로 닫습니다")

CW, CH, GAP, X0 = 400, 100, 24, 24       # stride = CW + GAP = 424
Y1, Y2 = 112, 244                        # 두 줄. 사이 corridor 32
cards = [
    ("§1", "애플리케이션 로그가 침묵할 때", "선에서 프레임을 뜨면 무엇이 더 보이나"),
    ("§2", "Wireshark 는 무엇 위에 서 있나", "libpcap · dumpcap · tshark 의 분업"),
    ("§3", "캡처 전에 통과할 다섯 관문", "정책 · OS 지원 · promiscuous · monitor"),
    ("§4", "Wireshark 가 못 하는 일", "편집 · 재생 · 모바일은 다른 도구로"),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), (Y1 if i < 2 else Y2)

def card(i, focal=False):
    x, y = pos(i); n, title, q = cards[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 30, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 58, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 82, q, 13, MUTED, KR, "start")

# 연결선을 먼저 — z-order
for i in range(3):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:                                   # 같은 줄: 오른쪽으로
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 4, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:                                          # 줄바꿈: 아래 corridor 를 타고 왼쪽으로
        cy = Y1 + CH + 16
        d.path(f"M {x1 + CW / 2} {y1 + CH} V {cy} H {X0 + CW / 2} V {y2 - 4}",
               MUTED, 1.4, m="ar")

for i in range(4):
    card(i, focal=(i == 3))

d.save("01-01.chapter-overview.svg")
