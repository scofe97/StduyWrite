# 05-01 학습 목표 뒤 전체 지도 — 절 다섯을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 칸이 실사용자에게 영향이 0인 유일한 기법".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes·§2 공식 대신 카드 한 줄 stride 로 놓는다(03-01·04-01 과 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

# 폭은 계약의 본문 삽입용 상한(880~1000) 안으로 두고, 4 열을 2 열로 접어 담는다.
# 계약: "넓은 캔버스에 담기지 않으면 폭을 늘리지 말고 배치를 바꾼다."
COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "배포와 릴리스를 다시 가른다", "블루/그린은 왜 여전히 빅뱅인가"),
    ("§2", "요청 내용으로 고르는 다크 런치", "subset · 헤더 매칭 · gateways: mesh"),
    ("§3", "가중치로 나누는 전환과 Flagger", "10/90 → 50/50 → 자동화"),
    ("§4", "응답을 버리는 복제 — 미러링", "실사용자 영향 0 · -shadow"),
    ("§5", "나가는 문 — REGISTRY_ONLY", "심층 방어 · ServiceEntry"),
]
FOCAL = 3
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · 05-01",
      "위험에 노출되는 트래픽을 줄여 가는 순서 — 읽는 순서",
      "5장 노트의 절 다섯을 읽는 순서로 이은 지도. 앞 넷이 새 코드가 해칠 수 있는 실사용자 트래픽의 몫을 한 단계씩 줄이고, 마지막이 방향을 뒤집어 나가는 트래픽을 다룬다.",
      "§2 → §3 → §4 로 갈수록 실사용자에게 닿는 위험이 줄고, §4 에서 0 이 됩니다")

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

d.legend(LEGY, [("실사용자 영향이 0인 기법", ACC)])
d.save("05-01.chapter-overview.svg")
