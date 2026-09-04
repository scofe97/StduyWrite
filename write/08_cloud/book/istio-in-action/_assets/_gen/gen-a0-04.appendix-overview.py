# a0-04 본문 정리 앞 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 본문: "앞의 셋이 에이전트 쪽이고 뒤의 셋이 Pilot 쪽입니다."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~14 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "사이드카 포트 여덟", "어느 쪽을 향해 열렸나"),
    ("§2", "15020 의 엔드포인트 여섯", "한 포트가 왜 여럿을 겸하나"),
    ("§3", "15004 로 묻는 길", "연결이 살아 있는지 어떻게 아나"),
    ("§4", "Pilot 포트 여섯", "15010 을 왜 권하지 않나"),
    ("§5", "디버그 엔드포인트 두 묶음", "무엇을 묻는가로 갈린다"),
    ("§6", "도구와 ControlZ", "평소엔 누가 대신 치나"),
]
FOCAL = 4
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · A0-04",
      "부록 D 를 읽는 순서",
      "앞의 셋이 에이전트 쪽이고 뒤의 셋이 Pilot 쪽이다. 양쪽 다 서비스를 향한 포트에서 사람을 향한 "
      "포트로, 다시 그 안의 엔드포인트로 내려간다. 색이 붙은 칸이 저자가 운영에서 끄라고 적은 자리다.",
      "번호가 장마다 흩어져 있어 저자가 이 부록에 모았습니다")

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

d.legend(LEGY, [("운영에서 끄라고 적은 자리", ACC)])
d.save("a0-04.appendix-overview.svg")
