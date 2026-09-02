# 14-01 본문 정리 앞 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 것 하나", "색이 붙은 칸이 저자가 유리를 깬다고 표현한 자리".
# 원문 14.2 가 EnvoyFilter 를 "a 'break glass' solution" 이라 부른다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~13 과 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 452
d = D(W, H, "ISTIO IN ACTION · 14-01",
      "확장의 네 문을 여는 순서 — 읽는 순서",
      "14 장 노트의 절 여덟을 읽는 순서로 이은 지도. 앞의 둘이 피하려는 것과 구조를 세우고, "
      "뒤의 여섯이 네 개의 문을 차례로 연다.",
      "문마다 무엇이 내 일이 되는지가 이 장을 읽는 축입니다")

CW, CH, GAP, X0 = 280, 96, 16, 36
Y1, Y2 = 104, 248
cards = [
    ("§1", "네 개의 문", "무엇을 피하려 하는가"),
    ("§2", "필터 안의 필터", "확장은 어디에 꽂히는가"),
    ("§3", "유리를 깨는 손잡이", "어느 좌표를 겨냥하는가"),
    ("§4", "밖으로 빼는 판정", "왜 전역이어야 하는가"),
    ("§5", "두 설정이 만나는 값", "누가 헤더를 값으로 바꾸는가"),
    ("§6", "심는 스크립트", "왜 아무 라이브러리나 못 쓰는가"),
    ("§7", "새로 만드는 필터", "두 단점을 어떻게 푸는가"),
    ("§8", "선언으로 올린다", "무엇을 대신 치렀는가"),
]
FOCAL = 2
def pos(i):
    if i < 4: return X0 + i * (CW + GAP), Y1
    return X0 + (i - 4) * (CW + GAP), Y2
def card(i):
    x, Y = pos(i); n, title, q = cards[i]; focal = (i == FOCAL)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 52, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 76, q, 11, MUTED, KR, "start")
for i in range(7):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} 224 L {x2 + CW / 2} 224 L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(8):
    card(i)
d.legend(396, [("저자가 유리를 깬다고 표현한 자리", ACC)])
d.save("14-01.chapter-overview.svg")
