# 02-01.loopback-not-a-boundary — 밖에서 경계를 넘어온 길
# 본문: "점선 안이 '로컬 전용'이라 믿는 구간. 노드 설정 하나가 그 안으로 들어가는 길을
#        열어 준 것이 CVE-2020-8558 이다."
# 타입 스펙: type-architecture.md — 인접 호스트 · 노드 NIC · 노드 설정 · lo · 서비스를 잇는 구성도. 점선 사각형이 '로컬 전용이라 믿는 구간'을 표시하는데, architecture 정본이 신뢰 경계를 그렇게 그리라고 적은 그 문법이다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 512
d = D(W, H, "CVE-2020-8558 · 127.0.0.1 IS NOT A FENCE",
      "127.0.0.1 은 접근 제어가 아니다 — 밖에서 경계를 넘어온 길",
      "점선 안이 '로컬 전용'이라 믿는 구간이다. 노드 설정 하나가 그 안으로 들어가는 길을 열어 줬다.",
      lead="점선 안이 '로컬 전용'이라 믿는 구간 · 설정 하나가 그 안으로 들어가는 길을 열었다")

# 2026-09-18 통로 24 → 48px. 폭을 넓히면 본문에서 글자가 작아지므로(스타일 계약 §캔버스 폭)
#            카드 폭을 164 → 152 로 줄여 통로를 얻는다. 카드 두 줄(부제·꼬리표)은 11px 이라
#            안쪽 여백을 10px 로 맞춘다 — 가장 긴 부제가 141px 이라 12px 여백으로는 넘친다.
BW, BH, GAP = 152, 104, 48
CX = [24 + BW // 2 + i * (BW + GAP) for i in range(5)]           # 100 300 500 700 900
CY = 300
# 링 왼쪽 테두리는 셋째·넷째 카드 사이 통로의 한가운데(600)를 지난다 — 카드를 자르지 않는다.
RING = (600, 212, (CX[4] + BW // 2 + 12) - 600, 176)
NODES = [("인접 호스트", "같은 네트워크의 옆 기계", "노드 밖", INFO, False),
         ("노드 NIC", "평범한 패킷 도착", "여기까진 정상", None, False),
         ("노드 설정", "로컬 주소로 가는 길 허용", "CVE-2020-8558", None, True),
         ("lo · 127.0.0.1", "호스트를 안 떠난다는 주소", "밖에서 도달", None, False),
         ("8080 서비스", "127.0.0.1 에 바인딩", "로컬 전용이라는 믿음", BAD, False)]
# 링 경계(x=584)가 세 번째 통로 한가운데를 지난다 — 그 통로 위아래 라벨은 테두리를 가로지르므로 비운다
EDGE = ["도착", "판단", "", ""]

ddx.band(d, 104, 440, "로컬 주소 ≠ 밖에서 못 닿음", x=12, w=980)
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
    d.t(cx, CY + 0, ddx.fit(s, 11, BW - 10, s), 11, MUTED, KR)
    d.t(cx, CY + 26, ddx.fit(t, 11, BW - 10, t), 11, ACC if focal else SOFT, KR)

for i, lab in enumerate(EDGE):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    c = ACC if i == 2 else MUTED                                 # 링을 뚫고 들어가는 그 한 걸음
    d.path(f"M {a+6} {CY} L {b-8} {CY}", c, 1.8 if c is ACC else 1.5, m="acc" if c is ACC else "ar")
    if lab: d.t((a + b) // 2, CY - BH // 2 - 12, lab, 11, c, KR)
# 링 아래로 내린다 — 링 세로 테두리는 ry+rh 에서 끝나므로 그 아래에는 가로지를 선이 없다
d.t(rx, ry + rh + 24, "경계가 뚫리는 자리", 12, ACC, KR)

d.legend(456, [("노드 밖", INFO), ("로컬 전용이라는 믿음", BAD), ("길을 연 설정", ACC)])
d.save("02-01.loopback-not-a-boundary.svg")
print("ok loopback-not-a-boundary")
