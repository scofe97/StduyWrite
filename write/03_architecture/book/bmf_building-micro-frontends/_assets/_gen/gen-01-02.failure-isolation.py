# 01-02 §5 — 조각 하나가 런타임에 실패했을 때의 판단. 저자가 처방을 적은 갈래와 적지 않은 갈래를 구분해 그린다.
# 원문이 명시하지 않은 갈래는 채우지 않고 "명시 없음"으로 남긴다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 모양이 종류를 나르고 색은 한 갈래에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 624
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-02 §5",
      "조각 하나가 실패했을 때의 판단",
      "런타임 조합이라 UI 조각마다 404·500 이 따로 난다. 저자는 비필수 조각의 처방만 적고 주 조각이 못 뜬 경우의 처방은 적지 않는다.",
      "마름모가 판단, 사각형이 처리, 타원이 종착입니다. 색이 붙은 갈래가 저자가 처방을 적은 자리입니다")

def oval(cx, cy, w, h, text, c=INK, stroke=RULE):
    d.o.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="20" fill="{PAPER2}" stroke="{stroke}" stroke-width="1.0"/>')
    d.t(cx, cy + 5, text, 12.5, c, KR, "middle", 600)

def diamond(cx, cy, hw, hh, text):
    d.o.append(f'<polygon points="{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(cx, cy + 5, text, 12.5, INK, KR, "middle", 600)

def rect(x, y, w, h, title, sub, acc=False, dashed=False):
    if acc:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER2}" stroke="{MUTED if dashed else RULE}" stroke-width="1.0"{dash}/>')
    d.t(x + 16, y + 22, title, 12.5, ACC if acc else INK, KR, "start", 600)
    d.t(x + 16, y + 42, sub, 10, MUTED, KR, "start")

SX, RX, RW = 280, 560, 320
# 연결선 먼저
d.arrow([(SX, 136), (SX, 178)], MUTED, "ar", 1.3)
d.arrow([(410, 232), (RX - 2, 232)], MUTED, "ar", 1.3); d.t(470, 222, "예", 11, MUTED, KR)
d.arrow([(SX, 284), (SX, 330)], MUTED, "ar", 1.3);      d.t(294, 312, "아니오", 11, MUTED, KR, "start")
d.arrow([(410, 384), (RX - 2, 384)], MUTED, "ar", 1.3); d.t(470, 374, "아니오", 11, MUTED, KR)
d.arrow([(SX, 436), (SX, 486)], MUTED, "ar", 1.3);      d.t(294, 466, "예", 11, MUTED, KR, "start")
d.arrow([(720, 256), (720, 298)], MUTED, "ar", 1.3)
d.arrow([(720, 408), (720, 450)], ACC, "acc", 1.3)

oval(SX, 112, 300, 48, "런타임에 조각을 불러온다")
diamond(SX, 232, 130, 52, "응답이 정상인가")
rect(RX, 208, RW, 48, "그대로 합쳐 보여 준다", "")
oval(720, 324, 300, 48, "완전한 화면")
diamond(SX, 384, 130, 52, "그 페이지의 주 조각인가")
rect(RX, 360, RW, 48, "대체 콘텐츠를 보이거나 감춘다", "")
oval(720, 476, 300, 48, "경험 손상을 줄인 화면", ACC, ACC)
rect(150, 488, 260, 60, "원문이 처방을 적지 않음", "저자의 문장이 여기서 끊긴다", dashed=True)

d.legend(576, [("저자가 처방을 적은 갈래", ACC)])
d.save("01-02.failure-isolation.svg")
print("h 필요:", 576 + 22 + 16, " 실제:", H)
