# 01-04 §1 — 라우터 하나에서 패킷이 겪는 네 지연. 무엇에 달려 있는지가 성분마다 다르다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(성분 · 무엇에 달렸나 · 실무 자릿수)이 반복되고
#           화살표가 패킷이 겪는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 452
CW, CH, GAP, X0, Y = 216, 132, 20, 24, 140

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-04 §1",
      "라우터 하나에서 겪는 네 지연",
      "패킷이 노드 하나를 지나며 차례로 겪는 성분. 넷을 더한 것이 노드 지연이고, 네 성분은 각각 다른 것에 달려 있어 같이 움직이지 않는다.",
      "가변인 것은 큐잉 하나뿐입니다 — 나머지 셋은 조건이 같으면 값이 같습니다")

CARDS = [
    ("01", "처리 지연", "d(proc)", "헤더를 보고 나갈 링크를 정하고\n비트 오류를 검사합니다", "마이크로초 이하", None),
    ("02", "큐잉 지연", "d(queue)", "앞서 도착해 기다리는\n패킷 수에 달렸습니다", "마이크로초 ~ 밀리초", ACC),
    ("03", "전송 지연", "d(trans) = L/R", "패킷 길이와 링크 전송률.\n거리와는 무관합니다", "마이크로초 ~ 밀리초", None),
    ("04", "전파 지연", "d(prop) = d/s", "거리와 매체의 전파 속도.\n패킷 길이와는 무관합니다", "광역망에서 밀리초", None),
]

for i, (n, name, formula, why, scale, c) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.o.append(f'<rect x="{x + 14}" y="{Y + 14}" width="22" height="18" rx="9" '
               f'fill="{c if c else PAPER}" stroke="{c if c else RULE}" stroke-width="1"/>')
    d.t(x + 25, Y + 27, n, 9, PAPER if c else MUTED, MONO)
    d.t(x + 46, Y + 27, name, 12, c if c else INK, KR, "start", 600)
    d.t(x + 14, Y + 52, formula, 11, MUTED, MONO, "start")
    for j, line in enumerate(why.split("\n")):
        d.t(x + 14, Y + 76 + j * 18, line, 11, MUTED, KR, "start")
    d.t(x + 14, Y + CH - 14, scale, 11, SOFT, KR, "start")
    if i < 3:
        d.arrow([(x + CW, Y + CH / 2), (x + CW + GAP - 4, Y + CH / 2)], MUTED, "ar", 1.3)

d.t(X0, Y + CH + 44, "d(nodal) = d(proc) + d(queue) + d(trans) + d(prop)", 12, INK, MONO, "start", 600)
d.t(X0, Y + CH + 68, "전송 지연은 라우터가 패킷을 밀어내는 시간이고 전파 지연은 비트 하나가 건너가는 시간입니다 — 둘은 서로 다른 것에 달려 있습니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("패킷마다 달라지는 성분", ACC), ("조건이 같으면 값이 같은 성분", MUTED)])
d.save("01-04.nodal-delay.svg")
