# 03-01 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 본문이 "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 마지막 칸이 이 장의 결론" 이라고 못 박는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례). 데이터 칩도 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

# 폭은 계약의 본문 삽입용 상한(880~1000) 안으로 두고, 4 열을 2 열로 접어 담는다.
# 계약: "넓은 캔버스에 담기지 않으면 폭을 늘리지 말고 배치를 바꾼다."
COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "프록시가 가운데 서면", "왜 하필 Envoy인가"),
    ("§2", "요청이 Envoy를 지나는 길", "Listener · Route · Cluster"),
    ("§3", "맡는 것과 앱에 남는 것", "\"코드 변경 없이\"의 예외 둘"),
    ("§4", "다른 프록시와 견주면", "강점 일곱과 그 이유"),
    ("§5", "정적 설정과 xDS", "순서 경쟁과 ADS"),
    ("§6", "정적 설정으로 Envoy 띄우기", "헤더 · Admin API · 재시도"),
    ("§7", "Envoy를 부양하는 것", "저자가 든 부양 예 넷"),
]
FOCAL = 6
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · 03-01",
      "Envoy가 맡는 일과 Istio가 보태는 일 — 읽는 순서",
      "3장 노트의 절 일곱을 읽는 순서로 이은 지도. 앞 여섯 절이 Envoy 하나를 벗기고 마지막 절이 Istio가 그 위에 무엇을 보태는지로 닫는다.",
      "앞 여섯 칸은 Envoy 하나를 벗기는 순서이고, 마지막 칸이 Istio 쪽으로 넘어가는 결론입니다")

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

d.legend(LEGY, [("이 장의 결론", ACC)])
d.save("03-01.chapter-overview.svg")
