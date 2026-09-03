# 13-01 본문 정리 앞 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 것 하나", "색이 붙은 칸이 저자가 마지막 이정표라고 부른 자리".
# 원문 13.1.3 이 이름 해석을 "the last milestone to integrate VMs into the service mesh" 라 부른다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~12 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

# 폭은 계약의 본문 삽입용 상한(880~1000) 안으로 두고, 4 열을 2 열로 접어 담는다.
# 계약: "넓은 캔버스에 담기지 않으면 폭을 늘리지 말고 배치를 바꾼다."
COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "옮길 수 없어서 남은 것", "왜 아직 VM 에 있는가"),
    ("§2", "신원은 꿔 온다", "무엇으로 자기를 증명하는가"),
    ("§3", "그룹과 엔트리", "쿠버네티스의 무엇을 베꼈는가"),
    ("§4", "준비성과 생존성", "누가 무엇을 보는가"),
    ("§5", "이름이 풀려야 나간다", "왜 DNS 가 또 필요한가"),
    ("§6", "다른 망에 문을 세운다", "무엇을 열어야 하는가"),
    ("§7", "설정 다섯 조각", "무엇이 어디에 앉는가"),
    ("§8", "200 보다 500 이 먼저", "어떤 순서로 내려가는가"),
]
FOCAL = 4
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · 13-01",
      "VM 을 메시에 넣는 여덟 마디 — 읽는 순서",
      "13 장 노트의 절 여덟을 읽는 순서로 이은 지도. 앞의 다섯 절이 쿠버네티스가 대신하던 일을 하나씩 "
      "이름 붙이고, 뒤의 세 절이 그것을 실제로 세운다.",
      "앞의 다섯은 무엇이 없는지를 세고 뒤의 셋은 그것을 하나씩 채웁니다")

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

d.legend(LEGY, [("저자가 마지막 이정표라 부른 자리", ACC)])
d.save("13-01.chapter-overview.svg")
