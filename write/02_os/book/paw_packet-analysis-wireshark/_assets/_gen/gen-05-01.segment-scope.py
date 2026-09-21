# 05-01 §1 — 네트워크 세그먼트. 스위치는 브로드캐스트를 모든 포트로 복사하고, 라우터는 넘기지 않는다.
# 그래서 브로드캐스트가 닿는 범위가 곧 세그먼트이고 라우터가 그 경계다. 01-01 §4 의 도착 범위를 라우터까지 넓힌 그림.
# 타입 스펙: type-architecture — 구성요소(장비 · 스위치 · 라우터)와 연결을 세그먼트 존 둘로 묶는다.
#           흐름은 왼쪽 → 오른쪽 하나. focal 은 브로드캐스트가 멈추는 라우터 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, BAD, PAPER, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

W, H = 940, 496
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §1",
      "브로드캐스트가 닿는 범위",
      "세그먼트 A 의 클라이언트가 보낸 브로드캐스트는 스위치가 모든 포트로 복사해 분석기와 이웃 장비에 닿는다. 라우터는 이것을 넘기지 않으므로 세그먼트 B 의 서버에는 닿지 않는다.",
      "라우터를 거치지 않고 닿는 범위가 세그먼트이고, 라우터가 그 경계입니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" stroke="{RULE}" stroke-width="1.0" stroke-dasharray="6,4"/>')
    d.t(x + 16, y + 22, label, 12, MUTED, KR, "start", 600)

def node(cx, y, w, h, name, sub, c=None, dashed=False):
    x = cx - w / 2
    if dashed:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4,3"/>')
        c = SOFT
    elif c:
        d.tone(x, y, w, h, c, 6)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(cx, y + 22, name, 13, c or INK, KR, "middle", 600)
    d.t(cx, y + 40, sub, 12, MUTED, kr(sub))

# 존 — 세그먼트 A · 라우터 · 세그먼트 B
ZY, ZH = 108, 312
zone(24, ZY, 556, ZH, "세그먼트 A")
zone(716, ZY, 200, ZH, "세그먼트 B")

SW_Y, SW_H = 160, 52          # 스위치 줄
HOST_Y, HOST_H = 312, 52      # 장비 줄
d.box(64, SW_Y, 468, SW_H, PAPER2, RULE, 1.0, 6)
d.t(298, SW_Y + 22, "스위치", 13, INK, KR, "middle", 600)
d.t(298, SW_Y + 40, "브로드캐스트를 모든 포트로 복사", 12, MUTED, KR)

# 클라이언트 → 스위치(위로), 스위치 → 나머지 장비(아래로)
d.arrow([(112, HOST_Y - 4), (112, SW_Y + SW_H + 4)], INFO, "info", 1.5)
d.t(124, 268, "255.255.255.255", 12, INFO, MONO, "start")
for cx in (298, 484):
    d.arrow([(cx, SW_Y + SW_H + 4), (cx, HOST_Y - 4)], INFO, "info", 1.5)
node(112, HOST_Y, 160, HOST_H, "클라이언트", "보낸 쪽")
node(298, HOST_Y, 160, HOST_H, "분석기", "도착", INFO)
node(484, HOST_Y, 160, HOST_H, "이웃 장비", "도착", INFO)

# 스위치 → 라우터, 라우터에서 멈춤
RX, RW = 644, 104
d.arrow([(532 + 4, SW_Y + SW_H / 2), (RX - RW / 2 - 4, SW_Y + SW_H / 2)], INFO, "info", 1.5)
d.o.append(f'<rect x="{RX - RW / 2}" y="{SW_Y}" width="{RW}" height="{SW_H}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(RX, SW_Y + 22, "라우터", 13, ACC, KR, "middle", 600)
d.t(RX, SW_Y + 40, "넘기지 않음", 12, ACC, KR)
d.t(RX, SW_Y + SW_H + 28, "경계", 12, ACC, KR, "middle", 600)

# 세그먼트 B — 닿지 않음
d.line(RX + RW / 2, SW_Y + SW_H / 2, 736, SW_Y + SW_H / 2, SOFT, 1.0, "4,3")
node(816, SW_Y, 160, SW_H, "스위치", "세그먼트 B", dashed=True)
d.line(816, SW_Y + SW_H, 816, HOST_Y, SOFT, 1.0, "4,3")
node(816, HOST_Y, 160, HOST_H, "DHCP 서버", "닿지 않음", dashed=True)

d.legend(H - 56, [("브로드캐스트가 멈추는 경계", ACC), ("브로드캐스트가 도착", INFO), ("닿지 않음", SOFT)])
d.save("05-01.segment-scope.svg")
