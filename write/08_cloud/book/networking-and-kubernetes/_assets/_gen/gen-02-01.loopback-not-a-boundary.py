# 02-01.loopback-not-a-boundary — 밖에서 경계를 넘어온 길
# 본문: "점선 안이 '로컬 전용'이라 믿는 구간. 노드 설정 하나가 그 안으로 들어가는 길을
#        열어 준 것이 CVE-2020-8558 이다."
# 타입 스펙: type-flowchart.md 의 단선 경로 + type-nested.md 의 경계 링.
#           경로가 링을 밖에서 뚫고 들어가는 자리 하나에만 focal 을 건다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 560
d = D(W, H, "CVE-2020-8558 · 127.0.0.1 IS NOT A FENCE",
      "127.0.0.1 은 접근 제어가 아니다 — 밖에서 경계를 넘어온 길",
      "점선 안이 '로컬 전용'이라 믿는 구간이다. 노드 설정 하나가 그 안으로 들어가는 길을 열어 줬다.",
      lead="점선 안이 '로컬 전용'이라 믿는 구간 · 설정 하나가 그 안으로 들어가는 길을 열었다")

BW, BH, GAP = 164, 104, 24
CX = [42 + BW // 2 + i * (BW + GAP) for i in range(5)]           # 124 312 500 688 876
CY = 300
RING = (CX[3] - BW // 2 - 22, 212, (CX[4] + BW // 2 + 22) - (CX[3] - BW // 2 - 22), 176)
NODES = [("인접 호스트", "같은 네트워크의 옆 기계", "노드 밖에 있다", INFO, False),
         ("노드 NIC", "평범한 패킷 도착", "여기까진 정상", None, False),
         ("노드 설정", "로컬 주소로 가는 길 허용", "CVE-2020-8558", None, True),
         ("lo · 127.0.0.1", "호스트를 안 떠난다는 주소", "그런데 밖에서 닿았다", None, False),
         ("8080 서비스", "127.0.0.1 에 바인딩", "로컬 전용이라 믿었다", BAD, False)]
EDGE = ["도착", "판단", "허용", ""]

ddx.band(d, 104, 512, "주소가 로컬이라는 사실과 밖에서 못 닿는다는 보장은 다른 말이다")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "로컬 전용이라 믿는 구간", 11, INFO, off=16)

for cx, (l, s, t, c, focal) in zip(CX, NODES):
    x, y = cx - BW // 2, CY - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, CY - 22, ddx.fit(l, 12, BW - 14, l), 12, tc, KR, "middle", 600)
    d.t(cx, CY + 0, ddx.fit(s, 11, BW - 12, s), 11, MUTED, KR)
    d.t(cx, CY + 26, ddx.fit(t, 10, BW - 10, t), 10, ACC if focal else SOFT, KR)

for i, lab in enumerate(EDGE):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    c = ACC if i == 2 else MUTED                                 # 링을 뚫고 들어가는 그 한 걸음
    d.path(f"M {a+6} {CY} L {b-8} {CY}", c, 1.8 if c is ACC else 1.5, m="acc" if c is ACC else "ar")
    if lab: d.t((a + b) // 2, CY - BH // 2 - 12, lab, 10, c, KR)
d.t((CX[2] + CX[3]) // 2, CY + BH // 2 + 26, "여기서 경계가 뚫린다", 11, ACC, KR)

d.t(36, 476, "주소가 로컬이라고 해서 밖에서 못 닿는 것은 아니다 — 닿을 수 있게 하는 설정이 "
             "따로 있었고, 그것이 이 취약점의 전부다", 12, MUTED, KR, "start")
d.legend(528, [("노드 밖", INFO), ("로컬 전용이라 믿었다", BAD), ("길을 연 설정", ACC)])
d.save("02-01.loopback-not-a-boundary.svg")
print("ok loopback-not-a-boundary")
