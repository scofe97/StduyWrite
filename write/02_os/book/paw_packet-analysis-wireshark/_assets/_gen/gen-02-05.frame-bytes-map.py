# 02-05 §6 — -x 덤프에는 강조가 없어 필드 위치를 오프셋으로 세어야 한다. 5번 프레임 101바이트가 이더넷 14·IP 20·TCP 20·HTTP 47 로 나뉘는 자리와 각 헤더의 첫 바이트.
# 타입 스펙: type-nested — 프레임이 헤더 넷을 품는 포함 관계. 폭을 바이트 수에 비례시켰고 focal 은 덤프 첫 14바이트인 이더넷 헤더.
# 사실 출처: 노트 L401~L415 (덤프 L406~L412, -V 출력 L331~L343 의 주소·포트)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 488
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-05 §6",
      "-x 덤프 101바이트의 자리",
      "프레임 5 의 덤프가 이더넷 14 · IP 20 · TCP 20 · HTTP 47 바이트로 이어진다. 필드는 오프셋을 세어 찾는다.",
      "칸 폭은 바이트 수에 비례하고 오프셋은 -x 왼쪽 열의 값입니다")

RX, RY, RW, RH = 24, 112, 952, 132
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="8" fill="{PAPER2}" fill-opacity="0.4" stroke="{RULE}" stroke-width="1.2"/>')
lab = "Frame 5 · 101바이트 · FCS 4바이트 없음"
d.o.append(f'<rect x="40" y="{RY - 8}" width="{len(lab) * 7 + 24}" height="16" fill="{PAPER}"/>')
d.t(48, RY + 4, lab, 11, SOFT, KR, "start", 600)

SEGS = [("Ethernet", 14, "0x0000–0x000d", 124), ("IPv4", 20, "0x000e–0x0021", 176),
        ("TCP", 20, "0x0022–0x0035", 176), ("HTTP", 47, "0x0036–0x0064", 412)]
CARDS = [
    [("0x0000", "00 00 5e 00 53 02", "목적지"), ("0x0006", "00 00 5e 00 53 01", "출발지"), ("0x000c", "08 00", "Type")],
    [("0x001a", "c0 00 02 0a", "출발지"), ("0x001e", "c6 33 64 14", "목적지")],
    [("0x0022", "c8 22", "출발지 포트"), ("0x0024", "00 50", "목적지 포트")],
    [("0x0036", "47 45 54", "GET"), ("0x0061", "0d 0a 0d 0a", "끝 \\r\\n\\r\\n")],
]
HEADS = ["이더넷 헤더", "IP 헤더", "TCP 헤더", "HTTP 요청"]
SY, SH, CY, CH = 148, 72, 288, 104
x = 56
for i, ((name, n, off, w), card, head) in enumerate(zip(SEGS, CARDS, HEADS)):
    focal = i == 0
    if focal:
        d.o.append(f'<rect x="{x}" y="{SY}" width="{w - 4}" height="{SH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, SY, w - 4, SH, PAPER2, RULE, 1.0, 6)
    c = ACC if focal else INK
    d.t(x + (w - 4) / 2, SY + 30, f"{name} · {n}", 13, c, KR, "middle", 600)
    d.t(x + (w - 4) / 2, SY + 52, off, 11, MUTED, MONO)
    cx = x + (w - 4) / 2
    cardx = 24 + i * 238
    ccx = cardx + 108
    d.path(f"M {cx} {SY + SH} V 262 H {ccx} V {CY - 4}", ACC if focal else MUTED, 1.0)
    d.box(cardx, CY, 216, CH, PAPER2, ACC if focal else RULE, 1.4 if focal else 1.0, 6)
    d.t(cardx + 12, CY + 22, head, 12, c, KR, "start", 600)
    for k, (o, hx, lbl) in enumerate(card):
        yy = CY + 44 + k * 20
        d.t(cardx + 12, yy, f"{o}", 11, SOFT, MONO, "start")
        d.t(cardx + 56, yy, hx, 11, INK, MONO, "start")
        d.t(cardx + 56 + len(hx) * 7 + 8, yy, lbl, 11, MUTED, KR, "start")
    x += w

d.legend(H - 72, [("이더넷 헤더 14바이트", ACC)])
d.save("02-05.frame-bytes-map.svg")
