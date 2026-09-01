# 03-04 §2 — 저자의 비디오 스트리밍 예에서 네 팀이 무엇을 소유하는가 (원문 Figure 3-10 ~ 3-12).
# 팀 이름과 책임 문구는 원문 목록 그대로다. 뷰 구성은 원문 세 그림의 서술을 각주 띠로 옮겼다.
# 타입 스펙: type-org-chart — 노드가 팀이고 물어야 할 것이 "누가 무엇을 갖는가"다. accent 는 앞문 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1240
RW, RH, RY = 340, 84, 108
NW, NH, NY = 340, 100, 252
XS = (48, 450, 852)
BUS_Y = RY + RH + 32
FOOT_Y = NY + NH + 40
LEGEND_Y = FOOT_Y + 76
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-04 §2",
      "한 화면을 네 팀이 나눠 갖는다",
      "위가 셸과 디자인 시스템을 대는 팀이고 아래가 뷰에 조각을 얹는 세 팀이다. 색이 붙은 팀이 다른 조각을 조합하는 자리다.",
      "노드마다 팀 이름과 그 팀이 소유하는 것이 붙습니다")

# 연결선 먼저
d.line(W / 2, RY + RH, W / 2, BUS_Y, MUTED, 1.0)
d.line(XS[0] + NW / 2, BUS_Y, XS[2] + NW / 2, BUS_Y, MUTED, 1.0)
for x in XS:
    d.line(x + NW / 2, BUS_Y, x + NW / 2, NY, MUTED, 1.0)

# 앞문 — 셸을 대고 나머지를 조합한다
d.tone((W - RW) / 2, RY, RW, RH, ACC, 6, "14", 1.4)
d.t(W / 2, RY + 30, "파운데이션 팀", 14, ACC, KR, "middle", 600)
d.t(W / 2, RY + 50, "foundation", 9, ACC, MONO)
d.t(W / 2, RY + 70, "앱 셸 · 디자인 시스템 · 헤더 · 푸터", 10.5, MUTED, KR)

teams = [
    ("랜딩 페이지 팀", "landing page", ["마케팅을 지원해 서비스를 홍보한다", "랜딩 페이지들을 만든다"]),
    ("카탈로그 팀", "catalog", ["인증 영역과 주문형 비디오 소비", "카탈로그 뷰의 최종 결과를 책임진다"]),
    ("재생 경험 팀", "playback experience", ["비디오 플레이어 · 비디오 분석", "DRM 과 무단 시청 보안"]),
]
for x, (name, en, lines) in zip(XS, teams):
    d.box(x, NY, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 18, NY + 28, name, 13.5, INK, KR, "start", 600)
    d.t(x + 18, NY + 46, en, 9, MUTED, MONO, "start")
    for i, ln in enumerate(lines):
        d.t(x + 18, NY + 68 + i * 18, "· " + ln, 10, MUTED, KR, "start")

# 뷰 구성 각주 띠 — 조각이 아니라 조합 결과라서 노드로 세우지 않는다
d.box(48, FOOT_Y, W - 96, 60, f"{INK}05", RULE, 0.8, 6)
d.t(66, FOOT_Y + 24, "랜딩 뷰", 11, INK, KR, "start", 600)
d.t(150, FOOT_Y + 24, "파운데이션 + 랜딩 페이지 + 재생 경험 · 조각 사이 통신이 필요 없다", 10.5, MUTED, KR, "start")
d.t(66, FOOT_Y + 46, "카탈로그 뷰", 11, INK, KR, "start", 600)
d.t(150, FOOT_Y + 46, "파운데이션 + 카탈로그 + 재생 경험 · 선택한 비디오 ID 와 에러를 주고받아야 한다", 10.5, MUTED, KR, "start")

d.legend(LEGEND_Y, [("셸을 대고 나머지를 조합하는 팀", ACC)])
d.save("03-04.team-ownership.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
