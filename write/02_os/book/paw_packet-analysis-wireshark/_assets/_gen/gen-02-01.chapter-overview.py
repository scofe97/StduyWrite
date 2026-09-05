# 02-01 학습 목표 뒤 전체 지도 — 절 일곱을 캡처 순서대로 잇는다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 이름 · 그 절이 답하는 것)이 반복되고
#           화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 592
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-01",
      "패킷을 잡는 법 — 읽는 순서",
      "2장 캡처 축 노트의 절 일곱을 캡처가 실제로 진행되는 순서로 이은 지도. 시작 화면에서 출발해 인터페이스와 옵션을 지나 필터·파일 분할로 가고, GUI 가 없는 환경과 안 잡힐 때로 닫는다.",
      "네 번째 칸이 이 편의 중심입니다 — 여기서 버린 패킷은 뒤에서 되살릴 수 없습니다")

CW, CH, GAP, X0 = 400, 80, 24, 24        # stride = CW + GAP = 424
ROW = 112                                 # 행 stride. 카드 사이 corridor 32
Y0 = 112
cards = [
    ("§1", "시작 화면의 네 갈래",        "어디로 들어가도 같은 캡처에 닿습니다"),
    ("§2", "인터페이스 이름이 알려주는 것", "eth0 · lo0 · en0 · wlan0 가 뜻하는 것"),
    ("§3", "무엇을 얼마나 담을지",        "promiscuous · snaplen · 이름 해석"),
    ("§4", "캡처 필터는 디스크 앞에 섭니다", "BPF 문법 · 버린 것은 안 돌아옵니다"),
    ("§5", "오래 잡을 때 파일을 자릅니다",  "개수 · 크기 · 시간 · 벽시계 기준"),
    ("§6", "Wireshark 가 없는 서버에서",   "tcpdump 와 snoop 로 떠서 가져옵니다"),
    ("§7", "패킷이 안 보일 때",           "인터페이스인지 권한인지 먼저 가릅니다"),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), Y0 + (i // 2) * ROW

def card(i, focal=False):
    x, y = pos(i); n, title, q = cards[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 50, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 70, q, 12, MUTED, KR, "start")

for i in range(6):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 4, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        cy = y1 + CH + 16
        d.path(f"M {x1 + CW / 2} {y1 + CH} V {cy} H {X0 + CW / 2} V {y2 - 4}",
               MUTED, 1.4, m="ar")

for i in range(7):
    card(i, focal=(i == 3))

d.save("02-01.chapter-overview.svg")
