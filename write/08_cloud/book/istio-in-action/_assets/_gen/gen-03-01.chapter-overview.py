# 03-01 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 본문이 "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 마지막 칸이 이 장의 결론" 이라고 못 박는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례). 데이터 칩도 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "ISTIO IN ACTION · 03-01",
      "Envoy가 맡는 일과 Istio가 보태는 일 — 읽는 순서",
      "3장 노트의 절 일곱을 읽는 순서로 이은 지도. 앞 여섯 절이 Envoy 하나를 벗기고 마지막 절이 Istio가 그 위에 무엇을 보태는지로 닫는다.",
      "앞 여섯 칸은 Envoy 하나를 벗기는 순서이고, 마지막 칸이 Istio 쪽으로 넘어가는 결론입니다")

CW, CH, GAP, X0 = 272, 96, 24, 40          # stride = CW + GAP = 296
Y1, Y2 = 104, 248                          # 두 줄. 사이 corridor 224
cards = [
    ("§1", "프록시가 가운데 서면", "왜 하필 Envoy인가"),
    ("§2", "요청이 Envoy를 지나는 길", "Listener · Route · Cluster"),
    ("§3", "맡는 것과 앱에 남는 것", "\"코드 변경 없이\"의 예외 둘"),
    ("§4", "다른 프록시와 견주면", "강점 일곱과 그 이유"),
    ("§5", "정적 설정과 xDS", "순서 경쟁과 ADS"),
    ("§6", "정적 설정으로 Envoy 띄우기", "헤더 · Admin API · 재시도"),
    ("§7", "Envoy를 부양하는 것", "저자가 든 부양 예 넷"),
]

def pos(i):
    if i < 4: return X0 + i * (CW + GAP), Y1
    return X0 + (i - 4) * (CW + GAP), Y2

def card(i, focal=False):
    x, y = pos(i); n, title, q = cards[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 52, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 76, q, 12, MUTED, KR, "start")

# 연결선을 먼저 — z-order
for i in range(6):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:   # 줄바꿈: 아래로 → corridor → 왼쪽 → 아래로
        cx1, cx2 = x1 + CW / 2, x2 + CW / 2
        d.path(f"M {cx1} {y1 + CH} V 224 H {cx2} V {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(7):
    card(i, focal=(i == 6))

d.legend(376, [("이 장의 결론", ACC)])
d.save("03-01.chapter-overview.svg")
print("h 필요:", 376 + 22 + 16, " 실제:", H)
