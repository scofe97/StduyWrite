# 02-02 학습 목표 뒤 전체 지도 — 절 다섯을 화면을 읽어 내려가는 순서로 잇는다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 이름 · 그 절이 답하는 것)이 반복되고
#           화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 480
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-02",
      "잡은 패킷을 읽는 법 — 읽는 순서",
      "2장 분석 축 노트의 절 다섯을 화면을 읽어 내려가는 순서로 이은 지도. 네 개 창의 관계에서 출발해 색과 필터로 범위를 좁히고, 목록 한 줄과 그 안의 계층으로 내려간다.",
      "세 번째 칸이 이 편의 중심입니다 — 필터는 지우지 않고 시야만 좁힙니다")

CW, CH, GAP, X0 = 400, 80, 24, 24
ROW, Y0 = 112, 112
cards = [
    ("§1", "네 개 창이 보는 같은 바이트",  "목록 · 계층 · 바이트가 겹쳐 있습니다"),
    ("§2", "색이 먼저 말해 줍니다",        "컬러링 규칙으로 눈에 먼저 걸립니다"),
    ("§3", "디스플레이 필터",             "지우지 않고 시야만 좁힙니다"),
    ("§4", "Packet List 의 일곱 열",      "한 줄이 답하는 것과 시간 기준"),
    ("§5", "Packet Details 의 계층",      "frame 부터 응용 계층까지 벗겨 내려갑니다"),
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

for i in range(4):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 4, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        cy = y1 + CH + 16
        d.path(f"M {x1 + CW / 2} {y1 + CH} V {cy} H {X0 + CW / 2} V {y2 - 4}",
               MUTED, 1.4, m="ar")

for i in range(5):
    card(i, focal=(i == 2))

d.save("02-02.chapter-overview.svg")
