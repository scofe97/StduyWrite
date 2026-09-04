# 01-03.default-route-chain — 라우팅 표 순차 대조
# 본문: "초록 화살표가 0.0.0.0/0 칸에서 출발한다"
#        표에서 어느 줄에 걸리느냐가 다음 행선지를 정한다 · 좁은 줄에 걸리면 집 안에서 끝나고,
#        아무 데도 안 걸려 0.0.0.0/0 으로 내려오면 그때 밖으로 나간다
# 타입 스펙: type-flowchart.md 의 분기 + 표 조회를 행 대조로.
#           걸리는 줄 하나에만 focal — 거기서 사슬이 시작된다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 820
d = D(W, H, "DEFAULT ROUTE · PASS IT UP",
      "모르면 위로 떠넘기기 — 그 사슬은 어디서 끝나는가",
      "표에서 어느 줄에 걸리느냐가 다음 행선지를 정한다. 좁은 줄에 걸리면 집 안에서 끝나고, 0.0.0.0/0 까지 내려오면 그때 밖으로 나간다.",
      lead="좁은 줄에 걸리면 집 안에서 끝나고, 0.0.0.0/0 까지 내려오면 밖으로 나간다")

BW, BH = 232, 92
CHX = 176
NB, HOME, ISP = (CHX, 206), (CHX, 340), (CHX, 500)
TOPR = (150, 640, 180, 92)
NBR  = (400, 640, 180, 92)
TBL  = (452, 262, 500, 168)
LAN  = (760, 500, 200, 92)
GNET, DNS = (660, 640, 180, 92), (872, 640, 180, 92)
RING = (44, 584, 520, 132)

def box(cx, cy, w, h, title, sub, tag, c=None, dash=False):
    x, y = cx - w // 2, cy - h // 2
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER2}" '
               f'stroke="{c or RULE}" stroke-width="1.1"{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(cx, cy - 16, title, 13, c or INK, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(sub, 11, w - 18, sub), 11, MUTED,
        MONO if all(ord(ch) < 128 for ch in sub) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 11, w - 14, tag), 11, SOFT, KR)

ddx.band(d, 104, 764, "모르면 위로 — 그러나 꼭대기에는 떠넘길 위가 없다")

# ── 떠넘기기 사슬 ─────────────────────────────────────────
box(*NB, BW, BH, "내 노트북", "10.0.0.5", "출발")
box(*HOME, BW, BH, "집 공유기", "표는 두세 줄뿐", "모르면 위로")
box(*ISP, BW, BH, "지역 ISP", "고객 대역만 안다", "모르면 위로")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "꼭대기 — 떠넘길 위가 없는 자리", 11, INFO, off=260)
box(*TOPR, "상위 사업자", "기본 경로가 없다", "전체 표 보유", INFO)
box(*NBR,  "이웃 사업자", "대등한 관계", "전체 표 보유", INFO)

d.path(f"M {CHX} {NB[1]+BH//2+6} L {CHX} {HOME[1]-BH//2-10}", MUTED, 1.5, m="ar")
d.path(f"M {CHX} {ISP[1]+BH//2+6} L {CHX} {TOPR[1]-TOPR[3]//2-10}", MUTED, 1.5, m="ar")
d.path(f"M {TOPR[0]+TOPR[2]//2+8} {TOPR[1]} L {NBR[0]-NBR[2]//2-10} {NBR[1]}", MUTED, 1.4, m="ar")
d.t((TOPR[0]+NBR[0])//2, TOPR[1]-24, ddx.fit("경로 광고", 11, NBR[0]-NBR[2]//2 - (TOPR[0]+TOPR[2]//2) - 8, "gap"), 11, MUTED, KR)

# ── 집 공유기의 표 — 걸리는 줄이 다음 행선지를 정한다 ─────
tx, ty, tw, th = TBL
d.box(tx, ty, tw, th, PAPER2, RULE, 1.1, 8)
d.t(tx + 16, ty + 26, "집 공유기의 라우팅 표 — 위에서부터 좁은 줄이 이긴다", 12, SOFT, KR, "start")
d.path(f"M {CHX+BW//2+8} {HOME[1]} L {tx-10} {HOME[1]}", MUTED, 1.5, m="ar")
ROWS = [(ty + 46, "10.0.0.0/24", "집 안 쪽 문", "8.8.8.8 안 걸림", SOFT, False),
        (ty + 106, "0.0.0.0/0",  "ISP 쪽 문",   "여기 걸린다",    ACC,  True)]
for ry_, cidr, door, note, c, focal in ROWS:
    if focal:
        d.o.append(f'<rect x="{tx+12}" y="{ry_}" width="{tw-24}" height="48" rx="5" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(tx + 12, ry_, tw - 24, 48, PAPER, RULE, 1.0, 5)
    d.t(tx + 28, ry_ + 30, cidr, 12, c, MONO, "start", 600)
    d.t(tx + 168, ry_ + 30, f"-> {door}", 11, c if focal else MUTED, KR, "start")
    d.t(tx + tw - 28, ry_ + 30, note, 11, c if focal else SOFT, KR, "end")

box(*LAN, "집 안 기기", "10.0.0.x 라면", "여기서 끝난다", dash=True)
d.path(f"M {tx+tw-90} {ty+94} L {tx+tw-90} {LAN[1]-46-10}", MUTED, 1.3, m="ar", dash="5 5")
# 0.0.0.0/0 에서 사슬이 시작된다
d.path(f"M {tx+40} {ty+154} L {tx+40} {ISP[1]} L {CHX+BW//2+10} {ISP[1]}", ACC, 1.8, m="acc")
d.t(tx + 56, ISP[1] - 14, "여기서 밖으로 나간다", 11, ACC, KR, "start")

box(*GNET, "구글 쪽 망", "8.8.8.0/24 광고", "여기가 주인", OK)
box(*DNS,  "8.8.8.8", "목적지 호스트", "도착", OK)
d.path(f"M {NBR[0]+NBR[2]//2+8} {NBR[1]} L {GNET[0]-GNET[2]//2-10} {GNET[1]}", MUTED, 1.4, m="ar")
d.path(f"M {GNET[0]+GNET[2]//2+8} {GNET[1]} L {DNS[0]-DNS[2]//2-10} {DNS[1]}", OK, 1.5, m="ok")

d.t(36, 744, "꼭대기 사업자들은 기본 경로를 두지 않는다 — 떠넘길 위가 없으니 전체 표를 갖고 "
             "직접 고를 수밖에 없다", 12, MUTED, KR, "start")
d.legend(780, [("전체 표 보유", INFO), ("도착", OK), ("걸리는 줄", ACC)])
d.save("01-03.default-route-chain.svg")
print("ok default-route-chain")
