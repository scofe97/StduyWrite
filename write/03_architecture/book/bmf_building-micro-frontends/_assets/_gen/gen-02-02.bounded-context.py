# 02-02 §1 — 바운디드 컨텍스트 하나의 안과 밖 (원문 Figure 2-3).
# 저자가 캡션과 본문에 적은 것만 그린다 — 카탈로그 마이크로 프론트엔드가 BFF 라는 단일 진입점으로
# 마이크로서비스 API 를 소비하고, 컨텍스트 사이는 계약으로 잇는다. 서비스 이름은 지어내지 않는다.
# 타입 스펙: type-architecture — 논리 경계로 묶은 구성요소와 그 사이 연결. 단일 진입점 하나에만 accent.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1100, 592
d = D(W, H, "BUILDING MICRO-FRONTENDS · 02-02 §1",
      "바운디드 컨텍스트 하나의 안과 밖",
      "논리 경계 안에 카탈로그 마이크로 프론트엔드와 BFF 와 마이크로서비스가 함께 놓이고, 밖으로는 API 계약만 노출한다.",
      "안쪽 구현은 감추고 밖으로는 계약만 냅니다. 색이 붙은 것이 단일 진입점입니다")

ZX, ZY, ZW, ZH = 60, 110, 620, 390
d.o.append(f'<rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="{INK}05" stroke="{RULE}" stroke-width="0.8"/>')
lbl = "BOUNDED CONTEXT · CATALOG"
lw = len(lbl) * 6.4 + 16
d.o.append(f'<rect x="{ZX + 20}" y="{ZY - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
d.t(ZX + 20 + lw / 2, ZY + 3, lbl, 7.5, SOFT, MONO)

MFE_X, MFE_Y, MFE_W = 140, 150, 460
BFF_X, BFF_Y, BFF_W = 260, 270, 220
MS_Y, MS_W = 400, 180
def msx(i): return 80 + i * 200

# 연결선 먼저
d.arrow([(370, MFE_Y + 64), (370, BFF_Y - 2)], MUTED, "ar", 1.3)
for i in range(3):
    cx = msx(i) + MS_W / 2
    if cx == 370:
        d.arrow([(370, BFF_Y + 64), (370, MS_Y - 2)], MUTED, "ar", 1.2)
    else:
        s = 8 if cx > 370 else -8
        d.path(f"M 370 {BFF_Y + 64} V {MS_Y - 40} Q 370 {MS_Y - 32} {370 + s} {MS_Y - 32} "
               f"H {cx - s} Q {cx} {MS_Y - 32} {cx} {MS_Y - 24} V {MS_Y - 2}", MUTED, 1.2, m="ar")
# 밖으로 나가는 계약
d.path(f"M {ZX + ZW} 302 H 752 Q 760 302 760 302", MUTED, 1.2, dash="5 4")
d.arrow([(760, 302), (798, 302)], MUTED, "ar", 1.2, dash="5 4")
d.o.append(f'<rect x="{700}" y="{278}" width="{64}" height="14" rx="2" fill="{PAPER}"/>')
d.t(732, 289, "API 계약", 9, MUTED, KR)

d.box(MFE_X, MFE_Y, MFE_W, 64, PAPER2, RULE, 1.0, 6)
d.t(370, MFE_Y + 28, "카탈로그 마이크로 프론트엔드", 13, INK, KR, "middle", 600)
d.t(370, MFE_Y + 48, "화면과 상태를 이 컨텍스트가 소유한다", 10, MUTED, KR)

d.o.append(f'<rect x="{BFF_X}" y="{BFF_Y}" width="{BFF_W}" height="64" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(370, BFF_Y + 28, "BFF", 13, ACC, KR, "middle", 600)
d.t(370, BFF_Y + 48, "단일 진입점", 10, MUTED, KR)

for i in range(3):
    x = msx(i)
    d.box(x, MS_Y, MS_W, 64, PAPER2, RULE, 1.0, 6)
    d.t(x + MS_W / 2, MS_Y + 30, "마이크로서비스", 12, INK, KR, "middle", 600)
    d.t(x + MS_W / 2, MS_Y + 50, "구현 세부는 감춘다", 10, MUTED, KR)

d.box(798, 270, 240, 64, PAPER2, RULE, 1.0, 6)
d.t(918, 298, "다른 바운디드 컨텍스트", 12, INK, KR, "middle", 600)
d.t(918, 318, "계약만 보고 소비한다", 10, MUTED, KR)

d.legend(540, [("컨텍스트의 단일 진입점", ACC)])
d.save("02-02.bounded-context.svg")
print("h:", 540 + 40, "/", H)
