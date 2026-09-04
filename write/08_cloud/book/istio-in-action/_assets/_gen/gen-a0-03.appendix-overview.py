# a0-03 본문 정리 앞 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 본문: "앞의 넷이 규격이고 뒤의 셋이 Istio 의 구현입니다."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~14 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "넘기고 남기는 선", "PKI 는 어디까지 남의 몫인가"),
    ("§2", "SPIFFE 규격 넷", "각각 어느 플레인에 서는가"),
    ("§3", "SPIFFE ID 의 형식", "변수는 왜 둘뿐인가"),
    ("§4", "비밀 금지 제약", "왜 부품이 하나 더 필요한가"),
    ("§5", "SVID 와 Istio 의 대응", "왜 X.509 를 골랐는가"),
    ("§6", "부트스트랩 다섯 걸음", "토큰이 어떻게 인증서가 되는가"),
    ("§7", "요청 신원", "무엇이 쌓이고 누가 읽는가"),
]
FOCAL = 3
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · A0-03",
      "부록 C 를 읽는 순서",
      "앞의 넷이 SPIFFE 규격이고 뒤의 셋이 Istio 의 구현이다. 색이 붙은 칸의 제약 하나가 규격의 "
      "나머지 구조를 거의 다 결정하므로, 거기서부터 뒤가 따라 나온다.",
      "규격을 먼저 세운 뒤 그 위에 구현을 얹는 순서입니다")

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

d.legend(LEGY, [("나머지를 결정하는 제약", ACC)])
d.save("a0-03.appendix-overview.svg")
