# a0-02 본문 정리 앞 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 본문: "앞의 넷이 파드 쪽이고 뒤의 셋이 VM 쪽입니다."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~14 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "사이드카를 이루는 넷", "Envoy 혼자 못 하는 일은 무엇인가"),
    ("§2", "주입의 두 길", "누가 YAML 을 고치는가"),
    ("§3", "자동 주입이 서는 자리", "무엇이 그 연결을 만드는가"),
    ("§4", "특권과 CNI 플러그인", "왜 멀티테넌트에서 문제가 되는가"),
    ("§5", "VM 이 받는 다섯 파일", "각각 무엇에 답하는가"),
    ("§6", "cluster.env 의 값", "12 장의 식별자 셋은 어디 있는가"),
    ("§7", "고치고 다시 띄운다", "왜 손이 더 빠른 자리가 있는가"),
]
FOCAL = 4
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · A0-02",
      "부록 B·E 를 읽는 순서",
      "프록시가 자기 설정을 어떻게 받는가라는 한 질문에 두 환경이 다른 답을 내놓는다. 앞의 넷이 파드 "
      "쪽이고 뒤의 셋이 VM 쪽이다. 색이 붙은 칸이 그 경계가 넘어가는 자리다.",
      "13 장이 \"사이드카는 자기가 파드 안인지 VM 위인지 구분하지 않는다\" 고 적은 문장의 뒷면입니다")

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

d.legend(LEGY, [("파드에서 VM 으로 넘어가는 자리", ACC)])
d.save("a0-02.appendix-overview.svg")
