# 13-02 §2·§7 — MTU 하나가 IP 헤더 · TCP 헤더 · 옵션 · 데이터로 갈리는 모습. MSS 와 실제로 실리는 데이터의 차이.
# 값 출처: 원문 13.3.1(MSS 1460 이 IPv4 의 전형, 데이터그램은 40바이트 더 커서 1500) +
#   OrbStack Ubuntu 캡처(2026-10-04): MSS 1460 을 주고받았지만 Timestamps 를 쓰는 데이터 세그먼트는 1448바이트씩 실렸고(IP length 1500),
#   PTB(mtu 1000) 뒤에는 948바이트씩(IP length 1000) 실렸다. 1500 − 20 − 20 − 12 = 1448, 1000 − 20 − 20 − 12 = 948.
# 타입 스펙: type-layers — 같은 MTU 를 세 줄(MSS 의 계산 · 실제 1500 · PTB 뒤 1000)로 쌓고 칸을 바이트 폭 비례로 가른 변형.
#           focal 은 MSS 계산에 들어가지 않는 Timestamps 12바이트(NOP 2 포함) 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
X0, SCALE = 176, 0.48            # 1바이트 = 0.48px → 1500바이트 = 720px
RH = 52
ROWS = [
    ("MSS 의 계산", "MTU 1500", [(20, "IP", None), (20, "TCP", None), (1460, "MSS 1460", INFO)]),
    ("실제 데이터 세그먼트", "IP length 1500", [(20, "IP", None), (20, "TCP", None), (12, "TS", "focal"), (1448, "데이터 1448", OK)]),
    ("PTB(mtu 1000) 뒤", "IP length 1000", [(20, "IP", None), (20, "TCP", None), (12, "TS", "focal"), (948, "데이터 948", OK)]),
]

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-02 §2 · §7",
      "MSS 1460 인데 1448바이트씩 실리는 이유",
      "MSS 는 IP·TCP 기본 헤더 40바이트만 뺀 데이터 상한이라 MTU 1500 에서 1460 이다. 그런데 Timestamps 옵션을 쓰면 세그먼트마다 12바이트(옵션 10 + NOP 2)가 더 붙어 "
      "실제 데이터는 1448바이트씩 실린다. 경로 MTU 가 1000 으로 줄면 같은 계산으로 948바이트가 된다. 막대 길이는 바이트 수에 비례한다.",
      "MSS 는 데이터 상한이고, 옵션이 붙는 만큼 실제로 실리는 양은 줄어듭니다")

for r, (name, sub, cells) in enumerate(ROWS):
    y = 132 + r * (RH + 44)
    d.t(X0 - 12, y + 22, name, 13, INK, KR, "end", 600)
    d.t(X0 - 12, y + 40, sub, 11, MUTED, MONO, "end")
    x = X0
    for n, lab, kind in cells:
        w = n * SCALE
        if kind == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{RH}" fill="{ACC}22" stroke="{ACC}" stroke-width="1.4"/>'); c = ACC
        elif kind:
            d.tone(x, y, w, RH, kind, 0, "16", 1.0); c = kind
        else:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 0); c = MUTED
        if n >= 100:
            d.t(x + w / 2, y + 32, lab, 13, c, KR, "middle", 600)
        x += w
    # 작은 칸(헤더·옵션)은 너비가 10px 안팎이라 라벨을 막대 위 한 줄로 모은다
    hdr = "IP 20 + TCP 20"
    d.t(X0, y - 8, hdr, 11, SOFT, MONO, "start", 600)
    if any(k == "focal" for _, _, k in cells):
        d.t(X0 + 112, y - 8, "+ TS 12", 11, ACC, MONO, "start", 600)

d.legend(H - 56, [("MSS 에 안 들어가는 옵션 12바이트", ACC), ("데이터", OK), ("MSS 상한", INFO), ("IP · TCP 기본 헤더 20+20", MUTED)])
d.save("13-02.segment-sizes.svg")
