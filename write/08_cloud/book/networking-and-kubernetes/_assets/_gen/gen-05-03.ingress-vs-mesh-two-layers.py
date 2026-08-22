# 05-03.ingress-vs-mesh-two-layers — 방향이 다른 두 L7 인프라
# 본문 요구: Ingress 는 밖→안, 메시는 안↔안. 컨트롤 플레인이 죽어도 데이터 플레인은 돈다.
# 타입 스펙: type-nested.md 클러스터 경계 + 방향이 다른 두 색. 색이 곧 방향이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 660
d = D(W, H, "TWO L7 LAYERS · DIFFERENT DIRECTIONS",
      "트래픽 방향이 다른 두 L7 인프라",
      "Ingress 는 밖에서 안으로 들어오는 길을 맡고, 메시는 안쪽끼리 오가는 길을 사이드카가 맡는다.",
      lead="Ingress 는 밖→안, 메시는 안↔안 — 색이 곧 방향이다")

BW, BH = 196, 108
EXT = (108, 300)
RING = (232, 200, 728, 340)
ING, SVA, SVB = (356, 300), (598, 300), (840, 300)
CPL = (720, 452)

def box(cx, cy, t, s, tag, c=None, w=BW, dash=False):
    x, y = cx - w // 2, cy - BH // 2
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="6" fill="{PAPER2}" '
               f'stroke="{c or RULE}" stroke-width="1.1"{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(cx, cy - 22, ddx.fit(t, 13, w - 18, t), 13, c or INK, KR, "middle", 600)
    d.t(cx, cy + 0, ddx.fit(s, 11, w - 16, s), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, tag), 10, SOFT, KR)

ddx.band(d, 104, 600, "컨트롤 플레인이 죽어도 사이드카는 이미 받은 설정으로 계속 돈다")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "Kubernetes 클러스터 — 안쪽 통신은 사이드카가 맡는다", 11, INFO, off=16)

box(*EXT, "외부 클라이언트", "HTTP(S) 요청", "클러스터 밖", INFO, w=160)
box(*ING, "Ingress", "host·path fan-out", "밖 → 안 L7 라우터", INFO)
box(*SVA, "서비스 A", "app + 사이드카", "프록시가 mTLS 를 건다", ACC)
box(*SVB, "서비스 B", "app + 사이드카", "재시도·관측·라우팅 대행", ACC)
box(*CPL, "메시 컨트롤 플레인", "사이드카에 설정 배포", "죽어도 데이터 플레인은 동작", MUTED, w=280, dash=True)

d.path(f"M {EXT[0]+80+6} {EXT[1]} L {ING[0]-BW//2-10} {ING[1]}", INFO, 1.6, m="info")
d.t(rx - 6, EXT[1] - 16, "밖에서 안으로", 10, INFO, KR, "end")
d.path(f"M {ING[0]+BW//2+6} {ING[1]} L {SVA[0]-BW//2-10} {SVA[1]}", INFO, 1.6, m="info")
d.path(f"M {SVA[0]+BW//2+6} {SVA[1]} L {SVB[0]-BW//2-10} {SVB[1]}", ACC, 1.8, m="acc")
d.t((SVA[0] + SVB[0]) // 2, SVA[1] - 16, "안쪽끼리", 10, ACC, KR)
# 컨트롤 플레인 상자(580~860)가 서비스 A(598)·B(840)의 중심 x 를 둘 다 품으므로
# 꺾을 것 없이 그 두 열에서 곧게 올린다. '설정 배포' 라벨은 두 열 사이(720)에 있다.
for t in (SVA, SVB):
    d.path(f"M {t[0]} {CPL[1]-54-6} L {t[0]} {t[1]+BH//2+10}", MUTED, 1.3, m="ar", dash="5 5")
d.t(CPL[0], CPL[1] - 74, "설정 배포", 10, MUTED, KR)

d.t(36, 572, "같은 L7 이라도 방향이 다르다 — Ingress 는 진입 하나를 맡고, 메시는 서비스 사이 "
             "모든 홉에 프록시를 하나씩 붙인다", 12, MUTED, KR, "start")
d.legend(616, [("밖 → 안", INFO), ("안 ↔ 안", ACC)])
d.save("05-03.ingress-vs-mesh-two-layers.svg")
print("ok ingress-vs-mesh-two-layers")
