# 02-01.chapter-overview — 세로 체인 + 커널 경계
# 본문: "위는 유저 공간에서 부르는 쪽, 아래는 물리 네트워크. 그 사이 커널 안에서
#        벌어지는 네 단계가 §1~§6 이다. 이 편은 점선 안을 다룬다."
# 타입 스펙: type-layers.md — 위·아래가 의미를 갖는 축이므로 가로로 눕히지 않는다.
#           경계 링은 type-nested.md 관례. 링 밖 두 칸이 '이 편이 다루지 않는 곳'이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 788
d = D(W, H, "02-01 · CHAPTER MAP",
      "커널이 패킷을 다루는 법 전체 지도 — 이 편은 점선 안을 다룬다",
      "위는 유저 공간에서 부르는 쪽, 아래는 물리 네트워크. 그 사이 커널 안에서 벌어지는 네 단계가 이 편이다.",
      lead="위는 유저 공간, 아래는 물리 네트워크 · 그 사이 커널 안 네 단계가 이 편이다")

BX, BW, BH = 180, 640, 64
RING = (156, 232, 688, 332)
APP_CY, NIC_CY = 176, 624
STEPS = [(268, "소켓 · fd", "번역은 커널 몫", "§1 · §2"),
         (348, "veth · 브리지", "네임스페이스 연결", "§3"),
         (428, "훅 · 연결 추적", "버릴지 고칠지", "§4 · §5"),
         (508, "라우팅", "구체성이 먼저", "§6")]

def row(cy, label, sub, tag, c=None, h=BH, dash=False):
    y = cy - h // 2
    d.o.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{h}" rx="6" fill="{PAPER2}" '
               f'stroke="{c or RULE}" stroke-width="1.1"{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(BX + 20, cy - 4, ddx.fit(label, 13, 300, label), 13, c or INK, KR, "start", 600)
    d.t(BX + 20, cy + 16, ddx.fit(sub, 11, 340, sub), 11, MUTED, KR, "start")
    d.t(BX + BW - 20, cy + 4, tag, 11, SOFT, KR, "end")

ddx.band(d, 104, 728, "부르는 쪽과 물리 네트워크 사이에서 커널이 하는 일이 이 편의 범위다")

rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "커널 공간 — 이 편이 다루는 곳", 11, ACC)

row(APP_CY, "애플리케이션", "socket() 을 부른다", "유저 공간", INFO, 72, dash=True)
for cy, l, s, t in STEPS: row(cy, l, s, t)
row(NIC_CY, "NIC", "물리 네트워크로", "커널 밖", INFO, 72, dash=True)

d.path(f"M 500 {APP_CY+36+6} L 500 {STEPS[0][0]-BH//2-10}", MUTED, 1.5, m="ar")
for (a, *_), (b, *_) in zip(STEPS, STEPS[1:]):
    d.path(f"M 500 {a+BH//2+4} L 500 {b-BH//2-10}", MUTED, 1.5, m="ar")
d.path(f"M 500 {STEPS[-1][0]+BH//2+4} L 500 {NIC_CY-36-10}", MUTED, 1.5, m="ar")

d.t(36, 692, "점선 밖 두 칸은 이 편이 다루지 않는다 — 부르는 쪽은 01 장이, "
             "물리 네트워크는 그 아래가 맡는다", 12, MUTED, KR, "start")
d.legend(744, [("커널 밖", INFO), ("이 편의 범위", ACC)])
d.save("02-01.chapter-overview.svg")
print("ok 02-01.chapter-overview")
