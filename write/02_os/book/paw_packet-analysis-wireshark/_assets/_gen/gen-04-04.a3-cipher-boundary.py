# 04-04 A3 — 프레임 9 안의 레코드 셋과 보호가 걸리는 경계. content_type 22·20·22, handshake.type 16 하나만 읽힌 실측.
# 타입 스펙: type-nested — 세그먼트(바깥)가 레코드 셋(안)을 품는 포함 관계. focal 은 처음 보호되는 셋째 레코드.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import W, EYEBROW, D, kr, ACC, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
H = 400
d = D(W, H, EYEBROW + "A3", "A3 · 프레임 9 의 레코드 셋",
      "프레임 9 한 세그먼트에 ClientKeyExchange·ChangeCipherSpec·Finished 세 레코드가 들어 있다. ChangeCipherSpec 까지는 평문이고, 그 다음 레코드부터 보호가 걸려 셋째 레코드의 종류가 읽히지 않는다.",
      "전환을 알리는 레코드 자체는 평문이고, 보호는 그 다음부터입니다")
# 바깥 고리 — 세그먼트
d.o.append(f'<rect x="24" y="112" width="832" height="208" rx="8" fill="rgba(245,245,245,0.015)" stroke="rgba(191,192,192,0.40)" stroke-width="1"/>')
d.o.append(f'<rect x="36" y="106" width="128" height="14" fill="{PAPER}"/>')
d.t(40, 117, "FRAME 9 · TCP SEGMENT", 8, SOFT, MONO, "start")
recs = [("content_type 22", "ClientKeyExchange", "handshake.type 16", "record.length 37", "평문", False),
        ("content_type 20", "ChangeCipherSpec", "handshake.type 없음", "record.length 1", "평문", False),
        ("content_type 22", "Finished", "종류 읽히지 않음", "record.length 40", "암호화", True)]
BW, GAP, X0, Y = 248, 20, 56, 148
for i, (ct, name, ht, ln, tag, focal) in enumerate(recs):
    x = X0 + i * (BW + GAP)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{BW}" height="144" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, BW, 144, PAPER2, RULE, 1.0, 6)
    c = ACC if focal else INK
    d.t(x + 16, Y + 24, ct, 11, MUTED, MONO, "start")
    d.t(x + BW / 2, Y + 60, name, 14, c, MONO, "middle", 600)
    d.t(x + BW / 2, Y + 84, ht, 11, MUTED, kr(ht))
    d.t(x + BW / 2, Y + 104, ln, 11, MUTED, MONO)
    tc = ACC if focal else OK
    d.o.append(f'<rect x="{x + BW / 2 - 32}" y="{Y + 114}" width="64" height="20" rx="4" fill="{tc}22" stroke="{tc}" stroke-width="1"/>')
    d.t(x + BW / 2, Y + 128, tag, 11, tc, KR, "middle", 600)
# 경계선 — 둘째와 셋째 레코드 사이
bx = X0 + 2 * BW + GAP + GAP / 2
d.line(bx, 136, bx, 304, ACC, 1.4, "5 4")
d.t(bx, 340, "여기부터 보호", 12, ACC, KR, "middle", 600)
d.legend(360, [("처음 보호되는 레코드", ACC), ("평문 레코드", OK)])
d.save("04-04.a3-cipher-boundary.svg")
