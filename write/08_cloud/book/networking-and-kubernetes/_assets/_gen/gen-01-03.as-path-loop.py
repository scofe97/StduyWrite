# 01-03.as-path-loop — 순환 경로 + 자기 번호 검출
# 본문: "받은 쪽은 자기 번호를 목록 맨 앞에 붙여 다시 넘긴다. 한 바퀴를 돌면
#        처음 내보낸 곳으로 되돌아오고, 그때 목록에 이미 200 이 들어 있다."
# 타입 스펙: type-loop.md — 고리는 삼각으로 놓고 각 변에 그 시점의 목록을 칩으로 붙인다.
#           고리를 닫는 변 하나에만 상태색을 준다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 588
d = D(W, H, "BGP · AS_PATH LOOP DETECTION",
      "AS 목록이 돌아왔다 — 자기 번호가 이미 들어 있다",
      "받은 쪽은 자기 번호를 목록 맨 앞에 붙여 다시 넘긴다. 한 바퀴를 돌면 처음 내보낸 곳으로 되돌아온다.",
      lead="자기 번호를 목록 맨 앞에 붙여 넘기므로, 한 바퀴 돌면 자기 번호가 목록에 있다")

BW, BH = 200, 100
A200, A400, A500 = (500, 244), (784, 432), (216, 432)

def asbox(cx, cy, name, sub, tag, c=None):
    x, y = cx - BW // 2, cy - BH // 2
    d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 20, name, 14, c or INK, KR, "middle", 600)
    d.t(cx, cy + 2, ddx.fit(sub, 11, BW - 20, sub), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 11, BW - 16, tag), 11, SOFT, KR)

ddx.band(d, 104, 532, "한 바퀴 뒤 목록에 남는 고리의 증거")
ddx.focal_tag(d, 500, 152, "목록에 내 번호 → 수신 거부", 300)

asbox(*A200, "AS 200", "내보낼 때 [200]", "다시 도착", ACC)
asbox(*A400, "AS 400", "받아서 [400, 200]", "앞에 자기 번호")
asbox(*A500, "AS 500", "받아서 [500, 400, 200]", "앞에 자기 번호")

# 고리 세 변 — 목록은 변 위의 칩으로
# 두 빗변은 직각으로 편다. 꺾는 열을 A400·A500 의 중심 열로 잡아 세로 구간이
# 서로 다른 열에 서고, 가로 구간은 A200 상자를 사이에 두고 겹치지 않는다.
d.path(f"M {A200[0]+BW//2+8} {A200[1]} L {A400[0]} {A200[1]} L {A400[0]} {A400[1]-BH//2-8}",
       MUTED, 1.6, m="ar")
d.chip(A400[0], 312, "[200]", INFO, 12)
d.path(f"M {A400[0]-BW//2-8} {A400[1]} L {A500[0]+BW//2+10} {A500[1]}", MUTED, 1.6, m="ar")
d.chip(500, 404, "[400, 200]", INFO, 12)
d.path(f"M {A500[0]} {A500[1]-BH//2-8} L {A500[0]} {A200[1]} L {A200[0]-BW//2-8} {A200[1]}",
       BAD, 1.8, m="bad")
d.chip(A500[0], 312, "[500, 400, 200]", BAD, 12)

d.t(500, 352, "자기 번호를 목록 맨 앞에 붙여 전달", 12, MUTED, KR)
# 하단 해설(같은 AS 안에서는 목록이 안 자라 iBGP 는 재전달 금지)은 본문 §3 iBGP 대목이 같은 말로 적는다 — 뺐다
d.legend(548, [("넘겨지는 목록", INFO), ("고리를 닫는 변", BAD), ("여기서 알아본다", ACC)])
d.save("01-03.as-path-loop.svg")
print("ok as-path-loop")
