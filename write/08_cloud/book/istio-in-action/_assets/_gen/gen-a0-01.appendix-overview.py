# a0-01 본문 정리 앞 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 본문: "절 다섯이 좁은 데서 넓은 데로 갑니다", "마지막이 도구 선택으로 되돌아옵니다".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~14 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

# 폭은 계약의 본문 삽입용 상한(880~1000) 안으로 두고, 여섯을 2 열로 접어 담는다.
COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "올리는 길 넷", "무엇으로 리소스를 올리는가"),
    ("§2", "검증이 서는 자리", "왜 Helm 단독이 물러났는가"),
    ("§3", "프로파일 여덟", "무엇을 골라 올리는가"),
    ("§4", "리소스 둘로 나누기", "프로파일과 이름을 어떻게 고르는가"),
    ("§5", "이름이 하는 일", "갱신인가 새 설치인가"),
    ("§6", "도구 선택으로 되돌아옴", "이념인가 비용인가"),
]
FOCAL = 5
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · A0-01",
      "부록 A 를 읽는 순서",
      "설치를 고르는 판단을 좁은 데서 넓은 데로 놓은 지도. 앞의 둘이 무엇으로 올리는지를 세우고 셋째가 "
      "무엇을 골라 올리는지를 세운다. 넷째가 그 둘로 구성을 하나 만들고 마지막이 도구 선택으로 되돌아온다.",
      "앞의 다섯은 기계가 하는 일이고 §6 만 사람이 고르는 자리입니다")

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

d.legend(LEGY, [("사람이 판단하는 자리", ACC)])
d.save("a0-01.appendix-overview.svg")
