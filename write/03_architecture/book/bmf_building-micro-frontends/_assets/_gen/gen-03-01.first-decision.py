# 03-01 §1·§3 — 첫 결정과 두 갈래가 각각 사는 것 (원문 Figure 3-1 의 첫 분기).
# 조합 자리의 하위 분기는 02-03 의 격자가 이미 갖고 있으므로 여기서 되풀이하지 않고 종착에서 넘긴다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단. 모양이 종류를 나르고 accent 는
#           가장 파급이 큰 판단 하나에만 준다(저자가 "첫 결정"이라 부른 자리).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 732
d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-01 §1~§3",
      "첫 결정과 두 갈래가 사는 것",
      "수평이냐 수직이냐가 첫 결정이고, 그 뒤의 조합·라우팅·기술이 여기에 매인다. 색이 붙은 마름모가 파급이 가장 큰 판단이다.",
      "마름모가 판단, 사각형이 결과, 타원이 종착입니다")

def oval(cx, cy, w, h, text, c=INK, stroke=RULE):
    d.o.append(f'<rect x="{cx - w/2}" y="{cy - h/2}" width="{w}" height="{h}" rx="20" fill="{PAPER2}" stroke="{stroke}" stroke-width="1.0"/>')
    d.t(cx, cy + 5, text, 12.5, c, KR, "middle", 600)

CX, LX, RX = 620, 380, 860
# 연결선 먼저
d.arrow([(CX, 136), (CX, 178)], MUTED, "ar", 1.3)
d.path(f"M {CX - 200} 236 H {LX + 8} Q {LX} 236 {LX} 244 V 334", MUTED, 1.3, m="ar")
d.path(f"M {CX + 200} 236 H {RX - 8} Q {RX} 236 {RX} 244 V 334", MUTED, 1.3, m="ar")
# 라벨을 가로 구간에 두면 마름모 외곽선에 겹친다. 세로 구간 바깥쪽으로 옮긴다.
d.t(LX - 14, 292, "아니오", 11, MUTED, KR, "end")
d.t(RX + 14, 292, "예", 11, MUTED, KR, "start")
for x in (LX, RX):
    d.arrow([(x, 400), (x, 438)], MUTED, "ar", 1.3)
    d.arrow([(x, 580), (x, 602)], MUTED, "ar", 1.3)

oval(CX, 112, 320, 48, "프로젝트 특성을 본다")
d.o.append(f'<polygon points="{CX},180 {CX+200},236 {CX},292 {CX-200},236" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, 232, "서브도메인 하나가", 12.5, ACC, KR, "middle", 600)
d.t(CX, 252, "여러 뷰에 걸치는가", 12.5, ACC, KR, "middle", 600)

for x, name, en, lines in [
    (LX, "수직 분할", "vertical", ["선택지가 적고 복잡도가 낮다",
                                "SPA 에 가장 가까운 개발 경험",
                                "셸과 조각이 항상 1:1",
                                "셸은 한 번에 하나만 로드한다"]),
    (RX, "수평 분할", "horizontal", ["서브도메인을 여러 뷰에서 재사용",
                                   "SEO 가 핵심 요구일 때",
                                   "개발자가 수십에서 수백 명일 때",
                                   "멀티테넌트 고객 커스터마이징"]),
]:
    d.box(x - 160, 336, 320, 64, PAPER2, RULE, 1.0, 6)
    d.t(x, 362, name, 14, INK, KR, "middle", 600)
    d.t(x, 384, en, 9, SOFT, MONO)
    d.box(x - 160, 440, 320, 140, f"{INK}08", RULE, 0.9, 6)
    for i, ln in enumerate(lines):
        d.t(x - 142, 468 + i * 30, "· " + ln, 11, MUTED, KR, "start")

oval(LX, 626, 320, 48, "클라이언트 조합 · 클라이언트 라우팅")
oval(RX, 626, 320, 48, "조합 자리를 다시 고른다")

d.legend(692, [("파급이 가장 큰 판단", ACC)])
d.save("03-01.first-decision.svg")
print("h 필요:", 692 + 40, " 실제:", H)
