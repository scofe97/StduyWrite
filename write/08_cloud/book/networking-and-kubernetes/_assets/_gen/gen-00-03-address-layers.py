# 00-03-address-layers — 층이 다르면 쓰는 주소도, 그것을 읽는 장비도 다르다
# 본문 요구: "주소는 층마다 따로 있다" — MAC 이 뜻을 갖는 L2 가 이 절의 초점이라 거기에 focal.
# 타입 스펙: type-layers.md — 위가 앱 쪽, 아래가 선 쪽인 네 층 스택. 순서축이 형태로 존재한다.
#           accent 는 한 레이어에만(스펙 관례) — L2 다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER, KR, MONO

W, H = 1000, 448
LX, LW, LH, Y0 = 100, 840, 64, 128
LAYERS = [("L4", "포트 · Transport", "한 기계 안 어느 프로그램인지 가른다", False),
          ("L3", "IP 주소 · Network", "라우터가 읽고 다음 망을 고른다", False),
          ("L2", "MAC 주소 · Link", "스위치가 읽고 옆 기계로 건넨다", True),
          ("L1", "주소 없음 · Physical", "허브는 가리지 않고 그대로 복사한다", False)]

d = D(W, H, "LAYER STACK · ADDRESSES",
      "주소는 층마다 따로 있다",
      "네 개의 층을 위에서 아래로 쌓아, 각 층이 쓰는 주소와 그 주소를 읽는 장비를 짝지어 보인 계층 스택. "
      "MAC 주소가 있는 Link 층을 초점으로 강조했다.",
      lead="위가 앱 쪽이고 아래가 선 쪽입니다. 층이 다르면 쓰는 주소도, 그것을 읽는 장비도 다릅니다.")

for i, (tag, name, who, focal) in enumerate(LAYERS):
    y = Y0 + i * LH
    if focal:
        d.tone(LX, y, LW, LH, ACC, 0, "12", 1.2)
    else:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" fill="{PAPER}"/>')
    d.line(LX, y, LX + LW, y, RULE, 0.8)
    c = ACC if focal else SOFT
    d.t(LX + 20, y + 38, tag, 9, c, MONO, "start", 600 if focal else 400)
    d.t(LX + 140, y + 40, name, 16, INK, KR, "start", 600)
    d.t(LX + LW - 20, y + 40, who, 12, ACC if focal else MUTED, KR, "end")
d.line(LX, Y0 + 4 * LH, LX + LW, Y0 + 4 * LH, RULE, 0.8)

d.t(LX, 396, "MAC 은 이 층에서만 뜻이 있어, 라우터를 하나 넘는 순간 새로 쓰입니다.", 12, MUTED, KR, "start")
d.legend(408, [("주소를 쓰는 층", MUTED), ("MAC 이 뜻을 갖는 층", ACC)])
d.save("00-03-address-layers.svg")
print("ok address-layers")
