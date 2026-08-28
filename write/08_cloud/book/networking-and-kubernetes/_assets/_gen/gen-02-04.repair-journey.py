# 02-04.repair-journey — 실패와 조치가 세 번 오간 전체 흐름
# 본문 요구: §4 는 세 실패를 하나씩 해부하지만, 그것들이 '한 번에 하나씩 좁혀 간' 연속이라는
#           사실은 절 어디에도 한눈에 안 보인다. 이 도식이 절의 리드로 그 연속을 편다.
# 타입 스펙: type-swimlane.md — 주체 둘(커널 / 나)을 가로지르며 넘겨받는 절차다.
#           커널이 문구를 던지면 내가 고치고, 고치면 커널이 다음 문구를 던진다.
#           연결선은 직각 엘보만 쓴다. focal 은 마지막 관측 하나.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 620
d = D(W, H, "REPAIR JOURNEY · THREE ROUNDS",
      "커널이 문구를 던지고 내가 고치기를 세 번 반복했다",
      "실패할 때마다 커널이 다른 문구를 냈고, 문구마다 볼 테이블이 달랐습니다. "
      "한 번에 하나씩 좁혀 세 번 만에 통했습니다.",
      lead="문구가 바뀔 때마다 파야 할 자리도 바뀐다")

LBL_X, BODY_X = 40, 216
TOP_CY, BOT_CY = 268, 412
BW, BH = 168, 84
CX = [300, 492, 684, 876]

for cy, name, sub, c in ((TOP_CY, "커널이 말한 것", "관측", INFO), (BOT_CY, "내가 한 것", "조치", MUTED)):
    d.o.append(f'<rect x="{LBL_X}" y="{cy-66}" width="{W-80}" height="132" rx="8" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
    d.line(BODY_X - 16, cy - 66, BODY_X - 16, cy + 66, RULE, 0.9)
    d.t(LBL_X + 20, cy - 6, name, 13, INK, KR, "start", 600)
    d.t(LBL_X + 20, cy + 16, sub, 11, c, MONO, "start")

def box(cx, cy, t, s, c=None, focal=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, BW, BH, PAPER, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 8, ddx.fit(t, 11, BW - 12, t), 11, tc,
        MONO if all(ord(ch) < 128 or ch in ' ·→' for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(s, 11, BW - 12, s), 11, MUTED, KR)

TOP = [("Network is", "unreachable · 라우팅"), ("Destination Host", "Unreachable · ARP"),
       ("conntrack -L → 0건", "추적이 안 켜짐")]
BOT = [("default 경로 추가", "ns1 에"), ("br0 주소 교정", "10.0.1.1 오타"),
       ("-m conntrack 추가", "규칙이 추적을 요구")]

# 연결선 먼저
for i in range(3):
    d.path(f"M {CX[i]} {TOP_CY+BH//2} L {CX[i]} {BOT_CY-BH//2-8}", MUTED, 1.4, m="ar")
    mid = (CX[i] + CX[i + 1]) // 2
    d.path(f"M {CX[i]+BW//2} {BOT_CY} L {mid} {BOT_CY} L {mid} {TOP_CY} L {CX[i+1]-BW//2-8} {TOP_CY}",
           MUTED, 1.4, m="ar")

for i in range(3):
    box(CX[i], TOP_CY, *TOP[i], c=INFO)
    box(CX[i], BOT_CY, *BOT[i])
box(CX[3], TOP_CY, "통했다", "엔트리 1건 · TTL 63", focal=True)

d.t(36, 524, "세 문구가 각각 다른 테이블을 가리켰습니다 — 라우팅 테이블, 이웃 테이블, 그리고 규칙 목록입니다.",
    12, MUTED, KR, "start")
d.t(36, 546, "아래 사다리가 그 대응을 정리한 지도이고, 이 그림은 실제로 밟은 순서입니다.",
    12, MUTED, KR, "start")
d.legend(560, [("커널이 낸 문구", INFO), ("마지막 관측", ACC)])
d.save("02-04.repair-journey.svg")
print("ok repair-journey")
