# 13-02 §1·§3 — TCP 옵션 칸 40바이트를 실제 세그먼트 둘이 어떻게 채우는가.
# 값 출처: OrbStack Ubuntu(커널 7.0.14) 캡처(2026-10-04).
#   SYN: options [mss 1460,sackOK,TS val … ecr 0,nop,wscale 10] → MSS 4 + SACK-Permitted 2 + Timestamps 10 + NOP 1 + Window Scale 3 = 20바이트
#        (IP length 60 → TCP 헤더 40바이트).
#   SACK 3블록 ACK: options [nop,nop,TS val … ecr …,nop,nop,sack 3 {…}{…}{…}] → 1+1+10+1+1+(2+3×8) = 40바이트 (IP length 80 → TCP 헤더 60바이트).
#   원문 13.3.2: SACK 블록 n 개의 옵션은 8n+2 바이트, Timestamps 를 함께 쓰면 한 세그먼트에 최대 3블록.
# 타입 스펙: type-layers — 같은 40바이트 칸 두 줄을 위아래로 쌓고 칸을 바이트 폭 비례로 가른 변형(12-01 tcp-header 와 같은 축약).
#           focal 은 SACK 3블록 줄의 SACK 옵션 26바이트 한 칸. 남는 바이트는 점선 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 456
X0, BW, RH = 160, 18, 56            # 1바이트 = 18px, 40바이트 = 720px
ROWS = [
    ("SYN", "IP 60 · TCP 40", [(4, "MSS", "kind 2", INFO), (2, "SACK", "허용", INFO), (10, "Timestamps", "kind 8 · TSval · TSecr", INFO),
                                (1, "N", "", None), (3, "WS", "kind 3", INFO), (20, "", "남는 20바이트", "free")]),
    ("SACK 3블록 ACK", "IP 80 · TCP 60", [(1, "N", "", None), (1, "N", "", None), (10, "Timestamps", "kind 8", INFO),
                                (1, "N", "", None), (1, "N", "", None), (26, "SACK · 블록 3개", "kind 5 · len 26 = 8×3+2", "focal")]),
]

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-02 §1 · §3",
      "옵션 칸 40바이트를 실제로 채우는 모습",
      "리눅스가 실제로 보낸 세그먼트 둘의 옵션 칸을 바이트 폭 비례로 그렸다. 윗줄 SYN 은 MSS·SACK 허용·Timestamps·NOP·Window Scale 로 20바이트를 쓴다. "
      "아랫줄은 SACK 블록 세 개를 실은 ACK 로, 4바이트 정렬용 NOP 넷과 Timestamps 10바이트에 SACK 26바이트가 더해져 40바이트를 다 채운다. N 은 NOP 이다.",
      "Timestamps 를 함께 쓰면 SACK 블록은 세 개가 한도입니다")

# 바이트 눈금
d.line(X0, 120, X0 + 40 * BW, 120, RULE, 0.8)
for b in (0, 10, 20, 30, 40):
    d.t(X0 + b * BW, 112, str(b), 11, SOFT, MONO)

for r, (name, sub, cells) in enumerate(ROWS):
    y = 152 + r * (RH + 72)
    d.t(X0 - 12, y + 24, name, 13, INK, KR, "end", 600)
    d.t(X0 - 12, y + 42, sub, 11, MUTED, MONO, "end")
    x = X0
    for n, lab, s2, kind in cells:
        w = n * BW
        if kind == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{RH}" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); c = ACC
        elif kind == "free":
            d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{RH}" fill="{PAPER}" stroke="{RULE}" stroke-width="1" stroke-dasharray="5 4"/>'); c = SOFT
        elif kind:
            d.tone(x, y, w, RH, kind, 0, "16", 1.0); c = kind
        else:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 0); c = MUTED
        if lab:
            d.t(x + w / 2, y + (24 if s2 else 34), lab, 12, c, MONO if all(ord(ch) < 128 for ch in lab) else KR, "middle", 600)
        if s2:
            d.t(x + w / 2, y + (42 if lab else 34), s2, 11, MUTED, MONO if all(ord(ch) < 128 for ch in s2) else KR)
        x += w

d.legend(H - 56, [("SACK 블록 세 개", ACC), ("옵션", INFO), ("NOP · 4바이트 정렬", MUTED), ("쓰지 않은 칸", SOFT)])
d.save("13-02.option-space.svg")
