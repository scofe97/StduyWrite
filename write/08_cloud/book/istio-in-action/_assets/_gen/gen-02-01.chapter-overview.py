# 02-01 본문 정리 앞 전체 지도 — 절 넷을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 칸이 이 장의 결론이 놓이는 자리".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(03~09 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 452
d = D(W, H, "ISTIO IN ACTION · 02-01",
      "배포와 릴리스를 가르는 첫 실습 — 읽는 순서",
      "2장 노트의 절 다섯을 읽는 순서로 이은 지도. 앞의 네 절이 무엇이 서고 무엇을 대신 지는지를 "
      "세우고, 마지막 절이 그것으로 무엇을 하려 했는지를 낱말 둘로 가른다.",
      "앞의 넷은 준비이고 §5 가 이 장이 세우려는 구분입니다")

CW, CH, GAP, X0 = 280, 96, 16, 36
Y1, Y2 = 104, 248
cards = [
    ("§1", "설치가 남기는 것", "데이터 플레인은 아직 없다"),
    ("§2", "컨트롤 플레인의 아홉 책임", "무엇을 위임하게 되는가"),
    ("§3", "의도에서 Envoy 설정까지", "누가 낮은 수준을 쓰는가"),
    ("§4", "블랙박스 관측의 경계", "코드 변경 없이가 어디까지"),
    ("§5", "배포와 릴리스를 가른다", "누가 첫 시험대에 서는가"),
]
def pos(i):
    if i < 3: return X0 + i * (CW + GAP), Y1
    return X0 + (i - 3) * (CW + GAP), Y2
def card(i, focal=False):
    x, Y = pos(i); n, title, q = cards[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 52, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 76, q, 11, MUTED, KR, "start")
for i in range(4):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} 224 L {x2 + CW / 2} 224 L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(5):
    card(i, focal=(i == 4))
d.legend(396, [("이 장이 세우려는 구분", ACC)])
d.save("02-01.chapter-overview.svg")
