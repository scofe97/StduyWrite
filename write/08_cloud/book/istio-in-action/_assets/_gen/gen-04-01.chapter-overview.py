# 04-01 학습 목표 뒤 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 칸이 이 장의 논지가 서는 자리".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes·§2 공식 대신 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 관례). 03-01 개요와 같은 stride·여백.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

# 폭은 계약의 본문 삽입용 상한(880~1000) 안으로 두고, 4 열을 2 열로 접어 담는다.
# 계약: "넓은 캔버스에 담기지 않으면 폭을 늘리지 말고 배치를 바꾼다."
COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "진입점 앞의 두 장치", "가상 IP · 가상 호스팅"),
    ("§2", "문을 여는 일과 길을 내는 일", "Gateway · VirtualService · blackhole"),
    ("§3", "Ingress · API 게이트웨이와 견주면", "L4·L5 와 L7 을 가른 이유"),
    ("§4", "TLS 세 모드와 하나의 리다이렉트", "SIMPLE · MUTUAL · SNI"),
    ("§5", "TCP와 SNI 패스스루", "종료하지 않고 통과시킨다"),
    ("§6", "운영에서 내리는 네 가지 판단", "쪼개기 · 주입 · 로그 · 설정 크기"),
]
FOCAL = 2
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · 04-01",
      "문을 여는 일과 길을 내는 일을 가른다 — 읽는 순서",
      "4장 노트의 절 여섯을 읽는 순서로 이은 지도. 앞 둘이 진입점과 두 리소스를 놓고, 셋째에서 L4·L5 와 L7 을 가른 이유가 서며, 뒤 셋이 TLS·TCP·운영 판단이다.",
      "셋째 칸에서 이 장의 논지가 서고, 뒤 세 칸은 그 문에 무엇을 다는가입니다")

def pos(i):
    r, c = divmod(i, COLS)
    return X0 + c * (CW + GAP), Y0 + r * (CH + VGAP)

for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        my = y1 + CH + VGAP / 2
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {my} "
               f"L {x2 + CW / 2} {my} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")

for i, (num, title, q) in enumerate(cards):
    x, y = pos(i); focal = (i == FOCAL)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 28, num, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 56, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 82, q, 12, MUTED, KR, "start")

d.legend(LEGY, [("이 장의 논지", ACC)])
d.save("04-01.chapter-overview.svg")
