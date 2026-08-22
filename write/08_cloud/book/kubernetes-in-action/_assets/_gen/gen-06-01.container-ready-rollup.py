# 06-01 §4 — 컨테이너별 ready 가 모여 Pod 전체 Ready 가 된다
# 본문: "하나라도 ready=false 이면 ContainersReady 가 False 가 되고, 따라서 Pod 전체 Ready
#        condition 도 False 가 됩니다. 즉 컨테이너별 ready 를 모두 종합해야 정해집니다."
#       "READY 1/2" · "Service 가 이 Pod 로 요청을 보내지 않습니다"
# 타입 스펙: 여럿이 하나로 모이는 종합(AND)이라 fan-in 이 요점이다. type-tree 의 관례를
#           뒤집어 쓴다 — 잎에서 뿌리로 모으고, 연결선은 직각 엘보로만 긋는다("never diagonal").
#           단계 머리를 얹어 ①②③ 이 어느 층인지 이름을 준다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 572
d = D(W, H, "KUBERNETES IN ACTION · 06-01",
      "컨테이너별 ready 가 모여야 Pod 전체 Ready 가 선다",
      "컨테이너 하나라도 ready=false 이면 AND 로 종합한 ContainersReady 가 False 가 되고, "
      "Pod 전체 Ready 도 False 가 되어 Service 가 이 Pod 로 트래픽을 보내지 않는다.",
      lead="하나라도 false 면 위로 전파된다 — READY 1/2 는 그 종합의 표시다")

BW, BH = 208, 76
C1, C2, C3 = 156, 480, 800
TOP, BOT, CY = 236, 348, 292
SPINE = 300

ddx.band(d, 104, 516, "컨테이너 ready 는 각자의 readiness probe(06-02)가 정하고, 종합은 AND 다")

for cx, s in ((C1, "① 컨테이너별 ready"), (C2, "② 종합 — AND"), (C3, "③ Pod 전체")):
    d.t(cx, 168, s, 12, SOFT, KR, "middle", 600)

def box(cx, cy, name, sub, c, focal=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, BW, BH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 8, ddx.fit(name, 12, BW - 16, name), 12, ACC if focal else c,
        MONO if all(ord(ch) < 128 for ch in name) else KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(sub, 10, BW - 14, name), 10, SOFT, KR)

box(C1, TOP, "ready-ok", "readiness probe 통과", OK)
box(C1, BOT, "ready-fail", "readiness probe 실패", BAD)
box(C2, CY, "ContainersReady", "하나라도 false 면 False", BAD)
box(C3, CY, "Ready", "Service 가 트래픽을 안 보낸다", BAD, focal=True)

# fan-in — 잎 둘이 줄기 하나로 모인다. 직각으로만 꺾는다.
# 팔에는 화살촉을 달지 않는다 — 줄기로 합류할 뿐 도착지가 아니라, 촉을 달면 허공을
# 가리킨다. 합류점은 type-flowchart 의 관례대로 작은 채운 점으로 찍는다.
for cy, c in ((TOP, OK), (BOT, BAD)):
    d.path(f"M {C1+BW//2+6} {cy} L {SPINE} {cy}", c, 1.4)
d.path(f"M {SPINE} {TOP} L {SPINE} {BOT}", MUTED, 1.4)
d.o.append(f'<circle cx="{SPINE}" cy="{CY}" r="4" fill="{INK}"/>')
d.path(f"M {SPINE} {CY} L {C2-BW//2-8} {CY}", MUTED, 1.5, m="ar")
d.chip(348, CY, "AND", MUTED, 11)

d.path(f"M {C2+BW//2+6} {CY} L {C3-BW//2-8} {CY}", MUTED, 1.5, m="ar")
# 코리도어는 112px 뿐이다 — "readiness gate 까지 더해"(159px)는 왼쪽 상자를 24px 덮는다
d.t((C2 + C3) // 2, CY - 16, "readiness gate", 11, MUTED, MONO)

d.chip(C3, 412, "READY  1/2", BAD, 12)
d.path(f"M {C3} {CY+BH//2+6} L {C3} 400", RULE, 1.2, dash="4 5")

d.t(36, 466, "둘 다 ready=true 였다면 ContainersReady 도 Ready 도 True 가 되어 READY 2/2 가 되고, "
             "그때만 Service 가 이 Pod 로 트래픽을 보낸다", 12, MUTED, KR, "start")
d.legend(532, [("ready=true", OK), ("ready=false 와 그 전파", BAD), ("본문이 짚는 자리", ACC)])
d.save("06-01-container-ready-rollup.svg")
print("ok container-ready-rollup")
