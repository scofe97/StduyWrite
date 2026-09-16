# 04-03.dual-stack — 서비스의 ipFamilyPolicy 와 클러스터 스택이 만나 결과가 정해진다
# 본문 요구: "기본값이 SingleStack 인 이유 … 어느 클러스터에 올려도 뜨는 값이 기본이어야 합니다 …
#           옮겨 다닐 매니페스트라면 PreferDualStack … RequireDualStack 은 dual-stack 이라는 것을 아는 자리에서만"
# 타입 스펙: type-dp-security-matrix — 행이 ipFamilyPolicy 셋, 열이 클러스터 스택 둘. "어느 조합이 되고 안 되는가".
#           기본값을 가르는 단일 스택 열의 머리에만 accent 를 둔다. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 472
d = D(W, H, "DUAL STACK · TWO LAYERS DECIDE TOGETHER",
      "서비스가 어느 패밀리로 뜨는지는 두 층이 함께 정한다",
      "클러스터가 dual-stack 인지와 서비스의 ipFamilyPolicy 가 무엇인지가 만나 결과가 정해지며, "
      "기본값 SingleStack 은 어느 클러스터에서도 뜨기 때문에 기본이다.",
      lead="클러스터에 IPv6 를 켜는 결정과 서비스 하나의 패밀리 선택은 다른 층")

X0, GAP = 32, 16
COLS = [(280, "서비스가 고른 값"), (304, "클러스터가 단일 스택이면"), (304, "클러스터가 dual-stack 이면")]
HY, RY0, RH = 136, 152, 72
XS = []; x = X0
for i, (w, name) in enumerate(COLS):
    XS.append((x, w))
    d.t(x + w // 2, HY, name, 12, ACC if i == 1 else SOFT, KR, "middle", 600)
    x += w + GAP
d.line(XS[1][0], HY + 8, XS[1][0] + XS[1][1], HY + 8, ACC, 1.4)

ROWS = [("SingleStack", "기본값", OK, [("주소 하나", OK), ("주소 하나", OK)]),
        ("PreferDualStack", "옮겨 다닐 매니페스트", INFO, [("SingleStack 처럼 동작", OK), ("주소 둘", INFO)]),
        ("RequireDualStack", "dual-stack 확인된 자리", BAD, [("할당 실패", BAD), ("주소 둘", OK)])]

for r, (pol, sub, pc, cells) in enumerate(ROWS):
    y = RY0 + r * (RH + GAP)
    cx0, cw = XS[0]
    d.box(cx0, y, cw, RH, PAPER2, RULE, 1.0, 6)
    d.t(cx0 + 20, y + 30, pol, 13, pc, MONO, "start", 600)
    d.t(cx0 + 20, y + 52, sub, 12, MUTED, KR, "start")
    for i, (txt, c) in enumerate(cells, 1):
        cx0, cw = XS[i]
        d.o.append(f'<rect x="{cx0}" y="{y}" width="{cw}" height="{RH}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
        d.t(cx0 + cw // 2, y + 41, txt, 13, c, KR, "middle", 600)

d.legend(424, [("어디서나 성공", OK), ("되면 주소 둘", INFO), ("조건 불일치 시 실패", BAD), ("기본값을 가르는 열", ACC)])
d.save("04-03.dual-stack.svg")
print("ok dual-stack")
