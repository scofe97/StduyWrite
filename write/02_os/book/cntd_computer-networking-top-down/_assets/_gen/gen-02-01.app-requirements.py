# 02-01 §3 — 원문 Figure 2.4 "Requirements of selected network applications" 를 사분면으로 다시 놓은 것.
# 표의 값은 그림에서 판독한 원문 그대로이고(손실 불가/손실 내성, 시간 민감 여부), 배치만 바꿨다.
# 오른쪽 아래 칸이 비는 것은 표에 그 조합의 앱이 없기 때문이며, 그 공백이 이 도식의 요점이다.
# 타입 스펙: type-quadrant — 두 축이 만드는 2x2 위에 항목을 점으로 놓는다. 축 라벨은 끝점 하나에 한 단어.
#
# 스펙에서 둘을 조정했다.
#  (1) 축을 양끝 화살표로 그렸다. 스펙의 표준 사분면은 단방향이고 양방향은 consultant 변형의 표식이지만,
#      여기서는 양극이 모두 원문의 *명명된 범주*(손실 불가 / 손실 내성)이지 "적음/많음"이 아니라 양끝을 찍었다.
#      dd.py 의 마커는 marker-end 만 있으므로 중심에서 바깥으로 나가는 경로 넷으로 그린다.
#  (2) 축선 색은 INK 대신 MUTED 다. 어두운 지면에서 INK 는 거의 흰색이라 항목 점보다 강해진다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 648
CX, CY = 500, 320
XL, XR, YT, YB = 150, 850, 140, 500

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §3",
      "앱이 트랜스포트에 요구하는 것",
      "원문 Figure 2.4 를 손실 축과 시간 축의 사분면으로 다시 놓은 그림. 오른쪽 아래 칸에는 원문 표의 어떤 앱도 놓이지 않는다.",
      "손실을 견디는 앱은 전부 시간이 촉박한 앱입니다 — 시간이 있으면 다시 보내면 되기 때문입니다")

# 축 — 중심에서 네 방향으로
for x2, y2 in ((XR, CY), (XL, CY), (CX, YT), (CX, YB)):
    d.path(f"M {CX} {CY} L {x2} {y2}", MUTED, 1.2, m="ar")

# 축 라벨 — 끝점 바깥에 한 단어씩 (Geist Mono, 대문자, 자간)
def axlabel(x, y, txt, anchor):
    d.o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" '
               f'font-size="9" letter-spacing="0.18em" fill="{INK}">{txt}</text>')

axlabel(CX, YT - 14, "URGENT", "middle")
axlabel(CX, YB + 26, "RELAXED", "middle")
axlabel(XL - 14, CY + 4, "LOSSLESS", "end")
axlabel(XR + 14, CY + 4, "TOLERANT", "start")

# 항목 — (x, y, 이름, 곁줄, 초점 여부)
ITEMS = [
    (240, 374, "웹 문서", "탄력적", False),
    (368, 424, "전자 메일", "탄력적", False),
    (246, 462, "파일 전송·다운로드", "탄력적", False),
    (356, 252, "스마트폰 메시징", "원문 표기 — 예이면서 아니오", False),
    (700, 192, "인터넷 전화·화상회의", "수백 ms", True),
    (612, 244, "상호작용 게임", "수백 ms", False),
    (772, 266, "저장 비디오 스트리밍", "수 초", False),
]
for x, y, name, sub, focal in ITEMS:
    c = ACC if focal else MUTED
    d.o.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
    d.t(x, y - 14, name, 11, INK if focal else MUTED, KR, "middle", 600 if focal else 400)
    d.t(x, y + 20, sub, 11, SOFT, KR)

# 빈 사분면 — 이 도식의 요점
d.box(600, 380, 226, 84, PAPER2, RULE, 0.9)
d.t(713, 410, "여기에 놓이는 앱이 없습니다", 11, SOFT, KR)
d.t(713, 432, "손실은 견디는데 시간은 여유로운", 11, SOFT, KR)
d.t(713, 450, "조합이 원문 표에 없습니다", 11, SOFT, KR)

d.t(12, 556, "손실 불가 쪽은 전부 TCP 를 고릅니다. 손실 내성 쪽은 지연을 못 견뎌 UDP 를 고르지만, 방화벽이 UDP 를 막으면 TCP 를 예비로 둡니다.",
     11, MUTED, KR, "start")

d.legend(H - 76, [("UDP 를 부르는 자리", ACC), ("나머지", MUTED)])
d.save("02-01.app-requirements.svg")
