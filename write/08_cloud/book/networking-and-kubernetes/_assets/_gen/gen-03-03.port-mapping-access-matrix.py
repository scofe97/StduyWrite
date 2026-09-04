# 03-03.port-mapping-access-matrix — 진짜 행렬
# 본문 요구: 다른 호스트에서 세 가지로 두드려 본 결과 — 두드린 곳마다 결과와 이유가 다르다
# 타입 스펙: type-dp-security-matrix.md — 행은 시도, 열은 결과·이유. 값이 세 줄뿐이어도
#   행렬은 행렬로 그린다. archify 시절 이 도식이 이름만 matrix 이고 그림은 화살표 세 쌍이었다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 604
d = D(W, H, "KNOCK FROM ANOTHER HOST · RESULT MATRIX",
      "다른 호스트에서 세 가지로 두드려 본 결과",
      "두드린 곳이 무엇이냐에 따라 실패의 종류가 다르다. 거부와 닿지 않음은 원인이 전혀 다른 실패다.",
      lead="두드린 곳에 따라 실패의 종류가 다르다 — 거부와 닿지 않음은 다른 실패다")

X0, COLS = 44, [(340, "두드린 곳"), (200, "결과"), (372, "왜 그런가")]
HDR_Y, ROW_H, GAP = 200, 84, 12
ROWS = [(("호스트IP:80", "192.168.1.20:80"), ("성공", OK), ("매핑이 받아 넘긴다", "80 → 8080")),
        (("호스트IP:8080", "192.168.1.20:8080"), ("거부", WARN), ("Connection refused", "TCP RST — 아무도 안 들음")),
        (("컨테이너IP", "172.17.0.2:any"), ("닿지 않음", BAD), ("메시지는 셋으로 갈린다", "경로 항목이 없다"))]

ddx.band(d, 104, 548, "실패가 두 종류라는 것이 이 표의 요점이다")
x = X0
XS = []
for w, name in COLS:
    XS.append((x, w))
    d.t(x + w // 2, HDR_Y, name, 11, SOFT, KR, "middle", 600)
    x += w + GAP

for r, ((t1, t2), (res, rc), (w1, w2)) in enumerate(ROWS):
    y = HDR_Y + 24 + r * (ROW_H + GAP)
    for i, (cx0, cw) in enumerate(XS):
        focal = (i == 1)
        c = rc if focal else RULE
        d.o.append(f'<rect x="{cx0}" y="{y}" width="{cw}" height="{ROW_H}" rx="6" '
                   f'fill="{rc+"12" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    (c0, w0) = XS[0]
    d.t(c0 + 20, y + 34, ddx.fit(t1, 13, w0 - 40, t1), 13, INK, KR, "start", 600)
    d.t(c0 + 20, y + 58, ddx.fit(t2, 11, w0 - 40, t2), 11, MUTED, MONO, "start")
    (c1, w1c) = XS[1]
    d.t(c1 + w1c // 2, y + 48, res, 15, rc, KR, "middle", 600)
    (c2, w2c) = XS[2]
    d.t(c2 + 20, y + 34, ddx.fit(w1, 12, w2c - 40, w1), 12, INK,
        MONO if all(ord(ch) < 128 for ch in w1) else KR, "start")
    d.t(c2 + 20, y + 58, ddx.fit(w2, 11, w2c - 40, w2), 11, MUTED, KR, "start")

d.t(36, 524, "거부는 그 주소까지 닿았으나 아무도 안 듣는다는 뜻이고, 닿지 않음은 그 주소로 "
             "보낼 경로가 없다는 뜻이다 — 사설 대역이어서가 아니라 경로 항목이 없어서다", 12, MUTED, KR, "start")
d.legend(564, [("성공", OK), ("거부 — 닿았으나 안 들음", WARN), ("닿지 않음 — 경로가 없다", BAD)])
d.save("03-03.port-mapping-access-matrix.svg")
print("ok port-mapping-access-matrix")
