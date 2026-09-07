# 03-05 §3 — 혼잡 제어 갈래를 두 축으로 놓은 것. 축은 원문 3.7 이 갈래를 소개하는 두 기준이다.
#   가로 = 무엇을 혼잡의 신호로 삼나 (손실 ↔ 지연·대역폭)
#   세로 = 그 신호를 어떻게 얻나 (추론 ↔ 망이 명시적으로 알려 줌)
# 배치는 원문 3.7.1~3.7.3 의 서술을 이 두 축에 옮긴 것이고, 각 갈래의 성질은 원문 그대로다.
# 타입 스펙: type-quadrant — 두 축이 만드는 2x2 위에 항목을 점으로 놓는다. 축 라벨은 끝점 하나에 한 단어.
#           dd.py 의 마커는 marker-end 만 있으므로 중심에서 바깥으로 나가는 경로 넷으로 양끝 화살표를 만든다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 636
CX, CY = 500, 306
XL, XR, YT, YB = 150, 850, 148, 470

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-05 §3",
      "무엇을 신호로 삼느냐로 갈립니다",
      "혼잡 제어 갈래를 두 축에 놓은 것. 신호가 손실이냐 지연이냐, 그리고 그것을 추론하느냐 망이 알려 주느냐로 나뉜다.",
      "2024년 기준 BBR 이 나머지를 합친 것보다 많이 쓰입니다")

for x2, y2 in ((XR, CY), (XL, CY), (CX, YT), (CX, YB)):
    d.path(f"M {CX} {CY} L {x2} {y2}", MUTED, 1.2, m="ar")

def axlabel(x, y, txt, anchor):
    d.o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" '
               f'font-size="9" letter-spacing="0.18em" fill="{INK}">{txt}</text>')

axlabel(CX, YT - 14, "EXPLICIT", "middle")
axlabel(CX, YB + 26, "INFERRED", "middle")
axlabel(XL - 14, CY + 4, "LOSS", "end")
axlabel(XR + 14, CY + 4, "DELAY", "start")

ITEMS = [
    (250, 400, "Classic (Reno)", "손실 · AIMD", False),
    (330, 452, "CUBIC", "손실 · 세제곱 증가", False),
    (662, 420, "Vegas", "RTT 로 큐 형성 감지", False),
    (742, 366, "BBR", "대역폭·RTT · 2024년 최다", True),
    (300, 214, "ECN", "라우터가 표시 · 서버 80% 이상 지원", False),
    (392, 262, "DCTCP", "데이터센터용 · ECN 기반", False),
]
for x, y, name, sub, focal in ITEMS:
    c = ACC if focal else MUTED
    d.o.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
    d.t(x, y - 14, name, 11, INK if focal else MUTED, KR, "middle", 600 if focal else 400)
    d.t(x, y + 20, sub, 11, SOFT, KR)

d.box(596, 176, 300, 84, PAPER2, RULE, 0.9, 6)
d.t(746, 204, "여기가 비어 있는 이유", 11, SOFT, KR)
d.t(746, 226, "망이 지연을 직접 알려 주는 방식은", 11, SOFT, KR)
d.t(746, 244, "표준으로 배포된 것이 없습니다", 11, SOFT, KR)

d.t(20, 522, "손실은 이미 버퍼가 넘친 뒤에야 생기므로 알았을 때는 늦습니다. 지연 기반과 망 보조는 둘 다 그 늦음을 앞당기려는 시도입니다.",
     11, MUTED, KR, "start")
d.t(20, 544, "무선처럼 혼잡이 아닌 이유로 손실이 나는 경로에서는 손실 기반이 멀쩡한데도 물러섭니다. BBR 이 그 함정을 피합니다.",
     11, MUTED, KR, "start")

d.legend(H - 52, [("지금 가장 많이 쓰이는 갈래", ACC), ("나머지", MUTED)])
d.save("03-05.cc-flavors.svg")
