# 01-03.nat-port-mapping — 시퀀스 + 공유기 생존 막대
# 본문: "공유기 막대만 두 구간에 끊기지 않고 이어져 있다"
#        나갈 때 적어 둔 줄이 남아 있어야 돌아온 응답의 주인을 찾는다
# 타입 스펙: type-sequence.md — activation bar(w=8, muted, 0.8 hairline)를
#           두 구간에 걸쳐 끊지 않는 것이 이 도식의 요점. 되돌아오는 길은 dashed + filled.
import dd, ddx
from dd import D, Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 940
d = Seq(W, H, "NAT · PORT ADDRESS TRANSLATION",
        "NAT — 공인 주소 하나를 여럿이 나눠 쓰는 법",
        "나갈 때 사설 주소와 포트를 공인 주소와 새 포트로 바꿔 적고, 돌아올 때 도착 포트만 보고 표에서 주인을 찾는다",
        lead="나갈 때 적어 둔 줄이 남아 있어야 돌아온 응답의 주인을 찾는다")

LX = ddx.lanes(d, [("노트북", "192.168.0.15"), ("폰", "192.168.0.16"),
                   ("공유기", "매핑 표 보유"), ("웹 서버", "같은 주소로 보인다")],
               y0=104, lane_w=196)
NB, PH, GW, SV = (int(LX[k]) for k in ("노트북", "폰", "공유기", "웹 서버"))   # 122 366 610 854
SEG1, SEG2 = (164, 452), (572, 836)
TBL = (420, 468, 380, 88)                      # x, y, w, h
Y_RAILS = 852

ddx.band(d, *SEG1, "나갈 때 — 사설 주소와 포트를 공인 주소와 새 포트로 바꿔 적는다")
ddx.band(d, *SEG2, "돌아올 때 — 도착 포트만 보고 표에서 주인을 찾는다")
d.rails(Y_RAILS)

# 공유기 막대 — 두 구간에 걸쳐 한 번도 끊기지 않는다
d.o.append(f'<rect x="{GW-4}" y="200" width="8" height="612" rx="3" '
           f'fill="{MUTED}33" stroke="{MUTED}" stroke-width="0.8"/>')

def msg(a, b, y, label, sub, c, mk, dash=None):
    dirn = 1 if b > a else -1
    d.path(f"M {a+10*dirn} {y} L {b-12*dirn} {y}", c, 1.5, m=mk, dash=dash)
    mx = (a + b) // 2
    d.t(mx, y - 12, label, 12, c, MONO if all(ord(ch) < 128 for ch in label) else KR, "middle", 600)
    if sub: d.t(mx, y + 20, sub, 12, MUTED, KR)

# ① 나갈 때 — 내부 포트가 겹쳐도 밖에서는 다른 포트로 갈린다
msg(NB, GW, 220, "192.168.0.15:50000", "노트북이 연다", INFO, "info")
msg(GW, SV, 268, "공인IP:60001", "바꿔 적고 내보낸다", INFO, "info")
msg(PH, GW, 340, "192.168.0.16:50000", "내부 포트가 같아도 무관", INFO, "info")
msg(GW, SV, 388, "공인IP:60002", "다른 포트를 배정한다", INFO, "info")

# ② 그 사이에도 표는 지워지지 않는다 — 이 도식의 focal
tx, ty, tw, th = TBL
d.o.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(tx + tw // 2, ty + 22, "공유기 매핑 표 — 나갈 때 적어 둔 줄이 남아 있다", 12, ACC, KR, "middle", 600)
for i, (a, b) in enumerate([("192.168.0.15:50000", "공인IP:60001"),
                            ("192.168.0.16:50000", "공인IP:60002")]):
    y = ty + 46 + i * 24
    d.t(tx + 20, y, a, 11, INK, MONO, "start")
    d.t(tx + 190, y, "→", 11, MUTED, MONO)
    d.t(tx + tw - 20, y, b, 11, INK, MONO, "end")

# ③ 돌아올 때 — 도착 포트 하나로 주인을 가른다
msg(SV, GW, 628, "응답 → 공인IP:60001", None, OK, "ok", "6 5")
msg(GW, NB, 676, "표를 보고 노트북에게", None, OK, "ok", "6 5")
msg(SV, GW, 748, "응답 → 공인IP:60002", None, OK, "ok", "6 5")
msg(GW, PH, 796, "표를 보고 폰에게", None, OK, "ok", "6 5")

d.legend(Y_RAILS + 20, [("나가는 길", INFO), ("돌아오는 길", OK), ("지워지지 않는 표", ACC)])
d.save("01-03.nat-port-mapping.svg")
print("ok nat")
