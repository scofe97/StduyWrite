# 00-03-hop-header-matrix — 구간을 건널 때마다 무엇이 바뀌고 무엇이 남는가
# 본문 요구: "네 줄 중 한 줄만 처음 값 그대로 도착한다" — 목적지 IP 행이 그 한 줄이라 focal.
# 타입 스펙: type-dp-security-matrix.md — 행이 헤더 네 필드, 열이 구간 셋. 같은 행을 가로로
#           읽으면 그 필드가 몇 번 바뀌는지가 나오고, 그 대조가 이 도식의 전부다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 588
X0, XW, ROW_H, Y0 = 60, 908, 68, 152
COLS = [276, 512, 748]
HEADS = ["구간 1 · 노트북 → 공유기", "구간 2 · 공유기 → ISP 라우터", "구간 3 · 라우터 → 웹 서버"]
ROWS = [("출발지 MAC", INFO, False,
         [("AA:BB:CC:00:00:01", "내 노트북 NIC"), ("AA:BB:CC:00:00:02", "공유기 WAN"), ("AA:BB:CC:00:00:03", "마지막 라우터")]),
        ("목적지 MAC", INFO, False,
         [("AA:BB:CC:00:00:02", "공유기 LAN"), ("AA:BB:CC:00:00:03", "마지막 라우터"), ("AA:BB:CC:00:00:04", "웹 서버 NIC")]),
        ("출발지 IP", WARN, False,
         [("192.168.0.15", "사설 주소"), ("203.0.113.7", "NAT 이 바꿔 적음"), ("203.0.113.7", "그대로")]),
        ("목적지 IP", OK, True,
         [("93.184.216.34", "처음부터"), ("93.184.216.34", "그대로"), ("93.184.216.34", "끝까지 그대로")])]

d = D(W, H, "COMPARISON MATRIX · WHAT SURVIVES",
      "구간을 건널 때마다 무엇이 바뀌고 무엇이 남는가",
      "구간 세 개를 세로 열로, 헤더 네 필드를 가로 행으로 놓은 비교 행렬. MAC 두 줄은 구간마다 값이 "
      "바뀌고, 목적지 IP 한 줄만 끝까지 같은 값을 유지한다.",
      lead="같은 요청 한 장을 세 구간에서 각각 뜯어 본 것입니다. 네 줄 중 한 줄만 처음 값 그대로 도착합니다.")

d.o.append(f'<rect x="{X0}" y="132" width="{XW}" height="48" fill="{PAPER2}"/>')
for cx, head in zip(COLS, HEADS):
    d.t(cx, 162, head, 12, MUTED, KR, "start")

for r, (name, c, focal, cells) in enumerate(ROWS):
    y = 180 + r * ROW_H
    if focal:
        d.tone(X0, y, XW, ROW_H, ACC, 0, "12", 1.2)
    d.line(X0, y, X0 + XW, y, RULE, 0.8)
    d.t(X0 + 16, y + 40, name, 14, INK, KR, "start", 600)
    for cx, (val, who) in zip(COLS, cells):
        d.t(cx, y + 30, val, 11, c, MONO, "start")
        d.t(cx, y + 52, who, 12, MUTED, KR, "start")

d.t(X0, 496, "바뀌는 것은 겉봉(MAC)이고, 어디로 가는지(목적지 IP)는 처음 적힌 값이 끝까지 갑니다.",
    12, MUTED, KR, "start")
d.legend(516, [("구간마다 새로 쓰인다", INFO), ("NAT 지점에서 한 번 바뀐다", WARN), ("끝까지 그대로다", OK)])
d.save("00-03-hop-header-matrix.svg")
print("ok hop-header-matrix")
